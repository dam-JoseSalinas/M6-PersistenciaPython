#!/bin/usr/python3

"""
Backend llista de la compra.
Categoria modela una col·lecció d'articles rel·lacionats entre si.
"""
from ipersistencia_registre import IPersistencia_registre
from registre import Registre
from article import Article
import sqlite3
import logging

class Persistencia_registre_sqlite(IPersistencia_registre):
    def __init__(self, credencials):
        self._credencials = credencials
        self._conn = sqlite3.connect(
                credencials["path"]
                )
        if not self.check_table():
            self.create_table()

     
    def check_table(self):
        try:
            cursor = self._conn.cursor()
            cursor.execute("SELECT * FROM registres;")
            cursor.close()
        except sqlite3.Error:
            return False
        return True

    def create_table(self):
        cursor = self._conn.cursor()
        cursor.execute("""
                    Create table if not exists registres(
                      article int unique references articles(id),
                      quantitat int not null
                    )
                      """)
        cursor.close()
        self._conn.commit()

    def tots(self):
        cursor = self._conn.cursor()
        query = "select registres.rowid, articles.rowid, articles.nom, registres.quantitat from registres, articles where registres.article = articles.rowid;"
        cursor.execute(query)
        registres = cursor.fetchall()
        cursor.close()
        resultat = []
        for registre in registres:
            resultat.append(Registre(Article(registre[2], registre[1]), registre[3], registre[0])) 
        return resultat

    def desa(self, registre: Registre) -> Registre:
        cursor = self._conn.cursor()
        query = "insert into registres (article, quantitat) values(?, ?);"
        parameters = (registre.article.id, registre.quantitat)
        try:
            cursor.execute(query,parameters)
            logging.info(f"[Persistencia] Nou registre amb id = {cursor.lastrowid}.")
            self._conn.commit() 
        except sqlite3.Error:
            logging.info("[Persistencia] Integrity error escrivint registre.")
        return self.llegeix(registre.article.nom)
        
    def llegeix(self, nom: str) -> Registre:
        cursor = self._conn.cursor()
        query = "select registres.rowid, articles.rowid, articles.nom, registres.quantitat from registres, articles where registres.article = articles.rowid and articles.nom = ?;"
        parameters = (nom,)
        cursor.execute(query, parameters)
        registre = cursor.fetchone()
        cursor.close()
        if not registre is None:
            return Registre(Article(registre[2], registre[1]), registre[3], registre[0])
        return None

if __name__ == "__main__":
    from persistencia_article_sqlite import Persistencia_article_sqlite
    logging.basicConfig(filename='llista_compra.log', encoding='utf-8', level=logging.DEBUG)
    pa = Persistencia_article_sqlite({
        "path": "llista_compra.sqlite3"})
    pr = Persistencia_registre_sqlite({
        "path": "llista_compra.sqlite3"})
    a = Article("Arengades", pa)
    pa.desa(a)
    a = pa.llegeix('Arengades')
    r = Registre(a, 2)
    pr.desa(r)
    a = Article("Fabes", pa)
    pa.desa(a)
    a = pa.llegeix('Fabes')
    r = Registre(a, 1)
    pr.desa(r)
    print(pr.tots())

    