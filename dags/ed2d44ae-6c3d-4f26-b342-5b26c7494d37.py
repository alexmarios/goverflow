"""
This file has been generated from dag_runner.j2
"""
from airflow import DAG
from openmetadata_managed_apis.workflows import workflow_factory

workflow = workflow_factory.WorkflowFactory.create("/opt/airflow/dag_generated_configs/ed2d44ae-6c3d-4f26-b342-5b26c7494d37.json")
workflow.generate_dag(globals())
dag = workflow.get_dag()