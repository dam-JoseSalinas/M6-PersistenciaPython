#!/bin/usr/python3

"""
Backend llista de la compra.
Categoria modela una col·lecció d'articles rel·lacionats entre si.
"""

from abc import ABC, abstractclassmethod
from article import Article
from registre import Registre
from typing import List

class IPersistencia_registre(ABC):
    @abstractclassmethod
    def tots(self) -> List[Registre]:
        pass
    
    @abstractclassmethod
    def desa(self, registre: Registre) -> Registre:
        pass

    @abstractclassmethod
    def llegeix(self, nom: str) -> Registre:
        pass

