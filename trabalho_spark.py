# https://spark.apache.org/docs/latest/quick-start.html#self-contained-applications

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import os
import nltk
import datetime
nltk.download('stopwords')
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
    regex = '([,.?!]?\s+[.,?!]?)+'
    palavras_contadas = artigo_pdf.select(explode(split(artigo_pdf.value, regex)).alias("palavras")).groupBy("palavras").count()

    # ordena por count
    palavras_contadas = palavras_contadas.orderBy(desc("count"))

    # remove stopwords portugues e alguns outros caracteres
    stopwords_and_characteres = nltk.corpus.stopwords.words('portuguese') + ["-", "—", "", "–"]
    palavras_contadas = palavras_contadas.filter(~palavras_contadas["palavras"].isin(stopwords_and_characteres))

    return palavras_contadas


# MAIN
#inicializa dicionario
topArtigos = {}
palavra = input("Digite a palavra para verificar as ocorrencias nos artigos:\n")
try:
    # medir tempo
    dt1 = datetime.datetime.now()
    spark = SparkSession.builder.appName("SimpleApp").getOrCreate()

    pasta_artigos = 'artigos_txt' # trocar para artigos_teste para... ... ... teste (com arquivos menores) :D
    lista_de_artigos = os.listdir(pasta_artigos)

    artigos = cria_spark_cache(pasta_artigos)

    # https://spark.apache.org/docs/latest/quick-start.html#more-on-dataset-oaperations
    for artigo_nome, artigo_conteudo in artigos.items(): #dict.values() ->  [spark.read.text(artigo1).cache(), spark.read.text(artigo2).cache(), ...]
        palavras_contadas = conta_palavras(artigo_conteudo) # objeto <class 'pyspark.sql.dataframe.DataFrame'> 

        # https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrameWriter
        # https://stackoverflow.com/questions/31937958/how-to-export-data-from-spark-sql-to-csv
        palavras_contadas.coalesce(1).write.csv(path=os.path.join('resultado', artigo_nome), sep='|', mode='append')

        #Filtra as linhas que contem a palavra desejada
        artigoFiltrado = palavras_contadas.where(palavras_contadas.palavras == palavra)        
        try:
            #Adiciona no dicionario ("Nome do Artigo" : contagem)
            topArtigos[artigo_nome] = artigoFiltrado.first()[1]
        except:            
            pass
finally:
    if spark: spark.stop()
    dt2 = datetime.datetime.now()
    print("Tempo gasto: {tempo}".format(tempo = dt2-dt1))
    #print(topArtigos)
    print("Os três artigos com maior número de ocorrencias da palavra " + palavra + ": " + str(sorted(topArtigos, key=topArtigos.get, reverse =True)[:3]))




