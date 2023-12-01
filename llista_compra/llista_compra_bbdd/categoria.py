#!/bin/usr/python3

"""
Backend llista de la compra.
Categoria modela una col·lecció d'articles rel·lacionats entre si.
"""

from article import Article
from typing import List
import functools, json

class Categoria():
    def __init__(self, nom: str, persistencia, id=None) -> None:
        self._nom = nom
        self._articles = []
        self._id = id
        self._persistencia = persistencia
    
    @property
    def nom(self) -> str:
        return self._nom
    
    @nom.setter
    def nom(self, valor: str) -> None:
        self._nom = valor
    
    @property
    def id(self):
        return self._id
    
    @property
    def persistencia(self):
        return self._persistencia
    
    @property
    def articles(self) -> List[Article]:
        return self._articles
        
    def add_article(self, article: Article) -> Article:
        existeix = False
        if len(self._articles) > 0:
            comparacio = list(map(lambda element : article.nom != element.nom, self._articles))
            existeix = not functools.reduce(lambda a,b: a and b, comparacio)
        if not existeix:
            self._articles.append(article)
            return article
        return None
    
    def delete_article(self, nom_article: str) -> None:
        article = list(filter(lambda a: nom_article == a.nom, self._articles))
        if len(article) > 0:
            self._articles.remove(article[0])
        return 

    def toJSON(self):
        registres_json = list(map(lambda a: json.loads(a.toJSON()), self._articles))
        return json.dumps({"nom": self._nom, "articles": registres_json})
    
    def __repr__(self):
        return self.toJSON()
