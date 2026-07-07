"""
This file has been generated from dag_runner.j2
"""
from airflow import DAG
from openmetadata_managed_apis.workflows import workflow_factory

workflow = workflow_factory.WorkflowFactory.create("/opt/airflow/dag_generated_configs/fd65a29c-38c1-405e-bfaa-2b6f2c172350.json")
workflow.generate_dag(globals())
dag = workflow.get_dag()