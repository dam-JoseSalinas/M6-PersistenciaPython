#!/bin/usr/python3

"""
Backend llista de la compra.
Categoria modela una col·lecció d'articles rel·lacionats entre si.
"""
from ipersistencia_article import IPersistencia_article
from article import Article
import sqlite3
import logging

class Persistencia_article_sqlite(IPersistencia_article):
    def __init__(self, credencials):
        self._credencials = credencials
        self._conn = sqlite3.connect(
                credencials["path"]
                )
        if not self.check_table():
            logging.debug("[Persistencia article] Creant taula d'articles.")
            self.create_table()

     
    def check_table(self):
        try:
            cursor = self._conn.cursor()
            cursor.execute("SELECT * FROM articles;")
            cursor.close()
        except sqlite3.Error:
            return False
        return True

    def create_table(self):
        cursor = self._conn.cursor()
        cursor.execute("""
                    Create table if not exists articles(
                      nom text unique
                    )
                      """)
        self._conn.commit()

    def tots(self):
        raise (NotImplementedError("persistencia_article_sqlite.tots()"))
    
    def desa(self, article: Article) -> Article:
        cursor = self._conn.cursor()
        query = "insert into articles (nom) values(?);"
        parameters = (article.nom,)
        try:
            cursor.execute(query,parameters)
            logging.info(f"[Persistencia] Nou article amb id = {cursor.lastrowid}.")
            cursor.close()
            self._conn.commit() 
        except sqlite3.Error as e:
            logging.info(f"[Persistencia] Intent de tornar a escriure un article existent.     [{str(e)}]")
        return self.llegeix(article.nom)
        
    def llegeix(self, nom: str) -> Article:
        cursor = self._conn.cursor()
        query = "select rowid, nom from articles where nom = ?;"
        parameters = (nom,)
        cursor.execute(query, parameters)
        registre = cursor.fetchone()
        cursor.close()
        if not registre is None:
            return Article(registre[1], self,registre[0])
        return None

if __name__ == "__main__":
    logging.basicConfig(filename='llista_compra.log', encoding='utf-8', level=logging.DEBUG)
    p = Persistencia_article_sqlite({
        "path": "llista_compra.sqlite3"})
    a = Article("patates", p)
    a = a.persistencia.desa(a)
    print(a.persistencia.llegeix(a.nom))
    print(p.llegeix('sucre'))
    