#!/bin/usr/python3

"""
Backend llista de la compra.
Categoria modela una col·lecció d'articles rel·lacionats entre si.
"""

from abc import ABC, abstractclassmethod
from categoria import Categoria
from article import Article
from typing import List

class IPersistencia_categoria(ABC):
    @abstractclassmethod
    def totes(self) -> List[Categoria]:
        pass
    
    @abstractclassmethod
    def desa(self, categoria: Categoria) -> Categoria:
        pass

    @abstractclassmethod
    def llegeix(self, nom: str) -> Categoria:
        pass

