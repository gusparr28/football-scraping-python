from bs4 import BeautifulSoup
import pandas as pd
import requests

# Función que permite extraer las URL de los equipos pertenecientes a las Ligas del sitio transfermartk
def page_scrap(x):
    headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    page = x
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    
    # Definir sección pivote para realizar scrap.
    pageClub = pageSoup.find_all('td', {"class":"hauptlink no-border-links hide-for-small hide-for-pad"})

    # Definir arrays para almacenar datos
    clubName = []
    clubURL = []

    # Recorrer la sección definida como pivote.
    for i in pageClub:
        # Extraer el texto de la linea analizada
        clubName.append(i.text)

        # Avanzar a los 'a class' HTML para extraer la url del club
        web = i.find('a')
        clubURL.append(web.get('href'))

    # Crear data frame con club y url para hacer scrap a jugadores
    df = pd.DataFrame({"League":pageSoup.title.string[:-22], "Club Name":clubName, "URL":clubURL})
    
    return df.reset_index(drop=True)

    # Declarar variables
dataLeague = pd.DataFrame()

# Leer archivo.csv que contiene el enlace de cada liga a __Scrapear___ y lo transforma en __DataFrame__ 
# Cambiar nombre de archivo "league_links_test.csv" por "league_links_test.csv"
link = pd.read_csv("league_links_test.csv", sep=";")
dfLink = pd.DataFrame(link)

# Ejecuta la función de __Scrap__ 'n' veces como _LINK_ de ligas vengan en el archivo
for i in dfLink['link'] :
    dataLeague_temp = page_scrap(i)
    # Apilar los __DataFrames__ uno encima del otro __Vertical Stack__
    dataLeague = pd.concat([dataLeague, dataLeague_temp], axis=0)
    
    print("Cargando ", i, "de ", len(dfLink))