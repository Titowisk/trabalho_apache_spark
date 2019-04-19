# https://spark.apache.org/docs/latest/quick-start.html#self-contained-applications

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import os
import nltk
nltk.download('stopwords')
# =========== Trabalho de pesquisa e ordenação

# MAIN

spark = SparkSession.builder.appName("SimpleApp").getOrCreate()


dataframe = spark.read.text("artigos_teste/teste.txt") # retorna um dataframe
# select = dataframe.select('*').show()
# split = dataframe.select(split(dataframe.value, '\s+')).show()
"""
Split
+--------------------+
|   split(value, \s+)|
+--------------------+
|[Lorem, ipsum, do...|
|                  []|
|[Nulla, posuere, ...|
|                  []|
|[Nulla, sit, amet...|
|                  []|
|[Cras, turpis, nu...|
|                  []|
|[Suspendisse, sed...|
+--------------------+
"""

# explode = dataframe.select(explode(split(dataframe.value, '\s+')).alias("Palavras")).show()
"""
Explode
+-----------+            
|   Palavras|            
+-----------+            
|      Lorem|            
|      ipsum|            
|      dolor|            
|        sit|            
|      amet,|            
|consectetur|            
| adipiscing|            
|      elit.|            
|         In|            
|   iaculis,|            
|     ligula|            
|       quis|            
|   lobortis|            
|   aliquam,|            
|         mi|            
|       orci|            
|   faucibus|            
|     massa,|            
|         eu|            
|  imperdiet|            
+-----------+            
only showing top 20 rows 
"""

count_df = dataframe.select(explode(split(dataframe.value, '([,.?!]?\s+[.,?!]?)+')).alias("Palavras")).groupBy("palavras").count()
count_df.filter(~count_df["palavras"].isin(nltk.corpus.stopwords.words('portuguese'))).show()
"""
count
+------------+-----+     
|    palavras|count|     
+------------+-----+     
|      velit,|    1|     
|       eros.|    2|     
|consectetur.|    2|     
|        odio|    3|     
|         Sed|    3|     
|    volutpat|    2|     
|     pretium|    3|     
|   volutpat,|    1|     
|       nisl.|    1|     
|     lectus,|    1|     
|        vel.|    1|     
|     Quisque|    2|     
|   volutpat.|    1|     
|    sagittis|    3|     
|   hendrerit|    2|     
|       netus|    1|     
|       velit|    3|     
|sollicitudin|    2|     
|  hendrerit.|    1|     
|       lorem|    2|     
+------------+-----+     
only showing top 20 rows 
"""

# print(dataframe.value) # Column<b'value'>

spark.stop()
