"""
Created on Fri Dec 04 23:44:11 2020
@author: Igor & Leonardo
"""

import warnings
warnings.filterwarnings("ignore")
import re
from collections import Counter
import requests
from bs4 import BeautifulSoup
site="https://letterboxd.com"
    
def meus_favoritos(user):
    lista_principal=[]
    i=requests.get("https://letterboxd.com/"+user+"/films")
    user_page=BeautifulSoup(i.content)
    paginazinhas=user_page.select("li.paginate-page a")
    ult_page=int(paginazinhas[-1].string)
    for p in range(1,ult_page+1):
        pagg=pages(p,user)
        lista_principal.extend(pagg)
    top=avaliar(lista_principal)
    return top
    
def pages(page,usuario):
    r = requests.get("https://letterboxd.com/"+usuario+"/films/page/"+str(page),timeout=5)
    soup=BeautifulSoup(r.content)
    selectss=soup.select("li.poster-container div")
    geral=[]
    links=[]
    for select in selectss:
        links.append(select["data-film-slug"])
    for link in links:
        nome,generos=genre(site+str(link))
        geral.append((nome,generos))
    return geral
            
def genre1(path):
    s= requests.get(path, timeout=5)
    conteudo=BeautifulSoup(s.content)
    p=conteudo.select("div.text-sluglist p a") 
    generos=[genero.string for genero in p]
    if "Show All..." in generos: 
        generos.remove("Show All…")
    j=conteudo.select("h1.headline-1")
    nome=[ji.string for ji in j][0]
    return nome,generos

def genre(path):
    for attempt in range(10):
        try:
            s= requests.get(path, timeout=5,verify=False)
            conteudo=BeautifulSoup(s.content)
            p=conteudo.select("div.text-sluglist.capitalize")
            if len(p) >=1:
                w=p[0].find_all(href=re.compile("genre"))
                generos=[genre.string for genre in w]
            else:
                generos=["Sem Genero"]
            j=conteudo.select("h1.headline-1")
            nome=[ji.string for ji in j][0]
            return nome,generos
        except requests.exceptions.Timeout:
            continue
        else:
            break
    else:
        print("Timeout occurred"+path)
        return [path],["error"]
     
def avaliar(lista):
    contagem=[]
    for i in lista:
        contagem.extend(i[1])
    contagem=Counter(contagem)
    return contagem

#Insira seu nome de usuario no Letterboxd:
lista=meus_favoritos("")

ordenado={k: v for k, v in sorted(lista.items(), key=lambda item: item[1])}

top={key: value for (key,value) in ordenado.items() if value>10}

def record(filename,my_dict):
    with open(filename, 'w',encoding="utf-8") as f:
        for k,v in my_dict.items():
            f.write(f"{k}:{v}\n")
        
def record_lista(filename,lista):
     with open (filename,"w",encoding="utf-8") as f:
         a=(",").join(lista)
         f.write(a)
    
#Para rodar use o seguinte comando no console:
#   record("nome de seu arquivo.txt",ordenado)  
# O arquivo em formato .doc estará salvo na pasta designada.  
