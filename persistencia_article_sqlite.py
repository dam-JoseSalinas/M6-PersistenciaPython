#!/bin/usr/python3

"""
Persistencia_article_sqlite3
"""
from ipersistencia_article import IPersistencia_article
from article import Article
import sqlite3
import logging

class Persistencia_article_sqlite(IPersistencia_article):
    def __init__(self, sqlite_path):
        self._conn = sqlite3.connect(sqlite_path)
        
        if not self.check_table():
            logging.debug("[Persistencia article] Creant taula d'articles.")
            self.create_table()

     
    def check_table(self):
        try:
            #buffered = lambda cur: (cur, cur.fetchone())
            #cursor, buffer = self._conn.cursor().buffered()
            cursor = self._conn.cursor()
            cursor.execute("SELECT * FROM articles;")
            #cursor = reset = None
        except sqlite3.OperationalError:
            return False
        return True


    def create_table(self):
        cursor = self._conn.cursor()
        cursor.execute("""
                    Create table if not exists articles(
                      id integer not null primary key autoincrement,
                      nom varchar(255) unique
                    )
                      """)
        self._conn.commit()

    def tots(self):
        pass
    
    def desa(self, article: Article) -> Article:
        cursor = self._conn.cursor()
        query = "insert into articles (nom) values(?);"
        parameters = (article.nom,)
        try:
            cursor.execute(query, parameters)
            logging.info(f"[Persistencia] Nou article amb id = {cursor.lastrowid}.")
            self._conn.commit()
        except sqlite3.IntegrityError:
            logging.info("[Persistencia] Intent de tornar a escriure un article existent.")
        return self.llegeix(article.nom)
        
    def llegeix(self, nom: str) -> Article:
        cursor = self._conn.cursor()
        query = "select id, nom from articles where nom = ?;"
        parameters = (nom,)
        cursor.execute(query, parameters)
        registre = cursor.fetchone()
        #cursor = reset = None
        if not registre is None:
            return Article(nom=registre[1], persistencia=self, id=registre[0])
        return None

if __name__ == "__main__":
    logging.basicConfig(filename='llista_compra.log', encoding='utf-8', level=logging.DEBUG)
    p = Persistencia_article_sqlite("articles.db")
    a = Article("patates", p)
    a = a.persistencia.desa(a)
    print(a.persistencia.llegeix(a.nom))
    print(p.llegeix('sucre'))
    
