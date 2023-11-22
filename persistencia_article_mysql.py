#!/bin/usr/python3

"""
Backend llista de la compra.
Categoria modela una col·lecció d'articles rel·lacionats entre si.
"""
from ipersistencia_article import IPersistencia_article
from article import Article
import mysql.connector
import logging

class Persistencia_article_mysql(IPersistencia_article):
    def __init__(self, credencials):
        self._credencials = credencials
        self._conn = mysql.connector.connect(
                host=credencials["host"],
                user=credencials["user"],
                password=credencials["password"],
                database=credencials["database"]
                )
        if not self.check_table():
            logging.debug("[Persistencia article] Creant taula d'articles.")
            self.create_table()

     
    def check_table(self):
        try:
            cursor = self._conn.cursor(buffered=True)
            cursor.execute("SELECT * FROM articles;")
            cursor.reset()
        except mysql.connector.errors.ProgrammingError:
            return False
        return True

    def create_table(self):
        cursor = self._conn.cursor()
        cursor.execute("""
                    Create table if not exists articles(
                      id int not null auto_increment,
                      nom varchar(255) unique,
                      primary key (id)
                    )
                      """)
        self._conn.commit()

    def tots(self):
        pass
    
    def desa(self, article: Article) -> Article:
        cursor = self._conn.cursor()
        query = "insert into articles (nom) values(%s);"
        parameters = (article.nom,)
        try:
            cursor.execute(query,parameters)
            logging.info(f"[Persistencia] Nou article amb id = {cursor.lastrowid}.")
            self._conn.commit() 
        except mysql.connector.errors.IntegrityError:
            logging.info("[Persistencia] Intent de tornar a escriure un article existent.")
        return self.llegeix(article.nom)
        
    def llegeix(self, nom: str) -> Article:
        cursor = self._conn.cursor(buffered=True)
        query = "select id, nom from articles where nom = %s;"
        parameters = (nom,)
        cursor.execute(query, parameters)
        registre = cursor.fetchone()
        cursor.reset()
        if not registre is None:
            return Article(registre[1], self,registre[0])
        return None

if __name__ == "__main__":
    logging.basicConfig(filename='llista_compra.log', encoding='utf-8', level=logging.DEBUG)
    p = Persistencia_article_mysql({
        "host": "localhost",
        "user": "dam_app",
        "password": "1234",
        "database": "dam_m6"})
    a = Article("patates", p)
    a = a.persistencia.desa(a)
    print(a.persistencia.llegeix(a.nom))
    print(p.llegeix('sucre'))
    