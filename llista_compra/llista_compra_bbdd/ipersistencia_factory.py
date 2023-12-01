#!/usr/bin/python3
# -*- coding: utf-8 -*-

import abc

"""
    IPersistencia_factory.py
    Classe abstracta que defineix la interficie amb les fàbriques concretes de persistència.
"""

class IPersistencia_factory(abc.ABC):
    @abc.abstractmethod
    def get_Persistencia_factory_article(self):
        pass

    @abc.abstractmethod
    def get_Persistencia_factory_registre(self):
        pass

    @abc.abstractmethod
    def get_Persistencia_factory_categoria(self):
        pass

