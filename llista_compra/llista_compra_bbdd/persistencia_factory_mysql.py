#!/usr/bin/python3
# -*- coding: utf-8 -*-
from ipersistencia_factory import IPersistencia_factory
from persistencia_registre_mysql import Persistencia_article_mysql
from persistencia_registre_mysql import Persistencia_registre_mysql
from persistencia_categoria_mysql import Persistencia_categoria_mysql

"""
    Persistencia_factory.py
    Classe abstracta que defineix la interficie amb les fàbriques concretes de persistència.
"""

class Persistencia_factory_mysql(IPersistencia_factory):
    def __init__(self, credencials):
        self._credencials = credencials

    def get_Persistencia_factory_article(self):
        return Persistencia_article_mysql(self._credencials)

    def get_Persistencia_factory_registre(self):
        return Persistencia_registre_mysql(self._credencials)

    def get_Persistencia_factory_categoria(self):
        return Persistencia_categoria_mysql(self._credencials)

