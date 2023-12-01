#!/bin/usr/python3

"""
Backend llista de la compra.
Article modela un element que es pot comprar.
"""
import logging
import json
from typing import List
import functools
from categoria import Categoria
from registre import Registre
from article import Article
from ipersistencia_registre import IPersistencia_registre
from ipersistencia_article import IPersistencia_article
from ipersistencia_categoria import IPersistencia_categoria

PATH_TO_DADES = "./dades.json"
class Llista():
    def __init__(self, persistencia_article: IPersistencia_article,persistencia_registre: IPersistencia_registre , persistencia_categoria: IPersistencia_categoria) -> None:
        self._registres = []
        self._categories = []
        self._persistencia_categoria = persistencia_categoria
        self._persistencia_article = persistencia_article
        self._persistencia_registre = persistencia_registre
        # self._categories.append(Categoria("Frescos"))
        # self._categories.append(Categoria("Begudes"))
        # self._categories.append(Categoria("Làctics"))
        # self._categories.append(Categoria("Neteja"))
        # self._categories.append(Categoria("Fruites i verdures"))
        self.llegeix_de_disc()
    
    @property
    def registres(self) -> List[Registre]:
        return self._nom

    @property
    def pesistencia_categoria(self) -> IPersistencia_categoria:
        return self._persistencia_categoria
    
    @property
    def pesistencia_article(self) -> IPersistencia_article:
        return self._persistencia_article
    
    @property
    def pesistencia_registre(self) -> IPersistencia_categoria:
        return self._persistencia_registre
    
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
        for categoria in self._categories:
            categoria.persistencia.desa(categoria)

    def llegeix_de_disc(self):
        # with open(PATH_TO_DADES) as dades:
        #     self.fromJSON(dades.read())
        self._categories = self._persistencia_categoria.totes()
        self._registres = self._persistencia_registre.tots()

    def read_categoria(self, nom: str) -> Categoria:
        seleccio = [x for x in self._categories if x.nom.lower() == nom.lower()]
        if len(seleccio) > 0:
            return seleccio[0]
        return None
    
    def update_categoria(self, categoria: Categoria) -> Categoria:
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

if __name__ == "__main__":
    logging.basicConfig(filename='llista_compra.log', encoding='utf-8', level=logging.DEBUG)
    from persistencia_registre_sqlite import Persistencia_registre_sqlite
    from persistencia_article_sqlite import Persistencia_article_sqlite
    from persistencia_categoria_sqlite import Persistencia_categoria_sqlite
    from persistencia_registre_mysql import Persistencia_registre_mysql
    from persistencia_article_mysql import Persistencia_article_mysql
    from persistencia_categoria_mysql import Persistencia_categoria_mysql
    # credencials = {"path": "llista_compra_prod.sqlite3"}
    # persistencia_article= Persistencia_article_sqlite(credencials) 
    # persistencia_registre= Persistencia_registre_sqlite(credencials) 
    # persistencia_categoria= Persistencia_categoria_sqlite(credencials) 

    credencials = {
        "host": "localhost",
        "user": "dam_app",
        "password": "1234",
        "database": "dam_m6"}
    persistencia_article= Persistencia_article_mysql(credencials) 
    persistencia_registre= Persistencia_registre_mysql(credencials) 
    persistencia_categoria= Persistencia_categoria_mysql(credencials) 
    llista = Llista(persistencia_article= persistencia_article,
    persistencia_registre= persistencia_registre, 
    persistencia_categoria=persistencia_categoria )
    print(llista)
    llista.create_categoria(Categoria("Frescos", persistencia_categoria))
    llista.create_categoria(Categoria("Begudes", persistencia_categoria))
    llista.create_categoria(Categoria("Làctics", persistencia_categoria))
    llista.create_categoria(Categoria("Neteja", persistencia_categoria))
    llista.create_categoria(Categoria("Fruites i verdures", persistencia_categoria))
    llista.desa_a_disc()
    print(llista)