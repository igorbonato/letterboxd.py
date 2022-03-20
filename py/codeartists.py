# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 21:44:11 2020
@author: Leonardo
"""

from collections import Counter
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")
site = "https://letterboxd.com"


def meus_favoritos(user):
    lista_principal = []
    i = requests.get("https://letterboxd.com/"+user+"/films")
    user_page = BeautifulSoup(i.content)
    paginazinhas = user_page.select("li.paginate-page a")
    ult_page = int(paginazinhas[-1].string)
    for p in range(1, ult_page+1):
        igor = pages(p, user)
        lista_principal.extend(igor)
    top = avaliar(lista_principal)
    return top, lista_principal


def pages(page, usuario):
    r = requests.get("https://letterboxd.com/"+usuario +
                     "/films/page/"+str(page), timeout=10)
    soup = BeautifulSoup(r.content)
    selectss = soup.select("li.poster-container div")
    elenco = []
    links = []
    for select in selectss:
        links.append(select["data-film-slug"])
    for link in links:
        nome, pessoas = cast(site+str(link))
        elenco.append((nome, pessoas))
    return elenco


# def cast1(path):
#     s = requests.get(path, timeout=5)
#     conteudo = BeautifulSoup(s.content)
#     p = conteudo.select("div.cast-list p a")
#     pessoas = [pessoa.string for pessoa in p]
#     if 'Show All…' in pessoas:
#         pessoas.remove("Show All…")
#     j = conteudo.select("h1.headline-1")
#     nome = [ji.string for ji in j][0]
#     return nome, pessoas

def avaliar(lista):
    contagem = []
    for i in lista:
        contagem.extend(i[1])
    contagem = Counter(contagem)
    return contagem


def cast(path):
    try:
        s = requests.get(path, timeout=5, verify=False)
        conteudo = BeautifulSoup(s.content)
        p = conteudo.select("div.cast-list p a")
        pessoas = [pessoa.string for pessoa in p]
        if 'Show All…' in pessoas:
            pessoas.remove("Show All…")
        j = conteudo.select("h1.headline-1")
        nome = [ji.string for ji in j][0]
        return nome, pessoas
    except requests.exceptions.Timeout:
        print("Timeout occurred -> "+path)
        return [path], ["erro"]


top, lista = meus_favoritos("igorbonato")

ordenado = {k: v for k, v in sorted(top.items(), key=lambda item: item[1])}

top1 = {key: value for (key, value) in ordenado.items() if value > 10}


def record(filename, my_dict):
    with open(filename, 'w', encoding="utf-8") as f:
        for k, v in my_dict.items():
            f.write(f"{k}:{v}\n")


def record_lista(filename, lista):
    with open(filename, "w", encoding="utf-8") as f:
        for i in lista:
            a = (",").join([1])
            f.write(a)


record("artists.txt", ordenado)
