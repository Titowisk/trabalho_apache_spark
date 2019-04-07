# https://spark.apache.org/docs/latest/quick-start.html#self-contained-applications

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import os

# =========== Trabalho de pesquisa e ordenação

# FUNÇÕES
def cria_spark_cache(pasta_artigos):
    # Ler vários artigos de uma pasta
    # cria um cache dos arquivos lidos através do spark
    # armazenar eles em um dicionario {'nome_do_arquivo': spark.read.text(artigo).cache()}
    # https://spark.apache.org/docs/latest/quick-start.html#self-contained-applications

    artigos_lidos_cache = dict() # {'key': 'value'}
     
    for artigo in lista_de_artigos:
        titulo = artigo.split(".")[0] # acessibilidade_e_tecnologia.pdf -> [acessibilidade_e_tecnologia, pdf]
        artigo_path = os.path.join(pasta_artigos, artigo)

        artigos_lidos_cache[titulo] = spark.read.text(artigo_path).cache()

    return artigos_lidos_cache

def conta_palavras(artigo_pdf):
    # conta a quantidade de palavras por palavra
    # https://spark.apache.org/docs/latest/quick-start.html#more-on-dataset-operations
    palavras_contadas = artigo_pdf.select(explode(split(artigo_pdf.value, "\s+")).alias("palavras")).groupBy("palavras").count()

    return palavras_contadas

def cria_arquivo_contagem(contagem, titulo_artigo):
   # Pegar o resultado e escrever num arquivo
   pass

# MAIN

spark = SparkSession.builder.appName("SimpleApp").getOrCreate()


pasta_artigos = 'artigos_teste' # trocar para artigos_teste para... ... ... teste (com arquivos menores) :D
lista_de_artigos = os.listdir(pasta_artigos)

artigos = cria_spark_cache(pasta_artigos)

# https://spark.apache.org/docs/latest/quick-start.html#more-on-dataset-operations
for artigo_spark in artigos.values(): #dict.values() ->  [spark.read.text(artigo1).cache(), spark.read.text(artigo2).cache(), ...]
    palavras_contadas = conta_palavras(artigo_spark)
    
    print( palavras_contadas.collect() ) # ! Problema de codificação de bits


spark.stop()
