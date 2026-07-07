"""
This file has been generated from dag_runner.j2
"""
from airflow import DAG
from openmetadata_managed_apis.workflows import workflow_factory

workflow = workflow_factory.WorkflowFactory.create("/opt/airflow/dag_generated_configs/353ed65d-8bae-43ce-b9b1-d08093336fd9.json")
workflow.generate_dag(globals())
dag = workflow.get_dag()