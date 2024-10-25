import pendulum
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
import json
import textwrap

with DAG(
    "dell_demo_dag",
    default_args={"retries": 2},
    description="dell demo DAG",
    schedule=None,
    start_date=pendulum.datetime(2024, 7, 10, tz="UTC"),
    catchup=False,
    tags=["dell"],
) as dag:
    
    dag.doc_md = __doc__
    
    #@dag(start_date=datetime(2024, 2, 1))
    def extract(**kwargs):
        ti = kwargs["ti"]
        data_string = '{"Laptop": 300000.45, "Workstation": 800001.36, "Server": 9911111.35}'
        ti.xcom_push("order_data", data_string)
    
    #@task(multiple_outputs=True)
    def transform(**kwargs): #order_data: dict
        ti = kwargs["ti"]
        extract_data_string = ti.xcom_pull(task_ids="extract", key="order_data")
        order_data = json.loads(extract_data_string)

        total_order_value = 0
        for value in order_data.values():
            total_order_value += value

        total_value = {"total_order_value": total_order_value}
        total_value_json_string = json.dumps(total_value)
        ti.xcom_push("total_order_value", total_value_json_string)

    def load(**kwargs):
        ti = kwargs["ti"]
        total_value_string = ti.xcom_pull(task_ids="transform", key="total_order_value")
        total_order_value = json.loads(total_value_string)

        print(total_order_value)

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract,
    )
    extract_task.doc_md = textwrap.dedent(
        """\
    #### Extract task
    """
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform,
    )
    transform_task.doc_md = textwrap.dedent(
        """\
    #### Transform task
       """
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=load,
    )
    load_task.doc_md = textwrap.dedent(
        """\
    #### Load task
        just prints it out.
    """
    )

    extract_task >> transform_task >> load_task

    #Airflow 2.0
    """order_data = extract()
    order_summary = transform(order_data)
    load(order_summary["total_order_value"])"""