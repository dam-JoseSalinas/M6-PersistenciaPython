#!/bin/usr/python3

"""
Backend llista de la compra.
Categoria modela una col·lecció d'articles rel·lacionats entre si.
"""

from ipersistencia_categoria import IPersistencia_categoria
from persistencia_article_mysql import Persistencia_article_mysql
from categoria import Categoria
from article import Article
from typing import List
import mysql.connector
import logging

class Persistencia_categoria_mysql(IPersistencia_categoria):
    def __init__(self, credencials):
        self._credencials = credencials
        self._conn = mysql.connector.connect(
                host=credencials["host"],
                user=credencials["user"],
                password=credencials["password"],
                database=credencials["database"]
                )
        if not self.check_table():
            self.create_table()

     
    def check_table(self):
        try:
            cursor = self._conn.cursor(buffered=True)
            cursor.execute("SELECT * FROM categories join articles_categoria on articles_categoria.categoria = categories.id;")
            cursor.reset()
        except mysql.connector.errors.ProgrammingError:
            return False
        return True

    def create_table(self):
        cursor = self._conn.cursor()
        cursor.execute("Drop table if exists articles_categoria;")
        cursor.execute("Drop table if exists categories;")
        cursor.execute("""
                    Create table if not exists categories(
                      id int not null auto_increment,
                      nom varchar(255) unique,
                      primary key (id)
                    )
                      """)
        cursor.execute("""
                    Create table if not exists articles_categoria(
                      id int not null auto_increment,
                      categoria int not null references categories(id),
                      article int not null references articles(id),
                      primary key (id)
                    )
                      """)
        self._conn.commit()

    
    def totes(self) -> List[Categoria]:
        cursor = self._conn.cursor(buffered=True)
        query = "select id, nom from categories;"
        cursor.execute(query)
        registres = cursor.fetchall()
        cursor.reset()
        resultat = []
        for registre in registres:
            categoria = Categoria(registre[1], self, registre[0])
            query = "select articles.id, articles.nom from articles_categoria join articles on articles_categoria.article = articles.id where articles_categoria.categoria = %s;"
            parametres = (categoria.id,)
            cursor.execute(query, parametres)
            articles = cursor.fetchall()
            for article in articles:
                categoria.add_article(Article(article[1], Persistencia_article_mysql(self._credencials), article[0]))
            resultat.append(categoria)
        return resultat
    
    def desa(self, categoria: Categoria) -> Categoria:
        cursor = self._conn.cursor()
        query = "insert into categories (nom) values(%s);"
        parameters = (categoria.nom, )
        try:
            cursor.execute(query,parameters)
            nova_id = cursor.lastrowid
            logging.info(f"[Persistencia] Nova categoria amb id = {nova_id}.")
            for article in categoria.articles:
                if article.id is None:
                    article = article.persistencia.desa(article)
                query = "insert into articles_categoria (categoria, article) values(%s,%s);"
                parametres = (nova_id, article.id)
                cursor.execute(query, parametres)
            self._conn.commit() 
        except mysql.connector.errors.IntegrityError:
            logging.info("[Persistencia] Integrity error escrivint categoria.")
        return self.llegeix(categoria.nom)

    def llegeix(self, nom: str) -> Categoria:
        cursor = self._conn.cursor(buffered=True)
        query = "select id, nom from categories where categories.nom = %s;"
        parametres = (nom,)
        cursor.execute(query, parametres)
        registre = cursor.fetchone()
        cursor.reset()
        if registre is None:
            logging.info(f"[Persistencia] Categoria inexistent {nom}.")
            return None
        resultat = Categoria(nom, self, cursor.lastrowid)
        logging.info(f"[Persistencia] Trobada categoria {nom}.")
        query = "select articles.id, articles.nom from articles_categoria join articles on articles_categoria.article = articles.id where articles_categoria.categoria = %s;"
        parametres = (resultat.id,)
        cursor.execute(query, parametres)
        articles = cursor.fetchall()
        for article in articles:
            resultat.add_article(Article(article[1], Persistencia_article_mysql(self._credencials), article[0]))
        return resultat

if __name__ == "__main__":
    logging.basicConfig(filename='llista_compra.log', encoding='utf-8', level=logging.DEBUG)
    credencials = {
        "host": "localhost",
        "user": "dam_app",
        "password": "1234",
        "database": "dam_m6"}
    pc = Persistencia_categoria_mysql(credencials)
    c = Categoria("CatProva", pc)
    pa = Persistencia_article_mysql(credencials)
    c.add_article(Article("Article prova 01", pa))
    c.add_article(Article("Article prova 02", pa))
    c.persistencia.desa(c)
    c = Categoria("CatProva_02", pc)
    pa = Persistencia_article_mysql(credencials)
    c.add_article(Article("Article prova 03", pa))
    c.add_article(Article("Article prova 04", pa))
    c.persistencia.desa(c)
    print(pc.totes())