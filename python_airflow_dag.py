from __future__ import annotations
import logging
import sys
import time
from pprint import pprint
from datetime import datetime
import pendulum
import pandas as pd


from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator

from airflow.decorators import task
from airflow.operators.bash import BashOperator

log = logging.getLogger(__name__)

#create a dag object
with DAG(dag_id="pandas_datacsvwrite_dag",
         start_date=pendulum.datetime(2024, 7, 10, tz="UTC"),
         schedule_interval="@hourly",
         catchup=False,
         tags=["delldatagenerator","dell"]) as dag:
    
#start defining the tasks
    welcome_msg_task = BashOperator(task_id="welcome_message_task", bash_command="echo welcome to airflow dell workflow")


    def sleeping_func(random_base):
         time.sleep(random_base)


    sleeping_task = PythonOperator(
            task_id=f"sleep_task", python_callable=sleeping_func, op_kwargs={"random_base": 10},dag=dag
        )

    #Generate Dell Data into a CSV
    def generateDellProducts(filename):

        try:

            products = {'Name': ['Dell 14 Thin & Light Laptop', 'Dell G15-5530 Gaming Laptop', 'Dell Latitude 5490 Business 7th Gen Laptop PC', 'Dell Inspiron 3520 Laptop, Intel Core i5'],
                    'Price': [500, 950, 350, 600]}

            df_product = pd.DataFrame(products)

            df_product.to_csv(filename)

        except Exception as ex:
            logging.error(ex)
      
    generateDellData_task = PythonOperator(task_id="generate_dell_data_task",python_callable=generateDellProducts,op_kwargs={"filename": "/mnt/e/DataScience-Code Repo/Data Engineering/Content/Day13/output/dellproducts.csv"},dag=dag)

#from 2.0 version of airflpow...it supports task decorator
    @task()
    def airflow():
        print("data ingested successfully")


    welcome_msg_task >> sleeping_task >> generateDellData_task >> airflow()