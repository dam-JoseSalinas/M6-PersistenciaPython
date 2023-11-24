#!/bin/usr/python3

"""
Backend llista de la compra.
Categoria modela una col·lecció d'articles rel·lacionats entre si.
"""

from ipersistencia_categoria import IPersistencia_categoria
from persistencia_article_sqlite import Persistencia_article_sqlite
from categoria import Categoria
from article import Article
from typing import List
import sqlite3
import logging

class Persistencia_categoria_sqlite(IPersistencia_categoria):
    def __init__(self, sqlite_path):
        self.sqlite_path = sqlite_path
        self._conn = sqlite3.connect(sqlite_path)
        if not self.check_table():
            self.create_table()

     
    def check_table(self):
        try:
            cursor = self._conn.cursor() #bufered
            cursor.execute("SELECT * FROM categories join articles_categoria on articles_categoria.categoria = categories.id;")
            #cursor = reset = None
        except sqlite3.OperationalError:
            return False
        return True

    def create_table(self):
        cursor = self._conn.cursor()
        cursor.execute("Drop table if exists articles_categoria;")
        cursor.execute("Drop table if exists categories;")
        cursor.execute("""
                    Create table if not exists categories(
                      id integer not null primary key autoincrement,
                      nom varchar(255) unique
                    )
                      """)
        cursor.execute("""
                    Create table if not exists articles_categoria(
                      id integer not null primary key autoincrement,
                      categoria integer not null,
                      article integer not null,
                      foreign key(categoria) references categories(id),
                      foreign key(article) references articles(id)
                    )
                      """)
        self._conn.commit()

    
    def totes(self) -> List[Categoria]:
        cursor = self._conn.cursor()
        query = "select id, nom from categories;"
        cursor.execute(query) #bufered
        registres = cursor.fetchall()
        #reset
        resultat = []
        for registre in registres:
            categoria = Categoria(persistencia=self, id=registre[0], nom=registre[1])
            query = """select a.id, a.nom 
                       from articles_categoria ac
                       join articles a
                       on ac.article = a.id 
                       where ac.categoria = ?;"""
            parametres = (categoria.id,)
            cursor.execute(query, parametres) ####################
            articles = cursor.fetchall()
            for article in articles:
                categoria.add_article(article=Article(
                                            nom = article[1], #nom = article[1]
                                            persistencia = Persistencia_article_sqlite(self.sqlite_path),
                                            id = article[0])) 
            resultat.append(categoria)
        return resultat
    
    def desa(self, categoria: Categoria) -> Categoria:
        cursor = self._conn.cursor()
        query = "insert into categories (nom) values(?);"
        parameters = (categoria.nom, )
        try:
            cursor.execute(query,parameters)
            self._conn.commit() ###################
            nova_id = cursor.lastrowid
            logging.info(f"[Persistencia] Nova categoria {categoria.nom} amb id = {nova_id}.")
            for article in categoria.articles:
                if article.id is None:
                    article = article.persistencia.desa(article)
                query = """insert into articles_categoria(
                            categoria, article) values(?,?);"""
                parametres = (nova_id, article.id)
                cursor.execute(query, parametres) #######
                self._conn.commit()
            self._conn.commit() 
        except sqlite3.IntegrityError:
            logging.info("[Persistencia] Integrity error escrivint categoria.")
        return self.llegeix(categoria.nom)

    def llegeix(self, nom: str) -> Categoria:
        cursor = self._conn.cursor() #bufered
        query = "select id, nom from categories where categories.nom = ?;" ##
        parametres = (nom,)
        cursor.execute(query, parametres)
        registre = cursor.fetchone()
        #reset
        if registre is None:
            logging.info(f"[Persistencia] Categoria inexistent {nom}.")
            return None
        resultat = Categoria(nom, self, cursor.lastrowid)
        logging.info(f"[Persistencia] Trobada categoria {nom}.")
        query = """select articles.id, articles.nom 
                from articles_categoria 
                join articles 
                on articles_categoria.article = articles.id 
                where articles_categoria.categoria = ?;""" 
        parametres = (resultat.id,)
        cursor.execute(query, parametres) ####
        articles = cursor.fetchall()
        for article in articles:
            resultat.add_article(article=Article(
                                    nom = article[1], 
                                    persistencia = Persistencia_article_sqlite(self.sqlite_path),
                                    id = article[0]))
        return resultat

if __name__ == "__main__":
    logging.basicConfig(filename='llista_compra.log', encoding='utf-8', level=logging.DEBUG)
    sqlite_file = "bd1.db"
    pc = Persistencia_categoria_sqlite(sqlite_path=sqlite_file)
    
    c = Categoria("CatProva", pc)
    
    pa = Persistencia_article_sqlite(sqlite_path=sqlite_file)
    c.add_article(Article("Article prova 01", pa))
    c.add_article(Article("Article prova 02", pa))
    c.persistencia.desa(c)
    c = Categoria("CatProva_02", pc)
    pa = Persistencia_article_sqlite(sqlite_path=sqlite_file)
    c.add_article(Article("Article prova 03", pa))
    c.add_article(Article("Article prova 04", pa))
    c.persistencia.desa(c)
    print(pc.totes())