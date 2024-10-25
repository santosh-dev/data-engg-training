from datetime import datetime, timedelta
import pendulum
from airflow import DAG
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.models import Variable

local_tz = pendulum.timezone("america/new_york")

default_args = {
    'owner': 'umathiva',
    'depends_on_past': False,
    'start_date': datetime(2020, 10, 10, tzinfo=local_tz),
    'email': ['uday.kumar@amazon.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 0,
    'retry_delay': timedelta(minutes=5)
}
dag = DAG(dag_id='patient_ingestion_dag',
          default_args=default_args,
          catchup=False,
          schedule_interval="0 * * * *") #contab-style scheduling pattern 
pyspark_app_home = Variable.get("PYSPARK_APP_AWS_HOME")

patient_data_ingestion = SparkSubmitOperator(task_id='patient_data_ingestion',
                                              conn_id='spark_local',
                                              application=f'{pyspark_app_home}/spark/patient_data_ingestion.py',
                                              total_executor_cores=4,
                                              packages="io.delta:delta-core_2.12:0.7.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0",
                                              executor_cores=2,
                                              executor_memory='5g',
                                              driver_memory='5g',
                                              name='patient_data_ingestion',
                                              execution_timeout=timedelta(minutes=10),
                                              dag=dag
                                              )

patient_claim_search = SparkSubmitOperator(task_id='patient_claim_search',
                                                 conn_id='spark_local',
                                                 application=f'{pyspark_app_home}/spark/patient_claim_search.py',
                                                 total_executor_cores=4,
                                                 packages="io.delta:delta-core_2.12:0.7.0,org.postgresql:postgresql:42.2.9",
                                                 executor_cores=2,
                                                 executor_memory='10g',
                                                 driver_memory='10g',
                                                 name='patient_claim_search',
                                                 execution_timeout=timedelta(minutes=10),
                                                 dag=dag
                                                 )

patient_org_search = SparkSubmitOperator(task_id='patient_org_search',
                                       conn_id='spark_local',
                                       application=f'{pyspark_app_home}/spark/patient_org_search.py',
                                       total_executor_cores=4,
                                       packages="io.delta:delta-core_2.12:0.7.0,org.postgresql:postgresql:42.2.9",
                                       executor_cores=2,
                                       executor_memory='10g',
                                       driver_memory='10g',
                                       name='patient_org_search',
                                       execution_timeout=timedelta(minutes=10),
                                       dag=dag
                                       )
#binary right shift >> operator to set the  dependency
patient_data_ingestion >> [patient_claim_search, patient_org_search]
