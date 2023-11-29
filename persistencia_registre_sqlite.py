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

class Persistencia_registre(IPersistencia_registre):
    def __init__(self, sqlite_path):
        self.sqlite_path = sqlite_path
        self._conn = sqlite3.connect(sqlite_path)
        if not self.check_table():
            self.create_table()

     
    def check_table(self):
        try:
            cursor = self._conn.cursor()
            cursor.execute("SELECT * FROM registres;")
            #cursor.reset()
        except sqlite3.OperationalError:
            return False
        return True

    def create_table(self):
        cursor = self._conn.cursor()
        cursor.execute("""
                    Create table if not exists registres(
                      id integer not null primary key autoincrement,
                      article integer unique,
                      quantitat integer not null,
                      foreign key(article) references articles(id)
                    )
                      """)
        self._conn.commit()

    def tots(self):
        cursor = self._conn.cursor() #buffered
        query = """select registres.id, articles.id, articles.nom, registres.quantitat 
                from registres, articles 
                where registres.article = articles.id;"""
        cursor.execute(query)
        registres = cursor.fetchall()
        #reset
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
        except sqlite3.IntegrityError:
            logging.info("[Persistencia] Integrity error escrivint registre.")
        return self.llegeix(registre.article.nom)
        
    def llegeix(self, nom: str) -> Registre:
        cursor = self._conn.cursor() #bufered
        query = "select registres.id, articles.id, articles.nom, registres.quantitat from registres, articles where registres.article = articles.id and articles.nom = ?;"
        parameters = (nom,)
        cursor.execute(query, parameters)
        registre = cursor.fetchone()
        #cursor.reset()
        if not registre is None:
            return Registre(Article(registre[2], registre[1]), registre[3], registre[0])
        return None

if __name__ == "__main__":
    from persistencia_article_sqlite import Persistencia_article_sqlite
    logging.basicConfig(filename='llista_compra.log', encoding='utf-8', level=logging.DEBUG)
    pa = Persistencia_article_sqlite("registres.db")
    pr = Persistencia_registre("registres.db")
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

    