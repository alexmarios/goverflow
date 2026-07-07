from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

with DAG("hello_world", start_date=days_ago(1), schedule_interval=None, catchup=False) as dag:
    PythonOperator(
        task_id="say_hello",
        python_callable=lambda: print("Hello from Airflow!"),
    )
