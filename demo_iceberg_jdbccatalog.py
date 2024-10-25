from pyspark.sql import SparkSession
from pyspark.sql import SparkSession, Row

try:
    # Initialize Spark session with Iceberg JDBC catalog configuration
    spark = SparkSession.builder \
    .appName("delldemo-app") \
    .config('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.2,org.postgresql:postgresql:42.2.23') \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config('spark.sql.catalog.dell_catalog','org.apache.iceberg.spark.SparkCatalog')\
    .config("spark.sql.catalog.dell_catalog.catalog-impl", "org.apache.iceberg.jdbc.JdbcCatalog")\
    .config("spark.sql.catalog.dell_catalog.uri", "jdbc:postgresql://ep-billowing-pond-a450qgrv.us-east-1.aws.neon.tech:5432/demoDB") \
    .config("spark.sql.catalog.dell_catalog.verifyServerCertificate", "true") \
    .config("spark.sql.catalog.dell_catalog.useSSL", "true") \
    .config("spark.sql.catalog.dell_catalog.jdbc.user", "demoDB_owner") \
    .config("spark.sql.catalog.dell_catalog.jdbc.password", "Pv4lxD3yuWJI") \
    .config("spark.sql.catalog.dell_catalog.jdbc.driver", "org.postgresql.Driver") \
    .config("spark.sql.catalog.dell_catalog.warehouse", "file:///c:/dell_scm_warehouse")\
    .getOrCreate()

    # Create an Iceberg table
    spark.sql("""
        CREATE TABLE IF NOT EXISTS dell_catalog.product(
        id INT,
        name STRING,
        price INT
    ) USING iceberg""")

    spark.sql("""
    INSERT INTO dell_catalog.product VALUES 
        (10, 'Latitude', 50000), 
        (20, 'Alienware', 100000),
        (30, 'Dell PowerEdge Tower', 250000)
    """)

    spark.sql("SELECT * FROM dell_catalog.product").show(truncate=False)

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

    df.writeTo("dell_catalog.productcategory").partitionedBy("country").createOrReplace()
    
    spark.sql("SELECT * FROM dell_catalog.productcategory").show(truncate=False)

    new_data = [(60,"Workstation","CA")]
    df = spark.createDataFrame(data=new_data, schema=schema)
    df.writeTo("dell_catalog.productcategory").append()
    spark.sql("SELECT * FROM dell_catalog.productcategory").show(truncate=False)

    spark.sql("DELETE FROM dell_catalog.productcategory WHERE id == 60")
    table = spark.table("dell_catalog.productcategory")
    table.show()

    spark.sql("UPDATE dell_catalog.productcategory set id = 100 WHERE id == 10")
    table.show()

except Exception as ex:
    print(ex)