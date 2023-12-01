#!/bin/usr/python3

"""
Backend llista de la compra.
Article modela un element que es pot comprar.
"""
import json
from typing import AnyStr
class Article():
    def __init__(self, nom: str, persistencia,id=None) -> None:
        self._nom = nom
        self._persistencia = persistencia
        self._id = id
    
    @property
    def nom(self) -> str:
        return self._nom
    
    @nom.setter
    def nom(self, valor: str):
        self._nom = valor

    @property
    def persistencia(self):
        return self._persistencia
    
    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, valor: int):
        self._id = valor

    def __repr__(self):
        return self.toJSON()
    
    def toJSON(self):
        return json.dumps({"id": self.id, "nom": self.nom})
