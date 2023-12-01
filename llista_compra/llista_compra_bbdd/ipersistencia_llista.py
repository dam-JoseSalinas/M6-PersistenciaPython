#!/bin/usr/python3

"""
Backend llista de la compra.
Categoria modela una col·lecció d'articles rel·lacionats entre si.
"""

from abc import ABC, abstractclassmethod
from llista import Llista
from typing import List

class IPersistencia_llista(ABC):
    @abstractclassmethod
    def desa(self, llista: Llista):
        pass

    @abstractclassmethod
    def llegeix(self) -> Llista:
        pass

