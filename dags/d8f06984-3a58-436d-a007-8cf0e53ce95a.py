"""
This file has been generated from dag_runner.j2
"""
from airflow import DAG
from openmetadata_managed_apis.workflows import workflow_factory

workflow = workflow_factory.WorkflowFactory.create("/opt/airflow/dag_generated_configs/d8f06984-3a58-436d-a007-8cf0e53ce95a.json")
workflow.generate_dag(globals())
dag = workflow.get_dag()