"""
This file has been generated from dag_runner.j2
"""
from airflow import DAG
from openmetadata_managed_apis.workflows import workflow_factory

workflow = workflow_factory.WorkflowFactory.create("/opt/airflow/dag_generated_configs/aad9860e-803c-4a84-9553-5ad5872a3bc9.json")
workflow.generate_dag(globals())
dag = workflow.get_dag()