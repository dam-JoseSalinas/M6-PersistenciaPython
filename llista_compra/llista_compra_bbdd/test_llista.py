#!/bin/usr/python3

"""
Test llista de la compra
"""

from llista import Llista
from registre import Registre
from categoria import Categoria
from article import Article

import json

def main():
    cat_predefinides = ["Frescos", "Làctics", "Fruites i verdures", "Begudes", "Neteja"]
    l = Llista()
    for nom_categoria_predefinida in cat_predefinides:
        cat = l.read_categoria(nom_categoria_predefinida)
        if cat.nom.lower() != nom_categoria_predefinida.lower():
            print(f"[X] Error: no he trobat la categoria {nom_categoria_predefinida} ")
        else:
            print(".", end="")
    cat_proves = Categoria("Proves")
    article_proves = Article("Un article")
    cat_proves.add_article(article_proves)
    cat_proves.add_article(Article("Per esborrar!!!"))
    cat_proves.delete_article("Per esborrar!!!")
    l.create_categoria(cat_proves)
    print(".", end="")
    cat = l.read_categoria("Proves")
    if cat.nom == "Proves":
        print(".", end="")
    else:
        print("[X] Error al llegir la nova categoria")
    l.create_registre(Registre(article_proves, 5))
    if len(l.get_registres()) > 0:
        print(".", end="")
    else:
        print("[X] Error al llegir la llista de registres.")
    reg = l.read_registre("Un article")
    if type(Registre(Article(article_proves), 1)) != type(reg):
        print("[X] Error al llegir la llista de registres.")
    else:
        print(".", end="")
    if reg.quantitat == 5:
        print(".", end="")
    else:
        print("[X] Error al llegir article")
    l.update_registre(Registre(Article("Un article"), 3))
    reg = l.read_registre("Un article")
    if reg.quantitat == 3:
        print(".", end="")
    else:
        print("[X] Error al actualitzar article")
    l.delete_categoria("Proves")
    cat = l.read_categoria("Proves")
    if cat:
        print("[X] Error al esborrar categoria")
    else:
        print(".", end="")
    print()
    l.desa_a_disc()
    print(l)
    l.llegeix_de_disc()
    print(l)
    l.delete_registre(article_proves.nom)
    l.desa_a_disc()
    print()
if __name__ == "__main__":
    main()