#!/usr/bin/python3

"""
app_llista_compra.py: app que t'ajuda a organitzar la teva
  llista de la compra al súper.
"""
import os, time, yaml, sys, json
from llista import Llista
from persistencia_registre_mysql import Persistencia_registre_mysql
from persistencia_registre_sqlite import Persistencia_registre_sqlite
from persistencia_article_mysql import Persistencia_article_mysql
from persistencia_article_sqlite import Persistencia_article_sqlite
from persistencia_categoria_mysql import Persistencia_categoria_mysql
from persistencia_categoria_sqlite import Persistencia_categoria_sqlite
from article import Article
from categoria import Categoria
from registre import Registre

THIS_PATH = os.path.dirname(os.path.abspath(__file__))
RUTA_FITXER_CONFIGURACIO = os.path.join(THIS_PATH, 'configuracio_sqlite.yml') 
print(RUTA_FITXER_CONFIGURACIO)


def get_configuracio(ruta_fitxer_configuracio) -> dict:
    config = {}
    with open(ruta_fitxer_configuracio, 'r') as conf:
        config = yaml.safe_load(conf)
    return config


def get_persistencies(conf: dict) -> dict:
    credencials = {}
    if conf["base de dades"]["motor"].lower().strip() == "mysql":
        credencials['host'] = conf["base de dades"]["host"]
        credencials['user'] = conf["base de dades"]["user"]
        credencials['password'] = conf["base de dades"]["password"]
        credencials['database'] = conf["base de dades"]["database"]
        return {
            'article': Persistencia_article_mysql(credencials),
            'registre': Persistencia_registre_mysql(credencials),
            'categoria': Persistencia_categoria_mysql(credencials)
        }
    elif conf["base de dades"]["motor"].lower().strip() == "sqlite":
        credencials['path'] = conf["base de dades"]["path"]
        return {
            'article': Persistencia_article_sqlite(credencials),
            'registre': Persistencia_registre_sqlite(credencials),
            'categoria': Persistencia_categoria_sqlite(credencials)
        }


def mostra_lent(missatge, v=0.05):
    for c in missatge:
        print(c, end='')
        sys.stdout.flush()
        time.sleep(v)
    print()


def landing_text():
    os.system('clear')
    print("Benvingut a la app de la llista de la compra.")
    time.sleep(1)
    msg = "Dessitjo que et sigui d'utilitat!"
    mostra_lent(msg, 0.01)
    input("Prem la tecla 'Enter' per a continuar")
    


def mostra_llista(llista):
    os.system('clear')
    mostra_lent(json.dumps(json.loads(llista.toJSON()), indent=4), v=0.01)
    input("prem enter per continuar")


def afegeix_article(llista):
    os.system('clear')
    pa = llista._persistencia_article
    nom = input("nom de l'article: ")
    a = Article(nom=nom, persistencia=pa)
    article_afegit = a.persistencia.desa(a)
    mostra_lent("Article afegit:", v=0.01)
    mostra_lent(article_afegit.toJSON(), v=0.01)
    input("prem enter per continuar")


def afegeix_categoria(llista):
    os.system('clear')
    pc = llista._persistencia_categoria
    pa = llista._persistencia_article
    nom = input("nom de la categoria: ")
    c = Categoria(nom=nom, persistencia=pc)
    opcio = None
    while opcio != "n":
        opcio = input("Crear un nou article dins la categoria? [s/n]: ")
        if opcio == "s":
            nom_a = input("nom de l'article: ")
            c.add_article(Article(nom=nom_a, persistencia=pa))
    categoria_afegida = c.persistencia.desa(c)
    mostra_lent("Categoria afegida:", v=0.01)
    mostra_lent(categoria_afegida.toJSON(), v=0.01)
    input("prem enter per continuar")


def afegeix_registre(llista):
    os.system('clear')
    pr = llista._persistencia_registre
    pa = llista._persistencia_article
    nom_a = input("Articulo a comprar: ")

    a = Article(nom=nom_a, persistencia=pa)
    a = a.persistencia.desa(a)
    q = int(input("Quantitat a comprar: "))
    r = Registre(article=a, quantitat=q)
    registre_afegit = pr.desa(r)
    mostra_lent("Registre afegit:", v=0.01)
    mostra_lent(registre_afegit.toJSON(), v=0.01)
    input("prem enter per continuar")
    

def rollback(llista):
    os.system('clear')
    r = input("Eliminare la data de memoria actual. Continuar [s/n]: ")
    if r == "s":
        llista._registres = []
        llista._categories = []
        mostra_llista(llista)



def mostra_menu():
    os.system('clear')
    print("0.- Surt de l'aplicació.")
    print("1.- Mostra la llista.")
    print("="*5 + " NEW FEATURES")
    print("2.- Afegir article.")
    print("3.- Afegir categoria.")
    print("4.- Afegir registre.")
    print("5.- Ajusta el condensador de fluxe per retrocedir en el temps (PSEUDO_ROLLBACK). Encara no fa res en les datasources")


def procesa_opcio(context):
    return {
        "0": lambda ctx : mostra_lent("Fins la propera"),
        "1": lambda ctx : mostra_llista(ctx['llista']),
        "2": lambda ctx : afegeix_article(ctx['llista']),
        "3": lambda ctx : afegeix_categoria(ctx['llista']),
        "4": lambda ctx : afegeix_registre(ctx['llista']),
        "5": lambda ctx : rollback(ctx['llista'])
    }.get(context["opcio"], lambda ctx : mostra_lent("opcio incorrecta!!!"))(context)


def bucle_principal(context):
    opcio = None
    while opcio != '0':
        context["llista"].llegeix_de_disc() #Es necesari per actualitzar les dades quan l'app esta en execucio
        mostra_menu()
        opcio = input("Selecciona una opció: ")
        context["opcio"] = opcio
        procesa_opcio(context)







def main():
    context = {
        "llista": None
    }
    landing_text()
    la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)
    persistencies = get_persistencies(la_meva_configuracio)
    llista = Llista(
        persistencia_article = persistencies['article'],
        persistencia_registre = persistencies['registre'],
        persistencia_categoria = persistencies['categoria'],
    )
    context["llista"] = llista
    bucle_principal(context)

if __name__ == "__main__":
    main()