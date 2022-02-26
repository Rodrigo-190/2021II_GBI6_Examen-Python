def download_pubmed(keyword):
    """ Esta funcion permite la realizacion de una busqueda en la base de datos NCBI
    'https://pubmed.ncbi.nlm.nih.gov/' con un parametro de entrada keydowrd """
    from Bio import Entrez
    Entrez.email = "arnoldd.hernandez@est.ikiam.edu.ec"
    record=Entrez.read(Entrez.esearch(db="pubmed",
                        term= keyword,
                        usehistory="y"))
    
    webenv=record["WebEnv"]
    query_key=record["QueryKey"]
    handle=Entrez.efetch(db="pubmed",
                      rettype='medline',
                      retmode="text",
                      retstart=0,
                      retmax=543, webenv=webenv, query_key=query_key)
    out_handle = open(keyword+".txt", "w")
    m=handle.read()
    out_handle.write(m)
    out_handle.close()
    handle.close()
    return m

def mining_pubs(tipo, archivo):
    """
    La función mining_pubs, utiliza un parametro de ''tipo'', para la busqueda dependiendo de la busqueda realizada en la función ´download_pubmed´
    - Si es  tipo "DP" -> recuperará el año de publicación del artículo. El retorno será un *dataframe* con el     **PMID** y el **DP_year**.
    - Si es tipo  "AU" -> recuperará el número de autores por **PMID**. El retorno será un *dataframe* con el **PMID** y el **num_auth**. 
    - Si es tipo "AD" -> recuperará el conteo de autores por país. El retorno será un *dataframe* con el **country** y el **num_auth**.
    """
    import csv
    import re
    import pandas as pd
    from collections import Counter
    with open(archivo+".txt", errors="ignore") as f: 
        mitexto = f.read() 
    if tipo == "DP":
        PMID = re.findall("PMID-\s\d{8}", mitexto)
        PMID = "".join(PMID)
        PMID = PMID.split("PMID- ")
        año = re.findall("DP\s{2}-\s(\d{4})", mitexto)
        pmid_y = pd.DataFrame()
        pmid_y["PMID"] = PMID
        pmid_y["Año de publicación"] = año
        return (pmid_y)
    elif tipo == "AU": 
        PMID = re.findall("PMID- (\d*)", mitexto) 
        autores = mitexto.split("PMID- ")
        autores.pop(0)
        num_autores = []
        for i in range(len(autores)):
            numero = re.findall("AU -", autores[i])
            n = (len(numero))
            num_autores.append(n)
        pmid_a = pd.DataFrame()
        pmid_a["PMID"] = PMID 
        pmid_a["Número de autores"] = num_autores
        return (pmid_a)
    elif tipo == "AD": 
        mitexto = re.sub(r" [A-Z]{1}\.","", mitexto)
        mitexto = re.sub(r"Av\.","", mitexto)
        mitexto = re.sub(r"Vic\.","", mitexto)
        mitexto = re.sub(r"Tas\.","", mitexto)
        AD = mitexto.split("AD  - ")
        n_paises = []
        for i in range(len(AD)): 
            pais = re.findall("\S, ([A-Za-z]*)\.", AD[i])
            if not pais == []: 
                if not len(pais) >= 2:  
                    if re.findall("^[A-Z]", pais[0]): 
                        n_paises.append(pais[0])
        conteo=Counter(n_paises)
        resultado = {}
        for clave in conteo:
            valor = conteo[clave]
            if valor != 1: 
                resultado[clave] = valor 
        veces_pais = pd.DataFrame()
        veces_pais["Países"] = resultado.keys()
        veces_pais["Número de autores"] = resultado.values()
        return (veces_pais)