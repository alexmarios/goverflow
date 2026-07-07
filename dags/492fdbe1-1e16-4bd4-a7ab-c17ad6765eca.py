"""
This file has been generated from dag_runner.j2
"""
from airflow import DAG
from openmetadata_managed_apis.workflows import workflow_factory

workflow = workflow_factory.WorkflowFactory.create("/opt/airflow/dag_generated_configs/492fdbe1-1e16-4bd4-a7ab-c17ad6765eca.json")
workflow.generate_dag(globals())
dag = workflow.get_dag()