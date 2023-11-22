#!/bin/usr/python3

"""
Backend llista de la compra.
Article modela un element que es pot comprar.
"""
import json
from typing import List
import functools
from categoria import Categoria
from registre import Registre
from article import Article

PATH_TO_DADES = "./dades.json"
class Llista():
    def __init__(self) -> None:
        self._registres = []
        self._categories = []
        # self._categories.append(Categoria("Frescos"))
        # self._categories.append(Categoria("Begudes"))
        # self._categories.append(Categoria("Làctics"))
        # self._categories.append(Categoria("Neteja"))
        # self._categories.append(Categoria("Fruites i verdures"))
        self.llegeix_de_disc()
    
    @property
    def registres(self) -> List[Registre]:
        return self._nom

    def create_registre(self, registre: Registre) -> Registre:
        existeix = any(map(lambda element : registre.article.nom == element.article.nom, self._registres))
        if not existeix:
            self._registres.append(registre)
            return registre
        return None
    
    def get_registres(self) -> List[Registre]:
        return self._registres
    
    def read_registre(self, nom: str) -> Registre:
        seleccio = [x for x in self._registres if x.article.nom.lower() == nom.lower()]
        if len(seleccio) > 0:
            return seleccio[0]
        return None
    
    def update_registre(self, registre: Registre) -> Registre:
        for index, element in enumerate(self._registres):
            if element.article.nom.lower() == registre.article.nom.lower():
                self._registres[index] = registre
                return registre
        return None
    
    def delete_registre(self, nom_article: str) -> None:
        for index, element in enumerate(self._registres):
            if element.article.nom.lower() == nom_article.lower():
                self._registres.remove(element)
                return None
        return None
    
    def create_categoria(self, categoria) -> Categoria:
        existeix = any(map(lambda element: categoria.nom == element.nom, self._categories))
        if not existeix:
            self._categories.append(categoria)
            return categoria
        return None
    
    def __repr__(self):
        return self.toJSON()
    
    def toJSON(self):
        registres_dict, categories_dict = [], []
        for registre in self._registres:
            registres_dict.append(json.loads(registre.toJSON()))
        for categoria in self._categories:
            categories_dict.append(json.loads(categoria.toJSON()))
        self_dict = {
            "registres": registres_dict,
            "categories": categories_dict
            }   
        return json.dumps(self_dict)

    def fromJSON(self, serialitzat):
        categories_dict = json.loads(serialitzat)["categories"]
        registres_dict = json.loads(serialitzat)["registres"]
        self._categories, self._registres = [], []
        for categoria in categories_dict:
            self.create_categoria(Categoria(categoria["nom"]))
        for registre in registres_dict:
            self.create_registre(Registre(Article(registre["article"]["_nom"]), registre["quantitat"]))
    
    def desa_a_disc(self):
        with open(PATH_TO_DADES, "w") as dades:
            dades.write(self.toJSON())

    def llegeix_de_disc(self):
        with open(PATH_TO_DADES) as dades:
            self.fromJSON(dades.read())

    def read_categoria(self, nom: str) -> Categoria:
        seleccio = [x for x in self._categories if x.nom.lower() == nom.lower()]
        if len(seleccio) > 0:
            return seleccio[0]
        return None
    
    def update_categoria(self, categoria: Categoria) -> Categoria:
        # for element in self._categories:
        #     if element.nom.lower() == categoria.nom.lower():
        #         element = categoria
        #         return categoria
        # return None
        for index, element in enumerate(self._categories):
            if element.nom.lower() == categoria.nom.lower():
                self._categories[index] = categoria
                return categoria
        return None
    
    def delete_categoria(self, nom_categoria: str) -> None:
        for index, element in enumerate(self._categories):
            if element.nom.lower() == nom_categoria.lower():
                self._categories.remove(element)
                return None
        return None
