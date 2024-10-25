from pyspark.sql import *

if __name__ == "__main__":
    print("hello spark")

    spark = SparkSession.builder \
            .appName("Hello Spark") \
            .master("local[2]") \
            .getOrCreate()
    
    data_list = [("Santosh",28),("David",30),("Oppie",45)]

    df =  spark.createDataFrame(data_list).toDF("Name","Age")

    #df.printSchema()
    df.show()