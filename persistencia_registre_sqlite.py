#!/bin/usr/python3

"""
Backend llista de la compra.
Categoria modela una col·lecció d'articles rel·lacionats entre si.
"""
from ipersistencia_registre import IPersistencia_registre
from registre import Registre
from article import Article
import mysql.connector
import logging

class Persistencia_registre(IPersistencia_registre):
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
            cursor.execute("SELECT * FROM registres;")
            cursor.reset()
        except mysql.connector.errors.ProgrammingError:
            return False
        return True

    def create_table(self):
        cursor = self._conn.cursor()
        cursor.execute("""
                    Create table if not exists registres(
                      id int not null auto_increment,
                      article int unique references articles(id),
                      quantitat int not null,
                      primary key (id)
                    )
                      """)
        self._conn.commit()

    def tots(self):
        cursor = self._conn.cursor(buffered=True)
        query = "select registres.id, articles.id, articles.nom, registres.quantitat from registres, articles where registres.article = articles.id;"
        cursor.execute(query)
        registres = cursor.fetchall()
        cursor.reset()
        resultat = []
        for registre in registres:
            resultat.append(Registre(Article(registre[2], registre[1]), registre[3], registre[0])) 
        return resultat

    def desa(self, registre: Registre) -> Registre:
        cursor = self._conn.cursor()
        query = "insert into registres (article, quantitat) values(%s, %s);"
        parameters = (registre.article.id, registre.quantitat)
        try:
            cursor.execute(query,parameters)
            logging.info(f"[Persistencia] Nou registre amb id = {cursor.lastrowid}.")
            self._conn.commit() 
        except mysql.connector.errors.IntegrityError:
            logging.info("[Persistencia] Integrity error escrivint registre.")
        return self.llegeix(registre.article.nom)
        
    def llegeix(self, nom: str) -> Registre:
        cursor = self._conn.cursor(buffered=True)
        query = "select registres.id, articles.id, articles.nom, registres.quantitat from registres, articles where registres.article = articles.id and articles.nom = %s;"
        parameters = (nom,)
        cursor.execute(query, parameters)
        registre = cursor.fetchone()
        cursor.reset()
        if not registre is None:
            return Registre(Article(registre[2], registre[1]), registre[3], registre[0])
        return None

if __name__ == "__main__":
    from persistencia_article_mysql import Persistencia_article_mysql
    logging.basicConfig(filename='llista_compra.log', encoding='utf-8', level=logging.DEBUG)
    pa = Persistencia_article_mysql({
        "host": "localhost",
        "user": "dam_app",
        "password": "1234",
        "database": "dam_m6"})
    pr = Persistencia_registre({
        "host": "localhost",
        "user": "dam_app",
        "password": "1234",
        "database": "dam_m6"})
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

    