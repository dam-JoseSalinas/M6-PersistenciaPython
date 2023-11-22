#!/bin/usr/python3

"""
Backend llista de la compra.
Article modela un element que es pot comprar.
"""
from article import Article
import json

class Registre():
    def __init__(self, article: Article, quantitat: int, id=None) -> None:
        self._article = article
        self._quantitat = quantitat
        self._id = id
    
    @property
    def article(self) -> Article:
        return self._article
    
    @property
    def quantitat(self) -> int:
        return self._quantitat
    
    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, valor: int):
        self._id = valor

    @quantitat.setter
    def quantitat(self, valor: int):
        self._quantitat = valor

    def __repr__(self):
        return self.toJSON()
    
    def toJSON(self):
        return json.dumps({"article": json.loads(self._article.toJSON()), "quantitat": self._quantitat, "id": self._id})

