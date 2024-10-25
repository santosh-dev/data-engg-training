from pyspark.sql import SparkSession, Row


# Initialize Spark session with Iceberg JDBC catalog configuration
spark = SparkSession.builder \
    .appName("udaydemo-app") \
    .config('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.2,org.postgresql:postgresql:42.2.23,org.apache.iceberg:iceberg-aws-bundle:1.5.2') \
    .config('spark.sql.catalog.santosh_minio_catalog','org.apache.iceberg.spark.SparkCatalog')\
    .config("spark.sql.catalog.santosh_minio_catalog.catalog-impl", "org.apache.iceberg.jdbc.JdbcCatalog")\
    .config("spark.sql.catalog.santosh_minio_catalog.uri", "jdbc:postgresql://ep-billowing-pond-a450qgrv.us-east-1.aws.neon.tech:5432/demoDB") \
    .config("spark.sql.catalog.santosh_minio_catalog.verifyServerCertificate", "true") \
    .config("spark.sql.catalog.santosh_minio_catalog.useSSL", "true") \
    .config("spark.sql.catalog.santosh_minio_catalog.jdbc.user", "demoDB_owner") \
    .config("spark.sql.catalog.santosh_minio_catalog.jdbc.password", "Pv4lxD3yuWJI") \
    .config("spark.sql.catalog.santosh_minio_catalog.jdbc.driver", "org.postgresql.Driver") \
    .config("spark.sql.catalog.santosh_minio_catalog.warehouse", "s3a://demobucket")\
    .config("spark.sql.catalog.santosh_minio_catalog.s3.endpoint","http://127.0.0.1:9000")\
    .config("spark.sql.catalog.santosh_minio_catalog.io-impl", "org.apache.iceberg.aws.s3.S3FileIO")\
    .config('spark.hadoop.fs.s3a.access.key', "gPNIiw9jJiRYtViL3UAS")\
    .config('spark.hadoop.fs.s3a.endpoint.region','us-east-1')\
    .config("spark.hadoop.fs.s3a.secret.key", "OGHHtRsIuyE7EigySxx2to1ZnGuvmbId12LYTXX0")\
    .config("spark.sql.catalog.santosh_minio_catalog.s3a.path-style-access", "true")\
    .config("spark.sql.catalogImplementation","in-memory")\
    .config("spark.executor.heartbeatInterval", "300000")\
    .config("spark.network.timeout", "400000")\
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")\
    .config("spark.hadoop.fs.s3a.path.style.access", "true")\
    .config("spark.hadoop.fs.s3a.attempts.maximum", "1")\
    .config("spark.hadoop.fs.s3a.connection.establish.timeout", "5000")\
    .config("spark.hadoop.fs.s3a.connection.timeout", "10000")\
    .getOrCreate()

sc = spark.sparkContext
sc.setLogLevel("ERROR")

# Create an Iceberg table
spark.sql("""
        CREATE TABLE IF NOT EXISTS santosh_minio_catalog.product (
        id INT,
        name STRING,
        price INT
    ) USING iceberg""")

spark.sql("""
    INSERT INTO santosh_minio_catalog.product VALUES 
        (1, 'laptop', 50000), 
        (2, 'workstation', 100000),
        (3, 'server', 250000),
        (4, 'Rack Server', 350000)
    """)

spark.sql("SELECT * FROM santosh_minio_catalog.product").show(truncate=False)

spark.stop()