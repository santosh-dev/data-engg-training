from datetime import datetime, timezone
from airflow.decorators import dag, task
from airflow.models.dag import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.dates import days_ago
from airflow.decorators import task
import pendulum

default_args = {
    'owner': 'airflow',"retries":2
}


with DAG(
    "dell_child_dag",
    default_args=default_args,
    description="dell demo trigger external dag",
    schedule=None,
    start_date=pendulum.datetime(2024, 7, 10, tz="UTC"),
    catchup=False,
    tags=["dell"]
) as dag:

 child_task=  TriggerDagRunOperator(
            task_id="dell_child_task_id",
            execution_date=datetime.now().replace(tzinfo=timezone.utc),
            trigger_dag_id="dell_parent_dag",  
            reset_dag_run=True,
            wait_for_completion=True,
            poke_interval=60,
            dag = dag,
        )

child_task