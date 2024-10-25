from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.dates import days_ago
from airflow.models.dag import DAG
import json
from airflow.decorators import task
import pendulum

default_args = {
    'owner': 'airflow',
}


with DAG(
    "dell_parent_dag",
    default_args={"retries": 2},
    description="dell demo trigger external dag",
    schedule=None,
    start_date=pendulum.datetime(2024, 7, 10, tz="UTC"),
    catchup=False,
    tags=["dell"]
) as dag:


    @task()
    def multiply_by_9(value):
        return value * 9

    @task()
    def divide_by_5(value):
        return value / 5

    @task()
    def add_32(value):
        temp_in_fahrenheit = value + 32
        print(f"Temperature in Fahrenheit:{ temp_in_fahrenheit }")
        return temp_in_fahrenheit

    multiplied_value = multiply_by_9(37)              # task 1
    divided_value = divide_by_5(multiplied_value)     # task 2
    add_32(divided_value)                             # task 3