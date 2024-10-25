import pendulum
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
import json
import textwrap

from airflow.decorators import task

with DAG(
    "dell_demo_dag_withoutxcom",
    default_args={"retries": 2},
    description="dell demo DAG",
    schedule=None,
    start_date=pendulum.datetime(2024, 7, 10, tz="UTC"),
    catchup=False,
    tags=["dell"],
) as dag:
    
    dag.doc_md = __doc__
    
    @task()
    def extract():
        data_string = '{"Laptop": 300000.45, "Workstation": 800001.36, "Server": 9911111.35}'
        return data_string
    
    @task()
    def transform(extract_data_string): #order_data: dict
        #extract_data_string = ti.xcom_pull(task_ids="extract", key="order_data")
        order_data = json.loads(extract_data_string)

        total_order_value = 0
        for value in order_data.values():
            total_order_value += value

        # total_value = {"total_order_value": total_order_value}
        # total_value_json_string = json.dumps(total_value)
        return total_order_value
        #ti.xcom_push("total_order_value", total_value_json_string)

    @task()
    def load(total_order_value):
        print("Totla order value:",total_order_value)
        # total_order_value = json.loads(total_value_string)

        # print(total_order_value)

 
    #Airflow 2.0
    order_data = extract()
    order_summary = transform(order_data)
    load(order_summary)

    #load(transform(extract()))