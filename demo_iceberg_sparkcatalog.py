from pyspark.sql import SparkSession


try:
    # Initialize Spark session with Iceberg configurations
    spark = SparkSession.builder \
    .appName("dell-demo-icebergapp") \
    .master("local[*]")\
    .config('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.2') \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config("spark.sql.catalog.localdellcatalog", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.localdellcatalog.type", "hadoop") \
    .config("spark.sql.catalog.localdellcatalog.warehouse", "dell-scm-warehouse/iceberg") \
    .config("spark.sql.defaultCatalog", "localdellcatalog")\
    .getOrCreate()

    # Create an Iceberg table
    spark.sql("""
        CREATE TABLE IF NOT EXISTS localdellcatalog.product(
        id INT,
        name STRING,
        price INT
    ) USING iceberg""")

    spark.sql("""
    INSERT INTO localdellcatalog.product VALUES 
        (10, 'Latitude', 50000), 
        (20, 'Alienware', 100000),
        (30, 'Dell PowerEdge Tower', 250000)
    """)

    spark.sql("SELECT * FROM localdellcatalog.product").show(truncate=False)

    from pyspark.sql.types import StructType, StructField, StringType, IntegerType

    schema = StructType([
        StructField("id", IntegerType(), nullable=False),
        StructField("name", StringType(), nullable=True),
        StructField("country", StringType(), nullable=True)
    ])


    data = [
        (1, "Laptop", "US"),
        (2, "Gaming", "US"),
        (3, "Server", "CA")
    ]

    df = spark.createDataFrame(data, schema)

    df.writeTo("localdellcatalog.productcategory").partitionedBy("country").createOrReplace()
    
    spark.sql("SELECT * FROM localdellcatalog.productcategory").show(truncate=False)

    new_data = [(60,"Workstation","CA")]
    df = spark.createDataFrame(data=new_data, schema=schema)
    df.writeTo("localdellcatalog.productcategory").append()
    spark.sql("SELECT * FROM localdellcatalog.productcategory").show(truncate=False)

    spark.sql("DELETE FROM localdellcatalog.productcategory WHERE id == 60")
    table = spark.table("localdellcatalog.productcategory")
    table.show()

    spark.sql("UPDATE localdellcatalog.productcategory set id = 100 WHERE id == 10")
    table.show()

except Exception as ex:
    print(ex)