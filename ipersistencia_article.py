#!/bin/usr/python3

"""
Backend llista de la compra.
Categoria modela una col·lecció d'articles rel·lacionats entre si.
"""

from abc import ABC, abstractclassmethod
from article import Article
from typing import List

class IPersistencia_article(ABC):
    @abstractclassmethod
    def tots(self) -> List[Article]:
        pass

    @abstractclassmethod
    def desa(self, article: Article) -> Article:
        pass

    @abstractclassmethod
    def llegeix(self, nom: str) -> Article:
        pass

