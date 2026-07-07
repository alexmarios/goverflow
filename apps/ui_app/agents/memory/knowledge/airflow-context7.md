### Install Airflow with Pip and Extras (Bash)

Source: https://airflow.apache.org/docs/stable/start.html

Installs Apache Airflow using pip, including specified extras and a constraint file for reproducible builds. This command is an example of how to install Airflow with specific dependencies.

```bash
pip install "apache-airflow[celery]==3.0.0" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.0.0/constraints-3.10.txt"
```

--------------------------------

### Setup Scope and Dependencies

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/setup-and-teardown.html

Explains the concept of setup 'scope' and how clearing tasks within the scope affects setup and teardown tasks.

```APIDOC
## Setup Scope and Dependencies

### Description
This section explains the 'scope' of tasks between a setup and its teardown. Tasks within this scope are implicitly dependent on the setup task. Clearing a task within the scope will also clear the associated setup and teardown tasks.

### Method
N/A (Conceptual Example)

### Endpoint
N/A (Conceptual Example)

### Parameters
N/A

### Request Example
```python
s1 >> w1 >> w2 >> t1.as_teardown(setups=s1) >> w3
w2 >> w4
```

### Response
N/A
```

--------------------------------

### Quickstart Asset Scheduling

Source: https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/asset-scheduling.html

A basic example showing the syntax for declaring an asset outlet within a DAG task and configuring a separate DAG to trigger upon that asset's update.

```python
from airflow.sdk import DAG, Asset

with DAG(...):
    MyOperator(
        outlets=[Asset("s3://asset-bucket/example.csv")],
        ...,
    )

with DAG(
    schedule=[Asset("s3://asset-bucket/example.csv")],
    ...,
):
    ...
```

--------------------------------

### Add Python Packages via PyPI

Source: https://airflow.apache.org/docs/docker-stack/build.html

Examples of installing Python packages using pip, including options for using constraints files or the experimental uv installer for faster performance.

```Dockerfile
FROM apache/airflow:2.11.2
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" lxml
```

```Dockerfile
FROM apache/airflow:2.11.2
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" lxml --constraint "${HOME}/constraints.txt"
```

```Dockerfile
FROM apache/airflow:2.11.2
RUN uv pip install --no-cache "apache-airflow==${AIRFLOW_VERSION}" lxml
```

--------------------------------

### Basic Setup and Teardown

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/setup-and-teardown.html

Demonstrates the basic usage of setup and teardown tasks using `as_setup` and `as_teardown` methods.

```APIDOC
## Basic Setup and Teardown

### Description
This example shows how to designate tasks as setup and teardown using `as_setup()` and `as_teardown()` methods and establish their relationships.

### Method
N/A (Conceptual Example)

### Endpoint
N/A (Conceptual Example)

### Parameters
N/A

### Request Example
```python
create_cluster.as_setup()
run_query
delete_cluster.as_teardown()

# Or in one line:
create_cluster >> run_query >> delete_cluster.as_teardown(setups=create_cluster)
```

### Response
N/A
```

--------------------------------

### Install Snowflake Provider with Extras

Source: https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/index.html

This command shows how to install the Snowflake provider for Airflow, including optional extras for cross-provider compatibility. The `common.compat` extra is used here as an example.

```bash
pip install apache-airflow-providers-snowflake[common.compat]
```

--------------------------------

### Installation

Source: https://airflow.apache.org/docs/task-sdk/stable/index.html

Instructions on how to install the Apache Airflow Task SDK using pip.

```APIDOC
## Installation

To install the Task SDK, run:

```bash
pip install apache-airflow-task-sdk
```
```

--------------------------------

### Install Airflow Helm Chart

Source: https://airflow.apache.org/docs/helm-chart/stable/quick-start.html

Installs the Apache Airflow Helm chart into the specified Kubernetes namespace. It demonstrates basic installation and an advanced installation with example DAGs enabled.

```bash
export RELEASE_NAME=example-release
helm install $RELEASE_NAME apache-airflow/airflow --namespace $NAMESPACE
helm install $RELEASE_NAME apache-airflow/airflow \
  --namespace $NAMESPACE \
  --set-string "env[0].name=AIRFLOW__CORE__LOAD_EXAMPLES" \
  --set-string "env[0].value=True"
```

--------------------------------

### GET /airflow/providers/edge3/integration_test/my_setup

Source: https://airflow.apache.org/docs/apache-airflow-providers-edge3/stable/_api/airflow/providers/edge3/example_dags/integration_test/index.html

Executes the setup function for the Edge provider integration test suite to verify environment configuration.

```APIDOC
## GET /airflow/providers/edge3/integration_test/my_setup

### Description
This function initializes the necessary environment state for integration tests within the Edge provider. It is designed to run in all standard Airflow setups to ensure core functionality is operational.

### Method
GET

### Endpoint
/airflow/providers/edge3/integration_test/my_setup

### Parameters
#### Path Parameters
- None

#### Query Parameters
- None

#### Request Body
- None

### Request Example
{}

### Response
#### Success Response (200)
- **status** (string) - Indicates the success of the setup operation.

#### Response Example
{
  "status": "success",
  "message": "Integration test environment initialized successfully."
}
```

--------------------------------

### SFTP Connection URI Examples (Environment Variable)

Source: https://airflow.apache.org/docs/apache-airflow-providers-sftp/stable/connections/sftp.html

Examples of setting up SFTP connections using environment variables with URI syntax. Demonstrates configurations with key_file and host_key.

```bash
export AIRFLOW_CONN_SFTP_DEFAULT='sftp://user:pass@localhost:22?key_file=%2Fhome%2Fairflow%2F.ssh%2Fid_rsa'
```

```bash
export AIRFLOW_CONN_SFTP_DEFAULT='sftp://user:pass@localhost:22?host_key=AAAHD...YDWwq%3D%3D&no_host_key_check=false'
```

--------------------------------

### Install YDB Provider with Extras

Source: https://airflow.apache.org/docs/apache-airflow-providers-ydb/stable/index.html

Demonstrates how to install the apache-airflow-providers-ydb package with optional cross-provider dependencies like common.compat.

```bash
pip install apache-airflow-providers-ydb[common.compat]
```

--------------------------------

### GET /airflow/providers/standard/example_dags/example_short_circuit_operator

Source: https://airflow.apache.org/docs/apache-airflow-providers-standard/stable/_api/airflow/providers/standard/example_dags/example_short_circuit_operator/index.html

Retrieves the module contents and attributes for the ShortCircuitOperator example DAG.

```APIDOC
## GET /airflow/providers/standard/example_dags/example_short_circuit_operator

### Description
Fetches the configuration and attribute definitions for the ShortCircuitOperator example DAG module.

### Method
GET

### Endpoint
/airflow/providers/standard/example_dags/example_short_circuit_operator

### Parameters
None

### Request Example
GET /airflow/providers/standard/example_dags/example_short_circuit_operator

### Response
#### Success Response (200)
- **cond_true** (attribute) - A boolean condition attribute used within the ShortCircuitOperator example.

#### Response Example
{
  "module": "airflow.providers.standard.example_dags.example_short_circuit_operator",
  "attributes": {
    "cond_true": true
  }
}
```

--------------------------------

### GET /system/yandex/example_yandexcloud_yq

Source: https://airflow.apache.org/docs/apache-airflow-providers-yandex/stable/_api/tests/system/yandex/example_yandexcloud_yq/index.html

Retrieves the configuration attributes and module definitions for the Yandex Cloud YQ example DAG.

```APIDOC
## GET /system/yandex/example_yandexcloud_yq

### Description
Returns the metadata and task identifiers for the example_yandexcloud_yq DAG used in system testing.

### Method
GET

### Endpoint
/system/yandex/example_yandexcloud_yq

### Parameters
None

### Response
#### Success Response (200)
- **ENV_ID** (string) - The environment identifier for the test.
- **DAG_ID** (string) - The unique identifier for the DAG ('example_yandexcloud_yq').
- **run_this_last** (object) - Reference to the final task in the DAG execution flow.
- **test_run** (object) - Reference to the primary test execution task.

#### Response Example
{
  "ENV_ID": "test-env-001",
  "DAG_ID": "example_yandexcloud_yq",
  "run_this_last": "task_instance",
  "test_run": "task_instance"
}
```

--------------------------------

### Install Exasol Provider with Extras

Source: https://airflow.apache.org/docs/apache-airflow-providers-exasol/stable/index.html

Demonstrates how to install the Exasol provider package along with specific cross-provider dependencies using pip. This is useful for enabling all features of the provider.

```bash
pip install apache-airflow-providers-exasol[common.compat]
```

--------------------------------

### Helm Install with Airflow Kerberos Parameters

Source: https://airflow.apache.org/docs/helm-chart/stable/parameters-ref.html

Demonstrates how to install the Apache Airflow Helm chart and enable Kerberos authentication by setting specific parameters using the `--set` flag. This method allows for direct configuration during the installation process.

```bash
helm install my-release apache-airflow/airflow \
  --set executor=CeleryExecutor \
  --set enablePodLaunching=false \
  --set kerberos.enabled=true \
  --set kerberos.principal=airflow@EXAMPLE.COM \
  --set kerberos.keytabPath=/etc/airflow.keytab
```

--------------------------------

### Prerequisites and Installation

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/bedrock.html

Instructions on setting up AWS resources and installing the necessary Airflow provider package for Amazon integration.

```APIDOC
## Prerequisites

To use these operators, you must do a few things:

* Create necessary resources using AWS Console or AWS CLI.
* Install API libraries via **pip**.

```pip
pip install 'apache-airflow[amazon]'
```

Detailed information is available in the [Installation of Airflow®](link-to-installation-guide).

* Setup Connection.
```

--------------------------------

### Start Neptune Database Cluster Operator

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/neptune.html

Demonstrates how to use the NeptuneStartDbClusterOperator to start an existing Amazon Neptune database cluster. The operator can be run in deferrable mode if aiobotocore is installed.

```python
start_cluster = NeptuneStartDbClusterOperator(task_id="start_task", db_cluster_id=cluster_id)
```

--------------------------------

### Install MySQL Provider with Extras

Source: https://airflow.apache.org/docs/apache-airflow-providers-mysql/stable/index.html

Demonstrates how to install the MySQL provider package along with optional extra dependencies for other cloud services. This allows for extended functionality by including specific integrations.

```bash
pip install apache-airflow-providers-mysql[amazon]
```

--------------------------------

### Setup Without Teardown

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/setup-and-teardown.html

Shows a scenario where a setup task is used without an explicit teardown task.

```APIDOC
## Setup Without Teardown

### Description
This example illustrates a setup task used without a corresponding teardown task. In this case, all tasks downstream of the setup task are considered to require it.

### Method
N/A (Conceptual Example)

### Endpoint
N/A (Conceptual Example)

### Parameters
N/A

### Request Example
```python
create_cluster >> run_query >> other_task
```

### Response
N/A
```

--------------------------------

### SnowparkOperator Example: Setup and Check Data

Source: https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/operators/snowpark.html

Demonstrates using the SnowparkOperator to set up data in Snowflake and then verify the number of rows. It shows two methods for accessing the Snowpark session: injecting it as an argument or retrieving it using get_active_session.

```python
from airflow.providers.snowflake.operators.snowflake import SnowparkOperator
from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session

with DAG(...) as dag:
    def setup_data(session: Session):
        # The Snowpark session object is injected as an argument
        data = [
            (1, 0, 5, "Product 1", "prod-1", 1, 10),
            (2, 1, 5, "Product 1A", "prod-1-A", 1, 20),
            (3, 1, 5, "Product 1B", "prod-1-B", 1, 30),
            (4, 0, 10, "Product 2", "prod-2", 2, 40),
            (5, 4, 10, "Product 2A", "prod-2-A", 2, 50),
            (6, 4, 10, "Product 2B", "prod-2-B", 2, 60),
            (7, 0, 20, "Product 3", "prod-3", 3, 70),
            (8, 7, 20, "Product 3A", "prod-3-A", 3, 80),
            (9, 7, 20, "Product 3B", "prod-3-B", 3, 90),
            (10, 0, 50, "Product 4", "prod-4", 4, 100),
            (11, 10, 50, "Product 4A", "prod-4-A", 4, 100),
            (12, 10, 50, "Product 4B", "prod-4-B", 4, 100),
        ]
        columns = ["id", "parent_id", "category_id", "name", "serial_number", "key", "3rd"]
        df = session.create_dataframe(data, schema=columns)
        table_name = "sample_product_data"
        df.write.save_as_table(table_name, mode="overwrite")
        return table_name

    setup_data_operator = SnowparkOperator(
        task_id="setup_data",
        python_callable=setup_data,
        dag=dag,
    )

    def check_num_rows(table_name: str):
        # Alternatively, retrieve the Snowpark session object using `get_active_session`
        session = get_active_session()
        df = session.table(table_name)
        assert df.count() == 12

    check_num_rows_operator = SnowparkOperator(
        task_id="check_num_rows",
        python_callable=check_num_rows,
        op_kwargs={"table_name": "{{ task_instance.xcom_pull(task_ids='setup_data') }}"},
        dag=dag,
    )

    setup_data_operator >> check_num_rows_operator

```

--------------------------------

### Install SFTP Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-sftp/stable/index.html

Shows the basic command to install the apache-airflow-providers-sftp package on top of an existing Airflow installation using pip.

```bash
pip install apache-airflow-providers-sftp
```

--------------------------------

### Install Additional Python Requirements at Runtime

Source: https://airflow.apache.org/docs/docker-stack/entrypoint.html

Shows how to dynamically install extra Python packages when the container starts using the _PIP_ADDITIONAL_REQUIREMENTS variable. This is intended strictly for development and testing environments.

```bash
docker run -it -p 8080:8080 \
  --env "_PIP_ADDITIONAL_REQUIREMENTS=lxml==4.6.3 charset-normalizer==1.4.1" \
  --env "_AIRFLOW_DB_MIGRATE=true" \
  --env "_AIRFLOW_WWW_USER_CREATE=true" \
  --env "_AIRFLOW_WWW_USER_PASSWORD_CMD=echo admin" \
    apache/airflow:2.11.2-python3.10 webserver
```

--------------------------------

### Basic Setup/Teardown Task Definition in Airflow

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/setup-and-teardown.html

Demonstrates how to define setup and teardown tasks using `as_setup()` and `as_teardown()` methods in Airflow. It shows the basic dependency chaining and how to link a teardown task with its setup task.

```python
create_cluster.as_setup() >> run_query >> delete_cluster.as_teardown()
create_cluster >> delete_cluster
```

```python
create_cluster >> run_query >> delete_cluster.as_teardown(setups=create_cluster)
```

--------------------------------

### Install Kind and Create Cluster

Source: https://airflow.apache.org/docs/helm-chart/stable/quick-start.html

This snippet shows how to install the 'kind' tool and create a Kubernetes cluster for testing Airflow. It includes commands to create the cluster and verify its status.

```bash
kind create cluster --image kindest/node:v1.30.13
kubectl cluster-info --context kind-kind
```

--------------------------------

### setup

Source: https://airflow.apache.org/docs/task-sdk/stable/api.html

Decorator or function to set up resources or configurations, often used for initialization tasks.

```APIDOC
## setup

### Description
Decorator or function to set up resources or configurations.

### Parameters
#### Parameters
- **func** (collections.abc.Callable)
```

--------------------------------

### GET /api/v2/providers

Source: https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html

Retrieve a list of installed providers.

```APIDOC
## GET /api/v2/providers

### Description
Get a list of all installed providers in the Airflow instance.

### Method
GET

### Endpoint
/api/v2/providers

### Parameters
#### Query Parameters
- **limit** (integer) - Optional - Limit results (Default: 50)
- **offset** (integer) - Optional - Offset (Default: 0)

### Response
#### Success Response (200)
- **providers** (array) - List of provider objects
- **total_entries** (integer) - Total count
```

--------------------------------

### Initialize and Use AzureComputeHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/_api/airflow/providers/microsoft/azure/hooks/compute/index.html

Demonstrates how to instantiate the AzureComputeHook and perform basic VM lifecycle operations like starting and stopping an instance.

```python
from airflow.providers.microsoft.azure.hooks.compute import AzureComputeHook

hook = AzureComputeHook(azure_conn_id='my_azure_conn')

# Start a VM
hook.start_instance(resource_group_name='my_rg', vm_name='my_vm')

# Stop a VM
hook.stop_instance(resource_group_name='my_rg', vm_name='my_vm')

# Get power state
state = hook.get_power_state(resource_group_name='my_rg', vm_name='my_vm')
print(f'VM state: {state}')
```

--------------------------------

### GET /tests/system/docker/example_docker_swarm

Source: https://airflow.apache.org/docs/apache-airflow-providers-docker/stable/_api/tests/system/docker/example_docker_swarm/index.html

Retrieves the module attributes and configuration constants for the Docker Swarm example DAG system test.

```APIDOC
## GET /tests/system/docker/example_docker_swarm

### Description
This module defines the constants and test execution objects for the Docker Swarm integration test DAG.

### Method
GET

### Endpoint
/tests/system/docker/example_docker_swarm

### Parameters
None

### Request Example
GET /tests/system/docker/example_docker_swarm

### Response
#### Success Response (200)
- **DAG_ID** (string) - The identifier for the Docker Swarm DAG, set to 'docker_swarm_dag'.
- **ENV_ID** (string) - The environment identifier used for the test.
- **t1** (object) - The primary task object defined in the test.
- **test_run** (object) - The test execution instance.

#### Response Example
{
  "DAG_ID": "docker_swarm_dag",
  "ENV_ID": "example_env",
  "t1": "<TaskInstance>",
  "test_run": "<TestRun>"
}
```

--------------------------------

### Install Discord Provider with Extras

Source: https://airflow.apache.org/docs/apache-airflow-providers-discord/stable/index.html

Demonstrates how to install the apache-airflow-providers-discord package with optional extras, such as 'common.compat', to include additional dependencies.

```bash
pip install apache-airflow-providers-discord[common.compat]
```

--------------------------------

### Initialize SparkSubmitHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-spark/stable/_api/airflow/providers/apache/spark/hooks/spark_submit/index.html

Demonstrates how to instantiate the SparkSubmitHook with basic configuration parameters to prepare for a Spark job submission.

```python
from airflow.providers.apache.spark.hooks.spark_submit import SparkSubmitHook

spark_hook = SparkSubmitHook(
    conn_id='spark_default',
    name='my-spark-job',
    executor_memory='2G',
    num_executors=4,
    verbose=True
)
```

--------------------------------

### Install Datadog Provider with Extras

Source: https://airflow.apache.org/docs/apache-airflow-providers-datadog/stable/index.html

Command to install the Datadog provider along with specific cross-provider dependencies using extras.

```bash
pip install apache-airflow-providers-datadog[common.compat]
```

--------------------------------

### Install Teradata Provider with Extras

Source: https://airflow.apache.org/docs/apache-airflow-providers-teradata/stable/index.html

Demonstrates how to install the Teradata provider package along with optional extra dependencies, such as for Amazon integration. This allows for extended functionality beyond basic Teradata connectivity.

```bash
pip install apache-airflow-providers-teradata[amazon]
```

--------------------------------

### Airflow API Server Deployment Options

Source: https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/web-stack.html

Demonstrates how to start the Airflow API server, including options to serve all applications, or to separate the core and execution API servers for independent scaling or deployment.

```bash
airflow api-server
# same as
airflow api-server --apps all
# or
airflow api-server --apps core,execution
```

```bash
# serve only the Core API Server
airflow api-server --apps core
# serve only the Execution API Server
airflow api-server --apps execution
```

--------------------------------

### Get Airflow OpenSearch Provider Info (Python)

Source: https://airflow.apache.org/docs/apache-airflow-providers-opensearch/stable/_api/airflow/providers/opensearch/index.html

Retrieves information about the installed Airflow OpenSearch provider, including its version. This is useful for verifying the provider's installation and compatibility.

```python
from airflow.providers.opensearch.get_provider_info import get_provider_info

provider_info = get_provider_info()
print(provider_info)
```

--------------------------------

### Install Provider with Optional Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-common-compat/index.html

Command to install the provider package along with specific extras, such as OpenLineage support, to enable additional functionality.

```bash
pip install apache-airflow-providers-common-compat[openlineage]
```

--------------------------------

### Install Samba Provider with Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-samba/stable/index.html

Commands to install the Samba provider package and its optional cross-provider dependencies using pip.

```bash
pip install apache-airflow-providers-samba
pip install apache-airflow-providers-samba[common.compat]
```

--------------------------------

### Install Airflow Provider with Extras (Bash)

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/index.html

Demonstrates how to install a specific Apache Airflow provider package with its associated extras using pip. This is useful for installing dependencies required for specific functionalities of a provider.

```bash
pip install apache-airflow-providers-google[amazon]
```

--------------------------------

### Install Airflow with Extras and Providers using Constraints

Source: https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html

This command installs a specific version of Apache Airflow along with specified extras (like async) and providers (like postgres and google). It uses a constraint file URL to ensure compatibility with the Airflow version. This method installs providers that were available at the time of the Airflow release.

```bash
AIRFLOW_VERSION=3.1.8
PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow[async,postgres,google]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

--------------------------------

### Package Airflow Plugin with Setuptools

Source: https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/plugins.html

Illustrates how to package an Airflow plugin as a Python package and load it automatically using setuptools entry points. This involves defining the plugin class in a Python file and specifying the entry point in `pyproject.toml`.

```python
# my_package/my_plugin.py
from airflow.plugins_manager import AirflowPlugin

class MyAirflowPlugin(AirflowPlugin):
    name = "my_namespace"
```

```toml
[project.entry-points."airflow.plugins"]
my_plugin = "my_package.my_plugin:MyAirflowPlugin"
```

--------------------------------

### GET /airflow/providers/slack/version

Source: https://airflow.apache.org/docs/apache-airflow-providers-slack/stable/_api/airflow/providers/slack/index.html

Retrieves the current version information for the installed Slack provider package.

```APIDOC
## GET /airflow/providers/slack/version

### Description
Returns the version string of the currently installed airflow.providers.slack package.

### Method
GET

### Endpoint
/airflow/providers/slack/version

### Parameters
None

### Response
#### Success Response (200)
- **version** (string) - The current version of the Slack provider package.

#### Response Example
{
  "version": "9.9.0"
}
```

--------------------------------

### Start Airflow Celery Flower UI

Source: https://airflow.apache.org/docs/apache-airflow-providers-celery/stable/celery_executor.html

Launches Celery Flower, a web-based monitoring tool for Celery workers and tasks. Requires the 'flower' Python library to be installed.

```bash
airflow celery flower
```

--------------------------------

### GET /airflow/providers/github/version

Source: https://airflow.apache.org/docs/apache-airflow-providers-github/stable/_api/airflow/providers/github/index.html

Retrieves the current version information for the installed GitHub provider package.

```APIDOC
## GET /airflow/providers/github/version

### Description
Returns the version string for the airflow.providers.github package.

### Method
GET

### Endpoint
/airflow/providers/github/version

### Parameters
None

### Response
#### Success Response (200)
- **version** (string) - The current version of the GitHub provider.

#### Response Example
{
  "version": "2.11.1"
}
```

--------------------------------

### System Test Setup for PgVector Example DAG

Source: https://airflow.apache.org/docs/apache-airflow-providers-pgvector/stable/_modules/tests/system/pgvector/example_pgvector.html

This Python code snippet is part of the system tests for the PgVector provider. It imports the `get_test_run` utility to enable running the example DAG within a pytest environment, as detailed in the system tests README.

```python
from tests_common.test_utils.system_tests import get_test_run  # noqa: E402

# Needed to run the example DAG with pytest (see: tests/system/README.md#run_via_pytest)


[docs]
test_run = get_test_run(dag)

```

--------------------------------

### Install Airflow with Specific Providers

Source: https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html

Demonstrates how to install a specific version of Apache Airflow alongside a specific provider version. This approach avoids using constraint files to ensure the requested versions are strictly enforced.

```bash
pip install "apache-airflow==3.1.8" "apache-airflow-providers-google==8.0.0"
```

--------------------------------

### Install Provider with Extra Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-openlineage/index.html

Command to install the OpenLineage provider along with specific cross-provider dependencies using extras.

```bash
pip install apache-airflow-providers-openlineage[common.compat]
```

--------------------------------

### Install Big Data Stack in Dockerfile

Source: https://airflow.apache.org/docs/docker-stack/recipes.html

Installs Java, Apache Hadoop, Apache Hive, and the GCS connector within a Docker environment. This setup prepares the container for big data processing tasks by configuring environment variables and paths.

```dockerfile
RUN mkdir -pv /usr/share/man/man1 && mkdir -pv /usr/share/man/man7 && curl -fsSL https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | apt-key add - && echo "deb https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/ $(lsb_release -cs) main" > /etc/apt/sources.list.d/adoptopenjdk.list && apt-get update && apt-get install --no-install-recommends -y adoptopenjdk-8-hotspot-jre && apt-get autoremove -yqq --purge && apt-get clean && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME=/usr/lib/jvm/adoptopenjdk-8-hotspot-jre-amd64
RUN mkdir -p /opt/spark/jars
ARG HADOOP_VERSION=2.10.1
ENV HADOOP_HOME=/opt/hadoop
RUN HADOOP_URL="https://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz" && curl 'https://dist.apache.org/repos/dist/release/hadoop/common/KEYS' | gpg --import - && curl -fSL "$HADOOP_URL" -o /tmp/hadoop.tar.gz && curl -fSL "$HADOOP_URL.asc" -o /tmp/hadoop.tar.gz.asc && gpg --verify /tmp/hadoop.tar.gz.asc && mkdir -p "${HADOOP_HOME}" && tar -xvf /tmp/hadoop.tar.gz -C "${HADOOP_HOME}" --strip-components=1 && rm /tmp/hadoop.tar.gz /tmp/hadoop.tar.gz.asc
ARG HIVE_VERSION=2.3.7
ENV HIVE_HOME=/opt/hive
RUN HIVE_URL="https://archive.apache.org/dist/hive/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz" && curl -fSL 'https://downloads.apache.org/hive/KEYS' | gpg --import - && curl -fSL "$HIVE_URL" -o /tmp/hive.tar.gz && curl -fSL "$HIVE_URL.asc" -o /tmp/hive.tar.gz.asc && gpg --verify /tmp/hive.tar.gz.asc && mkdir -p "${HIVE_HOME}" && tar -xf /tmp/hive.tar.gz -C "${HIVE_HOME}" --strip-components=1 && rm /tmp/hive.tar.gz /tmp/hive.tar.gz.asc
ARG GCS_VARIANT="hadoop2"
ARG GCS_VERSION="2.1.5"
RUN GCS_JAR_PATH="/opt/spark/jars/gcs-connector-${GCS_VARIANT}-${GCS_VERSION}.jar" && GCS_JAR_URL="https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-${GCS_VARIANT}-${GCS_VERSION}.jar" && curl "${GCS_JAR_URL}" -o "${GCS_JAR_PATH}"
```

--------------------------------

### Initialize and Use AsanaHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-asana/stable/_api/airflow/providers/asana/hooks/asana/index.html

Demonstrates how to instantiate the AsanaHook and use it to perform basic task operations like creating and finding tasks.

```python
from airflow.providers.asana.hooks.asana import AsanaHook

# Initialize the hook
hook = AsanaHook(asana_conn_id='my_asana_connection')

# Create a task
task = hook.create_task(task_name='New Task', params={'notes': 'Task details'})

# Find tasks
matching_tasks = hook.find_task(params={'workspace': '12345'})
```

--------------------------------

### GET /airflow/providers/vertica/info

Source: https://airflow.apache.org/docs/apache-airflow-providers-vertica/stable/_api/airflow/providers/vertica/index.html

Retrieves information about the installed Vertica provider package, including the current version.

```APIDOC
## GET /airflow/providers/vertica/info

### Description
Retrieves the metadata and current version of the airflow.providers.vertica package.

### Method
GET

### Endpoint
/airflow/providers/vertica/info

### Parameters
None

### Response
#### Success Response (200)
- **version** (string) - The current version of the Vertica provider (e.g., '4.3.1').

#### Response Example
{
  "version": "4.3.1"
}
```

--------------------------------

### Install FTP Provider with Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-ftp/index.html

Command to install the FTP provider package along with specific cross-provider dependencies such as common.compat.

```bash
pip install apache-airflow-providers-ftp[common.compat]
```

--------------------------------

### GET /airflow/providers/singularity/version

Source: https://airflow.apache.org/docs/apache-airflow-providers-singularity/stable/_api/airflow/providers/singularity/index.html

Retrieves the current version of the Singularity provider package installed in the Airflow environment.

```APIDOC
## GET /airflow/providers/singularity/version

### Description
Returns the version string for the airflow.providers.singularity package.

### Method
GET

### Endpoint
/airflow/providers/singularity/__version__

### Parameters
None

### Request Example
GET /airflow/providers/singularity/__version__

### Response
#### Success Response (200)
- **version** (string) - The current version of the provider package (e.g., '3.9.3')

#### Response Example
{
  "version": "3.9.3"
}
```

--------------------------------

### Install Go Module Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/go_module_utils/index.html

Installs the dependencies for a specified Go module.

```APIDOC
## install_dependencies

### Description
Install dependencies for a Go module.

### Parameters
#### Path Parameters
- **go_module_path** (str) - Required - The path to the directory containing the Go module.

### Request Example
```python
install_dependencies(go_module_path="/path/to/module")
```

### Response
#### Success Response (200)
No specific response body is detailed, indicating an in-place modification or a void return.

#### Response Example
None
```

--------------------------------

### Install and Verify Package

Source: https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/modules_management.html

Installs the generated wheel file using pip and verifies the package functionality via the Python interpreter.

```bash
pip install dist/airflow_operators-0.0.0-py3-none-any.whl
```

```python
import airflow_operators
```

--------------------------------

### Install Google Provider with Apache Beam Support (Older PIP)

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/changelog.html

This command demonstrates how to install the Google provider with the 'apache.beam' extra, enabling compatibility with older PIP versions (<= 20.2.4). This ensures the previous behavior and functionality, though potential BigQuery operator issues might arise.

```bash
pip install apache-airflow-providers-google[apache.beam]
```

--------------------------------

### GET /providers/microsoft/winrm/info

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-winrm/stable/_api/airflow/providers/microsoft/winrm/index.html

Retrieves information about the installed WinRM provider package, including versioning and available submodules.

```APIDOC
## GET /providers/microsoft/winrm/info

### Description
Returns metadata and versioning information for the airflow.providers.microsoft.winrm package.

### Method
GET

### Endpoint
/providers/microsoft/winrm/info

### Parameters
None

### Request Example
GET /providers/microsoft/winrm/info

### Response
#### Success Response (200)
- **version** (string) - The current version of the provider (e.g., '3.14.1')
- **submodules** (array) - List of available submodules including hooks, operators, and triggers.

#### Response Example
{
  "version": "3.14.1",
  "submodules": [
    "airflow.providers.microsoft.winrm.hooks",
    "airflow.providers.microsoft.winrm.operators",
    "airflow.providers.microsoft.winrm.triggers"
  ]
}
```

--------------------------------

### GET /airflow/providers/google/version

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/index.html

Retrieves the current version information for the installed Apache Airflow Google provider package.

```APIDOC
## GET /airflow/providers/google/version

### Description
Returns the current version string of the airflow.providers.google package.

### Method
GET

### Endpoint
/airflow/providers/google/version

### Parameters
None

### Request Example
GET /airflow/providers/google/version

### Response
#### Success Response (200)
- **version** (string) - The current version of the Google provider package.

#### Response Example
{
  "version": "21.0.0"
}
```

--------------------------------

### Start Airflow Celery Worker

Source: https://airflow.apache.org/docs/apache-airflow-providers-celery/stable/cli-ref.html

This command starts a Celery worker node for Apache Airflow. It supports various configuration options to manage worker behavior, logging, and scaling. Ensure Celery and its dependencies are installed.

```bash
airflow celery worker [-h] [-a AUTOSCALE] [-H CELERY_HOSTNAME] [-c CONCURRENCY] [-D] [-l LOG_FILE] [--pid [PID]] [-q QUEUES] [-s] [--stderr STDERR] [--stdout STDOUT] [-t TEAM] [-u UMASK] [-v] [--without-gossip] [--without-mingle]
```

--------------------------------

### Configure Oracle Connection Host Examples

Source: https://airflow.apache.org/docs/apache-airflow-providers-oracle/stable/connections/oracle.html

Demonstrates different ways to specify the Oracle connection host and schema. This includes using a full TNS description, or separate host and schema parameters.

```text
Host = "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=dbhost.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=orclpdb1)))"

or

Host = "dbhost.example.com"
Schema = "orclpdb1"

or

Host = "dbhost.example.com"
Schema = "orcl"
```

--------------------------------

### Install Apache Pig Provider with Extras

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-pig/stable/index.html

Demonstrates how to install the apache-airflow-providers-apache-pig package with specific extra dependencies, such as 'common.compat'. This is useful for enabling all features of the provider.

```bash
pip install apache-airflow-providers-apache-pig[common.compat]
```

--------------------------------

### Airflow TaskFlow API: Setup and Teardown Tasks

Source: https://airflow.apache.org/docs/task-sdk/stable/examples.html

Illustrates the use of setup and teardown tasks within Airflow's TaskFlow API. It shows how to define tasks that act as setups or teardowns using decorators and how to link them with regular tasks and TaskGroups to manage resources or states.

```python
import pendulum

from airflow.sdk import DAG, setup, task, task_group, teardown

with DAG(
    dag_id="example_setup_teardown_taskflow",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
) as dag:

    @task
    def my_first_task():
        print("Hello 1")

    @task
    def my_second_task():
        print("Hello 2")

    @task
    def my_third_task():
        print("Hello 3")

    task_1 = my_first_task()
    task_2 = my_second_task()
    task_3 = my_third_task()
    task_1 >> task_2 >> task_3.as_teardown(setups=task_1)

    @setup
    def outer_setup():
        print("I am outer_setup")
        return "some cluster id"

    @teardown
    def outer_teardown(cluster_id):
        print("I am outer_teardown")
        print(f"Tearing down cluster: {cluster_id}")

    @task
    def outer_work():
        print("I am just a normal task")

    @task_group
    def section_1():
        @setup
        def inner_setup():
            print("I set up")
            return "some_cluster_id"

        @task
        def inner_work(cluster_id):
            print(f"doing some work with {cluster_id=}")

        @teardown
        def inner_teardown(cluster_id):
            print(f"tearing down {cluster_id=}")

        inner_setup_task = inner_setup()
        inner_work(inner_setup_task) >> inner_teardown(inner_setup_task)

    with outer_teardown(outer_setup()):
        outer_work()
        section_1()
```

--------------------------------

### GET /tests/system/postgres/example_postgres

Source: https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/_api/tests/system/postgres/example_postgres/index.html

Retrieves the configuration and attributes for the Postgres system test DAG.

```APIDOC
## GET /tests/system/postgres/example_postgres

### Description
This endpoint provides access to the attributes and module contents of the postgres_operator_dag system test.

### Method
GET

### Endpoint
/tests/system/postgres/example_postgres

### Parameters
None

### Response
#### Success Response (200)
- **ENV_ID** (string) - The environment identifier for the test.
- **DAG_ID** (string) - The identifier for the DAG, defaults to 'postgres_operator_dag'.
- **create_pet_table** (callable) - Utility function for creating the test table.
- **test_run** (callable) - Execution entry point for the system test.

#### Response Example
{
  "ENV_ID": "test-env-01",
  "DAG_ID": "postgres_operator_dag"
}
```

--------------------------------

### tests.system.alibaba.example_oss_bucket

Source: https://airflow.apache.org/docs/apache-airflow-providers-alibaba/stable/_api/tests/system/alibaba/example_oss_bucket/index.html

Documentation for the Alibaba OSS bucket system test module, including environment variables and test execution attributes.

```APIDOC
## Module: tests.system.alibaba.example_oss_bucket

### Description
This module provides system tests for Alibaba OSS bucket operations within Apache Airflow. It defines the necessary environment variables and test execution hooks.

### Attributes
- **ENV_ID** (string) - The environment identifier for the test suite.
- **DAG_ID** (string) - The identifier for the OSS bucket DAG ('oss_bucket_dag').
- **REGION** (string) - The cloud region where the bucket operations are performed.

### Functions
- **create_bucket** - Function responsible for initializing the creation of an OSS bucket.
- **test_run** - The primary execution entry point for the system test.
```

--------------------------------

### Airflow System Test Execution Setup

Source: https://airflow.apache.org/docs/apache-airflow-providers-teradata/stable/operators/tpt.html

This code sets up the execution of an Airflow system test using the 'get_test_run' utility. It's designed to be used with pytest for running example DAGs, as detailed in the system tests README. This facilitates testing DAGs in a controlled environment.

```python
from tests_common.test_utils.system_tests import get_test_run  # noqa: E402

# Needed to run the example DAG with pytest (see: tests/system/README.md#run_via_pytest)
test_run = get_test_run(dag)
```

--------------------------------

### Compile and Install SQLite from Source

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html

Downloads, configures, and installs the latest version of SQLite from source, including essential extensions and flags for Airflow compatibility.

```bash
wget https://www.sqlite.org/src/tarball/sqlite.tar.gz
tar xzf sqlite.tar.gz
cd sqlite/
export CFLAGS="-DSQLITE_ENABLE_FTS3 -DSQLITE_ENABLE_FTS3_PARENTHESIS -DSQLITE_ENABLE_FTS4 -DSQLITE_ENABLE_FTS5 -DSQLITE_ENABLE_JSON1 -DSQLITE_ENABLE_LOAD_EXTENSION -DSQLITE_ENABLE_RTREE -DSQLITE_ENABLE_STAT4 -DSQLITE_ENABLE_UPDATE_DELETE_LIMIT -DSQLITE_SOUNDEX -DSQLITE_TEMP_STORE=3 -DSQLITE_USE_URI -O2 -fPIC"
export PREFIX="/usr/local"
LIBS="-lm" ./configure --disable-tcl --enable-shared --enable-tempstore=always --prefix="$PREFIX"
make
make install
```

--------------------------------

### GET /sql/instances/{instance}/overview

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/links/cloud_sql/index.html

Retrieves the link to the Google Cloud SQL Instance overview page.

```APIDOC
## GET /sql/instances/{instance}/overview

### Description
Constructs a URL to the overview page of a specific Google Cloud SQL instance.

### Method
GET

### Endpoint
/sql/instances/{instance}/overview?project={project_id}

### Parameters
#### Path Parameters
- **instance** (string) - Required - The ID of the Cloud SQL instance.

#### Query Parameters
- **project_id** (string) - Required - The Google Cloud project ID.

### Response
#### Success Response (200)
- **url** (string) - The generated URL to the Cloud SQL instance overview.
```

--------------------------------

### Install Apache Airflow Task SDK

Source: https://airflow.apache.org/docs/task-sdk/stable/index.html

Command to install the Task SDK package via pip.

```bash
pip install apache-airflow-task-sdk
```

--------------------------------

### Install Alibaba Provider with Common Compat

Source: https://airflow.apache.org/docs/apache-airflow-providers-alibaba/stable/index.html

Demonstrates how to install the Alibaba provider for Airflow, including the common compatibility extras. This ensures that shared functionalities across providers are available.

```bash
pip install apache-airflow-providers-alibaba[common.compat]
```

--------------------------------

### Install Sendgrid Provider with Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-sendgrid/stable/index.html

Command to install the Sendgrid provider package along with specific cross-provider dependencies using extras.

```bash
pip install apache-airflow-providers-sendgrid[common.compat]
```

--------------------------------

### Install KEDA via Helm

Source: https://airflow.apache.org/docs/helm-chart/stable/keda.html

Commands to add the KEDA Helm repository, create the necessary namespace, and install the KEDA controller into the Kubernetes cluster.

```bash
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
kubectl create namespace keda
helm install keda kedacore/keda \
  --namespace keda \
  --version "v2.0.0"
```

--------------------------------

### Install Provider with Cross-Provider Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-singularity/stable/index.html

Command to install the Singularity provider along with specific cross-provider dependencies, such as common.compat.

```bash
pip install apache-airflow-providers-singularity[common.compat]
```

--------------------------------

### Snowflake Snowpark Decorator Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/_api/tests/system/snowflake/example_snowpark_decorator/index.html

Demonstrates the setup and execution of a test using Snowflake Snowpark decorators in an Airflow DAG. It includes constants for connection and DAG IDs, and a function to set up data using the Snowpark session.

```python
from airflow.decorators import dag, task
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook

SNOWFLAKE_CONN_ID = "my_snowflake_conn"
DAG_ID = "example_snowpark_decorator"

@dag(
    dag_id=DAG_ID,
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["snowflake", "snowpark", "example"],
)
def example_snowpark_decorator():
    @task
    def setup_data(session):
        # Example: Create a DataFrame
        data = [Row(col1='value1'), Row(col2='value2')]
        df = session.create_dataframe(data)
        df.show()
        return df.collect()

    @task
    def run_snowpark_query(session):
        # Example: Execute a Snowpark query
        result = session.sql("SELECT current_version()").collect()
        print(result)

    # Using the Snowpark decorator to get a session
    # The session is automatically passed to the decorated task
    setup_data_task = setup_data()
    run_snowpark_query_task = run_snowpark_query()

    setup_data_task >> run_snowpark_query_task

example_snowpark_decorator()

```

--------------------------------

### Install OpenSearch Provider with Extra Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-opensearch/stable/index.html

Command to install the OpenSearch provider package along with specific cross-provider dependencies like common.compat.

```bash
pip install apache-airflow-providers-opensearch[common.compat]
```

--------------------------------

### Get Airflow Git Provider Version

Source: https://airflow.apache.org/docs/apache-airflow-providers-git/stable/_api/airflow/providers/git/index.html

Retrieves the version of the airflow.providers.git package. This is useful for checking compatibility and understanding the installed version.

```python
import airflow.providers.git

__version__ = airflow.providers.git.__version__
print(f"Airflow Git Provider Version: {__version__}")
```

--------------------------------

### Install Go in Dockerfile

Source: https://airflow.apache.org/docs/docker-stack/recipes.html

This shell script detects the system architecture, downloads the appropriate Go binary, and extracts it to the installation directory. It also sets the necessary environment variables GOROOT and PATH to ensure Go is accessible.

```bash
RUN if [[ "$(uname -a)" = *"x86_64"* ]] ; then export ARCH=amd64 ; else export ARCH=arm64 ; fi \
    && DOWNLOAD_URL="https://dl.google.com/go/go${GO_VERSION}.linux-${ARCH}.tar.gz" \
    && TMP_DIR="$(mktemp -d)" \
    && curl -fL "${DOWNLOAD_URL}" --output "${TMP_DIR}/go.linux-${ARCH}.tar.gz" \
    && mkdir -p "${GO_INSTALL_DIR}" \
    && tar xzf "${TMP_DIR}/go.linux-${ARCH}.tar.gz" -C "${GO_INSTALL_DIR}" --strip-components=1 \
    && rm -rf "${TMP_DIR}"

ENV GOROOT=/usr/local/go
ENV PATH="$GOROOT/bin:$PATH"
```

--------------------------------

### Install Samba Provider with Extra Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-samba/index.html

Command to install the Samba provider package along with specific cross-provider dependencies such as common.compat.

```bash
pip install apache-airflow-providers-samba[common.compat]
```

--------------------------------

### Pinecone Example Create Pod Index

Source: https://airflow.apache.org/docs/apache-airflow-providers-pinecone/stable/_api/tests/system/pinecone/example_create_pod_index/index.html

This section describes the system test module `example_create_pod_index` which is used for testing Pinecone index creation.

```APIDOC
## Module: tests.system.pinecone.example_create_pod_index

### Description
This module contains system tests for creating a Pinecone index.

### Attributes

- **index_name** (attribute) - Represents the name of the index.
- **create_index** (attribute) - Function or object related to index creation.
- **test_run** (attribute) - Represents a test run or execution context.
```

--------------------------------

### GET /batches/{session_id}/log

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-livy/stable/_api/airflow/providers/apache/livy/hooks/livy/index.html

Retrieves the logs for a specified batch session, allowing for pagination via start position and batch size.

```APIDOC
## GET /batches/{session_id}/log

### Description
Fetches logs for a given batch session. Supports pagination by specifying the starting line and the number of lines to retrieve.

### Method
GET

### Endpoint
/batches/{session_id}/log

### Parameters
#### Query Parameters
- **log_start_position** (int) - Required - The line number to start pulling logs from.
- **log_batch_size** (int) - Required - The number of lines to return in this request.

### Response
#### Success Response (200)
- **log** (list) - A list of log lines.

#### Response Example
{
  "id": 1,
  "from": 0,
  "size": 10,
  "log": ["Line 1", "Line 2"]
}
```

--------------------------------

### Install Trino Provider with Extra Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-trino/index.html

Command to install the Trino provider along with specific cross-provider dependencies using extras.

```bash
pip install apache-airflow-providers-trino[common.compat]
```

--------------------------------

### Install Salesforce Provider with Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-salesforce/index.html

Command to install the Salesforce provider package along with specific optional cross-provider dependencies.

```bash
pip install apache-airflow-providers-salesforce[common.compat]
```

--------------------------------

### Get Airflow Microsoft Psrp Provider Version

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-psrp/stable/_api/airflow/providers/microsoft/psrp/index.html

Retrieves the version string for the airflow.providers.microsoft.psrp package. This is useful for verifying the installed version or for programmatic checks.

```python
import airflow.providers.microsoft.psrp

print(airflow.providers.microsoft.psrp.__version__)
```

--------------------------------

### Initialize and Use GrpcHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-grpc/stable/_api/airflow/providers/grpc/hooks/grpc/index.html

Demonstrates how to instantiate the GrpcHook and execute a gRPC call using the run method.

```python
from airflow.providers.grpc.hooks.grpc import GrpcHook

hook = GrpcHook(grpc_conn_id='my_grpc_connection')
# Execute a gRPC call
response = hook.run(stub_class=MyStub, call_func='MyMethod', data={'key': 'value'})
```

--------------------------------

### Airflow Parallel Setups and Teardowns

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/setup-and-teardown.html

Shows how to define and execute setup and teardown tasks in parallel using Airflow. This pattern is useful for managing resources that need to be provisioned and de-provisioned concurrently.

```python
(
    [create_cluster, create_bucket]
    >> run_query
    >> [delete_cluster.as_teardown(setups=create_cluster), delete_bucket.as_teardown(setups=create_bucket)]
)
```

```python
with TaskGroup("setup") as tg_s:
    create_cluster = create_cluster()
    create_bucket = create_bucket()
run_query = run_query()
with TaskGroup("teardown") as tg_t:
    delete_cluster = delete_cluster().as_teardown(setups=create_cluster)
    delete_bucket = delete_bucket().as_teardown(setups=create_bucket)
tg_s >> run_query >> tg_t
```

--------------------------------

### Install SFTP Provider with Common Compat

Source: https://airflow.apache.org/docs/apache-airflow-providers-sftp/stable/index.html

Demonstrates how to install the SFTP provider package with the common.compat extra dependency. This is useful for leveraging shared functionalities across different Airflow providers.

```bash
pip install apache-airflow-providers-sftp[common.compat]
```

--------------------------------

### Install Apache Airflow with all core dependencies

Source: https://airflow.apache.org/docs/apache-airflow/stable/extra-packages-ref.html

Installs Apache Airflow with all optional core dependencies enabled. This provides a broader feature set than a standard installation without including every provider.

```bash
pip install apache-airflow[all-core]
```

--------------------------------

### DatabricksWorkflowTaskGroup Example in Airflow DAG

Source: https://airflow.apache.org/docs/apache-airflow-providers-databricks/stable/operators/workflow.html

This Python code demonstrates how to define a DatabricksWorkflowTaskGroup within an Airflow DAG. It includes configurations for job clusters, notebook parameters, and package installations. The example also shows how to define individual DatabricksNotebookOperator and DatabricksTaskOperator tasks within the task group and specifies their dependencies.

```python
task_group = DatabricksWorkflowTaskGroup(
        group_id=f"test_workflow_{USER}_{GROUP_ID}",
        databricks_conn_id=DATABRICKS_CONN_ID,
        job_clusters=job_cluster_spec,
        notebook_params={"ts": "{{ ts }}"},
        notebook_packages=[
            {
                "pypi": {
                    "package": "simplejson==3.18.0",  # Pin specification version of a package like this.
                    "repo": "https://pypi.org/simple",  # You can specify your required Pypi index here.
                }
            },
        ],
        extra_job_params={
            "email_notifications": {
                "on_start": [DATABRICKS_NOTIFICATION_EMAIL],
            },
        },
    )
    with task_group:
        notebook_1 = DatabricksNotebookOperator(
            task_id="workflow_notebook_1",
            databricks_conn_id=DATABRICKS_CONN_ID,
            notebook_path="/Shared/Notebook_1",
            notebook_packages=[{"pypi": {"package": "Faker"}}],
            source="WORKSPACE",
            job_cluster_key="Shared_job_cluster",
            execution_timeout=timedelta(seconds=600),
        )

        notebook_2 = DatabricksNotebookOperator(
            task_id="workflow_notebook_2",
            databricks_conn_id=DATABRICKS_CONN_ID,
            notebook_path="/Shared/Notebook_2",
            source="WORKSPACE",
            job_cluster_key="Shared_job_cluster",
            notebook_params={"foo": "bar", "ds": "{{ ds }}"},
        )

        task_operator_nb_1 = DatabricksTaskOperator(
            task_id="nb_1",
            databricks_conn_id=DATABRICKS_CONN_ID,
            job_cluster_key="Shared_job_cluster",
            task_config={
                "notebook_task": {
                    "notebook_path": "/Shared/Notebook_1",
                    "source": "WORKSPACE",
                },
                "libraries": [
                    {"pypi": {"package": "Faker"}},
                ],
            },
        )

        sql_query = DatabricksTaskOperator(
            task_id="sql_query",
            databricks_conn_id=DATABRICKS_CONN_ID,
            task_config={
                "sql_task": {
                    "query": {
                        "query_id": QUERY_ID,
                    },
                    "warehouse_id": WAREHOUSE_ID,
                }
            },
        )

        notebook_1 >> notebook_2 >> task_operator_nb_1 >> sql_query

```

--------------------------------

### Execute SQL Queries with SQLExecuteQueryOperator for Kylin

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-kylin/stable/operators.html

This example demonstrates how to use the SQLExecuteQueryOperator to perform DDL and DML operations on an Apache Kylin cluster. It includes tasks for creating, altering, inserting data into, selecting from, and dropping a table. Ensure the 'apache-airflow-providers-apache-kylin' package is installed.

```python
create_table_kylin_task = SQLExecuteQueryOperator(
        task_id="create_table_kylin",
        sql="""
            CREATE TABLE IF NOT EXISTS kylin_example (
                a VARCHAR(100),
                b INT
            )
        """,
    )

    alter_table_kylin_task = SQLExecuteQueryOperator(
        task_id="alter_table_kylin",
        sql="ALTER TABLE kylin_example ADD COLUMN c INT",
    )

    insert_data_kylin_task = SQLExecuteQueryOperator(
        task_id="insert_data_kylin",
        sql="""
            INSERT INTO kylin_example (a, b, c)
            VALUES ('x', 10, 1), ('y', 20, 2), ('z', 30, 3)
        """,
    )

    select_data_kylin_task = SQLExecuteQueryOperator(
        task_id="select_data_kylin",
        sql="SELECT * FROM kylin_example",
    )

    drop_table_kylin_task = SQLExecuteQueryOperator(
        task_id="drop_table_kylin",
        sql="DROP TABLE kylin_example",
    )
```

--------------------------------

### Install Kafka Provider with Common Compat

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-kafka/stable/index.html

Demonstrates how to install the apache-airflow-providers-apache-kafka package with the 'common.compat' extra dependency. This is useful for leveraging shared functionalities across different Airflow providers.

```bash
pip install apache-airflow-providers-apache-kafka[common.compat]
```

--------------------------------

### Install Presto Provider with Extras

Source: https://airflow.apache.org/docs/apache-airflow-providers-presto/index.html

Demonstrates how to install the Presto provider package for Airflow, including optional extras for cross-provider functionalities like common compatibility layers.

```bash
pip install apache-airflow-providers-presto[common.compat]
```

--------------------------------

### Initialize ObjectStoragePath

Source: https://airflow.apache.org/docs/apache-airflow/stable/tutorial/objectstorage.html

Demonstrates how to create an ObjectStoragePath instance using a URL string or by explicitly providing a connection ID for authentication.

```python
base = ObjectStoragePath("s3://aws_default@airflow-tutorial-data/")
ObjectStoragePath("s3://airflow-tutorial-data/", conn_id="aws_default")
```

--------------------------------

### Add PyPI Package to Airflow Docker Image

Source: https://airflow.apache.org/docs/docker-stack/build.html

This Dockerfile example shows how to install a Python package (lxml) from PyPI into an Airflow image using pip. It's recommended to install the same version of apache-airflow as the base image to avoid dependency conflicts. This operation must be done as the 'airflow' user.

```docker
FROM apache/airflow:2.11.2
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" lxml
```

--------------------------------

### KubernetesJobOperator Example DAG

Source: https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/_api/tests/system/cncf/kubernetes/example_kubernetes_job/index.html

This section provides details about an example DAG that utilizes the KubernetesJobOperator. It outlines the attributes and module contents relevant to this example.

```APIDOC
## tests.system.cncf.kubernetes.example_kubernetes_job

This is an example dag for using the KubernetesJobOperator.

### Attributes

| Attribute     | Description |
|---------------|-------------|
| `ENV_ID`      |             |
| `DAG_ID`      |             |
| `JOB_NAME`    |             |
| `JOB_NAMESPACE` |             |
| `k8s_job`     |             |
| `test_run`    |             |

### Module Contents

- `tests.system.cncf.kubernetes.example_kubernetes_job.ENV_ID`
- `tests.system.cncf.kubernetes.example_kubernetes_job.DAG_ID`
- `tests.system.cncf.kubernetes.example_kubernetes_job.JOB_NAME`
- `tests.system.cncf.kubernetes.example_kubernetes_job.JOB_NAMESPACE`
- `tests.system.cncf.kubernetes.example_kubernetes_job.k8s_job`
- `tests.system.cncf.kubernetes.example_kubernetes_job.test_run`
```

--------------------------------

### Install Keycloak Provider with Extra Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-keycloak/stable/index.html

Command to install the Keycloak provider along with specific cross-provider dependencies like common.compat.

```bash
pip install apache-airflow-providers-keycloak[common.compat]
```

--------------------------------

### Install Provider with Cross-Provider Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-openai/stable/index.html

Command to install the OpenAI provider package along with specific cross-provider extras like common.compat.

```bash
pip install apache-airflow-providers-openai[common.compat]
```

--------------------------------

### Install OpenSearch Provider Package

Source: https://airflow.apache.org/docs/apache-airflow-providers-opensearch/stable/index.html

Command to install the OpenSearch provider package into an existing Apache Airflow environment.

```bash
pip install apache-airflow-providers-opensearch
```

--------------------------------

### Add Python Packages from requirements.txt to Airflow Docker Image

Source: https://airflow.apache.org/docs/docker-stack/build.html

This example demonstrates adding multiple Python packages listed in a requirements.txt file to an Airflow Docker image. The requirements.txt file is copied to the image, and then pip is used to install the packages. Similar to individual package installation, this must be performed as the 'airflow' user.

```docker
FROM apache/airflow:2.11.2
COPY requirements.txt /
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
```

```text
lxml
beautifulsoup4
```

--------------------------------

### Install Slack Provider for Apache Airflow

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the Slack provider for Apache Airflow, enabling integration with Slack API and Incoming Webhooks. Pip is necessary for this installation.

```bash
pip install 'apache-airflow-providers-slack'
```

--------------------------------

### Install Apache Airflow with all optional dependencies

Source: https://airflow.apache.org/docs/apache-airflow/stable/extra-packages-ref.html

Installs Apache Airflow along with all available optional dependencies and providers. This is useful for comprehensive testing environments.

```bash
pip install apache-airflow[all]
```

--------------------------------

### Execute SQL Commands with SQLExecuteQueryOperator in Python

Source: https://airflow.apache.org/docs/apache-airflow-providers-exasol/stable/operators.html

This Python code demonstrates how to use the SQLExecuteQueryOperator to perform various SQL operations on an Exasol database. It includes examples for creating, altering, inserting data into, selecting from, and dropping tables. Ensure the 'apache-airflow-providers-exasol' package and its 'pyexasol' dependency are installed.

```python
create_table_exasol = SQLExecuteQueryOperator(
    task_id="create_table_exasol",
    sql="""
        CREATE OR REPLACE TABLE exasol_example (
            a VARCHAR(100),
            b DECIMAL(18,0)
        );
    ",
)

alter_table_exasol = SQLExecuteQueryOperator(
    task_id="alter_table_exasol",
    sql="ALTER TABLE exasol_example ADD COLUMN c DECIMAL(18,0);",
)

insert_data_exasol = SQLExecuteQueryOperator(
    task_id="insert_data_exasol",
    sql="""
        INSERT INTO exasol_example (a, b, c)
        VALUES
          ('a', 1, 1),
          ('a', 2, 1),
          ('b', 3, 1);
    ",
)

select_data_exasol = SQLExecuteQueryOperator(
    task_id="select_data_exasol",
    sql="SELECT * FROM exasol_example;",
)

drop_table_exasol = SQLExecuteQueryOperator(
    task_id="drop_table_exasol",
    sql="DROP TABLE exasol_example;",
)
```

--------------------------------

### Configure Backend Parameters

Source: https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/secrets-backends/kubernetes-secrets-backend.html

Example of providing custom label keys for connection and variable discovery via backend_kwargs.

```ini
[secrets]
backend = airflow.providers.cncf.kubernetes.secrets.kubernetes_secrets_backend.KubernetesSecretsBackend
backend_kwargs = {"connections_label": "my-org.io/connection", "variables_label": "my-org.io/variable"}
```

--------------------------------

### Execute BTEQ with UTF-8 Script and UTF-8 Session Encoding

Source: https://airflow.apache.org/docs/apache-airflow-providers-teradata/stable/operators/bteq.html

This example configures the BteqOperator for UTF-8 script encoding and UTF-8 session encoding. This is a common setup for consistent character handling.

```python
execute_bteq_utf8_session_utf8_file = BteqOperator(
        task_id="execute_bteq_utf8_session_utf8_file",
        file_path="providers/teradata/tests/system/teradata/script_utf8.bteq",
        params=params,
        bteq_script_encoding="UTF8",
        bteq_session_encoding="UTF8",
    )
```

--------------------------------

### Install Airflow with Celery Support

Source: https://airflow.apache.org/docs/apache-airflow-providers-celery/stable/celery_executor.html

Installs the necessary Airflow provider package for Celery integration or installs Airflow with the 'celery' extra, enabling the use of the CeleryExecutor.

```bash
pip install apache-airflow-providers-celery>=3.3.0
```

```bash
pip install 'apache-airflow[celery]'
```

--------------------------------

### Get Datadog UI Field Behavior in Python

Source: https://airflow.apache.org/docs/apache-airflow-providers-datadog/stable/_api/airflow/providers/datadog/hooks/datadog/index.html

Returns custom field behavior configurations for the Datadog connection in the Airflow UI. This class method helps in customizing the user interface for connection setup.

```python
ui_config = DatadogHook.get_ui_field_behaviour()

```

--------------------------------

### Get All Objects from Weaviate

Source: https://airflow.apache.org/docs/apache-airflow-providers-weaviate/stable/_api/airflow/providers/weaviate/hooks/weaviate/index.html

Retrieves all objects from a specified Weaviate collection. Supports pagination by allowing a starting point ('after' parameter) and can return results as a pandas DataFrame if specified. Additional query parameters can be included.

```python
def get_all_objects(_collection_name_ , _after =None_, _as_dataframe =False_, _** kwargs_):
    """Get all objects from weaviate."""
    pass
```

--------------------------------

### Install OpenFaaS Provider with Extras

Source: https://airflow.apache.org/docs/apache-airflow-providers-openfaas/stable/index.html

Demonstrates how to install the OpenFaaS provider for Airflow, including optional extras for common compatibilities. This command ensures all necessary dependencies for utilizing the provider's features are met.

```bash
pip install apache-airflow-providers-openfaas[common.compat]
```

--------------------------------

### Install Provider with Extra Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-beam

Command to install the Apache Beam provider along with specific cross-provider dependencies such as common.compat.

```bash
pip install apache-airflow-providers-apache-beam[common.compat]
```

--------------------------------

### Install OpenLineage Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-openlineage/index.html

Command to install the OpenLineage provider package into an existing Apache Airflow environment.

```bash
pip install apache-airflow-providers-openlineage
```

--------------------------------

### Install Sendgrid Provider Package

Source: https://airflow.apache.org/docs/apache-airflow-providers-sendgrid/stable/index.html

Command to install the Sendgrid provider package into an existing Apache Airflow environment.

```bash
pip install apache-airflow-providers-sendgrid
```

--------------------------------

### Initialize and Use InfluxDBHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-influxdb/stable/_api/airflow/providers/influxdb/hooks/influxdb/index.html

Demonstrates how to instantiate the InfluxDBHook and perform a basic write operation to a bucket.

```python
from airflow.providers.influxdb.hooks.influxdb import InfluxDBHook

hook = InfluxDBHook(influxdb_conn_id='my_influx_conn')
hook.write(
    bucket_name='my_bucket',
    point_name='my_measurement',
    tag_name='location',
    tag_value='Prague',
    field_name='temperature',
    field_value=25.3
)
```

--------------------------------

### Install Apache Airflow FAB Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-fab/stable/index.html

This command installs the apache-airflow-providers-fab package on top of an existing Airflow installation. It ensures that the necessary components for the FAB provider are available.

```bash
pip install apache-airflow-providers-fab
```

--------------------------------

### Install Apache Airflow Standard Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-standard/stable/index.html

Commands to install the standard provider package and its associated cross-provider dependencies using pip.

```bash
pip install apache-airflow-providers-standard
```

```bash
pip install apache-airflow-providers-standard[common.compat]
```

--------------------------------

### Initialize SalesforceHook and Execute Query

Source: https://airflow.apache.org/docs/apache-airflow-providers-salesforce/stable/_api/airflow/providers/salesforce/hooks/salesforce/index.html

Demonstrates how to instantiate the SalesforceHook using a connection ID and perform a SOQL query against the Salesforce instance.

```python
from airflow.providers.salesforce.hooks.salesforce import SalesforceHook

# Initialize the hook
hook = SalesforceHook(salesforce_conn_id='my_salesforce_conn')

# Execute a query
results = hook.make_query("SELECT Id, Name FROM Account LIMIT 10")
print(results)
```

--------------------------------

### GitHub App Authentication Extras Configuration

Source: https://airflow.apache.org/docs/apache-airflow-providers-github/stable/connections/github.html

Example JSON structure for the 'Extras' field in an Airflow connection to authenticate using a GitHub App. This includes parameters like key path, app ID, installation ID, and token permissions.

```json
{
  "key_path": "FAKE_KEY.pem",
  "app_id": "123456s",
  "installation_id": 123456789,
  "token_permissions": {
    "issues":"write",
    "contents":"read"
  }
}
```

--------------------------------

### System Test Setup for Airflow DAG

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-kafka/stable/_modules/tests/system/apache/kafka/example_dag_hello_kafka.html

This code snippet is used for setting up system tests for an Airflow DAG, likely within a testing framework like pytest. It imports a utility function to get the test run context for the DAG.

```python
from tests_common.test_utils.system_tests import get_test_run  # noqa: E402


# Needed to run the example DAG with pytest (see: tests/system/README.md#run_via_pytest)


test_run = get_test_run(dag)
```

--------------------------------

### Register Plugins via Setuptools Entrypoints

Source: https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/plugins.html

Configures a plugin to be automatically loaded by Airflow using Python package entry points defined in pyproject.toml.

```python
class MyAirflowPlugin(AirflowPlugin):
    name = "my_namespace"
```

```toml
[project.entry-points."airflow.plugins"]
my_plugin = "my_package.my_plugin:MyAirflowPlugin"
```

--------------------------------

### Install Apache Airflow Keycloak Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the Apache Airflow provider for Keycloak, an identity and access management solution. Use pip for installation.

```bash
pip install 'apache-airflow-providers-keycloak'
```

--------------------------------

### Install Airbyte Provider Package

Source: https://airflow.apache.org/docs/apache-airflow-providers-airbyte/stable/index.html

Standard command to install the Airbyte provider package into an existing Apache Airflow environment.

```bash
pip install apache-airflow-providers-airbyte
```

--------------------------------

### Call Microsoft Graph API to Get SharePoint Site Pages

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/operators/msgraph.html

This example shows how to use MSGraphAsyncOperator to fetch pages for a specific SharePoint site. It utilizes XCom to pull the site ID from a previous task and specifies the API version as 'beta'.

```python
site_pages_task = MSGraphAsyncOperator(
    task_id="news_pages",
    conn_id="msgraph_api",
    api_version="beta",
    url=("sites/%s/pages" % "{{ ti.xcom_pull(task_ids='news_site') }}"),  # noqa: UP031
)
```

--------------------------------

### SFTP Sensor Example Module

Source: https://airflow.apache.org/docs/apache-airflow-providers-sftp/stable/_api/tests/system/sftp/example_sftp_sensor/index.html

Details the SFTP Sensor example module, including its attributes and functions.

```APIDOC
## Module: tests.system.sftp.example_sftp_sensor

### Description
This module provides an example implementation and usage of an SFTP sensor within Airflow's system tests.

### Attributes

- **SFTP_DIRECTORY** (string) - The SFTP directory to monitor.
- **FULL_FILE_PATH** (string) - The full path to the file to monitor on SFTP.
- **SFTP_DEFAULT_CONNECTION** (string) - The default SFTP connection ID to use.

### Functions

- **sleep_function()** - A simple function that pauses execution.
- **sftp_sensor_decorator()** - A decorator function for SFTP sensor operations.

### Module Contents

- `SFTP_DIRECTORY`
- `FULL_FILE_PATH`
- `SFTP_DEFAULT_CONNECTION`
- `sleep_function()`
- `sftp_sensor_decorator()`
- `test_run`
```

--------------------------------

### Install SFTP Provider for Apache Airflow

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the SFTP provider for Apache Airflow, which supports SSH File Transfer Protocol. The installation requires pip.

```bash
pip install 'apache-airflow-providers-sftp'
```

--------------------------------

### Retrieve Task Instance Logs via REST API

Source: https://airflow.apache.org/docs/apache-airflow/stable/security/audit_logs.html

These cURL commands demonstrate how to fetch task instance logs using the Airflow REST API. It includes examples for getting basic logs and retrieving logs with full content and metadata.

```bash
# Get task instance logs
curl -X GET "http://localhost:8080/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/logs/{try_number}"

# Get task logs with metadata
curl -X GET "http://localhost:8080/api/v1/dags/example_dag/dagRuns/2024-01-01T00:00:00+00:00/taskInstances/example_task/logs/1?full_content=true"
```

--------------------------------

### tests.system.apache.beam.example_go

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-beam/stable/_api/tests/system/apache/beam/example_go/index.html

API reference for the example Go pipeline execution module in Apache Airflow system tests.

```APIDOC
## Python Module: tests.system.apache.beam.example_go

### Description
This module contains system tests and example DAGs for executing Apache Beam pipelines written in Go using Airflow operators.

### Attributes
- **start_go_pipeline_local_direct_runner**: An operator or task instance configured to execute a Go pipeline using the DirectRunner locally.
- **test_run**: A test execution hook to validate the successful completion of the pipeline.

### Module Contents
- `start_go_pipeline_local_direct_runner()`: Triggers the Go pipeline execution.
- `test_run()`: Executes the validation logic for the system test.

### Usage Example
```python
from tests.system.apache.beam.example_go import start_go_pipeline_local_direct_runner

# Example of triggering the pipeline in a DAG
start_go_pipeline_local_direct_runner()
```
```

--------------------------------

### Install Neo4j Provider with Extra Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-neo4j/stable/index.html

Command to install the Neo4j provider package along with specific cross-provider dependencies such as common.compat.

```bash
pip install apache-airflow-providers-neo4j[common.compat]
```

--------------------------------

### Configure Backend Parameters

Source: https://airflow.apache.org/docs/apache-airflow-providers-yandex/stable/secrets-backends/yandex-cloud-lockbox-secret-backend.html

Example of setting custom prefixes for connections and variables within the backend_kwargs configuration.

```ini
[secrets]
backend = airflow.providers.yandex.secrets.lockbox.LockboxSecretBackend
backend_kwargs = {"connections_prefix": "example-connections-prefix", "variables_prefix": "example-variables-prefix"}
```

--------------------------------

### Deploying Init Containers in Airflow

Source: https://airflow.apache.org/docs/helm-chart/stable/using-additional-containers.html

This snippet shows how to deploy init containers for Airflow components using the `extraInitContainers` parameter in `values.yaml`. It provides an example of a simple init container that echoes 'hello'. Init containers run before the main container starts.

```yaml
scheduler:
  extraInitContainers:
    - name: hello
      image: debian
      args:
        - echo
        - hello

```

--------------------------------

### Install Singularity Provider for Apache Airflow

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the Singularity provider for Apache Airflow. This package is used for Singularity containerization tasks. Pip is required for installation.

```bash
pip install 'apache-airflow-providers-singularity'
```

--------------------------------

### Add System and Provider Packages

Source: https://airflow.apache.org/docs/docker-stack/build.html

Shows how to install system-level dependencies using apt-get and Python packages via pip, specifically for providers requiring external binaries like Java.

```Dockerfile
FROM apache/airflow:2.11.2
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         openjdk-17-jre-headless \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" apache-airflow-providers-apache-spark==2.1.3
```

--------------------------------

### Install Airbyte Provider with Extra Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-airbyte/stable/index.html

Command to install the Airbyte provider package along with specific cross-provider dependencies, such as common.compat.

```bash
pip install apache-airflow-providers-airbyte[common.compat]
```

--------------------------------

### Install Git Provider with Extra Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-git/stable/index.html

Command to install the Git provider package along with optional cross-provider dependencies such as common-compat.

```bash
pip install apache-airflow-providers-git[common.compat]
```

--------------------------------

### Datadog Connection Configuration Example (JSON)

Source: https://airflow.apache.org/docs/apache-airflow-providers-datadog/stable/connections/datadog.html

This JSON structure demonstrates how to configure the Datadog connection, including host, description, and extra parameters like API keys and host.

```json
{
  "conn_type": "datadog",
  "description": "Datadog connection for my app",
  "extra": {
    "api_host": "https://api.datadoghq.com",
    "api_key": "my api key",
    "app_key": "my app key",
    "source_type_name": "apache"
  },
  "host": "environment-region-application.domain.com"
}
```

--------------------------------

### Install Provider with Extra Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-iceberg

Command to install the Apache Iceberg provider along with specific cross-provider dependencies like common.compat.

```bash
pip install apache-airflow-providers-apache-iceberg[common.compat]
```

--------------------------------

### Airflow Custom Callback Methods Example

Source: https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/callbacks.html

Demonstrates how to use custom Python functions as callbacks for DAG and task events in Apache Airflow. It shows the setup for on_success_callback at the DAG level, on_failure_callback and on_execute_callback at the task level, and how these functions receive a context dictionary.

```python
from airflow.sdk import DAG
from airflow.providers.standard.operators.empty import EmptyOperator


def task_execute_callback(context):
    print(f"Task has begun execution, task_instance_key_str: {context['task_instance_key_str']}")


def task_failure_alert(context):
    print(f"Task has failed, task_instance_key_str: {context['task_instance_key_str']}")

def dag_success_alert(context):
    print(f"Dag has succeeded, run_id: {context['run_id']}")


with DAG(
    dag_id="example_callback",
    on_success_callback=dag_success_alert,
    default_args={"on_execute_callback": task_execute_callback},
):
    task1 = EmptyOperator(task_id="task1", on_failure_callback=[task_failure_alert])
    task2 = EmptyOperator(task_id="task2")
    task3 = EmptyOperator(task_id="task3")
    task1 >> task2 >> task3

```

--------------------------------

### Start Airflow Services

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/run-with-self-signed-certificate.html

Command to initialize and start the Airflow containers defined in the docker-compose configuration.

```bash
docker compose up
```

--------------------------------

### Install Provider with Extra Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-livy/stable/index.html

Command to install the Apache Livy provider along with specific cross-provider dependencies using pip extras.

```bash
pip install apache-airflow-providers-apache-livy[common.compat]
```

--------------------------------

### Install Custom Airflow Provider Packages

Source: https://airflow.apache.org/docs/docker-stack/build.html

Demonstrates how to upgrade or install specific versions of Airflow provider packages by extending the base image and using pip.

```Dockerfile
FROM apache/airflow:2.11.2
RUN pip install "apache-airflow==${AIRFLOW_VERSION}" --no-cache-dir apache-airflow-providers-docker==2.5.1
```

--------------------------------

### tests.system.ydb.example_ydb Module

Source: https://airflow.apache.org/docs/apache-airflow-providers-ydb/stable/_api/tests/system/ydb/example_ydb/index.html

Overview of the YDB example system tests module.

```APIDOC
## Module: tests.system.ydb.example_ydb

### Description
This module contains system tests for YDB, specifically focusing on example functionalities.

### Attributes

- **ENV_ID** (any) - Environment identifier.
- **DAG_ID** (str) - The DAG ID used for YDB operator tests. Defaults to 'ydb_operator_dag'.

### Functions

- **create_pet_table**()
  - Description: Function to create the pet table.

- **populate_pet_table_via_bulk_upsert**()
  - Description: Populates the pet table using bulk upsert.

- **sanitize_date**(_value_)
  - Description: Ensures the provided value is in a valid date format.
  - Parameters:
    - **_value_** (any) - The value to sanitize.

- **test_run**()
  - Description: Executes a test run.

- **transform_dates_func**(**kwargs)
  - Description: Transforms dates based on provided keyword arguments.
```

--------------------------------

### Initialize and Use SesNotifier

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/notifications/ses/index.html

Demonstrates how to instantiate the SesNotifier class with required parameters like sender, recipient, and content, and how to trigger the notification.

```python
from airflow.providers.amazon.aws.notifications.ses import SesNotifier

notifier = SesNotifier(
    mail_from='sender@example.com',
    to='recipient@example.com',
    subject='Airflow Notification',
    html_content='<p>Task completed successfully.</p>',
    aws_conn_id='aws_default'
)

# Triggering the notification within a context
notifier.notify(context={})
```

--------------------------------

### Install Samba Provider for Apache Airflow

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the Samba provider for Apache Airflow. This package enables integration with Samba services. It requires pip to be installed.

```bash
pip install 'apache-airflow-providers-samba'
```

--------------------------------

### Install Apache Airflow Slack Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-slack/stable/index.html

Commands to install the Slack provider package for Apache Airflow. This includes the base installation and the command to include optional cross-provider dependencies.

```bash
pip install apache-airflow-providers-slack
```

```bash
pip install apache-airflow-providers-slack[common.compat]
```

--------------------------------

### Get OpenLineage Database Specific Lineage with SnowflakeHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/_api/airflow/providers/snowflake/hooks/snowflake/index.html

Emits OpenLineage events for each Snowflake query based on executed query IDs. It can add an `ExternalQueryRunFacet` if a single query ID is present. This method is typically called after task execution and emits START and COMPLETE events for each query.

```python
def get_openlineage_database_specific_lineage(self, task_instance) -> OperatorLineage | None:
    """
    Emit separate OpenLineage events for each Snowflake query, based on executed query IDs.
    If a single query ID is present, also add an ExternalQueryRunFacet to the returned lineage metadata.
    Note that get_openlineage_database_specific_lineage is usually called after task’s execution, so if multiple query IDs are present, both START and COMPLETE event for each query will be emitted after task’s execution. If we are able to query Snowflake for query execution metadata, query event times will correspond to actual query’s start and finish times. 

    Args:
        
      task_instance: The Airflow TaskInstance object for which lineage is being collected. 

    Returns:
        
      An OperatorLineage object if a single query ID is found; otherwise None.
    """
    pass
```

--------------------------------

### Install HTTP Provider with Cross-Provider Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-http/stable/index.html

Command to install the HTTP provider package along with specific extra dependencies required for cross-provider compatibility.

```bash
pip install apache-airflow-providers-http[common.compat]
```

--------------------------------

### Airflow DAG with WinRMOperator

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-winrm/stable/_modules/tests/system/microsoft/winrm/example_winrm.html

This Python code defines an Apache Airflow DAG that utilizes the WinRMOperator to execute commands on a remote Windows machine. It showcases the creation of a WinRMHook and multiple WinRMOperator tasks for running commands in parallel. Note that this DAG is for example purposes and requires specific setup to run.

```python
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

```

```python

#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

```

```python

"""
This is an example dag for using the WinRMOperator.
"""

from __future__ import annotations

# --------------------------------------------------------------------------------
# Load The Dependencies
# --------------------------------------------------------------------------------
import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.microsoft.winrm.hooks.winrm import WinRMHook
from airflow.providers.microsoft.winrm.operators.winrm import WinRMOperator

# --------------------------------------------------------------------------------
# Caveat: This Dag will not run because of missing scripts.
# The purpose of this is to give you a sample of a real world example DAG!
# --------------------------------------------------------------------------------
from airflow.providers.standard.operators.empty import EmptyOperator



ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")



DAG_ID = "POC_winrm_parallel"

with DAG(
    dag_id=DAG_ID,
    schedule="0 0 * * *",
    start_date=datetime(2021, 1, 1),
    dagrun_timeout=timedelta(minutes=60),
    tags=["example"],
    catchup=False,
) as dag:


    run_this_last = EmptyOperator(task_id="run_this_last")



    # [START create_hook]
    winRMHook = WinRMHook(ssh_conn_id="ssh_POC1")
    # [END create_hook]

    # [START run_operator]
    t1 = WinRMOperator(task_id="wintask1", command="ls -altr", winrm_hook=winRMHook)

    t2 = WinRMOperator(task_id="wintask2", command="sleep 60", winrm_hook=winRMHook)

    t3 = WinRMOperator(task_id="wintask3", command="echo 'luke test' ", winrm_hook=winRMHook)
    # [END run_operator]

    [t1, t2, t3] >> run_this_last

    from tests_common.test_utils.watcher import watcher

    # This test needs watcher in order to properly mark success/failure
    # when "tearDown" task with trigger rule is part of the DAG
    list(dag.tasks) >> watcher()

from tests_common.test_utils.system_tests import get_test_run  # noqa: E402

# Needed to run the example DAG with pytest (see: tests/system/README.md#run_via_pytest)



test_run = get_test_run(dag)

```

--------------------------------

### Install Airflow Kerberos Support

Source: https://airflow.apache.org/docs/apache-airflow/stable/security/kerberos.html

Command to install the Apache Airflow package with the required Kerberos dependencies.

```bash
pip install 'apache-airflow[kerberos]'
```

--------------------------------

### Install Facebook Provider with Cross-Provider Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-facebook

Command to install the Facebook provider package along with optional cross-provider dependencies using extras.

```bash
pip install apache-airflow-providers-facebook[common.compat]
```

--------------------------------

### Call Microsoft Graph API to Get Power BI Workspaces Info

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/operators/msgraph.html

This example demonstrates fetching detailed information for Power BI workspaces using MSGraphAsyncOperator. It includes POST method, query parameters for detailed info, and data payload referencing a previous task's output.

```python
workspaces_info_task = MSGraphAsyncOperator(
    task_id="get_workspace_info",
    conn_id="powerbi",
    url="myorg/admin/workspaces/getInfo",
    method="POST",
    query_parameters={
        "lineage": True,
        "datasourceDetails": True,
        "datasetSchema": True,
        "datasetExpressions": True,
        "getArtifactUsers": True,
    },
    data={"workspaces": workspaces_task.output},
    result_processor=lambda context, response: {"scanId": response["id"]},  # type: ignore[typeddict-item]
)
```

--------------------------------

### Execute Pig Script using PigCliHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-pig/stable/_api/airflow/providers/apache/pig/hooks/pig/index.html

Demonstrates how to instantiate the PigCliHook and execute a Pig command using the run_cli method. The example shows passing pig_opts to configure the execution environment.

```python
from airflow.providers.apache.pig.hooks.pig import PigCliHook

# Initialize the hook
ph = PigCliHook()

# Run a pig command with specific options
result = ph.run_cli("ls /;", pig_opts="-x mapreduce")

# Verify the output
print("hdfs://" in result)
```

--------------------------------

### POST /2.0/libraries/install

Source: https://airflow.apache.org/docs/apache-airflow-providers-databricks/stable/_api/airflow/providers/databricks/hooks/databricks/index.html

Installs libraries on a specified Databricks cluster.

```APIDOC
## POST /2.0/libraries/install

### Description
Installs a list of libraries on a Databricks cluster.

### Method
POST

### Endpoint
/2.0/libraries/install

### Request Body
- **json** (dict) - Required - Dictionary containing cluster_id and an array of libraries to install.

### Request Example
{
  "cluster_id": "0000-000000-000000",
  "libraries": [{"pypi": {"package": "pandas"}}]
}
```

--------------------------------

### Airflow DAG with HTTP Operator Examples

Source: https://airflow.apache.org/docs/apache-airflow-providers-http/stable/_modules/tests/system/http/example_http.html

This Python code defines an Apache Airflow DAG that includes multiple HttpOperator tasks. It demonstrates sending POST requests with JSON and form-urlencoded data, performing GET requests with parameters, and handling responses. It also includes tasks for PUT and DELETE methods.

```python
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Example HTTP operator and sensor"""

from __future__ import annotations

import json
import os
from datetime import datetime

from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.providers.http.sensors.http import HttpSensor



ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")



DAG_ID = "example_http_operator"



dag = DAG(
    DAG_ID,
    default_args={"retries": 1},
    tags=["example"],
    start_date=datetime(2021, 1, 1),
    schedule=None,
    catchup=False,
)


dag.doc_md = __doc__

# task_post_op, task_get_op and task_put_op are examples of tasks created by instantiating operators
# [START howto_operator_http_task_post_op]


task_post_op = HttpOperator(
    task_id="post_op",
    endpoint="post",
    data=json.dumps({"priority": 5}),
    headers={"Content-Type": "application/json"},
    response_check=lambda response: response.json()["json"]["priority"] == 5,
    dag=dag,
)


# [END howto_operator_http_task_post_op]
# [START howto_operator_http_task_post_op_formenc]


task_post_op_formenc = HttpOperator(
    task_id="post_op_formenc",
    endpoint="post",
    data="name=Joe",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    dag=dag,
)


# [END howto_operator_http_task_post_op_formenc]
# [START howto_operator_http_task_get_op]


task_get_op = HttpOperator(
    task_id="get_op",
    method="GET",
    endpoint="get",
    data={"param1": "value1", "param2": "value2"},
    headers={},
    dag=dag,
)


# [END howto_operator_http_task_get_op]
# [START howto_operator_http_task_get_op_response_filter]


task_get_op_response_filter = HttpOperator(
    task_id="get_op_response_filter",
    method="GET",
    endpoint="get",
    response_filter=lambda response: response.json()["nested"]["property"],
    dag=dag,
)


# [END howto_operator_http_task_get_op_response_filter]
# [START howto_operator_http_task_put_op]


task_put_op = HttpOperator(
    task_id="put_op",
    method="PUT",
    endpoint="put",
    data=json.dumps({"priority": 5}),
    headers={"Content-Type": "application/json"},
    dag=dag,
)


# [END howto_operator_http_task_put_op]
# [START howto_operator_http_task_del_op]


task_del_op = HttpOperator(
    task_id="del_op",
    method="DELETE",
    endpoint="delete",
    data="some=data",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    dag=dag,
)


# [END howto_operator_http_task_del_op]

```

--------------------------------

### Complete Postgres Operator DAG Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/operators.html

A full DAG example showcasing multiple `SQLExecuteQueryOperator` tasks with various configurations.

```APIDOC
## The complete Postgres Operator Dag

### Description
This example presents a complete Apache Airflow DAG that utilizes the `SQLExecuteQueryOperator` for various database operations, including table creation, data population, data retrieval, and parameterized queries with advanced hook configurations.

### Method
N/A (This is a DAG definition, not an API endpoint)

### Endpoint
N/A

### Parameters
N/A (This is a DAG definition)

### Request Example
```python
import os
import datetime

from airflow import DAG
from airflow.providers.postgres.operators.postgres import SQLExecuteQueryOperator

ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
DAG_ID = "postgres_operator_dag"

with DAG(
    dag_id=DAG_ID,
    start_date=datetime.datetime(2020, 2, 2),
    schedule="@once",
    catchup=False,
) as dag:
    create_pet_table = SQLExecuteQueryOperator(
        task_id="create_pet_table",
        sql="""
            CREATE TABLE IF NOT EXISTS pet (
            pet_id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            pet_type VARCHAR NOT NULL,
            birth_date DATE NOT NULL,
            OWNER VARCHAR NOT NULL);
          """,
    )
    populate_pet_table = SQLExecuteQueryOperator(
        task_id="populate_pet_table",
        sql="""
            INSERT INTO pet (name, pet_type, birth_date, OWNER)
            VALUES ( 'Max', 'Dog', '2018-07-05', 'Jane');
            INSERT INTO pet (name, pet_type, birth_date, OWNER)
            VALUES ( 'Susie', 'Cat', '2019-05-01', 'Phil');
            INSERT INTO pet (name, pet_type, birth_date, OWNER)
            VALUES ( 'Lester', 'Hamster', '2020-06-23', 'Lily');
            INSERT INTO pet (name, pet_type, birth_date, OWNER)
            VALUES ( 'Quincy', 'Parrot', '2013-08-11', 'Anne');
            """,
    )
    get_all_pets = SQLExecuteQueryOperator(task_id="get_all_pets", sql="SELECT * FROM pet;")
    get_birth_date = SQLExecuteQueryOperator(
        task_id="get_birth_date",
        sql="SELECT * FROM pet WHERE birth_date BETWEEN SYMMETRIC %(begin_date)s AND %(end_date)s",
        parameters={"begin_date": "2020-01-01", "end_date": "2020-12-31"},
        hook_params={"options": "-c statement_timeout=3000ms"},
    )

    create_pet_table >> populate_pet_table >> get_all_pets >> get_birth_date
```

### Response
#### Success Response (200)
N/A (This is a DAG definition, not an API endpoint)

#### Response Example
N/A
```

--------------------------------

### Install Edge Provider with Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-edge3/stable/index.html

Commands to install the edge provider package and its optional cross-provider dependencies using pip.

```bash
pip install apache-airflow-providers-edge3
pip install apache-airflow-providers-edge3[common.compat]
```

--------------------------------

### Install Jenkins Provider with Common Compat

Source: https://airflow.apache.org/docs/apache-airflow-providers-jenkins/stable/index.html

This command installs the apache-airflow-providers-jenkins package along with the common.compat extra, which might be needed for certain functionalities. Ensure you have a compatible Airflow version installed.

```bash
pip install apache-airflow-providers-jenkins[common.compat]
```

--------------------------------

### Configure Airflow Helm Chart for CI/CD Tools

Source: https://airflow.apache.org/docs/helm-chart/stable/index.html

When installing the Airflow Helm chart with CI/CD tools such as Argo CD, Flux, Rancher, or Terraform, it is mandatory to set specific values to ensure the application starts correctly and database migrations are run. This configuration prevents issues during updates by preserving the immutability of Kubernetes Job manifests.

```yaml
createUserJob:
  useHelmHooks: false
  applyCustomEnv: false
migrateDatabaseJob:
  useHelmHooks: false
  applyCustomEnv: false
```

--------------------------------

### Install Apache Airflow Docker Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-docker/stable/index.html

Commands to install the Docker provider package for Apache Airflow. It includes both the base installation and the command for installing with specific extra dependencies.

```bash
pip install apache-airflow-providers-docker
```

```bash
pip install apache-airflow-providers-docker[common.compat]
```

--------------------------------

### Salesforce Connection URI Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-salesforce/stable/connections/salesforce.html

Example of how to set the Salesforce connection as a URI in an environment variable. This format is used for passing connection details, including extras, following the standard DB connection syntax.

```bash
export AIRFLOW_CONN_SALESFORCE_DEFAULT='http://your_username:your_password@https%3A%2F%2Fyour_host.lightning.force.com?security_token=your_token'
```

--------------------------------

### Install Samba Provider Package

Source: https://airflow.apache.org/docs/apache-airflow-providers-samba/index.html

Command to install the Samba provider package into an existing Apache Airflow environment.

```bash
pip install apache-airflow-providers-samba
```

--------------------------------

### Mark function as Setup Task using @setup decorator

Source: https://airflow.apache.org/docs/task-sdk/stable/api.html

The `@setup` decorator marks a function to be executed as a setup task. Setup tasks run before other tasks in their Dag or TaskGroup context, typically for initialization or resource preparation. It takes a callable as input and returns a callable.

```python
from airflow.decorators import setup

@setup
def initialize_resources():
    print("Initializing resources...")

```

--------------------------------

### Install Common SQL Provider with Extra Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-common-sql

Command to install the common SQL provider along with specific cross-provider dependencies, such as Amazon integration.

```bash
pip install apache-airflow-providers-common-sql[amazon]
```

--------------------------------

### Install Datadog Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-datadog/stable/index.html

Command to install the Datadog provider package into an existing Apache Airflow environment.

```bash
pip install apache-airflow-providers-datadog
```

--------------------------------

### Install Build Dependencies for SQLite Upgrade

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html

Installs necessary system packages required to compile and install SQLite from source on AmazonLinux.

```bash
yum -y install wget tar gzip gcc make expect
```

--------------------------------

### Install Apache Beam Provider with Google Support (Older PIP)

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/changelog.html

This command shows how to install the Apache Beam provider with the 'google' extra, maintaining compatibility with older PIP versions (<= 20.2.4). This approach allows for continued use of existing integrations, but may limit the availability of certain BigQuery operator features.

```bash
pip install apache-airflow-providers-apache-beam[google]
```

--------------------------------

### Install Airflow FTP Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-ftp/index.html

Command to install the FTP provider package into an existing Airflow environment.

```bash
pip install apache-airflow-providers-ftp
```

--------------------------------

### Install Provider with Cross-Provider Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-atlassian-jira/stable/index.html

Command to install the Atlassian Jira provider along with specific extra dependencies for cross-provider compatibility.

```bash
pip install apache-airflow-providers-atlassian-jira[common.compat]
```

--------------------------------

### Install Apache Airflow InfluxDB Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the Apache Airflow provider for InfluxDB, a time-series database. The installation is done via pip.

```bash
pip install 'apache-airflow-providers-influxdb'
```

--------------------------------

### DbtCloudRunJobOperator Examples

Source: https://airflow.apache.org/docs/apache-airflow-providers-dbt-cloud/stable/_modules/tests/system/dbt/cloud/example_dbt_cloud.html

Examples demonstrating how to use the DbtCloudRunJobOperator to trigger dbt Cloud jobs.

```APIDOC
## POST /dbt/cloud/run_job

### Description
Triggers a dbt Cloud job run. This operator can either wait for the job to complete or run asynchronously.

### Method
POST

### Endpoint
/dbt/cloud/run_job

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **job_id** (integer) - Required - The ID of the dbt Cloud job to run.
- **check_interval** (integer) - Optional - The interval in seconds to check for job status.
- **timeout** (integer) - Optional - The timeout in seconds for the job run.
- **wait_for_termination** (boolean) - Optional - If true, waits for the job to complete. Defaults to true.
- **additional_run_config** (object) - Optional - Additional configuration for the job run.
- **project_name** (string) - Required if job_id is not provided - The name of the dbt Cloud project.
- **environment_name** (string) - Required if job_id is not provided - The name of the dbt Cloud environment.
- **job_name** (string) - Required if job_id is not provided - The name of the dbt Cloud job.

### Request Example
```json
{
  "job_id": 48617,
  "check_interval": 10,
  "timeout": 300
}
```

### Response
#### Success Response (200)
- **run_id** (integer) - The ID of the triggered job run.

#### Response Example
```json
{
  "run_id": 12345
}
```
```

--------------------------------

### Install PagerDuty Provider with Extras

Source: https://airflow.apache.org/docs/apache-airflow-providers-pagerduty/stable/index.html

Command to install the PagerDuty provider package along with specific cross-provider dependencies using extras.

```bash
pip install apache-airflow-providers-pagerduty[common.compat]
```

--------------------------------

### SFTPSensor Usage

Source: https://airflow.apache.org/docs/apache-airflow-providers-sftp/stable/sensors/sftp_sensor.html

Example of using the SFTPSensor with basic parameters.

```APIDOC
## POST /websites/airflow_apache

### Description
This endpoint is used to configure and trigger the SFTP Sensor to look for files on an SFTP server.

### Method
POST

### Endpoint
/websites/airflow_apache

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **task_id** (string) - Required - The unique identifier for the task.
- **path** (string) - Required - The path to the file or pattern to look for on the SFTP server.
- **poke_interval** (integer) - Optional - The time in seconds that the sensor should wait between checks.
- **deferrable** (boolean) - Optional - If set to True, the sensor will run in deferrable mode.

### Request Example
```json
{
  "task_id": "sftp_operator",
  "path": "/path/to/your/file.txt",
  "poke_interval": 10
}
```

### Response
#### Success Response (200)
- **status** (string) - Indicates the success of the operation.

#### Response Example
```json
{
  "status": "Task configured successfully"
}
```
```

--------------------------------

### Install Tableau Provider with Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-tableau

Command to install the Tableau provider package along with its specific cross-provider dependencies, such as common-compat.

```bash
pip install apache-airflow-providers-tableau[common.compat]
```

--------------------------------

### Install Apache Airflow SMTP Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-smtp/stable/index.html

Installs the apache-airflow-providers-smtp package using pip. This command adds the SMTP provider to an existing Airflow installation.

```bash
pip install apache-airflow-providers-smtp
```

--------------------------------

### Setup Task Without Teardown in Airflow

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/setup-and-teardown.html

Demonstrates a scenario where a setup task is defined but no explicit teardown task is associated. In this case, all tasks downstream of the setup task are considered to require it, affecting clearing behavior.

```python
create_cluster >> run_query >> other_task
```

--------------------------------

### Install Provider with Cross-Provider Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-postgres/index.html

Command to install the PostgreSQL provider package along with specific extra dependencies, such as Amazon integration.

```bash
pip install apache-airflow-providers-postgres[amazon]
```

--------------------------------

### Install OpenTelemetry Dependencies

Source: https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/traces.html

Installs the required Apache Airflow provider package for OpenTelemetry support.

```bash
pip install 'apache-airflow[otel]'
```

--------------------------------

### Install Apache Airflow Jenkins Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the Apache Airflow provider for Jenkins, a CI/CD automation server. The installation is performed using pip.

```bash
pip install 'apache-airflow-providers-jenkins'
```

--------------------------------

### Initialize and Use CohereHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-cohere/stable/_api/airflow/providers/cohere/hooks/cohere/index.html

Demonstrates how to instantiate the CohereHook to interact with the Cohere platform. It allows for configuring connection IDs, timeouts, and request options.

```python
from airflow.providers.cohere.hooks.cohere import CohereHook

# Initialize the hook
hook = CohereHook(conn_id='my_cohere_conn', timeout=30)

# Retrieve the connection client
client = hook.get_conn()

# Generate embeddings
embeddings = hook.create_embeddings(texts=['Hello world'], model='embed-multilingual-v3.0')
```

--------------------------------

### Install SFTP Provider with SSHFS

Source: https://airflow.apache.org/docs/apache-airflow-providers-sftp/stable/filesystems/sftp.html

Installs the necessary Apache Airflow provider for SFTP and the sshfs library to enable SSH filesystem access.

```bash
pip install apache-airflow-providers-sftp[sshfs]
```

--------------------------------

### Install Neo4j Provider Package

Source: https://airflow.apache.org/docs/apache-airflow-providers-neo4j/stable/index.html

Command to install the Neo4j provider package into an existing Apache Airflow environment using pip.

```bash
pip install apache-airflow-providers-neo4j
```

--------------------------------

### Airbyte Connection Configuration Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-airbyte/stable/connections.html

This example demonstrates how to configure connection parameters for the Airbyte API Python SDK. It includes required fields like host, client ID, and client secret, along with optional fields like token URL and extra parameters for proxy settings.

```python
from airbyte_api_python_sdk import AirbyteClient

# Example for Airbyte Cloud
client_cloud = AirbyteClient(
    host="https://api.airbyte.com/v1/",
    token_url="v1/applications/token",
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    extra={"http": "http://proxy.example.com:8080", "https": "http://proxy.example.com:8080"}
)

# Example for Airbyte OSS
client_oss = AirbyteClient(
    host="http://localhost:8000/api/public/v1/",
    token_url="/api/public/v1/applications/token",
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET"
)
```

--------------------------------

### Install Git Provider Package

Source: https://airflow.apache.org/docs/apache-airflow-providers-git/stable/index.html

Command to install the Apache Airflow Git provider package into an existing Airflow environment.

```bash
pip install apache-airflow-providers-git
```

--------------------------------

### POST /instances

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/hooks/cloud_sql/index.html

Create a new Cloud SQL instance.

```APIDOC
## POST /instances

### Description
Creates a new Cloud SQL instance based on the provided configuration body.

### Method
POST

### Endpoint
/instances

### Parameters
#### Request Body
- **body** (dict) - Required - Configuration object as defined by the Google Cloud SQL Admin API insert request body.
- **project_id** (string) - Optional - Project ID where the instance will be created.

### Request Example
{
  "name": "new-instance",
  "settings": {
    "tier": "db-f1-micro"
  }
}

### Response
#### Success Response (200)
- **status** (null) - Returns None upon successful creation.
```

--------------------------------

### Install SSH Provider Package

Source: https://airflow.apache.org/docs/apache-airflow-providers-ssh/index.html

Installs the SSH provider package for Apache Airflow. This command adds the necessary SSH capabilities to an existing Airflow installation.

```bash
pip install apache-airflow-providers-ssh
```

--------------------------------

### Install HDFS Provider with Cross-Provider Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-hdfs/stable/index.html

Command to install the HDFS provider package along with optional cross-provider dependencies such as common.compat.

```bash
pip install apache-airflow-providers-apache-hdfs[common.compat]
```

--------------------------------

### Install Trino Provider Package

Source: https://airflow.apache.org/docs/apache-airflow-providers-trino/index.html

Command to install the Trino provider package for Apache Airflow using pip.

```bash
pip install apache-airflow-providers-trino
```

--------------------------------

### Install Airflow with Pip and Constraints

Source: https://airflow.apache.org/docs/apache-airflow/stable/start.html

Installs a specific version of Apache Airflow using pip, along with extras, and applies version constraints to ensure a reproducible installation. It dynamically determines the Python version to use for constraint file selection.

```bash
AIRFLOW_VERSION=3.1.3

# Extract the version of Python you have installed. If you're currently using a Python version that is not supported by Airflow, you may want to set this manually.
# See above for supported versions.
PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"

CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
```

--------------------------------

### Install Airflow with Pip and Constraints (Bash)

Source: https://airflow.apache.org/docs/stable/start.html

Installs Apache Airflow using pip, specifying the version and a constraint file URL. The constraint file ensures reproducible builds by pinning dependency versions based on Airflow and Python versions.

```bash
AIRFLOW_VERSION=3.1.3

# Extract the version of Python you have installed. If you're currently using a Python version that is not supported by Airflow, you may want to set this manually.
# See above for supported versions.
PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"

CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install "apache-airflow[celery]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

--------------------------------

### Implement Standard SFTPSensor

Source: https://airflow.apache.org/docs/apache-airflow-providers-sftp/stable/sensors/sftp_sensor.html

Demonstrates how to instantiate a standard SFTPSensor to monitor a file path on an SFTP server with a specified poke interval.

```python
sftp_with_operator = SFTPSensor(task_id="sftp_operator", path=FULL_FILE_PATH, poke_interval=10)
```

--------------------------------

### Install Atlassian Jira Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-atlassian-jira/stable/index.html

Command to install the Atlassian Jira provider package into an existing Airflow environment.

```bash
pip install apache-airflow-providers-atlassian-jira
```

--------------------------------

### Install Segment Provider for Apache Airflow

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the Segment provider for Apache Airflow. This package facilitates integration with Segment. Ensure pip is available for installation.

```bash
pip install 'apache-airflow-providers-segment'
```

--------------------------------

### Initialize and Use SlackHook for API Calls

Source: https://airflow.apache.org/docs/apache-airflow-providers-slack/stable/_api/airflow/providers/slack/hooks/slack/index.html

Demonstrates how to instantiate the SlackHook using a connection ID and perform a generic API call to post a message to a Slack channel.

```python
from airflow.providers.slack.hooks.slack import SlackHook

# Create hook
slack_hook = SlackHook(slack_conn_id="slack_api_default")

# Call generic API with parameters
slack_hook.call("chat.postMessage", json={"channel": "#random", "text": "Hello world!"})
```

--------------------------------

### Install Airflow Keycloak Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-keycloak/stable/index.html

Command to install the Keycloak provider package into an existing Apache Airflow environment.

```bash
pip install apache-airflow-providers-keycloak
```

--------------------------------

### Install OpenAI Provider Package

Source: https://airflow.apache.org/docs/apache-airflow-providers-openai/stable/index.html

Command to install the OpenAI provider package for Apache Airflow using pip.

```bash
pip install apache-airflow-providers-openai
```

--------------------------------

### Install InfluxDB Provider with Extras

Source: https://airflow.apache.org/docs/apache-airflow-providers-influxdb/stable/index.html

Command to install the InfluxDB provider package along with specific cross-provider dependencies.

```bash
pip install apache-airflow-providers-influxdb[common.compat]
```

--------------------------------

### Complete Postgres Operator DAG Example (Python)

Source: https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/operators.html

Presents a full Apache Airflow DAG example demonstrating the usage of SQLExecuteQueryOperator for various tasks including table creation, population, data retrieval, and parameterized queries with connection options.

```python
# create_pet_table, populate_pet_table, get_all_pets, and get_birth_date are examples of tasks created by
# instantiating the Postgres Operator

import os
import datetime
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.postgres_operator import SQLExecuteQueryOperator

ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
DAG_ID = "postgres_operator_dag"

with DAG(
    dag_id=DAG_ID,
    start_date=datetime.datetime(2020, 2, 2),
    schedule="@once",
    catchup=False,
) as dag:
    create_pet_table = SQLExecuteQueryOperator(
        task_id="create_pet_table",
        sql="""
            CREATE TABLE IF NOT EXISTS pet (
            pet_id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            pet_type VARCHAR NOT NULL,
            birth_date DATE NOT NULL,
            OWNER VARCHAR NOT NULL);
          """,
    )
    populate_pet_table = SQLExecuteQueryOperator(
        task_id="populate_pet_table",
        sql="""
            INSERT INTO pet (name, pet_type, birth_date, OWNER)
            VALUES ( 'Max', 'Dog', '2018-07-05', 'Jane');
            INSERT INTO pet (name, pet_type, birth_date, OWNER)
            VALUES ( 'Susie', 'Cat', '2019-05-01', 'Phil');
            INSERT INTO pet (name, pet_type, birth_date, OWNER)
            VALUES ( 'Lester', 'Hamster', '2020-06-23', 'Lily');
            INSERT INTO pet (name, pet_type, birth_date, OWNER)
            VALUES ( 'Quincy', 'Parrot', '2013-08-11', 'Anne');
            """,
    )
    get_all_pets = SQLExecuteQueryOperator(task_id="get_all_pets", sql="SELECT * FROM pet;")
    get_birth_date = SQLExecuteQueryOperator(
        task_id="get_birth_date",
        sql="SELECT * FROM pet WHERE birth_date BETWEEN SYMMETRIC %(begin_date)s AND %(end_date)s",
        parameters={"begin_date": "2020-01-01", "end_date": "2020-12-31"},
        hook_params={"options": "-c statement_timeout=3000ms"},
    )

    create_pet_table >> populate_pet_table >> get_all_pets >> get_birth_date

```

--------------------------------

### Configure Google Cloud Pub/Sub Resources via CLI

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_modules/tests/system/google/event_scheduling/example_event_schedule_pubsub.html

Commands to create a Pub/Sub topic and subscription required for the event-driven workflow.

```bash
gcloud pubsub topics create test-topic --project={PROJECT_ID}
gcloud pubsub subscriptions create test-subscription --topic=test-topic --project={PROJECT_ID}
```

--------------------------------

### Install Apache Airflow HTTP Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the Apache Airflow provider for Hypertext Transfer Protocol (HTTP) services. The installation is performed using pip.

```bash
pip install 'apache-airflow-providers-http'
```

--------------------------------

### Install Apache Livy Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-livy/stable/index.html

Command to install the Apache Livy provider package into an existing Airflow environment.

```bash
pip install apache-airflow-providers-apache-livy
```

--------------------------------

### Install MySQL Provider Package

Source: https://airflow.apache.org/docs/apache-airflow-providers-mysql/stable/index.html

Provides the command to install the apache-airflow-providers-mysql package using pip. This is the standard method for adding the MySQL provider to an existing Airflow installation.

```bash
pip install apache-airflow-providers-mysql
```

--------------------------------

### Initialize and Use TelegramHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-telegram/stable/_api/airflow/providers/telegram/hooks/telegram/index.html

Demonstrates how to instantiate the TelegramHook using a connection ID or direct credentials, and how to send a message to a Telegram chat.

```python
# Create hook
telegram_hook = TelegramHook(telegram_conn_id="telegram_default")
# or
telegram_hook = TelegramHook(token='xxx:xxx', chat_id='-1xxx')

# Call method from telegram bot client
telegram_hook.send_message({"text": "message", "chat_id": "-1xxx"})
```

--------------------------------

### Install Tableau Provider Package

Source: https://airflow.apache.org/docs/apache-airflow-providers-tableau

Command to install the Apache Airflow Tableau provider package into an existing Airflow environment.

```bash
pip install apache-airflow-providers-tableau
```

--------------------------------

### Install Apache Beam Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-beam

Command to install the Apache Beam provider package into an existing Airflow environment.

```bash
pip install apache-airflow-providers-apache-beam
```

--------------------------------

### Install Apprise Provider for Airflow

Source: https://airflow.apache.org/docs/apache-airflow-providers-apprise/stable/index.html

This command installs the Apprise provider package for Apache Airflow. It ensures that the necessary components for using Apprise notifications within Airflow are available. The installation requires a minimum Airflow version of 2.11.0.

```bash
pip install apache-airflow-providers-apprise
```

--------------------------------

### Apache Pinot Example DAG

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-pinot/stable/_api/tests/system/apache/pinot/example_pinot/index.html

This section describes an example DAG used for testing the SQLExecuteQueryOperator with Apache Pinot.

```APIDOC
## tests.system.apache.pinot.example_pinot

This is an example DAG for the use of the SQLExecuteQueryOperator with Apache Pinot.

### Attributes

| Attribute | Description |
|---|---|
| `DAG_ID` | The unique identifier for the DAG. |
| `select_1_task` | Represents a task for selecting data. |
| `test_run` | Represents the main task for running the test. |

### Module Contents

#### `DAG_ID`

- **Type**: string
- **Description**: The DAG ID for the example Pinot DAG.

#### `select_1_task`

- **Type**: Task
- **Description**: A task that likely performs a SELECT query on Pinot.

#### `test_run`

- **Type**: Task
- **Description**: The main task for executing the system test, potentially orchestrating other tasks.
```

--------------------------------

### Install Apache Airflow JDBC Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the Apache Airflow provider for Java Database Connectivity (JDBC). This command uses pip to install the necessary package.

```bash
pip install 'apache-airflow-providers-jdbc'
```

--------------------------------

### Install Yandex Provider for Airflow

Source: https://airflow.apache.org/docs/apache-airflow-providers-yandex/stable/index.html

Installs the apache-airflow-providers-yandex package on top of an existing Airflow installation. Requires a minimum Airflow version of 2.11.0 and specific versions of yandexcloud and yandex-query-client.

```bash
pip install apache-airflow-providers-yandex
```

--------------------------------

### Install Airflow Kubernetes Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/local_kubernetes_executor.html

Command to install the necessary provider package to enable Kubernetes-based executors in Airflow.

```bash
pip install 'apache-airflow[cncf.kubernetes]'
```

--------------------------------

### Airflow BashSensor Example

Source: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/sensors.html

This example demonstrates how to create a BashSensor in Airflow to wait for a file. It configures essential parameters like task_id, bash_command, poke_interval, timeout, and mode.

```python
BashSensor(
    task_id="wait_for_file",
    bash_command="test -f /data/input.csv",
    poke_interval=60,
    timeout=60 * 60,
    mode="reschedule",
)
```

--------------------------------

### Install Airflow Core with Constraints

Source: https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html

Shows how to install only the Apache Airflow core package using a version-specific constraint file. This minimizes dependencies and ensures compatibility with the core release.

```bash
AIRFLOW_VERSION=3.1.8
PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-no-providers-${PYTHON_VERSION}.txt"
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

--------------------------------

### Install Apache Airflow IMAP Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the Apache Airflow provider for Internet Message Access Protocol (IMAP) services. This command utilizes pip for package installation.

```bash
pip install 'apache-airflow-providers-imap'
```

--------------------------------

### Install Apache Drill Provider with Extra Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-drill/stable/index.html

Command to install the Apache Drill provider package along with optional cross-provider dependencies like common.sql.

```bash
pip install apache-airflow-providers-apache-drill[common.sql]
```

--------------------------------

### Install Apache Airflow Hashicorp Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the Apache Airflow provider for Hashicorp services, including Hashicorp Vault. This command uses pip to install the specified package.

```bash
pip install 'apache-airflow-providers-hashicorp'
```

--------------------------------

### KubernetesSecretsBackend Configuration Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/_api/airflow/providers/cncf/kubernetes/secrets/kubernetes_secrets_backend/index.html

This snippet shows an example of how to configure the KubernetesSecretsBackend in airflow.cfg. It specifies the backend class and provides custom labels for discovering secrets.

```ini
[secrets]
backend = airflow.providers.cncf.kubernetes.secrets.kubernetes_secrets_backend.KubernetesSecretsBackend
backend_kwargs = {"namespace": "airflow", "connections_label": "airflow.apache.org/connection-id"}

```

--------------------------------

### Define Package Initialization

Source: https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/modules_management.html

Creates the __init__.py file to define the package and verify successful import.

```python
print("Hello from airflow_operators")
```

--------------------------------

### Install Informatica Airflow Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-informatica/stable/guides/usage.html

Command to install the Apache Airflow Informatica provider using pip. This is the first step to enable lineage tracking.

```bash
pip install apache-airflow-providers-informatica
```

--------------------------------

### Install SMTP Provider for Apache Airflow

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the SMTP provider for Apache Airflow, facilitating integration with Simple Mail Transfer Protocol. Pip must be installed to run this command.

```bash
pip install 'apache-airflow-providers-smtp'
```

--------------------------------

### tests.system.alibaba.example_maxcompute_sql Module

Source: https://airflow.apache.org/docs/apache-airflow-providers-alibaba/stable/_api/tests/system/alibaba/example_maxcompute_sql/index.html

Provides details on the attributes and module contents for the MaxCompute SQL example system test.

```APIDOC
## Module: tests.system.alibaba.example_maxcompute_sql

### Description
This module contains system test configurations for running SQL queries against Alibaba MaxCompute.

### Attributes

- **ENV_ID** (string) - The environment ID for the test.
- **DAG_ID** (string) - The DAG ID associated with this test.
- **SQL** (string) - The SQL query to be executed.
- **run_sql** (function) - A function to execute the SQL query.
- **test_run** (function) - The main test function to run the MaxCompute SQL test case.
```

--------------------------------

### Install Apache Airflow HDFS Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-hdfs/stable/index.html

Command to install the HDFS provider package into an existing Airflow environment.

```bash
pip install apache-airflow-providers-apache-hdfs
```

--------------------------------

### Example Presto DAG

Source: https://airflow.apache.org/docs/apache-airflow-providers-presto/stable/_api/tests/system/presto/example_presto/index.html

This section describes the `example_presto` DAG, which serves as an example for using the SQLExecuteQueryOperator with Presto. It outlines the DAG's attributes and the contents of its module.

```APIDOC
## tests.system.presto.example_presto

This is an example DAG for the use of the SQLExecuteQueryOperator with Presto.

### Attributes

| Attribute     | Description |
|---------------|-------------|
| `ENV_ID`      |             |
| `DAG_ID`      |             |
| `select_presto_task` |             |
| `test_run`    |             |

### Module Contents

- `ENV_ID`
- `DAG_ID`
- `select_presto_task`
- `test_run`
```

--------------------------------

### Install FAB Provider with Common Compat Extra

Source: https://airflow.apache.org/docs/apache-airflow-providers-fab/stable/index.html

This command installs the apache-airflow-providers-fab package along with the common.compat extra dependencies. This is useful when you need to leverage shared functionalities provided by the common compatibility layer.

```bash
pip install apache-airflow-providers-fab[common.compat]
```

--------------------------------

### DayOfWeekSensor Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-standard/stable/sensors/datetime.html

Shows how to use DayOfWeekSensor to check if the current day matches a specified day of the week. This example includes timeout and soft_fail parameters.

```python
t11 = DayOfWeekSensor(
    task_id="week_day_sensor_failing_on_timeout", timeout=3, soft_fail=True, week_day=WeekDay.MONDAY
)
```

--------------------------------

### Initialize and Query Azure Data Explorer

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/_api/airflow/providers/microsoft/azure/hooks/adx/index.html

Demonstrates how to instantiate the AzureDataExplorerHook and execute a KQL query against a specific database. The hook manages the connection lifecycle and returns a KustoResponseDataSet.

```python
from airflow.providers.microsoft.azure.hooks.adx import AzureDataExplorerHook

# Initialize the hook
hook = AzureDataExplorerHook(azure_data_explorer_conn_id='my_adx_conn')

# Run a KQL query
query = "MyTable | take 10"
database = "MyDatabase"
response = hook.run_query(query=query, database=database)
```

--------------------------------

### Install Libraries on Databricks Cluster

Source: https://airflow.apache.org/docs/apache-airflow-providers-databricks/stable/_api/airflow/providers/databricks/hooks/databricks/index.html

Installs specified libraries on a Databricks cluster. This function interacts with the `2.0/libraries/install` endpoint and requires a JSON payload containing the cluster ID and a list of libraries to install.

```python
def install(json: dict):
    """
    Install libraries on the cluster.
    Utility function to call the `2.0/libraries/install` endpoint.

    Parameters:
        json (dict): json dictionary containing cluster_id and an array of library
    """
    pass
```

--------------------------------

### Install Apache Drill Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-drill/stable/index.html

Command to install the Apache Drill provider package into an existing Airflow environment.

```bash
pip install apache-airflow-providers-apache-drill
```

--------------------------------

### Download and Verify Provider Packages (Bash)

Source: https://airflow.apache.org/docs/apache-airflow-providers-influxdb/stable/installing-providers-from-sources.html

This bash script downloads a specified Apache Airflow provider package (wheel file), its ASC signature, and its SHA512 checksum file from PyPI. It uses `pip download` to get the package and `curl` to fetch the signature and checksum files. The script then prints the directory where these files are stored for manual verification. It creates a temporary directory that should be removed after verification.

```bash
#!/bin/bash
PACKAGE_VERSION=2.10.3
PACKAGE_NAME=apache-airflow-providers-influxdb
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_influxdb-2.10.3-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_influxdb-2.10.3-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_influxdb-2.10.3-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_influxdb-2.10.3-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### Install Apache Airflow Qdrant Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

This snippet shows the command to install the Apache Airflow provider for Qdrant. This integration allows for managing Qdrant vector databases with Airflow.

```bash
pip install 'apache-airflow-providers-qdrant'
```

--------------------------------

### Install Cohere Provider Package

Source: https://airflow.apache.org/docs/apache-airflow-providers-cohere/stable/index.html

Command to install the Cohere provider package into an existing Apache Airflow environment using pip.

```bash
pip install apache-airflow-providers-cohere
```

--------------------------------

### Airflow Kubernetes CMD Decorator Examples

Source: https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html

Demonstrates the usage of the @task.kubernetes_cmd decorator for running tasks in Kubernetes pods. It shows variations like full command specification and using args_only=True, as well as templating for dynamic pod names.

```python
    @task
    def foo() -> str:
        return "foo"

    @task
    def bar() -> str:
        return "bar"

    @task.kubernetes_cmd(
        image="bash:5.2",
        name="full_cmd",
        in_cluster=False,
    )
    def execute_in_k8s_pod_full_cmd(foo_result: str, bar_result: str) -> list[str]:
        return ["echo", "-e", f"With full cmd:\t{foo_result}\t{bar_result}"]

    # The args_only parameter is used to indicate that the decorated function will
    # return a list of arguments to be passed as arguments to the container entrypoint:
    # in this case, the `bash` command
    @task.kubernetes_cmd(args_only=True, image="bash:5.2", in_cluster=False)
    def execute_in_k8s_pod_args_only(foo_result: str, bar_result: str) -> list[str]:
        return ["-c", f"echo -e 'With args only:\t{foo_result}\t{bar_result}'"]

    # Templating can be used in the returned command and all other templated fields in
    # the decorator parameters.
    @task.kubernetes_cmd(image="bash:5.2", name="my-pod-{{ ti.task_id }}", in_cluster=False)
    def apply_templating(message: str) -> list[str]:
        full_message = "Templated task_id: {{ ti.task_id }}, dag_id: " + message
        return ["echo", full_message]

    foo_result = foo()
    bar_result = bar()

    full_cmd_instance = execute_in_k8s_pod_full_cmd(foo_result, bar_result)
    args_instance = execute_in_k8s_pod_args_only(foo_result, bar_result)

    [full_cmd_instance, args_instance] >> apply_templating("{{ dag.dag_id }}")

```

--------------------------------

### GET /sftp/file/modtime

Source: https://airflow.apache.org/docs/apache-airflow-providers-sftp/stable/_api/airflow/providers/sftp/hooks/sftp/index.html

Get the last modification time of a specific file on the SFTP server.

```APIDOC
## GET /sftp/file/modtime

### Description
Returns the last modification timestamp for a given remote file path.

### Method
GET

### Endpoint
/sftp/file/modtime

### Parameters
#### Query Parameters
- **path** (str) - Required - The full path to the remote file.

### Response
#### Success Response (200)
- **mod_time** (datetime) - The last modification timestamp.

#### Response Example
{
  "mod_time": "2023-10-27T10:00:00Z"
}
```

--------------------------------

### POST /sagemaker/training-job

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/operators/sagemaker/index.html

Starts a model training job in Amazon SageMaker.

```APIDOC
## POST /sagemaker/training-job

### Description
Starts a model training job. After training completes, Amazon SageMaker saves the resulting model artifacts to an Amazon S3 location that you specify.

### Method
POST

### Endpoint
/sagemaker/training-job

### Parameters
#### Request Body
- **config** (dict) - Required - The configuration necessary to start a training job (templated).
- **wait_for_completion** (bool) - Optional - Set to True to wait until the training job finishes.
- **print_log** (bool) - Optional - Whether to print logs during training.
```

--------------------------------

### Configure Azure File Share Connection via Environment Variable

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/connections/azure_fileshare.html

Example of setting up an Azure File Share connection using environment variables with URI syntax. This method allows for flexible authentication, including token credentials.

```bash
export AIRFLOW_CONN_WASP_DEFAULT='azure_fileshare://blob%20username@myblob.com?sas_token=token'
```

--------------------------------

### Install airflowctl from PyPI using pip

Source: https://airflow.apache.org/docs/apache-airflow-ctl/stable/installation/installing-from-pypi.html

This command installs the specified version of the apache-airflow-ctl package from PyPI using pip. It's a common method for installing Airflow's command-line interface in a reproducible manner. Ensure you are in a virtual environment for best practices.

```bash
pip install "apache-airflow-ctl==0.1.3"
```

--------------------------------

### Install ODBC dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-odbc/stable/operators.html

Command to install the necessary Python package for ODBC support in Airflow.

```bash
pip install apache-airflow[odbc]
```

--------------------------------

### Example Sensor DAG Attributes

Source: https://airflow.apache.org/docs/apache-airflow-providers-standard/stable/_api/airflow/providers/standard/example_dags/example_sensors/index.html

This section details the attributes available in the example sensor DAGs.

```APIDOC
## Attributes in airflow.providers.standard.example_dags.example_sensors

### `t0`

An example attribute within the sensor DAG module. Its specific purpose would depend on the DAG's implementation.
```

--------------------------------

### Datadog Secret Management Example (Text)

Source: https://airflow.apache.org/docs/apache-airflow-providers-datadog/stable/connections/datadog.html

This example shows the naming convention for storing Datadog connection details in a secret management system, using the default connection ID.

```text
secret name: airflow/connections/datadog_default
```

--------------------------------

### Install Alibaba Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-alibaba/stable/index.html

Shows the basic command to install the apache-airflow-providers-alibaba package using pip. This is the primary method for adding Alibaba Cloud integration to an Airflow environment.

```bash
pip install apache-airflow-providers-alibaba
```

--------------------------------

### Initialize PinotDbApiHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-pinot/stable/hooks.html

Demonstrates how to instantiate the PinotDbApiHook to execute SQL queries against an Apache Pinot instance. This hook utilizes the standard-SQL endpoint.

```python
@task
def pinot_dbi_api():
    PinotDbApiHook(
        task_id="run_example_pinot_script",
        pinot="ls /;",
        pinot_options="-x local",
    )
```

--------------------------------

### Databricks Example Sensors

Source: https://airflow.apache.org/docs/apache-airflow-providers-databricks/stable/_api/tests/system/databricks/example_databricks_sensors/index.html

Details of the example Databricks sensors, including their attributes and module contents.

```APIDOC
## tests.system.databricks.example_databricks_sensors

### Description
This module contains example Databricks sensors used for system testing in Apache Airflow.

### Attributes
- **ENV_ID** (string) - Environment ID for the test.
- **DAG_ID** (string) - The ID of the DAG.
- **connection_id** (string) - The Airflow connection ID for Databricks.
- **test_run** (object) - An object representing the test run configuration.

### Module Contents
- `ENV_ID`
- `DAG_ID`
- `connection_id`
- `test_run`
```

--------------------------------

### Start Airflow API Server

Source: https://airflow.apache.org/docs/stable/start.html

Starts the Airflow API server, which is responsible for handling API requests and serving the Airflow UI. This command must be running for users to access the Airflow UI.

```bash
airflow api-server --port 8080
```

--------------------------------

### tests.system.alibaba.example_oss_object

Source: https://airflow.apache.org/docs/apache-airflow-providers-alibaba/stable/_api/tests/system/alibaba/example_oss_object/index.html

Provides details on the system test module for Alibaba OSS object operations, including its attributes and module contents.

```APIDOC
## tests.system.alibaba.example_oss_object

### Description
This module contains system tests for Alibaba OSS object operations.

### Attributes

- **ENV_ID** (string) - Environment identifier.
- **DAG_ID** (string) - The ID of the DAG being tested.
- **REGION** (string) - The AWS region for the OSS operation.
- **create_object** (function) - Function to create an OSS object.
- **test_run** (function) - Function to execute the test run.

### Module Contents

- **ENV_ID**: Environment identifier.
- **DAG_ID**: The ID of the DAG being tested.
- **REGION**: The AWS region for the OSS operation.
- **create_object**: Function to create an OSS object.
- **test_run**: Function to execute the test run.
```

--------------------------------

### Install Apache Spark Provider with pyspark extra

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-spark/stable/changelog.html

To maintain support for spark connection types other than spark-connect, the pyspark package must be installed as an extra dependency. This is necessary because the pyspark package is now optional to reduce installation size.

```bash
pip install apache-airflow-providers-apache-spark[pyspark]==6.0.0
```

--------------------------------

### Start SageMaker Notebook Instance

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/operators/sagemaker/index.html

The SageMakerStartNoteBookOperator initiates the startup sequence for a SageMaker notebook instance. It ensures the instance reaches the desired state before proceeding if wait_for_completion is enabled.

```python
from airflow.providers.amazon.aws.operators.sagemaker import SageMakerStartNoteBookOperator

start_notebook = SageMakerStartNoteBookOperator(
    task_id='start_notebook_task',
    instance_name='my-notebook-instance',
    wait_for_completion=True
)
```

--------------------------------

### Example SQL to Slack DAG

Source: https://airflow.apache.org/docs/apache-airflow-providers-slack/stable/_api/tests/system/slack/example_sql_to_slack/index.html

This section describes the example DAG that uses the SqlToSlackOperator to send SQL query results to Slack.

```APIDOC
## tests.system.slack.example_sql_to_slack

### Description
Example DAG using SqlToSlackOperator.

### Attributes

- **SQL_CONN_ID** (string) - Description not provided.
- **ENV_ID** (string) - Description not provided.
- **DAG_ID** (string) - Description not provided.
- **test_run** (object) - Description not provided.

### Module Contents

- **SQL_CONN_ID**
- **ENV_ID**
- **DAG_ID**
- **test_run**
```

--------------------------------

### System Tests: Azure Synapse Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/_api/tests/system/microsoft/azure/example_azure_synapse/index.html

This section details the system tests for the Azure Synapse example within Apache Airflow.

```APIDOC
## tests.system.microsoft.azure.example_azure_synapse

### Description
This module contains system tests for the Azure Synapse example.

### Attributes

- **AIRFLOW_HOME** (string) - The Airflow home directory.
- **EXECUTION_TIMEOUT** (int) - The execution timeout in seconds.
- **default_args** (dict) - Default arguments for the DAG.
- **SPARK_JOB_PAYLOAD** (dict) - Payload for the Spark job.

### Functions

- **run_spark_job** (function) - A function to run a Spark job.
- **test_run** (function) - The main test function to execute the Azure Synapse example.
```

--------------------------------

### Limiting Setup Scope with EmptyOperator in Airflow

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/setup-and-teardown.html

Shows how to use an `EmptyOperator` to explicitly limit the scope of a setup task when a teardown is not desired for all downstream tasks. This prevents clearing the setup task when unrelated downstream tasks are cleared.

```python
create_cluster >> run_query >> other_task
run_query >> EmptyOperator(task_id="cluster_teardown").as_teardown(setups=create_cluster)
```

--------------------------------

### Install Go Module Dependencies - Python

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/go_module_utils/index.html

Installs the dependencies for a given Go module. This function requires the path to the Go module directory.

```python
def install_dependencies(_go_module_path_: str):
    """Install dependencies for a Go module.

    Parameters:
        _go_module_path_ (str): The path to the directory containing the Go module.
    """
    pass
```

--------------------------------

### Initialize JenkinsHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-jenkins/stable/_api/airflow/providers/jenkins/hooks/jenkins/index.html

Example of how to instantiate the JenkinsHook class to interact with a Jenkins server using a specific connection ID.

```python
from airflow.providers.jenkins.hooks.jenkins import JenkinsHook

# Initialize the hook with a connection ID
hook = JenkinsHook(conn_id='jenkins_default')

# Retrieve the Jenkins server instance
server = hook.get_jenkins_server()
```

--------------------------------

### Install Apache Airflow ODBC Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-odbc/stable/index.html

This command installs the apache-airflow-providers-odbc package. It ensures compatibility with common Airflow provider functionalities.

```bash
pip install apache-airflow-providers-odbc
```

--------------------------------

### Initialize and Use MongoHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-mongo/stable/_api/airflow/providers/mongo/hooks/mongo/index.html

Demonstrates how to instantiate the MongoHook and use it as a context manager to interact with a MongoDB collection.

```python
from airflow.providers.mongo.hooks.mongo import MongoHook

with MongoHook(mongo_conn_id='my_mongo_conn') as hook:
    collection = hook.get_collection(mongo_collection='my_collection', mongo_db='my_db')
    result = collection.find_one({'key': 'value'})
```

--------------------------------

### Install InfluxDB Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-influxdb/stable/index.html

Command to install the InfluxDB provider package for Apache Airflow via pip.

```bash
pip install apache-airflow-providers-influxdb
```

--------------------------------

### Install ODBC Provider with Extra Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-odbc/stable/index.html

This command installs the apache-airflow-providers-odbc package along with the 'common.compat' extra, which provides compatibility features for common Airflow providers.

```bash
pip install apache-airflow-providers-odbc[common.compat]
```

--------------------------------

### Botocore Config Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/kinesis_analytics.html

Provides an example of a botocore configuration dictionary that can be used to customize AWS SDK behavior, such as setting retry modes, timeouts, and regional endpoints.

```json
{
    "signature_version": "unsigned",
    "s3": {
        "us_east_1_regional_endpoint": true,
    },
    "retries": {
      "mode": "standard",
      "max_attempts": 10,
    },
    "connect_timeout": 300,
    "read_timeout": 300,
    "tcp_keepalive": true,
}
```

--------------------------------

### Create Directory with Parents

Source: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/objectstorage.html

Shows how to use the `mkdir` method to create a directory in object storage. The `parents=True` argument ensures that any necessary parent directories are also created.

```python
from airflow.sdk import ObjectStoragePath

path = ObjectStoragePath("s3://my-bucket/new_dir/subdir/")
path.mkdir(parents=True)
```

--------------------------------

### SlackWebhookHook Usage Examples - Python

Source: https://airflow.apache.org/docs/apache-airflow-providers-slack/stable/_api/airflow/providers/slack/hooks/slack_webhook/index.html

Demonstrates how to instantiate and use the SlackWebhookHook to send messages to Slack. It shows examples for sending both dictionary-formatted messages and simple text messages.

```python
from airflow.providers.slack.hooks.slack_webhook import SlackWebhookHook

# Create hook
hook = SlackWebhookHook(slack_webhook_conn_id="slack_default")

# Post message in Slack channel by JSON formatted message
# See: https://api.slack.com/messaging/webhooks#posting_with_webhooks
hook.send_dict({"text": "Hello world!"})

# Post simple message in Slack channel
hook.send_text("Hello world!")
```

--------------------------------

### Dropping Tables Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-teradata/stable/operators/tpt.html

An example demonstrating how to use the DdlOperator to drop multiple tables in a Teradata database.

```APIDOC
## Dropping tables in Teradata

You can use the DdlOperator to drop tables in Teradata. The following example demonstrates how to drop multiple tables:

```python
from airflow.providers.teradata.operators.ddl import DdlOperator

drop_tables_task = DdlOperator(
    task_id='drop_multiple_tables',
    ddl=[
        'DROP TABLE IF EXISTS table1;',
        'DROP TABLE IF EXISTS table2;',
        'DROP TABLE IF EXISTS table3;',
    ],
    teradata_conn_id='teradata_default',
)
```
```

--------------------------------

### Run Go Pipeline with DirectRunner

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-beam/stable/operators.html

Demonstrates executing a Go pipeline using the DirectRunner. It shows both local file execution and GCS-based execution with pipeline options.

```python
start_go_pipeline_local_direct_runner = BeamRunGoPipelineOperator(
    task_id="start_go_pipeline_local_direct_runner",
    go_file="files/apache_beam/examples/wordcount.go",
)

start_go_pipeline_direct_runner = BeamRunGoPipelineOperator(
    task_id="start_go_pipeline_direct_runner",
    go_file=GCS_GO,
    pipeline_options={"output": GCS_OUTPUT},
)
```

--------------------------------

### Trino Example DAG Attributes

Source: https://airflow.apache.org/docs/apache-airflow-providers-trino/stable/_api/tests/system/trino/example_trino/index.html

This section lists the attributes used within the Trino example DAG.

```APIDOC
## Attributes

`SCHEMA` |   
---|---
`TABLE` |   
`TABLE1` |   
`TABLE2` |   
`trino_create_schema` |   
`test_run` |   
```

--------------------------------

### Install Cohere Provider with Cross-Provider Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-cohere/stable/index.html

Command to install the Cohere provider package along with specific extra dependencies, such as common.compat, to enable full feature support.

```bash
pip install apache-airflow-providers-cohere[common.compat]
```

--------------------------------

### PgVectorIngestOperator Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-pgvector/stable/_modules/tests/system/pgvector/example_pgvector.html

This example demonstrates how to use the PgVectorIngestOperator to insert data into a PostgreSQL table with a vector column.

```APIDOC
## POST /api/v1/dags/example_pgvector_dag/dagRuns

### Description
This endpoint triggers a DAG run for the `example_pgvector_dag` which includes an example of using the `PgVectorIngestOperator`.

### Method
POST

### Endpoint
/api/v1/dags/example_pgvector_dag/dagRuns

### Parameters
#### Query Parameters
- **conf** (string) - Optional - JSON string representing the DAG run configuration.

### Request Example
```json
{
  "conf": "{}"
}
```

### Response
#### Success Response (200)
- **dag_run_id** (string) - The ID of the created DAG run.
- **dag_id** (string) - The ID of the DAG.
- **state** (string) - The state of the DAG run.

#### Response Example
```json
{
  "dag_run_id": "manual__2023-10-27T10:00:00+00:00",
  "dag_id": "example_pgvector_dag",
  "state": "running"
}
```
```

--------------------------------

### Define a Simple DAG with Task SDK

Source: https://airflow.apache.org/docs/task-sdk/stable/index.html

Example demonstrating how to define a basic DAG and task using the new airflow.sdk decorators.

```python
from airflow.sdk import dag, task

@dag
def example_simplest_dag():
    @task
    def my_task():
        pass

    my_task()
```

--------------------------------

### Install Sendgrid Provider for Apache Airflow

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the Sendgrid provider for Apache Airflow, enabling integration with Sendgrid services. This command requires pip.

```bash
pip install 'apache-airflow-providers-sendgrid'
```

--------------------------------

### DbtCloudListJobsOperator Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-dbt-cloud/stable/_modules/tests/system/dbt/cloud/example_dbt_cloud.html

Example demonstrating how to use the DbtCloudListJobsOperator to list dbt Cloud jobs within a project.

```APIDOC
## POST /dbt/cloud/list_jobs

### Description
Lists all dbt Cloud jobs for a given account and project.

### Method
POST

### Endpoint
/dbt/cloud/list_jobs

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **account_id** (integer) - Required - The dbt Cloud account ID.
- **project_id** (integer) - Required - The dbt Cloud project ID.

### Request Example
```json
{
  "account_id": 106277,
  "project_id": 160645
}
```

### Response
#### Success Response (200)
- **jobs** (array) - A list of dbt Cloud jobs, where each job is an object containing job details.

#### Response Example
```json
{
  "jobs": [
    {
      "id": 1,
      "name": "my_dbt_job_1",
      "project_id": 160645
    },
    {
      "id": 2,
      "name": "my_dbt_job_2",
      "project_id": 160645
    }
  ]
}
```
```

--------------------------------

### Manage Asana Projects

Source: https://airflow.apache.org/docs/apache-airflow-providers-asana/stable/_api/airflow/providers/asana/hooks/asana/index.html

Shows how to use the AsanaHook to manage projects, including creating, searching, and updating project details.

```python
from airflow.providers.asana.hooks.asana import AsanaHook

hook = AsanaHook(asana_conn_id='my_asana_connection')

# Create a project
project = hook.create_project(params={'name': 'New Project', 'workspace': '12345'})

# Update a project
hook.update_project(project_id='67890', params={'name': 'Updated Project Name'})
```

--------------------------------

### Install Apache Druid Provider with Extra Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-druid/stable/index.html

This command shows how to install the apache-airflow-providers-apache-druid package along with an extra dependency for Apache Hive. This allows for integration with Hive functionalities.

```bash
pip install apache-airflow-providers-apache-druid[apache.hive]
```

--------------------------------

### DbtCloudJobRunSensor Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-dbt-cloud/stable/_modules/tests/system/dbt/cloud/example_dbt_cloud.html

Example demonstrating how to use the DbtCloudJobRunSensor to monitor the status of a dbt Cloud job run.

```APIDOC
## POST /dbt/cloud/job_run_sensor

### Description
Waits for a dbt Cloud job run to complete. This sensor can operate in standard or deferred mode.

### Method
POST

### Endpoint
/dbt/cloud/job_run_sensor

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **run_id** (integer) - Required - The ID of the dbt Cloud job run to monitor.
- **timeout** (integer) - Optional - The timeout in seconds for the sensor.
- **deferrable** (boolean) - Optional - If true, the sensor will run in deferred mode. Defaults to false.

### Request Example
```json
{
  "run_id": 12345,
  "timeout": 600,
  "deferrable": false
}
```

### Response
#### Success Response (200)
- **status** (string) - The final status of the job run (e.g., 'success', 'error').

#### Response Example
```json
{
  "status": "success"
}
```
```

--------------------------------

### Install Apache Airflow Common SQL Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-common-sql

Command to install the common SQL provider package into an existing Airflow environment.

```bash
pip install apache-airflow-providers-common-sql
```

--------------------------------

### Module: tests.system.apache.pig.example_pig

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-pig/stable/_api/tests/system/apache/pig/example_pig/index.html

Details the attributes and configuration for the PigOperator example DAG used in system testing.

```APIDOC
## Module: tests.system.apache.pig.example_pig

### Description
This module provides an example DAG demonstrating the implementation and usage of the PigOperator within Apache Airflow system tests.

### Attributes
- **ENV_ID** (string) - Environment identifier for the test execution.
- **DAG_ID** (string) - The unique identifier for the DAG, set to 'example_adf_run_pipeline'.
- **run_this** (object) - Task instance for execution.
- **test_run** (object) - Task instance for validation.

### Usage
This module is intended for internal system testing and provides a reference implementation for Pig-related workflows.
```

--------------------------------

### DbtCloudGetJobRunArtifactOperator Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-dbt-cloud/stable/_modules/tests/system/dbt/cloud/example_dbt_cloud.html

Example demonstrating how to use the DbtCloudGetJobRunArtifactOperator to retrieve artifacts from a dbt Cloud job run.

```APIDOC
## POST /dbt/cloud/get_artifact

### Description
Retrieves a specific artifact from a dbt Cloud job run.

### Method
POST

### Endpoint
/dbt/cloud/get_artifact

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **run_id** (integer) - Required - The ID of the dbt Cloud job run.
- **path** (string) - Required - The path to the artifact within the job run.

### Request Example
```json
{
  "run_id": 12345,
  "path": "run_results.json"
}
```

### Response
#### Success Response (200)
- **artifact_content** (string) - The content of the requested artifact.

#### Response Example
```json
{
  "artifact_content": "{\"results\": [...], \"elapsed_time\": 120.5}"
}
```
```

--------------------------------

### Importing from airflow.sdk

Source: https://airflow.apache.org/docs/task-sdk/stable/index.html

Demonstrates the recommended way to import core components from the `airflow.sdk` namespace for Dag authoring.

```APIDOC
## Public Interface

Airflow now provides the `airflow.sdk` namespace for core authoring interfaces.

### Key imports from airflow.sdk

**Classes**
  * `airflow.sdk.Asset`
  * `airflow.sdk.BaseHook`
  * `airflow.sdk.BaseNotifier`
  * `airflow.sdk.BaseOperator`
  * `airflow.sdk.BaseOperatorLink`
  * `airflow.sdk.BaseSensorOperator`
  * `airflow.sdk.Connection`
  * `airflow.sdk.Context`
  * `airflow.sdk.DAG`
  * `airflow.sdk.EdgeModifier`
  * `airflow.sdk.Label`
  * `airflow.sdk.ObjectStoragePath`
  * `airflow.sdk.Param`
  * `airflow.sdk.TaskGroup`
  * `airflow.sdk.TaskInstanceState`
  * `airflow.sdk.DagRunState`
  * `airflow.sdk.WeightRule`
  * `airflow.sdk.Variable`

**Decorators and helper functions**
  * `airflow.sdk.asset()`
  * `airflow.sdk.dag()`
  * `airflow.sdk.setup()`
  * `airflow.sdk.task()`
  * `airflow.sdk.task_group()`
  * `airflow.sdk.teardown()`
  * `airflow.sdk.chain()`
  * `airflow.sdk.chain_linear()`
  * `airflow.sdk.cross_downstream()`
  * `airflow.sdk.get_current_context()`
  * `airflow.sdk.get_parsing_context()`
```

--------------------------------

### Install Apache Airflow Hive Provider with Extras

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-hive/stable/index.html

This command installs the apache-airflow-providers-apache-hive package along with specified extra dependencies, such as 'amazon'. This allows for integration with other cloud services.

```bash
pip install apache-airflow-providers-apache-hive[amazon]
```

--------------------------------

### Configure Docker Connection via Environment Variable

Source: https://airflow.apache.org/docs/apache-airflow-providers-docker/stable/connections/docker.html

Demonstrates how to set up a Docker connection using an environment variable. This method uses URI syntax, and all components must be URL-encoded. It includes parameters like username, password, registry URL, port, email, and reauthentication status.

```bash
export AIRFLOW_CONN_DOCKER_DEFAULT='docker://username:password@https%3A%2F%2Findex.docker.io%2Fv1:80?email=myemail%40my.com&reauth=False'
```

--------------------------------

### Initialize DagRunInfo

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/timetable.html

Demonstrates how to create a DagRunInfo object to define data intervals and execution times. It also shows the shortcut method for aligning the end of the interval with the run time.

```python
info = DagRunInfo(
    data_interval=DataInterval(start=start, end=end),
    run_after=run_after,
)

# Shortcut for when end and run_after are the same
info = DagRunInfo.interval(start=start, end=end)
assert info.data_interval.end == info.run_after
```

--------------------------------

### Install Google Package for Airflow

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/logging/stackdriver.html

This command installs the necessary Google Cloud integration for Apache Airflow, which includes the dependencies required for Stackdriver logging.

```bash
pip install 'apache-airflow[google]'

```

--------------------------------

### Build Airflow Image with UV Package Installer (Shell)

Source: https://airflow.apache.org/docs/docker-stack/build.html

Builds a production Airflow Docker image using UV as the package installer. This is an experimental feature utilizing UV's speed. It requires Docker BuildKit to be enabled.

```shell
export DOCKER_BUILDKIT=1
docker build .
    --build-arg AIRFLOW_USE_UV="true"
    --tag "my-custom-use-uv-airflow:0.0.1"
```

--------------------------------

### Install Google Provider for Airflow

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/secrets-backends/google-cloud-secret-manager-backend.html

Installs the necessary Google subpackage to enable integration with Google Cloud services, including Secret Manager.

```bash
pip install apache-airflow[google]
```

--------------------------------

### Run Airflow Standalone

Source: https://airflow.apache.org/docs/apache-airflow/stable/start.html

Initializes the database, creates an admin user, and starts all necessary Airflow components in a single process.

```bash
airflow standalone
```

--------------------------------

### Install Amazon Provider with Extra Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/index.html

Command to install the Amazon provider package along with specific cross-provider dependencies, such as Apache Hive support.

```bash
pip install apache-airflow-providers-amazon[apache.hive]
```

--------------------------------

### Install Google Cloud SDK in Airflow Docker Image

Source: https://airflow.apache.org/docs/docker-stack/recipes.html

This Dockerfile recipe installs the Google Cloud SDK, including kubectl and beta components, onto an existing Airflow image. It requires a base Airflow image as an argument and configures the environment variables for gcloud access.

```Dockerfile
ARG BASE_AIRFLOW_IMAGE
FROM ${BASE_AIRFLOW_IMAGE}

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

USER 0

ARG CLOUD_SDK_VERSION=322.0.0
ENV GCLOUD_HOME=/opt/google-cloud-sdk

ENV PATH="${GCLOUD_HOME}/bin/:${PATH}"

RUN DOWNLOAD_URL="https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz" \
    && TMP_DIR="$(mktemp -d)" \
    && curl -fL "${DOWNLOAD_URL}" --output "${TMP_DIR}/google-cloud-sdk.tar.gz" \
    && mkdir -p "${GCLOUD_HOME}" \
    && tar xzf "${TMP_DIR}/google-cloud-sdk.tar.gz" -C "${GCLOUD_HOME}" --strip-components=1 \
    && "${GCLOUD_HOME}/install.sh" \
       --bash-completion=false \
       --path-update=false \
       --usage-reporting=false \
       --additional-components alpha beta kubectl \
       --quiet \
    && rm -rf "${TMP_DIR}" \
    && rm -rf "${GCLOUD_HOME}/.install/.backup/" \
    && gcloud --version

USER ${AIRFLOW_UID}
```

--------------------------------

### Defining Cluster Policies

Source: https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/cluster-policies.html

How to implement policy functions using the Pluggy interface and setuptools entrypoints.

```APIDOC
## Defining Cluster Policies

### Description
Cluster policies allow administrators to enforce rules or mutate objects (DAGs, Tasks, Pods) globally across an Airflow environment. Policies can be defined via `airflow_local_settings.py` or via custom Python packages using the `airflow.policy` entrypoint group.

### Implementation Example
```python
from airflow.policies import hookimpl

@hookimpl
def task_policy(task) -> None:
    # Mutate task in place
    print(f"Hello from {__file__}")
```

### Entrypoint Configuration (pyproject.toml)
```toml
[project.entry-points.'airflow.policy']
_ = 'my_airflow_plugin.policies'
```
```

--------------------------------

### Install Yandex Provider with Common Compat

Source: https://airflow.apache.org/docs/apache-airflow-providers-yandex/stable/index.html

Installs the apache-airflow-providers-yandex package along with the common.compat extra dependency. This is useful for leveraging cross-provider functionalities.

```bash
pip install apache-airflow-providers-yandex[common.compat]
```

--------------------------------

### Install Apache Airflow pgvector Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

This snippet demonstrates the installation of the Apache Airflow provider for pgvector. This is necessary for integrating pgvector functionalities into Airflow DAGs.

```bash
pip install 'apache-airflow-providers-pgvector'
```

--------------------------------

### Install Kubernetes Provider with Common Compat Extra

Source: https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/index.html

This command installs the Kubernetes provider along with the 'common.compat' extra. This extra dependency might be required for certain functionalities or to ensure compatibility with other Airflow provider packages.

```bash
pip install apache-airflow-providers-cncf-kubernetes[common.compat]
```

--------------------------------

### Start EC2 Instance with Airflow

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/ec2.html

Uses the EC2StartInstanceOperator to start a specified Amazon EC2 instance. Requires the instance ID as input.

```python
start_instance = EC2StartInstanceOperator(
    task_id="start_instance",
    instance_id=instance_id,
)
```

--------------------------------

### tests.system.neo4j.example_neo4j_query

Source: https://airflow.apache.org/docs/apache-airflow-providers-neo4j/stable/_api/tests/system/neo4j/example_neo4j_query/index.html

This section describes the example Neo4j query used in Airflow system tests. It outlines the attributes and module contents related to this example.

```APIDOC
## tests.system.neo4j.example_neo4j_query

### Description
Example use of Neo4j related operators with parameters.

### Attributes

- **ENV_ID** (string) - Description for ENV_ID
- **DAG_ID** (string) - Description for DAG_ID
- **neo4j_task** (object) - Description for neo4j_task
- **test_run** (object) - Description for test_run

### Module Contents

- **ENV_ID**
- **DAG_ID**
- **neo4j_task**
- **test_run**
```

--------------------------------

### Configure Azure Connection via Environment Variable - Airflow

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/connections/azure.html

Demonstrates how to set up an Azure connection using an environment variable with URI syntax. This example shows how to specify the key path for JSON file authentication, ensuring all components are URL-encoded.

```bash
export AIRFLOW_CONN_AZURE_DEFAULT='azure://?key_path=%2Fkeys%2Fkey.json'
```

--------------------------------

### Example Weaviate Dynamic Mapping DAG

Source: https://airflow.apache.org/docs/apache-airflow-providers-weaviate/stable/_api/tests/system/weaviate/example_weaviate_dynamic_mapping_dag/index.html

This section details the example DAG which utilizes the WeaviateIngestOperator for inserting embeddings into Weaviate with dynamic mapping.

```APIDOC
## tests.system.weaviate.example_weaviate_dynamic_mapping_dag

### Description
Example DAG which uses WeaviateIngestOperator to insert embeddings to Weaviate using dynamic mapping.

### Attributes
- **COLLECTION_NAMES** (list) - A list of collection names used in the example.
- **default_args** (dict) - Default arguments for the DAG.
- **test_run** (object) - Represents a test run or execution context.

### Functions
- **example_weaviate_dynamic_mapping_dag()** - The main function defining the example DAG.

### Module Contents
- **COLLECTION_NAMES**: ['Weaviate_DTM_example_collection_1', 'Weaviate_DTM_example_collection_2']
- **default_args**: [Details of default arguments]
- **example_weaviate_dynamic_mapping_dag()**: [Source code or detailed description of the DAG logic]
- **test_run**: [Source code or detailed description of the test run object]
```

--------------------------------

### Example Sensor DAG Functions

Source: https://airflow.apache.org/docs/apache-airflow-providers-standard/stable/_api/airflow/providers/standard/example_dags/example_sensors/index.html

This section details the functions available in the example sensor DAGs, which can be used as callbacks or within DAG logic.

```APIDOC
## Functions in airflow.providers.standard.example_dags.example_sensors

### `success_callable()`

This function serves as an example callable that might be used in a DAG to indicate success.

### `failure_callable()`

This function serves as an example callable that might be used in a DAG to indicate failure.

```

--------------------------------

### GET /instances/{instance}

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/hooks/cloud_sql/index.html

Retrieve information about a specific Cloud SQL instance.

```APIDOC
## GET /instances/{instance}

### Description
Retrieves a resource containing detailed information about a specific Cloud SQL instance.

### Method
GET

### Endpoint
/instances/{instance}

### Parameters
#### Path Parameters
- **instance** (string) - Required - Database instance ID.

#### Query Parameters
- **project_id** (string) - Optional - Project ID containing the instance.

### Request Example
GET /instances/my-db-instance?project_id=my-project

### Response
#### Success Response (200)
- **instance_resource** (dict) - A dictionary containing the Cloud SQL instance details.

#### Response Example
{
  "name": "my-db-instance",
  "state": "RUNNABLE",
  "databaseVersion": "POSTGRES_13"
}
```

--------------------------------

### Install JDBC dependencies for Airflow

Source: https://airflow.apache.org/docs/apache-airflow-providers-jdbc/stable/operators.html

Install the required Python package for JDBC connectivity within an Airflow environment.

```bash
pip install apache-airflow[jdbc]
```

--------------------------------

### MSSQL Example DAG for System Tests

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-mssql/stable/_api/tests/system/microsoft/mssql/example_mssql/index.html

Demonstrates the example usage of MsSql operators within an Apache Airflow DAG for system testing purposes. It defines tasks for creating a table and running tests against a MSSQL database.

```python
import pendulum

from airflow.models.dag import DAG
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator

ENV_ID = "default_env"
DAG_ID = "example_mssql"

with DAG(
    dag_id=f"{ENV_ID}.{DAG_ID}",
    schedule=None,
    start_date=pendulum.datetime(2023, 10, 26, tz="UTC"),
    catchup=False,
    tags=["mssql"],
)
as dag:
    create_table_mssql_task = MsSqlOperator(
        task_id="create_table_mssql",
        mssql_conn_id="mssql_default",
        sql="CREATE TABLE IF NOT EXISTS test_table (id INT, name VARCHAR(50));",
    )

    test_run = MsSqlOperator(
        task_id="test_run_mssql",
        mssql_conn_id="mssql_default",
        sql="SELECT 1;",
    )

    create_table_mssql_task >> test_run

```

--------------------------------

### Qdrant Example DAG System Tests

Source: https://airflow.apache.org/docs/apache-airflow-providers-qdrant/stable/_api/tests/system/qdrant/example_dag_qdrant/index.html

This section outlines the system tests for the example DAG related to Qdrant in Apache Airflow. It includes details about the `vectors` and `test_run` attributes.

```APIDOC
## tests.system.qdrant.example_dag_qdrant

### Description
This module contains system tests for the example DAG that integrates with Qdrant.

### Attributes

| Attribute | Description |
|---|---|
| `vectors` | A predefined list of vectors used in the test. |
| `test_run` | Represents a test run or execution. |

### Module Contents

#### `vectors`

`tests.system.qdrant.example_dag_qdrant.vectors` _ = [[0.732, 0.611, 0.289, 0.421], [0.217, 0.526, 0.416, 0.981], [0.326, 0.483, 0.376, 0.136]]

Source: [source](link_to_source)

#### `test_run`

`tests.system.qdrant.example_dag_qdrant.test_run`

Source: [source](link_to_source)
```

--------------------------------

### Airflow Ignore File Glob Syntax Example

Source: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html

Example of an .airflowignore file using glob syntax to specify patterns for files and directories that Airflow should ignore. This helps in optimizing DAG discovery by excluding irrelevant files or directories.

```text
**/*project_a*
tenant_[0-9]*

```

--------------------------------

### Install Oracle Provider with Extra Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-oracle/index.html

Command to install the Oracle provider package along with specific cross-provider dependencies. This ensures that all necessary features for compatibility or SQL integration are available.

```bash
pip install apache-airflow-providers-oracle[common.compat]
```

--------------------------------

### Verify PGP Signature Example

Source: https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-sources.html

An example output of verifying a PGP signature using GPG, showing a 'Good signature' confirmation. It also highlights a common warning about untrusted signatures for self-signed keys, which is normal for release managers.

```bash
$ gpg --verify apache-airflow-3.1.8-source.tar.gz.asc apache-airflow-3.1.8-source.tar.gz
  gpg: Signature made Sat 11 Sep 12:49:54 2021 BST
  gpg:                using RSA key CDE15C6E4D3A8EC4ECF4BA4B6674E08AD7DE406F
  gpg:                issuer "kaxilnaik@apache.org"
  gpg: Good signature from "Kaxil Naik <kaxilnaik@apache.org>" [unknown]
  gpg:                 aka "Kaxil Naik <kaxilnaik@gmail.com>" [unknown]
  gpg: WARNING: The key's User ID is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: CDE1 5C6E 4D3A 8EC4 ECF4  BA4B 6674 E08A D7DE 406F

```

--------------------------------

### CassandraHook Initialization and Configuration

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-cassandra/stable/_api/airflow/providers/apache/cassandra/hooks/cassandra/index.html

Demonstrates how to initialize the CassandraHook and configure connection details, including contact points, port, SSL options, and load balancing policies. It highlights the flexibility in specifying different load balancing strategies like DCAwareRoundRobinPolicy, WhiteListRoundRobinPolicy, and TokenAwarePolicy.

```python
from airflow.providers.apache.cassandra.hooks.cassandra import CassandraHook

# Example of initializing the hook with default connection ID
cassandra_hook = CassandraHook()

# Example with a custom connection ID
# cassandra_hook = CassandraHook(cassandra_conn_id='my_cassandra_conn')

# Configuration details are typically set in Airflow connections.
# For SSL, use the 'extra' field in the connection:
# {"ssl_options": {"ca_certs": "PATH_TO_CA_CERTS"}}

# For custom load balancing policies:
# {
#     "load_balancing_policy": "DCAwareRoundRobinPolicy",
#     "load_balancing_policy_args": {
#         "local_dc": "us-east-1"
#     }
# }
```

--------------------------------

### Install Kueue on GKE Cluster

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/kubernetes_engine.html

Uses the GKEStartKueueInsideClusterOperator to install a specific version of the Kueue batch scheduler on a GKE cluster. Requires project ID, location, and cluster name.

```python
add_kueue_cluster = GKEStartKueueInsideClusterOperator(
    task_id="add_kueue_cluster",
    project_id=GCP_PROJECT_ID,
    location=GCP_LOCATION,
    cluster_name=CLUSTER_NAME,
    kueue_version="v0.6.2",
)
```

--------------------------------

### Example Remote Log Output

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/logging/gcs.html

An example of the log output generated when remote logging is successfully enabled, showing the path to the remote log file in Google Cloud Storage.

```text
*** Reading remote log from gs://<bucket where logs should be persisted>/example_bash_operator/run_this_last/2017-10-03T00:00:00/16.log.
[2017-10-03 21:57:50,056] {cli.py:377} INFO - Running on host chrisr-00532
[2017-10-03 21:57:50,093] {base_task_runner.py:115} INFO - Running: ['bash', '-c', 'airflow tasks run example_bash_operator run_this_last 2017-10-03T00:00:00 --job-id 47 --raw -S DAGS_FOLDER/example_dags/example_bash_operator.py']
[2017-10-03 21:57:51,264] {base_task_runner.py:98} INFO - Subtask: [2017-10-03 21:57:51,263] {__init__.py:45} INFO - Using executor SequentialExecutor
[2017-10-03 21:57:51,306] {base_task_runner.py:98} INFO - Subtask: [2017-10-03 21:57:51,306] {models.py:186} INFO - Filling up the DagBag from /airflow/dags/example_dags/example_bash_operator.py
```

--------------------------------

### Install and Run Ruff for Airflow Linting

Source: https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html

Provides commands to install the ruff linter and execute it against a DAG directory to identify Airflow 3.0 migration issues using the AIR rule set.

```bash
pip install "ruff>=0.15.4"
ruff check dags/ --select AIR3
```

--------------------------------

### Install Amazon Provider Package

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/index.html

Command to install the Amazon provider package for Apache Airflow using pip.

```bash
pip install apache-airflow-providers-amazon
```

--------------------------------

### Initialize and Use AzureContainerInstanceHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/_api/airflow/providers/microsoft/azure/hooks/container_instance/index.html

Example demonstrating how to instantiate the AzureContainerInstanceHook and perform basic operations like retrieving logs or checking the state of a container group.

```python
from airflow.providers.microsoft.azure.hooks.container_instance import AzureContainerInstanceHook

# Initialize the hook with a specific connection ID
hook = AzureContainerInstanceHook(azure_conn_id='my_azure_conn')

# Get the state of a container group
state = hook.get_state(resource_group='my_rg', name='my_container_group')

# Retrieve logs from a container group
logs = hook.get_logs(resource_group='my_rg', name='my_container_group', tail=500)
```

--------------------------------

### System Tests - Example Docker Module

Source: https://airflow.apache.org/docs/apache-airflow-providers-docker/stable/_api/tests/system/docker/example_docker/index.html

Details about the example_docker module within the system tests for Airflow, including its attributes and module contents.

```APIDOC
## tests.system.docker.example_docker

### Description
This section details the `example_docker` module used in system tests, outlining its attributes and exported contents.

### Attributes

| Attribute | Description |
|---|---|
| `ENV_ID` |  |
| `DAG_ID` |  |
| `t1` |  |
| `test_run` |  |

### Module Contents

#### `ENV_ID`

#### `DAG_ID`

#### `t1`

#### `test_run`
```

--------------------------------

### Example Dingding DAG

Source: https://airflow.apache.org/docs/apache-airflow-providers-dingding/stable/_api/tests/system/dingding/example_dingding/index.html

This section details the `example_dingding` DAG, which serves as an example for using the DingdingOperator in Apache Airflow.

```APIDOC
## Module: tests.system.dingding.example_dingding

### Description
This module contains an example DAG for utilizing the DingdingOperator.

### Attributes
- **ENV_ID** (string) - Environment ID.
- **DAG_ID** (string) - The unique identifier for the DAG, set to 'example_dingding_operator'.

### Functions
- **failure_callback**(context)
  - Description: The function that will be executed when a task fails.
  - Parameters:
    - **context** (dict) - The context of the executed task.

### Module Contents
- **ENV_ID**
- **DAG_ID**
- **failure_callback()**
- **text_msg_remind_none**
- **test_run**
```

--------------------------------

### Dockerfile .dockerignore Example

Source: https://airflow.apache.org/docs/docker-stack/build.html

Illustrates the use of a .dockerignore file to control which files and directories are included in the Docker build context. It shows a common pattern of ignoring everything and then explicitly allowing specific directories.

```dockerfile
# Ignore everything
**

# Allow only these directories
!airflow

```

--------------------------------

### Install Apache Airflow SMTP Provider with Extras

Source: https://airflow.apache.org/docs/apache-airflow-providers-smtp/stable/index.html

Installs the apache-airflow-providers-smtp package with optional extras, such as common compatibility features. This is useful for leveraging additional functionalities.

```bash
pip install apache-airflow-providers-smtp[common.compat]
```

--------------------------------

### Install Apache Airflow Informatica Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the Apache Airflow provider for Informatica services. Use this pip command to add the provider to your Airflow environment.

```bash
pip install 'apache-airflow-providers-informatica'
```

--------------------------------

### Install Apache Airflow MongoDB Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-mongo/index.html

This command installs the MongoDB provider package for Apache Airflow. It ensures that the necessary components for interacting with MongoDB from Airflow are available. The installation requires a minimum Airflow version and specific provider compatibility packages.

```bash
pip install apache-airflow-providers-mongo
```

--------------------------------

### CassandraHook - Connection Configuration Examples

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-cassandra/stable/_api/airflow/providers/apache/cassandra/hooks/cassandra/index.html

Illustrates how to configure different load balancing policies for the CassandraHook via Airflow connections.

```APIDOC
### Connection Configuration Examples

#### Load Balancing Policies

*   **RoundRobinPolicy** (Default)
    No specific configuration needed, uses the default.

*   **DCAwareRoundRobinPolicy**
    ```json
    {
        "load_balancing_policy": "DCAwareRoundRobinPolicy",
        "load_balancing_policy_args": {
            "local_dc": "<your_local_dc>",
            "used_hosts_per_remote_dc": 1
        }
    }
    ```

*   **WhiteListRoundRobinPolicy**
    ```json
    {
        "load_balancing_policy": "WhiteListRoundRobinPolicy",
        "load_balancing_policy_args": {
            "hosts": ["host1", "host2", "host3"]
        }
    }
    ```

*   **TokenAwarePolicy**
    ```json
    {
        "load_balancing_policy": "TokenAwarePolicy",
        "load_balancing_policy_args": {
            "child_load_balancing_policy": "RoundRobinPolicy" 
        }
    }
    ```

#### SSL Options

If SSL is enabled in Cassandra, pass a dictionary in the `extra` field as kwargs for `ssl.wrap_socket()`:

```json
{
    "ssl_options": {
        "ca_certs": "/path/to/your/ca.crt"
    }
}
```
```

--------------------------------

### Migrate Service Account Token Configuration

Source: https://airflow.apache.org/docs/helm-chart/stable/service-account-token-examples.html

Demonstrates the step-by-step transition from automatic token mounting to manual volume mounting in Helm values files. This process ensures validation before fully disabling automatic tokens.

```yaml
scheduler:
  serviceAccount:
    automountServiceAccountToken: true
    serviceAccountTokenVolume:
      enabled: false
```

```yaml
scheduler:
  serviceAccount:
    automountServiceAccountToken: true
    serviceAccountTokenVolume:
      enabled: true
      expirationSeconds: 3600
```

```yaml
scheduler:
  serviceAccount:
    automountServiceAccountToken: false
    serviceAccountTokenVolume:
      enabled: true
      expirationSeconds: 3600
```

--------------------------------

### Install Apache Airflow Provider Packages

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Commands to install specific Apache Airflow provider packages using pip. These packages enable integration with various external services and data platforms.

```bash
pip install 'apache-airflow-providers-amazon'
pip install 'apache-airflow-providers-apache-cassandra'
pip install 'apache-airflow-providers-apache-drill'
pip install 'apache-airflow-providers-apache-druid'
pip install 'apache-airflow-providers-apache-flink'
pip install 'apache-airflow-providers-apache-hdfs'
pip install 'apache-airflow-providers-apache-hive'
```

--------------------------------

### Download and Verify Provider Package (Bash)

Source: https://airflow.apache.org/docs/apache-airflow-providers-fab/stable/installing-providers-from-sources.html

This script downloads a specified Apache Airflow provider package from PyPI, along with its signature and SHA sum files. It then prints the location of the downloaded files for manual verification. Dependencies include bash, pip, and curl.

```bash
#!/bin/bash
PACKAGE_VERSION=3.6.0
PACKAGE_NAME=apache-airflow-providers-fab
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_fab-3.6.0-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_fab-3.6.0-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_fab-3.6.0-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_fab-3.6.0-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### Create Default Connections

Source: https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html

Command to create all default connections provided by installed providers.

```APIDOC
## POST /connections/create-default-connections

### Description
Automatically creates default connections for all Airflow providers that are installed in your environment.

### Method
`airflow connections create-default-connections`

### Endpoint
N/A (CLI command)

### Parameters
#### Named Arguments
- **-v, --verbose** (boolean) - Optional - Increases the verbosity of the logging output. Default: `False`

### Request Example
```json
{
  "example": "airflow connections create-default-connections -v"
}
```

### Response
(CLI output indicating success or failure)
```

--------------------------------

### Connect to a database using jaydebeapi

Source: https://airflow.apache.org/docs/apache-airflow-providers-jdbc/stable/operators.html

Establish a manual database connection using the jaydebeapi library by specifying the driver class, path, URL, and credentials.

```python
import jaydebeapi

driver_class = "com.exasol.jdbc.EXADriver"
driver_path = "/opt/airflow/drivers/exasol/EXASolution_JDBC-7.0.2/exajdbc.jar"
connection_url = "jdbc:exa:localhost"
credentials = ["", ""]

conn = jaydebeapi.connect(
    driver_class,
    connection_url,
    credentials,
    driver_path,
)
```

--------------------------------

### Install Apache Airflow via uv

Source: https://airflow.apache.org/docs/apache-airflow/stable/start.html

Installs a specific version of Apache Airflow using the uv package manager with constraint files to ensure dependency compatibility.

```bash
uv pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

--------------------------------

### Example ODBC DAG System Test

Source: https://airflow.apache.org/docs/apache-airflow-providers-odbc/stable/_api/tests/system/odbc/example_odbc/index.html

This section describes an example DAG that demonstrates the usage of the SQLExecuteQueryOperator with PostgreSQL within the Apache Airflow system tests.

```APIDOC
## tests.system.odbc.example_odbc

### Description
Example DAG demonstrating the usage of the SQLExecuteQueryOperator with Postgres.

### Attributes

| Attribute | Description |
|---|---|
| `ENV_ID` | Environment ID for the test. |
| `DAG_ID` | The unique identifier for the DAG. |
| `create_table` | A task or function to create necessary tables for the test. |
| `test_run` | The main task or function that executes the test logic. |

### Module Contents

#### `ENV_ID`

This variable holds the environment ID.

#### `DAG_ID`

This variable defines the DAG ID as 'example_odbc_operator'.

#### `create_table`

This represents a function or task for creating tables.

#### `test_run`

This represents the function or task that runs the test.
```

--------------------------------

### Install Apache Airflow Salesforce Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

This snippet shows the command to install the Apache Airflow provider for Salesforce. It enables Airflow to interact with the Salesforce platform.

```bash
pip install 'apache-airflow-providers-salesforce'
```

--------------------------------

### Create Kubernetes Namespace

Source: https://airflow.apache.org/docs/helm-chart/stable/quick-start.html

This command creates a Kubernetes namespace named 'example-namespace' which will be used to deploy Airflow. The NAMESPACE variable is exported for subsequent commands.

```bash
export NAMESPACE=example-namespace
kubectl create namespace $NAMESPACE
```

--------------------------------

### Install MongoDB Provider with Extra Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-mongo/index.html

This command installs the MongoDB provider along with optional cross-provider dependencies, such as common compatibility features. This is useful if you need to leverage extended functionalities that rely on other Airflow provider packages.

```bash
pip install apache-airflow-providers-mongo[common.compat]
```

--------------------------------

### Install Airflow Provider Extras

Source: https://airflow.apache.org/docs/apache-airflow/stable/extra-packages-ref.html

Commands to install specific provider packages for Apache Airflow. These packages include the necessary hooks, operators, and sensors for integrating with external services.

```bash
pip install 'apache-airflow[amazon]'
pip install 'apache-airflow[google]'
pip install 'apache-airflow[microsoft-azure]'
pip install 'apache-airflow[openai]'
pip install 'apache-airflow[slack]'
pip install 'apache-airflow[snowflake]'
```

--------------------------------

### POST /instances/{instance}/databases

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/hooks/cloud_sql/index.html

Create a new database inside an existing Cloud SQL instance.

```APIDOC
## POST /instances/{instance}/databases

### Description
Creates a new database within the specified Cloud SQL instance.

### Method
POST

### Endpoint
/instances/{instance}/databases

### Parameters
#### Path Parameters
- **instance** (string) - Required - The ID of the instance.

#### Request Body
- **body** (dict) - Required - Database configuration as defined by the Google Cloud SQL Admin API.
- **project_id** (string) - Optional - Project ID.

### Request Example
{
  "name": "my_new_db",
  "charset": "utf8"
}

### Response
#### Success Response (200)
- **status** (null) - Returns None upon successful creation.
```

--------------------------------

### SFTP Filesystem Operations with ObjectStoragePath

Source: https://airflow.apache.org/docs/apache-airflow-providers-sftp/stable/filesystems/sftp.html

Demonstrates how to use the ObjectStoragePath class to interact with SFTP servers. This includes reading, writing, listing directory contents, and copying files between SFTP and local storage.

```python
from airflow.sdk import ObjectStoragePath

path = ObjectStoragePath("sftp://my_conn@myserver/data/file.csv")

# read
with path.open() as f:
    data = f.read()

# write
with path.open("w") as f:
    f.write("content")

# list
for p in path.parent.iterdir():
    print(p.name)

# copy
path.copy(ObjectStoragePath("file:///tmp/local.csv"))
```

--------------------------------

### Download Airflow dependencies for air-gapped builds

Source: https://airflow.apache.org/docs/docker-stack/build.html

This script prepares the local environment by creating a directory for dependencies, downloading the specific Airflow version constraints, and fetching all required wheel files for offline installation.

```bash
mkdir -p docker-context-files
export AIRFLOW_VERSION="2.5.3"
rm docker-context-files/*.whl docker-context-files/*.tar.gz docker-context-files/*.txt || true

curl -Lo "docker-context-files/constraints-3.8.txt" \
    "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-3.8.txt"

echo
echo "Make sure you use the right python version here (should be same as in constraints)!"
echo
python --version

pip download --dest docker-context-files \
    --constraint docker-context-files/constraints-3.8.txt  \
    "apache-airflow[async,celery,elasticsearch,kubernetes,postgres,redis,ssh,statsd,virtualenv]==${AIRFLOW_VERSION}"
```

--------------------------------

### Download and Verify PyPI Provider Packages (Bash)

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-flink/stable/installing-providers-from-sources.html

This script downloads a specified Apache Airflow provider package version from PyPI, along with its PGP signature and SHA sum files. It then displays the downloaded files in a temporary directory for manual verification. Dependencies include bash, pip, and curl.

```bash
#!/bin/bash
PACKAGE_VERSION=1.8.4
PACKAGE_NAME=apache-airflow-providers-apache-flink
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_apache_flink-1.8.4-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_apache_flink-1.8.4-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_apache_flink-1.8.4-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_apache_flink-1.8.4-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### GET /tests/system/microsoft/azure/example_powerbi

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/_api/tests/system/microsoft/azure/example_powerbi/index.html

Retrieves the configuration and attributes for the PowerBI system test DAG, including the DAG ID and associated task references.

```APIDOC
## GET /tests/system/microsoft/azure/example_powerbi

### Description
This endpoint or module reference provides the configuration details for the PowerBI system test DAG, which is used to validate Microsoft Azure integration workflows.

### Method
GET

### Endpoint
tests.system.microsoft.azure.example_powerbi

### Parameters
None

### Request Example
N/A

### Response
#### Success Response (200)
- **DAG_ID** (string) - The unique identifier for the PowerBI example DAG ('example_powerbi').
- **workspaces_task** (object) - Reference to the workspace task definition.
- **test_run** (object) - Reference to the test execution logic.

#### Response Example
{
  "DAG_ID": "example_powerbi",
  "workspaces_task": "<task_reference>",
  "test_run": "<test_execution_reference>"
}
```

--------------------------------

### Teradata Compute Cluster Provision Operator Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-teradata/stable/_api/tests/system/teradata/example_teradata_compute_cluster/index.html

This section provides an example of how to use the Teradata Compute Cluster Provision Operator. It outlines the key attributes and their purpose within the system test.

```APIDOC
## tests.system.teradata.example_teradata_compute_cluster

### Description
Example use of Teradata Compute Cluster Provision Operator.

### Attributes

| Attribute Name | Description |
|---|---|
| `ENV_ID` | Environment ID |
| `DAG_ID` | DAG ID |
| `compute_cluster_provision_operation` | Represents the compute cluster provision operation |
| `test_run` | Represents a test run
```

--------------------------------

### Install Kueue Operator

Source: https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/_modules/tests/system/cncf/kubernetes/example_kubernetes_kueue.html

Installs the Kueue operator on Kubernetes using the KubernetesInstallKueueOperator. This operator is essential for managing Kueue resources.

```python
install_kueue = KubernetesInstallKueueOperator(
    task_id="install_kueue",
    kueue_version="v0.9.1",
)
```

--------------------------------

### Install Airflow Helm Chart

Source: https://airflow.apache.org/docs/helm-chart/stable/index.html

Installs the Apache Airflow Helm chart on a Kubernetes cluster using Helm 3. This command deploys Airflow with default configurations in the 'airflow' namespace.

```bash
helm repo add apache-airflow https://airflow.apache.org
helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace
```

--------------------------------

### Install Apache Iceberg Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-iceberg

Command to install the Apache Iceberg provider package for Apache Airflow using pip.

```bash
pip install apache-airflow-providers-apache-iceberg
```

--------------------------------

### ObjectStoragePath Initialization

Source: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/objectstorage.html

How to initialize an ObjectStoragePath object to interact with cloud storage buckets.

```APIDOC
## POST /airflow/sdk/ObjectStoragePath

### Description
Instantiates a path object representing a location in a cloud object store.

### Method
POST

### Endpoint
airflow.sdk.ObjectStoragePath(uri, conn_id=None)

### Parameters
#### Path Parameters
- **uri** (string) - Required - The URI of the object (e.g., s3://bucket/path).

#### Query Parameters
- **conn_id** (string) - Optional - The Airflow connection ID to use for authentication.

### Request Example
ObjectStoragePath("s3://my-bucket/", conn_id="aws_default")

### Response
#### Success Response (200)
- **ObjectStoragePath** (object) - An instance representing the cloud path.
```

--------------------------------

### Set Backend Parameters via Configuration

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/secrets-backends/google-cloud-secret-manager-backend.html

Demonstrates how to pass custom parameters like prefixes, project IDs, and impersonation chains to the Secret Manager backend using JSON in the configuration file.

```ini
[secrets]
backend = airflow.providers.google.cloud.secrets.secret_manager.CloudSecretManagerBackend
backend_kwargs = {"connections_prefix": "example-connections-prefix", "variables_prefix": "example-variables-prefix"}
```

```ini
[secrets]
backend = airflow.providers.google.cloud.secrets.secret_manager.CloudSecretManagerBackend
backend_kwargs = {"project_id": "example-project", "impersonation_chain": "impersonated_account@example_project.iam.gserviceaccount.com"}
```

--------------------------------

### Databricks SQL Example DAG

Source: https://airflow.apache.org/docs/apache-airflow-providers-databricks/stable/_api/tests/system/databricks/example_databricks_sql/index.html

This example DAG utilizes the DatabricksSqlOperator and DatabricksCopyIntoOperator. It includes tasks for creating tables, inserting data, selecting data, and loading data into Delta tables using Copy Into.

```APIDOC
## Databricks SQL Example DAG

### Description
This example DAG demonstrates the use of `DatabricksSqlOperator` and `DatabricksCopyIntoOperator`. It covers creating a table, inserting values, selecting data, and loading data from a file into a Delta table.

### Module Contents

#### `tests.system.databricks.example_databricks_sql`

This module contains an example DAG for Databricks SQL operations.

##### Attributes

- **`ENV_ID`** (string) - Environment ID for the Databricks connection.
- **`DAG_ID`** (string) - The unique identifier for the DAG. Defaults to 'example_databricks_sql_operator'.
- **`connection_id`** (string) - The Airflow connection ID for Databricks. Defaults to 'my_connection'.
- **`test_run`** (boolean) - Flag to indicate if this is a test run.

##### Example Tasks

1.  **Create and Insert**: Creates a table and inserts sample data using SQL.
2.  **Select Data**: Uses `DatabricksSqlOperator` to query data.
3.  **Select and Save**: Selects data and saves the output to a specified file path and format.
4.  **Run SQL from File**: Executes a SQL statement defined in a `test.sql` file.
5.  **Load Data with Copy Into**: Uses `DatabricksCopyIntoOperator` to load data from a file location into a Delta table.
```

--------------------------------

### tests.system.common.sql.example_sql_execute_query Module

Source: https://airflow.apache.org/docs/apache-airflow-providers-common-sql/stable/_api/tests/system/common/sql/example_sql_execute_query/index.html

Details about the example_sql_execute_query module within the system tests for Apache Airflow.

```APIDOC
## Module: tests.system.common.sql.example_sql_execute_query

### Description
This module contains example SQL execution query functionalities used in system tests.

### Attributes
- **AIRFLOW_DB_METADATA_TABLE** (string) - The name of the Airflow database metadata table.
- **connection_args** (dict) - Arguments for establishing a database connection.
- **execute_query** (function) - A function to execute a given SQL query.
- **test_run** (object) - An object representing a test run context.

### Module Contents

#### `AIRFLOW_DB_METADATA_TABLE`
- **Type**: string
- **Description**: Represents the database table used for metadata.
- **Source**: `tests.system.common.sql.example_sql_execute_query`

#### `connection_args`
- **Type**: dict
- **Description**: Connection parameters for database access.
- **Source**: `tests.system.common.sql.example_sql_execute_query`

#### `execute_query`
- **Type**: function
- **Description**: Executes a SQL query against a database.
- **Source**: `tests.system.common.sql.example_sql_execute_query`

#### `test_run`
- **Type**: object
- **Description**: Context object for running tests.
- **Source**: `tests.system.common.sql.example_sql_execute_query`
```

--------------------------------

### Module: tests.system.microsoft.azure.example_synapse_run_pipeline

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/_api/tests/system/microsoft/azure/example_synapse_run_pipeline/index.html

This module provides system tests for the Azure Synapse integration, specifically focusing on running pipelines.

```APIDOC
## Module: tests.system.microsoft.azure.example_synapse_run_pipeline

### Description
This module contains system tests for the Azure Synapse operator in Apache Airflow. It defines the environment and test execution logic for running pipelines.

### Attributes
- **ENV_ID** (string) - The unique identifier for the environment used during testing.
- **begin** (object) - The starting point or setup task for the test sequence.
- **test_run** (object) - The primary test execution function or task for the Synapse pipeline.

### Usage
This module is intended for internal system testing of the `microsoft.azure` provider package within the Airflow ecosystem.
```

--------------------------------

### Example Elasticsearch Query DAG

Source: https://airflow.apache.org/docs/apache-airflow-providers-elasticsearch/stable/_api/tests/system/elasticsearch/example_elasticsearch_query/index.html

This section details the example Airflow DAG for Elasticsearch queries, including its attributes and functions.

```APIDOC
## Example Airflow DAG for Elasticsearch Query

### Description
This is an example Airflow DAG designed to demonstrate querying Elasticsearch.

### Attributes
- **ENV_ID** (string) - Environment identifier.
- **DAG_ID** (string) - The unique identifier for the DAG.
- **CONN_ID** (string) - The Airflow connection ID for Elasticsearch.
- **execute_query** (boolean) - Flag to determine if queries should be executed.
- **test_run** (boolean) - Flag for test run mode.

### Functions
- **show_tables()** - Queries Elasticsearch to list available tables.
- **use_elasticsearch_hook()** - Uses the ElasticSearchPythonHook to print results from a local Elasticsearch instance.

### Module Contents
- `tests.system.elasticsearch.example_elasticsearch_query.ENV_ID`
- `tests.system.elasticsearch.example_elasticsearch_query.DAG_ID`
- `tests.system.elasticsearch.example_elasticsearch_query.CONN_ID`
- `tests.system.elasticsearch.example_elasticsearch_query.show_tables()`
- `tests.system.elasticsearch.example_elasticsearch_query.use_elasticsearch_hook()`
- `tests.system.elasticsearch.example_elasticsearch_query.execute_query`
- `tests.system.elasticsearch.example_elasticsearch_query.test_run`
```

--------------------------------

### Install Apprise Provider with Common Compat

Source: https://airflow.apache.org/docs/apache-airflow-providers-apprise/stable/index.html

This command installs the Apprise provider package along with the common compatibility extras. This is useful for leveraging shared functionalities across different Airflow providers. Ensure your Airflow version is at least 2.11.0.

```bash
pip install apache-airflow-providers-apprise[common.compat]
```

--------------------------------

### Initialize and Use OpenFaasHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-openfaas/stable/_api/airflow/providers/openfaas/hooks/openfaas/index.html

Demonstrates how to instantiate the OpenFaasHook and use its methods to interact with OpenFaaS functions. This hook requires a valid Airflow connection ID.

```python
from airflow.providers.openfaas.hooks.openfaas import OpenFaasHook

# Initialize the hook
hook = OpenFaasHook(conn_id='my_openfaas_conn', function_name='my-function')

# Check if function exists
exists = hook.does_function_exist()

# Invoke function synchronously
response = hook.invoke_function(body='{"data": "test"}')
```

--------------------------------

### SQL Partition Clause Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-common-sql/stable/_api/airflow/providers/common/sql/operators/sql/index.html

An example of a partial SQL statement used within the WHERE clause of a partition-based check operator.

```sql
date = '1970-01-01'
```

--------------------------------

### GET /auth/login

Source: https://airflow.apache.org/docs/apache-airflow-providers-keycloak/stable/api-ref/token-api-ref.html

Initiates the authentication process for the user.

```APIDOC
## GET /auth/login

### Description
Initiate the authentication process.

### Method
GET

### Endpoint
/auth/login

### Response
#### Success Response (200)
- **null** - Successful Response

#### Response Example
null
```

--------------------------------

### Example Message Queue Trigger System Test

Source: https://airflow.apache.org/docs/apache-airflow-providers-common-messaging/stable/_api/tests/system/common/messaging/example_message_queue_trigger/index.html

This section details the system test for example message queue triggers.

```APIDOC
## tests.system.common.messaging.example_message_queue_trigger

### Description
This module contains system tests for example message queue triggers.

### Module Contents

#### `trigger`

This likely represents the trigger component for message queue operations.

#### `asset`

This likely represents an asset related to the message queue trigger test.

#### `test_run`

This likely represents the execution of the test run for the message queue trigger.
```

--------------------------------

### KubernetesPodOperator with Logging Interval (Deferrable Mode)

Source: https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html

This example demonstrates using the `KubernetesPodOperator` in deferrable mode with a specified `logging_interval`. It includes a command to periodically echo a counter and sleep, then create an XCom file. The `get_logs=True` parameter ensures logs are fetched, and `do_xcom_push=True` enables XCom functionality.

```python
kubernetes_task_async_log = KubernetesPodOperator(
        task_id="kubernetes_task_async_log",
        namespace="kubernetes_task_async_log",
        in_cluster=False,
        name="astro_k8s_test_pod",
        image="ubuntu",
        cmds=[
            "bash",
            "-cx",
            (
                "i=0; "
                "while [ $i -ne 100 ]; "
                "do i=$(($i+1)); "
                "echo $i; "
                "sleep 1; "
                "done; "
                "mkdir -p /airflow/xcom/; "
                'echo \'{"message": "good afternoon!"}\' > /airflow/xcom/return.json'"
            ),
        ],
        do_xcom_push=True,
        deferrable=True,
        get_logs=True,
        logging_interval=5,
    )
```

--------------------------------

### Dynamic DAG Creation Example (Python)

Source: https://airflow.apache.org/docs/apache-airflow/stable/faq.html

An example demonstrating how a DAG file (`dag_file.py`) can import and create DAG objects from another file (`dag_loader.py`). This pattern is relevant when considering file parsing performance, as changes in imported files might not be immediately reflected if only the importing file's modification time is checked.

```python
from dag_loader import create_dag

# Assuming dag_id, schedule, dag_number, and default_args are defined elsewhere
dag_id = "my_dynamic_dag"
schedule = None
dag_number = 1
default_args = {}

globals()[dag.dag_id] = create_dag(dag_id, schedule, dag_number, default_args)

```

```python
from airflow.sdk import DAG
from airflow.sdk import task

import pendulum


def create_dag(dag_id, schedule, dag_number, default_args):
    dag = DAG(
        dag_id,
        schedule=schedule,
        default_args=default_args,
        pendulum.datetime(2021, 9, 13, tz="UTC"),
    )

    with dag:

        @task()
        def hello_world():
            print("Hello World")
            print(f"This is Dag: {dag_number}")

        hello_world()

    return dag

```

--------------------------------

### Parameterize DAGs with Environment Variables in Python

Source: https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html

Demonstrates how to use environment variables to parameterize DAGs, allowing for dynamic configuration of paths or database connections without hardcoding values. This improves flexibility and maintainability across different environments.

```python
import os

dest = os.environ.get("MY_DAG_DEST_PATH", "s3://default-target/path/")

```

--------------------------------

### Configure Google Cloud SQL Connection via Environment Variable

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/connections/gcp_sql.html

This example demonstrates how to set the Google Cloud SQL connection details using an environment variable in the standard URI format. It includes parameters for database type, project, location, instance, and proxy settings. Ensure all components are URL-encoded.

```bash
export AIRFLOW_CONN_GOOGLE_CLOUD_SQL_DEFAULT='gcpcloudsql://user:XXXXXXXXX@1.1.1.1:3306/mydb?database_type=mysql&project_id=example-project&location=europe-west1&instance=testinstance&use_proxy=True&sql_proxy_use_tcp=False'
```

--------------------------------

### PrestoHook - Basic Usage Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-presto/stable/_api/airflow/providers/presto/hooks/presto/index.html

Demonstrates the basic usage of the PrestoHook to connect to Presto and execute a SQL query to count records.

```python
from airflow.providers.presto.hooks.presto import PrestoHook

ph = PrestoHook()
sql = "SELECT count(1) AS num FROM airflow.static_babynames"
ph.get_records(sql)
```

--------------------------------

### Example Job Directory Structure

Source: https://airflow.apache.org/docs/apache-airflow-providers-ssh/stable/operators/ssh_remote_job.html

Visual representation of the directory structure created on the remote host for each job execution.

```text
/tmp/airflow-ssh-jobs/af_mydag_mytask_run123_try1_abc12345/
├── stdout.log         # Combined stdout/stderr
├── exit_code          # Final exit code (0 or non-zero)
├── pid                # Process ID (for on_kill)
└── status             # Optional status file (for user scripts)
```

--------------------------------

### Initialize AirbyteHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-airbyte/stable/_modules/airflow/providers/airbyte/hooks/airbyte.html

Demonstrates how to instantiate the AirbyteHook, which sets up the API session using connection parameters retrieved from Airflow's connection manager.

```python
from airflow.providers.airbyte.hooks.airbyte import AirbyteHook

# Initialize the hook using a defined connection ID
hook = AirbyteHook(airbyte_conn_id='my_airbyte_connection')
```

--------------------------------

### Define a Deferrable Sensor with Class-Level Trigger Configuration

Source: https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html

Demonstrates how to configure a sensor to start directly in the triggerer by defining class-level attributes start_from_trigger and start_trigger_args.

```python
from __future__ import annotations

from datetime import timedelta
from typing import Any

from airflow.sdk import BaseSensorOperator, Context, StartTriggerArgs


class WaitOneHourSensor(BaseSensorOperator):
    start_trigger_args = StartTriggerArgs(
        trigger_cls="airflow.providers.standard.triggers.temporal.TimeDeltaTrigger",
        trigger_kwargs={"moment": timedelta(hours=1)},
        next_method="execute_complete",
        next_kwargs=None,
        timeout=None,
    )
    start_from_trigger = True

    def execute_complete(self, context: Context, event: dict[str, Any] | None = None) -> None:
        # We have no more work to do here. Mark as complete.
        return
```

--------------------------------

### Install Apache Airflow Google Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the apache-airflow-providers-google package, which integrates Apache Airflow with various Google services. This includes Google Ads, Google Cloud Platform (GCP), Firebase, and Workspace.

```bash
pip install 'apache-airflow-providers-google'
```

--------------------------------

### Install PagerDuty Provider Package

Source: https://airflow.apache.org/docs/apache-airflow-providers-pagerduty/stable/index.html

Command to install the PagerDuty provider package into an existing Apache Airflow environment using pip.

```bash
pip install apache-airflow-providers-pagerduty
```

--------------------------------

### Initialize and Use WasbTaskHandler

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/_api/airflow/providers/microsoft/azure/log/wasb_task_handler/index.html

Demonstrates how to instantiate the WasbTaskHandler to manage task logs, including setting the context and closing the handler to trigger log uploads to Azure.

```python
from airflow.providers.microsoft.azure.log.wasb_task_handler import WasbTaskHandler

# Initialize the handler
handler = WasbTaskHandler(
    base_log_folder='/tmp/logs',
    wasb_log_folder='remote/logs',
    wasb_container='my-container'
)

# Set context for a task instance
handler.set_context(ti=task_instance)

# Close handler to upload logs to WASB
handler.close()
```

--------------------------------

### Asana Operator Examples (Python)

Source: https://airflow.apache.org/docs/apache-airflow-providers-asana/stable/operators/asana.html

Demonstrates the usage of Asana operators in Airflow for task management. Includes creating, finding, updating, and deleting tasks. Requires specifying task parameters, search criteria, or task IDs as appropriate. Dependencies include datetime and timedelta for date calculations.

```python
from airflow.providers.asana.operators.asana \
    import AsanaCreateTaskOperator, AsanaDeleteTaskOperator, AsanaFindTaskOperator, AsanaUpdateTaskOperator
from datetime import datetime, timedelta

# Placeholder variables for demonstration
ASANA_PROJECT_ID_OVERRIDE = "your_project_id"
ASANA_TASK_TO_UPDATE = "your_task_id_to_update"
ASANA_TASK_TO_DELETE = "your_task_id_to_delete"

# Create a task. `task_parameters` is used to specify attributes the new task should have.
# You must specify at least one of 'workspace', 'projects', or 'parent' in `task_parameters`
# unless these are specified in the connection. Any attributes you specify in
# `task_parameters` will override values from the connection.
create = AsanaCreateTaskOperator(
    task_id="run_asana_create_task",
    task_parameters={"notes": "Some notes about the task."},
    name="New Task Name",
)
# Find tasks matching search criteria. `search_parameters` is used to specify these criteria.
# You must specify `project`, `section`, `tag`, `user_task_list`, or both
# `assignee` and `workspace` in `search_parameters` or in the connection.
# This example shows how you can override a project specified in the connection by
# passing a different value for project into `search_parameters`
one_week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
find = AsanaFindTaskOperator(
    task_id="run_asana_find_task",
    search_parameters={"project": ASANA_PROJECT_ID_OVERRIDE, "modified_since": one_week_ago},
)
# Update a task. `task_parameters` is used to specify the new values of
# task attributes you want to update.
update = AsanaUpdateTaskOperator(
    task_id="run_asana_update_task",
    asana_task_gid=ASANA_TASK_TO_UPDATE,
    task_parameters={"notes": "This task was updated!", "completed": True},
)
# Delete a task. This task will complete successfully even if `asana_task_gid` does not exist.
delete = AsanaDeleteTaskOperator(
    task_id="run_asana_delete_task",
    asana_task_gid=ASANA_TASK_TO_DELETE,
)

create >> find >> update >> delete

```

--------------------------------

### Create and Start EC2 Instance with Airflow

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/ec2.html

Uses the EC2CreateInstanceOperator to create and start a new Amazon EC2 instance. Requires image ID, minimum and maximum instance counts, and configuration details.

```python
create_instance = EC2CreateInstanceOperator(
    task_id="create_instance",
    image_id=image_id,
    max_count=1,
    min_count=1,
    config=config,
)
```

--------------------------------

### Install Alibaba Cloud Airflow Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Command to install the Apache Airflow provider package for Alibaba Cloud integration. This allows users to manage and orchestrate resources within the Alibaba Cloud ecosystem.

```bash
pip install 'apache-airflow-providers-alibaba'
```

--------------------------------

### Initialize DataprocMetastoreRestoreServiceOperator

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/operators/dataproc_metastore/index.html

Example of how to instantiate the DataprocMetastoreRestoreServiceOperator to trigger a restore operation for a Dataproc Metastore service from a specific backup.

```python
from airflow.providers.google.cloud.operators.dataproc_metastore import DataprocMetastoreRestoreServiceOperator

restore_task = DataprocMetastoreRestoreServiceOperator(
    task_id="restore_metastore",
    project_id="my-project",
    region="us-central1",
    service_id="my-service",
    backup_project_id="my-project",
    backup_region="us-central1",
    backup_service_id="my-service",
    backup_id="my-backup-id"
)
```

--------------------------------

### Start SageMaker Notebook Instance with Airflow

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/sagemaker.html

Use the SageMakerStartNotebookOperator to launch a SageMaker Notebook Instance. This operator creates a new compute instance with the latest libraries and re-attaches the ML storage volume. The instance name is a required parameter.

```python
start_instance = SageMakerStartNoteBookOperator(
    task_id="start_instance",
    instance_name=instance_name,
)
```

--------------------------------

### Install Apache Airflow Provider Packages

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Commands to install specific Apache Airflow provider packages via pip. These packages extend Airflow's capabilities to interact with various external systems.

```bash
pip install 'apache-airflow-providers-microsoft-azure'
pip install 'apache-airflow-providers-microsoft-mssql'
pip install 'apache-airflow-providers-microsoft-psrp'
pip install 'apache-airflow-providers-microsoft-winrm'
pip install 'apache-airflow-providers-mongo'
pip install 'apache-airflow-providers-mysql'
pip install 'apache-airflow-providers-neo4j'
```

--------------------------------

### Download and Verify Airflow Provider Packages (Bash)

Source: https://airflow.apache.org/docs/apache-airflow-providers-odbc/stable/installing-providers-from-sources.html

This bash script automates the download of a specified Apache Airflow provider package version from PyPI, along with its signature (.asc) and SHA512 sum files. It utilizes `pip download` and `curl` to fetch the necessary components into a temporary directory for verification. The script then lists the downloaded files for manual inspection.

```bash
#!/bin/bash
PACKAGE_VERSION=4.12.1
PACKAGE_NAME=apache-airflow-providers-odbc
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_odbc-4.12.1-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_odbc-4.12.1-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_odbc-4.12.1-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_odbc-4.12.1-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### OpenLineage Schedule List Complex Assets DAG Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-openlineage/stable/_api/tests/system/openlineage/example_openlineage_schedule_list_complex_assets_dag/index.html

This example demonstrates a simple DAG with multiple asset logical conditions in a list schedule for Airflow 3, utilizing OpenLineage integration. It verifies schedule serialization.

```APIDOC
## tests.system.openlineage.example_openlineage_schedule_list_complex_assets_dag

### Description
Simple DAG with multiple asset logical condition in list schedule for Airflow 3. Use of list will result in the whole condition being wrapped with additional asset_all. It checks schedule serialization.

### Attributes
- `schedule`: (type unknown) - Description of the schedule attribute.
- `DAG_ID`: (string) - The unique identifier for the DAG.
- `do_nothing_task`: (type unknown) - Description of the do_nothing_task.
- `test_run`: (type unknown) - Description of the test_run.

### Module Contents

#### tests.system.openlineage.example_openlineage_schedule_list_complex_assets_dag.schedule

This module likely contains schedule-related logic or definitions.

#### tests.system.openlineage.example_openlineage_schedule_list_complex_assets_dag.DAG_ID

This is the DAG ID constant for the example DAG.

#### tests.system.openlineage.example_openlineage_schedule_list_complex_assets_dag.do_nothing_task

This represents a task that does nothing, often used for testing or as a placeholder.

#### tests.system.openlineage.example_openlineage_schedule_list_complex_assets_dag.test_run

This likely represents a test run or a function to initiate a test run.
```

--------------------------------

### Install Kueue on GKE Cluster

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/kubernetes_engine.html

Installs Kueue, a Kubernetes-native job scheduler, on a GKE cluster with a specified version using the GKEStartKueueInsideClusterOperator.

```APIDOC
## Install Kueue on GKE Cluster

### Description
Installs Kueue, a Kubernetes-native job scheduler, on a GKE cluster with a specified version using the `GKEStartKueueInsideClusterOperator`.

### Method
Not Applicable (This is a configuration example)

### Endpoint
Not Applicable

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
```python
add_kueue_cluster = GKEStartKueueInsideClusterOperator(
    task_id="add_kueue_cluster",
    project_id=GCP_PROJECT_ID,
    location=GCP_LOCATION,
    cluster_name=CLUSTER_NAME,
    kueue_version="v0.6.2",
)
```

### Response
None (This is an operator instantiation)

#### Success Response (200)
None

#### Response Example
None
```

--------------------------------

### Install Providers with Extras via PIP

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-beam/stable/changelog.html

Commands to install Apache Airflow providers with specific extras enabled. These commands are intended for use with PIP version 20.2.4 or lower to maintain compatibility with legacy dependency behavior.

```bash
pip install apache-airflow-providers-google[apache.beam]
pip install apache-airflow-providers-apache-beam[google]
```

--------------------------------

### Simple Dynamic Task Mapping Example

Source: https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/dynamic-task-mapping.html

Demonstrates a basic usage of Dynamic Task Mapping by mapping over a list defined directly within the DAG file using the `expand()` function. This creates multiple instances of a task based on the provided list elements.

```python
# Licensed to the Apache Software Foundation (ASF) under one

```

--------------------------------

### Initialize Airflow Environment with Docker Compose

Source: https://airflow.apache.org/docs/apache-airflow/stable/tutorial/pipeline.html

This script downloads the official Airflow docker-compose.yaml file, creates the required local directories for DAGs, logs, and plugins, and initializes the database before starting the services.

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker compose up airflow-init
docker compose up
```

--------------------------------

### Initialize Python Package Directory

Source: https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/modules_management.html

Creates the base directory for the custom Python package.

```bash
mkdir airflow_operators
```

--------------------------------

### Basic Airflow DateTimeTrigger Example (Python)

Source: https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html

Demonstrates the structure of a basic Airflow trigger, inheriting from `BaseTrigger`. It includes `__init__` for initialization, `serialize` for state reconstruction, and an asynchronous `run` method that yields a `TriggerEvent` after a specified time. This example highlights the use of `asyncio.sleep` and the importance of serializable arguments.

```python
import asyncio

from airflow.triggers.base import BaseTrigger, TriggerEvent
from airflow.sdk.timezone import utcnow


class DateTimeTrigger(BaseTrigger):
    def __init__(self, moment):
        super().__init__()
        self.moment = moment

    def serialize(self):
        return ("airflow.providers.standard.triggers.temporal.DateTimeTrigger", {"moment": self.moment})

    async def run(self):
        while self.moment > utcnow():
            await asyncio.sleep(1)
        yield TriggerEvent(self.moment)

```

--------------------------------

### Installing Airflow with custom values

Source: https://airflow.apache.org/docs/helm-chart/stable/manage-dag-files.html

Deploys or upgrades the Airflow Helm release using a custom configuration file.

```bash
helm upgrade --install airflow apache-airflow/airflow -f override-values.yaml
```

--------------------------------

### Vertica Connection Extras Configuration

Source: https://airflow.apache.org/docs/apache-airflow-providers-vertica/stable/connections/vertica.html

Example JSON configurations for the 'Extra' parameter in a Vertica connection. These examples demonstrate how to set parameters for connection load balancing, logging levels, SSL, session labels, connection timeouts, and backup server nodes.

```json
{
   "connection_load_balance": true,
   "log_level": "error",
   "ssl": true
}
```

```json
{
   "session_label": "airflow-session",
   "connection_timeout": 30,
   "backup_server_node": ["bck_server_1", "bck_server_2"]
}
```

--------------------------------

### Download and Verify Airflow Provider Package (Bash)

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/installing-providers-from-sources.html

This script downloads a specific version of an Apache Airflow provider package (.whl file), its signature (.asc), and its SHA512 checksum from PyPI. It then displays the downloaded files in a temporary directory for manual verification. Dependencies include 'pip' and 'curl'.

```bash
#!/bin/bash
PACKAGE_VERSION=9.24.0
PACKAGE_NAME=apache-airflow-providers-amazon
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_amazon-9.24.0-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_amazon-9.24.0-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_amazon-9.24.0-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_amazon-9.24.0-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### Example PgVector DAG

Source: https://airflow.apache.org/docs/apache-airflow-providers-pgvector/stable/_api/tests/system/pgvector/example_pgvector_openai/index.html

This section describes the example_pgvector_dag function, which serves as an example DAG for pgvector, showcasing the PgVectorIngestOperator in conjunction with OpenAI.

```APIDOC
## example_pgvector_dag()

### Description
Example pgvector DAG demonstrating usage of the PgVectorIngestOperator.

### Method
N/A (This is a function definition within a DAG)

### Endpoint
N/A

### Parameters
N/A

### Request Example
N/A

### Response
N/A

### Error Handling
N/A
```

--------------------------------

### Perform HTTP GET Request with Parameters

Source: https://airflow.apache.org/docs/apache-airflow-providers-http/stable/operators.html

Executes a GET request with query parameters. The task succeeds regardless of the response content.

```python
task_get_op = HttpOperator(
    task_id="get_op",
    method="GET",
    endpoint="get",
    data={"param1": "value1", "param2": "value2"},
    headers={},
    dag=dag,
)
```

--------------------------------

### Execute SQL Queries with DatabricksSqlHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-databricks/stable/_api/airflow/providers/databricks/hooks/databricks_sql/index.html

Shows how to use the run method to execute SQL statements. It supports passing parameters, handling results via a handler, and setting execution timeouts.

```python
hook.run(
    sql='SELECT * FROM my_table WHERE id = %(id)s',
    parameters={'id': 123},
    execution_timeout=timedelta(minutes=5)
)
```

--------------------------------

### Start Amazon Managed Service for Apache Flink Application

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/kinesis_analytics.html

Uses KinesisAnalyticsV2StartApplicationOperator to initiate the start process for a specified Flink application.

```python
start_application = KinesisAnalyticsV2StartApplicationOperator(
    task_id="start_application",
    application_name=application_name,
)
```

--------------------------------

### POST /sagemaker/create-notebook

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/operators/sagemaker/index.html

Creates a SageMaker notebook instance with specified configuration.

```APIDOC
## POST /sagemaker/create-notebook

### Description
Creates a SageMaker notebook instance for interactive development.

### Method
POST

### Endpoint
/airflow.providers.amazon.aws.operators.sagemaker.SageMakerCreateNotebookOperator

### Parameters
#### Request Body
- **instance_name** (str) - Required - The name of the notebook instance.
- **instance_type** (str) - Required - The type of instance to create.
- **role_arn** (str) - Required - The IAM role ARN for SageMaker access.
- **volume_size_in_gb** (int) - Optional - Size in GB of the EBS root volume.
- **wait_for_completion** (bool) - Optional - Whether to wait for the instance to be ready.
```

--------------------------------

### Kylin Example DAG in Airflow System Tests

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-kylin/stable/_api/tests/system/apache/kylin/example_kylin_dag/index.html

This Python script defines an example DAG for Apache Airflow's system tests. It utilizes the KylinCubeOperator to perform build, refresh, and merge operations on Kylin cubes. The DAG also includes a helper function to generate and push build times to XCom.

```python
from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.providers.apache.kylin.operators.kylin import KylinCubeOperator

ENV_ID = ""
DAG_ID = "example_kylin_operator"

def gen_build_time() -> dict[str, str]:
    """Gen build time and push to XCom (with key of “return_value”)

    :return: A dict with build time values.
    """
    build_time = pendulum.now().format("YYYY-MM-DDTHH:mm:ssZ")
    return {"build_time": build_time}


with DAG(
    dag_id=DAG_ID,
    schedule=None,
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    tags=["kylin"],
)
as dag:
    kylin_build = KylinCubeOperator(task_id="kylin_build", kylin_conn_id="kylin_default", env_id=ENV_ID, cube_name="test_cube", action="build")
    kylin_refresh = KylinCubeOperator(task_id="kylin_refresh", kylin_conn_id="kylin_default", env_id=ENV_ID, cube_name="test_cube", action="refresh")
    kylin_merge = KylinCubeOperator(task_id="kylin_merge", kylin_conn_id="kylin_default", env_id=ENV_ID, cube_name="test_cube", action="merge")

    kylin_build >> kylin_refresh >> kylin_merge

```

--------------------------------

### Module: tests.system.microsoft.mssql.example_mssql

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-mssql/stable/_api/tests/system/microsoft/mssql/example_mssql/index.html

Defines the attributes and components for the MS SQL example DAG used in system testing.

```APIDOC
## Module: tests.system.microsoft.mssql.example_mssql

### Description
This module provides an example implementation of Microsoft SQL Server operators for system testing purposes within Apache Airflow.

### Attributes
- **ENV_ID** (string) - The environment identifier for the test.
- **DAG_ID** (string) - The unique identifier for the example DAG, currently set to 'example_mssql'.
- **create_table_mssql_task** (Task) - The specific task responsible for creating a table in the MS SQL instance.
- **test_run** (Callable) - The execution entry point for the system test.

### Usage
This module is intended to be used as a reference for implementing and testing MS SQL operators in Airflow DAGs.
```

--------------------------------

### S3ToFTPOperator Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/transfer/s3_to_ftp.html

Demonstrates the usage of the S3ToFTPOperator to copy a file from an S3 bucket to an FTP server. It requires task_id, ftp_path, s3_bucket, and s3_key as parameters.

```python
s3_to_ftp_task = S3ToFTPOperator(
    task_id="ftp_to_s3_task",
    ftp_path="/tmp/ftp_path",
    s3_bucket=s3_bucket,
    s3_key=s3_key,
)
```

--------------------------------

### Create Airflow Plugin to Serve React App

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/custom-view-plugin.html

Demonstrates how to initialize a FastAPI application within an Airflow plugin to serve static assets for a React application.

```python
from pathlib import Path
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
import mimetypes
from airflow.plugins_manager import AirflowPlugin

# Ensure proper MIME types for cjs files
mimetypes.add_type("application/javascript", ".cjs")

# Create FastAPI app to serve static files
app = FastAPI()
```

--------------------------------

### Download and Verify Airflow Provider Packages (Bash)

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-drill/stable/installing-providers-from-sources.html

This script downloads a specific version of an Apache Airflow provider package from PyPI, along with its associated signature (.asc) and SHA sum (.sha512) files. It saves these files to a temporary directory and then lists the contents of that directory, prompting the user to manually verify the downloaded files according to security best practices. Dependencies include bash, pip, curl, and mktemp.

```bash
#!/bin/bash
PACKAGE_VERSION=3.3.1
PACKAGE_NAME=apache-airflow-providers-apache-drill
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_apache_drill-3.3.1-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_apache_drill-3.3.1-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_apache_drill-3.3.1-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_apache_drill-3.3.1-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### Install Apache Airflow Azure Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/operators/adls.html

Installs the necessary Apache Airflow provider for Azure services, enabling the use of Azure-specific operators.

```bash
pip install 'apache-airflow[azure]'
```

--------------------------------

### Download and Verify Provider Packages (Bash)

Source: https://airflow.apache.org/docs/apache-airflow-providers-git/stable/installing-providers-from-sources.html

This script downloads a specified Apache Airflow provider package version from PyPI, along with its ASC signature and SHA512 checksum files. It saves these to a temporary directory and lists the downloaded files for manual verification. This helps ensure the integrity and authenticity of the downloaded package.

```bash
#!/bin/bash
PACKAGE_VERSION=0.3.0
PACKAGE_NAME=apache-airflow-providers-git
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_git-0.3.0-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_git-0.3.0-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_git-0.3.0-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_git-0.3.0-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### Initialize PostgreSQL Database and User

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html

SQL commands to create the dedicated Airflow database and user, grant necessary privileges, and ensure the public schema is accessible.

```sql
CREATE DATABASE airflow_db;
CREATE USER airflow_user WITH PASSWORD 'airflow_pass';
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;
GRANT ALL ON SCHEMA public TO airflow_user;
```

--------------------------------

### Initialize Airflow Database

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

Executes the airflow-init service to run database migrations and create the default user account.

```bash
docker compose up airflow-init
```

--------------------------------

### Provider Package Structure and Entry Points

Source: https://airflow.apache.org/docs/apache-airflow-providers/howto/create-custom-providers.html

Details on how to structure a custom provider package and configure the necessary entry points in `pyproject.toml`.

```APIDOC
## Provider Package Configuration

### Description
To make a Python package available as an Airflow provider, you need to define an entry point in your `pyproject.toml` file. This entry point, specifically `apache_airflow_provider`, should return a dictionary containing metadata about your provider.

### Key Metadata Fields
- `package-name` (string): The name of the package on PyPI.
- `name` (string): A human-readable name for the provider.
- `description` (string): A description of the provider in RST format.
- `hook-class-names` (array of strings, deprecated): Hook class names for connection types (use `connection-types` for Airflow >= 2.2.0).
- `filesystems` (array of strings): Names of filesystem modules provided.
- `integrations` (array of objects): Details about integrations provided by the package.
  - `integration-name` (string): Name of the integration.
  - `external-doc-url` (string): URL for external documentation.
  - `logo` (string): URL or path to the integration's logo.
  - `tags` (array of strings): Tags describing the integration.
- `operators` (array of objects): Details about operators provided by the package.
  - `integration-name` (string): Name of the integration the operator belongs to.
  - `operator-module-name` (string): The Python module path to the operator.

### `pyproject.toml` Example
```toml
[project.entry-points]
apache_airflow_provider = "my_provider.provider_info"
```

### Provider Metadata Function Example (`my_provider/provider_info.py`)
```python
def provider_info():
    return {
        "package-name": "airflow-provider-my-custom-package",
        "name": "My Custom Package Provider",
        "description": "A custom provider for my specific needs.",
        "connection-types": [
            {
                "connection-type": "my_custom_conn",
                "hook-class-name": "my_provider.hooks.MyCustomHook",
            }
        ],
        "integrations": [
            {
                "integration-name": "my_custom_integration",
                "external-doc-url": "https://example.com/docs/my_custom_integration",
                "logo": "https://example.com/logos/my_custom_integration.png",
                "tags": ["custom", "integration"]
            }
        ],
        "operators": [
            {
                "integration-name": "my_custom_integration",
                "operator-module-name": "my_provider.operators.MyCustomOperator"
            }
        ]
    }
```

### Note on Deprecation
The `hook-class-names` field is deprecated in favor of `connection-types` for improved performance, allowing Airflow to import individual Hooks rather than all hooks at once. This change was introduced in Airflow version 2.2.0.
```

--------------------------------

### Install Apache Airflow Hive Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-hive/stable/index.html

This command installs the apache-airflow-providers-apache-hive package. Ensure your Airflow version meets the minimum requirement of 2.11.0.

```bash
pip install apache-airflow-providers-apache-hive
```

--------------------------------

### Install Sentry Integration for Airflow

Source: https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/errors.html

Installs the necessary Sentry package for Airflow integration. This is the first step to enable Sentry error tracking.

```bash
pip install 'apache-airflow[sentry]'
```

--------------------------------

### Initialize Go Module - Python

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/go_module_utils/index.html

Initializes a Go module by creating a `go.mod` file if one does not already exist. This function takes the module name and path as input.

```python
def init_module(_go_module_name_: str, _go_module_path_: str):
    """Initialize a Go module.
    If a `go.mod` file already exists, this function will do nothing.

    Parameters:
        _go_module_name_ (str): The name of the Go module to initialize.
        _go_module_path_ (str): The path to the directory containing the Go module.
    """
    pass
```

--------------------------------

### Trino Example DAG Module Contents

Source: https://airflow.apache.org/docs/apache-airflow-providers-trino/stable/_api/tests/system/trino/example_trino/index.html

This section details the module contents of the Trino example DAG, including specific variables and functions.

```APIDOC
## Module Contents

tests.system.trino.example_trino.SCHEMA _ = 'hive.cities'_[source]¶
     

tests.system.trino.example_trino.TABLE _ = 'city'_[source]¶
     

tests.system.trino.example_trino.TABLE1 _ = 'city1'_[source]¶
     

tests.system.trino.example_trino.TABLE2 _ = 'city2'_[source]¶
     

tests.system.trino.example_trino.trino_create_schema[source]¶
     

tests.system.trino.example_trino.test_run[source]¶
    
```

--------------------------------

### Module: tests.system.pinecone.example_pinecone_openai

Source: https://airflow.apache.org/docs/apache-airflow-providers-pinecone/stable/_api/tests/system/pinecone/example_pinecone_openai/index.html

This module provides the necessary attributes and functions to perform system tests for Pinecone and OpenAI integrations.

```APIDOC
## Module: tests.system.pinecone.example_pinecone_openai

### Description
This module defines the configuration and execution logic for testing Pinecone index operations combined with OpenAI data processing workflows.

### Attributes
- **index_name** (string) - The name of the Pinecone index to be used for testing.
- **namespace** (string) - The specific namespace within the Pinecone index.
- **data** (object) - The dataset used for ingestion and retrieval testing.

### Functions
- **create_index()** - Initializes the Pinecone index configuration.
- **test_run()** - Executes the full system test workflow.

### Usage Example
```python
from tests.system.pinecone.example_pinecone_openai import test_run

# Execute the system test
test_run()
```
```

--------------------------------

### Start Airflow Scheduler

Source: https://airflow.apache.org/docs/stable/start.html

Starts the Airflow scheduler, which is the core component responsible for monitoring tasks and triggering their execution based on schedules and dependencies.

```bash
airflow scheduler
```

--------------------------------

### Download and Verify PyPI Provider Packages (Bash)

Source: https://airflow.apache.org/docs/apache-airflow-providers-salesforce/stable/installing-providers-from-sources.html

This bash script automates the download of a specific Apache Airflow provider package from PyPI, along with its associated signature and SHA sum files. It utilizes `pip download` and `curl` to fetch the necessary components into a temporary directory, allowing for subsequent manual verification.

```bash
#!/bin/bash
PACKAGE_VERSION=5.13.0
PACKAGE_NAME=apache-airflow-providers-salesforce
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_salesforce-5.13.0-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_salesforce-5.13.0-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_salesforce-5.13.0-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_salesforce-5.13.0-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### DataInterval Definition

Source: https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/timetables/base/index.html

Represents a data interval for a DagRun, defining its start and end times. Both start and end must be timezone-aware datetime objects.

```python
class DataInterval(NamedTuple):
    start: pendulum.DateTime
    end: pendulum.DateTime

    @classmethod
    def exact(cls, at: pendulum.DateTime) -> 'DataInterval':
        """Represent an “interval” containing only an exact time."""
        return cls(start=at, end=at)
```

--------------------------------

### Initialize and Use SqoopHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-sqoop/stable/_api/airflow/providers/apache/sqoop/hooks/sqoop/index.html

Demonstrates how to instantiate the SqoopHook and perform a table import operation. The hook requires a connection ID and optional configuration parameters for the Sqoop job.

```python
from airflow.providers.apache.sqoop.hooks.sqoop import SqoopHook

# Initialize the hook
hook = SqoopHook(conn_id='my_sqoop_conn', verbose=True)

# Import a table from RDBMS to HDFS
hook.import_table(
    table='employees',
    target_dir='/user/hadoop/employees',
    file_type='parquet'
)
```

--------------------------------

### Extend Airflow Image with Compilation Dependencies (Dockerfile)

Source: https://airflow.apache.org/docs/docker-stack/build.html

This Dockerfile extends the base Airflow image to include packages that require compilation, such as mpi4py. It installs build-essential and mpi compiler prerequisites using apt-get before installing the Python package with pip. This ensures that packages with native extensions can be built successfully within the Docker image. The process involves updating package lists, installing dependencies, cleaning up, and then installing the required Python packages.

```docker
FROM apache/airflow:2.11.2
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         build-essential libopenmpi-dev \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" "mpi4py==4.1.1"
```

--------------------------------

### Install Snowpark Provider Package

Source: https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/operators/snowpark.html

Installs the necessary Apache Airflow provider package for Snowflake using pip. This is a prerequisite for using Snowpark operators.

```bash
pip install 'apache-airflow-providers-snowflake'
```

--------------------------------

### Implement Standard and Deferrable SFTP Sensors

Source: https://airflow.apache.org/docs/apache-airflow-providers-sftp/stable/_modules/tests/system/sftp/example_sftp_sensor.html

Demonstrates the instantiation of the SFTPSensor class in both standard and deferrable modes. Deferrable mode allows the sensor to release worker slots while waiting, improving resource efficiency.

```python
# Standard SFTPSensor
sftp_with_operator = SFTPSensor(task_id="sftp_operator", path=FULL_FILE_PATH, poke_interval=10)

# Deferrable SFTPSensor
sftp_sensor_with_async = SFTPSensor(
    task_id="sftp_operator_async", path=FULL_FILE_PATH, poke_interval=10, deferrable=True
)
```

--------------------------------

### Module: tests.system.snowflake.example_snowpark_operator

Source: https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/_api/tests/system/snowflake/example_snowpark_operator/index.html

Defines the configuration and setup functions for the Snowflake Snowpark operator system tests.

```APIDOC
## Module: tests.system.snowflake.example_snowpark_operator

### Description
This module contains example implementations and test configurations for using Snowflake Snowpark operators within Apache Airflow DAGs.

### Attributes
- **SNOWFLAKE_CONN_ID** (string) - The connection ID used to authenticate with Snowflake. Default: 'my_snowflake_conn'.
- **DAG_ID** (string) - The unique identifier for the example Snowpark operator DAG. Default: 'example_snowpark_operator'.

### Functions
#### setup_data(session)
- **Description**: Prepares the necessary data environment within a Snowflake session for testing purposes.
- **Parameters**:
  - **session** (object) - The active Snowpark session object.

### Usage Example
```python
from tests.system.snowflake.example_snowpark_operator import SNOWFLAKE_CONN_ID, DAG_ID

# Accessing the connection ID
print(f"Using connection: {SNOWFLAKE_CONN_ID}")
```
```

--------------------------------

### Registering an Airflow Listener Plugin

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/listener-plugin.html

Demonstrates how to create a custom Airflow plugin class that registers a listener module. This class should be placed in the $AIRFLOW_HOME/plugins/ directory to be loaded during startup.

```python
from airflow.plugins_manager import AirflowPlugin
import listener

class MetadataCollectionPlugin(AirflowPlugin):
    name = "MetadataCollectionPlugin"
    listeners = [listener]
```

--------------------------------

### Install Discord Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-discord/stable/index.html

Shows the basic command to install the apache-airflow-providers-discord package using pip, which is necessary for integrating Discord notifications and features into Airflow.

```bash
pip install apache-airflow-providers-discord
```

--------------------------------

### Initialize Package Path for Keycloak System Tests

Source: https://airflow.apache.org/docs/apache-airflow-providers-keycloak/stable/_modules/tests/system/keycloak.html

This code snippet initializes the package path for the system tests module using the pkgutil library. It ensures that the module is correctly recognized as part of the package namespace.

```python
__path__ = __import__("pkgutil").extend_path(__path__, __name__)
```

--------------------------------

### Configure Alternative Backend for DBFS Scheme

Source: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/objectstorage.html

Demonstrates how to attach a custom filesystem backend for a specific protocol, in this case, using DBFSFileSystem for the 'dbfs' scheme. This allows Airflow to interact with different storage systems using a consistent interface.

```python
from airflow.sdk import ObjectStoragePath
from airflow.sdk.io import attach

from fsspec.implementations.dbfs import DBFSFileSystem

attach(protocol="dbfs", fs=DBFSFileSystem(instance="myinstance", token="mytoken"))
base = ObjectStoragePath("dbfs://my-location/")
```

--------------------------------

### Create Bucket

Source: https://airflow.apache.org/docs/apache-airflow-providers-alibaba/stable/_modules/airflow/providers/alibaba/cloud/hooks/oss.html

Creates a new OSS bucket.

```APIDOC
## POST /websites/airflow_apache/create_bucket

### Description
Creates a new OSS bucket.

### Method
POST

### Endpoint
/websites/airflow_apache/create_bucket

### Parameters
#### Query Parameters
- **bucket_name** (string) - Required - The name of the bucket to create.

### Request Example
```http
POST /websites/airflow_apache/create_bucket?bucket_name=my-new-bucket
```

### Response
#### Success Response (201)
- **message** (string) - Confirmation message.

#### Response Example
```json
{
  "message": "Bucket 'my-new-bucket' created successfully."
}
```
```

--------------------------------

### Basic DAG and Task Definition

Source: https://airflow.apache.org/docs/task-sdk/stable/index.html

A simple example demonstrating how to define a basic DAG and a task using the Task SDK.

```APIDOC
## Getting Started

Define a basic Dag and task in just a few lines of Python:

```python
from airflow.sdk import dag, task


@dag
def example_simplest_dag():
    @task
    def my_task():
        pass

    my_task()
```
```

--------------------------------

### Define a Basic DAG with Task SDK

Source: https://airflow.apache.org/docs/task-sdk/stable

Example of defining a simple DAG and a task using the `@dag` and `@task` decorators from `airflow.sdk`. This demonstrates the concise syntax for creating workflows.

```python
from airflow.sdk import dag, task


@dag
def example_simplest_dag():
    @task
    def my_task():
        pass

    my_task()

```

--------------------------------

### Install Git for Airflow Versions Prior to 3.0.2

Source: https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/dag-bundles.html

Dockerfile commands to install Git and configure environment variables for Airflow environments older than 3.0.2.

```dockerfile
RUN apt-get update && apt-get install -y git
ENV GIT_PYTHON_GIT_EXECUTABLE=/usr/bin/git
ENV GIT_PYTHON_REFRESH=quiet
```

--------------------------------

### Module: tests.system.dbt.cloud.example_dbt_cloud

Source: https://airflow.apache.org/docs/apache-airflow-providers-dbt-cloud/stable/_api/tests/system/dbt/cloud/example_dbt_cloud/index.html

Reference documentation for the attributes and constants defined in the dbt cloud system test module.

```APIDOC
## Module: tests.system.dbt.cloud.example_dbt_cloud

### Description
This module provides the structure for dbt Cloud integration system tests in Apache Airflow, defining key identifiers and execution steps.

### Attributes
- **ENV_ID** (string) - Environment identifier for the dbt cloud test suite.
- **DAG_ID** (string) - The unique identifier for the example DAG, set to 'example_dbt_cloud'.
- **begin** (object) - Entry point or initialization task for the test DAG.
- **test_run** (object) - The primary execution task for the dbt cloud test run.

### Usage
These attributes are used to programmatically define and execute system tests to ensure dbt Cloud operator compatibility with the Airflow environment.
```

--------------------------------

### DataprocMetastoreCreateServiceOperator Initialization

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/operators/dataproc_metastore/index.html

This snippet shows the initialization of the DataprocMetastoreCreateServiceOperator, a Python class used in Apache Airflow to create a metastore service in Google Cloud. It accepts parameters like region, project_id, service, service_id, and optional parameters such as request_id, retry, timeout, metadata, gcp_conn_id, and impersonation_chain.

```python
class DataprocMetastoreCreateServiceOperator(_* , _region_ , _project_id_ , _service_ , _service_id_ , _request_id =None_, _retry =DEFAULT_, _timeout =None_, _metadata =()_, _gcp_conn_id ='google_cloud_default'_, _impersonation_chain =None_, _** kwargs_)[source]:
    """Bases: `airflow.providers.google.cloud.operators.cloud_base.GoogleCloudBaseOperator`
    Create a metastore service in a project and location. 

    Parameters:
        
      * **region** (_str_) – Required. The ID of the Google Cloud region that the service belongs to.
      * **project_id** (_str_) – Required. The ID of the Google Cloud project that the service belongs to.
      * **service** (_dict_ _|__google.cloud.metastore_v1.types.Service_) – 
Required. The Metastore service to create. The `name` field is ignored. The ID of the created metastore service must be provided in the request’s `service_id` field.
This corresponds to the `service` field on the `request` instance; if `request` is provided, this should not be set.
      * **service_id** (_str_) – 
Required. The ID of the metastore service, which is used as the final component of the metastore service’s name. This value must be between 2 and 63 characters long inclusive, begin with a letter, end with a letter or number, and consist of alphanumeric ASCII characters or hyphens.
This corresponds to the `service_id` field on the `request` instance; if `request` is provided, this should not be set.
      * **request_id** (_str_ _|__None_) – Optional. A unique id used to identify the request.
      * **retry** (_google.api_core.retry.Retry_ _|__google.api_core.gapic_v1.method._MethodDefault_) – Designation of what errors, if any, should be retried.
      * **timeout** (_float_ _|__None_) – The timeout for this request.
      * **metadata** (_collections.abc.Sequence_ _[__tuple_ _[__str_ _,__str_ _]__]_) – Strings which should be sent along with the request as metadata.
      * **gcp_conn_id** (_str_) – The connection ID to use connecting to Google Cloud.
      * **impersonation_chain** (_str_ _|__collections.abc.Sequence_ _[__str_ _]__|__None_) – Optional service account to impersonate using short-term credentials, or chained list of accounts required to get the access_token of the last account in the list, which will be impersonated in the request. If set as a string, the account must grant the originating account the Service Account Token Creator IAM role. If set as a sequence, the identities from the list must grant Service Account Token Creator IAM role to the directly preceding identity, with first account from the list granting this role to the originating account (templated). 
    """
```

--------------------------------

### Example External Task Parent Deferrable DAG

Source: https://airflow.apache.org/docs/apache-airflow-providers-standard/stable/_api/airflow/providers/standard/example_dags/example_external_task_parent_deferrable/index.html

This section describes the 'example_external_task_parent_deferrable' DAG, which serves as an example for external task triggering with deferrable operators.

```APIDOC
## Module airflow.providers.standard.example_dags.example_external_task_parent_deferrable

### Description
This module contains an example DAG demonstrating the use of external task triggering with deferrable operators in Apache Airflow.

### Module Contents

#### `start`
- **Description**: The main entry point or a significant component within this example DAG.
- **Source**: [source]

### Attributes

| Attribute | Description |
|---|---|
| `start` | Placeholder for a specific attribute or function within the module. |

### Navigation
- **Previous**: airflow.providers.standard.example_dags.example_external_task_parent_deferrable
- **Next**: airflow.providers.standard.example_dags.example_external_task_parent_deferrable.start
```

--------------------------------

### PgVector Example DAG in Python

Source: https://airflow.apache.org/docs/apache-airflow-providers-pgvector/stable/_api/tests/system/pgvector/example_pgvector/index.html

This Python code defines an example DAG for pgvector, showcasing the PgVectorIngestOperator. It includes attributes like TABLE_NAME and POSTGRES_CONN_ID.

```python
TABLE_NAME = 'my_table'
POSTGRES_CONN_ID = 'postgres_default'
def example_pgvector_dag():
    """Example pgvector DAG demonstrating usage of the PgVectorIngestOperator."""
    pass
test_run = None
```

--------------------------------

### Instantiate CassandraRecordSensor

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-cassandra/stable/_api/airflow/providers/apache/cassandra/sensors/record/index.html

Demonstrates how to initialize the CassandraRecordSensor to monitor a specific table for a record defined by primary keys. It requires the table name, a dictionary of keys, and the connection ID.

```python
cassandra_sensor = CassandraRecordSensor(
    table="k.t",
    keys={"p1": "v1", "p2": "v2"},
    cassandra_conn_id="cassandra_default",
    task_id="cassandra_sensor",
)
```

--------------------------------

### DataprocCreateBatchOperator Initialization (Python)

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/operators/dataproc/index.html

Initializes the DataprocCreateBatchOperator with various parameters to configure and create a batch workload in Google Cloud Dataproc. Key parameters include project ID, region, batch definition, and optional settings for retries, timeouts, and impersonation.

```python
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateBatchOperator

create_batch_task = DataprocCreateBatchOperator(
    task_id='create_dataproc_batch',
    project_id='your-gcp-project-id',
    region='your-gcp-region',
    batch={
        'name': 'projects/your-gcp-project-id/locations/your-gcp-region/batches/your-batch-id',
        'actions': [
            {
                'pyspark_batch': {
                    'main_python_package': {
                        'package': 'gs://your-bucket/your-package.tar.gz'
                    }
                }
            }
        ]
    },
    batch_id='your-batch-id',
    gcp_conn_id='google_cloud_default',
    impersonation_chain=None,
    deferrable=False,
    polling_interval_seconds=5
)
```

--------------------------------

### Azure Container Instances Operator Example DAG

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/_api/tests/system/microsoft/azure/example_azure_container_instances/index.html

This example DAG demonstrates the usage of the AzureContainerInstancesOperator for running tasks within Azure Container Instances.

```APIDOC
## Azure Container Instances Operator Example DAG

### Description
This is an example DAG for using the AzureContainerInstancesOperator.

### Attributes

- **ENV_ID** (string) - Environment ID.
- **DAG_ID** (string) - The ID of the DAG.
- **CONTAINER_REGISTRY_SERVER** (string) - The Azure Container Registry server.
- **AZURE_VOLUME_SHARE_NAME** (string) - The name of the Azure File Share for volumes.
- **AZURE_STORAGE_ACOOUNT** (string) - The Azure Storage Account name.
- **t1** (object) - Represents a task.
- **test_run** (object) - Represents a test run task.

### Module Contents

- `tests.system.microsoft.azure.example_azure_container_instances.ENV_ID`
- `tests.system.microsoft.azure.example_azure_container_instances.DAG_ID`
- `tests.system.microsoft.azure.example_azure_container_instances.CONTAINER_REGISTRY_SERVER`
- `tests.system.microsoft.azure.example_azure_container_instances.AZURE_VOLUME_SHARE_NAME`
- `tests.system.microsoft.azure.example_azure_container_instances.AZURE_STORAGE_ACOOUNT`
- `tests.system.microsoft.azure.example_azure_container_instances.t1`
- `tests.system.microsoft.azure.example_azure_container_instances.test_run`
```

--------------------------------

### Download and Verify Provider Packages (Bash)

Source: https://airflow.apache.org/docs/apache-airflow-providers-openfaas/stable/installing-providers-from-sources.html

This script downloads a specified Airflow provider package version from PyPI, along with its ASC signature and SHA512 sum files. It saves these to a temporary directory and lists the downloaded files for manual verification. Ensure you have `pip` and `curl` installed.

```bash
#!/bin/bash
PACKAGE_VERSION=3.9.3
PACKAGE_NAME=apache-airflow-providers-openfaas
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_openfaas-3.9.3-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_openfaas-3.9.3-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_openfaas-3.9.3-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_openfaas-3.9.3-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### Zendesk Custom Get Module Reference

Source: https://airflow.apache.org/docs/apache-airflow-providers-zendesk/stable/_api/tests/system/zendesk/example_zendesk_custom_get/index.html

Documentation for the Zendesk custom GET system test module, including its primary function for fetching organizations.

```APIDOC
## Module: tests.system.zendesk.example_zendesk_custom_get

### Description
This module provides a system test for the Zendesk provider, specifically focusing on custom GET requests to retrieve organization data.

### Attributes
- **ENV_ID**: Environment identifier for the test run.
- **DAG_ID**: The unique identifier for the test DAG ('zendesk_custom_get_dag').
- **test_run**: Execution context for the system test.

### Functions
#### fetch_organizations()
Retrieves a list of organizations from the Zendesk API as part of the system test workflow.

### Usage Example
```python
from tests.system.zendesk.example_zendesk_custom_get import fetch_organizations

# Execute the organization fetch function
organizations = fetch_organizations()
print(organizations)
```
```

--------------------------------

### Example DAG: example_bash_operator

Source: https://airflow.apache.org/docs/apache-airflow-providers-standard/stable/_api/airflow/providers/standard/example_dags/example_bash_operator/index.html

This DAG demonstrates the usage of the BashOperator. It includes tasks that run sequentially and can be configured to skip or run last.

```APIDOC
## airflow.providers.standard.example_dags.example_bash_operator

### Description
Example DAG demonstrating the usage of the BashOperator.

### Attributes
- **run_this_last** (Task) - A task that is designed to run last.
- **this_will_skip** (Task) - A task that is designed to be skipped under certain conditions.
```

--------------------------------

### Start Airflow Triggerer

Source: https://airflow.apache.org/docs/stable/start.html

Starts the Airflow triggerer, which is used to handle deferrable operators. This component is essential for running tasks that can be suspended and resumed later.

```bash
airflow triggerer
```

--------------------------------

### Instantiate AzureBlobStorageToGCSOperator

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/transfers/azure_blob_to_gcs/index.html

Example showing how to initialize the AzureBlobStorageToGCSOperator within an Airflow DAG to perform a data transfer.

```python
from airflow.providers.google.cloud.transfers.azure_blob_to_gcs import AzureBlobStorageToGCSOperator

transfer_task = AzureBlobStorageToGCSOperator(
    task_id='transfer_azure_to_gcs',
    blob_name='my-blob',
    container_name='my-container',
    bucket_name='my-gcs-bucket',
    object_name='my-gcs-object',
    filename='/tmp/local-file',
    wasb_conn_id='wasb_default',
    gcp_conn_id='google_cloud_default'
)
```

--------------------------------

### AWS SSM Parameter Store Secrets Backend Initialization

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/secrets/systems_manager/index.html

Illustrates the initialization of the SystemsManagerParameterStoreBackend class with various prefix and lookup pattern configurations for connections, variables, and configurations. It also shows how to pass additional Boto3 client arguments.

```python
from airflow.providers.amazon.aws.secrets.systems_manager import SystemsManagerParameterStoreBackend

# Example initialization with custom prefixes and lookup patterns
backend = SystemsManagerParameterStoreBackend(
    connections_prefix="/airflow/connections",
    connections_lookup_pattern=None,
    variables_prefix="/airflow/variables",
    variables_lookup_pattern=None,
    config_prefix="/airflow/config",
    config_lookup_pattern=None,
    profile_name="my-aws-profile",
    region_name="us-east-1"
)

```

--------------------------------

### Install Oracle Provider Package

Source: https://airflow.apache.org/docs/apache-airflow-providers-oracle/index.html

Command to install the Oracle provider package for Apache Airflow. This is required to interact with Oracle databases within Airflow DAGs.

```bash
pip install apache-airflow-providers-oracle
```

--------------------------------

### Download and Verify Airflow Provider Packages (Bash)

Source: https://airflow.apache.org/docs/apache-airflow-providers-zendesk/stable/installing-providers-from-sources.html

This bash script downloads a specified Apache Airflow provider package version from PyPI, along with its ASC signature and SHA512 sum files. It then displays the downloaded files in a temporary directory for manual verification. Dependencies include bash, pip, and curl.

```bash
#!/bin/bash
PACKAGE_VERSION=4.11.2
PACKAGE_NAME=apache-airflow-providers-zendesk
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_zendesk-4.11.2-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_zendesk-4.11.2-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_zendesk-4.11.2-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_zendesk-4.11.2-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### Install Common Compatibility Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-common-compat/index.html

Commands to install the compatibility provider package using pip. This is required for maintaining compatibility across different Airflow versions.

```bash
pip install apache-airflow-providers-common-compat
```

--------------------------------

### Submit Spark jobs using LivyOperator

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-livy/stable/operators.html

Demonstrates how to instantiate the LivyOperator to run Java and Python Spark applications. It shows how to configure task parameters such as file paths, executor counts, and class names.

```python
livy_java_task = LivyOperator(
    task_id="pi_java_task",
    file="/spark-examples.jar",
    num_executors=1,
    conf={
        "spark.shuffle.compress": "false",
    },
    class_name="org.apache.spark.examples.SparkPi",
)

livy_python_task = LivyOperator(task_id="pi_python_task", file="/pi.py", polling_interval=60)

livy_java_task >> livy_python_task
```

--------------------------------

### Install Airflow AWS Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/appflow.html

Installs the necessary Apache Airflow provider for AWS services, including Amazon AppFlow. This is a prerequisite for using the AppFlow operators.

```bash
pip install 'apache-airflow[amazon]'
```

--------------------------------

### tests.system.alibaba.example_adb_spark_sql

Source: https://airflow.apache.org/docs/apache-airflow-providers-alibaba/stable/_api/tests/system/alibaba/example_adb_spark_sql/index.html

Details of the ADB Spark SQL system test, including its attributes and module contents.

```APIDOC
## tests.system.alibaba.example_adb_spark_sql

### Description
This section details the system tests for Airflow, specifically focusing on the `example_adb_spark_sql` test suite within the Alibaba integration.

### Attributes

| Attribute | Description |
|---|---|
| `ENV_ID` | Environment ID for the test. |
| `DAG_ID` | The DAG ID used for this test. |
| `show_databases` | Function to show available databases. |
| `test_run` | Function to execute the test run. |

### Module Contents

This module contains the following key components:

- **`ENV_ID`**: Represents the environment identifier.
- **`DAG_ID`**: The unique identifier for the Airflow DAG.
- **`show_databases`**: A function designed to list available databases within the ADB Spark SQL environment.
- **`test_run`**: The primary function to initiate and execute the system test.

### Request Example

```json
{
  "message": "No specific request body defined for this test module."
}
```

### Response

#### Success Response (200)

- **status** (string) - Indicates the success of the test execution.
- **details** (object) - Contains specific information about the test results.

#### Response Example

```json
{
  "status": "success",
  "details": {
    "databases_shown": ["default", "spark_catalog"],
    "test_run_completed": true
  }
}
```
```

--------------------------------

### Download and Verify Airflow Provider Package (Bash)

Source: https://airflow.apache.org/docs/apache-airflow-providers-arangodb/stable/installing-providers-from-sources.html

This bash script downloads a specific version of an Apache Airflow provider package (e.g., apache-airflow-providers-arangodb) from PyPI, along with its associated signature (.asc) and SHA512 sum files. It then displays the downloaded files in a temporary directory for manual verification. Dependencies include bash, pip, and curl.

```bash
#!/bin/bash
PACKAGE_VERSION=2.9.3
PACKAGE_NAME=apache-airflow-providers-arangodb
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_arangodb-2.9.3-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_arangodb-2.9.3-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_arangodb-2.9.3-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_arangodb-2.9.3-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### Install Apache Airflow PostgreSQL Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

This snippet shows the command to install the Apache Airflow provider for PostgreSQL. It enables Airflow to interact with PostgreSQL databases.

```bash
pip install 'apache-airflow-providers-postgres'
```

--------------------------------

### Configure Elasticsearch TLS and Client Parameters

Source: https://airflow.apache.org/docs/apache-airflow-providers-elasticsearch/stable/logging/index.html

Demonstrates how to pass custom SSL/TLS configurations and Elasticsearch Python client parameters via the elasticsearch_configs section.

```ini
[logging]
remote_logging = True

[elasticsearch_configs]
verify_certs=True
ca_certs=/path/to/CA_certs
http_compress = True
api_key = "SOMEAPIKEY"
```

--------------------------------

### Install Amazon Provider for Airflow

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/email-config.html

Instructions for installing the Amazon subpackage for Apache Airflow using pip, which is required for using AWS SES for sending emails.

```bash
pip install 'apache-airflow[amazon]'

```

--------------------------------

### Ingest Data into Weaviate using WeaviateIngestOperator (Python)

Source: https://airflow.apache.org/docs/apache-airflow-providers-weaviate/stable/_modules/tests/system/weaviate/example_weaviate_operator.html

This example demonstrates ingesting data into a Weaviate collection using the WeaviateIngestOperator. It shows how to pass data directly from an XCom or from a callable function, utilizing the 'QuestionWithOpenAIVectorizerUsingOperator' collection.

```python
from airflow.providers.weaviate.operators.weaviate import WeaviateIngestOperator

# Example using XCom data
# xcom_data_without_vectors = store_data_without_vectors_in_xcom()
# batch_data_without_vectors_xcom_data = WeaviateIngestOperator(
#     task_id="batch_data_without_vectors_xcom_data",
#     conn_id="weaviate_default",
#     collection_name="QuestionWithOpenAIVectorizerUsingOperator",
#     input_data=xcom_data_without_vectors["return_value"],
#     trigger_rule="all_done",
# )

# Example using callable data
# batch_data_without_vectors_callable_data = WeaviateIngestOperator(
#     task_id="batch_data_without_vectors_callable_data",
#     conn_id="weaviate_default",
#     collection_name="QuestionWithOpenAIVectorizerUsingOperator",
#     input_data=get_data_without_vectors(),
#     trigger_rule="all_done",
# )
```

--------------------------------

### Install SendGrid Provider for Airflow

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/email-config.html

Instructions for installing the SendGrid provider for Apache Airflow using pip. This enables Airflow to send emails via SendGrid.

```bash
pip install 'apache-airflow[sendgrid]' --constraint ...

```

```bash
pip install 'apache-airflow-providers-sendgrid' --constraint ...

```

--------------------------------

### OracleHook Initialization

Source: https://airflow.apache.org/docs/apache-airflow-providers-oracle/stable/_modules/airflow/providers/oracle/hooks/oracle.html

Details on how to initialize the OracleHook and the available configuration parameters for Oracle connectivity.

```APIDOC
## OracleHook Initialization

### Description
Initializes a new connection to an Oracle database using the specified connection ID and configuration settings.

### Method
Constructor

### Parameters
#### Request Body
- **oracle_conn_id** (string) - Required - The Airflow connection ID for Oracle credentials.
- **thick_mode** (boolean) - Optional - Whether to use python-oracledb in thick mode (requires Oracle Client libraries).
- **thick_mode_lib_dir** (string) - Optional - Path to Oracle Client libraries for thick mode.
- **thick_mode_config_dir** (string) - Optional - Path to Oracle configuration files for thick mode.
- **fetch_decimals** (boolean) - Optional - Whether to fetch numbers as decimal.Decimal.
- **fetch_lobs** (boolean) - Optional - Whether to fetch CLOBs/BLOBs as strings/bytes instead of locators.

### Request Example
{
  "oracle_conn_id": "my_oracle_db",
  "thick_mode": false,
  "fetch_decimals": true
}
```

--------------------------------

### Parse Connection URI

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html

Demonstrates how to initialize a Connection object from an existing URI string to extract credentials and parameters.

```python
from airflow.sdk import Connection
c = Connection(uri="my-conn-type://my-login:my-password@my-host:5432/my-schema?param1=val1&param2=val2")
print(c.login)
print(c.password)
```

--------------------------------

### DingdingHook - Task Callback Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-dingding/stable/operators.html

This example shows how to use `DingdingHook` within a task callback function (e.g., `on_failure_callback`) to send a notification when a task fails.

```APIDOC
## POST /api/v1/messages/dingtalk

### Description
Sends a notification message via DingTalk when a task fails, using a callback function and DingdingHook.

### Method
POST

### Endpoint
/api/v1/messages/dingtalk

### Parameters
#### Request Body (Implicitly handled by DingdingHook)
- **message_type** (string) - Set to "text" by default in the example.
- **message** (string) - Dynamically generated based on task context.
- **at_all** (boolean) - Set to `True` to notify all users.

### Request Example (within a Python task)
```python
def failure_callback(context):
    """
    The function that will be executed on failure.

    :param context: The context of the executed task.
    """
    message = f"The task {context['ti'].task_id} failed"
    DingdingHook(message_type="text", message=message, at_all=True).send()

# Example task definition:
# task_with_callback = BashOperator(
#     task_id='task_that_might_fail',
#     bash_command='exit 1',
#     on_failure_callback=failure_callback,
# )
```

### Response
#### Success Response (200)
- **status** (string) - Indicates the success status of the operation.

#### Response Example
```json
{
  "status": "success"
}
```
```

--------------------------------

### Connect to Database using pyodbc

Source: https://airflow.apache.org/docs/apache-airflow-providers-odbc/stable/operators.html

A Python snippet demonstrating how to establish a connection to a database using the pyodbc library with a connection string.

```python
import pyodbc

driver = "{ODBC Driver 17 for SQL Server}"
server = "localhost"
database = "testdb"
username = "user"
password = "password"

conn_str = (
    f"DRIVER={driver};" f"SERVER={server};" f"DATABASE={database};" f"UID={username};" f"PWD={password};"
)

conn = pyodbc.connect(conn_str)
```

--------------------------------

### Cassandra Sensors Example DAG

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-cassandra/stable/_modules/tests/system/apache/cassandra/example_cassandra_dag.html

An example Airflow DAG that utilizes CassandraTableSensor to check for table existence and CassandraRecordSensor to check for record existence in a Cassandra database.

```APIDOC
## Cassandra Sensors Example DAG

### Description
This DAG demonstrates how to use `CassandraTableSensor` to verify if a table exists and `CassandraRecordSensor` to check if a specific record exists in a Cassandra database. It's a practical example for data pipeline monitoring and validation.

### Method
N/A (This is a DAG definition, not an API endpoint)

### Endpoint
N/A

### Parameters
N/A

### Request Example
N/A

### Response
N/A

## CassandraTableSensor

### Description
Checks if a table exists in Cassandra.

### Method
N/A

### Endpoint
N/A

### Parameters
#### Path Parameters
N/A

#### Query Parameters
N/A

#### Request Body
- **table** (string) - Required - The name of the table to check (e.g., 'keyspace_name.table_name').

### Request Example
```json
{
  "table": "my_keyspace.my_table"
}
```

### Response
#### Success Response (200)
- **None** (Implicitly returns success if the table exists and the sensor succeeds).

#### Response Example
N/A

## CassandraRecordSensor

### Description
Checks if a specific record exists in a Cassandra table.

### Method
N/A

### Endpoint
N/A

### Parameters
#### Path Parameters
N/A

#### Query Parameters
N/A

#### Request Body
- **table** (string) - Required - The name of the table to check (e.g., 'keyspace_name.table_name').
- **keys** (dict) - Required - A dictionary representing the primary key of the record to check. Keys in the dictionary should match the column names of the primary key.

### Request Example
```json
{
  "table": "my_keyspace.my_table",
  "keys": {
    "partition_key_col": "value1",
    "clustering_key_col": "value2"
  }
}
```

### Response
#### Success Response (200)
- **None** (Implicitly returns success if the record exists and the sensor succeeds).

#### Response Example
N/A
```

--------------------------------

### MyItemTrigger and MyItemsOperator Example

Source: https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html

Example implementation of a deferrable operator (`MyItemsOperator`) that uses a custom trigger (`MyItemTrigger`) to process a list of items, deferring execution for each item.

```APIDOC
## Deferring Multiple Times Example

### Description
This example demonstrates how to create an Airflow operator that can defer execution multiple times, processing a list of items sequentially. The `MyItemsOperator` defers when it needs to process the next item in a list, and the `MyItemTrigger` handles the actual deferral and event yielding.

### Method
This is a conceptual example illustrating a pattern, not a direct API endpoint. The core logic involves the `defer` method within the operator's `execute` method.

### Endpoint
N/A (Illustrative Code Pattern)

### Parameters
N/A (Illustrative Code Pattern)

### Request Example
N/A (Illustrative Code Pattern)

### Response
N/A (Illustrative Code Pattern)

### Code Implementation

```python
import asyncio

from airflow.sdk import BaseOperator
from airflow.triggers.base import BaseTrigger, TriggerEvent


class MyItemTrigger(BaseTrigger):
    def __init__(self, item):
        super().__init__()
        self.item = item

    def serialize(self):
        return (self.__class__.__module__ + "." + self.__class__.__name__, {"item": self.item})

    async def run(self):
        result = None
        try:
            # Somehow process the item to calculate the result
            # Replace with actual processing logic
            await asyncio.sleep(1) # Simulate work
            result = f"Processed: {self.item}"
            yield TriggerEvent({"result": result})
        except Exception as e:
            yield TriggerEvent({"error": str(e)})


class MyItemsOperator(BaseOperator):
    def __init__(self, items, **kwargs):
        super().__init__(**kwargs)
        self.items = items

    def execute(self, context, current_item_index=0, event=None):
        last_result = None
        if event is not None:
            # execute method was deferred
            if "error" in event:
                raise Exception(event["error"])
            last_result = event["result"]
            current_item_index += 1

        try:
            current_item = self.items[current_item_index]
        except IndexError:
            # All items processed
            self.log.info("All items processed.")
            return last_result

        self.log.info(f"Processing item {current_item_index + 1}/{len(self.items)}: {current_item}")
        self.defer(
            trigger=MyItemTrigger(item=current_item),
            method_name="execute",  # The trigger will call this same method again
            kwargs={"current_item_index": current_item_index},
        )

```
```

--------------------------------

### Get Task Instance Dependencies (API)

Source: https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html

Retrieves the dependencies that are blocking a task from getting scheduled. This is useful for understanding task execution flow and potential bottlenecks.

```json
{
  "dependencies": [
    {
      "name": "string",
      "reason": "string"
    }
  ]
}
```

--------------------------------

### Build Custom Airflow Image with Build Arguments

Source: https://airflow.apache.org/docs/docker-stack/build.html

This script demonstrates how to build a custom Airflow Docker image by passing various build arguments. It includes adding extra Python dependencies, configuring custom apt repositories, and installing additional system packages.

```bash
export AIRFLOW_VERSION=2.2.4
export DOCKER_BUILDKIT=1

docker build . -f Dockerfile \
    --pull \
    --platform 'linux/amd64' \
    --build-arg PYTHON_BASE_IMAGE="python:3.9-slim-bookworm" \
    --build-arg AIRFLOW_VERSION="${AIRFLOW_VERSION}" \
    --build-arg ADDITIONAL_AIRFLOW_EXTRAS="slack,odbc" \
    --build-arg ADDITIONAL_PYTHON_DEPS=" \
        azure-storage-blob<12.9.0 \
        oauth2client \
        beautifulsoup4 \
        dateparser \
        rocketchat_API \
        typeform" \
    --build-arg ADDITIONAL_DEV_APT_COMMAND="curl https://packages.microsoft.com/keys/microsoft.asc | \
    apt-key add --no-tty - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list" \
    --build-arg ADDITIONAL_DEV_APT_ENV="ACCEPT_EULA=Y" \
    --build-arg ADDITIONAL_DEV_APT_DEPS="msodbcsql17 unixodbc-dev g++" \
    --build-arg ADDITIONAL_RUNTIME_APT_COMMAND="curl https://packages.microsoft.com/keys/microsoft.asc | \
    apt-key add --no-tty - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list" \
    --build-arg ADDITIONAL_RUNTIME_APT_ENV="ACCEPT_EULA=Y" \
    --build-arg ADDITIONAL_RUNTIME_APT_DEPS="msodbcsql17 unixodbc git procps vim" \
    --tag "my-custom-sources-image:0.0.1"
```

--------------------------------

### S3Hook Initialization and Properties

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/hooks/s3/index.html

Details on how to initialize the S3Hook and access its properties like resource and extra_args.

```APIDOC
## S3Hook Class

### Description
Interact with Amazon Simple Storage Service (S3). Provide thick wrapper around `boto3.client("s3")` and `boto3.resource("s3")`.

### Parameters
* **aws_conn_id** (str) - Airflow connection ID for AWS. Defaults to `AwsBaseHook.default_conn_name`.
* **transfer_config_args** (dict | None) - Configuration object for managed S3 transfers.
* **extra_args** (dict | None) - Extra arguments that may be passed to the download/upload operations.

### Properties
* **resource**: Returns the S3 resource object.
* **extra_args**: Returns hook's extra arguments (immutable).

### See Also
* https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#s3-transfers
  * For allowed upload extra arguments see `boto3.s3.transfer.S3Transfer.ALLOWED_UPLOAD_ARGS`.
  * For allowed download extra arguments see `boto3.s3.transfer.S3Transfer.ALLOWED_DOWNLOAD_ARGS`.
* `airflow.providers.amazon.aws.hooks.base_aws.AwsBaseHook`
```

--------------------------------

### Loading Scripts from Files via Template Extensions

Source: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html

Shows how to reference external script files in operators by using file extensions that match the 'template_ext' configuration.

```python
run_script = BashOperator(
    task_id="run_script",
    bash_command="script.sh",
)
```

--------------------------------

### Execute Integration Test Setup Function in Python

Source: https://airflow.apache.org/docs/apache-airflow-providers-edge3/stable/_api/airflow/providers/edge3/example_dags/integration_test/index.html

This Python code defines and executes the 'my_setup' function within the Airflow integration test DAG. This function is designed to encapsulate critical operations for integration testing purposes. It is intended to run without errors in standard Airflow environments.

```python
from airflow.providers.edge3.example_dags.integration_test import my_setup

# Example of how you might call the setup function within a DAG task
def run_integration_test():
    my_setup()

# In a real DAG, this would be part of a task definition:
# from airflow.operators.python import PythonOperator
# 
# task = PythonOperator(
#     task_id='run_my_setup_test',
#     python_callable=run_integration_test,
# )
```

--------------------------------

### Checking Airflow Logging Configuration

Source: https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/logging-tasks.html

Demonstrates how to use the `airflow info` command to inspect the current task logging handler and other relevant logging configurations. This is useful for troubleshooting and verifying that the logging setup is as expected.

```bash
$ airflow info

Apache Airflow
version                | 2.9.0.dev0
executor               | LocalExecutor
task_logging_handler   | airflow.utils.log.file_task_handler.FileTaskHandler
sql_alchemy_conn       | postgresql+psycopg2://postgres:airflow@postgres/airflow
dags_folder            | /files/dags
plugins_folder         | /root/airflow/plugins
base_log_folder        | /root/airflow/logs
remote_base_log_folder |

[skipping the remaining outputs for brevity]

```

--------------------------------

### Install Airbyte Airflow Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Command to install the Apache Airflow provider package for Airbyte integration. This enables Airflow to interact with Airbyte for data movement tasks.

```bash
pip install 'apache-airflow-providers-airbyte'
```

--------------------------------

### DatabricksSubmitRunOperator: Use Named Parameters

Source: https://airflow.apache.org/docs/apache-airflow-providers-databricks/stable/operators/submit_run.html

This example demonstrates initializing the DatabricksSubmitRunOperator using individual named parameters for clarity and direct configuration. It shows how to specify cluster settings, task details (like a JAR task), and libraries.

```python
    # Example of using the named parameters of DatabricksSubmitRunOperator
    # to initialize the operator.
    spark_jar_task = DatabricksSubmitRunOperator(
        task_id="spark_jar_task",
        new_cluster=new_cluster,
        spark_jar_task={"main_class_name": "com.example.ProcessData"},
        libraries=[{"jar": "dbfs:/lib/etl-0.1.jar"}],
    )
```

--------------------------------

### Download and Verify Airflow Provider Package (Bash)

Source: https://airflow.apache.org/docs/apache-airflow-providers-redis/stable/installing-providers-from-sources.html

This script downloads a specific version of an Apache Airflow provider package from PyPI, along with its ASC signature and SHA512 checksum files. It uses `pip download` to get the package and `curl` to fetch the signature and checksum. The script then prints the location of the downloaded files for manual verification.

```bash
#!/bin/bash
PACKAGE_VERSION=4.4.3
PACKAGE_NAME=apache-airflow-providers-redis
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_redis-4.4.3-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_redis-4.4.3-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_redis-4.4.3-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_redis-4.4.3-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### Add apt packages to Airflow Docker image

Source: https://airflow.apache.org/docs/helm-chart/stable/quick-start.html

Demonstrates how to create a custom Dockerfile based on the official Airflow image to install system packages like 'vim'. It includes steps to build the image, load it into a kind cluster, and update a Helm deployment.

```Dockerfile
FROM apache/airflow
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
```

```bash
docker build --pull --tag my-image:0.0.1 .
kind load docker-image my-image:0.0.1
helm upgrade $RELEASE_NAME apache-airflow/airflow --namespace $NAMESPACE \
  --set images.airflow.repository=my-image \
  --set images.airflow.tag=0.0.1
```

--------------------------------

### Initialize Airflow Configuration

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

Runs the airflow-cli to generate default configuration files in the local config directory.

```bash
docker compose run airflow-cli airflow config list
```

--------------------------------

### System Test: Azure ADLS Delete Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/_api/tests/system/microsoft/azure/example_adls_delete/index.html

This section details the attributes and module contents for the Azure ADLS delete system test example in Apache Airflow.

```APIDOC
## tests.system.microsoft.azure.example_adls_delete

### Description
This module contains an example system test for deleting files from Azure Data Lake Storage (ADLS) using Apache Airflow.

### Attributes

- **LOCAL_FILE_PATH** (string) - The local path of the file to be uploaded.
- **REMOTE_FILE_PATH** (string) - The remote path in ADLS where the file will be stored.
- **ENV_ID** (string) - The environment ID for the test.
- **DAG_ID** (string) - The ID of the DAG used in the test.

### Module Contents

- **`LOCAL_FILE_PATH`**: Defines the local file path for the test.
- **`REMOTE_FILE_PATH`**: Defines the remote file path in ADLS.
- **`ENV_ID`**: Specifies the environment identifier.
- **`DAG_ID`**: The unique identifier for the DAG.
- **`upload_file`**: A function or task related to uploading a file.
- **`test_run`**: A function or task representing the execution of the test run.
```

--------------------------------

### Analyze Cloud Data with DuckDB

Source: https://airflow.apache.org/docs/apache-airflow/stable/tutorial/objectstorage.html

Demonstrates how to register an ObjectStoragePath filesystem with DuckDB to query Parquet files stored in the cloud using SQL.

```python
@task
def analyze(path: ObjectStoragePath):
    import duckdb
    conn = duckdb.connect(database=":memory:")
    conn.register_filesystem(path.fs)
    s3_path = path.path
    conn.execute(f"CREATE OR REPLACE TABLE airquality_urban AS SELECT * FROM read_parquet('{path.protocol}://{s3_path}')")
    df2 = conn.execute("SELECT * FROM airquality_urban").fetchdf()
    print(df2.head())
```

--------------------------------

### Download and Verify Airflow Provider Packages (Bash)

Source: https://airflow.apache.org/docs/apache-airflow-providers-dingding/stable/installing-providers-from-sources.html

This bash script downloads a specified Airflow provider package version from PyPI, along with its ASC signature and SHA512 sum files. It then displays the downloaded files in a temporary directory for manual verification. Dependencies include bash, pip, and curl.

```bash
#!/bin/bash
PACKAGE_VERSION=3.9.3
PACKAGE_NAME=apache-airflow-providers-dingding
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_dingding-3.9.3-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_dingding-3.9.3-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_dingding-3.9.3-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_dingding-3.9.3-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### Start Kueue Job Operator

Source: https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/_modules/tests/system/cncf/kubernetes/example_kubernetes_kueue.html

Starts a Kueue job on Kubernetes using the KubernetesStartKueueJobOperator. This operator submits a job to a specified Kueue queue with defined resource requirements.

```python
start_kueue_job = KubernetesStartKueueJobOperator(
    task_id="kueue_job",
    queue_name=QUEUE_NAME,
    namespace="default",
    image="perl:5.34.0",
    cmds=["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"],
    name="test-pi",
    suspend=True,
    container_resources=k8s.V1ResourceRequirements(
        requests={
            "cpu": 1,
            "memory": "200Mi",
        },
    ),
    wait_until_job_complete=True,
)
```

--------------------------------

### GET /sql/instances/{instance}/databases

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/links/cloud_sql/index.html

Retrieves the link to the Google Cloud SQL Instance databases management page.

```APIDOC
## GET /sql/instances/{instance}/databases

### Description
Constructs a URL to the databases management page for a specific Google Cloud SQL instance.

### Method
GET

### Endpoint
/sql/instances/{instance}/databases?project={project_id}

### Parameters
#### Path Parameters
- **instance** (string) - Required - The ID of the Cloud SQL instance.

#### Query Parameters
- **project_id** (string) - Required - The Google Cloud project ID.

### Response
#### Success Response (200)
- **url** (string) - The generated URL to the Cloud SQL instance databases page.
```

--------------------------------

### Configure External React App Hosting

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/custom-view-plugin.html

Shows how to register a React application that is hosted on an external CDN or infrastructure by providing the bundle URL directly in the react_apps configuration.

```python
react_apps = [
    {
        "name": "My External App",
        "url_route": "my-external-app",
        "bundle_url": "https://my-cdn.com/main.umd.cjs",
        "destination": "nav",
    }
]
```

--------------------------------

### Install SSH Provider with Common Compat Extra

Source: https://airflow.apache.org/docs/apache-airflow-providers-ssh/index.html

Installs the SSH provider package along with the 'common.compat' extra dependencies. This is useful for ensuring compatibility with other Airflow provider packages.

```bash
pip install apache-airflow-providers-ssh[common.compat]
```

--------------------------------

### Install Kubernetes Provider for Airflow

Source: https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/index.html

This command installs the apache-airflow-providers-cncf-kubernetes package, which is necessary for integrating Airflow with Kubernetes. It ensures compatibility with the specified Airflow version and includes essential dependencies.

```bash
pip install apache-airflow-providers-cncf-kubernetes
```

--------------------------------

### Download and Verify Provider Package (Bash)

Source: https://airflow.apache.org/docs/apache-airflow-providers-sqlite/stable/installing-providers-from-sources.html

This bash script downloads a specified Apache Airflow provider package version from PyPI, along with its signature and SHA512 sum files. It saves these files to a temporary directory and lists them for manual verification. Dependencies include bash, pip, and curl.

```bash
#!/bin/bash
PACKAGE_VERSION=4.3.1
PACKAGE_NAME=apache-airflow-providers-sqlite
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_sqlite-4.3.1-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_sqlite-4.3.1-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_sqlite-4.3.1-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_sqlite-4.3.1-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### Download and Verify Provider Packages (Bash)

Source: https://airflow.apache.org/docs/apache-airflow-providers-keycloak/stable/installing-providers-from-sources.html

This bash script downloads a specified Apache Airflow provider package version from PyPI, along with its detached signature (.asc) and SHA512 checksum files. It saves these files to a temporary directory and then lists them for manual verification. The script uses 'pip download' for the package and 'curl' for the signature and checksum files.

```bash
#!/bin/bash
PACKAGE_VERSION=0.7.0
PACKAGE_NAME=apache-airflow-providers-keycloak
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_keycloak-0.7.0-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_keycloak-0.7.0-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_keycloak-0.7.0-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_keycloak-0.7.0-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### GitHook Environment Setup - Python

Source: https://airflow.apache.org/docs/apache-airflow-providers-git/stable/_api/airflow/providers/git/hooks/git/index.html

Provides methods for setting up the environment for Git operations, such as configuring SSH environment variables. This is crucial for enabling secure and proper communication with Git repositories.

```python
class GitHook(BaseHook):
    # ... other methods and attributes ...

    def set_git_env(self, key=None):
        """Set git environment variables."""
        # Implementation details for setting environment variables
        pass

    def configure_hook_env(self):
        """Configure the hook's environment."""
        # Implementation details for configuring the hook environment
        pass

```

--------------------------------

### Install Apache Airflow Redis Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

This code snippet provides the command to install the Apache Airflow provider for Redis. It facilitates the use of Redis within Airflow workflows.

```bash
pip install 'apache-airflow-providers-redis'
```

--------------------------------

### SQLite Connection Configuration

Source: https://airflow.apache.org/docs/apache-airflow-providers-sqlite/stable/connections/sqlite.html

This section provides examples of how to configure the SQLite connection using environment variables, either through a URI format or a JSON format.

```APIDOC
## SQLite Connection Configuration

### URI Format Example

**Using a relative path:**
```bash
export AIRFLOW_CONN_SQLITE_DEFAULT='sqlite://relative/path/to/db?mode=ro'
```

**Using an absolute path:**
```bash
export AIRFLOW_CONN_SQLITE_DEFAULT='sqlite:///absolute/path/to/db?mode=ro'
```

**Using an in-memory database:**
```bash
export AIRFLOW_CONN_SQLITE_DEFAULT='sqlite://?mode=ro'
```

*Note: Ensure all components of the URI are URL-encoded.*

### JSON Format Example

```bash
export AIRFLOW_CONN_SQLITE_DEFAULT='{
    "conn_type": "sqlite",
    "host": "relative/path/to/db",
    "extra": {
        "mode": "ro"
    }
}'
```

### Parameters

- **Host** (string) - Optional - The host to connect to. Can be a file path or an in-memory database. Defaults to an in-memory database if not set.
- **Extra** (JSON object) - Optional - Specify extra parameters like `mode` (e.g., `ro` for read-only) as a JSON dictionary.
```

--------------------------------

### Configure GIT Connection with Bastion Host and Custom Port

Source: https://airflow.apache.org/docs/apache-airflow-providers-git/stable/connections/git.html

This JSON configuration illustrates setting up a GIT connection through a bastion host using SSH. It includes the path to the SSH key, proxy command, custom SSH port, strict host key checking, and a custom known_hosts file.

```json
{
    "key_file": "/path/to/id_rsa",
    "host_proxy_cmd": "ssh -W %h:%p bastion.example.com",
    "ssh_port": "2222",
    "strict_host_key_checking": "yes",
    "known_hosts_file": "/path/to/known_hosts"
}
```

--------------------------------

### Install Apache Airflow Git Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the apache-airflow-providers-git package, providing integration with the Git distributed version control system. This is useful for managing code repositories and deployments.

```bash
pip install 'apache-airflow-providers-git'
```

--------------------------------

### Qdrant Example DAG Vectors

Source: https://airflow.apache.org/docs/apache-airflow-providers-qdrant/stable/_api/tests/system/qdrant/example_dag_qdrant/index.html

Defines a list of vectors used in the Qdrant example DAG for system tests. These vectors are typically used for similarity search or other Qdrant operations.

```python
vectors = [[0.732, 0.611, 0.289, 0.421], [0.217, 0.526, 0.416, 0.981], [0.326, 0.483, 0.376, 0.136]]
```

--------------------------------

### Download and Verify Airflow Provider Package (Bash)

Source: https://airflow.apache.org/docs/apache-airflow-providers-yandex/stable/installing-providers-from-sources.html

This bash script downloads a specified Airflow provider package version from PyPI, along with its ASC signature and SHA512 checksum files. It then displays the downloaded files in a temporary directory for manual verification. Dependencies include bash, pip, and curl.

```bash
#!/bin/bash
PACKAGE_VERSION=4.4.1
PACKAGE_NAME=apache-airflow-providers-yandex
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_yandex-4.4.1-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_yandex-4.4.1-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_yandex-4.4.1-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_yandex-4.4.1-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### Execute Hive Command with QuboleOperator

Source: https://airflow.apache.org/docs/apache-airflow-providers-qubole/stable/operators/qubole.html

Demonstrates running a Hive query to show all tables using QuboleOperator. It supports fetching logs and attaching tags to the Qubole command. Dependencies include the Qubole provider for Airflow.

```python
hive_show_table = QuboleOperator(
    task_id="hive_show_table",
    command_type="hivecmd",
    query="show tables",
    cluster_label="{{ params.cluster_label }}",
    fetch_logs=True,
    # If `fetch_logs`=true, will fetch qubole command logs and concatenate
    # them into corresponding airflow task logs
    tags="airflow_example_run",
    # To attach tags to qubole command, auto attach 3 tags - dag_id, task_id, run_id
    params={
        "cluster_label": "default",
    },
)
```

--------------------------------

### Module: airflow.providers.standard.example_dags.example_python_decorator

Source: https://airflow.apache.org/docs/apache-airflow-providers-standard/stable/_api/airflow/providers/standard/example_dags/example_python_decorator/index.html

Details the attributes and functions available in the Python decorator example module for Apache Airflow.

```APIDOC
## Module: airflow.providers.standard.example_dags.example_python_decorator

### Description
This module provides an example DAG demonstrating the usage of the TaskFlow API to execute Python functions natively and within a virtual environment.

### Attributes
- **log** (object) - Logger instance for the module.
- **PATH_TO_PYTHON_BINARY** (string) - The path to the Python binary used for execution (default: '/usr/local/bin/python3').
- **example_dag** (DAG) - The example DAG object instance.

### Functions
#### example_python_decorator()
- **Description**: A function that demonstrates the implementation of the TaskFlow API decorator.
- **Returns**: None
```

--------------------------------

### Example Kubernetes Secret for Connection

Source: https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/_api/airflow/providers/cncf/kubernetes/secrets/kubernetes_secrets_backend/index.html

This YAML defines an example Kubernetes Secret resource. It demonstrates the required metadata labels and the data structure for storing a connection, variable, or configuration.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: anything
  labels:
    airflow.apache.org/connection-id: my_db
data:
  value: <base64-encoded-connection-uri>

```

--------------------------------

### Import Release Keys for Verification

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-flink/stable/installing-providers-from-sources.html

Commands to import the official Apache release keys required for verifying package signatures. These commands use GPG or PGP utilities to add the keys to your local keyring.

```bash
gpg -i KEYS
pgpk -a KEYS
pgp -ka KEYS
```

--------------------------------

### Using `parameters` attribute

Source: https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/operators.html

Demonstrates how to use the `parameters` attribute to pass dynamic values directly into SQL statements.

```APIDOC
## Using `parameters` attribute

### Description
This example shows how to use the `parameters` attribute of the `SQLExecuteQueryOperator` to inject values into a SQL query.

### Method
N/A (This is a configuration example for an operator)

### Endpoint
N/A

### Parameters
#### Request Body
- **task_id** (string) - Required - The unique identifier for the task.
- **conn_id** (string) - Required - The Airflow connection ID for the database.
- **sql** (string) - Required - The SQL query to execute.
- **parameters** (object) - Required - A dictionary of parameters to be substituted into the SQL query.

### Request Example
```python
get_birth_date = SQLExecuteQueryOperator(
    task_id="get_birth_date",
    conn_id="postgres_default",
    sql="SELECT * FROM pet WHERE birth_date BETWEEN SYMMETRIC %(begin_date)s AND %(end_date)s",
    parameters={"begin_date": "2020-01-01", "end_date": "2020-12-31"},
)
```

### Response
#### Success Response (200)
N/A (This is an operator configuration, not an API endpoint)

#### Response Example
N/A
```

--------------------------------

### BeamRunJavaPipelineOperator Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-beam/stable/_modules/tests/system/apache/beam/example_java_dataflow.html

This example demonstrates how to use the BeamRunJavaPipelineOperator to run a Java pipeline on Google Cloud Dataflow. It includes downloading the pipeline JAR from GCS and configuring pipeline options.

```APIDOC
## POST /example_beam_native_java_dataflow_runner

### Description
This endpoint demonstrates running a Java pipeline using the `BeamRunJavaPipelineOperator` with `DataflowRunner`. It first downloads the necessary JAR file from Google Cloud Storage to the local filesystem and then executes the pipeline with specified options.

### Method
POST

### Endpoint
`/example_beam_native_java_dataflow_runner`

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
This endpoint does not directly accept a request body. The configuration is handled within the Airflow DAG.

### Request Example
```json
{
  "message": "This is an example DAG, not a direct API endpoint. Configuration is within the DAG file."
}
```

### Response
#### Success Response (200)
- **message** (string) - Indicates the DAG has been triggered or processed.

#### Response Example
```json
{
  "status": "success",
  "message": "DAG run initiated successfully."
}
```

## How to use BeamRunJavaPipelineOperator

### Description
This section details the usage of the `BeamRunJavaPipelineOperator` to execute a Java pipeline, with a specific example for `DataflowRunner`.

### Method
N/A (This is a Python operator within an Airflow DAG)

### Endpoint
N/A

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
N/A

### Request Example
```python
# Example within an Airflow DAG
from airflow import models
from airflow.providers.apache.beam.operators.beam import BeamRunJavaPipelineOperator
from airflow.providers.google.cloud.transfers.gcs_to_local import GCSToLocalFilesystemOperator

with models.DAG(
    "example_beam_native_java_dataflow_runner",
    schedule=None,
    start_date=START_DATE,
    catchup=False,
    tags=["example"],
) as dag:
    jar_to_local_dataflow_runner = GCSToLocalFilesystemOperator(
        task_id="jar_to_local_dataflow_runner",
        bucket=GCS_JAR_DATAFLOW_RUNNER_BUCKET_NAME,
        object_name=GCS_JAR_DATAFLOW_RUNNER_OBJECT_NAME,
        filename="/tmp/beam_wordcount_dataflow_runner_{{ ds_nodash }}.jar",
    )

    start_java_pipeline_dataflow = BeamRunJavaPipelineOperator(
        task_id="start_java_pipeline_dataflow",
        runner="DataflowRunner",
        jar="/tmp/beam_wordcount_dataflow_runner_{{ ds_nodash }}.jar",
        pipeline_options={
            "tempLocation": GCS_TMP,
            "stagingLocation": GCS_STAGING,
            "output": GCS_OUTPUT,
        },
        job_class="org.apache.beam.examples.WordCount",
        dataflow_config={
            "job_name": "{{task.task_id}}",
            "location": "us-central1",
        },
    )

    jar_to_local_dataflow_runner >> start_java_pipeline_dataflow
```

### Response
#### Success Response (200)
- **status** (string) - Indicates the success of the task execution.
- **message** (string) - Provides details about the completed task.

#### Response Example
```json
{
  "status": "success",
  "message": "Beam Java pipeline 'start_java_pipeline_dataflow' completed successfully."
}
```
```

--------------------------------

### Initialize and Use GremlinHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-tinkerpop/stable/_api/airflow/providers/apache/tinkerpop/hooks/gremlin/index.html

Demonstrates how to instantiate the GremlinHook and execute a query against a Graph Database. This requires a configured connection ID in Airflow.

```python
from airflow.providers.apache.tinkerpop.hooks.gremlin import GremlinHook

# Initialize the hook with a connection ID
hook = GremlinHook(gremlin_conn_id='my_gremlin_conn')

# Execute a Gremlin query
results = hook.run(query='g.V().limit(10)')
print(results)
```

--------------------------------

### Instantiate ObjectStoragePath for S3

Source: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/objectstorage.html

Demonstrates how to create an ObjectStoragePath object pointing to an S3 bucket using a URI. It shows both direct URI specification and using a connection ID.

```python
from airflow.sdk import ObjectStoragePath

base = ObjectStoragePath("s3://aws_default@my-bucket/")
```

```python
# Equivalent to the previous example.
base = ObjectStoragePath("s3://my-bucket/", conn_id="aws_default")
```

--------------------------------

### Install Apache Flink Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-flink/stable/index.html

Command to install the Apache Flink provider package for Airflow using pip. This is the standard method for adding Flink support to an existing Airflow environment.

```bash
pip install apache-airflow-providers-apache-flink
```

--------------------------------

### GitDagBundle Initialization and Configuration

Source: https://airflow.apache.org/docs/apache-airflow-providers-git/stable/_api/airflow/providers/git/bundles/git/index.html

Details on how to configure and initialize a GitDagBundle for managing DAGs from a remote repository.

```APIDOC
## GitDagBundle Configuration

### Description
Initializes a new GitDagBundle instance to manage DAG files from a Git repository.

### Parameters
#### Constructor Parameters
- **tracking_ref** (str) - Required - Branch or tag for this DAG bundle.
- **subdir** (str) - Optional - Subdirectory within the repository where the DAGs are stored.
- **git_conn_id** (str) - Optional - Connection ID for SSH/token based connection.
- **repo_url** (str) - Optional - Explicit Git repository URL.
- **submodules** (bool) - Optional - Whether to initialize git submodules.
- **prune_dotgit_folder** (bool) - Optional - Whether to remove the .git folder after cloning to save space.

### Methods
- **initialize()**: Prepares the bundle for use by the DAG processor.
- **refresh()**: Updates the local bundle files to the latest version.
- **get_current_version()**: Returns the current version identifier of the bundle.
- **view_url_template()**: Returns a URL template for viewing the bundle in an external UI.
```

--------------------------------

### Install Apache Airflow Presto Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

This code snippet provides the command to install the Apache Airflow provider for Presto. It is used to connect and manage Presto clusters within Airflow.

```bash
pip install 'apache-airflow-providers-presto'
```

--------------------------------

### Install Apache Airflow Papermill Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

This snippet shows how to install the Apache Airflow provider for Papermill using pip. It is a common task for integrating Papermill notebooks with Airflow workflows.

```bash
pip install 'apache-airflow-providers-papermill'
```

--------------------------------

### POST /buckets

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/hooks/gcs/index.html

Creates a new Google Cloud Storage bucket with specified configurations.

```APIDOC
## POST /buckets

### Description
Creates a new bucket in Google Cloud Storage with optional storage class, location, and labels.

### Method
POST

### Parameters
#### Request Body
- **bucket_name** (str) - Required - The name of the bucket.
- **resource** (dict) - Optional - Parameters for creating the bucket.
- **storage_class** (str) - Optional - Storage class (MULTI_REGIONAL, REGIONAL, STANDARD, NEARLINE, COLDLINE).
- **location** (str) - Optional - The location of the bucket.
- **project_id** (str) - Required - The ID of the Google Cloud Project.
- **labels** (dict) - Optional - User-provided labels.

### Response
#### Success Response (200)
- **id** (str) - The ID of the created bucket.
```

--------------------------------

### Install Apache Airflow Facebook Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the apache-airflow-providers-facebook package, enabling Airflow to interact with Facebook Ads API. This provider is useful for data extraction and campaign management tasks.

```bash
pip install 'apache-airflow-providers-facebook'
```

--------------------------------

### Verify PyPI Provider Package Download (Bash)

Source: https://airflow.apache.org/docs/apache-airflow-providers-elasticsearch/stable/installing-providers-from-sources.html

This bash script downloads a specified Apache Airflow provider package from PyPI, along with its signature and SHA sum files. It then displays the downloaded files in a temporary directory for manual verification. Dependencies include 'pip' and 'curl'.

```bash
#!/bin/bash
PACKAGE_VERSION=6.5.1
PACKAGE_NAME=apache-airflow-providers-elasticsearch
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_elasticsearch-6.5.1-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_elasticsearch-6.5.1-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_elasticsearch-6.5.1-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_elasticsearch-6.5.1-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### Install Apache Airflow Providers

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Commands to install specific Apache provider packages for Airflow using pip. These packages enable integration between Airflow and various Apache ecosystem tools.

```bash
pip install 'apache-airflow-providers-apache-iceberg'
pip install 'apache-airflow-providers-apache-impala'
pip install 'apache-airflow-providers-apache-kafka'
pip install 'apache-airflow-providers-apache-kylin'
pip install 'apache-airflow-providers-apache-livy'
pip install 'apache-airflow-providers-apache-pig'
pip install 'apache-airflow-providers-apache-pinot'
pip install 'apache-airflow-providers-apache-spark'
pip install 'apache-airflow-providers-apache-tinkerpop'
```

--------------------------------

### Airflow Task Nesting Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-openlineage/stable/_api/tests/system/openlineage/example_openlineage_base_complex_dag/index.html

This example demonstrates a scenario where a BashOperator is executed within a decorated task function. It highlights the potential for nested operator usage, which is controlled by the 'allow_nested_operators' parameter.

```python
@task(provide_context=True)
def say_hello_world(**context):
    hello_world_task = BashOperator(
        task_id="hello_world_task",
        bash_command="python -c \"print('Hello, world!')\"",
        dag=dag,
    )
    hello_world_task.execute(context)
```

--------------------------------

### Configure Container Lifecycle Hooks (YAML)

Source: https://airflow.apache.org/docs/helm-chart/stable/parameters-ref.html

Defines container lifecycle hooks such as postStart and preStop commands. These hooks allow for executing scripts or commands when a container starts or stops, useful for initialization or cleanup tasks. This configuration can be applied globally or to specific components like apiServer, cleanup, createUserJob, dagProcessor, and dags.gitSync.

```yaml
containerLifecycleHooks:
  postStart:
    exec:
      command:
      - /bin/sh
      - -c
      - echo postStart handler > /usr/share/message
  preStop:
    exec:
      command:
      - /bin/sh
      - -c
      - echo preStop handler > /usr/share/message
```

--------------------------------

### Taskflow API Docker Virtualenv Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-docker/stable/decorators/docker.html

An example demonstrating the usage of the `@task.docker` decorator for defining a Dockerized task within the Taskflow API, including type hints for input and output.

```APIDOC
## @task.docker Usage Example

### Description
This example shows how to define a Dockerized task using the `@task.docker` decorator in Airflow's Taskflow API. The task processes a dictionary of order data and calculates the total order value.

### Method
Decorator

### Endpoint
N/A (This is a decorator usage)

### Parameters

#### Request Body (Implicit via decorator arguments)
- **image** (string) - Required - The Docker image to use for the task (e.g., "python:3.9-slim-bookworm").
- **multiple_outputs** (boolean) - Optional - If True, allows the task to return multiple outputs.

#### Task Function Parameters
- **order_data_dict** (dict) - Required - A dictionary containing order data.

### Request Example (Decorator)
```python
@task.docker(image="python:3.9-slim-bookworm", multiple_outputs=True)
def transform(order_data_dict: dict):
    """
    #### Transform task
    A simple Transform task which takes in the collection of order data and
    computes the total order value.
    """
    # Task logic here
```

### Response (Task Output)
#### Success Response (Task Completion)
- **total_order_value** (integer) - The computed total value of all orders.

#### Response Example (Return Value)
```json
{
  "total_order_value": 1500
}
```
```

--------------------------------

### Start Airflow DAG Processor

Source: https://airflow.apache.org/docs/stable/start.html

Starts the Airflow DAG processor, which is responsible for parsing DAG files and making them available to the scheduler. This component ensures that Airflow is aware of all your defined DAGs.

```bash
airflow dag-processor
```

--------------------------------

### Execute BTEQ Files with Encoding Options

Source: https://airflow.apache.org/docs/apache-airflow-providers-teradata/stable/operators/bteq.html

Demonstrates how to execute external .bteq files using the BteqOperator while specifying different script and session encodings like UTF8, UTF16, and ASCII.

```python
execute_bteq_utf8_session_utf16_file = BteqOperator(
    task_id="execute_bteq_utf8_session_utf16_file",
    file_path="providers/teradata/tests/system/teradata/script.bteq",
    params=params,
    bteq_script_encoding="UTF8",
    bteq_session_encoding="UTF16"
)
```

--------------------------------

### Install Apache Airflow Pinecone Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

This code snippet provides the command to install the Apache Airflow provider for Pinecone. This allows for seamless integration of Pinecone services within Airflow pipelines.

```bash
pip install 'apache-airflow-providers-pinecone'
```

--------------------------------

### POST /instances/import

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/operators/cloud_sql/index.html

Imports data into a Cloud SQL instance using the CloudSQLImportInstanceOperator.

```APIDOC
## POST /instances/import

### Description
Imports data from a storage bucket into a Cloud SQL instance. This operator is idempotent if the SQL file was exported by Cloud SQL.

### Method
POST

### Endpoint
/instances/{instance}/import

### Parameters
#### Path Parameters
- **instance** (string) - Required - Cloud SQL instance ID.

#### Request Body
- **importContext** (object) - Required - The request body as defined in the Google Cloud SQL Admin API.

### Request Example
{
  "importContext": {
    "uri": "gs://my-bucket/backup.sql",
    "database": "my_db"
  }
}

### Response
#### Success Response (200)
- **operation** (string) - The ID of the operation created for the import task.

#### Response Example
{
  "operation": "operation-12345"
}
```

--------------------------------

### Install Apache Airflow GitHub Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the apache-airflow-providers-github package, enabling Apache Airflow to interact with the GitHub platform. This provider is useful for managing GitHub repositories, issues, and pull requests.

```bash
pip install 'apache-airflow-providers-github'
```

--------------------------------

### Configure Airflow Policy Entrypoint

Source: https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/cluster-policies.html

Demonstrates how to register a policy module as an entrypoint in pyproject.toml. This enables the policy to be discovered and executed by Airflow components.

```toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-airflow-plugin"
version = "0.0.1"

dependencies = ["apache-airflow>=2.6"]
[project.entry-points.'airflow.policy']
_ = 'my_airflow_plugin.policies'
```

--------------------------------

### Navigate Object Storage Directory Tree

Source: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/objectstorage.html

Shows how to construct new paths within an object storage hierarchy by appending directory names to an existing base path. This mimics local filesystem directory traversal.

```python
from airflow.sdk import ObjectStoragePath

base = ObjectStoragePath("s3://my-bucket/")
subdir = base / "subdir"

# prints ObjectStoragePath("s3://my-bucket/subdir")
print(subdir)
```

--------------------------------

### Define DAG ID for Docker Copy Data Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-docker/stable/_api/tests/system/docker/example_docker_copy_data/index.html

This snippet defines the DAG ID for the Docker copy data example. It's a constant string used to identify the Airflow DAG.

```python
DAG_ID = 'docker_sample_copy_data'
```

--------------------------------

### Asynchronous VM Management

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/_api/airflow/providers/microsoft/azure/hooks/compute/index.html

Shows how to use the asynchronous capabilities of the AzureComputeHook to check the power state of a VM.

```python
import asyncio
from airflow.providers.microsoft.azure.hooks.compute import AzureComputeHook

async def check_vm():
    async with AzureComputeHook(azure_conn_id='my_azure_conn') as hook:
        state = await hook.async_get_power_state(resource_group_name='my_rg', vm_name='my_vm')
        print(f'Async VM state: {state}')

asyncio.run(check_vm())
```

--------------------------------

### Example Generic SQL Transfer Test Run

Source: https://airflow.apache.org/docs/apache-airflow-providers-common-sql/stable/_api/tests/system/common/sql/example_generic_transfer/index.html

Represents the test run execution for the example generic SQL transfer system test. This is a placeholder indicating the test's execution point.

```python
test_run = {}

```

--------------------------------

### Passing Server Configuration Options (Python)

Source: https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/operators.html

Demonstrates passing server configuration options, such as `statement_timeout`, to the database connection via the `hook_params` attribute in SQLExecuteQueryOperator. This allows for fine-grained control over connection parameters.

```python
get_birth_date = SQLExecuteQueryOperator(
    task_id="get_birth_date",
    sql="SELECT * FROM pet WHERE birth_date BETWEEN SYMMETRIC %(begin_date)s AND %(end_date)s",
    parameters={"begin_date": "2020-01-01", "end_date": "2020-12-31"},
    hook_params={"options": "-c statement_timeout=3000ms"},
)
```

--------------------------------

### Example Generic SQL Transfer Connection Arguments

Source: https://airflow.apache.org/docs/apache-airflow-providers-common-sql/stable/_api/tests/system/common/sql/example_generic_transfer/index.html

Defines the connection arguments used in the example generic SQL transfer system test. This is typically a Python variable holding connection details.

```python
connection_args = {}

```

--------------------------------

### Verify PyPI Provider Package Download Script (Bash)

Source: https://airflow.apache.org/docs/apache-airflow-providers-common-compat/stable/installing-providers-from-sources.html

This bash script downloads a specified Apache Airflow provider package version from PyPI, along with its ASC signature and SHA512 sum files from Apache's download servers. It saves these files to a temporary directory and lists them for verification. Dependencies include 'bash', 'pip', and 'curl'.

```bash
#!/bin/bash
PACKAGE_VERSION=1.14.2
PACKAGE_NAME=apache-airflow-providers-common-compat
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_common_compat-1.14.2-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_common_compat-1.14.2-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_common_compat-1.14.2-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_common_compat-1.14.2-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### Custom DAG discovery function example

Source: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html

Provides an example of a custom callable function 'might_contain_dag' that can be used to control which Python files Airflow parses for DAGs, offering more flexibility than the default heuristic.

```python
import zipfile

def might_contain_dag(file_path: str, zip_file: zipfile.ZipFile | None = None) -> bool:
    # Your logic to check if there are Dags defined in the file_path
    # Return True if the file_path needs to be parsed, otherwise False
    pass

```

--------------------------------

### Airflow CLI: List Assets

Source: https://airflow.apache.org/docs/apache-airflow-ctl/stable/cli-and-env-variables-ref.html

Lists all available assets. Requires an API token for authentication and allows specifying the environment and output format.

```bash
airflowctl assets list [-h] [--api-token API_TOKEN] [-e ENV] [--output (table, json, yaml, plain)]
```

--------------------------------

### Dynamic Configuration via Commands and Secrets

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/set-config.html

Derive configuration values at runtime by appending _cmd to execute shell commands or _secret to retrieve values from configured secret backends like Hashicorp Vault.

```ini
[database]
sql_alchemy_conn_cmd = bash_command_to_run
sql_alchemy_conn_secret = sql_alchemy_conn
```

```bash
export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN_CMD=bash_command_to_run
export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN_SECRET=sql_alchemy_conn
```

--------------------------------

### OSSRemoteLogIO: Upload and Read Logs to/from OSS

Source: https://airflow.apache.org/docs/apache-airflow-providers-alibaba/stable/_api/airflow/providers/alibaba/cloud/log/oss_task_handler/index.html

The OSSRemoteLogIO class provides methods to upload log files to Alibaba Cloud OSS, read logs from OSS, and check for the existence of log files in remote storage. It supports appending to existing logs or overwriting them.

```python
class OSSRemoteLogIO(LoggingMixin):
    """Convenience super-class to have a logger configured with the class name."""
    base_log_folder: pathlib.Path
    remote_base: str = ''
    delete_local_copy: bool = True
    processors = ()

    def upload(self, path: str, ti) -> None:
        """Upload the given log path to the remote storage."""
        ...

    @property
    def base_folder(self) -> str:
        ...

    @property
    def bucket_name(self) -> str:
        ...

    @property
    def hook(self) -> OSSHook:
        ...

    def read(self, relative_path: str, ti) -> str:
        """Read the log from remote storage.

        :param relative_path: log relative path
        :param ti: task instance object
        :return: log string
        """
        ...

    def oss_log_exists(self, remote_log_location: str) -> bool:
        """Check if remote_log_location exists in remote storage.

        Parameters:
            remote_log_location – log’s location in remote storage
        Returns:
            True if location exists else False
        """
        ...

    def oss_read(self, remote_log_location: str, return_error: bool = False) -> str:
        """Return the log at the remote_log_location or ‘’ if no logs are found or there is an error.

        Parameters:
            remote_log_location – the log’s location in remote storage
            return_error – if True, returns a string error message if an error occurs. Otherwise, returns ‘’ when an error occurs.
        """
        ...

    def oss_write(self, log: str, remote_log_location: str, append: bool = True) -> bool:
        """Write the log to remote_log_location and return True; fails silently and returns False on error.

        Parameters:
            log – the log to write to the remote_log_location
            remote_log_location – the log’s location in remote storage
            append – if False, any existing log file is overwritten. If True, the new log is appended to any existing logs.
        Returns:
            whether the log is successfully written to remote location or not.
        Return type:
            bool
        """
        ...
```

--------------------------------

### Instantiate DatabricksCreateJobsOperator with Named Parameters

Source: https://airflow.apache.org/docs/apache-airflow-providers-databricks/stable/operators/jobs_create.html

This example shows how to initialize the DatabricksCreateJobsOperator using its named parameters, such as 'tasks' and 'job_clusters'. This approach provides a more structured way to define job configurations compared to using a raw JSON payload.

```python
tasks = [
    {
        "task_key": "test",
        "job_cluster_key": "job_cluster",
        "notebook_task": {
            "notebook_path": "/Shared/test",
        },
    },
]
job_clusters = [
    {
        "job_cluster_key": "job_cluster",
        "new_cluster": {
            "spark_version": "7.3.x-scala2.12",
            "node_type_id": "i3.xlarge",
            "num_workers": 2,
        },
    },
]

jobs_create_named = DatabricksCreateJobsOperator(
    task_id="jobs_create_named", tasks=tasks, job_clusters=job_clusters
)
```

--------------------------------

### Install Flink Provider with Kubernetes Support

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-flink/stable/index.html

Command to install the Apache Flink provider package along with optional CNCF Kubernetes dependencies. This allows for utilizing Kubernetes-specific features within Flink DAGs.

```bash
pip install apache-airflow-providers-apache-flink[cncf.kubernetes]
```

--------------------------------

### Initialize and Use GitDagBundle

Source: https://airflow.apache.org/docs/apache-airflow-providers-git/stable/_api/airflow/providers/git/bundles/git/index.html

Demonstrates how to instantiate the GitDagBundle class to manage DAGs from a remote Git repository. This class handles repository cloning, versioning, and path resolution for Airflow DAG processing.

```python
from airflow.providers.git.bundles.git import GitDagBundle

# Initialize the bundle
bundle = GitDagBundle(
    tracking_ref="main",
    repo_url="https://github.com/example/dags.git",
    subdir="dags",
    submodules=True
)

# Initialize the bundle for use
bundle.initialize()

# Access the path to the DAGs
dag_path = bundle.path
print(f"DAGs are located at: {dag_path}")
```

--------------------------------

### Download and Verify Airflow Provider Packages (Bash)

Source: https://airflow.apache.org/docs/apache-airflow-providers-edge3/stable/installing-providers-from-sources.html

This bash script downloads a specified Apache Airflow provider package version from PyPI, along with its associated signature (.asc) and SHA512 sum files. It uses 'pip download' to get the package and 'curl' to fetch the signature and checksum files, saving them to a temporary directory for verification.

```bash
#!/bin/bash
PACKAGE_VERSION=3.3.0
PACKAGE_NAME=apache-airflow-providers-edge3
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_edge3-3.3.0-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_edge3-3.3.0-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_edge3-3.3.0-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_edge3-3.3.0-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### Install Apache Airflow gRPC Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the apache-airflow-providers-grpc package, adding support for gRPC (Google Remote Procedure Call) in Apache Airflow. This provider is useful for building microservices and distributed systems.

```bash
pip install 'apache-airflow-providers-grpc'
```

--------------------------------

### Initialize ComputeEngineSSHHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/hooks/compute_ssh/index.html

Demonstrates how to instantiate the ComputeEngineSSHHook with specific connection parameters such as instance name, zone, and project ID. This hook is used to facilitate secure remote command execution on GCP instances.

```python
from airflow.providers.google.cloud.hooks.compute_ssh import ComputeEngineSSHHook

hook = ComputeEngineSSHHook(
    instance_name="my-instance",
    zone="us-central1-a",
    project_id="my-gcp-project",
    user="airflow",
    use_iap_tunnel=True
)

# Retrieve the underlying SSH connection
ssh_client = hook.get_conn()
```

--------------------------------

### Download and Verify Airflow Provider Packages

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-pinot/stable/installing-providers-from-sources.html

This script downloads a specific version of an Apache Airflow provider package from PyPI and fetches its associated signature and checksum files for manual verification. It uses a temporary directory to store the files and outputs the directory path upon completion.

```bash
#!/bin/bash
PACKAGE_VERSION=4.10.1
PACKAGE_NAME=apache-airflow-providers-apache-pinot
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_apache_pinot-4.10.1-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_apache_pinot-4.10.1-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_apache_pinot-4.10.1-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_apache_pinot-4.10.1-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo
```

--------------------------------

### Install Apache Airflow FTP Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the apache-airflow-providers-ftp package, which adds support for File Transfer Protocol (FTP) operations within Apache Airflow. This allows for file transfers to and from FTP servers.

```bash
pip install 'apache-airflow-providers-ftp'
```

--------------------------------

### Download and Verify Provider Package - Bash

Source: https://airflow.apache.org/docs/apache-airflow-providers-pinecone/stable/installing-providers-from-sources.html

This script downloads a specific version of an Apache Airflow provider package from PyPI, along with its PGP signature and SHA512 checksum files. It uses 'pip download' to get the wheel and 'curl' to fetch the signature and checksum. The script then displays the downloaded files in a temporary directory for manual verification.

```bash
#!/bin/bash
PACKAGE_VERSION=2.4.3
PACKAGE_NAME=apache-airflow-providers-pinecone
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_pinecone-2.4.3-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_pinecone-2.4.3-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_pinecone-2.4.3-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_pinecone-2.4.3-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### Install Apache Airflow Flask App Builder Provider

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Installs the apache-airflow-providers-fab package, which provides Flask App Builder integration for Apache Airflow. This is typically used for managing authentication and user interfaces.

```bash
pip install 'apache-airflow-providers-fab'
```

--------------------------------

### Auth List Environments

Source: https://airflow.apache.org/docs/apache-airflow-ctl/stable/cli-and-env-variables-ref.html

Lists all CLI environments and their authentication status.

```APIDOC
## GET /api/auth/list-envs

### Description
Lists all CLI environments and their authentication status.

### Method
GET

### Endpoint
/api/auth/list-envs

### Parameters
#### Query Parameters
- **api-token** (string) - Optional - The token to use for authentication.
- **output** (string) - Optional - The output format. Possible choices: table, json, yaml, plain. Default: 'json'.

### Request Example
```json
{}
```

### Response
#### Success Response (200)
- **environments** (array) - A list of environments with their auth status.

#### Response Example
```json
{
  "environments": [
    {
      "name": "production",
      "authenticated": true
    },
    {
      "name": "staging",
      "authenticated": false
    }
  ]
}
```
```

--------------------------------

### Install Airflow Provider with Constraints

Source: https://airflow.apache.org/docs/apache-airflow-providers/installing-from-pypi.html

Installs a specific Airflow provider package using pip while applying a version constraint file to ensure dependency compatibility. This is the recommended approach for maintaining stable environments.

```bash
pip install "apache-airflow-providers-celery" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.2/constraints-3.10.txt"
```

--------------------------------

### Initialize AthenaHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/hooks/athena/index.html

Demonstrates how to instantiate the AthenaHook class to interact with Amazon Athena services within an Airflow DAG.

```python
from airflow.providers.amazon.aws.hooks.athena import AthenaHook

hook = AthenaHook(aws_conn_id='aws_default', log_query=True)
```

--------------------------------

### Explicitly Adding Tasks to Setup Scope in Airflow

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/setup-and-teardown.html

Shows how to explicitly add an already instantiated task to the scope of a setup/teardown context. This is useful when tasks are defined separately and need to be associated with a setup scope.

```python
with my_teardown_task as scope:
    scope.add_task(work_task)  # work_task was already instantiated elsewhere
```

--------------------------------

### OSSCreateBucketOperator

Source: https://airflow.apache.org/docs/apache-airflow-providers-alibaba/stable/_api/airflow/providers/alibaba/cloud/operators/oss/index.html

This operator creates an OSS bucket in Alibaba Cloud.

```APIDOC
## OSSCreateBucketOperator

### Description
This operator creates an OSS bucket.

### Method
Not Applicable (Operator)

### Endpoint
Not Applicable (Operator)

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
None

### Response
#### Success Response (200)
None

#### Response Example
None
```

--------------------------------

### Initialize FlinkKubernetesOperator

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-flink/stable/_api/airflow/providers/apache/flink/operators/flink_kubernetes/index.html

Demonstrates the instantiation of the FlinkKubernetesOperator, which requires an application file path and connection details to interact with a Kubernetes cluster.

```python
from airflow.providers.apache.flink.operators.flink_kubernetes import FlinkKubernetesOperator

flink_task = FlinkKubernetesOperator(
    task_id='flink_deployment_task',
    application_file='path/to/flink_deployment.yaml',
    namespace='default',
    kubernetes_conn_id='kubernetes_default',
    api_group='flink.apache.org',
    api_version='v1beta1'
)
```

--------------------------------

### Qdrant Example DAG Test Run

Source: https://airflow.apache.org/docs/apache-airflow-providers-qdrant/stable/_api/tests/system/qdrant/example_dag_qdrant/index.html

Represents a test run function within the Qdrant example DAG for system tests. This function likely executes a specific test scenario involving Qdrant.

```python
def test_run():
    pass
```

--------------------------------

### Initialize Airflow Database and Create Admin User

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/executors/lambda-executor.html

Command to initialize the Airflow metadata database and create an initial administrative user account.

```bash
airflow users create --username admin --password admin --firstname <your first name> --lastname <your last name> --email <your email> --role Admin
```

--------------------------------

### System Tests: example_local_to_wasb

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/_api/tests/system/microsoft/azure/example_local_to_wasb/index.html

This section details the attributes and module contents for the example_local_to_wasb system test within the Azure integration of Apache Airflow.

```APIDOC
## tests.system.microsoft.azure.example_local_to_wasb

### Description
This module contains system test configurations for uploading local files to Azure Blob Storage (WASB) using Apache Airflow.

### Attributes

- **PATH_TO_UPLOAD_FILE** (string) - The local path to the file that needs to be uploaded.
- **ENV_ID** (string) - The environment identifier for the test.
- **DAG_ID** (string) - The ID of the Airflow DAG used for the test.
- **AZURE_CONTAINER_NAME** (string) - The name of the Azure Blob Storage container.
- **AZURE_BLOB_NAME** (string) - The name of the blob object in Azure.
- **upload** (function) - A function or task related to the upload process.
- **test_run** (function) - A function or task representing the execution of the test run.

### Module Contents

- `PATH_TO_UPLOAD_FILE`: Path to the local file for upload.
- `ENV_ID`: Environment ID for the test.
- `DAG_ID`: Airflow DAG ID.
- `AZURE_CONTAINER_NAME`: Azure container name.
- `AZURE_BLOB_NAME`: Azure blob name.
- `upload`: Upload task or function.
- `test_run`: Test execution task or function.
```

--------------------------------

### Postgres Connection Extra Field Examples

Source: https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/connections/postgres.html

Examples of JSON configurations for the 'Extra' field in Airflow Postgres connections. These snippets demonstrate how to configure SSL, AWS IAM, Redshift, and Azure Entra authentication.

```json
{
   "sslmode": "verify-ca",
   "sslcert": "/tmp/client-cert.pem",
   "sslca": "/tmp/server-ca.pem",
   "sslkey": "/tmp/client-key.pem"
}
```

```json
{
   "iam": true,
   "aws_conn_id": "aws_awesome_rds_conn"
}
```

```json
{
   "iam": true,
   "aws_conn_id": "aws_awesome_redshift_conn",
   "redshift": "/tmp/server-ca.pem",
   "cluster-identifier": "awesome-redshift-identifier"
}
```

```json
{
   "iam": true,
   "azure_conn_id": "azure_default_conn"
}
```

--------------------------------

### Initialize Go Module

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/go_module_utils/index.html

Initializes a Go module. If a go.mod file already exists, this function will not perform any action.

```APIDOC
## init_module

### Description
Initialize a Go module. If a `go.mod` file already exists, this function will do nothing.

### Parameters
#### Path Parameters
- **go_module_name** (str) - Required - The name of the Go module to initialize.
- **go_module_path** (str) - Required - The path to the directory containing the Go module.

### Request Example
```python
init_module(go_module_name="my_go_module", go_module_path="/path/to/module")
```

### Response
#### Success Response (200)
No specific response body is detailed, indicating an in-place modification or a void return.

#### Response Example
None
```

--------------------------------

### Get Pod Events - Python (Async)

Source: https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/_api/airflow/providers/cncf/kubernetes/hooks/kubernetes/index.html

Asynchronously retrieves events associated with a specific pod. It allows filtering events by resource version to get only newer events. Requires pod name and namespace.

```python
_async _get_pod_events(_name_ , _namespace_ , _resource_version =None_)
```

--------------------------------

### Cross-Product Mapping with Multiple Parameters in Airflow

Source: https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/dynamic-task-mapping.html

Demonstrates how to expand a task over multiple parameters simultaneously, creating a cross-product of all parameter combinations. The order of expansion is not guaranteed.

```python
from airflow.decorators import task

@task
def add(x: int, y: int):
    return x + y


added_values = add.expand(x=[2, 4, 8], y=[5, 10])
# This results in the add function being called with
# add(x=2, y=5)
# add(x=2, y=10)
# add(x=4, y=5)
# add(x=4, y=10)
# add(x=8, y=5)
# add(x=8, y=10)

```

--------------------------------

### Download and Verify Airflow Provider Package

Source: https://airflow.apache.org/docs/apache-airflow-providers-ftp/stable/installing-providers-from-sources.html

This bash script automates the process of downloading an Apache Airflow provider package from PyPI, along with its signature and SHA sum files. It uses `pip download` to get the package and `curl` to fetch the signature and checksum files. The script then displays the downloaded files in a temporary directory for manual verification.

```bash
#!/bin/bash
PACKAGE_VERSION=3.14.2
PACKAGE_NAME=apache-airflow-providers-ftp
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_ftp-3.14.2-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_ftp-3.14.2-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_ftp-3.14.2-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_ftp-3.14.2-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### Module: tests.system.providers.plexus.example_plexus

Source: https://airflow.apache.org/docs/apache-airflow-providers-plexus/stable/_api/tests/system/providers/plexus/example_plexus/index.html

This module defines the configuration and execution objects for Plexus system tests in Apache Airflow.

```APIDOC
## Module: tests.system.providers.plexus.example_plexus

### Description
This module contains the setup and execution logic for system tests related to the Plexus provider. It defines environment variables and DAG-specific constants.

### Constants
- **HOME** (string) - The default home directory path, e.g., '/home/acc'.
- **ENV_ID** (string) - The unique identifier for the test environment.
- **DAG_ID** (string) - The identifier for the system test DAG, defaults to 'test'.

### Execution Objects
- **t1** (object) - A task instance used within the test DAG.
- **test_run** (object) - The primary execution object for triggering the system test suite.

### Usage
These constants and objects are intended to be used within Airflow DAG files to facilitate integration testing of the Plexus provider.
```

--------------------------------

### Weaviate Cohere Example DAG - Python

Source: https://airflow.apache.org/docs/apache-airflow-providers-weaviate/stable/_api/tests/system/weaviate/example_weaviate_cohere/index.html

An example Airflow DAG that demonstrates the use of CohereEmbeddingOperator to generate embeddings and WeaviateIngestOperator to insert these embeddings into a Weaviate instance. It defines collection name and default arguments for the DAG.

```python
COLLECTION_NAME = 'weaviate_cohere_example_collection'
def_args = {}
def example_weaviate_cohere():
    """Example DAG which creates embeddings using CohereEmbeddingOperator and the uses WeaviateIngestOperator to insert embeddings to Weaviate ."""
    pass
test_run = None
```

--------------------------------

### Create Postgres Table using SQLExecuteQueryOperator

Source: https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/operators.html

This snippet demonstrates how to create a PostgreSQL table using the SQLExecuteQueryOperator. It shows both inline SQL and the recommended approach of using external SQL files for better organization and maintainability.

```python
from airflow import DAG
import datetime
from airflow.providers.postgres.operators.postgres import SQLExecuteQueryOperator
import os

ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
DAG_ID = "postgres_operator_dag"

with DAG(
    dag_id=DAG_ID,
    start_date=datetime.datetime(2020, 2, 2),
    schedule="@once",
    catchup=False,
) as dag:
    create_pet_table = SQLExecuteQueryOperator(
        task_id="create_pet_table",
        sql="""
            CREATE TABLE IF NOT EXISTS pet (
            pet_id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            pet_type VARCHAR NOT NULL,
            birth_date DATE NOT NULL,
            OWNER VARCHAR NOT NULL);
          """,
    )

create_pet_table_from_file = SQLExecuteQueryOperator(
    task_id="create_pet_table_from_file",
    conn_id="postgres_default",
    sql="sql/pet_schema.sql",
)
```

```sql
-- create pet table
CREATE TABLE IF NOT EXISTS pet (
    pet_id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    pet_type VARCHAR NOT NULL,
    birth_date DATE NOT NULL,
    OWNER VARCHAR NOT NULL);

```

--------------------------------

### Install Apache Airflow Edge Provider on Windows

Source: https://airflow.apache.org/docs/apache-airflow-providers-edge3/stable/install_on_windows.html

Installs the Edge provider for Apache Airflow using pip, referencing Airflow constraints for compatibility. This command is essential for enabling Edge Worker functionality within Airflow.

```bash
pip install apache-airflow-providers-edge3 --constraint https://raw.githubusercontent.com/apache/airflow/constraints-2.10.5/constraints-3.12.txt
```

--------------------------------

### Schedule DAGs with Logical Asset Expressions

Source: https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/asset-scheduling.html

Demonstrates how to use AND (&) and OR (|) operators to trigger DAGs based on multiple asset updates. These expressions allow for complex conditional dependencies between assets.

```python
dag1_asset = Asset("s3://dag1/output_1.txt")
dag2_asset = Asset("s3://dag2/output_1.txt")
dag3_asset = Asset("s3://dag3/output_3.txt")

# AND logic
with DAG(schedule=(dag1_asset & dag2_asset), ...): pass

# OR logic
with DAG(schedule=(dag1_asset | dag2_asset), ...): pass

# Combined logic
with DAG(schedule=(dag1_asset | (dag2_asset & dag3_asset)), ...): pass
```

--------------------------------

### Implement Cloud DLP Link Helper Classes

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/links/data_loss_prevention/index.html

Demonstrates the implementation of helper classes for generating UI links in Airflow. These classes define the link name and the format string required to construct valid Google Cloud console URLs.

```python
class CloudDLPJobTriggersListLink(BaseGoogleLink):
    name = 'Cloud DLP Job Triggers List'
    key = 'cloud_dlp_job_triggers_list_key'
    format_str = 'https://console.cloud.google.com/security/dlp/landing/inspection/triggers?project={project_id}'
```

--------------------------------

### Configure Go Environment for Apache Beam

Source: https://airflow.apache.org/docs/docker-stack/recipes.html

Initial Dockerfile configuration to support Apache Beam Go pipelines. It sets up the base image and defines environment variables for Go installation.

```dockerfile
ARG BASE_AIRFLOW_IMAGE
FROM ${BASE_AIRFLOW_IMAGE}
SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]
USER 0
ARG GO_VERSION=1.16.4
ENV GO_INSTALL_DIR=/usr/local/go
```

--------------------------------

### GET /tests/system/openlineage/example_openlineage_docs_file_dag

Source: https://airflow.apache.org/docs/apache-airflow-providers-openlineage/stable/_api/tests/system/openlineage/example_openlineage_docs_file_dag/index.html

Retrieves the definition and attributes of the OpenLineage documentation file DAG used for system testing.

```APIDOC
## GET /tests/system/openlineage/example_openlineage_docs_file_dag

### Description
This endpoint or module reference provides the structure for the OpenLineage documentation file DAG. It is used to verify the content of the DocumentationJobFacet within the Airflow system test suite.

### Method
GET

### Endpoint
/tests/system/openlineage/example_openlineage_docs_file_dag

### Parameters
None

### Request Example
N/A

### Response
#### Success Response (200)
- **DAG_ID** (string) - The identifier for the DAG: 'openlineage_docs_file_dag'
- **do_nothing_task** (object) - A placeholder task for DAG execution testing
- **test_run** (object) - The execution test run instance

#### Response Example
{
  "DAG_ID": "openlineage_docs_file_dag",
  "tasks": ["do_nothing_task"],
  "status": "active"
}
```

--------------------------------

### Example Generic SQL Transfer SQL Query

Source: https://airflow.apache.org/docs/apache-airflow-providers-common-sql/stable/_api/tests/system/common/sql/example_generic_transfer/index.html

Specifies the SQL query used within the example generic SQL transfer system test. This query is designed to fetch a limited number of records from a 'connection' table.

```sql
sql = 'SELECT * FROM connection LIMIT 10;'

```

--------------------------------

### Download and Verify Airflow Provider Package (Bash)

Source: https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/installing-providers-from-sources.html

This bash script downloads a specific version of an Apache Airflow provider package from PyPI, along with its signature and SHA sum files. It then displays the downloaded files for manual verification. Dependencies include 'pip' and 'curl'.

```bash
#!/bin/bash
PACKAGE_VERSION=6.12.0
PACKAGE_NAME=apache-airflow-providers-snowflake
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_snowflake-6.12.0-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_snowflake-6.12.0-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_snowflake-6.12.0-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_snowflake-6.12.0-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### Kubernetes Executor: Delete Option Kwargs Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/configurations-ref.html

This example demonstrates how to pass optional keyword arguments to the `delete_namespaced_pod` method in the Kubernetes client. This allows for fine-grained control over pod deletion, such as specifying a grace period for termination.

```json
{"grace_period_seconds": 10}
```

--------------------------------

### Example Drill DAG System Test

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-drill/stable/_api/tests/system/apache/drill/example_drill_dag/index.html

This section describes the example Airflow DAG designed to execute SQL queries in an Apache Drill environment using the DrillOperator. It outlines the DAG's attributes and module contents.

```APIDOC
## tests.system.apache.drill.example_drill_dag

Example Airflow DAG to execute SQL in an Apache Drill environment using the DrillOperator.

### Attributes

| Attribute | Description |
|---|---|
| `ENV_ID` |  |
| `DAG_ID` |  |
| `sql_task` |  |
| `test_run` |  |

### Module Contents

- `ENV_ID`
- `DAG_ID`
- `sql_task`
- `test_run`
```

--------------------------------

### Manage Google Cloud Data Fusion Instances with Airflow

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/operators/datafusion/index.html

Demonstrates the initialization of Data Fusion operators for restarting, deleting, and creating instances. These operators require specific GCP project details, instance names, and location configurations.

```python
from airflow.providers.google.cloud.operators.datafusion import (
    CloudDataFusionRestartInstanceOperator,
    CloudDataFusionDeleteInstanceOperator,
    CloudDataFusionCreateInstanceOperator
)

# Restart an instance
restart_task = CloudDataFusionRestartInstanceOperator(
    task_id="restart_instance",
    instance_name="my-instance",
    location="us-central1",
    project_id="my-project"
)

# Delete an instance
delete_task = CloudDataFusionDeleteInstanceOperator(
    task_id="delete_instance",
    instance_name="my-instance",
    location="us-central1",
    project_id="my-project"
)

# Create an instance
create_task = CloudDataFusionCreateInstanceOperator(
    task_id="create_instance",
    instance_name="new-instance",
    instance={"type": "BASIC"},
    location="us-central1",
    project_id="my-project"
)
```

--------------------------------

### Example of get_ui_field_behaviour Implementation - Python

Source: https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/hooks/base/index.html

An example demonstrating how to override the get_ui_field_behaviour method in a derived hook class to customize the connection form's UI fields. It shows calling the superclass method to inherit base customizations.

```python
@classmethod
def get_ui_field_behaviour(cls):
    return super().get_ui_field_behaviour()
```

--------------------------------

### GET /api/v2/pools

Source: https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html

Retrieve a list of pools.

```APIDOC
## GET /api/v2/pools

### Description
Retrieve a list of pools with optional filtering and sorting.

### Method
GET

### Endpoint
/api/v2/pools

### Parameters
#### Query Parameters
- **limit** (integer) - Optional - Limit the number of results (Default: 50)
- **offset** (integer) - Optional - Offset for pagination (Default: 0)
- **order_by** (Array of strings) - Optional - Attributes to order by (Default: ["id"])
- **pool_name_pattern** (string) - Optional - SQL LIKE expression for filtering pool names

### Response
#### Success Response (200)
- **pools** (array) - List of pool objects
- **total_entries** (integer) - Total number of pools

#### Response Example
{
  "pools": [
    {
      "name": "string",
      "slots": -1,
      "description": "string",
      "include_deferred": true,
      "occupied_slots": 0,
      "running_slots": 0,
      "queued_slots": 0,
      "scheduled_slots": 0,
      "open_slots": 0,
      "deferred_slots": 0
    }
  ],
  "total_entries": 0
}
```

--------------------------------

### Verify PGP Signatures with GPG

Source: https://airflow.apache.org/docs/apache-airflow-providers-apache-kylin/stable/installing-providers-from-sources.html

This snippet demonstrates how to verify the PGP signature of a downloaded file using the GPG command-line tool. It requires the KEYS file and the .asc signature file for the distribution. The output indicates whether the signature is 'Good' or not, confirming the integrity and origin of the file.

```bash
gpg --verify apache-airflow-providers-********.asc apache-airflow-********* 
```

--------------------------------

### Configure Provider YAML for CLI Commands

Source: https://airflow.apache.org/docs/apache-airflow-providers/core-extensions/cli-commands.html

Example of how to configure the `cli` section in a provider's `provider.yaml` file to point to the function that returns CLI commands.

```APIDOC
## UPDATE provider.yaml

### Description
This section details how to update the `provider.yaml` file for your Airflow provider to include the custom CLI commands. By specifying the path to the function that returns the list of CLI commands, you enable Airflow to discover and load them.

### Method
UPDATE

### Endpoint
`provider.yaml` file

### Parameters
#### Request Body
- **cli** (array) - Required - A list of strings, where each string is the Python path to a function that returns CLI commands.

### Request Example
```yaml
cli:
  - airflow.providers.<your_provider_name>.cli.definition.get_my_cli_commands
```

### Response
This is a configuration file update, no direct API response. The changes take effect upon Airflow's next startup or CLI command execution.
```

--------------------------------

### GET /api/v2/dagWarnings

Source: https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html

Lists DAG warnings.

```APIDOC
## GET /api/v2/dagWarnings

### Description
Retrieves a list of warnings associated with DAGs.

### Method
GET

### Endpoint
/api/v2/dagWarnings

### Parameters
#### Query Parameters
- **dag_id** (string) - Optional - Filter by DAG ID.
- **warning_type** (string) - Optional - Filter by warning type.
- **limit** (integer) - Optional - Limit results.
- **offset** (integer) - Optional - Offset results.

### Response
#### Success Response (200)
- **dag_warnings** (array) - List of warnings.
- **total_entries** (integer) - Total count.

#### Response Example
{
  "dag_warnings": [
    {
      "dag_id": "string",
      "warning_type": "asset conflict",
      "message": "string",
      "timestamp": "2019-08-24T14:15:22Z"
    }
  ],
  "total_entries": 0
}
```

--------------------------------

### Configure Azure Cosmos Connection via Environment Variable

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/connections/azure_cosmos.html

This example demonstrates how to set the Azure Cosmos connection details using an environment variable with URI syntax. It includes specifying the endpoint, master key, and optional parameters like database name and collection name. Ensure all URI components are URL-encoded.

```bash
export AIRFLOW_CONN_AZURE_COSMOS_DEFAULT='azure-cosmos://https%3A%2F%2Fairflow.azure.com:master%20key@?database_name=mydatabase&collection_name=mycollection'
```

--------------------------------

### GET /api/v2/config

Source: https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html

Retrieves the Airflow configuration.

```APIDOC
## GET /api/v2/config

### Description
Fetches the current Airflow configuration sections and options.

### Method
GET

### Endpoint
/api/v2/config

### Parameters
#### Query Parameters
- **section** (string) - Optional - Filter by configuration section.

### Response
#### Success Response (200)
- **sections** (array) - List of configuration sections.

#### Response Example
{
  "sections": [
    {
      "name": "string",
      "options": [{"key": "string", "value": "string"}]
    }
  ]
}
```

--------------------------------

### GET /api/v2/dagStats

Source: https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html

Retrieves statistics for DAGs.

```APIDOC
## GET /api/v2/dagStats

### Description
Returns statistics for DAGs, optionally filtered by specific IDs.

### Method
GET

### Endpoint
/api/v2/dagStats

### Parameters
#### Query Parameters
- **dag_ids** (Array of strings) - Optional - List of DAG IDs to filter by.

### Response
#### Success Response (200)
- **dags** (array) - List of DAG statistics.
- **total_entries** (integer) - Total count of entries.

#### Response Example
{
  "dags": [
    {
      "dag_id": "string",
      "dag_display_name": "string",
      "stats": [{"state": "queued", "count": 0}]
    }
  ],
  "total_entries": 0
}
```

--------------------------------

### Run Celery Flower

Source: https://airflow.apache.org/docs/apache-airflow-providers-celery/stable/cli-ref.html

Command to start the Celery Flower monitoring tool with various configuration options like authentication, port, and logging.

```bash
airflow celery flower -p 5555 -A user:password
```

--------------------------------

### Configure DAG Bundle List

Source: https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html

Defines the backend configurations for DAG bundles. Each entry requires a name, classpath, and optional keyword arguments to specify how DAGs are loaded.

```json
[
  {
    "name": "dags-folder",
    "classpath": "airflow.dag_processing.bundles.local.LocalDagBundle",
    "kwargs": {}
  }
]
```

```json
[
  {
    "name": "my-git-repo",
    "classpath": "airflow.providers.git.bundles.git.GitDagBundle",
    "kwargs": {
      "subdir": "dags",
      "tracking_ref": "main",
      "refresh_interval": 0
    }
  }
]
```

--------------------------------

### Install Python Dependencies

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/executors/batch-executor.html

Installs Python dependencies from a requirements.txt file during Docker image build. The requirements file can be in the Docker context or specified via a build argument. Ensure the file path is correct relative to the Docker context.

```bash
# Example Dockerfile snippet for installing dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --user -r /tmp/requirements.txt
```

--------------------------------

### Enable Logging and XCom in Async Pods

Source: https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/_modules/tests/system/cncf/kubernetes/example_kubernetes_async.html

Shows how to enable logs and XCom pushing for an asynchronous Kubernetes task, allowing the pod to return data to Airflow.

```python
kubernetes_task_async_log = KubernetesPodOperator(
    task_id="kubernetes_task_async_log",
    image="ubuntu",
    do_xcom_push=True,
    deferrable=True,
    get_logs=True,
    logging_interval=5,
)
```

--------------------------------

### Initialize and Use PackageIndexHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-standard/stable/_api/airflow/providers/standard/hooks/package_index/index.html

Demonstrates how to instantiate the PackageIndexHook and retrieve the connection URL. This hook is used to manage connections to custom Python package repositories.

```python
from airflow.providers.standard.hooks.package_index import PackageIndexHook

# Initialize the hook
hook = PackageIndexHook(pi_conn_id='my_package_index')

# Retrieve the connection URL with credentials
url = hook.get_connection_url()

# Test the connection
status, message = hook.test_connection()
print(f"Connection status: {status}, Message: {message}")
```

--------------------------------

### MySQL System Test Example DAG

Source: https://airflow.apache.org/docs/apache-airflow-providers-mysql/stable/_api/tests/system/mysql/example_mysql/index.html

This snippet demonstrates an example DAG used for system testing MySQL operations. It includes tasks for dropping tables and running tests, showcasing the integration of MySQL operators within Airflow.

```python
from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator

ENV_ID = "mysql"
DAG_ID = "example_mysql"

with DAG(
    dag_id=DAG_ID,
    schedule=None,
    start_date=pendulum.datetime(2023, 10, 26, tz="UTC"),
    catchup=False,
    tags=["mysql"],
)
as dag:
    start = EmptyOperator(task_id="start")

    drop_table_mysql_task = MySqlOperator(
        task_id="drop_table_mysql_task",
        mysql_conn_id="mysql_default",
        sql="DROP TABLE IF EXISTS test_mysql_table;",
    )

    run_mysql_task = MySqlOperator(
        task_id="run_mysql_task",
        mysql_conn_id="mysql_default",
        sql="CREATE TABLE test_mysql_table (id INT, name VARCHAR(50));",
    )

    end = EmptyOperator(task_id="end")

    start >> drop_table_mysql_task >> run_mysql_task >> end

```

--------------------------------

### Verify PyPI Provider Package with Bash Script

Source: https://airflow.apache.org/docs/apache-airflow-providers-cloudant/stable/installing-providers-from-sources.html

This bash script automates the process of downloading a specific Apache Airflow provider package from PyPI, along with its signature and SHA512 sum files. It uses `pip download` to get the package and `curl` to fetch the signature and checksum files. The script then displays the downloaded files in a temporary directory for manual verification.

```bash
#!/bin/bash
PACKAGE_VERSION=4.3.3
PACKAGE_NAME=apache-airflow-providers-cloudant
provider_download_dir=$(mktemp -d)
pip download --no-deps "${PACKAGE_NAME}==${PACKAGE_VERSION}" --dest "${provider_download_dir}"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_cloudant-4.3.3-py3-none-any.whl.asc" \
    -L -o "${provider_download_dir}/apache_airflow_providers_cloudant-4.3.3-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/providers/apache_airflow_providers_cloudant-4.3.3-py3-none-any.whl.sha512" \
    -L -o "${provider_download_dir}/apache_airflow_providers_cloudant-4.3.3-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${provider_download_dir}"
ls -la "${provider_download_dir}"
echo

```

--------------------------------

### Example Airflow DAG with Informatica Lineage

Source: https://airflow.apache.org/docs/apache-airflow-providers-informatica/stable/guides/usage.html

An example Airflow DAG demonstrating how to use the PythonOperator with inlets and outlets defined for Informatica lineage tracking. When the 'my_python_task' succeeds, the provider automatically creates a lineage link in Informatica EDC.

```python
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime

def my_python_task(**kwargs):
    print("Hello Informatica Lineage!")

with DAG(
    dag_id="example_informatica_lineage_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    python_task = PythonOperator(
        task_id="my_python_task",
        python_callable=my_python_task,
        inlets=[{"dataset_uri": "edc://object/source_table_abc123"}],
        outlets=[{"dataset_uri": "edc://object/target_table_xyz789"}],
    )

```

--------------------------------

### Airflow HTTP Sensor Check Examples

Source: https://airflow.apache.org/docs/apache-airflow-providers-http/stable/_modules/tests/system/http/example_http.html

This Python code demonstrates the use of Airflow's HttpSensor to check the status of an HTTP endpoint. It includes examples for both standard polling and deferrable modes, allowing for more efficient resource utilization.

```python
# [START howto_operator_http_http_sensor_check]


task_http_sensor_check = HttpSensor(
    task_id="http_sensor_check",
    http_conn_id="http_default",
    endpoint="",
    request_params={},
    response_check=lambda response: "httpbin" in response.text,
    poke_interval=5,
    dag=dag,
)


# [END howto_operator_http_http_sensor_check]
# [START howto_operator_http_http_sensor_check_deferrable]


task_http_sensor_check_async = HttpSensor(
    task_id="http_sensor_check_async",
    http_conn_id="http_default",
    endpoint="",
    deferrable=True,
    request_params={},
    poke_interval=5,
    dag=dag,
)


# [END howto_operator_http_http_sensor_check_deferrable]

```

--------------------------------

### Initialize and Close LevelDB Connection - Python

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/leveldb/hooks/leveldb/index.html

Demonstrates how to initialize a LevelDB connection using the LevelDBHook and subsequently close it. The get_conn method creates the connection, and close_conn ensures it is properly terminated. It handles potential initialization errors.

```python
from airflow.providers.google.leveldb.hooks.leveldb import LevelDBHook

# Initialize the hook with a connection ID
hook = LevelDBHook(leveldb_conn_id='my_leveldb_conn')

# Get the LevelDB connection (creates it if it doesn't exist)
try:
    db = hook.get_conn(name='/tmp/testdb/', create_if_missing=True)
    print("LevelDB connection established.")
    # Perform database operations here

    # Close the connection when done
    hook.close_conn()
    print("LevelDB connection closed.")
except Exception as e:
    print(f"An error occurred: {e}")

```

--------------------------------

### BigQueryToPostgresOperator Initialization and Execution

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/transfers/bigquery_to_postgres/index.html

This snippet demonstrates the initialization of the BigQueryToPostgresOperator, which fetches data from BigQuery and inserts it into a PostgreSQL table. It highlights key parameters like target_table_name, postgres_conn_id, replace, selected_fields, and replace_index. The execute method is the core task execution logic.

```python
from airflow.providers.google.cloud.transfers.bigquery_to_postgres import BigQueryToPostgresOperator

# Example usage within an Airflow DAG
with DAG(...) as dag:
    transfer_data = BigQueryToPostgresOperator(
        task_id='bigquery_to_postgres_transfer',
        bigquery_conn_id='google_cloud_default',
        postgres_conn_id='postgres_default',
        sql='SELECT * FROM my_bigquery_dataset.my_table',
        target_table_name='my_postgres_table',
        replace=False,
        selected_fields=None,
        replace_index=None
    )
```

```python
class BigQueryToPostgresOperator(BigQueryToSqlBaseOperator):
    """Fetch data from a BigQuery table (alternatively fetch selected columns) and insert into PostgreSQL table."""
    def __init__(
        self,
        *,  # Force keyword arguments
        target_table_name: str,
        postgres_conn_id: str = 'postgres_default',
        replace: bool = False,
        selected_fields: list[str] | str | None = None,
        replace_index: list[str] | str | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        # ... operator logic ...

    def execute(self, context):
        # ... execution logic ...
        pass

    @property
    def postgres_hook(self) -> PostgresHook:
        """Return a concrete SQL Hook (a PostgresHook for instance)."""
        return PostgresHook(postgres_conn_id=self.postgres_conn_id, schema=self.postgres_schema)

    def get_sql_hook(self) -> PostgresHook:
        """Return a concrete SQL Hook (a PostgresHook for instance)."""
        return self.postgres_hook
```

--------------------------------

### OSSHook

Source: https://airflow.apache.org/docs/apache-airflow-providers-alibaba/stable/_api/airflow/providers/alibaba/cloud/hooks/oss/index.html

Interact with Alibaba Cloud OSS using the oss2 library.

```APIDOC
## OSSHook

### Description
Interact with Alibaba Cloud OSS, using the oss2 library.

### Class
`OSSHook`

### Methods
(Details for methods would typically be listed here if available in the source text)

### Example Usage
(Example usage would be provided here if available in the source text)
```

--------------------------------

### Airflow Notifier Usage Example

Source: https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/callbacks.html

Illustrates how to integrate custom notifiers with Airflow callbacks. This example shows passing a custom notifier instance to on_success_callback and on_failure_callback at both the DAG and task levels to send notifications based on execution status.

```python
from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator

from myprovider.notifier import MyNotifier

with DAG(
    dag_id="example_notifier",
    on_success_callback=MyNotifier(message="Success!"),
    on_failure_callback=MyNotifier(message="Failure!"),
):
    task = BashOperator(
        task_id="example_task",
        bash_command="exit 1",
        on_success_callback=MyNotifier(message="Task Succeeded!"),
    )

```

--------------------------------

### Airflow CLI: List Assets by Alias

Source: https://airflow.apache.org/docs/apache-airflow-ctl/stable/cli-and-env-variables-ref.html

Lists assets based on their aliases. Authentication via API token is required, and environment and output format can be specified.

```bash
airflowctl assets list-by-alias [-h] [--api-token API_TOKEN] [-e ENV] [--output (table, json, yaml, plain)]
```

--------------------------------

### Get Docker Connection using DockerHook in Python

Source: https://airflow.apache.org/docs/apache-airflow-providers-docker/stable/_api/airflow/providers/docker/hooks/docker/index.html

This method establishes and returns a connection to the Docker host, returning a cached `docker.APIClient` instance. It's the primary way to get an active client object for interacting with Docker functionalities.

```python
from airflow.providers.docker.hooks.docker import DockerHook

docker_hook = DockerHook()
docker_client = docker_hook.get_conn()
```

--------------------------------

### POST /spanner/instance/deploy

Source: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/operators/spanner/index.html

Creates or updates a Google Cloud Spanner instance.

```APIDOC
## POST /spanner/instance/deploy

### Description
Creates a new Cloud Spanner instance or updates an existing one.

### Method
POST

### Endpoint
/spanner/instance/deploy

### Parameters
#### Request Body
- **project_id** (string) - Required - The Google Cloud project ID.
- **instance_id** (string) - Required - The ID of the Spanner instance.
- **configuration** (string) - Required - The instance configuration.

### Request Example
{
  "project_id": "my-project",
  "instance_id": "my-instance",
  "configuration": "regional-us-central1"
}

### Response
#### Success Response (200)
- **status** (string) - The result of the deployment operation.
```

--------------------------------

### Configure Airflow Email Backend

Source: https://airflow.apache.org/docs/apache-airflow/stable/howto/email-config.html

Set the email backend for Airflow. This example shows how to retrieve the current email backend configuration using the Airflow CLI.

```bash
$ airflow config get-value email email_backend
airflow.utils.email.send_email_smtp
```

--------------------------------

### Install Apache Airflow Providers

Source: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

Commands to install specific Apache Airflow provider packages using pip. These packages extend Airflow functionality to interact with external systems like Snowflake, SQLite, SSH, Tableau, Telegram, and Teradata.

```bash
pip install 'apache-airflow-providers-snowflake'
```

```bash
pip install 'apache-airflow-providers-sqlite'
```

```bash
pip install 'apache-airflow-providers-ssh'
```

```bash
pip install 'apache-airflow-providers-standard'
```

```bash
pip install 'apache-airflow-providers-tableau'
```

```bash
pip install 'apache-airflow-providers-telegram'
```

```bash
pip install 'apache-airflow-providers-teradata'
```

--------------------------------

### Install/Upgrade Airflow Dependencies

Source: https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html

Installs or upgrades Airflow and specific providers using pip, with an option to use official constraints for version compatibility. This command allows for flexible dependency management, including installing versions not present in the default constraints.

```bash
pip install "apache-airflow[celery]==3.1.8" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.1.8/constraints-3.10.txt"
pip install "apache-airflow==3.1.8" apache-airflow-providers-google==10.1.1
```

```bash
pip install "apache-airflow[celery]==3.1.8" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.1.8/constraints-3.10.txt"
pip install "apache-airflow[celery]==3.1.8" dbt-core==0.20.0
```

--------------------------------

### Configure and Start Edge Worker on Windows

Source: https://airflow.apache.org/docs/apache-airflow-providers-edge3/stable/install_on_windows.html

A batch script to set environment variables and start the Edge Worker service on Windows. It configures authentication, API endpoints, logging, and executor settings. This script is crucial for running the Edge Worker.

```batch
@echo off
REM For versions 3.0.0 or later
set AIRFLOW__API_AUTH__JWT_SECRET=<matching the api-server...>
REM for versions earlier than 3.0.0
set AIRFLOW__CORE__INTERNAL_API_SECRET_KEY=<use this as configured centrally in api-server...>

REM For all versions
set AIRFLOW__CORE__DAGS_FOLDER=dags
set AIRFLOW__LOGGING__BASE_LOG_FOLDER=edge_logs
set AIRFLOW__EDGE__API_URL=https://your-hostname-and-port/edge_worker/v1/rpcapi
set AIRFLOW__CORE__EXECUTOR=airflow.providers.edge3.executors.edge_executor.EdgeExecutor
set AIRFLOW__CORE__LOAD_EXAMPLES=False
set AIRFLOW_ENABLE_AIP_44=true
@REM Add if needed: set http_proxy=http://my-company-proxy.com:3128
@REM Add if needed: set https_proxy=http://my-company-proxy.com:3128
airflow edge worker --concurrency 4 --queues windows

```

--------------------------------

### Initialize KubernetesPatchJobOperator

Source: https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/_api/airflow/providers/cncf/kubernetes/operators/job/index.html

Example showing how to instantiate the KubernetesPatchJobOperator to update a Kubernetes Job's specification, such as suspending it.

```python
from airflow.providers.cncf.kubernetes.operators.job import KubernetesPatchJobOperator

patch_job = KubernetesPatchJobOperator(
    task_id="patch_job_task",
    name="my-job",
    namespace="default",
    body={"spec": {"suspend": True}},
    kubernetes_conn_id="kubernetes_default"
)
```

--------------------------------

### S3GetBucketTaggingOperator

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/operators/s3/index.html

This operator gets tagging from an S3 bucket.

```APIDOC
## GET /websites/airflow_apache/operators/s3/get_bucket_tagging

### Description
This operator gets tagging from an S3 bucket.

### Method
GET

### Endpoint
/websites/airflow_apache/operators/s3/get_bucket_tagging

### Parameters
#### Query Parameters
- **bucket_name** (str) - Required - The name of the S3 bucket to reference.
- **aws_conn_id** (str) - Optional - The Airflow connection used for AWS credentials. Defaults to None, using default boto3 behavior.
- **region_name** (str) - Optional - The AWS region name. Defaults to None, using default boto3 behavior.
- **verify** (bool) - Optional - Whether or not to verify SSL certificates.
- **botocore_config** (dict) - Optional - Configuration dictionary for botocore client.

### Request Example
```json
{
  "bucket_name": "my-s3-bucket-with-tags",
  "aws_conn_id": "aws_default",
  "region_name": "eu-central-1"
}
```

### Response
#### Success Response (200)
- **tag_set** (list) - A list of dictionaries, where each dictionary represents a tag with 'Key' and 'Value' fields.

#### Response Example
```json
{
  "tag_set": [
    {
      "Key": "Environment",
      "Value": "Production"
    },
    {
      "Key": "Project",
      "Value": "Airflow"
    }
  ]
}
```
```

--------------------------------

### Configure Botocore Settings

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/cloudformation.html

Example dictionary configuration for botocore.config.Config, used to manage connection timeouts, retries, and signature versions.

```python
{
    "signature_version": "unsigned",
    "s3": {
        "us_east_1_regional_endpoint": True,
    },
    "retries": {
      "mode": "standard",
      "max_attempts": 10,
    },
    "connect_timeout": 300,
    "read_timeout": 300,
    "tcp_keepalive": True,
}
```

--------------------------------

### S3GetBucketTaggingOperator

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/operators/s3/index.html

This operator gets tagging from an S3 bucket.

```APIDOC
## GET /s3/get_bucket_tagging

### Description
Retrieves the tagging information for an S3 bucket.

### Method
GET

### Endpoint
/s3/get_bucket_tagging

### Parameters
#### Query Parameters
- **bucket_name** (string) - Required - The name of the bucket to retrieve tags from.

### Request Example
GET /s3/get_bucket_tagging?bucket_name=my-tagged-bucket

### Response
#### Success Response (200)
- **tag_set** (array) - A list of tag key-value pairs associated with the bucket.
  - **Key** (string) - The tag key.
  - **Value** (string) - The tag value.

#### Response Example
{
  "tag_set": [
    {"Key": "environment", "Value": "production"},
    {"Key": "owner", "Value": "data-team"}
  ]
}
```

--------------------------------

### GET /get_query_results

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/hooks/athena/index.html

Fetches the results of a submitted query.

```APIDOC
## GET /get_query_results

### Description
Fetch submitted query results.

### Method
GET

### Endpoint
`/get_query_results`

### Parameters
#### Query Parameters
- **query_execution_id** (str) - Required - Id of submitted Athena query.
- **next_token_id** (str) - Optional - The token that specifies where to start pagination.
- **max_results** (int) - Optional - The maximum number of results (rows) to return in this request. Defaults to 1000.

### Response
#### Success Response (200)
- **results** (dict | None) - None if the query is in intermediate, failed, or cancelled state. Otherwise a dict of query outputs.

### Response Example
```json
{
  "results": {
    "ResultSet": {
      "Rows": [
        {
          "Data": [
            {
              "VarCharValue": "column1_value1"
            },
            {
              "VarCharValue": "column2_value1"
            }
          ]
        },
        {
          "Data": [
            {
              "VarCharValue": "column1_value2"
            },
            {
              "VarCharValue": "column2_value2"
            }
          ]
        }
      ],
      "ResultSetMetadata": {
        "ColumnInfo": [
          {
            "Catalog": "AwsDataCatalog",
            "SchemaName": "default",
            "TableName": "example_table",
            "Name": "column1",
            "Type": "varchar"
          },
          {
            "Catalog": "AwsDataCatalog",
            "SchemaName": "default",
            "TableName": "example_table",
            "Name": "column2",
            "Type": "varchar"
          }
        ]
      }
    },
    "NextToken": "example-next-token"
  }
}
```
```

--------------------------------

### Airflow Operator XCom and Documentation Parameters

Source: https://airflow.apache.org/docs/apache-airflow-providers-openlineage/stable/_api/tests/system/openlineage/example_openlineage_base_complex_dag/index.html

Illustrates the usage of parameters like 'do_xcom_push', 'multiple_outputs' for controlling XCom behavior, and various 'doc_*' parameters for adding documentation in different formats to Airflow tasks.

```python
# Example for do_xcom_push and multiple_outputs
# Assuming 'result' is the return value of the operator
# If do_xcom_push is True, 'result' will be pushed as an XCom.
# If multiple_outputs is True and result is a dict, each key-value pair is pushed as a separate XCom.

# Example for documentation parameters
# doc='This is a simple note.'
# doc_md='## Markdown Documentation\nThis is a markdown note.'
# doc_rst='.. This is an RST note.'
```

--------------------------------

### GET /check_query_status

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/hooks/athena/index.html

Fetches the state of a submitted query.

```APIDOC
## GET /check_query_status

### Description
Fetch the state of a submitted query.

### Method
GET

### Endpoint
`/check_query_status`

### Parameters
#### Query Parameters
- **query_execution_id** (str) - Required - Id of submitted Athena query.
- **use_cache** (bool) - Optional - If True, use execution information cache.

### Response
#### Success Response (200)
- **state** (str | None) - One of valid query states (e.g., 'QUEUED', 'RUNNING', 'SUCCEEDED', 'FAILED', 'CANCELLED'), or None if the response is malformed.

### Response Example
```json
{
  "state": "SUCCEEDED"
}
```
```

--------------------------------

### SageMakerStartPipelineOperator

Source: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/operators/sagemaker/index.html

Starts an Amazon SageMaker pipeline execution.

```APIDOC
## SageMakerStartPipelineOperator

### Description
This operator starts an execution of a SageMaker pipeline. It allows for specifying pipeline parameters and waiting for completion.

### Method
Not Applicable (Operator)

### Endpoint
Not Applicable (Operator)

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None (Configuration is done via operator parameters)

### Request Example
```python
from airflow.providers.amazon.aws.operators.sagemaker import SageMakerStartPipelineOperator

start_pipeline_op = SageMakerStartPipelineOperator(
    task_id='sagemaker_start_pipeline_operator',
    pipeline_name='your-pipeline-name',
    pipeline_params={
        'PipelineParameterName1': 'value1',
        'PipelineParameterName2': 'value2'
    },
    wait_for_completion=True,
    check_interval=60,
    waiter_max_attempts=60,
    verbose=True,
    deferrable=False
)
```

### Response
#### Success Response (200)
Details of the started SageMaker pipeline execution.

#### Response Example
```json
{
  "PipelineExecutionArn": "arn:aws:sagemaker:us-east-1:123456789012:pipeline/your-pipeline-name/execution/execution-id",
  "PipelineExecutionStatus": "Executing"
}
```
```

--------------------------------

### Neo4jSensor Usage Example

Source: https://airflow.apache.org/docs/apache-airflow-providers-neo4j/stable/_api/airflow/providers/neo4j/sensors/neo4j/index.html

This example demonstrates how to use the Neo4jSensor to wait for a condition in Neo4j. It connects to Neo4j using a specified connection ID and executes a Cypher query. The sensor polls until the query result satisfies a condition or a failure condition is met.

```python
from airflow.providers.neo4j.sensors.neo4j import Neo4jSensor

wait_person_exists = Neo4jSensor(
    task_id="wait_person_exists",
    neo4j_conn_id="neo4j_default",
    cypher="MATCH (p:Person) RETURN count(p) > 0",
)
```

--------------------------------

### AzureKeyVaultBackend Class Overview

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/_api/airflow/providers/microsoft/azure/secrets/key_vault/index.html

Overview of the AzureKeyVaultBackend class, its attributes, and methods for interacting with Azure Key Vault.

```APIDOC
## AzureKeyVaultBackend

This class provides a backend for retrieving secrets, variables, and configurations from Azure Key Vault.

### Attributes

- **vault_url** (str) - The URL of the Azure Key Vault.
- **connections_prefix** (str) - Prefix for connections stored in Key Vault.
- **variables_prefix** (str) - Prefix for variables stored in Key Vault.
- **config_prefix** (str) - Prefix for configurations stored in Key Vault.
- **sep** (str) - Separator used to concatenate prefixes and keys.
- **tenant_id** (str) - The Azure Active Directory tenant ID.
- **client_id** (str) - The Azure Active Directory client ID.
- **client_secret** (str) - The Azure Active Directory client secret.
- **managed_identity_client_id** (str) - Client ID for managed identity authentication.
- **workload_identity_tenant_id** (str) - Tenant ID for workload identity authentication.
- **kwargs** (dict) - Additional keyword arguments passed to the Key Vault client.
- **client** - The initialized Azure Key Vault client object.

### Methods

- **get_conn_value(conn_id)**
  Retrieves a connection value from Azure Key Vault.

- **get_variable(key)**
  Retrieves a variable from Azure Key Vault.

- **get_config(key)**
  Retrieves a configuration value from Azure Key Vault.

- **build_path(prefix, key)**
  Builds the full path for a secret in Azure Key Vault by concatenating a prefix and a key using the defined separator.
```

--------------------------------

### MSSQL Example Operator Usage in Airflow System Tests

Source: https://airflow.apache.org/docs/apache-airflow-providers-microsoft-mssql/stable/_modules/tests/system/microsoft/mssql/example_mssql.html

This Python code snippet demonstrates the example usage of Microsoft SQL Server (MSSQL) related operators within the Apache Airflow system tests. It includes necessary imports and licensing information.

```python
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
Example use of MsSql related operators.
"""

from __future__ import annotations

```

--------------------------------

### Creating a mapped TaskGroup

Source: https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/dynamic-task-mapping.html

Demonstrates how to apply the expand method to a @task_group to create multiple instances of a group of tasks based on input data.

```python
@task_group
def file_transforms(filename):
    return convert_to_yaml(filename)

file_transforms.expand(filename=["data1.json", "data2.json"])
```

--------------------------------

### KubernetesInstallKueueOperator

Source: https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/_api/airflow/providers/cncf/kubernetes/operators/kueue/index.html

Installs a specific version of Kubernetes Kueue into the cluster.

```APIDOC
## POST /operators/kueue/install

### Description
Installs a Kubernetes Kueue instance using the specified version and connection ID.

### Method
POST

### Parameters
#### Request Body
- **kueue_version** (str) - Required - The version of Kueue to install.
- **kubernetes_conn_id** (str) - Optional - The Airflow connection ID for the Kubernetes cluster (default: 'kubernetes_default').

### Request Example
{
  "kueue_version": "0.5.0",
  "kubernetes_conn_id": "my_k8s_cluster"
}

### Response
#### Success Response (200)
- **status** (string) - Installation status message.
```

--------------------------------

### GET /sdk/variables/{key}

Source: https://airflow.apache.org/docs/task-sdk/stable/api.html

Retrieve a variable value by its key.

```APIDOC
## GET /sdk/variables/{key}

### Description
Retrieves the value of a variable stored in the Airflow system.

### Method
GET

### Endpoint
/sdk/variables/{key}

### Parameters
#### Path Parameters
- **key** (str) - Required - The key of the variable to retrieve.

#### Query Parameters
- **deserialize_json** (bool) - Optional - Whether to deserialize the value from JSON.

### Response
#### Success Response (200)
- **value** (Any) - The retrieved variable value.

#### Response Example
{
  "value": "my_value"
}
```

--------------------------------

### Get Weaviate Collection

Source: https://airflow.apache.org/docs/apache-airflow-providers-weaviate/stable/_api/airflow/providers/weaviate/hooks/weaviate/index.html

Retrieves a collection from Weaviate by its name.

```python
collection = weaviate_hook.get_collection(name='my_collection')

```

--------------------------------

### GET /test_connection

Source: https://airflow.apache.org/docs/apache-airflow-providers-salesforce/stable/_api/airflow/providers/salesforce/hooks/salesforce/index.html

Verifies the current Salesforce connection configuration.

```APIDOC
## GET /test_connection

### Description
Tests the connectivity to the configured Salesforce instance to ensure credentials and endpoints are valid.

### Method
GET

### Endpoint
/test_connection

### Response
#### Success Response (200)
- **status** (string) - Indicates successful connection validation.
```