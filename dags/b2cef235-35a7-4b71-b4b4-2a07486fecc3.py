"""
This file has been generated from dag_runner.j2
"""
from airflow import DAG
from openmetadata_managed_apis.workflows import workflow_factory

workflow = workflow_factory.WorkflowFactory.create("/opt/airflow/dag_generated_configs/b2cef235-35a7-4b71-b4b4-2a07486fecc3.json")
workflow.generate_dag(globals())
dag = workflow.get_dag()