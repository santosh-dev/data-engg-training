from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.models import Variable
from datetime import datetime, timedelta
import pendulum

local_tz = pendulum.timezone("Asia/Kolkata")

default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 4, tzinfo=local_tz),
    #'email': ['udayakumar.net@gmail.com'],
    #'email_on_failure': True,
    #'email_on_retry': True,
    'retries': 0,
    'retry_delay': timedelta(minutes=5)
}
dag = DAG(dag_id='products_ingestion_dag',
          default_args=default_args,
          catchup=False,
          schedule_interval="00 09-17 * * * *",tags=["dell"]) # everyday (including weekends) during the working hours 9 a.m – 6 p.m

#other options include @daily(0 0 * * *) @hourly(0 * * * *) @once @weekly(0 0 * * 0) @monthly(0 0 1 * *) @yearly (0 0 1 1 *) None

pyspark_app_home = Variable.get("PYSPARK_APP_HOME")


products_data_ingestion = SparkSubmitOperator(task_id='product_data_ingestion',
                                              conn_id='spark_local_master',
                                              application=f'{pyspark_app_home}/spark_product_ingestion_db.py',
                                              total_executor_cores=4,
                                              #packages="org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0",
                                              executor_cores=4,
                                              executor_memory='4g',
                                              driver_memory='2g',
                                              name='product_data_ingestion',
                                              jars=f'{pyspark_app_home}/mysql-connector-java-8.0.13.jar',
                                              execution_timeout=timedelta(minutes=10),
                                              dag=dag
                                              )    
  
products_data_ingestion