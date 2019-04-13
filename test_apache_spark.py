# https://spark.apache.org/docs/latest/quick-start.html#self-contained-applications

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import os

# =========== Trabalho de pesquisa e ordenação

# MAIN

spark = SparkSession.builder.appName("SimpleApp").getOrCreate()


dataframe = spark.read.text("artigos_teste/teste.txt")
print(dataframe.collect())





spark.stop()
