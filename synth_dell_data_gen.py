from faker import Faker
import numpy as npy
import pandas as pd
from pyspark.sql import SparkSession
import logging 

from faker.providers import DynamicProvider

dellsupplier_provider = DynamicProvider(
     provider_name="dell_supplier",
     elements=["Celestica", "Compal", "Foxconn",
               "Inventec","Broadcom","Adata", 
               "Chicony Electronics","Catcher Technolog",
               "Fibocom","Finisar","Forin",
               "Hannstar","Innolux","IBM Corporation",
               "Wistron","Pegatron"],
)

synthVendorData = Faker()

#add the provider
synthVendorData.add_provider(dellsupplier_provider)

supplierId = []
supplierNames = []
supplierCompany = []
supplierEmail = []
sharePrice = []
supplierDate = []

filename_supplier = "dellsuppliers.csv"

recordCount = 500

for x in range(recordCount):
    supplierId.append(npy.random.randint(1000,9000))
    supplierNames.append(synthVendorData.name())
    sharePrice.append(npy.round(npy.random.uniform(1,10000), 2))
    supplierEmail.append(synthVendorData.email())
    supplierDate.append(synthVendorData.date())
    supplierCompany.append(synthVendorData.dell_supplier())

dfsuppliers = pd.DataFrame({"Supplier_Contact":supplierNames,"Company":supplierCompany,"Email":supplierEmail,"Share_Price":sharePrice,"Date":supplierDate})

dfsuppliers.to_csv(filename_supplier,index=False,header=True)

try:
    spark = SparkSession \
        .builder \
        .appName("demodellsuppliers-app") \
        .master("local[*]")\
        .getOrCreate()

    df_supplier = spark.read.csv(filename_supplier,header=True)

    #df_supplier.createOrReplaceTempView("supplier_company")
    #df_supplier_company = spark.sql("select * from supplier_company group by company order by company ")

    #df_supplier_company = df_supplier.groupBy("Company").count()
    #df_supplier_company.show()

    df_supplier.write.mode("overwrite").partitionBy("Company").csv("temp/suppliers",header=True)

except Exception as ex:
    logging.error(ex)
    print("Error Occured",ex)

