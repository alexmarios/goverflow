from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

with DAG("test_gkd_dag", start_date=days_ago(1), schedule_interval=None, catchup=False) as dag:
    PythonOperator(
        task_id="test",
        python_callable=lambda: print("test"),
    )
