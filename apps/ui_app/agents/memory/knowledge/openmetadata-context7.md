### Install OpenMetadata Go Client SDK

Source: https://docs.open-metadata.org/api-reference

Install the OpenMetadata Go client SDK using the go get command. This provides a robust, type-safe API for Go applications.

```bash
go get github.com/open-metadata/openmetadata-sdk/openmetadata-go-client
```

--------------------------------

### Custom Helm Chart Installation with Values File

Source: https://docs.open-metadata.org/v1.12.x/deployment/kubernetes/on-prem

Example of how to install a Helm chart using a custom values file, allowing for specific configurations.

```command-line
helm install openmetadata-dependencies open-metadata/openmetadata-dependencies --values <path-to-values-file>
```

--------------------------------

### Quick Start: List Tables (Python)

Source: https://docs.open-metadata.org/api-reference

A Python example demonstrating how to configure the SDK and list tables in your OpenMetadata catalog. Ensure you replace placeholders with your actual host and JWT token.

```python
from metadata.sdk import configure, Tables

configure(host="https://your-company.open-metadata.org/api", jwt_token="your-jwt-token")

# List tables
for table in Tables.list().auto_paging_iterable():
    print(f"{table.fullyQualifiedName}: {table.description}")
```

--------------------------------

### Python Quick Start

Source: https://docs.open-metadata.org/api-reference

Get started with a simple API call to list tables in your catalog using the Python SDK.

```APIDOC
## Python Quick Start

Get started with a simple API call to list tables in your catalog:

```python
from metadata.sdk import configure, Tables

configure(host="https://your-company.open-metadata.org/api", jwt_token="your-jwt-token")

# List tables
for table in Tables.list().auto_paging_iterable():
    print(f"{table.fullyQualifiedName}: {table.description}")
```
```

--------------------------------

### Install Node and Yarn Versions

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/openmetadata-ui

Ensure you have the specified versions of Node.js and Yarn installed before proceeding with the UI setup.

```json
"node": ">=18.19.0",
"yarn": "^1.22.0"
```

--------------------------------

### Example Tool Versions on Macbook

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/prerequisites

This snapshot shows the expected output when checking the versions of various development tools on a Macbook, confirming successful installation.

```bash
> docker --version
Docker version 20.10.8, build 3967b7d

> java -version
openjdk version "21.0.7" 2025-04-15
OpenJDK Runtime Environment Homebrew (build 21.0.7)
OpenJDK 64-Bit Server VM Homebrew (build 21.0.7, mixed mode, sharing)

> antlr4
ANTLR Parser Generator  Version 4.9.2
 -o ___              specify output directory where all output is generated
 -lib ___            specify location of grammars, tokens files
 -atn                generate rule augmented transition network diagrams
 -encoding ___       specify grammar file encoding; e.g., euc-jp
 -message-format ___ specify output style for messages in antlr, gnu, vs2005
 -long-messages      show exception details when available for errors and warnings
 -listener           generate parse tree listener (default)
 -no-listener        don\'t generate parse tree listener
 -visitor            generate parse tree visitor
 -no-visitor         don\'t generate parse tree visitor (default)
 -package ___        specify a package/namespace for the generated code
 -depend             generate file dependencies
 -D<option>=value    set/override a grammar-level option
 -Werror             treat warnings as errors
 -XdbgST             launch StringTemplate visualizer on generated code
 -XdbgSTWait         wait for STViz to close before continuing
 -Xforce-atn         use the ATN simulator for all predictions
 -Xlog               dump lots of logging info to antlr-timestamp.log
 -Xexact-output-dir  all output goes into -o dir regardless of paths/package

> mvn -version
Apache Maven 3.9.9 (8e8579a9e76f7d015ee5ec7bfcdc97d260186937)
Maven home: /opt/homebrew/Cellar/maven/3.9.9/libexec
Java version: 23.0.2, vendor: Homebrew, runtime: /opt/homebrew/Cellar/openjdk/23.0.2/libexec/openjdk.jdk/Contents/Home
Default locale: en_IN, platform encoding: UTF-8
OS name: "mac os x", version: "15.5", arch: "aarch64", family: "mac"

>  make -version
GNU Make 3.81
Copyright (C) 2006  Free Software Foundation, Inc.
This is free software; see the source for copying conditions.
There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.

This program built for i386-apple-darwin11.3.0
> python --version
Python 3.10.17

> node --version
v22.0.0

> yarn --version
1.22.22

> rpm --version
RPM version 4.17.0

> jq --version
jq-1.7.1

```

--------------------------------

### List Tables using Go SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/getting-started

Use the Go SDK to fetch tables. This example demonstrates making a GET request and decoding the JSON response.

```go
resp, err := rest.Get("tables", map[string]string{"limit": "10"})
if err != nil {
    log.Fatal(err)
}
deferr resp.Body.Close()

var result struct {
    Data []struct {
        FullyQualifiedName string `json:"fullyQualifiedName"`
    } `json:"data"`
}
if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
    log.Fatal(err)
}

for _, table := range result.Data {
    fmt.Println(table.FullyQualifiedName)
}
```

--------------------------------

### Install OpenMetadata Go SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/go

Add the OpenMetadata SDK module to your Go application using the go get command.

```bash
go get github.com/open-metadata/openmetadata-sdk/openmetadata-go-client

```

--------------------------------

### Host and Port Configuration Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/lightdash

Specify the network location of your Lightdash instance using a URI format. Use http for local setups and https for server deployments.

```text
http://localhost:8080
```

```text
https://lightdash.example.com:3000
```

--------------------------------

### Start OpenMetadata UI Locally

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/openmetadata-ui

Start the OpenMetadata UI in development mode using this command.

```bash
# starting the UI locally
> make yarn_start_dev_ui
```

--------------------------------

### List Tables Example

Source: https://docs.open-metadata.org/v1.12.x/api-reference

Get started with a simple API call to list tables in your catalog.

```APIDOC
## List Tables

### Description
Lists tables in the data catalog.

### Method
GET

### Endpoint
/tables

### Query Parameters
- **limit** (integer) - Optional - The maximum number of tables to return.
- **fields** (string) - Optional - Comma-separated list of fields to return.
- **sort_by** (string) - Optional - Field to sort the results by.
- **sort_order** (string) - Optional - Order of sorting (asc or desc).

### Request Example
```bash
curl -X GET "https://your-company.open-metadata.org/api/v1/tables?limit=10" \
  -H "Authorization: Bearer your-jwt-token" \
  -H "Content-Type: application/json"
```

### Response
#### Success Response (200)
- **data** (array) - List of tables.
  - **fullyQualifiedName** (string) - The fully qualified name of the table.
  - **description** (string) - The description of the table.

#### Response Example
```json
{
  "data": [
    {
      "fullyQualifiedName": "my_database.my_schema.my_table",
      "description": "This is a sample table."
    }
  ]
}
```
```

```APIDOC
## List Tables (Python SDK)

### Description
Lists tables in the data catalog using the Python SDK.

### Method
SDK Method

### Code
```python
from metadata.sdk import configure, Tables

configure(host="https://your-company.open-metadata.org/api", jwt_token="your-jwt-token")

# List tables
for table in Tables.list().auto_paging_iterable():
    print(f"{table.fullyQualifiedName}: {table.description}")
```
```

```APIDOC
## List Tables (Java SDK)

### Description
Lists tables in the data catalog using the Java SDK.

### Method
SDK Method

### Code
```java
// Configure connection
OpenMetadataConfig config = OpenMetadataConfig.builder()
    .serverUrl("https://your-company.open-metadata.org/api")
    .accessToken("your-jwt-token")
    .build();

OpenMetadataClient client = new OpenMetadataClient(config);

// List tables
TablesApi tablesApi = client.buildClient(TablesApi.class);
TableList tables = tablesApi.listTables(null, 10, null, null, null);
for (Table table : tables.getData()) {
    System.out.println(table.getFullyQualifiedName());
}
```
```

--------------------------------

### Install Nginx

Source: https://docs.open-metadata.org/v1.12.x/deployment/security/enable-ssl/nginx

Installs Nginx on Ubuntu 20. Ensure Nginx is running after installation.

```bash
sudo apt update
sudo apt install nginx
sudo systemctl start nginx
```

--------------------------------

### Installation

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/overview

Install the OpenMetadata Python SDK using pip.

```APIDOC
pip install openmetadata-ingestion
```

--------------------------------

### Start Minikube Cluster (M1 Chip)

Source: https://docs.open-metadata.org/v1.12.x/quick-start/local-kubernetes-deployment

Starts a minikube cluster with specific configurations for MacOS M1 chipsets, ensuring compatibility with Docker Desktop as the container runtime. This is essential for OpenMetadata Helm Charts to install correctly.

```bash
minikube start --cpus=4 --memory=8192 --cni=bridge --driver=docker
```

--------------------------------

### Example 3: Include Databases Starting with 'SNOWFLAKE' or Ending with 'DB'

Source: https://docs.open-metadata.org/connectors/ingestion/workflows/metadata/filter-patterns/database

Use `^SNOWFLAKE.*` and `.*DB$` patterns to include databases that start with 'SNOWFLAKE' or end with 'DB'. This example demonstrates filtering via CLI.

```yaml
sourceConfig:
  config:
    ...
    useFqnForFiltering: false
    databaseFilterPattern:
      includes:
        - ^SNOWFLAKE.*
        - .*DB$

```

--------------------------------

### Docker Compose Version Output Example

Source: https://docs.open-metadata.org/v1.12.x/deployment/docker

Example output when checking the Docker Compose version.

```bash
Docker Compose version v2.2.3

```

--------------------------------

### Install Pre-commit Hooks and Development Dependencies

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/prerequisites

Set up pre-commit hooks for code style checks and install development dependencies by cloning the repository, creating a virtual environment, and running installation commands.

```bash
git clone https://github.com/open-metadata/OpenMetadata
cd openmetadata
python3 -m venv env
source env/bin/activate
pip install pre-commit
make install_dev
make install_test precommit_install

```

--------------------------------

### Install OpenMetadata

Source: https://docs.open-metadata.org/v1.12.x/deployment/kubernetes/aks

Install OpenMetadata using the Helm chart, referencing the `openmetadata-values.yaml` configuration file.

```bash
helm install openmetadata open-metadata/openmetadata \
  --values openmetadata-values.yaml \
  --namespace openmetadata
```

--------------------------------

### Example 2: Include Databases Starting with 'SNOWFLAKE'

Source: https://docs.open-metadata.org/connectors/ingestion/workflows/metadata/filter-patterns/database

Use the `^SNOWFLAKE.*` pattern to include databases whose names start with 'SNOWFLAKE'. This example demonstrates filtering via CLI.

```yaml
sourceConfig:
  config:
    ...
    useFqnForFiltering: false
    databaseFilterPattern:
      includes:
        - ^SNOWFLAKE.*

```

--------------------------------

### Install All Connector Modules

Source: https://docs.open-metadata.org/deployment/ingestion/openmetadata

Install the openmetadata-ingestion package with all connector plugins to support any connector. Replace `x.y.z` with your OpenMetadata server version.

```bash
pip3 install "openmetadata-ingestion[all]==x.y.z"
```

--------------------------------

### Install Playwright and Browsers

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/playwright-integration-tests

Navigate to the UI directory and install dependencies, then install Playwright browsers required for test execution.

```sh
cd openmetadata-ui/src/main/resources/ui
# Install dependencies (if not already done during UI setup)
yarn install
# Install Playwright browsers (required for running tests)
yarn playwright install

```

--------------------------------

### Set Up Python Development Environment

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/developing-a-new-connector/ai-assisted-development/install-skills

Create and activate a Python virtual environment, then install development dependencies and generate necessary code.

```bash
python3.11 -m venv env
source env/bin/activate
make install_dev generate
```

--------------------------------

### REST Metadata Ingestion UI Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/api/rest

Example usage of the MetadataIngestionUi component for the REST connector. This displays the step-by-step guide for setting up REST metadata ingestion.

```javascript
<MetadataIngestionUi connector={"REST"} selectServicePath={"/public/images/connectors/rest/select-service.png"} addNewServicePath={"/public/images/connectors/rest/add-new-service.png"} serviceConnectionPath={"/public/images/connectors/rest/service-connection.png"} />
```

--------------------------------

### Response for Get Sample Data

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/tables/sample-data

This is an example of the JSON response when retrieving sample data for a table.

```json
{
  "columns": [
    {"name": "agent_id", "dataType": "VARCHAR"},
    {"name": "performance_score", "dataType": "DECIMAL"}
  ],
  "rows": [
    ["AGT-001", 92.5],
    ["AGT-002", 87.3],
    ["AGT-003", 95.1]
  ]
}

```

--------------------------------

### Example openmetadata.yaml Configuration for Subpath

Source: https://docs.open-metadata.org/v1.12.x/deployment/bare-metal/subpath

This example shows a complete relevant section of the `openmetadata.yaml` file, demonstrating how to configure basePath, publicKeyUrl, web paths, and asset paths for subpath deployment.

```yaml
basePath: ${BASE_PATH:-/openmetadata}
publicKeyUrl: ${BASE_PATH:-/}api/v1/system/config/jwks

web:
  applicationContextPath: ${BASE_PATH:-/openmetadata}
  rootPath: ${BASE_PATH:-/openmetadata}api/*

assets:
  resourcePath: /openmetadata/assets/
  uriPath: ${BASE_PATH:-/openmetadata}
```

--------------------------------

### Install UI Dependencies

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/openmetadata-ui

Install the necessary dependencies for the OpenMetadata UI. This is a one-time task unless package.json changes.

```bash
# installing dependencies
> make yarn_install_cache
```

--------------------------------

### Example Airflow DAG

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/airflow/lineage-operator

An example DAG demonstrating the setup for using Airflow operators. This snippet includes necessary imports and basic DAG structure.

```python
#  Copyright 2025 OpenMetadata
#  Licensed under the OpenMetadata Community License, Version 1.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  https://github.com/open-metadata/OpenMetadata/blob/main/ingestion/LICENSE
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""
You can run this DAG from the default OM installation
"""

from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# These args will get passed on to each operator

```

--------------------------------

### Start OpenMetadata Server

Source: https://docs.open-metadata.org/v1.12.x/deployment/bare-metal

Run this command to start the OpenMetadata server. Consider using a process manager like 'serviced' for automatic restarts.

```bash
./bin/openmetadata.sh start
```

--------------------------------

### Create a Database Service (MySQL Example)

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/ingestion/lineage

Create a new database service instance, specifying the service type and connection details. This example uses a mocked MySQL instance.

```python
from metadata.sdk import DatabaseServices
from metadata.generated.schema.api.services.createDatabaseService import (
    CreateDatabaseServiceRequest,
)
from metadata.generated.schema.entity.services.connections.database.common.basicAuth import (
    BasicAuth,
)
from metadata.generated.schema.entity.services.connections.database.mysqlConnection import (
    MysqlConnection,
)
from metadata.generated.schema.entity.services.databaseService import (
    DatabaseConnection,
    DatabaseServiceType,
)

db_service = CreateDatabaseServiceRequest(
    name="test-service-db-lineage",
    serviceType=DatabaseServiceType.Mysql,
    connection=DatabaseConnection(
        config=MysqlConnection(
            username="username",
            authType=BasicAuth(password="password"),
            hostPort="http://localhost:1234",
        )
    ),
)

db_service_entity = DatabaseServices.create(db_service)

```

--------------------------------

### Install OpenMetadata Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/overview

Install the OpenMetadata Python SDK using pip. This command installs the necessary package for using the SDK.

```bash
pip install openmetadata-ingestion

```

--------------------------------

### Install SingleStore Connector

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/singlestore/yaml

Install the SingleStore connector for the OpenMetadata Ingestion Framework. This command installs the necessary packages for SingleStore ingestion.

```bash
pip3 install "openmetadata-ingestion[singlestore]"
```

--------------------------------

### Install DB2 Connector with Pip

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/db2

Install the DB2 connector using pip, specifying the OpenMetadata ingestion package with the DB2 extra. Ensure you use the appropriate version for your setup.

```bash
pip install 'openmetadata-ingestion[db2]==1.2.4.0'
```

--------------------------------

### Set up Development Environment for Sample Data Ingestion

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/openmetadata-server

Creates a virtual environment, installs development dependencies, and generates necessary files for ingesting sample data.

```bash
python3 -m venv venv
source venv/bin/activate
make install_dev generate
cd ingestion
pip install -e '.[sample-data, elasticsearch]'
```

--------------------------------

### Astronomer HostPort Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/airflow/rest-api-connection

Example of the hostPort parameter for an Astronomer deployment.

```text
https://<deployment-id>.ay.astronomer.run/<workspace>/
```

--------------------------------

### Install UI Dependencies

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/generate-typescript-types-from-json-schema

Navigate to the UI directory and install project dependencies using yarn.

```bash
cd openmetadata-ui/src/main/resources/ui
yarn install

```

--------------------------------

### Python Search Query Example

Source: https://docs.open-metadata.org/v1.12.x/api-reference/discovery/search

Use the OpenMetadata SDK to search for entities. Configure the client with your server details and JWT token, then make a GET request to the /search/query endpoint with your search parameters.

```python
from metadata.sdk import configure, get_client

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)
client = get_client()

# Search for tables matching "customer"
response = client.get("/search/query", params={
    "q": "customer",
    "index": "table_search_index",
    "from": 0,
    "size": 10
})

for hit in response["hits"]["hits"]:
    entity = hit["_source"]
    print(f"{entity['entityType']}: {entity['fullyQualifiedName']} (score: {hit['_score']})")
```

--------------------------------

### Set up Development Environment

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/developing-a-new-connector/ai-assisted-development/scaffold-connector

Before running the scaffold tool, set up the development environment by navigating to the OpenMetadata directory, creating a virtual environment, activating it, and installing development dependencies.

```bash
cd OpenMetadata
python3.11 -m venv env
source env/bin/activate
make install_dev generate

```

--------------------------------

### Quick Start: List Tables (Java)

Source: https://docs.open-metadata.org/v1.12.x/api-reference

Configure the Java SDK with server URL and access token. Build an OpenMetadataClient and use the TablesApi to retrieve a list of tables. Handles pagination.

```java
// Configure connection
OpenMetadataConfig config = OpenMetadataConfig.builder()
    .serverUrl("https://your-company.open-metadata.org/api")
    .accessToken("your-jwt-token")
    .build();

OpenMetadataClient client = new OpenMetadataClient(config);

// List tables
TablesApi tablesApi = client.buildClient(TablesApi.class);
TableList tables = tablesApi.listTables(null, 10, null, null, null);
for (Table table : tables.getData()) {
    System.out.println(table.getFullyQualifiedName());
}
```

--------------------------------

### List and Call MCP Tools with Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/ai-sdk

Demonstrates how to initialize the SDK, list available MCP tools, and call specific tools like 'search_metadata', 'get_entity_details', and 'get_entity_lineage'. Ensure the AISdkConfig is properly set up from environment variables.

```python
from ai_sdk import AISdk, AISdkConfig

config = AISdkConfig.from_env()
client = AISdk.from_config(config)

# List available tools
tools = client.mcp.list_tools()
for tool in tools:
    print(f"{tool.name}: {tool.description}")

# Search for tables
result = client.mcp.call_tool("search_metadata", {
    "query": "customers",
    "entity_type": "table",
    "limit": 5,
})
print(result.data)

# Get entity details
result = client.mcp.call_tool("get_entity_details", {
    "fqn": "sample_data.ecommerce_db.shopify.customers",
    "entity_type": "table",
})
print(result.data)

# Get lineage
result = client.mcp.call_tool("get_entity_lineage", {
    "entity_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "upstream_depth": 3,
    "downstream_depth": 2,
})
print(result.data)
```

--------------------------------

### Complete Example: Testing Customer Table

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/data-quality-observability/quality/data-quality-as-code/test-runner

A comprehensive example demonstrating the configuration of the SDK, creation of a TestRunner, definition of various table and column-level data quality tests, and execution of these tests.

```python
from metadata.sdk import configure
from metadata.sdk.data_quality import (
    TestRunner,
    TableRowCountToBeBetween,
    ColumnValuesToBeNotNull,
    ColumnValuesToBeUnique,
    ColumnValuesToMatchRegex,
    ColumnValuesToBeBetween
)

# Configure SDK
configure(
    host="http://localhost:8585/api",
    jwt_token="your-jwt-token"
)

# Create runner
runner = TestRunner.for_table("MySQL.ecommerce.public.customers")

# Define data quality tests
runner.add_tests(
    # Table should have between 1000 and 1M customers
    TableRowCountToBeBetween(min_count=1000, max_count=1000000),

    # Required fields must not be null
    ColumnValuesToBeNotNull(column="customer_id"),
    ColumnValuesToBeNotNull(column="email"),
    ColumnValuesToBeNotNull(column="created_at"),

    # Customer ID must be unique
    ColumnValuesToBeUnique(column="customer_id"),

    # Email must match valid pattern
    ColumnValuesToMatchRegex(
        column="email",
        regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    ),

    # Age should be reasonable
    ColumnValuesToBeBetween(column="age", min_value=18, max_value=120)
)

# Run tests
results = runner.run()
```

--------------------------------

### Install Python SDK

Source: https://docs.open-metadata.org/latest/sdk/python

Install the Python SDK using pip, ensuring the version matches your OpenMetadata server version. Use the '~=' operator for compatible versioning.

```bash
pip install "openmetadata-ingestion~=1.12.6.0"
```

--------------------------------

### Run OpenMetadata Server

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/openmetadata-server

Start the OpenMetadata server using the provided script and configuration file.

```bash
cd open-metadata-<version>
sh bin/openmetadata-server-start.sh conf/openmetadata.yaml
```

--------------------------------

### Airflow DAG with OpenMetadata Lineage Callbacks

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/airflow/lineage-backend

This example shows how to configure an Airflow DAG to use OpenMetadata's lineage callbacks for success and failure events. Ensure the `airflow_provider_openmetadata` is installed.

```python
from airflow_provider_openmetadata.lineage.callback import success_callback, failure_callback


default_args = {
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': failure_callback,
    'on_success_callback': success_callback,
}


def explode():
    raise Exception("I am an angry exception!")

with DAG(
    'lineage_tutorial',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:

    # t1, t2 and t3 are examples of tasks created by instantiating operators
    t1 = BashOperator(
        task_id='print_date',
        bash_command='date',
        outlets={
            "tables": ["mysql.default.openmetadata_db.bot_entity"]
        }
    )

    t2 = BashOperator(
        task_id='sleep',
        depends_on_past=False,
        bash_command='sleep 5',
        retries=3,
        inlets={
            "tables": ["snow.TEST.PUBLIC.COUNTRIES"]
        }
    )

    risen = PythonOperator(
        task_id='explode',
        provide_context=True,
        python_callable=explode,
        retries=0,
    )

    dag.doc_md = __doc__  # providing that you have a docstring at the beginning of the DAG
    dag.doc_md = """
    This is a documentation placed anywhere
    """  # otherwise, type it like this
    templated_command = dedent("")

    t3 = BashOperator(
        task_id='templated',
        depends_on_past=False,
        bash_command=templated_command,
        params={'my_param': 'Parameter I passed in'},
    )

    t1 >> [t2, t3]
```
```

--------------------------------

### Install Alation Sink Connector

Source: https://docs.open-metadata.org/v1.12.x/connectors/metadata/alationsink/yaml

Install the Alation Sink connector using pip. This command installs the necessary package for the OpenMetadata Ingestion Framework.

```bash
pip3 install "openmetadata-ingestion[alationsink]"
```

--------------------------------

### Enable Apache Site and Reload

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/dbt/storage-http-guide

Enable the Apache site configuration, create the artifact directory, set permissions, and reload the Apache service.

```bash
sudo a2ensite dbt-artifacts
sudo mkdir -p /var/www/dbt-artifacts
sudo chmod 755 /var/www/dbt-artifacts
sudo systemctl reload apache2

```

--------------------------------

### Get Lineage using cURL (Bash)

Source: https://docs.open-metadata.org/v1.12.x/api-reference/lineage/get

Examples using cURL to interact with the Lineage API. Demonstrates fetching lineage by ID or FQN, with options for custom depth and including deleted entities.

```bash
# Get lineage by entity type and ID
curl "{base_url}/api/v1/lineage/table/455e3d9d-dbbf-455e-b3be-7191daa825f3" \
  -H "Authorization: Bearer {access_token}"

# Get lineage with custom depth
curl "{base_url}/api/v1/lineage/table/455e3d9d-dbbf-455e-b3be-7191daa825f3?upstreamDepth=3&downstreamDepth=2" \
  -H "Authorization: Bearer {access_token}"

# Get lineage by fully qualified name
curl "{base_url}/api/v1/lineage/table/name/sample_data.ecommerce_db.shopify.dim_customer" \
  -H "Authorization: Bearer {access_token}"

# Get lineage including deleted entities
curl "{base_url}/api/v1/lineage/table/name/sample_data.ecommerce_db.shopify.dim_customer?includeDeleted=true&upstreamDepth=2&downstreamDepth=2" \
  -H "Authorization: Bearer {access_token}"

```

--------------------------------

### Validate Prerequisites Installation

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/prerequisites

Run this command to verify that all necessary tools for OpenMetadata development are correctly installed and configured.

```bash
make prerequisites

```

--------------------------------

### Enable Nginx Site and Reload

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/dbt/storage-http-guide

Enable the Nginx site configuration, create the artifact directory, set permissions, test the configuration, and reload Nginx.

```bash
sudo ln -s /etc/nginx/sites-available/dbt-artifacts /etc/nginx/sites-enabled/
sudo mkdir -p /var/www/dbt-artifacts
sudo chmod 755 /var/www/dbt-artifacts
sudo nginx -t
sudo systemctl reload nginx

```

--------------------------------

### Create setup.py for Custom Drive Connector

Source: https://docs.open-metadata.org/v1.12.x/connectors/drive/custom-drive

A minimal setup.py file is required to package your custom drive connector as a Python module.

```python
from setuptools import setup, find_packages

setup(
    name="custom_drive_connector",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
)
```

--------------------------------

### Install QuickSight Ingestion Package

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/quicksight/yaml

Install the OpenMetadata ingestion package with QuickSight support using pip. This command ensures all necessary dependencies for the QuickSight connector are installed.

```bash
pip3 install "openmetadata-ingestion[quicksight]"
```

--------------------------------

### Complete dbt_project.yml Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/dbt/auto-ingest-dbt-core

A comprehensive example of the dbt_project.yml file, demonstrating how to configure OpenMetadata settings using environment variables and optional parameters, along with filter patterns.

```yaml
# dbt_project.yml
name: 'my_analytics_project'
version: '1.0.0'
config-version: 2

profile: 'my_analytics_project'
model-paths: ["models"]
# ... other dbt settings ...

vars:
  # OpenMetadata Configuration - Using Environment Variables
  openmetadata_host_port: "${OPENMETADATA_HOST_PORT}"
  openmetadata_jwt_token: "{{ env_var('OPENMETADATA_JWT_TOKEN') }}"
  openmetadata_service_name: "{{ env_var('OPENMETADATA_JWT_TOKEN', 'postgres_analytics') }}"

  # Optional Settings
  openmetadata_dbt_update_descriptions: true
  openmetadata_dbt_update_owners: true
  openmetadata_include_tags: true
  openmetadata_dbt_classification_name: "{{ env_var('DBT_CLASSIFICATION', 'dbt_analytics_tags') }}"

  # Filtering
  openmetadata_database_filter_pattern:
    includes: ["analytics", "data_warehouse"]
    excludes: ["temp_db", "test_db"]

  openmetadata_table_filter_pattern:
    includes: [".*"]
    excludes: ["temp_.*", "tmp_.*", "test_.*"]
```

--------------------------------

### Install ANTLR CLI

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/openmetadata-ui

Install the ANTLR Command Line Interface using the provided make command.

```bash
sudo make install_antlr_cli
```

--------------------------------

### Install Kafka Plugin

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/ingestion-framework

Command to install the kafka plugin for the ingestion framework. This may encounter errors on macOS if librdkafka is not installed.

```bash
pip install "./ingestion[kafka]"
```

--------------------------------

### Install QlikCloud Ingestion

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/qlikcloud/yaml

Install the QlikCloud ingestion package using pip. This command installs the necessary dependencies for the QlikCloud connector.

```bash
pip3 install "openmetadata-ingestion[qlikcloud]"
```

--------------------------------

### Start OpenMetadata Server

Source: https://docs.open-metadata.org/v1.12.x/deployment/upgrade/bare-metal/steps

Restart the OpenMetadata server using the new release binaries after the migration is complete. This command starts the upgraded server.

```bash
./bin/openmetadata.sh start

```

--------------------------------

### Test Docker Compose Installation

Source: https://docs.open-metadata.org/v1.12.x/quick-start/local-docker-deployment

Confirm that Docker Compose is installed correctly and displays its version.

```bash
docker compose version
> Docker Compose version v2.2.3
```

--------------------------------

### List Data Products with Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/governance/data-products/list

Demonstrates how to list data products using the OpenMetadata Python SDK. Includes examples for basic listing, auto-pagination, and filtering by domain with specific fields. Ensure the SDK is configured with your host and JWT token.

```python
from metadata.sdk import configure
from metadata.sdk.entities import DataProducts

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# List first page
products = DataProducts.list(limit=50)
for dp in products.data:
    print(f"{dp.fullyQualifiedName}")

# List all with auto-pagination
for dp in DataProducts.list_all():
    print(f"{dp.fullyQualifiedName}")

# Filter by domain with fields
products = DataProducts.list(
    domain="Marketing",
    fields=["owners", "domain", "experts", "assets"],
    limit=50
)

for dp in products.data:
    print(f"{dp.fullyQualifiedName}")
    if dp.owners:
        print(f"  Owners: {[o.name for o in dp.owners]}")

```

--------------------------------

### Install ClickHouse Ingestion Dependencies

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/clickhouse/yaml

Install the OpenMetadata ingestion framework with ClickHouse support using pip. This command installs the base connector.

```bash
pip3 install "openmetadata-ingestion[clickhouse]"
```

--------------------------------

### Configure OpenMetadata Server for Airflow

Source: https://docs.open-metadata.org/v1.12.x/deployment/ingestion/openmetadata

Update the 'pipelineServiceClientConfiguration' in your 'openmetadata.yaml' file to connect to an Airflow instance. This example shows configuration for Bare Metal installations.

```yaml
# For Bare Metal Installations
[...] 

pipelineServiceClientConfiguration:
  className: ${PIPELINE_SERVICE_CLIENT_CLASS_NAME:-"org.openmetadata.service.clients.pipeline.airflow.AirflowRESTClient"}
  apiEndpoint: ${PIPELINE_SERVICE_CLIENT_ENDPOINT:-http://localhost:8080}
  metadataApiEndpoint: ${SERVER_HOST_API_URL:-http://localhost:8585/api}
  hostIp: ${PIPELINE_SERVICE_CLIENT_HOST_IP:-""}
  verifySSL: ${PIPELINE_SERVICE_CLIENT_VERIFY_SSL:-"no-ssl"} # Possible values are "no-ssl", "ignore", "validate"
  sslConfig:
    certificatePath: ${PIPELINE_SERVICE_CLIENT_SSL_CERT_PATH:-""} # Local path for the Pipeline Service Client

  # Default required parameters for Airflow as Pipeline Service Client
  parameters:
    username: ${AIRFLOW_USERNAME:-admin}
    password: ${AIRFLOW_PASSWORD:-admin}
    timeout: ${AIRFLOW_TIMEOUT:-10}

[...] 

```

--------------------------------

### Install Tableau Connector

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/tableau/yaml

Install the OpenMetadata Ingestion Framework with Tableau support using pip. This command installs the necessary packages for the Tableau connector.

```bash
pip3 install "openmetadata-ingestion[tableau]"
```

--------------------------------

### Install OpenMetadata Dependencies

Source: https://docs.open-metadata.org/v1.12.x/deployment/kubernetes/aks

Install the OpenMetadata dependencies using the Helm chart, referencing the `values-dependencies.yaml` file and disabling MySQL.

```bash
helm install openmetadata-dependencies open-metadata/openmetadata-dependencies \
  --values values-dependencies.yaml \
  --namespace openmetadata \
  --set mysql.enabled=false
```

--------------------------------

### Start PostgreSQL and OpenSearch with Docker

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/openmetadata-server

Use this command to set up PostgreSQL and OpenSearch for development using Docker Compose.

```bash
docker compose -f docker/development/docker-compose-postgres.yml up postgresql opensearch --build -d
```

--------------------------------

### Write New Playwright Integration Test

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/playwright-integration-tests

Create a new test file in the `playwright/e2e` directory. This example demonstrates basic setup, navigation, interaction, and assertion.

```typescript
import { test, expect } from "@playwright/test";

test.describe("Feature Name", () => {
  test.beforeEach(async ({ page }) => {
    // Setup code before each test
    await page.goto("/");
  });

  test("should perform expected behavior", async ({ page }) => {
    // Test implementation
    await page.click('button[data-testid="submit"]');
    await expect(page.locator(".success-message")).toBeVisible();
  });
});

```

--------------------------------

### Install and Configure NFS Server

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/dbt/storage-local-guide

Commands to install NFS server, create a shared directory, and configure exports on the NFS server.

```bash
# Install NFS server
sudo apt install -y nfs-kernel-server

# Create shared directory
sudo mkdir -p /export/dbt-artifacts
sudo chmod 777 /export/dbt-artifacts

# Configure exports
echo "/export/dbt-artifacts *(rw,sync,no_subtree_check,no_root_squash)" | \
    sudo tee -a /etc/exports

# Restart NFS
sudo systemctl restart nfs-kernel-server

```

--------------------------------

### TrustAll Configuration Example

Source: https://docs.open-metadata.org/v1.12.x/deployment/security/ldap/kubernetes

Example of configuring the TrustAll trust store for LDAP authentication, ensuring certificates are validated against their validity dates.

```yaml
openmetadata:
  config:
     ...
     authentication:
        ...
        ldapConfiguration:
           ...
           truststoreConfigType: TrustAll
           trustStoreConfig:
              examineValidityDates: true
  ...
```

--------------------------------

### Initialize the SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/getting-started

Configure the OpenMetadata client with your host and authentication token.

```APIDOC
## Initialize the SDK

### Description
Configure the OpenMetadata client with your host and authentication token.

### Python
```python
from metadata.sdk import configure

configure(host="https://your-company.open-metadata.org", jwt_token="your-jwt-token")
```

### Java
```java
import org.openmetadata.sdk.client.OpenMetadataClient;
import org.openmetadata.sdk.config.OpenMetadataConfig;

OpenMetadataConfig config = new OpenMetadataConfig(new URI("https://your-company.open-metadata.org"), "your-jwt-token");
OpenMetadataClient client = new OpenMetadataClient(config);
```

### Go
```go
import (
	"log"

	"github.com/open-metadata/openmetadata-connectors/openmetadata-sdk/go/clients"
)

restConfig := clients.NewRestConfig(
	"https://your-company.open-metadata.org",
	"", // APIVersion
	0,  // Retry -> defaults to 3
	0,  // RetryWait -> defaults to 30 seconds
	nil, // RetryCodes -> defaults to [429, 504]
	"your-jwt-token",
)
client, err := clients.NewRestClient(restConfig)
if err != nil {
	log.Fatal(err)
}
```

### cURL
```bash
# Set your token as an environment variable
export OPENMETADATA_TOKEN="your-jwt-token"
export OPENMETADATA_HOST="https://your-company.open-metadata.org/api/v1"
```
```

--------------------------------

### Databricks Pipeline Metadata Ingestion UI Component

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/databricks-pipeline

A React component to guide users through the metadata ingestion setup for the Databricks Pipeline connector in the OpenMetadata UI.

```javascript
export const MetadataIngestionUi = ({connector, selectServicePath, addNewServicePath, serviceConnectionPath}) => {
  return <Steps>
      <Step title="Visit the Services Page">
        Click `Settings` in the side navigation bar and then `Services`.

        The first step is to ingest the metadata from your sources. To do that, you first need to create a Service connection first.

        This Service will be the bridge between OpenMetadata and your source system.

        Once a Service is created, it can be used to configure your ingestion workflows.

        <img src="/public/images/connectors/visit-services-page.png" alt="Visit Services Page" />
      </Step>

      <Step title="Create a New Service">
        Click on _Add New Service_ to start the Service creation.

        <img src="/public/images/connectors/create-new-service.png" alt="Create a new Service" />
      </Step>

      <Step title="Select the Service Type">
        Select {connector} as the Service type and click _Next_.

        {selectServicePath && <img src={selectServicePath} alt="Select Service" />}
      </Step>

      <Step title="Name and Describe your Service">
        Provide a name and description for your Service.

        <h4>Service Name</h4>

        OpenMetadata uniquely identifies Services by their **Service Name**. Provide
        a name that distinguishes your deployment from other Services, including
        the other {connector} Services that you might be ingesting metadata
        from.

        Note that when the name is set, it cannot be changed.

        {addNewServicePath && <img src={addNewServicePath} alt="Add New Service" />}
      </Step>

      <Step title="Configure the Service Connection">
        In this step, we will configure the connection settings required for {connector}.

        Please follow the instructions below to properly configure the Service to read from your sources. You will also find
        helper documentation on the right-hand side panel in the UI.

        {serviceConnectionPath && <img src={serviceConnectionPath} alt="Configure Service connection" />}
      </Step>
    </Steps>;
};

<MetadataIngestionUi connector={"Databricks Pipeline"} selectServicePath={"/public/images/connectors/databricks-pipeline/select-service.png"} addNewServicePath={"public/images/connectors/databricks-pipeline/add-new-service.png"} serviceConnectionPath={"public/images/connectors/databricks-pipeline/service-connection.png"} />
```

--------------------------------

### Start Minikube Cluster

Source: https://docs.open-metadata.org/v1.12.x/quick-start/local-kubernetes-deployment

Starts a minikube cluster with specified resources. Use this command to initiate your local Kubernetes environment for OpenMetadata deployment.

```bash
minikube start --cpus=4 --memory=8192
```

--------------------------------

### Install BurstIQ Ingestion

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/burstiq/yaml

Install the BurstIQ ingestion package using pip. This command installs the necessary libraries for the BurstIQ connector.

```bash
pip3 install "openmetadata-ingestion[burstiq]"
```

--------------------------------

### Example Request and Response

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/messaging-services/retrieve

Example of how to retrieve a messaging service by name and the structure of the successful response.

```APIDOC
## Request Example
```python
import requests

base_url = "http://localhost:8585"
headers = {
    "Authorization": "Bearer YOUR_API_TOKEN"
}

response = requests.get(
    f"{base_url}/v1/services/messagingServices/name/sample_kafka",
    params={
        "fields": "owners,tags,domains"
    },
    headers=headers
)
```

## Response Example (200 OK)
```json
{
  "id": "469ef25e-9bdf-4d5f-8553-eb0ce8581f30",
  "name": "sample_kafka",
  "fullyQualifiedName": "sample_kafka",
  "serviceType": "Kafka",
  "connection": {
    "config": {
      "type": "Kafka",
      "bootstrapServers": "localhost:9092",
      "securityProtocol": "PLAINTEXT",
      "saslMechanism": "PLAIN",
      "schemaRegistryTopicSuffixName": "-value",
      "supportsMetadataExtraction": true
    }
  },
  "tags": [],
  "version": 0.1,
  "updatedAt": 1769982621031,
  "updatedBy": "admin",
  "href": "http://localhost:8585/api/v1/services/messagingServices/469ef25e-9bdf-4d5f-8553-eb0ce8581f30",
  "deleted": false,
  "owners": [],
  "domains": []
}
```
```

--------------------------------

### List Domains with Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/governance/domains/list

Demonstrates how to list domains using the Python SDK. Includes examples for basic listing, auto-pagination, and fetching specific fields.

```python
from metadata.sdk import configure
from metadata.sdk.entities import Domains

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# List first page
domains = Domains.list(limit=50)
for d in domains.data:
    print(f"{d.fullyQualifiedName} ({d.domainType})")

# List all with auto-pagination
for d in Domains.list_all():
    print(f"{d.fullyQualifiedName}")

# With fields
domains = Domains.list(
    fields=["owners", "children", "experts"],
    limit=50
)

for d in domains.data:
    print(f"{d.fullyQualifiedName}")
    if d.owners:
        print(f"  Owners: {[o.name for o in d.owners]}")

```

--------------------------------

### Airflow Standalone Startup Error

Source: https://docs.open-metadata.org/deployment/ingestion/openmetadata

This traceback shows the 'ValueError: The name 'template_blueprint' is already registered for this blueprint.' error that occurs when starting Airflow standalone on CentOS/Debian systems with openmetadata-managed-apis installed.

```bash
airflow standalone
standalone | Starting Airflow Standalone
standalone | Checking database is initialized
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
WARNI [airflow.models.crypto] empty cryptography key - values will not be stored encrypted.
standalone | Database ready
[2023-08-11 05:39:28,851] {manager.py:508} INFO - Created Permission View: can create on DAGs
[2023-08-11 05:39:28,910] {manager.py:508} INFO - Created Permission View: menu access on REST API Plugin
[2023-08-11 05:39:28,916] {manager.py:568} INFO - Added Permission menu access on REST API Plugin to role Admin
Traceback (most recent call last):
  File "/home/pmcevoy/airflow233/bin/airflow", line 8, in <module>
    sys.exit(main())
  File "/home/pmcevoy/airflow233/lib64/python3.9/site-packages/airflow/__main__.py", line 38, in main
    args.func(args)
  File "/home/pmcevoy/airflow233/lib64/python3.9/site-packages/airflow/cli/cli_parser.py", line 51, in command
    return func(*args, **kwargs)
  File "/home/pmcevoy/airflow233/lib64/python3.9/site-packages/airflow/cli/commands/standalone_command.py", line 48, in entrypoint
    StandaloneCommand().run()
  File "/home/pmcevoy/airflow233/lib64/python3.9/site-packages/airflow/cli/commands/standalone_command.py", line 64, in run
    self.initialize_database()
  File "/home/pmcevoy/airflow233/lib64/python3.9/site-packages/airflow/cli/commands/standalone_command.py", line 180, in initialize_database
    appbuilder = cached_app().appbuilder
  File "/home/pmcevoy/airflow233/lib64/python3.9/site-packages/airflow/www/app.py", line 158, in cached_app
    app = create_app(config=config, testing=testing)
  File "/home/pmcevoy/airflow233/lib64/python3.9/site-packages/airflow/www/app.py", line 140, in create_app
    init_plugins(flask_app)
  File "/home/pmcevoy/airflow233/lib64/python3.9/site-packages/airflow/www/extensions/init_views.py", line 141, in init_plugins
    app.register_blueprint(blue_print["blueprint"])
  File "/home/pmcevoy/airflow233/lib64/python3.9/site-packages/flask/scaffold.py", line 56, in wrapper_func
    return f(self, *args, **kwargs)
  File "/home/pmcevoy/airflow233/lib64/python3.9/site-packages/flask/app.py", line 1028, in register_blueprint
    blueprint.register(self, options)
  File "/home/pmcevoy/airflow233/lib64/python3.9/site-packages/flask/blueprints.py", line 305, in register
    raise ValueError(
ValueError: The name 'template_blueprint' is already registered for this blueprint. Use 'name=' to provide a unique name.

```

--------------------------------

### Qlik Cloud Connector Header Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/qlikcloud/yaml

Example usage of the ConnectorDetailsHeader component for the Qlik Cloud connector.

```javascript
<ConnectorDetailsHeader icon="/public/images/connectors/qlikcloud.webp" name="Qlik Cloud" stage="PROD" availableFeatures={[ "Projects", "Dashboards", "Charts", "Datamodels", "Lineage"]} unavailableFeatures={["Owners", "Tags"]} />
```

--------------------------------

### Install SAP HANA Connector

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/sap-hana/yaml

Install the SAP HANA connector using pip. This command installs the necessary packages for SAP HANA ingestion.

```bash
pip3 install "openmetadata-ingestion[sap-hana]"
```

--------------------------------

### Create GitHub Copilot Instructions File

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/developing-a-new-connector/ai-assisted-development/install-skills

Create a `.github/copilot-instructions.md` file at the repository root to guide GitHub Copilot on OpenMetadata connector development conventions.

```markdown
When working on OpenMetadata connectors, follow these conventions:

```

--------------------------------

### List Users with Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/teams-and-users/users/list

Demonstrates how to list users using the Python SDK. Includes examples for listing the first page, auto-pagination, filtering by team and fields, and filtering bot accounts.

```python
from metadata.sdk import configure
from metadata.sdk.entities import Users

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# List first page
users = Users.list(limit=50)
for user in users.data:
    print(f"{user.fullyQualifiedName}")

# List all with auto-pagination
for user in Users.list_all():
    print(f"{user.fullyQualifiedName}")

# Filter by team with fields
users = Users.list(
    team="Sales",
    fields=["teams", "roles", "domains"],
    limit=50
)

for user in users.data:
    print(f"{user.fullyQualifiedName}")
    if user.teams:
        print(f"  Teams: {[t.name for t in user.teams]}")
    if user.roles:
        print(f"  Roles: {[r.name for r in user.roles]}")

# Filter bot accounts
bots = Users.list(isBot=True, limit=50)

```

--------------------------------

### Extend OpenMetadata Ingestion Docker Image

Source: https://docs.open-metadata.org/v1.12.x/deployment/kubernetes/on-prem

Create a custom Dockerfile based on the official OpenMetadata ingestion image to include custom connectors or dependencies. This example shows how to install a Python package.

```dockerfile
FROM docker.open-metadata.org/openmetadata/ingestion:x.y.z

USER airflow
# Let's use the home directory of airflow user
WORKDIR /home/airflow

# Install our custom connector
COPY <your_package> <your_package>
COPY setup.py .
RUN pip install --no-deps .
```

--------------------------------

### Install OpenMetadata Ingestion Package

Source: https://docs.open-metadata.org/deployment/ingestion/openmetadata

Install the openmetadata-ingestion package with specific connector plugins. Replace `<connector-name>` with the desired connector and `x.y.z` with your OpenMetadata server version.

```bash
pip3 install "openmetadata-ingestion[<connector-name>]==x.y.z"
```

--------------------------------

### Install Power BI Ingestion Package

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/powerbi/yaml

Install the OpenMetadata ingestion package with Power BI support. This command installs the necessary dependencies to run the Power BI connector.

```bash
pip3 install "openmetadata-ingestion[powerbi]"
```

--------------------------------

### Start OpenMetadata Server Locally

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/openmetadata-ui

Spin up the OpenMetadata server locally by executing this script from the specified directory. Ensure you use the correct configuration file.

```bash
./bin/openmetadata-server-start.sh conf/openmetadata.yaml
```

--------------------------------

### Install OpenMetadata Helm Chart

Source: https://docs.open-metadata.org/v1.12.x/deployment/kubernetes/on-prem

Command to install the main OpenMetadata Helm chart after the dependencies chart has been deployed.

```command-line
helm install openmetadata open-metadata/openmetadata
```

--------------------------------

### Install Nginx

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/dbt/storage-http-guide

Install Nginx on Ubuntu/Debian, CentOS/RHEL, or macOS. Nginx will serve dbt artifacts as a static file server.

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y nginx

# CentOS/RHEL
sudo yum install -y nginx

# macOS
brew install nginx

```

--------------------------------

### Install SageMaker Ingestion Package

Source: https://docs.open-metadata.org/v1.12.x/connectors/ml-model/sagemaker/yaml

Install the SageMaker connector package using pip. This command installs the necessary dependencies for the SageMaker ingestion workflow.

```bash
pip3 install "openmetadata-ingestion[sagemaker]"
```

--------------------------------

### Quick Start: List Tables (cURL)

Source: https://docs.open-metadata.org/v1.12.x/api-reference

Use cURL to make a GET request to the tables endpoint, including your JWT Bearer token in the Authorization header. Specify the desired limit for the number of results.

```bash
curl -X GET "https://your-company.open-metadata.org/api/v1/tables?limit=10" \
    -H "Authorization: Bearer your-jwt-token" \
    -H "Content-Type: application/json"
```

--------------------------------

### Google Cloud Composer HostPort Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/airflow/rest-api-connection

Example of the hostPort parameter for a Google Cloud Composer deployment.

```text
https://<hash>-dot-<region>.composer.googleusercontent.com
```

--------------------------------

### Install Apache

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/dbt/storage-http-guide

Install Apache HTTP Server on Ubuntu/Debian or CentOS/RHEL. This server will be configured to host dbt artifacts.

```bash
# Ubuntu/Debian
sudo apt install -y apache2

# CentOS/RHEL
sudo yum install -y httpd

```

--------------------------------

### Airbyte Metadata Ingestion UI Usage

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/airbyte

Instantiates the MetadataIngestionUi component for the Airbyte connector, providing specific image paths for the UI flow. This component is used to guide users through the Airbyte service setup within OpenMetadata.

```javascript
<MetadataIngestionUi connector={"Airbyte"} selectServicePath={"/public/images/connectors/airbyte/select-service.png"} addNewServicePath={"public/images/connectors/airbyte/add-new-service.png"} serviceConnectionPath={"/public/images/connectors/airbyte/service-connection.png"} />
```

--------------------------------

### Amazon MWAA HostPort Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/airflow/rest-api-connection

Example of the hostPort parameter for an Amazon MWAA deployment.

```text
https://<id>.c2.airflow.<region>.on.aws
```

--------------------------------

### Airflow DAG for OpenMetadata Ingestion (Python Operator)

Source: https://docs.open-metadata.org/v1.12.x/deployment/ingestion/external/airflow

Example DAG using Airflow's PythonOperator to run an OpenMetadata ingestion workflow. Ensure the 'openmetadata-ingestion' package is installed in your Airflow environment. The YAML configuration should be defined within the 'config' variable.

```python
import yaml
from datetime import timedelta
from airflow import DAG

try:
    from airflow.operators.python import PythonOperator
except ModuleNotFoundError:
    from airflow.operators.python_operator import PythonOperator

from metadata.config.common import load_config_file
from metadata.workflow.metadata import MetadataWorkflow


from airflow.utils.dates import days_ago

default_args = {
    "owner": "user_name",
    "email": ["username@org.com"],
    "email_on_failure": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(minutes=60)
}

config = """
<your YAML configuration>
"""

def metadata_ingestion_workflow():
    workflow_config = yaml.safe_load(config)
    workflow = MetadataWorkflow.create(workflow_config)
    workflow.execute()
    workflow.raise_from_status()
    workflow.print_status()
    workflow.stop()

with DAG(
    "sample_data",
    default_args=default_args,
    description="An example DAG which runs a OpenMetadata ingestion workflow",
    start_date=days_ago(1),
    is_paused_upon_creation=False,
    schedule_interval='*/5 * * * *',
    catchup=False,
) as dag:
    ingest_task = PythonOperator(
        task_id="ingest_using_recipe",
        python_callable=metadata_ingestion_workflow,
    )


```

--------------------------------

### Install DynamoDB Connector Package

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/dynamodb/yaml

Install the OpenMetadata ingestion package with DynamoDB support using pip. This command installs the necessary libraries to run the DynamoDB ingestion workflow.

```bash
pip3 install "openmetadata-ingestion[dynamodb]"
```

--------------------------------

### SingleStore Connector Header Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/singlestore

Example usage of the ConnectorDetailsHeader component for the SingleStore connector.

```typescript
<ConnectorDetailsHeader icon="/public/images/connectors/singlestore.webp" name="SingleStore" stage="PROD" availableFeatures={["Metadata", "Data Profiler", "Data Quality", "View Lineage", "View Column-level Lineage", "dbt", "Sample Data", "Auto-Classification"]} unavailableFeatures={["Query Usage", "Stored Procedures", "Owners", "Tags"]} />
```

--------------------------------

### Great Expectations 1.x.x Integration with OpenMetadataValidationAction1xx

Source: https://docs.open-metadata.org/v1.12.x/connectors/ingestion/great-expectations

Example for integrating Great Expectations v1.x.x with OpenMetadata using the OpenMetadataValidationAction1xx. This requires installing the `open-metadata[great-expectations-1xx]` package. The code demonstrates setting up a data source, asset, expectation suite, validation definition, and a checkpoint with the action.

```python
import great_expectations as gx

from metadata.great_expectations.action1xx import OpenMetadataValidationAction1xx # OpenMetadata Validation Action for GX 1.x.x


context = gx.get_context()
conn_string = f"redshift+psycopg2://user:pw@host:port/db"

data_source = context.data_sources.add_redshift(
    name="name",
    connection_string=conn_string,
)

data_asset = data_source.add_table_asset(
    name="name",
    table_name="table_name",
    schema_name="schema_name",
)

batch_definition = data_asset.add_batch_definition_whole_table("batch definition")
batch = batch_definition.get_batch()

suite = context.suites.add(
    gx.core.expectation_suite.ExpectationSuite(name="name")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="column_name"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(column="column_name", min_value=50, max_value=1000000)
)

validation_definition = context.validation_definitions.add(
    gx.core.validation_definition.ValidationDefinition(
        name="validation definition",
        data=batch_definition,
        suite=suite,
    )
)

action_list = [
    OpenMetadataValidationAction1xx(
        database_service_name="openmetadata_service_name",
        database_name="openmetadata_database_name",
        table_name="openmetadata_table_name",
        schema_name="openmetadata_schema_name",
        config_file_path="path/to/config/file",
    )
]

checkpoint = context.checkpoints.add(
    gx.checkpoint.checkpoint.Checkpoint(
        name="checkpoint", validation_definitions=[validation_definition], actions=action_list
    )
)

checkpoint_result = checkpoint.run()
```

--------------------------------

### Example Docker ps Output

Source: https://docs.open-metadata.org/latest/quick-start/local-docker-deployment

This is an example of the output you might see when running `docker ps`, indicating that the OpenMetadata server, ingestion container, Elasticsearch, and the database (MySQL in this case) are up and running.

```text
CONTAINER ID   IMAGE                                                  COMMAND                  CREATED          STATUS                    PORTS                                                            NAMES
470cc8149826   openmetadata/server:1.12.6                             "./openmetadata-star…"   45 seconds ago   Up 43 seconds             3306/tcp, 9200/tcp, 9300/tcp, 0.0.0.0:8585-8586->8585-8586/tcp   openmetadata_server
63578aacbff5   openmetadata/ingestion:1.12.6                           "./ingestion_depende…"   45 seconds ago   Up 43 seconds             0.0.0.0:8080->8080/tcp                                           openmetadata_ingestion
9f5ee8334f4b   docker.elastic.co/elasticsearch/elasticsearch:7.16.3   "/tini -- /usr/local…"   45 seconds ago   Up 44 seconds             0.0.0.0:9200->9200/tcp, 0.0.0.0:9300->9300/tcp                   openmetadata_elasticsearch
08947ab3424b   openmetadata/db:1.12.6                                  "/entrypoint.sh mysq…"   45 seconds ago   Up 44 seconds (healthy)   3306/tcp, 33060-33061/tcp                                        openmetadata_mysql

```

--------------------------------

### Airbyte Connector Example Usage

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/airbyte/yaml

Example of how to use the ConnectorDetailsHeader component to display information for the Airbyte connector.

```javascript
<ConnectorDetailsHeader icon="/public/images/connectors/airbyte.webp" name="Airbyte" stage="PROD" availableFeatures={["Pipelines", "Pipeline Status", "Lineage", "Usage"]} unavailableFeatures={["Owners", "Tags"]} />
```

--------------------------------

### Install Development Dependencies

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/ingestion-framework

Run these commands to prepare your Python development environment for the Ingestion Framework. Ensure Python 3.10+ is installed.

```bash
make install_dev
sudo make install_antlr_cli
make generate

```

--------------------------------

### Redpanda Metadata Ingestion UI Component

Source: https://docs.open-metadata.org/v1.12.x/connectors/messaging/redpanda

A React component that guides users through the Redpanda metadata ingestion setup process in the OpenMetadata UI, including steps for visiting the services page, creating a new service, selecting the service type, naming the service, and configuring connection settings.

```javascript
export const MetadataIngestionUi = ({connector, selectServicePath, addNewServicePath, serviceConnectionPath}) => {
  return <Steps>
      <Step title="Visit the Services Page">
        Click `Settings` in the side navigation bar and then `Services`.

        The first step is to ingest the metadata from your sources. To do that, you first need to create a Service connection first.

        This Service will be the bridge between OpenMetadata and your source system.

        Once a Service is created, it can be used to configure your ingestion workflows.

        <img src="/public/images/connectors/visit-services-page.png" alt="Visit Services Page" />
      </Step>

      <Step title="Create a New Service">
        Click on _Add New Service_ to start the Service creation.

        <img src="/public/images/connectors/create-new-service.png" alt="Create a new Service" />
      </Step>

      <Step title="Select the Service Type">
        Select {connector} as the Service type and click _Next_.

        {selectServicePath && <img src={selectServicePath} alt="Select Service" />}
      </Step>

      <Step title="Name and Describe your Service">
        Provide a name and description for your Service.

        <h4>Service Name</h4>

        OpenMetadata uniquely identifies Services by their **Service Name**. Provide
        a name that distinguishes your deployment from other Services, including
        the other {connector} Services that you might be ingesting metadata
        from.

        Note that when the name is set, it cannot be changed.

        {addNewServicePath && <img src={addNewServicePath} alt="Add New Service" />}
      </Step>

      <Step title="Configure the Service Connection">
        In this step, we will configure the connection settings required for {connector}.

        Please follow the instructions below to properly configure the Service to read from your sources. You will also find
        helper documentation on the right-hand side panel in the UI.

        {serviceConnectionPath && <img src={serviceConnectionPath} alt="Configure Service connection" />}
      </Step>
    </Steps>;
};

<MetadataIngestionUi connector={"Redpanda"} selectServicePath={"/public/images/connectors/redpanda/select-service.png"} addNewServicePath={"/public/images/connectors/redpanda/add-new-service.png"} serviceConnectionPath={"/public/images/connectors/redpanda/service-connection.png"} />
```

--------------------------------

### Start Docker Compose with Okta Environment File

Source: https://docs.open-metadata.org/v1.12.x/deployment/security/okta/docker

Use this command to start your Docker Compose services, applying the Okta configuration from the specified environment file. Ensure the path to your `.env` file is correct.

```bash
docker compose --env-file ~/openmetadata_okta.env up -d

```

--------------------------------

### Install OpenMetadata Ingestion Package

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/data-quality-observability/quality/data-quality-as-code/getting-started

Install the basic openmetadata-ingestion package. Ensure you are using version 1.12.0.0 or higher.

```bash
pip install "openmetadata-ingestion>=1.12.0.0"
```

--------------------------------

### Full Airflow DAG Example with Inlets and Outlets

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/airflow/lineage-backend

A complete Airflow DAG example demonstrating how to define both 'inlets' and 'outlets' for tasks. Ensure the FQNs provided for inlets and outlets correspond to existing assets in OpenMetadata.

```python
from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# These args will get passed on to each operator

```

--------------------------------

### Qlik Sense YAML Configuration Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/qliksense/yaml

This is a sample YAML configuration for connecting to Qlik Sense. It includes essential parameters like hostPort, displayUrl, and authentication details.

```yaml
source:
  type: qlik-sense
serviceName: "my-qlik-sense"
serviceConnection:
  config:
    hostPort: "wss://server.domain.com:4747"
    displayUrl: "https://server.domain.com"
    clientCertificate: "/path/to/client.pem"
    clientKeyCertificate: "/path/to/client_key.pem"
    rootCertificate: "/path/to/root.pem"
    userId: "admin"
    userDirectory: "qlik"
    validateHostName: true
    sourceConfig:
      enableDashboardMetadata: true
      enableChartMetadata: true
      enableDataModelMetadata: true
      enableLineage: true
      dashboardFilterPattern: "My Dashboard, My Dash.*, .*Dashboard"
      chartFilterPattern: "My Chart, My Chart.*, .*Chart"
      dataModelFilterPattern: "My Data Model, My Data.*, .*Data Model"
      projectFilterPattern: "My Project, My Proj.*, .*Project"
      includeOwners: true
```

--------------------------------

### Complete Profiler YAML Example: Before (Native Engine)

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/data-quality-observability/profiler/spark-engine/configuration/external-configuration

This is an example of a profiler configuration using the native engine, serving as a baseline before migrating to Spark.

```yaml
sourceConfig:
  config:
    type: Profiler
    schemaFilterPattern:
      includes:
        - ^your_schema$
    tableFilterPattern:
      includes:
        - your_table_name

processor:
  type: orm-profiler
  config: {}
```

--------------------------------

### Install OpenMetadata Ingestion Package

Source: https://docs.open-metadata.org/v1.12.x/deployment/ingestion/external/airflow

Install the openmetadata-ingestion package with specific plugins and version. Replace <plugin> with your sources (e.g., mysql, snowflake) and x.y.z with your OpenMetadata server version.

```bash
pip3 install openmetadata-ingestion[<plugin>]==x.y.z

```

```bash
pip3 install openmetadata-ingestion[mysql,snowflake,s3]==1.6.1

```

--------------------------------

### Install OpenMetadata Ingestion Package

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/dbt/auto-ingest-dbt-core

Install the OpenMetadata ingestion package with dbt support using pip.

```bash
pip install "openmetadata-ingestion[dbt]"
```

--------------------------------

### Install OpenMetadata Ingestion Packages

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/data-quality-observability/profiler/external-workflow

Install the necessary packages for the openmetadata-ingestion framework, including connector-specific plugins and data lake/trino support. Replace `<connector>` with the actual connector name.

```bash
pip install "openmetadata-ingestion[<connector>,datalake,trino]~=1.2.1"

```

```bash
pip install "openmetadata-ingestion[athena,datalake,trino]~=1.2.1"

```

--------------------------------

### Install Redshift Ingestion Package

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/redshift/yaml

Install the openmetadata-ingestion package with Redshift support using pip.

```bash
pip3 install "openmetadata-ingestion[redshift]"
```

--------------------------------

### Kafka Connector Header Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/messaging/kafka/yaml

Example usage of the ConnectorDetailsHeader component for the Kafka connector.

```jsx
<ConnectorDetailsHeader icon="/public/images/connectors/kafka.webp" name="Kafka" stage="PROD" availableFeatures={["Topics", "Sample Data"]} unavailableFeatures={[]} />
```

--------------------------------

### Install Teradata Ingestion

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/teradata/yaml

Install the necessary package for Teradata ingestion using pip.

```bash
pip3 install "openmetadata-ingestion[teradata]"
```

--------------------------------

### Start OpenMetadata with MySQL

Source: https://docs.open-metadata.org/v1.12.x/quick-start/local-docker-deployment

Run this command to deploy OpenMetadata and its dependencies using the MySQL docker-compose file. Ensure the docker-compose.yml file is in your current directory.

```bash
docker compose -f docker-compose.yml up --detach
```

--------------------------------

### Example Usage of ConnectorDetailsHeader

Source: https://docs.open-metadata.org/v1.12.x/connectors/search/opensearch/yaml

An example of how to use the ConnectorDetailsHeader component to display information for the OpenSearch connector.

```javascript
<ConnectorDetailsHeader icon="/public/images/connectors/opensearch.webp" name="OpenSearch" stage="PROD" availableFeatures={["Search Indexes", "Sample Data"]} unavailableFeatures={[]} />
```

--------------------------------

### HostName Configuration Example

Source: https://docs.open-metadata.org/v1.12.x/deployment/security/ldap/kubernetes

Example of configuring the HostName trust store for LDAP authentication, specifying acceptable hostnames and disabling wildcard matching.

```yaml
openmetadata:
  config:
     ...
     authentication:
        ...
        ldapConfiguration:
           ...
           truststoreConfigType: HostName
           trustStoreConfig:
              hostNameConfig:
              allowWildCards: false
              acceptableHostNames: [localhost]
  ...
```

--------------------------------

### Create Cursor Skills Directory and Copy Files

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/developing-a-new-connector/ai-assisted-development/install-skills

Set up the necessary directory structure and copy the skill files into the `.cursor/skills` directory for Cursor integration.

```bash
mkdir -p .cursor/skills
cp -r skills/standards .cursor/skills/
cp skills/connector-building/SKILL.md .cursor/skills/connector-building.md
cp skills/connector-review/SKILL.md .cursor/skills/connector-review.md
cp skills/load-standards/SKILL.md .cursor/skills/load-standards.md
```

--------------------------------

### Install Flink Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/flink/yaml

Install the necessary Python package for Flink ingestion. This command ensures all dependencies for the Flink connector are installed.

```bash
pip3 install "openmetadata-ingestion[flink]"
```

--------------------------------

### Start OpenMetadata with Google SSO

Source: https://docs.open-metadata.org/v1.12.x/deployment/security/google/docker

Use Docker Compose to start your OpenMetadata services, applying the environment variables defined in the `openmetadata_google.env` file. This command ensures the server runs with the specified Google SSO configuration.

```bash
docker compose --env-file ~/openmetadata_google.env up -d

```

--------------------------------

### Example Docker ps Output

Source: https://docs.open-metadata.org/v1.12.x/deployment/docker

This is an example output of the `docker ps` command, showing the running OpenMetadata server container with its ID, image, status, ports, and name.

```text
❯ docker ps
CONTAINER ID   IMAGE                                                  COMMAND                  CREATED          STATUS                    PORTS                                                            NAMES
470cc8149826   openmetadata/server:1.12.6                              "./openmetadata-star…"   45 seconds ago   Up 43 seconds             3306/tcp, 9200/tcp, 9300/tcp, 0.0.0.0:8585-8586->8585-8586/tcp   openmetadata_server
```

--------------------------------

### Clone and Open OpenMetadata Repository

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/development-environment-setup

Clone the OpenMetadata repository and open it in VS Code to begin setup.

```bash
git clone https://github.com/<username>/OpenMetadata.git
code OpenMetadata
```

--------------------------------

### Configure SDK and Create TestRunner

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/data-quality-observability/quality/data-quality-as-code/test-runner

Configure the SDK with your OpenMetadata host and JWT token, then create a TestRunner instance for a specific table using its fully qualified name (FQN).

```python
from metadata.sdk import configure
from metadata.sdk.data_quality import TestRunner

# Configure SDK first
configure(
    host="http://localhost:8585/api",
    jwt_token="your-jwt-token"
)

# Create runner for a table
runner = TestRunner.for_table("MySQL.ecommerce.public.customers")
```

--------------------------------

### Example Usage of ConnectorDetailsHeader

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/redash/yaml

An example of how to use the ConnectorDetailsHeader component to display Redash connector information.

```jsx
<ConnectorDetailsHeader icon="/public/images/connectors/redash.webp" name="Redash" stage="PROD" availableFeatures={["Dashboards", "Charts", "Lineage", "Owners", "Tags"]} unavailableFeatures={["Datamodels", "Projects"]} />
```

--------------------------------

### Install Delta Lake Connector for Metastore Extraction

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/deltalake/yaml

Install the OpenMetadata Ingestion Framework with Delta Lake support for extracting metadata from a metastore.

```bash
pip3 install "openmetadata-ingestion[deltalake-spark]"
```

--------------------------------

### Install OpenMetadata Kinesis Ingestion

Source: https://docs.open-metadata.org/v1.12.x/connectors/messaging/kinesis/yaml

Install the OpenMetadata ingestion package with Kinesis support. This command installs the necessary libraries to run the Kinesis connector.

```bash
pip3 install "openmetadata-ingestion[kinesis]"
```

--------------------------------

### Add Lineage with Column Details and SQL

Source: https://docs.open-metadata.org/v1.12.x/api-reference/lineage/add

This example demonstrates creating lineage with detailed column mappings and the SQL query that drives the transformation. It also includes associating the lineage with a specific pipeline.

```python
from metadata.generated.schema.entity.data.table import Table
from metadata.generated.schema.type.entityReference import EntityReference
from metadata.generated.schema.api.lineage.addLineage import AddLineageRequest
from metadata.generated.schema.type.entityLineage import (
    ColumnLineage,
    EntitiesEdge,
    LineageDetails,
)
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import (
    OpenMetadataConnection,
)
from metadata.generated.schema.security.client.openMetadataJWTClientConfig import (
    OpenMetadataJWTClientConfig,
)

server_config = OpenMetadataConnection(
    hostPort="https://your-company.open-metadata.org/api",
    authProvider="openmetadata",
    securityConfig=OpenMetadataJWTClientConfig(
        jwtToken="<YOUR-JWT-TOKEN>"
    ),
)
metadata = OpenMetadata(server_config)

# With column-level lineage and SQL query
column_lineage = ColumnLineage(
    fromColumns=["service.db.schema.source_table.customer_id"],
    toColumn="service.db.schema.target_table.cust_id",
)

lineage_details = LineageDetails(
    sqlQuery="INSERT INTO target_table SELECT customer_id FROM source_table",
    columnsLineage=[column_lineage],
    pipeline=EntityReference(id=pipeline_entity.id, type="pipeline"),
)

add_lineage_request = AddLineageRequest(
    edge=EntitiesEdge(
        fromEntity=EntityReference(id=source_table.id, type="table"),
        toEntity=EntityReference(id=target_table.id, type="table"),
        lineageDetails=lineage_details,
    ),
)
created_lineage = metadata.add_lineage(data=add_lineage_request)
```

--------------------------------

### Render QuickSight Connector Header Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/quicksight

This is an example of how to use the ConnectorDetailsHeader component to display information for the QuickSight connector. It specifies the icon, name, stage, and feature list.

```javascript
<ConnectorDetailsHeader icon="/public/images/connectors/quicksight.webp" name="QuickSight" stage="PROD" availableFeatures={["Dashboards", "Charts", "Lineage", "Datamodels"]} unavailableFeatures={["Owners", "Tags", "Projects"]} />
```

--------------------------------

### Build and Test OpenMetadata Server

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/openmetadata-server

Compile the project and run all tests. Use -DskipTests to skip tests if only building.

```bash
mvn clean install
```

--------------------------------

### Install Salesforce Connector

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/salesforce/yaml

Install the Salesforce connector using pip. Ensure you are using a supported Python version (3.9-3.11).

```bash
pip3 install "openmetadata-ingestion[salesforce]"
```

--------------------------------

### List Charts with Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/charts/list

Demonstrates how to list charts using the Python SDK. Includes examples for fetching the first page, listing all charts with auto-pagination, and filtering by service.

```python
from metadata.sdk import configure
from metadata.sdk.entities import Charts

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# List first page
charts = Charts.list(limit=50)
for c in charts.data:
    print(f"{c.fullyQualifiedName}")

# List all with auto-pagination
for c in Charts.list_all():
    print(f"{c.fullyQualifiedName}")

# Filter by service
charts = Charts.list(
    service="sample_superset",
    fields=["owners", "tags", "domains"],
    limit=50
)

for c in charts.data:
    print(f"{c.fullyQualifiedName} ({c.chartType})")
    if c.owners:
        print(f"  Owners: {[o.name for o in c.owners]}")
    if c.tags:
        print(f"  Tags: {[t.tagFQN for t in c.tags]}")

```

--------------------------------

### Start OpenMetadata Docker Compose with Keycloak

Source: https://docs.open-metadata.org/v1.12.x/deployment/security/keycloak/docker

Execute this command to start your OpenMetadata services using Docker Compose, applying the configurations from your `openmetadata_keycloak.env` file.

```bash
docker compose --env-file ~/openmetadata_keycloak.env up -d

```

--------------------------------

### Start OpenMetadata with MySQL Docker Compose

Source: https://docs.open-metadata.org/latest/quick-start/local-docker-deployment

Use this command to deploy OpenMetadata with a MySQL database. It pulls necessary Docker images and starts the services in detached mode.

```bash
docker compose -f docker-compose.yml up --detach 
```

--------------------------------

### Install librdkafka on macOS

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/ingestion-framework

Command to install the librdkafka library using Homebrew, often required to resolve build errors when installing the kafka plugin on macOS.

```bash
brew install librdkafka
```

--------------------------------

### Install Airflow Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/airflow/yaml

Install the necessary Python package for Airflow ingestion. This command installs the Airflow plugin along with the core ingestion framework.

```bash
pip3 install "openmetadata-ingestion[airflow]"
```

--------------------------------

### Bootstrap OpenMetadata Database

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/openmetadata-server

Extract the distribution tar.gz and run this script to set up the database. It handles Java dependencies, configurations, and environment variables.

```bash
cd open-metadata-<version>
sh bootstrap/openmetadata-ops.sh drop-create
```

--------------------------------

### Initialize REST Client Configuration

Source: https://docs.open-metadata.org/v1.12.x/api-reference/getting-started

Configure the REST client with your OpenMetadata instance URL, API version, retry settings, and authentication token.

```go
import (
	"log"

	"github.com/open-metadata/openmetadata-connectors/openmetadata-sdk/go/openmetadata/sdk"
)

func main() {
	restConfig := sdk.ClientConfig{
		Host: "https://your-company.open-metadata.org",
		APIVersion: "",  // APIVersion
		Retry: 0,   // Retry -> defaults to 3
		RetryWait: 0,   // RetryWait -> defaults to 30 seconds
		RetryCodes: nil, // RetryCodes -> defaults to [429, 504]
		Token: "your-jwt-token",
	}
	client, err := sdk.NewREST(restConfig)
	if err != nil {
		log.Fatalf("Failed to create REST client: %v", err)
	}
	// Use the client for API calls
	_ = client
}
```

--------------------------------

### Install Delta Lake Connector for Direct Storage Extraction

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/deltalake/yaml

Install the OpenMetadata Ingestion Framework with Delta Lake support for extracting metadata directly from storage.

```bash
pip3 install "openmetadata-ingestion[deltalake-storage]"
```

--------------------------------

### Install MSSQL Ingestion Package

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/mssql/yaml

Install the OpenMetadata Ingestion package with MSSQL support using pip. This command ensures all necessary dependencies for MSSQL ingestion are installed.

```bash
pip3 install "openmetadata-ingestion[mssql]"
```

--------------------------------

### Prepare the OpenMetadata Client

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/ingestion/tags

Initializes the OpenMetadata client with server connection details and authentication. Ensure the server is reachable by checking its health.

```python
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import (
    OpenMetadataConnection,
)
from metadata.generated.schema.security.client.openMetadataJWTClientConfig import (
    OpenMetadataJWTClientConfig,
)
from metadata.ingestion.ometa.ometa_api import OpenMetadata

server_config = OpenMetadataConnection(
    hostPort="http://localhost:8585/api",
    authProvider="openmetadata",
    securityConfig=OpenMetadataJWTClientConfig(
        jwtToken="<token>"
    ),
)
metadata = OpenMetadata(server_config)

assert metadata.health_check()  # Will fail if we cannot reach the server
```

--------------------------------

### Install Test Dependencies and Run Coverage

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/ingestion-framework

Install necessary packages for running tests and validate the environment by running the test coverage report. Some tests require the OpenMetadata server to be running.

```bash
make install_test
make coverage

```

--------------------------------

### Install OpenMetadata Ingestion with Database Connectors

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/data-quality-observability/quality/data-quality-as-code/getting-started

Install the openmetadata-ingestion package with specific database connector extras. Use this when you need to test data quality for particular databases.

```bash
# For PostgreSQL
pip install "openmetadata-ingestion[postgres]>=1.12.0.0"

# For MySQL
pip install "openmetadata-ingestion[mysql]>=1.12.0.0"

# For BigQuery
pip install "openmetadata-ingestion[bigquery]>=1.12.0.0"

# For multiple databases
pip install "openmetadata-ingestion[postgres,mysql,bigquery]>=1.12.0.0"
```

--------------------------------

### Install Looker Ingestion Package

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/looker/yaml

Install the OpenMetadata Ingestion package with Looker support using pip.

```bash
pip3 install "openmetadata-ingestion[looker]"
```

--------------------------------

### Start MySQL and Elasticsearch with Docker

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/openmetadata-server

Use this command to set up MySQL and Elasticsearch for development using Docker Compose.

```bash
docker compose -f docker/development/docker-compose.yml up mysql elasticsearch --build -d
```

--------------------------------

### List Pipelines with Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/pipelines/list

Demonstrates how to list pipelines, including fetching the first page, iterating through all pipelines with auto-pagination, and filtering by service. Ensure the SDK is configured with your host and JWT token.

```python
from metadata.sdk import configure
from metadata.sdk.entities import Pipelines

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# List first page
pipelines = Pipelines.list(limit=50)
for p in pipelines.data:
    print(f"{p.fullyQualifiedName}")

# List all with auto-pagination
for p in Pipelines.list_all():
    print(f"{p.fullyQualifiedName}")

# Filter by service
pipelines = Pipelines.list(
    service="sample_airflow",
    fields=["owners", "tags", "tasks"],
    limit=50
)

for p in pipelines.data:
    print(f"{p.fullyQualifiedName}")
    if p.owners:
        print(f"  Owners: {[o.name for o in p.owners]}")
    if p.tasks:
        print(f"  Tasks: {[t.name for t in p.tasks]}")

```

--------------------------------

### Start OpenMetadata with PostgreSQL Docker Compose

Source: https://docs.open-metadata.org/latest/quick-start/local-docker-deployment

Use this command to deploy OpenMetadata with a PostgreSQL database. It pulls necessary Docker images and starts the services in detached mode.

```bash
docker compose -f docker-compose-postgres.yml up --detach
```

--------------------------------

### Start Docker Compose with LDAP Environment File

Source: https://docs.open-metadata.org/v1.12.x/deployment/security/ldap/docker

Start the OpenMetadata services using Docker Compose, loading LDAP configurations from a specified environment file.

```bash
docker compose --env-file ~/openmetadata_ldap.env up -d
```

--------------------------------

### Working with Entities

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/overview

Examples of how to interact with entities like Database Services and Tables using the SDK.

```APIDOC
from metadata.sdk import Tables, DatabaseServices

# Get all database services
services = list(DatabaseServices.list().auto_paging_iterable())
print(f"Found {len(services)} database services")

# Get a specific table by name
table = Tables.retrieve_by_name("your-service.your-database.your-schema.your-table")

if table:
    print(f"Table: {table.name}")
    print(f"Columns: {len(table.columns) if table.columns else 0}")
```

--------------------------------

### Complete Profiler YAML Example: After (Spark Engine)

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/data-quality-observability/profiler/spark-engine/configuration/external-configuration

This example shows the updated profiler configuration after integrating the Spark Engine, including `processingEngine` and `sparkTableProfilerConfig`.

```yaml
sourceConfig:
  config:
    type: Profiler
    schemaFilterPattern:
      includes:
        - ^your_schema$
    tableFilterPattern:
      includes:
        - your_table_name
    processingEngine:
      type: Spark
      remote: sc://your_spark_connect_host:15002
      config:
        tempPath: s3://your_s3_bucket/table
        # extraConfig:
        #     key: value
processor:
  type: orm-profiler
  config:
    tableConfig:
      - fullyQualifiedName: YourService.YourDatabase.YourSchema.YourTable
        sparkTableProfilerConfig:
          partitioning:
            partitionColumn: your_partition_column
            # lowerBound: 0
            # upperBound: 1000000
```

--------------------------------

### UI Documentation for Connector Configuration

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/developing-a-new-connector/apply-ui-changes

Create a Markdown file (e.g., `YourConnector.mdx`) in the `locales/en-US/{source_type}` directory to provide follow-along documentation for your connector's configuration. Use `$(id="{something}")` notation to sync documentation with UI properties.

```markdown
## Connection Details

Within the `## Connection Details` section you can see that we use some special notation `$(id="{something}")`.This is used to sync the documentation here with the property that the user is configuring at a given time (The “follow along” feature if you will).In order to make it work properly you need to set the ID of each section to the property of the JSON Schema.
```

--------------------------------

### Athena Connector Details Header Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/athena/yaml

An example of how to use the ConnectorDetailsHeader component to display information for the Athena connector.

```javascript
<ConnectorDetailsHeader icon="/public/images/connectors/athena.webp" name="Athena" stage="PROD" availableFeatures={["Metadata", "Query Usage", "Lineage", "Column-level Lineage", "Data Profiler", "Auto-Classification", "Data Quality", "Tags", "dbt", "Sample Data"]} unavailableFeatures={["Owners", "Stored Procedures"]} />
```

--------------------------------

### Install Athena Ingestion Dependencies

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/athena/yaml

Install the necessary Python packages for running the Athena ingestion workflow. This command ensures all required dependencies, including the Athena connector, are installed.

```bash
pip3 install "openmetadata-ingestion[athena]"
```

--------------------------------

### List Topics with Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/topics/list

Demonstrates how to list topics using the OpenMetadata Python SDK. Includes examples for listing the first page, using auto-pagination to list all topics, and filtering topics by service. Ensure the SDK is configured with your host and JWT token.

```python
from metadata.sdk import configure
from metadata.sdk.entities import Topics

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# List first page
topics = Topics.list(limit=50)
for t in topics.data:
    print(f"{t.fullyQualifiedName}")

# List all with auto-pagination
for t in Topics.list_all():
    print(f"{t.fullyQualifiedName}")

# Filter by service
topics = Topics.list(
    service="sample_kafka",
    fields=["owners", "tags", "domain"],
    limit=50
)

for t in topics.data:
    print(f"{t.fullyQualifiedName}")
    if t.owners:
        print(f"  Owners: {[o.name for o in t.owners]}")
    if t.tags:
        print(f"  Tags: {[t.tagFQN for t in t.tags]}")

```

--------------------------------

### Install QlikSense Ingestion Dependencies

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/qliksense/yaml

Install the necessary Python package for the QlikSense ingestion connector. This command ensures all required dependencies are met.

```bash
pip3 install "openmetadata-ingestion[qliksense]"
```

--------------------------------

### Self-hosted Airflow HostPort Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/airflow/rest-api-connection

Example of the hostPort parameter for a self-hosted Airflow instance when the ingestion is running on the same host.

```text
http://localhost:8080
```

--------------------------------

### Qlik Cloud Metadata Ingestion UI Steps

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/qlikcloud

Guides the user through the UI steps for setting up Qlik Cloud metadata ingestion, including creating a new service and configuring connection details.

```javascript
export const MetadataIngestionUi = ({connector, selectServicePath, addNewServicePath, serviceConnectionPath}) => {
  return <Steps>
      <Step title="Visit the Services Page">
        Click `Settings` in the side navigation bar and then `Services`.

        The first step is to ingest the metadata from your sources. To do that, you first need to create a Service connection first.

        This Service will be the bridge between OpenMetadata and your source system.

        Once a Service is created, it can be used to configure your ingestion workflows.

        <img src="/public/images/connectors/visit-services-page.png" alt="Visit Services Page" />
      </Step>

      <Step title="Create a New Service">
        Click on _Add New Service_ to start the Service creation.

        <img src="/public/images/connectors/create-new-service.png" alt="Create a new Service" />
      </Step>

      <Step title="Select the Service Type">
        Select {connector} as the Service type and click _Next_.

        {selectServicePath && <img src={selectServicePath} alt="Select Service" />}
      </Step>

      <Step title="Name and Describe your Service">
        Provide a name and description for your Service.

        <h4>Service Name</h4>

        OpenMetadata uniquely identifies Services by their **Service Name**.
        Provide a name that distinguishes your deployment from other Services, including
        the other {connector} Services that you might be ingesting metadata
        from.

        Note that when the name is set, it cannot be changed.

        {addNewServicePath && <img src={addNewServicePath} alt="Add New Service" />}
      </Step>

      <Step title="Configure the Service Connection">
        In this step, we will configure the connection settings required for {connector}.

        Please follow the instructions below to properly configure the Service to read from your sources. You will also find
        helper documentation on the right-hand side panel in the UI.

        {serviceConnectionPath && <img src={serviceConnectionPath} alt="Configure Service connection" />}
      </Step>
    </Steps>;
};

<MetadataIngestionUi connector={"QlikCloud"} selectServicePath={"/public/images/connectors/qlikcloud/select-service.png"} addNewServicePath={"/public/images/connectors/qlikcloud/add-new-service.png"} serviceConnectionPath={"/public/images/connectors/qlikcloud/service-connection.png"} />
```

--------------------------------

### Install OpenMetadata Ingestion Framework

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/lightdash/yaml

Install the necessary package for running OpenMetadata ingestion workflows. Ensure you are using Python 3.9-3.11.

```bash
pip3 install "openmetadata-ingestion"
```

--------------------------------

### JVMDefault Configuration Example

Source: https://docs.open-metadata.org/v1.12.x/deployment/security/ldap/kubernetes

Example of configuring the JVMDefault trust store for LDAP authentication, with hostname verification enabled.

```yaml
openmetadata:
  config:
     ...
     authentication:
        ...
        ldapConfiguration:
           ...
           truststoreConfigType: JVMDefault
           trustStoreConfig:
              jvmDefaultConfig:
              verifyHostname: true
  ...
```

--------------------------------

### Install Docker Compose on Linux

Source: https://docs.open-metadata.org/latest/quick-start/local-docker-deployment

Installs Docker Compose version 2.2.3 for the current user on Linux systems. Ensure you have the necessary permissions or adjust the path for system-wide installation.

```bash
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}

mkdir -p $DOCKER_CONFIG/cli-plugins 
curl -SL https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose

```

```bash
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose 

```

```bash
docker compose version
> Docker Compose version v2.2.3

```

--------------------------------

### Install Certbot for HTTPS

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/dbt/storage-http-guide

Install Certbot and its Nginx plugin to obtain and manage SSL certificates for enabling HTTPS.

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d artifacts.yourcompany.com

# Auto-renew
sudo certbot renew --dry-run

```

--------------------------------

### Install Python Packages on Ubuntu

Source: https://docs.open-metadata.org/v1.12.x/quick-start/local-docker-deployment

Install pip and venv for Python 3 on Ubuntu systems, required for Docker deployment.

```bash
apt install python3-pip  python3-venv
```

--------------------------------

### List Available MCP Tools

Source: https://docs.open-metadata.org/v1.12.x/sdk/ai-sdk

Demonstrates how to list all available MCP tools and iterate through them to print their names and descriptions.

```python
tools = client.mcp.list_tools()
for tool in tools:
    print(f"{tool.name}: {tool.description}")
```

--------------------------------

### Start Docker Compose with Auth0 Environment File

Source: https://docs.open-metadata.org/v1.12.x/deployment/security/auth0/docker

Use this command to start the OpenMetadata Docker Compose service, applying the Auth0 environment variables defined in the specified .env file.

```bash
docker compose --env-file ~/openmetadata_auth0.env up -d

```

--------------------------------

### Delete Pipeline Service Examples (Python)

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/pipeline-services/delete

Demonstrates how to delete pipeline services using the Python requests library. Includes examples for soft delete by ID, hard delete with recursion, delete by name, and restoring a soft-deleted service.

```python
import requests

base_url = "https://your-company.open-metadata.org/api"
headers = {"Authorization": "Bearer your-jwt-token"}

# Soft delete by ID
requests.delete(
    f"{base_url}/v1/services/pipelineServices/daa58a49-df05-48a3-a417-45dfd12eacf5",
    headers=headers
)

# Hard delete with recursive
requests.delete(
    f"{base_url}/v1/services/pipelineServices/daa58a49-df05-48a3-a417-45dfd12eacf5?hardDelete=true&recursive=true",
    headers=headers
)

# Delete by name
requests.delete(
    f"{base_url}/v1/services/pipelineServices/name/sample_airflow",
    headers=headers
)

# Restore a soft-deleted pipeline service
requests.put(
    f"{base_url}/v1/services/pipelineServices/restore",
    json={"id": "daa58a49-df05-48a3-a417-45dfd12eacf5"},
    headers={**headers, "Content-Type": "application/json"}
)

```

--------------------------------

### Full YAML Configuration Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/burstiq/yaml

This is a complete YAML configuration file for the BurstIQ connector, including source, processor, sink, and workflow configurations. Ensure you replace placeholders like '<OpenMetadata host and port>' and '<OpenMetadata auth provider>' with your actual values.

```yaml
source:
  type: TestSuite
  serviceName: MyAwesomeTestSuite
  sourceConfig:
    config:
      type: TestSuite
      entityFullyQualifiedName: MySQL.default.openmetadata_db.tag_usage
#     testCases: ["run_only_this_test_case"] # Optional, if not provided all tests will be executed

processor:
  type: "orm-test-runner"
  config:
    forceUpdate: false
    testCases:
      - name: column_value_length_tagFQN
        testDefinitionName: columnValueLengthsToBeBetween
        columnName: tagFQN
        parameterValues:
          - name: minLength
            value: 10
          - name: maxLength
            value: 25
      - name: table_row_count_test
        testDefinitionName: tableRowCountToEqual
        parameterValues:
          - name: value
            value: 10

sink:
  type: metadata-rest
  config: {}
workflowConfig:
  openMetadataServerConfig:
    hostPort: <OpenMetadata host and port>
    authProvider: <OpenMetadata auth provider>

```

--------------------------------

### Install PII Processor Package

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/data-governance/classification/auto-classification/external-workflow

Install the OpenMetadata ingestion package with the PII Processor module to enable auto-classification features.

```bash
pip install "openmetadata-ingestion[pii-processor]"
```

--------------------------------

### Verify MCP Application Installation

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/mcp/claude-code

Check the installation status of the MCP Application within your OpenMetadata instance by navigating to the specified URL.

```bash
Visit <YOUR-OpenMetadata-SERVER>/marketplace/apps/McpApplication
```

--------------------------------

### Navigate to Release Directory

Source: https://docs.open-metadata.org/v1.12.x/deployment/upgrade/bare-metal/steps

Change into the newly created directory after extracting the release binaries. Replace 'x.y.z' with the specific version number.

```bash
cd openmetadata-x.y.z

```

```bash
cd openmetadata-1.1.0

```

--------------------------------

### Install Azure SQL Ingestion Package

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/azuresql/yaml

Install the openmetadata-ingestion package with the Azure SQL extra to enable the connector. This command is for Python environments.

```bash
pip3 install "openmetadata-ingestion[azuresql]"
```

--------------------------------

### Install Claude Code Skills Plugin

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/developing-a-new-connector/ai-assisted-development/install-skills

Install the OpenMetadata skills package as a plugin for Claude Code from the repository root.

```bash
claude plugin install skills/
```

--------------------------------

### Install Exasol Ingestion Package

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/exasol/yaml

Install the necessary Python package for the Exasol connector. This command includes the Exasol extra.

```bash
pip3 install "openmetadata-ingestion[Exasol]"
```

--------------------------------

### List Containers with Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/containers/list

Demonstrates how to list containers using the OpenMetadata Python SDK. Includes examples for listing the first page, listing all containers with auto-pagination, and filtering by service with specific fields.

```python
from metadata.sdk import configure
from metadata.sdk.entities import Containers

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# List first page
containers = Containers.list(limit=50)
for c in containers.data:
    print(f"{c.fullyQualifiedName}")

# List all with auto-pagination
for c in Containers.list_all():
    print(f"{c.fullyQualifiedName}")

# Filter by storage service
containers = Containers.list(
    service="s3_datalake",
    fields=["owners", "tags", "dataModel"],
    limit=50
)

for c in containers.data:
    print(f"{c.fullyQualifiedName}")
    if c.owners:
        print(f"  Owners: {[o.name for o in c.owners]}")
    if c.tags:
        print(f"  Tags: {[t.tagFQN for t in c.tags]}")

```

```json
{
  "data": [
    {
      "id": "14744329-85c2-499e-b1fa-249fb8162341",
      "name": "analytics-bucket",
      "displayName": "Analytics Bucket",
      "fullyQualifiedName": "s3_datalake.analytics-bucket",
      "description": "Primary analytics data lake bucket",
      "version": 0.1,
      "updatedAt": 1769982673032,
      "updatedBy": "admin",
      "service": {
        "id": "d1589e1d-2ab0-431c-a383-15e4be20a106",
        "type": "storageService",
        "name": "s3_datalake",
        "fullyQualifiedName": "s3_datalake",
        "deleted": false
      },
      "serviceType": "S3",
      "prefix": "/analytics/",
      "numberOfObjects": 150000,
      "size": 5368709120,
      "fileFormats": ["parquet", "json"],
      "href": "http://localhost:8585/api/v1/containers/14744329-85c2-499e-b1fa-249fb8162341",
      "deleted": false,
      "owners": [],
      "tags": [],
      "followers": [],
      "votes": {
        "upVotes": 0,
        "downVotes": 0
      },
      "domains": []
    }
  ],
  "paging": {
    "after": "...",
    "total": 5
  }
}

```

--------------------------------

### Python SDK Example for Deleting Storage Services

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/storage-services/delete

Examples demonstrating how to use the Python SDK to delete storage services by ID or name, with options for hard delete and recursive deletion.

```python
from metadata.sdk import configure
from metadata.sdk.entities import StorageServices

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# Soft delete by ID
StorageServices.delete("d1589e1d-2ab0-431c-a383-15e4be20a106")

# Hard delete
StorageServices.delete(
    "d1589e1d-2ab0-431c-a383-15e4be20a106",
    hard_delete=True
)

# Delete by name
StorageServices.delete_by_name("s3_datalake")

# Delete by name with options
StorageServices.delete_by_name(
    "s3_datalake",
    hard_delete=True,
    recursive=True
)

# Restore a soft-deleted storage service
StorageServices.restore("d1589e1d-2ab0-431c-a383-15e4be20a106")

```

--------------------------------

### Install LangChain Integration for AI SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/ai-sdk

Installs the AI SDK with LangChain support. This is a prerequisite for using OpenMetadata's MCP tools within LangChain agents.

```bash
pip install data-ai-sdk[langchain]
```

--------------------------------

### Build and Run Local Docker Environment (Full)

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/developing-a-new-connector/ai-assisted-development/build-with-ai

Perform a full build of the OpenMetadata stack in Docker, including UI, database, and services. Use this for the initial setup or when significant changes to Java or UI components are made.

```bash
./docker/run_local_docker.sh -m ui -d mysql -s false -i true -r true

```

--------------------------------

### Install Virtualenv Prerequisites

Source: https://docs.open-metadata.org/v1.12.x/deployment/ingestion/external/airflow

Install the 'virtualenv' package on the Airflow host. If using a different Python version in the virtual environment than Airflow's, install corresponding development packages like 'python3.9-dev' and 'python3.9-distutils'.

```bash
gcc python3.9-dev python3.9-distutils

```

--------------------------------

### provider_registry.okta_auth_init

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/api-reference

Initialize authentication with Okta.

```APIDOC
## okta_auth_init

### Description
Initializes authentication using Okta.

### Method
provider_registry.okta_auth_init()
```

--------------------------------

### Install Docker Compose V2 on Linux

Source: https://docs.open-metadata.org/v1.12.x/deployment/docker

Download and install Docker Compose V2 for the current user on Linux systems. Ensure executable permissions are set.

```bash
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}

mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64 -o
$DOCKER_CONFIG/cli-plugins/docker-compose

```

```bash
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose

```

```bash
docker compose version
> Docker Compose version v2.2.3

```

--------------------------------

### Create Table using Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/getting-started

Initialize the SDK with configuration and use the fluent API to create a new table with specified columns and descriptions.

```python
from metadata.sdk import Tables, configure
from metadata.generated.schema.api.data.createTable import CreateTableRequest
from metadata.generated.schema.entity.data.table import Column, DataType

# Initialize the SDK
configure(host="https://your-company.open-metadata.org", jwt_token="your-jwt-token")

# Create and persist the table
table = Tables.create(CreateTableRequest(
    name="customers",
    databaseSchema="mysql-prod.analytics.public",
    description="Customer master table",
    columns=[
        Column(name="id", dataType=DataType.BIGINT, description="Primary key"),
        Column(name="name", dataType=DataType.VARCHAR, dataLength=255, description="Customer name"),
        Column(name="email", dataType=DataType.VARCHAR, dataLength=255, description="Email address"),
    ],
))

print(f"Created: {table.fullyQualifiedName}")
```

--------------------------------

### Install OpenMetadata Ingestion Extras

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/data-quality-observability/quality/data-quality-as-code/test-runner

Install the necessary extras for OpenMetadata ingestion based on your cloud provider. This is required for secrets manager integration.

```bash
# For AWS
pip install "openmetadata-ingestion[aws]"

# For Azure
pip install "openmetadata-ingestion[azure]"

# For GCP
pip install "openmetadata-ingestion[gcp]"
```

--------------------------------

### Install OpenMetadata Dependencies

Source: https://docs.open-metadata.org/v1.12.x/quick-start/local-kubernetes-deployment

Installs the OpenMetadata Dependencies Helm chart, which includes essential services like MySQL, OpenSearch, and Airflow. This command deploys the necessary infrastructure for OpenMetadata.

```bash
helm install openmetadata-dependencies open-metadata/openmetadata-dependencies
```

--------------------------------

### Install Snowflake Ingestion Dependencies

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/snowflake/yaml

Install the necessary Python packages for the Snowflake ingestion connector.

```bash
pip3 install "openmetadata-ingestion[snowflake]"
```

--------------------------------

### Install OpenMetadata Helm Chart

Source: https://docs.open-metadata.org/v1.12.x/deployment/kubernetes/eks

Add the OpenMetadata Helm repository, update it, and install the OpenMetadata chart. This assumes you are using the Kubernetes orchestrator and do not need the dependencies chart.

```bash
# Add the OpenMetadata Helm repository
helm repo add open-metadata https://helm.open-metadata.org/
helm repo update

# Install OpenMetadata (no dependencies chart needed with K8s orchestrator)
helm install openmetadata open-metadata/openmetadata \
  --values openmetadata-values.yaml
```

--------------------------------

### Cassandra Connection String Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/cassandra

Use this format for the hostPort parameter when connecting to Cassandra.

```text
localhost:9042
```

--------------------------------

### AI Implementation Instructions

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/developing-a-new-connector/ai-assisted-development

Provide these instructions to your AI agent to guide it in completing the connector implementation. It specifies reading the context file and implementing TODO items, using a reference connector as a pattern.

```bash
Read ingestion/src/metadata/ingestion/source/{type}/{name}/CONNECTOR_CONTEXT.md
and implement all TODO items. Use the reference connector as a pattern.
```

--------------------------------

### Data Discovery Example

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/overview

Shows how to list all tables and filter them for a specific keyword, like 'customer', using a list comprehension and iterating through the results.

```APIDOC
## Data Discovery Example

### Description
Shows how to list all tables and filter them for a specific keyword, like 'customer', using a list comprehension and iterating through the results.

### Code
```python
from metadata.sdk import Tables

# Iterate all tables and filter for a keyword
matching_tables = [
    table for table in Tables.list().auto_paging_iterable()
    if "customer" in table.name.lower()
]

for table in matching_tables:
    print(f"Found customer table: {table.fullyQualifiedName}")
```
```

--------------------------------

### Build Custom Drive Connector Package

Source: https://docs.open-metadata.org/v1.12.x/connectors/drive/custom-drive

Use the setup.py script to build the source distribution (sdist) of your custom drive connector package.

```bash
python setup.py sdist
```

--------------------------------

### Get User by ID

Source: https://docs.open-metadata.org/v1.12.x/api-reference/teams-and-users/users

Retrieve a specific user by their unique ID using the GET method.

```shell
GET /v1/users/{id}
```

--------------------------------

### Install NFS Provisioner Helm Chart

Source: https://docs.open-metadata.org/v1.12.x/deployment/kubernetes/on-prem

Install the `nfs-subdir-external-provisioner` helm chart to dynamically provision PersistentVolumes using a StorageClass. Replace `<NFS_HOSTNAME_OR_IP>` with your NFS server's hostname or IP address.

```command-line
helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner

helm install nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
  --create-namespace \
  --namespace nfs-provisioner \
  --set nfs.server=<NFS_HOSTNAME_OR_IP> \
  --set nfs.path=/airflow
```

--------------------------------

### Check if OpenMetadata Package is Installed

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/data-quality-observability/quality/data-quality-as-code/getting-started

Use this command to verify if the OpenMetadata ingestion package is installed in your environment.

```bash
pip list | grep openmetadata
```

--------------------------------

### Install Elasticsearch Ingestion

Source: https://docs.open-metadata.org/v1.12.x/connectors/search/elasticsearch/yaml

Install the necessary package for the Elasticsearch ingestion. This command should be run in your Python environment.

```bash
pip3 install "openmetadata-ingestion[elasticsearch]"
```

--------------------------------

### OpenSearch YAML Configuration Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/search/opensearch/yaml

This is a sample YAML configuration for connecting to an OpenSearch instance. It includes parameters for host, port, authentication, and SSL settings.

```yaml
hostPort: "https://localhost:9200"
username: "admin"
password: "admin"
verifySSL: "true"
sslConfig:
  caCertPath: "/path/to/ca.crt"
  clientCertPath: "/path/to/client.crt"
  privateKeyPath: "/path/to/client.key"
connectionTimeoutSecs: 5
```

--------------------------------

### Installing Vertica Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/vertica/yaml

Install the OpenMetadata ingestion package with Vertica support using pip.

```bash
pip3 install "openmetadata-ingestion[vertica]"
```

--------------------------------

### Install OpenMetadata Ingestion SDK (Python)

Source: https://docs.open-metadata.org/api-reference

Install the OpenMetadata ingestion SDK for Python. This package provides tools for data ingestion and metadata management.

```bash
pip install "openmetadata-ingestion~=1.12.1"
```

--------------------------------

### Install SFTP Connector Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/drive/sftp/yaml

Install the necessary Python package for SFTP ingestion. This command ensures all dependencies for the SFTP connector are available.

```bash
pip3 install "openmetadata-ingestion[sftp]"
```

--------------------------------

### provider_registry.saml_auth_init

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/api-reference

Initialize authentication with SAML.

```APIDOC
## saml_auth_init

### Description
Initializes authentication using SAML.

### Method
provider_registry.saml_auth_init()
```

--------------------------------

### Full YAML Configuration Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/azuresql/yaml

A complete YAML configuration including source, processor with specific test cases, sink, and workflow settings for running data quality tests.

```yaml
source:
  type: TestSuite
  serviceName: MyAwesomeTestSuite
  sourceConfig:
    config:
      type: TestSuite
      entityFullyQualifiedName: MySQL.default.openmetadata_db.tag_usage
#     testCases: ["run_only_this_test_case"] # Optional, if not provided all tests will be executed

processor:
  type: "orm-test-runner"
  config:
    forceUpdate: false
    testCases:
      - name: column_value_length_tagFQN
        testDefinitionName: columnValueLengthsToBeBetween
        columnName: tagFQN
        parameterValues:
          - name: minLength
            value: 10
          - name: maxLength
            value: 25
      - name: table_row_count_test
        testDefinitionName: tableRowCountToEqual
        parameterValues:
          - name: value
            value: 10

sink:
  type: metadata-rest
  config: {}
workflowConfig:
  openMetadataServerConfig:
    hostPort: <OpenMetadata host and port>
    authProvider: <OpenMetadata auth provider>
```

--------------------------------

### Go SDK Get Method

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/go-api-methods

Use the Get method to retrieve data from a specified API path. Ensure the path is correctly formatted.

```go
// main.go
... 
func main() {
    ...
    path := "tables"
	body, err := rest.Get(path, nil, nil, nil)
}
```

--------------------------------

### Exported CSV Data Example

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/tables/import-export

An example of the CSV formatted data that is returned when exporting table metadata.

```text
"name,displayName,description,dataType,tags\nagent_id,,Agent identifier,VARCHAR,\nperformance_score,,Overall performance score,DECIMAL,"
```

--------------------------------

### Exported Messaging Service Data Example

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/messaging-services/import-export

Example of the CSV format for exported messaging service metadata.

```csv
"name,displayName,description,owner,tags,domain\norder_events,Order Events,Events for order processing,team:data-engineering,Tier.Tier1,,"
```

--------------------------------

### Install ClickHouse Usage Connector Dependencies

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/clickhouse/yaml

Install the OpenMetadata ingestion framework with ClickHouse usage connector support. This is required if you plan to run the Usage Connector.

```bash
pip3 install "openmetadata-ingestion[clickhouse-usage]"
```

--------------------------------

### Sample Response for Get a Prompt

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/mcp/connect-api

This response provides the description of the prompt and the generated user message for the tool.

```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "result": {
    "description": "Creates a prompt for Searching metadata in OpenMetadata.",
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Search for tables related to 'customer tables' in the OpenMetadata catalog. Filter results to show only 'table' entities and limit to 10 results. Look for tables that contain customer information, customer data, or are related to customer operations."
        }
      }
    ]
  }
}
```

--------------------------------

### Response Example (Soft Delete)

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/messaging-services/delete

Example JSON response after a successful soft delete of a messaging service.

```json
{
  "id": "469ef25e-9bdf-4d5f-8553-eb0ce8581f30",
  "name": "sample_kafka",
  "fullyQualifiedName": "sample_kafka",
  "serviceType": "Kafka",
  "connection": {
    "config": {
      "type": "Kafka",
      "bootstrapServers": "localhost:9092",
      "securityProtocol": "PLAINTEXT",
      "saslMechanism": "PLAIN",
      "supportsMetadataExtraction": true
    }
  },
  "version": 0.2,
  "updatedAt": 1769982750000,
  "updatedBy": "admin",
  "href": "http://localhost:8585/api/v1/services/messagingServices/469ef25e-9bdf-4d5f-8553-eb0ce8581f30",
  "owners": [],
  "tags": [],
  "deleted": true,
  "domains": []
}

```

--------------------------------

### Install OpenMetadata Managed APIs

Source: https://docs.open-metadata.org/deployment/ingestion/openmetadata

Install the openmetadata-managed-apis package to deploy custom APIs on top of Airflow. Replace `x.y.z` with your OpenMetadata server version.

```bash
pip3 install "openmetadata-managed-apis==x.y.z"
```

--------------------------------

### Domo Connector Header Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/domo-dashboard

An example of how to use the ConnectorDetailsHeader component to display information for the Domo connector. This includes its icon, name, stage, and lists of available and unavailable features.

```javascript
<ConnectorDetailsHeader icon="/public/images/connectors/domo.webp" name="Domo" stage="PROD" availableFeatures={["Dashboards", "Charts", "Owners"]} unavailableFeatures={["Tags", "Datamodels", "Projects", "Lineage"]} />
```

--------------------------------

### Install OpenMetadata Ingestion with DataFrame Support

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/data-quality-observability/quality/data-quality-as-code/getting-started

Install the openmetadata-ingestion package with pandas extras for DataFrame validation features.

```bash
pip install "openmetadata-ingestion[pandas]>=1.12.0.0"
```

--------------------------------

### Superset Connector Header Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/superset

Example usage of the ConnectorDetailsHeader component for the Superset connector. This renders the header with Superset's specific details.

```javascript
<ConnectorDetailsHeader icon="/public/images/connectors/superset.webp" name="Superset" stage="PROD" availableFeatures={["Dashboards", "Charts", "Lineage", "Owners", "Datamodels", "Column Lineage"]} unavailableFeatures={["Tags", "Projects"]} />
```

--------------------------------

### Start OpenMetadata Docker Compose with Azure .env

Source: https://docs.open-metadata.org/v1.12.x/deployment/security/azure/docker

Execute this command to start your OpenMetadata Docker containers using the specified Azure environment file. Ensure the path to your .env file is correct.

```bash
docker compose --env-file ~/openmetadata_azure.env up -d

```

--------------------------------

### Initialize AI SDK Client in Python (Environment Variables)

Source: https://docs.open-metadata.org/v1.12.x/sdk/ai-sdk

Initialize the AI SDK client by loading configuration directly from environment variables.

```python
from ai_sdk import AISdk, AISdkConfig

config = AISdkConfig.from_env()
client = AISdk.from_config(config)
```

--------------------------------

### Run Your First Data Quality Test with SDK

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/data-quality-observability/quality/data-quality-as-code/getting-started

Configure the SDK, create a TestRunner for a specific table, add a row count test, and run the tests. Prints the status and result of each test.

```python
from metadata.sdk import configure
from metadata.sdk.data_quality import TestRunner, TableRowCountToBeBetween

# Configure SDK
configure(
    host="http://localhost:8585/api",
    jwt_token="your-jwt-token-here"
)

# Create a test runner for a specific table
runner = TestRunner.for_table("MySQL.ecommerce.public.customers")

# Add a test to verify row count is within expected range
runner.add_test(
    TableRowCountToBeBetween(min_count=1000, max_count=100000)
)

# Run the tests
results = runner.run()

# Print results
for result in results:
    test_case = result.testCase
    test_result = result.testCaseResult

    print(f"Test: {test_case.name.root}")
    print(f"Status: {test_result.testCaseStatus}")
    print(f"Result: {test_result.result}")
```

--------------------------------

### Install or Upgrade OpenMetadata Helm Release

Source: https://docs.open-metadata.org/v1.12.x/deployment/azure-passwordless-auth

Use this command to install or upgrade your OpenMetadata Helm release with the configured passwordless database connection settings. Ensure you replace `<OPENMETADATA_HELM_VALUES_FILE_PATH>` with the actual path to your Helm values file.

```bash
helm repo update open-metadata
helm upgrade --install openmetadata open-metadata/openmetadata --values <OPENMETADATA_HELM_VALUES_FILE_PATH>
```

--------------------------------

### Automated SQL Lineage via CLI

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/ingestion/lineage

Instructions on how to set up and run automated SQL lineage generation using the OpenMetadata CLI.

```APIDOC
## Automated SQL lineage via CLI

SQL-based lineage parsing is not part of `metadata.sdk.api.Lineage` today. If you need lineage generated from raw SQL, use the lineage ingestion workflow or CLI. The older `add_lineage_by_query` helper belongs to the legacy `metadata.ingestion.ometa` client surface, not the current `metadata.sdk` API.

To create the automated sql lineage via CLI, you need to make sure that you have installed the openmetadata-ingestion package in your local environment using command `pip install openmetadata-ingestion`. Once that is done you will have to prepare a yaml file as follows.

```yaml
serviceName: local_mysql
query: insert into target_table(id) as select id from source_table
# filePath: test.sql
# parseTimeout: 360 # timeout in seconds
workflowConfig:
  # loggerLevel: DEBUG  # DEBUG, INFO, WARN or ERROR
  openMetadataServerConfig:
    hostPort: <OpenMetadata host and port>
    authProvider: <OpenMetadata auth provider>

```

*   **serviceName** : Name of the database service which contains the table involved in query.
*   **query** : You can specify the raw sql query within the yaml file itself.
*   **filePath** : In case the query is too big then you can also save query in a file and pass the path to the file in this field.
*   **parseTimeout** : Timeout for the lineage parsing process.
*   **workflowConfig** : The main property here is the openMetadataServerConfig, where you can define the host and security provider of your OpenMetadata installation.

Once the yaml file is prepare you can run the command

```bash
metadata lineage -c path/to/your_config_yaml.yaml

```
```

--------------------------------

### Example 1: Include Databases Containing 'SNOWFLAKE'

Source: https://docs.open-metadata.org/connectors/ingestion/workflows/metadata/filter-patterns/database

Use the `.*SNOWFLAKE.*` pattern to include all databases with 'SNOWFLAKE' in their name. This example demonstrates filtering via CLI.

```yaml
sourceConfig:
  config:
    ...
    useFqnForFiltering: false
    databaseFilterPattern:
      includes:
        - .*SNOWFLAKE.*

```

--------------------------------

### List Glossaries with Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/governance/glossaries/list

Demonstrates how to list glossaries using the OpenMetadata Python SDK. Includes examples for fetching the first page, listing all glossaries with auto-pagination, and specifying fields to retrieve.

```python
from metadata.sdk import configure
from metadata.sdk.entities import Glossaries

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# List first page
glossaries = Glossaries.list(limit=50)
for g in glossaries.data:
    print(f"{g.fullyQualifiedName}")

# List all with auto-pagination
for g in Glossaries.list_all():
    print(f"{g.fullyQualifiedName}")

# With fields
glossaries = Glossaries.list(
    fields=["owners", "tags", "reviewers"],
    limit=50
)

for g in glossaries.data:
    print(f"{g.fullyQualifiedName}")
    if g.reviewers:
        print(f"  Reviewers: {[r.name for r in g.reviewers]}")

```

--------------------------------

### Bash Search Query Examples

Source: https://docs.open-metadata.org/v1.12.x/api-reference/discovery/search

Interact with the Search API using cURL. Examples demonstrate basic searches, searching within specific indices, applying sorting, and using query filters with Elasticsearch DSL.

```bash
# Basic search across all entities
curl "{base_url}/api/v1/search/query?q=dim&from=0&size=10" \
  -H "Authorization: Bearer {access_token}"
```

```bash
# Search within a specific index
curl "{base_url}/api/v1/search/query?q=customer&index=table_search_index&size=5" \
  -H "Authorization: Bearer {access_token}"
```

```bash
# Search with sorting
curl "{base_url}/api/v1/search/query?q=*&index=table_search_index&sortField=name&sortOrder=asc&size=20" \
  -H "Authorization: Bearer {access_token}"
```

```bash
# Search with query filter (Elasticsearch DSL)
curl -G "{base_url}/api/v1/search/query" \
  --data-urlencode "q=*" \
  --data-urlencode "index=table_search_index" \
  --data-urlencode 'queryFilter={"query":{"bool":{"must":[{"term":{"serviceType":"BigQuery"}}]}}}' \
  -H "Authorization: Bearer {access_token}"
```

--------------------------------

### Install Snowflake Usage Connector Dependencies

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/snowflake/yaml

Install the Python packages required for ingesting Snowflake usage data.

```bash
pip3 install "openmetadata-ingestion[snowflake-usage]"
```

--------------------------------

### Build API Clients with Java

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/java

Demonstrates how to build clients for different OpenMetadata APIs using the `openMetadataGateway.buildClient()` method. This is the initial step before making API calls.

```java
DashboardsApi dashboardApi = openMetadataGateway.buildClient(DashboardsApi.class);

// Tables API
TablesApi tablesApiClient = openMetadataGateway.buildClient(TablesApi.class);

// Users API
UsersApi usersApi = openMetadataGateway.buildClient(UsersApi.class);

// Locations API
LocationsApi locationsApi = openMetadataGateway.buildClient(LocationsApi.class);
```

--------------------------------

### MicroStrategy Connector Header Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/microstrategy

Renders the header for the MicroStrategy connector documentation, specifying its production stage and available/unavailable features.

```typescript
<ConnectorDetailsHeader icon="/public/images/connectors/microstrategy.webp" name="MicroStrategy" stage="PROD" availableFeatures={["Dashboards", "Charts", "Owners", "Datamodels", "Lineage"]} unavailableFeatures={["Tags", "Projects"]} />
```

--------------------------------

### Metabase Connector Details Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/metabase/yaml

Example usage of the ConnectorDetailsHeader component for the Metabase connector, specifying its icon, name, stage, and feature availability.

```javascript
<ConnectorDetailsHeader icon="/public/images/connectors/metabase.webp" name="Metabase" stage="PROD" availableFeatures={["Dashboards", "Charts", "Lineage", "Projects"]} unavailableFeatures={["Owners", "Tags", "Datamodels"]} />
```

--------------------------------

### List Versions Response Example

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/dashboard-services/versions

Example JSON response when listing all versions of a dashboard service. The 'versions' field contains a list of JSON strings, each representing a version of the service.

```JSON
{
  "entityType": "dashboardService",
  "versions": [
    "{\"id\":\"2c0c7c05-d820-4bea-a471-047deb7f92fd\",\"name\":\"sample_looker\",\"fullyQualifiedName\":\"sample_looker\",\"version\":0.2,\"description\":\"Updated Looker production instance\",\"serviceType\":\"Looker\"}",
    "{\"id\":\"2c0c7c05-d820-4bea-a471-047deb7f92fd\",\"name\":\"sample_looker\",\"fullyQualifiedName\":\"sample_looker\",\"version\":0.1,\"serviceType\":\"Looker\"}"
  ]
}
```

--------------------------------

### List Test Suites with Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-quality/test-suites/list

Demonstrates how to list test suites using the OpenMetadata Python SDK. Includes examples for fetching the first page, iterating through all suites with auto-pagination, and filtering by test suite type.

```python
from metadata.sdk import configure
from metadata.sdk.entities import TestSuites

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# List first page
suites = TestSuites.list(limit=50)
for ts in suites.data:
    print(f"{ts.displayName} (executable: {ts.executable})")

# List all with auto-pagination
for ts in TestSuites.list_all():
    print(f"{ts.fullyQualifiedName}")

# Filter by type
logical_suites = TestSuites.list(
    testSuiteType="logical",
    fields=["owners", "tests"],
    limit=50
)

for ts in logical_suites.data:
    print(f"{ts.displayName}")

```

--------------------------------

### Start OpenMetadata Docker Compose with SSO Configuration

Source: https://docs.open-metadata.org/v1.12.x/deployment/security/one-login/docker

Use the docker compose command with the --env-file flag to start the OpenMetadata service using the previously created environment file for One Login SSO.

```bash
docker compose --env-file ~/openmetadata_onelogin.env up -d

```

--------------------------------

### Install OpenMetadata Ingestion

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/airflow/lineage-operator

Install the openmetadata-ingestion package to use the Lineage Operator. Ensure the client version matches your OpenMetadata server version. Requires version 0.13.1 or higher.

```bash
pip3 install "openmetadata-ingestion==x.y.z"
```

--------------------------------

### List Topics

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/topics/list

This example demonstrates how to list topics, filtering by a specific service and requesting additional fields like owners and tags. It also shows how to iterate through the returned topics and access their properties.

```APIDOC
## GET /api/v1/topics

### Description
List all topics with optional filtering and pagination.

### Method
GET

### Endpoint
/api/v1/topics

### Parameters
#### Query Parameters
- **service** (string) - Optional - Filter by messaging service fully qualified name.
- **limit** (integer) - Optional - Maximum number of results to return (max: 1000000). Defaults to 10.
- **before** (string) - Optional - Cursor for backward pagination.
- **after** (string) - Optional - Cursor for forward pagination.
- **fields** (string) - Optional - Comma-separated list of fields to include: `owners`, `tags`, `followers`, `votes`, `extension`, `domains`, `sourceHash`. See Supported Fields below.
- **include** (string) - Optional - Include `all`, `deleted`, or `non-deleted` entities. Defaults to `non-deleted`.

### Response
#### Success Response (200)
- **data** (array) - Array of topic objects.
  - **id** (string) - Unique identifier for the topic (UUID format).
  - **name** (string) - Topic name.
  - **fullyQualifiedName** (string) - Fully qualified name in format `service.topicName`.
  - **displayName** (string) - Human-readable display name.
  - **service** (object) - Reference to the parent messaging service.
  - **serviceType** (string) - Type of messaging service (e.g., Kafka, Redpanda, Kinesis).
  - **messageSchema** (object) - Schema definition for messages in the topic.
  - **partitions** (integer) - Number of partitions.
  - **cleanupPolicies** (array) - Cleanup policies for the topic.
  - **replicationFactor** (integer) - Replication factor.
  - **owners** (array) - List of owners assigned to the topic. Only included when `fields` contains `owners`.
  - **tags** (array) - Classification tags applied. Only included when `fields` contains `tags`.
  - **domains** (array) - Domain assignments for governance. Only included when `fields` contains `domains`.
  - **followers** (array) - Users following this topic. Only included when `fields` contains `followers`.
  - **votes** (object) - User votes and ratings. Only included when `fields` contains `votes`.
  - **extension** (object) - Custom properties. Only included when `fields` contains `extension`.
- **paging** (object) - Pagination information.
  - **total** (integer) - Total count of topics matching the query.
  - **after** (string) - Cursor for the next page of results. Null if this is the last page.
  - **before** (string) - Cursor for the previous page of results. Null if this is the first page.

### Request Example
```python
topics = Topics.list(
    service="sample_kafka",
    fields=["owners", "tags", "domain"],
    limit=50
)

for t in topics.data:
    print(f"{t.fullyQualifiedName}")
    if t.owners:
        print(f"  Owners: {[o.name for o in t.owners]}")
    if t.tags:
        print(f"  Tags: {[t.tagFQN for t in t.tags]}")
```

### Response Example
```json
{
  "data": [
    {
      "id": "0a021819-982e-4ee4-a5a2-4af30eaa3016",
      "name": "address_book",
      "fullyQualifiedName": "sample_kafka.address_book",
      "description": "All Protobuf record related events gets captured in this topic",
      "version": 0.1,
      "updatedAt": 1769982663546,
      "updatedBy": "admin",
      "service": {
        "id": "469ef25e-9bdf-4d5f-8553-eb0ce8581f30",
        "type": "messagingService",
        "name": "sample_kafka",
        "fullyQualifiedName": "sample_kafka",
        "displayName": "sample_kafka",
        "deleted": false
      },
      "serviceType": "Kafka",
      "messageSchema": {
        "schemaText": "syntax = \"proto2\";\npackage tutorial;\nmessage Person { ... }",
        "schemaType": "Protobuf",
        "schemaFields": [
          {
            "name": "AddressBook",
            "dataType": "RECORD",
            "fullyQualifiedName": "sample_kafka.address_book.AddressBook",
            "children": []
          }
        ]
      },
      "partitions": 1,
      "cleanupPolicies": ["delete"],
      "replicationFactor": 1,
      "maximumMessageSize": 1,
      "retentionSize": -1,
      "deleted": false,
      "owners": [],
      "tags": [],
      "domains": []
    }
  ],
  "paging": {
    "after": "...",
    "total": 12
  }
}
```
```

--------------------------------

### Simple Container Configuration

Source: https://docs.open-metadata.org/v1.12.x/connectors/storage

Configure a basic container without partitions. Requires dataPath and structureFormat. Optionally specify a separator for delimited files.

```json
{
  "containerId": "my-container",
  "dataPath": "s3://my-bucket/my-data/",
  "structureFormat": {
    "name": "parquet"
  }
}
```

--------------------------------

### Start Docker Compose with JWT Configuration

Source: https://docs.open-metadata.org/deployment/security/enable-jwt-tokens

Run this command to start your Docker services using the specified compose file and environment file, which includes your JWT key configurations.

```bash
docker compose -f docker-compose.yml --env-file openmetadata.prod.env up -d
```

--------------------------------

### Install Superset Ingestion Dependencies

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/superset/yaml

Install the necessary Python package for the Superset ingestion connector. This command ensures all required dependencies are included.

```bash
pip3 install "openmetadata-ingestion[superset]"
```

--------------------------------

### Configure Okta SSO Client

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/java

Set up the Okta SSO client configuration with your Okta credentials. Ensure the Org URL includes the '/v1/token' path.

```java
OktaSSOClientConfig oktaSSOClientConfig = new OktaSSOClientConfig();
oktaSSOClientConfig.setClientId("{client_id}");
oktaSSOClientConfig.setOrgURL("{org_url}/v1/token");
oktaSSOClientConfig.setPrivateKey("{public/private keypair}");
oktaSSOClientConfig.setEmail("{email}");
oktaSSOClientConfig.setScopes({scope_list});
```

```java
server.setAuthProvider(OpenMetadataServerConnection.AuthProvider.OKTA);
server.setSecurityConfig(oktaSSOClientConfig);
```

--------------------------------

### Soft Delete User Response Example

Source: https://docs.open-metadata.org/v1.12.x/api-reference/teams-and-users/users/delete

Example JSON response after performing a soft delete operation on a user.

```json
{
  "id": "77655e6e-ad33-49da-bbca-db4ba4d4e2cd",
  "name": "aaron_johnson0",
  "fullyQualifiedName": "aaron_johnson0",
  "displayName": "Aaron Johnson",
  "version": 0.2,
  "updatedAt": 1769982624214,
  "updatedBy": "admin",
  "email": "aaron_johnson0@gmail.com",
  "isBot": false,
  "isAdmin": false,
  "allowImpersonation": false,
  "teams": [
    {
      "id": "7a2b921b-f623-4eb5-9736-649788ad842c",
      "type": "team",
      "name": "Sales",
      "fullyQualifiedName": "Sales"
    }
  ],
  "deleted": true,
  "roles": [
    {
      "id": "761c2bb2-0b77-4bc5-9af9-cf89536d6a12",
      "type": "role",
      "name": "DataSteward",
      "fullyQualifiedName": "DataSteward"
    }
  ],
  "domains": []
}

```

--------------------------------

### Install Metabase Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/metabase/yaml

Install the necessary Python packages for the Metabase ingestion connector. This command ensures all dependencies for Metabase are included.

```bash
pip3 install "openmetadata-ingestion[metabase]"
```

--------------------------------

### Exported Pipeline Service Data Example

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/pipeline-services/import-export

Example of the CSV data format for exported pipeline service metadata.

```csv
"name,displayName,description,owner,tags,domain\ndbt_analytics_customers,DBT Customer Analytics,Analytics pipeline for customer data,team:data-engineering,Tier.Tier1,,"
```

--------------------------------

### Soft Delete Response Example

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/pipeline-services/delete

Example JSON response after a successful soft delete operation on a pipeline service.

```json
{
  "id": "daa58a49-df05-48a3-a417-45dfd12eacf5",
  "name": "sample_airflow",
  "fullyQualifiedName": "sample_airflow",
  "serviceType": "Airflow",
  "version": 0.2,
  "updatedAt": 1769982621418,
  "updatedBy": "admin",
  "deleted": true,
  "owners": [],
  "tags": [],
  "domains": []
}

```

--------------------------------

### Example Exported CSV Data

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/database-schemas/import-export

This is an example of the CSV data format returned when exporting database schema metadata.

```csv
"name,displayName,description,owner,tags,retentionPeriod,sourceUrl,domain\nusers,Users Table,User account data,team:data-engineering,Tier.Tier1,,,"
```

--------------------------------

### Enable Nginx Site and Restart

Source: https://docs.open-metadata.org/v1.12.x/deployment/security/enable-ssl/nginx

Links the new Nginx configuration to the sites-enabled directory and restarts the Nginx service to apply changes.

```bash
sudo ln -s /etc/nginx/sites-available/openmetadata /etc/nginx/sites-enabled/openmetadata
sudo systemctl restart nginx
```

--------------------------------

### Install OpenMetadata Ingestion with Multiple Features

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/data-quality-observability/quality/data-quality-as-code/getting-started

Combine multiple extras for comprehensive support, such as DataFrame validation with database connectivity or ETL capabilities.

```bash
# For DataFrame validation with Postgres support
pip install "openmetadata-ingestion[pandas,postgres]>=1.12.0.0"

# For comprehensive ETL support
pip install "openmetadata-ingestion[pandas,postgres,pyarrow]>=1.12.0.0"
```

--------------------------------

### Install OpenMetadata Dependencies Helm Chart

Source: https://docs.open-metadata.org/v1.12.x/deployment/kubernetes/on-prem

Command to install the OpenMetadata dependencies Helm chart using a custom values file for persistent storage configuration.

```command-line
helm install openmetadata-dependencies open-metadata/openmetadata-dependencies --values values-dependencies.yaml
```

--------------------------------

### dbt manifest.json Owner Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/dbt/ingest-dbt-owner

Sample manifest.json node showing owner information under metadata->owner.

```json
"model.jaffle_shop.orders": {
			"metadata": {
				"type": "BASE TABLE",
				"schema": "dbt_jaffle",
				"name": "orders",
				"database": "dev",
				"comment": null,
				"owner": "openmetadata_team"
			}
}
```

--------------------------------

### Create SingleStore User and Grant Permissions

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/singlestore

Use these SQL commands to create a new user and grant them the necessary SELECT privileges on databases or specific objects for metadata extraction and data quality checks.

```sql
CREATE USER <username>[@<hostName>] IDENTIFIED BY '<password>';
```

```sql
GRANT SELECT ON world.* TO '<username>';
```

```sql
GRANT SELECT ON world.hello TO '<username>';
```

--------------------------------

### Create Data Product (POST variant)

Source: https://docs.open-metadata.org/v1.12.x/api-reference/governance/data-products

Use the POST method to create a new data product. This is a non-idempotent variant for creation.

```bash
POST /v1/dataProducts
```

--------------------------------

### Manage Data Product Ports and Assets with Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/governance/data-products/ports-assets

Use the Python SDK to configure your connection and then add or remove input ports, output ports, and assets for a data product. Ensure you have the correct data product ID and asset/port identifiers.

```python
from metadata.sdk import configure
from metadata.sdk.entities import DataProducts

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# Add input ports
DataProducts.add_input_ports(
    "b1839f98-f046-5f35-bdef-20f9b3395cb2",
    [{"id": "table-uuid-1", "type": "table"}]
)

# Remove input ports
DataProducts.remove_input_ports(
    "b1839f98-f046-5f35-bdef-20f9b3395cb2",
    [{"id": "table-uuid-1", "type": "table"}]
)

# Add output ports
DataProducts.add_output_ports(
    "b1839f98-f046-5f35-bdef-20f9b3395cb2",
    [{"id": "dashboard-uuid-1", "type": "dashboard"}]
)

# Remove output ports
DataProducts.remove_output_ports(
    "b1839f98-f046-5f35-bdef-20f9b3395cb2",
    [{"id": "dashboard-uuid-1", "type": "dashboard"}]
)

# Add assets
DataProducts.add_assets(
    "b1839f98-f046-5f35-bdef-20f9b3395cb2",
    [{"id": "table-uuid-2", "type": "table"}]
)

# Remove assets
DataProducts.remove_assets(
    "b1839f98-f046-5f35-bdef-20f9b3395cb2",
    [{"id": "table-uuid-2", "type": "table"}]
)

```

--------------------------------

### List Test Cases

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-quality/test-cases/list

This example demonstrates how to list test cases, filtering by entity link and requesting specific fields.

```APIDOC
## GET /api/v1/testcases

### Description
List all test cases with optional filtering and pagination.

### Method
GET

### Endpoint
/api/v1/testcases

### Query Parameters
- **limit** (integer) - Optional - Maximum number of results to return (max: 1000000). Defaults to "10".
- **before** (string) - Optional - Cursor for backward pagination.
- **after** (string) - Optional - Cursor for forward pagination.
- **fields** (string) - Optional - Comma-separated list of fields to include: `owners`, `testSuite`, `testDefinition`, `testCaseResult`.
- **include** (string) - Optional - Include `all`, `deleted`, or `non-deleted` entities. Defaults to "non-deleted".
- **testSuiteId** (string) - Optional - Filter by test suite UUID.
- **entityLink** (string) - Optional - Filter by entity link (URL-encoded). Returns test cases for a specific table or column.
- **includeAllTests** (boolean) - Optional - Include test cases from all test suites, not just the primary executable suite. Defaults to "false".
- **orderByLastExecutionDate** (boolean) - Optional - Order results by the most recent test execution date. Defaults to "false".

### Response
#### Success Response (200)
- **data** (array) - Array of test case objects.
  - **id** (string) - Unique identifier for the test case (UUID format).
  - **name** (string) - Test case name.
  - **fullyQualifiedName** (string) - Fully qualified name of the test case.
  - **entityLink** (string) - Entity link to the target table or column.
  - **testDefinition** (object) - Reference to the test definition. Only included when `fields` contains `testDefinition`.
  - **testSuite** (object) - Reference to the test suite. Only included when `fields` contains `testSuite`.
  - **parameterValues** (array) - Parameter values for this test case.
  - **testCaseResult** (object) - Most recent test result. Only included when `fields` contains `testCaseResult`.
  - **owners** (array) - List of owners. Only included when `fields` contains `owners`.
- **paging** (object) - Pagination information.
  - **total** (integer) - Total count of test cases matching the query.
  - **after** (string) - Cursor for the next page of results.
  - **before** (string) - Cursor for the previous page of results.

### Response Example
```json
{
  "data": [
    {
      "id": "c1bce355-fa2f-48c6-ab4d-fad722a56ed7",
      "name": "column_value_max_to_be_between",
      "fullyQualifiedName": "sample_data.ecommerce_db.shopify.dim_address.shop_id.column_value_max_to_be_between",
      "version": 0.1,
      "updatedAt": 1769982759035,
      "updatedBy": "admin",
      "testDefinition": {
        "id": "def-id",
        "type": "testDefinition",
        "name": "columnValueMaxToBeBetween",
        "fullyQualifiedName": "columnValueMaxToBeBetween",
        "deleted": false
      },
      "testSuite": {
        "id": "suite-id",
        "type": "testSuite",
        "name": "b5fcae09-02c2-4c0b-8c4a-5b52d650e592",
        "deleted": false
      },
      "entityLink": "<#E::table::sample_data.ecommerce_db.shopify.dim_address::columns::shop_id>",
      "parameterValues": [
        {"name": "minValueForMaxInCol", "value": "1"},
        {"name": "maxValueForMaxInCol", "value": "100"}
      ],
      "deleted": false,
      "owners": []
    }
  ],
  "paging": {
    "after": "...",
    "total": 8
  }
}
```

### Error Handling
- **401** - `UNAUTHORIZED`: Invalid or missing authentication token.
- **403** - `FORBIDDEN`: User lacks permission to list test cases.
```

--------------------------------

### Install KafkaConnect Ingestion

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/kafkaconnect/yaml

Install the KafkaConnect ingestion package using pip. Ensure you are using Python versions 3.9-3.11.

```bash
pip3 install "openmetadata-ingestion[kafkaconnect]"
```

--------------------------------

### AzureSQL Connector Instance

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/azuresql/yaml

Example of how to render the ConnectorDetailsHeader component for the AzureSQL connector. This sets up the basic information displayed for the connector.

```javascript
<ConnectorDetailsHeader icon="/public/images/connectors/azuresql.webp" name="AzureSQL" stage="PROD" availableFeatures={["Metadata", "Query Usage", "Lineage", "Column-level Lineage", "Data Profiler", "Data Quality", "dbt", "Sample Data", "Auto-Classification"]} unavailableFeatures={["Stored Procedures", "Owners", "Tags"]} />
```

--------------------------------

### Install GCS Requirements (OpenMetadata < 0.13)

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/gcs-datalake/yaml

Install the necessary requirements for GCS ingestion if your OpenMetadata version is less than 0.13.

```bash
pip3 install "openmetadata-ingestion[datalake]"
```

--------------------------------

### Initialize OpenMetadata Java Client

Source: https://docs.open-metadata.org/v1.12.x/api-reference/getting-started

Initialize the OpenMetadata client in Java by creating a configuration object with the server URL and access token, then instantiating the client.

```java
import org.openmetadata.sdk.client.OpenMetadataClient;
import org.openmetadata.sdk.config.OpenMetadataConfig;

OpenMetadataConfig config = OpenMetadataConfig.builder()
    .serverUrl("https://your-company.open-metadata.org/api")
    .accessToken("your-jwt-token")
    .build();

OpenMetadataClient client = new OpenMetadataClient(config);
```

--------------------------------

### Creating a Table

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/ingestion/tags

Example of creating a table with a single column using the Python SDK.

```APIDOC
## Creating a Table

We are doing a simple example with a single column.

```python
from metadata.generated.schema.api.data.createTable import CreateTableRequest
from metadata.generated.schema.entity.data.table import Column, DataType

table = CreateTableRequest(
    name="my_table",
    databaseSchema=create_schema_entity.fullyQualifiedName,
    columns=[Column(name="id", dataType=DataType.BIGINT)],
)

table = metadata.create_or_update(data=table)
```
```

--------------------------------

### Create Table via REST API (POST /api/v1/tables)

**IMPORTANT:** When creating a table via the REST API, the request body requires
`databaseSchema` (the fully-qualified name of the schema, e.g. `service.database.schema`).
The field `database` is only present in GET responses as a resolved reference —
it is NOT accepted in POST/PUT request bodies and will cause HTTP 400.

```bash
curl -X POST "http://localhost:8585/api/v1/tables" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_table",
    "displayName": "My Table",
    "description": "A sample table.",
    "databaseSchema": "my_service.my_database.my_schema",
    "tableType": "Regular",
    "columns": [
      {"name": "id",   "dataType": "BIGINT",  "description": "Primary key"},
      {"name": "name", "dataType": "VARCHAR", "dataLength": 255, "description": "Name field"}
    ]
  }'
```

Required fields for CreateTable:
- `name` (string) — table name
- `databaseSchema` (string) — fully-qualified schema name: `service.database.schema`
- `columns` (array) — at minimum `[{"name": "...", "dataType": "..."}]`

Optional but recommended:
- `displayName`, `description`, `tableType` ("Regular", "View", "External", etc.)

DO NOT include `database` in the POST body — it will cause HTTP 400.

--------------------------------

### Metadata Automation Example

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/overview

Illustrates how to automate metadata updates by iterating through all tables, adding a description if it's missing, and then updating the table.

```APIDOC
## Metadata Automation Example

### Description
Illustrates how to automate metadata updates by iterating through all tables, adding a description if it's missing, and then updating the table.

### Code
```python
from metadata.sdk import Tables

# Bulk update table descriptions
for table in Tables.list().auto_paging_iterable():
    if not table.description:
        table.description = f"Production table: {table.name}"
        Tables.update(str(table.id), table)
```
```

--------------------------------

### provider_registry.google_auth_init

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/api-reference

Initialize authentication with Google.

```APIDOC
## google_auth_init

### Description
Initializes authentication using Google.

### Method
provider_registry.google_auth_init()
```

--------------------------------

### Install dbt Ingestion Package

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/dbt/run-dbt-workflow-externally

Install the necessary package to run the dbt ingestion. Supports Python versions 3.9-3.11.

```bash
pip3 install "openmetadata-ingestion[dbt]"
```

--------------------------------

### SFTP Source with Username/Password Authentication

Source: https://docs.open-metadata.org/v1.12.x/connectors/drive/sftp/yaml

Example of SFTP source configuration using username and password for authentication.

```yaml
source:
  type: sftp
  serviceName: sftp_prod
  serviceConnection:
    config:
      type: Sftp
      host: sftp.example.com
      port: 22
      authType:
        username: sftp_user
        password: your_secure_password
      rootDirectories:
        - /data/exports
        - /data/reports
```

--------------------------------

### Run Connector from CLI

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/developing-a-new-connector/test-it

Test your connector using the CLI after ensuring the OpenMetadata stack is running locally and the ingestion package is installed.

```bash
metadata ingest -c {your_yaml_file}
```

--------------------------------

### Example Language JSON Structure

Source: https://docs.open-metadata.org/v1.12.x/developers/how-to-add-language-support

This is an example of how a language JSON file is structured for internationalization. It maps keys to translated strings.

```json
{
  "home.welcome": "Bienvenue",
  "table.title": "Tables",
  ...
}
```

--------------------------------

### Install Entity Recognition Model

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/data-governance/classification/auto-classification/auto-pii-tagging

Manually install the Entity Recognition model if you encounter SSL certificate verification errors when the profiler tries to download it. This command should be run on the ingestion container or Airflow host.

```bash
pip --trusted-host github.com --trusted-host objects.githubusercontent.com install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.5.0/en_core_web_md-3.5.0.tar.gz

```

--------------------------------

### Airbyte Connector Header Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/airbyte

Renders the header for the Airbyte connector documentation, specifying its icon, name, production stage, and available/unavailable features. This is a direct usage example of the ConnectorDetailsHeader component.

```javascript
<ConnectorDetailsHeader icon="/public/images/connectors/airbyte.webp" name="Airbyte" stage="PROD" availableFeatures={["Pipelines", "Pipeline Status", "Lineage"]} unavailableFeatures={["Owners", "Tags"]} />
```

--------------------------------

### Soft Delete Response Example (JSON)

Source: https://docs.open-metadata.org/v1.12.x/api-reference/governance/domains/delete

Example JSON response when a domain is soft-deleted. The 'deleted' field will be set to true.

```json
{
  "id": "a0729e98-e946-4e25-acde-10e8a2294ba1",
  "domainType": "Aggregate",
  "name": "TestDomain",
  "fullyQualifiedName": "TestDomain",
  "description": "Lorem ipsum...",
  "version": 0.2,
  "updatedAt": 1769984330261,
  "updatedBy": "admin",
  "deleted": true,
  "owners": [],
  "children": []
}
```

--------------------------------

### Sample Response for Create Glossary

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/mcp/reference

This is a sample response confirming the successful creation of a glossary, including its details and next steps.

```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "✅ Successfully created glossary: **Marketing Terms**\n\n**Details**:\n- **Name**: Marketing Terms\n- **Description**: Collection of marketing-related terms and definitions used across campaigns, analytics, and reporting\n- **Owners**: marketing-team, alice.smith@company.com\n- **Reviewers**: data-governance-team\n- **Mutually Exclusive**: No\n- **Status**: Active\n\n**Next Steps**:\n- You can now add glossary terms to this glossary\n- Consider creating hierarchical terms for better organization\n- Set up approval workflows if needed\n\n[View Glossary in OpenMetadata](https://your-om.com/glossary/marketing-terms)"
      }
    ]
  }
}
```

--------------------------------

### Soft Delete Response Example

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/mlmodel-services/delete

Example JSON response after a successful soft delete operation on an ML Model Service.

```json
{
  "id": "ca22d46e-81b9-4e48-85b5-0adc44980da9",
  "name": "mlflow_svc",
  "fullyQualifiedName": "mlflow_svc",
  "serviceType": "Mlflow",
  "version": 0.2,
  "updatedAt": 1769982621618,
  "updatedBy": "admin",
  "connection": {
    "config": {
      "type": "Mlflow",
      "trackingUri": "http://localhost:8088",
      "registryUri": "http://localhost:8088",
      "supportsMetadataExtraction": true
    }
  },
  "owners": [],
  "tags": [],
  "deleted": true,
  "domains": []
}

```

--------------------------------

### Create Data Product using Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/governance/data-products/create

Use the Python SDK to create a new data product. Ensure you have configured the SDK with your host and JWT token. The request body includes essential details like name, domain, and description.

```python
from metadata.sdk import configure
from metadata.sdk.entities import DataProducts

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

request = {
    "name": "CustomerInsights",
    "displayName": "Customer Insights",
    "domain": "Marketing",
    "description": "Curated customer analytics data product"
}

data_product = DataProducts.create(request)
print(f"Created: {data_product.fullyQualifiedName}")

```

--------------------------------

### Lightdash Connector Header Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/lightdash

An example of how to use the ConnectorDetailsHeader component to display information for the Lightdash connector. It specifies the icon, name, stage, and lists available and unavailable features.

```javascript
<ConnectorDetailsHeader icon="/public/images/connectors/lightdash.webp" name="Lightdash" stage="PROD" availableFeatures={["Dashboards", "Charts", "Owners", "Datamodels", "Lineage"]} unavailableFeatures={["Tags", "Projects"]} />
```

--------------------------------

### Prepare OpenMetadata Database and Indexes

Source: https://docs.open-metadata.org/v1.12.x/deployment/bare-metal

This command generates necessary tables and indexes. Warning: it will drop existing data in the database.

```bash
./bootstrap/openmetadata-ops.sh drop-create
```

--------------------------------

### Install AWS Dependencies for Secrets Manager

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/data-quality-observability/quality/data-quality-as-code/test-runner

Install the necessary openmetadata-ingestion package with AWS support for integrating with AWS Secrets Manager.

```bash
pip install "openmetadata-ingestion[aws]">=1.12.0.0
```

--------------------------------

### List All Databases with Auto-Pagination

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/databases/list

Demonstrates how to list all databases using auto-pagination. This is useful for iterating through a large number of databases without manually managing cursors.

```python
all_databases = Databases.list_all(batch_size=100)
for database in all_databases:
    print(f"{database.fullyQualifiedName}")
```

--------------------------------

### Mode Connector Header Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/mode

An example of how to use the ConnectorDetailsHeader component to display information for the Mode connector. It specifies the icon, name, stage, and lists available and unavailable features.

```javascript
<ConnectorDetailsHeader icon="/public/images/connectors/mode.webp" name="Mode" stage="PROD" availableFeatures={["Dashboards", "Charts", "Lineage"]} unavailableFeatures={["Owners", "Tags", "Datamodels", "Projects"]} />
```

--------------------------------

### provider_registry.auth0_auth_init

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/api-reference

Initialize authentication with Auth0.

```APIDOC
## auth0_auth_init

### Description
Initializes authentication using Auth0.

### Method
provider_registry.auth0_auth_init()
```

--------------------------------

### Install MLflow Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/ml-model/mlflow/yaml

Install the necessary package for MLflow ingestion. This command ensures that all dependencies for the MLflow connector are available.

```bash
pip3 install "openmetadata-ingestion[mlflow]"
```

--------------------------------

### Implement Connector with Windsurf

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/developing-a-new-connector/ai-assisted-development/install-skills

After scaffolding a new connector, use Windsurf by pointing it to the `CONNECTOR_CONTEXT.md` file and instructing it to implement all TODO items in the generated skeleton files.

```text
Read this CONNECTOR_CONTEXT.md and implement all TODO items
in the generated skeleton files.
```

--------------------------------

### Install S3 Datalake Ingestion (OpenMetadata > 0.13)

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/s3-datalake/yaml

Install the Datalake ingestion package for S3 if your OpenMetadata version is greater than 0.13.

```bash
pip3 install "openmetadata-ingestion[datalake-s3]"
```

--------------------------------

### Install DB2 Connector in Docker

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/db2

Install the DB2 connector within the OpenMetadata ingestion container using Docker. This command ensures the necessary Python package is available.

```bash
docker exec -it openmetadata_ingestion pip install '.[db2]'
```

--------------------------------

### Install/Upgrade OpenMetadata Helm Release

Source: https://docs.open-metadata.org/v1.12.x/deployment/kubernetes/eks/airflow

Use this command to install or upgrade your OpenMetadata Helm release. Ensure you have a `values.yaml` file for custom configurations.

```bash
helm upgrade --install openmetadata open-metadata/openmetadata--values values.yaml

```

--------------------------------

### Start Docker Compose Deployment

Source: https://docs.open-metadata.org/v1.12.x/deployment/upgrade/docker

Command to start the OpenMetadata Docker Compose services after replacing the docker-compose.yml file. The '-d' flag runs the containers in detached mode.

```bash
docker compose -f docker-compose.yml up -d
```

--------------------------------

### Install PinotDB Ingestion

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/pinotdb/yaml

Install the necessary Python package for PinotDB ingestion. This command ensures all dependencies for the PinotDB connector are included.

```bash
pip3 install "openmetadata-ingestion[pinotdb]"
```

--------------------------------

### Install Glue Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/glue/yaml

Install the necessary Python packages for the Glue ingestion. Ensure your Python version is between 3.9 and 3.11.

```bash
pip3 install "openmetadata-ingestion[glue]"
```

--------------------------------

### Install Databricks Ingestion Package

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/databricks/yaml

Install the necessary Python package for Databricks ingestion. This command ensures you have the Databricks connector and its dependencies.

```bash
pip3 install "openmetadata-ingestion[databricks]"
```

--------------------------------

### Create a Test Suite

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-quality/test-suites

Use this endpoint to create a new test suite. This is a POST request to the /v1/dataQuality/testSuites endpoint.

```bash
curl -X POST \
  http://localhost:8585/v1/dataQuality/testSuites \
  -H 'Content-Type: application/json' \
  -d '{ 
    "name": "api_test_suite", 
    "displayName": "API Test Suite", 
    "description": "This is a test suite created via API", 
    "executable": false 
  }'
```

--------------------------------

### Get User by Fully Qualified Name (FQN)

Source: https://docs.open-metadata.org/v1.12.x/api-reference/teams-and-users/users

Retrieve a user by their Fully Qualified Name (FQN) using the GET method. The FQN format is typically 'username'.

```shell
GET /v1/users/name/{fqn}
```

--------------------------------

### Check Docker Version

Source: https://docs.open-metadata.org/latest/quick-start/local-docker-deployment

Verify if Docker is installed and meets the minimum version requirement (20.10.0 or greater).

```bash
docker --version

```

--------------------------------

### Start Docker Compose with Custom OIDC Configuration

Source: https://docs.open-metadata.org/v1.12.x/deployment/security/custom-oidc/docker

Use the `docker compose` command with the `--env-file` flag to start your OpenMetadata services using the custom OIDC environment configuration.

```bash
docker compose --env-file ~/openmetadata_oidc.env up -d

```

--------------------------------

### Install BigQuery Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/bigquery/yaml

Install the necessary Python package for BigQuery ingestion. This command ensures you have the BigQuery connector and its dependencies.

```bash
pip3 install "openmetadata-ingestion[bigquery]"
```

--------------------------------

### Create OpenMetadata OIDC Environment File

Source: https://docs.open-metadata.org/v1.12.x/deployment/security/custom-oidc/docker

Create an `openmetadata_oidc.env` file and populate it with your OIDC provider details. Ensure to update placeholders like domain, client ID, and realm.

```env
# OpenMetadata Server Authentication Configuration
AUTHORIZER_CLASS_NAME=org.openmetadata.service.security.DefaultAuthorizer
AUTHORIZER_REQUEST_FILTER=org.openmetadata.service.security.JwtFilter
AUTHORIZER_ADMIN_PRINCIPALS=[admin]  # Your `name` from name@domain.com
AUTHORIZER_PRINCIPAL_DOMAIN=open-metadata.org # Update with your domain

AUTHENTICATION_PROVIDER=custom-oidc
CUSTOM_OIDC_AUTHENTICATION_PROVIDER_NAME=KeyCloak
AUTHENTICATION_PUBLIC_KEYS=[http://localhost:8080/realms/myrealm/protocol/openid-connect/certs, https://{your domain}/api/v1/system/config/jwks] # Update with your Domain and Make sure this "/api/v1/system/config/jwks" is always configured to enable JWT tokens
AUTHENTICATION_AUTHORITY={http://localhost:8080/realms/myrealm}
AUTHENTICATION_CLIENT_ID={Client ID} # Update with your Client ID
AUTHENTICATION_CALLBACK_URL=http://localhost:8585/callback

```

--------------------------------

### Stored Procedure Creation Response Example

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/stored-procedures/create

This is an example of the JSON response received after successfully creating a stored procedure. It includes details like the procedure's ID, name, fully qualified name, description, code, version, and associated metadata.

```JSON
{
  "id": "d02b24fa-a246-4563-adf1-9ad21f251c0e",
  "name": "calculate_average",
  "fullyQualifiedName": "sample_data.ecommerce_db.shopify.calculate_average",
  "description": "Procedure to calculate average",
  "storedProcedureCode": {
    "code": "CREATE OR REPLACE PROCEDURE calculate_average(numbers INT ARRAY) RETURNS FLOAT NOT NULL LANGUAGE SQL AS $$DECLARE sum_val INT = 0;count_val INT = 0;average_val FLOAT;BEGIN\n  FOR num IN ARRAY numbers DO sum_val := sum_val + num;\n  count_val := count_val + 1;\nEND FOR;\nIF count_val = 0 THEN\n  average_val := 0.0;\nELSE\n  average_val := sum_val / count_val;\nEND IF;\nRETURN average_val;\nEND;$$;"
  },
  "version": 0.1,
  "updatedAt": 1769982660822,
  "updatedBy": "admin",
  "storedProcedureType": "StoredProcedure",
  "href": "http://localhost:8585/api/v1/storedProcedures/d02b24fa-a246-4563-adf1-9ad21f251c0e",
  "databaseSchema": {
    "id": "4dd30184-009c-4792-b296-9562eaed651f",
    "type": "databaseSchema",
    "name": "shopify",
    "fullyQualifiedName": "sample_data.ecommerce_db.shopify",
    "description": "This **mock** database contains schema related to shopify sales and orders with related dimension tables.",
    "displayName": "shopify",
    "deleted": false,
    "href": "http://localhost:8585/api/v1/databaseSchemas/4dd30184-009c-4792-b296-9562eaed651f"
  },
  "database": {
    "id": "0be090de-0941-48c4-af49-a6157c91cda0",
    "type": "database",
    "name": "ecommerce_db",
    "fullyQualifiedName": "sample_data.ecommerce_db",
    "description": "This **mock** database contains schemas related to shopify sales and orders with related dimension tables.",
    "displayName": "ecommerce_db",
    "deleted": false,
    "href": "http://localhost:8585/api/v1/databases/0be090de-0941-48c4-af49-a6157c91cda0"
  },
  "serviceType": "BigQuery",
  "deleted": false,
  "owners": [],
  "tags": [],
  "domains": [],
  "processedLineage": false,
  "entityStatus": "Unprocessed"
}

```

--------------------------------

### dbt catalog.json Owner Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/dbt/ingest-dbt-owner

Sample catalog.json node showing owner information under metadata->owner.

```json
"model.jaffle_shop.customers": {
      "metadata": {
        "type": "BASE TABLE",
        "schema": "dbt_jaffle",
        "name": "customers",
        "database": "dev",
        "comment": null,
        "owner": "openmetadata"
      },
}
```

--------------------------------

### Looker Connector Header Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/looker

Example usage of the ConnectorDetailsHeader component for the Looker connector. Displays its production stage and supported features.

```javascript
<ConnectorDetailsHeader icon="/public/images/connectors/looker.webp" name="Looker" stage="PROD" availableFeatures={["Dashboards", "Charts", "Owners", "Datamodels", "Lineage", "Usage"]} unavailableFeatures={["Tags", "Projects"]} />
```

--------------------------------

### Exported Database Service CSV Data Example

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/database-services/import-export

An example of the CSV data format returned when exporting database service metadata.

```csv
"name,displayName,description,owner,tags,domain\nanalytics,Analytics Database,Central analytics warehouse,team:data-engineering,Tier.Tier1,,"
```

--------------------------------

### `Get` method

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/go-api-methods

The `Get` method is used to retrieve data from the OpenMetadata API. It takes a path, optional headers, and query parameters.

```APIDOC
## GET

### Description
Retrieves data from a specified OpenMetadata API endpoint.

### Method
GET

### Endpoint
[ENDPOINT]

### Parameters
#### Query Parameters
- **path** (string) - Required - The API path to retrieve data from.
- **header** (http.Header) - Optional - Custom HTTP headers.
- **extraHeader** (map[string][]string) - Optional - Additional headers.
- **queryParams** (map[string]string) - Optional - Query parameters for the request.

### Request Example
```go
path := "tables"
body, err := rest.Get(path, nil, nil, nil)
```

### Response
#### Success Response (200)
- **map[string]any** - A map representing the JSON response body.
- **error** - An error object if the request fails.
```

--------------------------------

### REST Client GET Method

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/api-reference/client

Executes a GET HTTP request to the specified path. Optional data can be provided in the request body.

```python
client.get(path, data=None)
```

--------------------------------

### Install Entity Recognition Model with Trusted Hosts

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/data-quality-observability/profiler/auto-pii-tagging

Manually download the Entity Recognition model on the ingestion container or Airflow host if you encounter SSL certificate verification errors. This command installs the model using pip, specifying trusted hosts to bypass certificate issues.

```bash
pip --trusted-host github.com --trusted-host objects.githubusercontent.com install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.5.0/en_core_web_md-3.5.0.tar.gz
```

--------------------------------

### provider_registry.ldap_auth_init

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/api-reference

Initialize authentication with LDAP.

```APIDOC
## ldap_auth_init

### Description
Initializes authentication using LDAP.

### Method
provider_registry.ldap_auth_init()
```

--------------------------------

### Install OpenSearch Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/search/opensearch/yaml

Install the necessary Python package for the OpenSearch ingestion connector. This command includes the OpenSearch extra dependencies.

```bash
pip3 install "openmetadata-ingestion[opensearch]"
```

--------------------------------

### Basic Pagination with cURL

Source: https://docs.open-metadata.org/v1.12.x/api-reference/pagination

Make a GET request to the tables endpoint with a limit parameter to get the first page. Use the 'after' cursor from the response in subsequent requests to fetch the next page of results.

```bash
# Get first page
curl -X GET "https://your-company.open-metadata.org/api/v1/tables?limit=20" \
  -H "Authorization: Bearer $TOKEN"

# Response includes paging.after cursor
# {
#   "data": [...],
#   "paging": {
#     "total": 150,
#     "after": "eyJsYXN0SWQiOiIxMjM0NTY3ODkwIn0="
#   }
# }

# Get next page using after cursor
curl -X GET "https://your-company.open-metadata.org/api/v1/tables?limit=20&after=eyJsYXN0SWQiOiIxMjM0NTY3ODkwIn0=" \
  -H "Authorization: Bearer $TOKEN"
```

--------------------------------

### Install OpenLineage Ingestion

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/openlineage/yaml

Install the necessary Python package for OpenLineage metadata ingestion. This command ensures all dependencies for the OpenLineage connector are included.

```bash
pip3 install "openmetadata-ingestion[openlineage]"
```

--------------------------------

### List API Collections with Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/api-collections/list

Demonstrates how to list API Collections, including fetching the first page, iterating through all collections with auto-pagination, and filtering by service. Ensure the SDK is configured with your host and JWT token.

```python
from metadata.sdk import configure
from metadata.sdk.entities import APICollections

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# List first page
collections = APICollections.list(limit=50)
for ac in collections.data:
    print(f"{ac.fullyQualifiedName}")

# List all with auto-pagination
for ac in APICollections.list_all():
    print(f"{ac.fullyQualifiedName}")

# Filter by service
collections = APICollections.list(
    service="sample_api_service",
    fields=["owners", "tags", "domain"],
    limit=50
)

for ac in collections.data:
    print(f"{ac.fullyQualifiedName}")
    if ac.owners:
        print(f"  Owners: {[o.name for o in ac.owners]}")
    if ac.tags:
        print(f"  Tags: {[t.tagFQN for t in ac.tags]}")

```

--------------------------------

### Install Atlas Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/metadata/atlas/yaml

Install the necessary Python package for Atlas ingestion. This command ensures all dependencies for the Atlas connector are included.

```bash
pip3 install "openmetadata-ingestion[atlas]"
```

--------------------------------

### Configure Google SSO Environment Variables

Source: https://docs.open-metadata.org/v1.12.x/deployment/security/google/docker

Create an `.env` file with the necessary Google SSO configuration. Ensure you replace placeholders like `{Client ID}` and `{your domain}` with your specific details. This file sets up authentication and authorization for OpenMetadata.

```env
# OpenMetadata Server Authentication Configuration
AUTHORIZER_CLASS_NAME=org.openmetadata.service.security.DefaultAuthorizer
AUTHORIZER_REQUEST_FILTER=org.openmetadata.service.security.JwtFilter
AUTHORIZER_ADMIN_PRINCIPALS=[admin]  # Your `name` from name@domain.com
AUTHORIZER_INGESTION_PRINCIPALS=[ingestion-bot]
AUTHORIZER_PRINCIPAL_DOMAIN=open-metadata.org # Update with your domain

AUTHENTICATION_PROVIDER=google
AUTHENTICATION_PUBLIC_KEYS=[https://www.googleapis.com/oauth2/v3/certs, https://{your domain}/api/v1/system/config/jwks] # Update with your Domain and Make sure this "/api/v1/system/config/jwks" is always configured to enable JWT tokens
AUTHENTICATION_AUTHORITY=https://accounts.google.com
AUTHENTICATION_CLIENT_ID={Client ID} # Update with your Google SSO Client ID
AUTHENTICATION_CALLBACK_URL=http://localhost:8585/callback

```

--------------------------------

### Check Pod Status

Source: https://docs.open-metadata.org/v1.12.x/deployment/kubernetes/aks

Verify that all OpenMetadata dependency pods are running correctly after installation.

```bash
kubectl get pods -n openmetadata
```

--------------------------------

### Install Kafka Ingestion Package

Source: https://docs.open-metadata.org/v1.12.x/connectors/messaging/kafka/yaml

Install the necessary Python package for Kafka ingestion. This command ensures all dependencies for the Kafka connector are included.

```bash
pip3 install "openmetadata-ingestion[kafka]"
```

--------------------------------

### List API Endpoints with Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/api-endpoints/list

Demonstrates how to list API Endpoints using the Python SDK. Includes examples for fetching the first page, listing all endpoints with auto-pagination, and filtering by API collection with specific fields.

```python
from metadata.sdk import configure
from metadata.sdk.entities import APIEndpoints

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# List first page
endpoints = APIEndpoints.list(limit=50)
for ep in endpoints.data:
    print(f"{ep.fullyQualifiedName}")

# List all with auto-pagination
for ep in APIEndpoints.list_all():
    print(f"{ep.fullyQualifiedName}")

# Filter by API collection
endpoints = APIEndpoints.list(
    apiCollection="sample_api_service.pet",
    fields=["owners", "tags", "domain"],
    limit=50
)

for ep in endpoints.data:
    print(f"{ep.fullyQualifiedName} [{ep.requestMethod}]")
    if ep.owners:
        print(f"  Owners: {[o.name for o in ep.owners]}")
    if ep.tags:
        print(f"  Tags: {[t.tagFQN for t in ep.tags]}")

```

--------------------------------

### Install Trino Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/trino/yaml

Install the necessary Python package for Trino ingestion. This command ensures all dependencies for the Trino connector are available.

```bash
pip3 install "openmetadata-ingestion[trino]"
```

--------------------------------

### Install Amundsen Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/metadata/amundsen/yaml

Install the necessary Python packages for Amundsen ingestion. This command ensures all dependencies for the Amundsen connector are available.

```bash
pip3 install "openmetadata-ingestion[amundsen]"
```

--------------------------------

### List Tables with Auto-Pagination

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/tables/list

This example demonstrates how to list all tables using the `list_all` method, which handles pagination automatically. It iterates through all tables and prints their fully qualified names.

```APIDOC
## List all with auto-pagination
all_tables = Tables.list_all(batch_size=100)
for table in all_tables:
    print(f"{table.fullyQualifiedName}")
```

--------------------------------

### Install SAS Ingestion Package

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/sas/yaml

Install the necessary Python package for SAS ingestion. This command ensures all dependencies for the SAS connector are included.

```bash
pip3 install "openmetadata-ingestion[sas]"
```

--------------------------------

### Install Presto Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/presto/yaml

Install the necessary Python package for the Presto ingestion connector. This command ensures all dependencies for Presto are included.

```bash
pip3 install "openmetadata-ingestion[presto]"
```

--------------------------------

### Kafka Connector Configuration Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/messaging/kafka/yaml

This is a sample YAML configuration for the Kafka connector. It specifies connection details, schemas, and topics to ingest.

```yaml
--- # Kafka Connection Configuration

# Kafka broker connection details
kafkaBrokers: "localhost:9092"

# Authentication details (if any)
# sasl: 
#   mechanism: "PLAIN"
#   username: "user"
#   password: "password"

# SSL configuration (if any)
# ssl: 
#   enabled: true
#   truststorePath: "/path/to/truststore.jks"
#   truststorePassword: "password"

# Topic configuration
topics:
  - name: "user_login"
    # Schema configuration for the topic
    schema: 
      type: "avro"
      # If using Avro, specify the schema registry URL
      # schemaRegistryUrl: "http://localhost:8081"
      # If schema is inline, provide it here
      # schema: "{\"type\": \"record\", \"name\": \"UserLogin\", \"fields\": [ {\"name\": \"user_id\", \"type\": \"string\"}, {\"name\": \"timestamp\", \"type\": \"long\"} ]}"
    # Message structure configuration
    messageStructure: "json"
    # Event lineage configuration
    eventLineage: true
  - name: "order_placed"
    schema:
      type: "json"
    messageStructure: "json"
    eventLineage: false

# Other connector configurations
# batchSize: 100
# pollInterval: 5000
# autoOffsetReset: "latest"
# groupId: "metadata-collector-group"

```

--------------------------------

### Install MySQL Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/mysql/yaml

Install the necessary Python package for the MySQL ingestion connector. This command ensures all dependencies for MySQL are included.

```bash
pip3 install "openmetadata-ingestion[mysql]"
```

--------------------------------

### Verify Helm Repositories

Source: https://docs.open-metadata.org/v1.12.x/quick-start/local-kubernetes-deployment

Lists all configured Helm repositories to verify that the OpenMetadata repository has been added successfully. This command helps confirm your Helm setup.

```bash
helm repo list
NAME		URL                            
open-metadata	https://helm.open-metadata.org/
```

--------------------------------

### Install Impala Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/impala/yaml

Install the necessary Python package for the Impala ingestion connector. This command ensures all dependencies for Impala are included.

```bash
pip3 install "openmetadata-ingestion[impala]"
```

--------------------------------

### List Database Services using Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/overview

Retrieve a list of all database services configured in OpenMetadata using the Python SDK. This example demonstrates basic entity listing and iteration.

```python
from metadata.sdk import DatabaseServices

# Get all database services
services = list(DatabaseServices.list().auto_paging_iterable())
print(f"Found {len(services)} database services")

```

--------------------------------

### Install Hive Connector Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/hive/yaml

Install the necessary Python package for the Hive connector. This command ensures all dependencies for Hive ingestion are included.

```bash
pip3 install "openmetadata-ingestion[hive]"
```

--------------------------------

### OpenSearch YAML Configuration Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/search/opensearch/yaml

This snippet shows a basic YAML configuration for OpenSearch, including authentication and optional SSL settings.

```yaml
authProvider: openmetadata
securityConfig:
  jwtToken: "{bot_jwt_token}"
## Store the service Connection information
storeServiceConnection: true  # false
## Secrets Manager Configuration
# secretsManagerProvider: aws, azure or noop
# secretsManagerLoader: airflow or env
## If SSL, fill the following
# verifySSL: validate  # or ignore
# sslConfig:
#   caCertificate: /local/path/to/certificate
# ingestionPipelineFQN: <service name>.<ingestion name> ## e.g., "my_redshift.metadata"
```

--------------------------------

### Install MariaDB Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/mariadb/yaml

Install the necessary Python package for the MariaDB ingestion connector. This command ensures all dependencies for MariaDB are included.

```bash
pip3 install "openmetadata-ingestion[mariadb]"
```

--------------------------------

### Check Docker Compose Version

Source: https://docs.open-metadata.org/v1.12.x/quick-start/local-docker-deployment

Verify that Docker Compose is installed and accessible.

```bash
docker compose version
```

--------------------------------

### List Containers with Filtering

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/containers/list

Demonstrates how to list containers, filtering by a specific storage service and requesting additional fields like owners, tags, and data model. It then iterates through the results to print container details.

```python
containers = Containers.list(
    service="s3_datalake",
    fields=["owners", "tags", "dataModel"],
    limit=50
)

for c in containers.data:
    print(f"{c.fullyQualifiedName}")
    if c.owners:
        print(f"  Owners: {[o.name for o in c.owners]}")
    if c.tags:
        print(f"  Tags: {[t.tagFQN for t in c.tags]}")
```

--------------------------------

### Install Greenplum Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/greenplum/yaml

Install the necessary Python package for the Greenplum ingestion. This command includes the postgres extra for Greenplum compatibility.

```bash
pip3 install "openmetadata-ingestion[postgres]"
```

--------------------------------

### Create OpenMetadata Directory

Source: https://docs.open-metadata.org/latest/quick-start/local-docker-deployment

Creates a new directory named 'openmetadata-docker' and navigates into it, preparing the workspace for OpenMetadata deployment.

```bash
mkdir openmetadata-docker && cd openmetadata-docker

```

--------------------------------

### Install MongoDB Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/mongodb/yaml

Install the necessary Python package for the MongoDB connector. This command ensures all dependencies for MongoDB ingestion are available.

```bash
pip3 install "openmetadata-ingestion[mongo]"
```

--------------------------------

### Lineage Management Example

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/overview

Demonstrates how to retrieve lineage information for a specific table, including upstream and downstream entities, and print the counts.

```APIDOC
## Lineage Management Example

### Description
Demonstrates how to retrieve lineage information for a specific table, including upstream and downstream entities, and print the counts.

### Code
```python
from metadata.sdk.api import Lineage

lineage = Lineage.get_lineage(
    "service.database.schema.table",
    upstream_depth=1,
    downstream_depth=1
)

if lineage:
    print(f"Upstream entities: {len(lineage.get('upstreamEdges', []))}")
    print(f"Downstream entities: {len(lineage.get('downstreamEdges', []))}")
```
```

--------------------------------

### Install Druid Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/druid/yaml

Install the necessary Python package for Druid ingestion. This command ensures all dependencies for the Druid connector are available.

```bash
pip3 install "openmetadata-ingestion[druid]"
```

--------------------------------

### Install DB2 Ingestion Package

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/db2/yaml

Install the necessary Python package for DB2 ingestion using pip. Supports Python versions 3.9-3.11.

```bash
pip3 install "openmetadata-ingestion[db2]"
```

--------------------------------

### Create Location using Java

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/java

Demonstrates how to create a new location using the `LocationsApi`. A `CreateLocation` object is required as input.

```java
LocationsApi locationsApi = openMetadataGateway.buildClient(LocationsApi.class);
CreateLocation createLocation = new CreateLocation();
Location location = locationsApi.createLocation(createLocation);
```

--------------------------------

### Key Files Quick Reference

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/codebase-deep-dives/data-quality

A quick reference guide to key files in the data quality module, categorized by the task they relate to.

```text
What you want to do| Start here  
---|---
 Understand the workflow pipeline| `workflow/data_quality.py`  
 See how test cases are fetched| `source/test_suite.py`  
 See how tests are filtered and dispatched| `processor/test_case_runner.py`  
 Understand validator creation| `builders/validator_builder.py`  
 Read the base validator logic| `validations/base_test_handler.py`  
 See a concrete SQL validator| `validations/column/sqlalchemy/columnValuesToBeNotNull.py`  
 See a concrete Pandas validator| `validations/column/pandas/columnValuesToBeNotNull.py`  
 Understand dimensional analysis| `validations/base_test_handler.py` → `_run_dimensional_validation()`  
 Add runtime parameter resolution| `validations/runtime_param_setter/param_setter_factory.py`  
 See how results are published| `ingestion/sink/metadata_rest.py` → `write_test_case_result_list()`  

```

--------------------------------

### List Users

Source: https://docs.open-metadata.org/v1.12.x/api-reference/teams-and-users/users

Retrieve a list of all users in the system using the GET method.

```shell
GET /v1/users
```

--------------------------------

### Install Doris Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/doris/yaml

Install the necessary Python package for Doris ingestion. This command ensures all dependencies for the Doris connector are met.

```bash
pip3 install "openmetadata-ingestion[doris]"
```

--------------------------------

### Install GCS Datalake Ingestion (OpenMetadata > 0.13)

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/gcs-datalake/yaml

Use this command to install the Datalake ingestion for GCS if your OpenMetadata version is greater than 0.13.

```bash
pip3 install "openmetadata-ingestion[datalake-gcp]"
```

--------------------------------

### Metabase YAML Configuration Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/metabase/yaml

This is a sample YAML configuration for the Metabase connector. It includes essential parameters like service type, name, authentication credentials, and host/port details.

```yaml
type: "metabase"
service: "metabase_service_name"
serviceConnection:
  config:
    type: "Metabase"
    username: "user@organization.com"
    password: "password"
    hostPort: "https://org.metabase.com:3000"
    sourceConfig:
      config:
        type: "MetabaseSourceConfig"
        dbServiceNames: ["mysql_database_name"]
        dashboardFilterPattern: "My dashboard, My dash.*, .*Dashboard"
        chartFilterPattern: "My chart, My chart.*, .*Chart"
        dataModelFilterPattern: "My data model, My data model.*, .*Data Model"
        includeOwners: true
        includeTags: true
        includeDataModels: true
        markDeletedDashboards: true
        includeDraftDashboard: true
        markDeletedDataModels: true
```

--------------------------------

### Running Tests from CLI

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/burstiq/yaml

Execute the metadata tests using the provided command, specifying the path to your configuration YAML file.

```bash
metadata test -c /path/to/my/config.yaml

```

--------------------------------

### Install Cockroach Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/cockroach/yaml

Install the necessary Python package for the CockroachDB connector. This command ensures all dependencies for Cockroach ingestion are met.

```bash
pip3 install "openmetadata-ingestion[cockroach]"
```

--------------------------------

### List Search Indexes

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/search-indexes/list

This example demonstrates how to list search indexes, filtering by a specific service and requesting additional fields like owners and tags.

```APIDOC
## GET /api/v1/searchIndexes

### Description
List all search indexes with optional filtering and pagination.

### Method
GET

### Endpoint
/api/v1/searchIndexes

### Parameters
#### Query Parameters
- **service** (string) - Required - Filter by search service fully qualified name.
- **limit** (integer) - Optional - Maximum number of results to return (max: 1000000). Default: "10"
- **before** (string) - Optional - Cursor for backward pagination.
- **after** (string) - Optional - Cursor for forward pagination.
- **fields** (string) - Optional - Comma-separated list of fields to include: `owners`, `tags`, `followers`, `votes`, `extension`, `domains`, `sourceHash`. See Supported Fields below.
- **include** (string) - Optional - Include `all`, `deleted`, or `non-deleted` entities. Default: "non-deleted"

### Response
#### Success Response (200)
- **data** (array) - Array of search index objects.
  - **id** (string) - Unique identifier for the search index (UUID format).
  - **name** (string) - Search index name.
  - **fullyQualifiedName** (string) - Fully qualified name in format `service.indexName`.
  - **displayName** (string) - Human-readable display name.
  - **service** (object) - Reference to the parent search service.
  - **serviceType** (string) - Type of search service (e.g., ElasticSearch, OpenSearch).
  - **fields** (array) - Field definitions for the index schema.
  - **owners** (array) - List of owners assigned to the search index. Only included when `fields` contains `owners`.
  - **tags** (array) - Classification tags applied. Only included when `fields` contains `tags`.
  - **domains** (array) - Domain assignments for governance. Only included when `fields` contains `domains`.
  - **followers** (array) - Users following this search index. Only included when `fields` contains `followers`.
  - **votes** (object) - User votes and ratings. Only included when `fields` contains `votes`.
  - **extension** (object) - Custom properties. Only included when `fields` contains `extension`.
- **paging** (object) - Pagination information.
  - **total** (integer) - Total count of search indexes matching the query.
  - **after** (string) - Cursor for the next page of results. Null if this is the last page.
  - **before** (string) - Cursor for the previous page of results. Null if this is the first page.

### Response Example
```json
{
  "data": [
    {
      "id": "f5b0fa81-f241-4508-9219-dae31dcced18",
      "name": "table_search_index",
      "fullyQualifiedName": "elasticsearch_sample.table_search_index",
      "displayName": "TableSearchIndex",
      "version": 0.1,
      "updatedAt": 1769982670810,
      "updatedBy": "admin",
      "service": {
        "id": "search-service-id",
        "type": "searchService",
        "name": "elasticsearch_sample",
        "fullyQualifiedName": "elasticsearch_sample",
        "deleted": false
      },
      "serviceType": "ElasticSearch",
      "fields": [
        {"name": "name", "dataType": "TEXT"},
        {"name": "description", "dataType": "TEXT"}
      ],
      "deleted": false,
      "owners": [],
      "tags": [],
      "domains": []
    }
  ],
  "paging": {
    "after": "...",
    "total": 5
  }
}
```
```

--------------------------------

### Mount NFS Share on Client Machines

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/dbt/storage-local-guide

Commands to install NFS client, mount the NFS share, and configure fstab for persistence on both dbt and OpenMetadata servers.

```bash
# On dbt server:
sudo apt install -y nfs-common
sudo mkdir -p /mnt/dbt-artifacts
sudo mount nfs-server:/export/dbt-artifacts /mnt/dbt-artifacts

# Make permanent
echo "nfs-server:/export/dbt-artifacts /mnt/dbt-artifacts nfs defaults 0 0" | \
    sudo tee -a /etc/fstab

# On OpenMetadata server:
sudo apt install -y nfs-common
sudo mkdir -p /mnt/dbt-artifacts
sudo mount nfs-server:/export/dbt-artifacts /mnt/dbt-artifacts

# Make permanent
echo "nfs-server:/export/dbt-artifacts /mnt/dbt-artifacts nfs defaults 0 0" | \
    sudo tee -a /etc/fstab

```

--------------------------------

### Install Couchbase Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/couchbase/yaml

Install the necessary Python package for the Couchbase ingestion connector. This command ensures all dependencies for Couchbase are met.

```bash
pip3 install "openmetadata-ingestion[couchbase]"
```

--------------------------------

### Install Cassandra Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/cassandra/yaml

Install the necessary Python package for the Cassandra ingestion connector. This command ensures all dependencies for Cassandra are included.

```bash
pip3 install "openmetadata-ingestion[cassandra]"
```

--------------------------------

### Configure Test Runner Behavior

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/data-quality-observability/quality/data-quality-as-code/test-runner

Customize the TestRunner's behavior using the `setup()` method. Options include forcing test updates, setting log levels, controlling error handling, defining success thresholds, and enabling streamable logs.

```python
from metadata.generated.schema.metadataIngestion.workflow import LogLevels
from metadata.sdk.data_quality import TableRowCountToBeBetween

runner = TestRunner.for_table("MySQL.ecommerce.public.orders")

# Configure runner behavior
runner.setup(
    force_test_update=True,        # Update existing tests
    log_level=LogLevels.DEBUG,     # Set logging level
    raise_on_error=False,          # Don't raise exceptions on errors
    success_threshold=90,          # Pass if 90% of tests succeed
    enable_streamable_logs=True    # Enable streamable log output
)

# Add and run tests
runner.add_test(TableRowCountToBeBetween(min_count=100))
results = runner.run()
```

--------------------------------

### Basic Connection

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/overview

Configure the SDK with your OpenMetadata host and JWT token. You can also configure it using environment variables.

```APIDOC
from metadata.sdk import configure

# Configure with your host and JWT token
configure(
    host="http://localhost:8585/api",
    jwt_token="your-jwt-token"
)

# Reads OPENMETADATA_HOST and OPENMETADATA_JWT_TOKEN automatically
configure()
```

--------------------------------

### Install Bigtable Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/bigtable/yaml

Install the necessary Python package for Bigtable ingestion. This command ensures all dependencies for the Bigtable connector are met.

```bash
pip3 install "openmetadata-ingestion[bigtable]"
```

--------------------------------

### Create Windsurf Rules

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/developing-a-new-connector/ai-assisted-development/install-skills

Create a `.windsurf/rules.md` file at the repository root to provide project context for Windsurf. This consolidates standard files for AI processing.

```bash
mkdir -p .windsurf
cat skills/standards/main.md skills/standards/patterns.md > .windsurf/rules.md
```

--------------------------------

### Install Redash Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/redash/yaml

Install the necessary Python package for the Redash ingestion connector. This command ensures all dependencies for Redash are included.

```bash
pip3 install "openmetadata-ingestion[redash]"
```

--------------------------------

### Install SSRS Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/ssrs/yaml

Install the necessary Python package for SSRS ingestion. This command ensures all dependencies for the SSRS connector are available.

```bash
pip3 install "openmetadata-ingestion[ssrs]"
```

--------------------------------

### List Stored Procedures with SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/stored-procedures/list

Configure the OpenMetadata SDK and list stored procedures. Demonstrates basic listing with pagination and auto-pagination for retrieving all stored procedures.

```python
from metadata.sdk import configure
from metadata.sdk.entities import StoredProcedures

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# List first page
procedures = StoredProcedures.list(limit=50)
for sp in procedures.data:
    print(f"{sp.fullyQualifiedName}")

# List all with auto-pagination
for sp in StoredProcedures.list_all():
    print(f"{sp.fullyQualifiedName}")
```

--------------------------------

### Install MicroStrategy Ingestion Package

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/microstrategy/yaml

Install the necessary Python package for MicroStrategy ingestion. Ensure you are using a compatible Python version (3.9-3.11).

```bash
pip3 install "openmetadata-ingestion[microstrategy]"
```

--------------------------------

### Start Claude Code Session

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/mcp/claude-code

Initiates a Claude Code session for interacting with metadata.

```bash
claude
```

--------------------------------

### List Data Product Versions

Source: https://docs.open-metadata.org/v1.12.x/api-reference/governance/data-products/versions

Use the Python SDK to list all versions of a data product. Ensure you have configured the SDK with your host and JWT token.

```Python
from metadata.sdk import configure
from metadata.sdk.entities import DataProducts

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# List all versions
versions = DataProducts.get_versions("b1839f98-f046-5f35-bdef-20f9b3395cb2")
for v in versions:
    print(f"Version {v.version}: {v.description}")
```

--------------------------------

### Install/Upgrade Helm Chart with JWT Configuration

Source: https://docs.open-metadata.org/v1.12.x/deployment/security/enable-jwt-tokens

Apply your updated Helm values to install or upgrade your OpenMetadata release.

```bash
helm upgrade --install openmetadata open-metadata/openmetadata --values openmetadata.prod.values.yml

```

--------------------------------

### MysqlConnectionClassConverter.java Example

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/developing-a-new-connector/create-java-class-converter

Implement a ClassConverter for MysqlConnection by extending `ClassConverter`. This example shows how to instantiate `MysqlConnection` and handle `authType` using `basicAuth` or `iamAuthConfig`.

```java
package org.openmetadata.service.secrets.converter;

import org.openmetadata.schema.services.connections.MysqlConnection;
import org.openmetadata.schema.services.connections.auth.basicAuth;
import org.openmetadata.schema.services.connections.auth.iamAuthConfig;

import com.fasterxml.jackson.databind.JsonNode;

public class MysqlConnectionClassConverter extends ClassConverter<MysqlConnection> {

  @Override
  public MysqlConnection convert(JsonNode json) {
    MysqlConnection mysqlConnection = convertJsonToBean(json, MysqlConnection.class);
    if (mysqlConnection.getAuthType() == null) {
      return mysqlConnection;
    }

    // Try to instantiate basicAuth
    basicAuth basicAuth = convertJsonToBean(mysqlConnection.getAuthType(), basicAuth.class);
    if (basicAuth != null) {
      mysqlConnection.setAuthType(basicAuth);
      return mysqlConnection;
    }

    // Try to instantiate iamAuthConfig
    iamAuthConfig iamAuthConfig = convertJsonToBean(mysqlConnection.getAuthType(), iamAuthConfig.class);
    if (iamAuthConfig != null) {
      mysqlConnection.setAuthType(iamAuthConfig);
      return mysqlConnection;
    }

    return mysqlConnection;
  }
}
```

--------------------------------

### Implement Connector with Codex/Copilot/Windsurf

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/developing-a-new-connector/ai-assisted-development/build-with-ai

Instruct Codex, Copilot, or Windsurf to read specific files (context, reference metadata, and connection) and implement TODO items following established patterns.

```bash
Read these files:
1. ingestion/src/metadata/ingestion/source/{type}/{name}/CONNECTOR_CONTEXT.md
2. ingestion/src/metadata/ingestion/source/{type}/{reference}/metadata.py
3. ingestion/src/metadata/ingestion/source/{type}/{reference}/connection.py

Then implement all TODO items in the generated files, following the same patterns.
```

--------------------------------

### provider_registry.om_auth_init

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/api-reference

Initialize OpenMetadata authentication.

```APIDOC
## om_auth_init

### Description
Initializes OpenMetadata authentication.

### Method
provider_registry.om_auth_init()
```

--------------------------------

### Configure OpenMetadata SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-quality/test-cases/create

Basic SDK configuration required before making API calls. Set your OpenMetadata instance host and authentication token.

```python
from metadata.sdk import configure
from metadata.sdk.entities import TestCases
from metadata.generated.schema.api.tests.createTestCase import CreateTestCaseRequest

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)


```

--------------------------------

### Fivetran Connector Header Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/fivetran/yaml

Example usage of the ConnectorDetailsHeader component for the Fivetran connector, specifying its icon, name, stage, and feature availability.

```jsx
<ConnectorDetailsHeader icon="/public/images/connectors/fivetran.webp" name="Fivetran" stage="PROD" availableFeatures={["Pipelines", "Pipeline Status", "Lineage", "Usage"]} unavailableFeatures={["Owners", "Tags"]} />
```

--------------------------------

### Verify Java Version

Source: https://docs.open-metadata.org/v1.12.x/deployment/bare-metal

Run this command to check if a supported Java runtime is installed. Ensure Java 21.0.0 or higher is present.

```command
java --version
```

--------------------------------

### Self-hosted Airflow Docker HostPort Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/airflow/rest-api-connection

Example of the hostPort parameter for a self-hosted Airflow instance when the ingestion is running inside a Docker container.

```text
http://host.docker.internal:8080
```

--------------------------------

### Example Warning Message for Validation Failure

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/dbt/ingest-dbt-custom-properties

This is an example warning message logged when a custom property value fails validation against its defined type.

```text
Validation failed for custom property 'sla_hours' (type: integer): Expected integer value. Provided value: "24 hours"
```

--------------------------------

### Retrieve Data Product by Fully Qualified Name (FQN)

Source: https://docs.open-metadata.org/v1.12.x/api-reference/governance/data-products

Get a specific data product using its Fully Qualified Name (FQN).

```bash
GET /v1/dataProducts/name/{fqn}
```

--------------------------------

### Minimal Custom Connector Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/custom-connectors

A basic Python class that extends from `metadata.ingestion.api.steps.Source`. Implement the `_iter` method to yield Create Entity Requests.

```python
from metadata.ingestion.api.steps import Source

class MyAwesomeConnector(Source):
    def _iter(self):
        yield ""
```

--------------------------------

### Atlas Connector Header Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/metadata/atlas

Renders the header for the Atlas connector, indicating it is in production stage and supports Metadata features.

```javascript
<ConnectorDetailsHeader icon="/public/images/connectors/atlas.webp" name="Atlas" stage="PROD" availableFeatures={["Metadata"]} unavailableFeatures={[]} />
```

--------------------------------

### Verify OpenMetadata SDK Installation and Configuration

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/data-quality-observability/quality/data-quality-as-code/getting-started

Create a simple test to verify that the SDK is configured correctly by attempting to create a TestRunner instance for a table.

```python
from metadata.sdk import configure
from metadata.sdk.data_quality import TestRunner

# Configure SDK
configure(
    host="http://localhost:8585/api",
    jwt_token="your-jwt-token-here"
)

# Test connection by creating a runner
try:
    runner = TestRunner.for_table("your_service.database.schema.table")
    print("✓ SDK configured successfully!")
except Exception as e:
    print(f"✗ Configuration failed: {e}")
```

--------------------------------

### Sample Search Metadata Response

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/mcp/reference

This is an example of a successful response from the search_metadata tool, detailing found data assets with relevant information.

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Found 5 results matching 'sales':\n\n**Tables:**\n1. **sales_transactions** (mysql_prod.ecommerce.public.sales_transactions)\n   - Description: Daily sales transaction records\n   - Service: mysql_prod (MySQL)\n   - Owners: sales-team, john.doe@company.com\n   - Tags: PII, Financial\n   - [View in OpenMetadata](https://your-om.com/table/mysql_prod.ecommerce.public.sales_transactions)\n\n2. **sales_reports** (postgresql_analytics.reporting.main.sales_reports)\n   - Description: Aggregated sales reporting data\n   - Service: postgresql_analytics (PostgreSQL)\n   - Owners: analytics-team\n   - [View in OpenMetadata](https://your-om.com/table/postgresql_analytics.reporting.main.sales_reports)\n\n**Dashboards:**\n3. **Sales Performance Dashboard** (looker_prod.sales.sales_performance)\n   - Description: Real-time sales KPI dashboard\n   - Service: looker_prod (Looker)\n   - Charts: 8 charts\n   - [View in OpenMetadata](https://your-om.com/dashboard/looker_prod.sales.sales_performance)"
      }
    ]
  }
}
```

--------------------------------

### REST Connector Header Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/api/rest

Example usage of the ConnectorDetailsHeader component for the REST connector. This renders the header with specific details for the REST API.

```javascript
<ConnectorDetailsHeader icon="/public/images/connectors/rest.webp" name="REST" stage="BETA" availableFeatures={["API Endpoint", "Request Schema", "Response Schema"]} unavailableFeatures={[]} />
```

--------------------------------

### Example Test Definition FQN

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-quality/test-definitions

The Fully Qualified Name (FQN) for a test definition is its name. This example shows the FQN for a column-level test.

```text
columnValueLengthsToBeBetween
```

--------------------------------

### List and Retrieve Glossary Versions using Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/governance/glossaries/versions

Demonstrates how to use the Python SDK to list all versions of a glossary and retrieve a specific version. Ensure the SDK is configured with your host and JWT token.

```python
from metadata.sdk import configure
from metadata.sdk.entities import Glossaries

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# List all versions
versions = Glossaries.get_versions("c2940a98-f147-6g46-cdef-31f0c4406dc3")
for v in versions:
    print(f"Version {v.version}: {v.description}")

# Get a specific version
glossary_v1 = Glossaries.get_specific_version(
    "c2940a98-f147-6g46-cdef-31f0c4406dc3",
    "0.1"
)
print(f"Original description: {glossary_v1.description}")

```

--------------------------------

### Exported CSV Data Example

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/databases/import-export

Example of the CSV data structure returned by the database export API, including headers and a sample row.

```csv
"name,displayName,description,owner,tags,retentionPeriod,sourceUrl,domain\nposts_db,posts_db,,,,,https://localhost:3306/posts_db,"

```

--------------------------------

### List API Endpoints

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/api-endpoints/list

This example demonstrates how to list API endpoints, filtering by API collection and specifying fields to include.

```APIDOC
## List API Endpoints

### Description
List all API endpoints with optional filtering and pagination.

### Method
GET

### Endpoint
/api/v1/apiEndpoints

### Parameters
#### Query Parameters
- **apiCollection** (string) - Optional - Filter by API collection fully qualified name.
- **service** (string) - Optional - Filter by API service fully qualified name.
- **limit** (integer) - Optional - Maximum number of results to return (max: 1000000). Default: "10".
- **before** (string) - Optional - Cursor for backward pagination.
- **after** (string) - Optional - Cursor for forward pagination.
- **fields** (string) - Optional - Comma-separated list of fields to include: `owners`, `tags`, `extension`, `domains`, `sourceHash`. See Supported Fields below.
- **include** (string) - Optional - Include `all`, `deleted`, or `non-deleted` entities. Default: "non-deleted".

### Response
#### Success Response (200)
- **data** (array) - Array of API endpoint objects.
  - **id** (string) - Unique identifier for the API endpoint (UUID format).
  - **name** (string) - API endpoint name.
  - **fullyQualifiedName** (string) - Fully qualified name in format `service.collection.endpointName`.
  - **displayName** (string) - Human-readable display name.
  - **endpointURL** (string) - URL for the API endpoint.
  - **requestMethod** (string) - HTTP request method.
  - **service** (object) - Reference to the parent API service.
  - **serviceType** (string) - Type of API service (e.g., Rest).
  - **owners** (array) - List of owners assigned to the API endpoint. Only included when `fields` contains `owners`.
  - **tags** (array) - Classification tags applied. Only included when `fields` contains `tags`.
  - **domains** (array) - Domain assignments for governance. Only included when `fields` contains `domains`.
  - **extension** (object) - Custom properties. Only included when `fields` contains `extension`.
- **paging** (object) - Pagination information.
  - **total** (integer) - Total count of API endpoints matching the query.
  - **after** (string) - Cursor for the next page of results. Null if this is the last page.
  - **before** (string) - Cursor for the previous page of results. Null if this is the first page.

### Response Example
```json
{
  "data": [
    {
      "id": "1f61427a-4a64-4070-9ac8-1d29302dac7c",
      "name": "addPet",
      "displayName": "Add Pet",
      "fullyQualifiedName": "sample_api_service.pet.addPet",
      "description": "add a new pet",
      "version": 0.1,
      "updatedAt": 1769982733987,
      "updatedBy": "admin",
      "endpointURL": "https://petstore3.swagger.io/#/pet/addPet",
      "requestMethod": "POST",
      "requestSchema": {
        "schemaType": "JSON",
        "schemaFields": [
          {"name": "id", "dataType": "INT", "description": "ID of pet"}
        ]
      },
      "href": "http://localhost:8585/api/v1/apiEndpoints/1f61427a-4a64-4070-9ac8-1d29302dac7c",
      "owners": [],
      "tags": [],
      "service": {
        "id": "58d413a8-abc3-4a6d-bd8a-13a0234b1ff8",
        "type": "apiService",
        "name": "sample_api_service",
        "deleted": false
      },
      "serviceType": "Rest",
      "deleted": false,
      "domains": []
    }
  ],
  "paging": {
    "after": "...",
    "total": 8
  }
}
```
```

--------------------------------

### Example Decoded Token Payload

Source: https://docs.open-metadata.org/v1.12.x/api-reference/authentication

An example of a decoded JWT token payload, illustrating the available claims such as issuer, subject, roles, and expiration.

```json
{
  "iss": "open-metadata.org",
  "sub": "ingestion-bot",
  "roles": ["IngestionBotRole"],
  "email": "ingestion-bot@open-metadata.org",
  "isBot": true,
  "tokenType": "BOT",
  "iat": 1704067200,
  "exp": null
}
```

--------------------------------

### Example Reindexing Configuration

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/admin-guide/reindexing-search

Configure reindexing parameters for high-performance systems. Adjust `batchSize`, `queueSize`, `producerThreads`, and `maxConcurrentRequests` based on load and resources.

```json
{
  "batchSize": 300,
  "queueSize": 500,
  "producerThreads": 20,
  "maxConcurrentRequests": 500
}
```

--------------------------------

### Manage Table Sample Data with Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/tables/sample-data

Use the OpenMetadata SDK to get, add, and delete sample data for a table. Ensure the SDK is configured with your host and JWT token.

```python
from metadata.sdk import configure
from metadata.sdk.entities import Tables

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

table_id = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"

# Get sample data
sample = Tables.get_sample_data(table_id)
for row in sample.get("rows", []):
    print(row)

# Add sample data
Tables.add_sample_data(table_id, {
    "columns": [
        {"name": "id", "dataType": "INT"},
        {"name": "name", "dataType": "VARCHAR"},
        {"name": "email", "dataType": "VARCHAR"},
        {"name": "created_at", "dataType": "TIMESTAMP"}
    ],
    "rows": [
        [1, "Alice Johnson", "alice@example.com", "2024-01-15T10:30:00Z"],
        [2, "Bob Smith", "bob@example.com", "2024-02-20T14:15:00Z"],
        [3, "Carol Williams", "carol@example.com", "2024-03-10T09:45:00Z"]
    ]
})

# Delete sample data
Tables.delete_sample_data(table_id)

```

--------------------------------

### MSSQL Connector Configuration Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/mssql/yaml

This YAML configuration is used for setting up the MSSQL connector for metadata ingestion. It specifies connection details and ingestion options.

```yaml
source:
  type: mssql
  hostPort: "<mssql_host>:<mssql_port>"
  database: "<mssql_database>"
  username: "<mssql_username>"
  password: "<mssql_password>"
  schema: "<mssql_schema>"
sink:
  type: "metadata-rest"
  # The URL of the OpenMetadata Ingestion service
  # Example: http://localhost:8585/api
  openMetadataServerUri: "<openmetadata_server_uri>"
workflowConfig:
  openMetadataServerVersion: "v1.12.0"
```

--------------------------------

### SamplerInterface Key Methods

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/codebase-deep-dives/sampler

Defines the essential methods available in the SamplerInterface for interacting with data sources and retrieving sampled data.

```markdown
Method| Purpose  
---|---
`create(...)`| Factory method — creates a sampler with all dependencies  
`get_dataset()`| Returns the sampled dataset (CTE for SQL, DataFrame for pandas)  
`fetch_sample_data(columns)`| Fetches actual row data as `TableData`  
`generate_sample_data()`| Full pipeline: fetch → truncate → optionally upload  
`get_columns()`| Returns columns (respecting include/exclude filters)  
`raw_dataset`| Abstract property — the unsampled table/DataFrame  
`close()`| Cleanup connections  
```

--------------------------------

### Start Docker Compose Services

Source: https://docs.open-metadata.org/latest/quick-start/local-docker-deployment

Use this command to start the Docker Compose services after they have been stopped. This will restart the containers without requiring a rebuild.

```bash
docker compose start

```

--------------------------------

### Install Pre-commit Hooks

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/ingestion-framework

Install pre-commit hooks to automatically validate code at commit time. If validations fail, the tools will attempt to fix your code.

```bash
make precommit_install

```

--------------------------------

### Download Docker Compose for PostgreSQL (wget)

Source: https://docs.open-metadata.org/latest/quick-start/local-docker-deployment

Downloads the docker-compose-postgres.yml file for deploying OpenMetadata with a PostgreSQL backend using wget.

```bash
wget https://github.com/open-metadata/OpenMetadata/releases/download/1.12.6-release/docker-compose-postgres.yml

```

--------------------------------

### Install NiFi Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/nifi/yaml

Install the necessary Python package for the NiFi ingestion connector. This command ensures all dependencies for NiFi ingestion are met.

```bash
pip3 install "openmetadata-ingestion[nifi]"
```

--------------------------------

### Run Quality Tools

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/ingestion-framework

Execute these make recipes to check code quality and formatting. These tools help maintain standardized formatting throughout the codebase.

```bash
make lint
make black
make isort

```

--------------------------------

### Install Dagster Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/dagster/yaml

Install the necessary Python packages for Dagster ingestion. This command ensures you have the Dagster integration for the OpenMetadata ingestion framework.

```bash
pip3 install "openmetadata-ingestion[dagster]"
```

--------------------------------

### Download Docker Compose for PostgreSQL using wget

Source: https://docs.open-metadata.org/v1.12.x/quick-start/local-docker-deployment

Use wget to download the docker-compose-postgres.yml file for deploying OpenMetadata with a PostgreSQL database.

```bash
wget https://github.com/open-metadata/OpenMetadata/releases/download/1.12.6-release/docker-compose-postgres.yml
```

--------------------------------

### Install Redpanda Ingestion Package

Source: https://docs.open-metadata.org/v1.12.x/connectors/messaging/redpanda/yaml

Install the necessary Python package for the Redpanda ingestion connector. Ensure you are using a supported Python version (3.9-3.11).

```bash
pip3 install "openmetadata-ingestion[redpanda]"
```

--------------------------------

### Install ADLS Datalake Connector

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/adls-datalake/yaml

Install the OpenMetadata ingestion package with support for the datalake-azure connector. Ensure you are using a compatible Python version (3.9-3.11).

```bash
pip3 install "openmetadata-ingestion[datalake-azure]"
```

--------------------------------

### Install OpenMetadata Helm Chart with Airflow Configuration

Source: https://docs.open-metadata.org/v1.12.x/deployment/kubernetes/eks/airflow

Deploy the main OpenMetadata Helm chart, specifying Airflow configurations and connection details for OpenSearch and RDS.

```bash
helm install openmetadata open-metadata/openmetadata --values openmetadata-values-airflow.yaml

```

--------------------------------

### Install/Upgrade OpenMetadata and Dependencies Helm Charts

Source: https://docs.open-metadata.org/v1.12.x/deployment/kubernetes/on-prem

Execute these commands to install or upgrade the OpenMetadata and `openmetadata-dependencies` Helm charts with your specified values file and Kubernetes namespace.

```commandline
helm upgrade --install openmetadata-dependencies open-metadata/openmetadata-dependencies --values <<path-to-values-file>> --namespace <kubernetes_namespace>
helm upgrade --install openmetadata open-metadata/openmetadata --values <<path-to-values-file>> --namespace <kubernetes_namespace>
```

--------------------------------

### Install Mode Ingestion Requirements

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/mode/yaml

Install the necessary Python packages for the Mode ingestion connector. Ensure you are using a supported Python version (3.9-3.11).

```bash
pip3 install "openmetadata-ingestion[mode]"
```

--------------------------------

### Install Hex Connector Dependencies

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/hex/yaml

Install the necessary Python package for the Hex ingestion connector. This command ensures all dependencies for the Hex connector are included.

```bash
pip3 install "openmetadata-ingestion[hex]"
```

--------------------------------

### Run Tests from CLI

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/azuresql/yaml

Execute data quality tests using the `metadata test` command with a specified configuration file.

```bash
metadata test -c /path/to/my/config.yaml
```

--------------------------------

### Install/Upgrade OpenMetadata Dependencies Helm Chart

Source: https://docs.open-metadata.org/v1.12.x/deployment/kubernetes/on-prem

Use this command to upgrade or install the `openmetadata-dependencies` Helm chart with your custom `values.deps.yaml` file.

```bash
helm upgrade --install openmetadata-dependencies open-metadata/openmetadata-dependencies --values values.deps.yaml
```

--------------------------------

### SSRS Source Configuration Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/ssrs/yaml

Example YAML configuration for the SSRS source. This defines connection details, authentication, and optional filtering for metadata ingestion.

```yaml
source:
  type: ssrs
  serviceName: "your_ssrs_service_name"
  serviceConnection:
    config:
      type: "SSRS"
      hostPort: "https://your-ssrs-server/reportserver"
      username: "DOMAIN\username"
      password: "your_password"
      # verifySSL: "no-ssl" | "ignore" | "validate"
      # sslConfig:
      #   certificatePath: "/path/to/ca.crt"
      # dashboardFilterPattern:
      #   includes:
      #     - ".*"
      #   excludes:
      #     - ".*test.*"
      # chartFilterPattern:
      #   includes:
      #     - ".*"
      #   excludes:
      #     - ".*test.*"
      # projectFilterPattern:
      #   includes:
      #     - ".*"
      #   excludes:
      #     - ".*test.*"
```

--------------------------------

### Partition Handling with CTE

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/codebase-deep-dives/sampler

Demonstrates how partition filtering is applied by creating a CTE that filters rows based on partition predicates before sampling.

```sql
WITH partitioned AS (
    SELECT * FROM table WHERE partition_col >= '2024-01-01'
)
-- Then sample from the partitioned CTE

```

--------------------------------

### Expected S3 Artifacts

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/dbt/storage-s3-guide

Example output showing the dbt artifacts that should be present in the S3 bucket after a successful DAG run.

```text
2026-02-10 10:30:00   5242880 manifest.json
2026-02-10 10:30:01   1048576 catalog.json
2026-02-10 10:30:01    102400 run_results.json

```

--------------------------------

### Initialize OpenMetadata SDK

Source: https://docs.open-metadata.org/latest/sdk/python

Configure the OpenMetadata SDK client by providing the API host and JWT token. This call automatically performs a health check.

```python
from metadata.sdk import configure, Tables, Databases, DatabaseSchemas, DatabaseServices, Users

configure(host="http://localhost:8585/api", jwt_token="<YOUR-INGESTION-BOT-JWT-TOKEN>")
```

--------------------------------

### Install GCS Ingestion Dependencies

Source: https://docs.open-metadata.org/v1.12.x/connectors/storage/gcs/yaml

Install the necessary Python package for the GCS ingestion. This command includes the 'datalake-gcs' extra to ensure all GCS-specific dependencies are met.

```bash
pip3 install "openmetadata-ingestion[datalake-gcs]"
```

--------------------------------

### Retrieve a Test Suite by Name (FQN)

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-quality/test-suites

Get the details of a specific test suite using its fully qualified name (FQN).

```bash
curl -X GET \
  'http://localhost:8585/v1/dataQuality/testSuites/name/api_test_suite' \
  -H 'accept: application/json'
```

--------------------------------

### CURL Request to Create Test Suite

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/data-quality-observability/quality/custom-tests

This CURL command shows how to create an executable Test Suite via a POST request. Ensure the 'name', 'description', and 'executableEntityReference' are provided.

```bash
curl --request POST 'http://localhost:8585/api/v1/dataQuality/testSuites/executable' \
--header 'Content-Type: application/json' \
--data-raw '{
  "name": "<test_suite_name>",
  "description": "<test suite description>",
  "executableEntityReference": "<entityFQN>"
}'
```

--------------------------------

### Building API Clients

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/java

Demonstrates how to build clients for different OpenMetadata APIs by providing the class of the desired API to the `buildClient` method.

```APIDOC
## Building API Clients

You can use an API from the OpenMetadata Gateway. Using OpenMetadata Gateway, you will need to build the client by providing the `class` of the respected API. Below are some examples:

```java
// Dashboards API
DashboardsApi dashboardApi = openMetadataGateway.buildClient(DashboardsApi.class);

// Tables API
TablesApi tablesApiClient = openMetadataGateway.buildClient(TablesApi.class);

// Users API
UsersApi usersApi = openMetadataGateway.buildClient(UsersApi.class);

// Locations API
LocationsApi locationsApi = openMetadataGateway.buildClient(LocationsApi.class);
```
```

--------------------------------

### Install Fivetran Ingestion Package

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/fivetran/yaml

Install the OpenMetadata ingestion package with Fivetran support using pip. This command ensures all dependencies for Fivetran ingestion are included.

```bash
pip3 install "openmetadata-ingestion[fivetran]"
```

--------------------------------

### Install Airbyte Ingestion

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/airbyte/yaml

Install the necessary package for Airbyte ingestion using pip. This command ensures you have the Airbyte connector and its dependencies for the OpenMetadata ingestion framework.

```bash
pip3 install "openmetadata-ingestion[airbyte]"
```

--------------------------------

### Install Great Expectations Submodule

Source: https://docs.open-metadata.org/v1.12.x/connectors/ingestion/great-expectations

Install the necessary Great Expectations submodule for openmetadata-ingestion. This command ensures you have the required packages to integrate Great Expectations with OpenMetadata.

```bash
pip3 install 'openmetadata-ingestion[great-expectations]'
```

--------------------------------

### Create Dashboard with Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/dashboards/create

Use the OpenMetadata Python SDK to create a new dashboard. Ensure you have configured the SDK with your host and JWT token. The `CreateDashboardRequest` object requires essential details like name, display name, service, and source URL.

```python
from metadata.sdk import configure
from metadata.sdk.entities import Dashboards
from metadata.generated.schema.api.data.createDashboard import CreateDashboardRequest

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

request = CreateDashboardRequest(
    name="10",
    displayName="deck.gl Demo",
    service="sample_superset",
    description="Dashboard showcasing deck.gl visualizations",
    sourceUrl="http://localhost:808/superset/dashboard/10/"
)

dashboard = Dashboards.create(request)
print(f"Created: {dashboard.fullyQualifiedName}")

```

--------------------------------

### Create a Custom Database Sampler

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/codebase-deep-dives/sampler

Extend SQASampler to add database-specific sampling logic. Override set_tablesample to implement the database's TABLESAMPLE clause.

```python
from metadata.sampler.sqlalchemy.sampler import SQASampler

class MyDBSampler(SQASampler):
    def set_tablesample(self, selectable):
        # Add your database's TABLESAMPLE clause
        return selectable.tablesample(
            func.bernoulli(self.sample_config.profileSample)
        )
```

--------------------------------

### Run Code Generation

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/developing-a-new-connector/ai-assisted-development/build-with-ai

Activate the development environment and run make generate for Python models, mvn install for Java models, and yarn parse-schema for UI forms.

```bash
source env/bin/activate

# Generate Python Pydantic models from JSON Schema
make generate

# Generate Java models
mvn clean install -pl openmetadata-spec

# Generate resolved JSON for UI forms
cd openmetadata-ui/src/main/resources/ui && yarn parse-schema
```

--------------------------------

### Install Grafana Ingestion Plugin

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/grafana/yaml

Install the Grafana ingestion plugin for OpenMetadata using pip. This command ensures you have the necessary components to run the Grafana connector.

```bash
pip3 install "openmetadata-ingestion[grafana]"
```

--------------------------------

### Create OpenMetadata Client

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/api-reference/client-utils

Use this function to create an OpenMetadata client instance. It requires an OpenMetadataConnection configuration object.

```python
create_ometa_client(metadata_config: OpenMetadataConnection) → OpenMetadata
```

--------------------------------

### Install Domo Dashboard Ingestion Dependencies

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/domo-dashboard/yaml

Install the necessary Python packages for Domo Dashboard ingestion. This command ensures all required libraries are available for the connector.

```bash
pip3 install "openmetadata-ingestion[domo]"
```

--------------------------------

### List Tables with Manual Pagination

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/tables/list

This example shows how to list tables with manual pagination using the `list` method. You can specify the `limit` and `fields` to retrieve. The response contains entities and paging information.

```APIDOC
## List with pagination
page = Tables.list(limit=50, fields=["columns", "owners", "tags"])
for t in page.entities:
    print(f"{t.fullyQualifiedName} ({len(t.columns or [])} columns)")
```

--------------------------------

### Delete Data Product using Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/governance/data-products/delete

Demonstrates how to delete a data product using the Python SDK. Includes examples for soft delete by ID, hard delete by ID, delete by name, and restoring a soft-deleted data product.

```python
from metadata.sdk import configure
from metadata.sdk.entities import DataProducts

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# Soft delete by ID
DataProducts.delete("b1839f98-f046-5f35-bdef-20f9b3395cb2")

# Hard delete
DataProducts.delete(
    "b1839f98-f046-5f35-bdef-20f9b3395cb2",
    hard_delete=True
)

# Delete by name
DataProducts.delete_by_name("Marketing.CustomerInsights")

# Restore a soft-deleted data product
DataProducts.restore("b1839f98-f046-5f35-bdef-20f9b3395cb2")

```

--------------------------------

### GCS Datalake Connector Header Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/gcs-datalake

Example usage of the ConnectorDetailsHeader component for the GCS Datalake connector, specifying its icon, name, stage, and feature availability.

```javascript
<ConnectorDetailsHeader icon="/public/images/connectors/gcs.webp" name="GCS Datalake" stage="PROD" availableFeatures={["Metadata", "Data Profiler", "Data Quality", "Sample Data", "Auto-Classification"]} unavailableFeatures={["Query Usage", "Lineage", "Column-level Lineage", "Owners", "dbt", "Tags", "Stored Procedures"]} />
```

--------------------------------

### ODCS JSON Response Example

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-contracts/odcs

This is an example of a data contract exported in the ODCS JSON format. It includes schema definitions, quality metrics, and SLA properties.

```json
{
  "apiVersion": "v3.1.0",
  "kind": "DataContract",
  "name": "sales-orders-contract",
  "version": "1.0.0",
  "status": "active",
  "domain": "ecommerce",
  "description": {
    "purpose": "Data contract for the sales orders table"
  },
  "schema": [
    {
      "name": "orders",
      "logicalType": "object",
      "properties": [
        {
          "name": "order_id",
          "logicalType": "integer",
          "required": true,
          "primaryKey": true
        },
        {
          "name": "customer_id",
          "logicalType": "integer",
          "required": true
        },
        {
          "name": "order_date",
          "logicalType": "timestamp",
          "required": true
        },
        {
          "name": "total_amount",
          "logicalType": "decimal"
        }
      ]
    }
  ],
  "quality": [
    {
      "type": "custom",
      "dimension": "completeness",
      "description": "All required fields must be present"
    }
  ],
  "slaProperties": [
    {
      "property": "frequency",
      "value": "PT1H"
    },
    {
      "property": "availability",
      "value": "99.9"
    }
  ]
}
```

--------------------------------

### Run openmetadata-ops.sh with Options and Commands

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/openmetadata-ops

This is the general syntax for running the openmetadata-ops.sh script. Use options to configure the script's behavior and commands to perform specific operations.

```bash
sh bootstrap/openmetadata-ops.sh [OPTIONS] [COMMANDS]
```

--------------------------------

### Initialize AI SDK Client

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/ai-sdk

Initialize the AI SDK client using configuration loaded from environment variables or by directly providing host and token.

```python
from ai_sdk import AISdk, AISdkConfig

# From environment variables
config = AISdkConfig.from_env()
client = AISdk.from_config(config)

# Or directly
client = AISdk(
    host="https://your-openmetadata-instance.com",
    token="your-bot-jwt-token",
)
```

--------------------------------

### Snowflake User Privileges Setup

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/snowflake

SQL commands to create a new role and user, and grant the necessary privileges for metadata ingestion. Ensure to replace placeholders like WAREHOUSE_NAME, TEST_DB, TEST_SCHEMA, and PASSWORD with your actual values.

```sql
-- Create New Role
CREATE ROLE NEW_ROLE;
-- Create New User
CREATE USER NEW_USER DEFAULT_ROLE=NEW_ROLE PASSWORD='PASSWORD';
-- Grant role to user
GRANT ROLE NEW_ROLE TO USER NEW_USER;
-- Grant USAGE Privilege on Warehouse to New Role
GRANT USAGE ON WAREHOUSE WAREHOUSE_NAME TO ROLE NEW_ROLE;
-- Grant USAGE Privilege on Database to New Role
GRANT USAGE ON DATABASE TEST_DB TO ROLE NEW_ROLE;
-- Grant USAGE Privilege on required Schemas to New Role
GRANT USAGE ON SCHEMA TEST_SCHEMA TO ROLE NEW_ROLE;
-- Grant SELECT Privilege on required tables & views to New Role
GRANT SELECT ON ALL TABLES IN SCHEMA TEST_SCHEMA TO ROLE NEW_ROLE;
GRANT SELECT ON ALL EXTERNAL TABLES IN SCHEMA TEST_SCHEMA TO ROLE NEW_ROLE;
GRANT SELECT ON ALL VIEWS IN SCHEMA TEST_SCHEMA TO ROLE NEW_ROLE;
GRANT SELECT ON ALL DYNAMIC TABLES IN SCHEMA TEST_SCHEMA TO ROLE NEW_ROLE;
-- Grant IMPORTED PRIVILEGES on all Schemas of SNOWFLAKE DB to New Role,
-- optional but required for usage, lineage and stored procedure ingestion
GRANT IMPORTED PRIVILEGES ON ALL SCHEMAS IN DATABASE SNOWFLAKE TO ROLE NEW_ROLE;
```

--------------------------------

### Install OpenMetadata Oracle Ingestion

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/oracle/yaml

Install the OpenMetadata Ingestion package with Oracle support using pip. This command ensures you have all necessary dependencies to run the Oracle connector.

```bash
pip3 install "openmetadata-ingestion[oracle]"
```

--------------------------------

### Create Database Service (POST)

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/database-services/create

Use this endpoint to create a new database service. The request body requires essential details such as name, serviceType, and connection configuration. A `409` error will be returned if a service with the same name already exists.

```bash
curl -X POST "{base_url}/api/v1/services/databaseServices" \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{ ... body ... }'
```

--------------------------------

### Kubernetes Secret Naming Convention Examples

Source: https://docs.open-metadata.org/v1.12.x/deployment/secrets-manager/supported-implementations/kubernetes-secrets-manager

Examples of how secrets are named in Kubernetes, following the convention `<prefix>-<clusterName>-<path>-<components>`. Names are sanitized for Kubernetes compatibility.

```plaintext
openmetadata-bot-name-config-jwttoken
openmetadata-database-myservice-password

```

--------------------------------

### Initialize AI SDK Client (Java)

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/ai-sdk

Initialize the AI SDK client for Java applications using a builder pattern with host and token.

```java
import io.openmetadata.ai.AISdk;

AISdk client = new AISdk.Builder()
    .host("https://your-openmetadata-instance.com")
    .token("your-bot-jwt-token")
    .build();
```

--------------------------------

### provider_registry.basic_auth_init

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/api-reference

Initialize basic authentication.

```APIDOC
## basic_auth_init

### Description
Initializes basic authentication.

### Method
provider_registry.basic_auth_init()
```

--------------------------------

### Doris YAML Configuration

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/doris/yaml

Example YAML configuration for Doris metadata ingestion, including optional include/exclude patterns for databases, schemas, and tables.

```yaml
#   includes:
#     - database1
#     - database2
#   excludes:
#     - database3
#     - database4
#   schemaFilterPattern:
#     includes:
#       - schema1
#       - schema2
#     excludes:
#       - schema3
#       - schema4
#   tableFilterPattern:
#     includes:
#       - users
#       - type_test
#     excludes:
#       - table3
#       - table4
```

--------------------------------

### Create Topic with Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/topics/create

Use the OpenMetadata Python SDK to create a new topic. Ensure you have configured the SDK with your host and JWT token. This example demonstrates creating a topic with Protobuf message schema.

```python
from metadata.sdk import configure
from metadata.sdk.entities import Topics
from metadata.generated.schema.api.data.createTopic import CreateTopicRequest

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

request = CreateTopicRequest(
    name="address_book",
    displayName="Address Book",
    service="sample_kafka",
    description="All Protobuf record related events gets captured in this topic",
    messageSchema={
        "schemaType": "Protobuf",
        "schemaText": "syntax = \"proto2\";\npackage tutorial;\nmessage Person { ... }"
    },
    partitions=1,
    cleanupPolicies=["delete"],
    replicationFactor=1,
    maximumMessageSize=1,
    retentionSize=-1
)

topic = Topics.create(request)
print(f"Created: {topic.fullyQualifiedName}")

```

--------------------------------

### Create Dashboard Service using Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/dashboard-services/create

Use the OpenMetadata Python SDK to configure the connection and create a new dashboard service. Ensure you have your host and JWT token configured.

```python
from metadata.sdk import configure
import requests

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# Direct API call for dashboard services
response = requests.post(
    "https://your-company.open-metadata.org/api/v1/services/dashboardServices",
    headers={"Authorization": "Bearer your-jwt-token"},
    json={
        "name": "sample_looker",
        "displayName": "Sample Looker",
        "serviceType": "Looker",
        "description": "Production Looker instance",
        "connection": {
            "config": {
                "type": "Looker",
                "clientId": "your-client-id",
                "clientSecret": "***",
                "hostPort": "https://looker.example.com:443"
            }
        }
    }
)

service = response.json()
print(f"Created: {service['fullyQualifiedName']}")

```

--------------------------------

### Glossary Update Response Example

Source: https://docs.open-metadata.org/v1.12.x/api-reference/governance/glossaries/update

This is an example of the JSON response received after successfully updating a glossary. It includes details like the updated version, timestamps, and modified fields.

```json
{
  "id": "c2940a98-f147-6g46-cdef-31f0c4406dc3",
  "name": "BusinessGlossary",
  "fullyQualifiedName": "BusinessGlossary",
  "displayName": "Business Glossary",
  "description": "Updated: Comprehensive business terminology dictionary",
  "version": 0.2,
  "updatedAt": 1769984330261,
  "updatedBy": "admin",
  "href": "http://localhost:8585/api/v1/glossaries/c2940a98-f147-6g46-cdef-31f0c4406dc3",
  "deleted": false,
  "owners": [],
  "reviewers": [],
  "tags": [],
  "mutuallyExclusive": true
}

```

--------------------------------

### dbt manifest.json Node Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/dbt/dbt-troubleshooting

A sample node from a manifest.json file, illustrating the required keys for dbt processing in OpenMetadata. Ensure 'name/alias, schema, and database' match OpenMetadata table values.

```json
"model.jaffle_shop.customers": {
    "resource_type": "model",
    "depends_on": {
        "nodes": [
            "model.jaffle_shop.stg_customers",
            "model.jaffle_shop.stg_orders",
            "model.jaffle_shop.stg_payments"
        ]
    },
    "database": "dev",
    "schema": "dbt_jaffle",
    "name": "customers",
    "alias": "customers",
    "description": "sample description",
    "columns": {
        "customer_id": {
            "name": "customer_id",
            "description": "This is a unique identifier for a customer",
            "meta": {},
            "data_type": null,
            "quote": null,
            "tags": []
        },
        "first_name": {
            "name": "first_name",
            "description": "Customer's first name. PII.",
            "meta": {},
            "data_type": null,
            "quote": null,
            "tags": []
        }
    },
    "compiled_code": "sample query",
}
```

--------------------------------

### Stored Procedure Definition Example

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/stored-procedures/followers-votes

Example of a stored procedure definition in SQL for calculating an average. This includes variable declarations, a loop for summation, and conditional logic for division.

```sql
CREATE OR REPLACE PROCEDURE calculate_average(numbers INT ARRAY) RETURNS FLOAT NOT NULL LANGUAGE SQL AS $$
DECLARE
  sum_val INT = 0;
  count_val INT = 0;
  average_val FLOAT;
BEGIN
  FOR num IN ARRAY numbers DO
    sum_val := sum_val + num;
    count_val := count_val + 1;
  END FOR;
  IF count_val = 0 THEN
    average_val := 0.0;
  ELSE
    average_val := sum_val / count_val;
  END IF;
  RETURN average_val;
END;$$;
```

--------------------------------

### Authorization Header Example

Source: https://docs.open-metadata.org/api-reference

Example of how to include the JWT Bearer token in the Authorization header for API requests. Obtain your token from Settings > Bots or Profile > Access Tokens.

```http
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

--------------------------------

### Create a Database

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/ingestion/tags

Creates a database entity and links it to a specific service by providing the service's name. The `fullyQualifiedName` is crucial for establishing this relationship.

```python
from metadata.generated.schema.api.data.createDatabase import CreateDatabaseRequest

create_db = CreateDatabaseRequest(
    name="test-db",
    service=db_service_entity.EntityName,
)

create_db_entity = metadata.create_or_update(data=create_db)
```

--------------------------------

### Get Specific User Version

Source: https://docs.open-metadata.org/v1.12.x/api-reference/teams-and-users/users

Retrieve a specific historical version of a user's data by providing both the user ID and the version number using the GET method.

```shell
GET /v1/users/{id}/versions/{version}
```

--------------------------------

### Get or Create Test Suite

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/api-reference/tests-mixin

This method allows you to get an existing test suite by its name or create a new one. You can provide a custom description for the test suite.

```python
get_or_create_test_suite(
    test_suite_name: str,
    test_suite_description: Optional[str] = 'Test Suite created on 2023-12-04'
) → TestSuite
```

--------------------------------

### Create a Database Entity

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/ingestion/lineage

Create a database entity and link it to its parent service using the `fullyQualifiedName`. This establishes the database within the service context.

```python
from metadata.sdk import Databases
from metadata.generated.schema.api.data.createDatabase import CreateDatabaseRequest

create_db = CreateDatabaseRequest(
    name="test-db",
    service=db_service_entity.fullyQualifiedName,
)

create_db_entity = Databases.create(create_db)

```

--------------------------------

### List Storage Services with Fields

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/storage-services/list

Use the `StorageServices.list` method to retrieve a list of storage services. You can specify fields like 'owners', 'tags', and 'domains' to be included in the response. This example also demonstrates iterating through the results and printing owner names.

```python
services = StorageServices.list(
    fields=["owners", "tags", "domains"],
    limit=50
)

for svc in services.data:
    print(f"{svc.fullyQualifiedName}")
    if svc.owners:
        print(f"  Owners: {[o.name for o in svc.owners]}")
```

--------------------------------

### Create a Database Service

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/ingestion/tags

Defines and creates a database service, specifically mocking a MySQL instance. It requires specifying the correct connection configuration class.

```python
from metadata.generated.schema.api.services.createDatabaseService import (
    CreateDatabaseServiceRequest,
)
from metadata.generated.schema.entity.services.connections.database.common.basicAuth import (
    BasicAuth,
)
from metadata.generated.schema.entity.services.connections.database.mysqlConnection import (
    MysqlConnection,
)
from metadata.generated.schema.entity.services.databaseService import (
    DatabaseConnection,
    DatabaseService,
    DatabaseServiceType,
)

db_service = CreateDatabaseServiceRequest(
    name="test-service-db-lineage",
    serviceType=DatabaseServiceType.Mysql,
    connection=DatabaseConnection(
        config=MysqlConnection(
            username="username",
            authType=BasicAuth(password="password"),
            hostPort="http://localhost:1234",
        )
    ),
)

db_service_entity = metadata.create_or_update(data=db_service)
```

--------------------------------

### Global Metadata Command Options

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/dbt/auto-ingest-dbt-core

Examples of using global options like --version, --log-level, and --debug with the metadata ingest-dbt command.

```bash
metadata --version                    # Show version information
metadata --log-level DEBUG ingest-dbt -c /path/to/project  # Set log level
metadata --debug ingest-dbt -c /path/to/project           # Enable debug mode

```

--------------------------------

### Install SAP ERP Connector Dependencies

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/sap-erp/yaml

Install the necessary Python packages for the SAP ERP ingestion connector. This command ensures all required dependencies are available for running the connector.

```bash
pip3 install "openmetadata-ingestion[sap-erp]"
```

--------------------------------

### Fivetran Connector Header Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/fivetran

Example usage of the ConnectorDetailsHeader component to display information for the Fivetran connector. It specifies the icon, name, stage, and lists available and unavailable features.

```javascript
<ConnectorDetailsHeader icon="/public/images/connectors/fivetran.webp" name="Fivetran" stage="PROD" availableFeatures={["Pipelines", "Pipeline Status", "Lineage", "Usage"]} unavailableFeatures={["Owners", "Tags"]} />

```

--------------------------------

### List ML Model Services (Python)

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/mlmodel-services/list

Configure the SDK and list ML Model Services. Supports basic listing, auto-pagination, and selecting specific fields like owners and tags.

```python
from metadata.sdk import configure
from metadata.sdk.entities import MlModelServices

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# List first page
services = MlModelServices.list(limit=50)
for svc in services.data:
    print(f"{svc.fullyQualifiedName} ({svc.serviceType})")

# List all with auto-pagination
for svc in MlModelServices.list_all():
    print(f"{svc.fullyQualifiedName}")

# List with fields
services = MlModelServices.list(
    fields=["owners", "tags", "domains"],
    limit=50
)

for svc in services.data:
    print(f"{svc.fullyQualifiedName}")
    if svc.owners:
        print(f"  Owners: {[o.name for o in svc.owners]}")

```

--------------------------------

### Configure Google SSO Client

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/java

Set up Google as the authentication provider by configuring the SSO client with audience and secret key.

```java
GoogleSSOClientConfig googleSSOClientConfig = new GoogleSSOClientConfig();
ssoConfig.setAudience("https://www.googleapis.com/oauth2/v4/token");
ssoConfig.setSecretKey("{secret_key.json}");
```

```java
server.setAuthProvider(OpenMetadataServerConnection.AuthProvider.GOOGLE);
server.setSecurityConfig(googleSSOClientConfig);
```

--------------------------------

### Dagster Connector Header Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/dagster

An example of how to use the ConnectorDetailsHeader component to display information for the Dagster connector. It specifies the icon, name, stage, and lists its available and unavailable features.

```javascript
<ConnectorDetailsHeader icon="/public/images/connectors/dagster.webp" name="Dagster" stage="PROD" availableFeatures={["Pipelines", "Pipeline Status", "Tags", "Usage", "Lineage"]} unavailableFeatures={["Owners"]} />
```

--------------------------------

### provider_registry.azure_auth_init

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/api-reference

Initialize authentication with Azure AD.

```APIDOC
## azure_auth_init

### Description
Initializes authentication using Azure AD.

### Method
provider_registry.azure_auth_init()
```

--------------------------------

### Salesforce Connector Header Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/salesforce

Example usage of the ConnectorDetailsHeader component to display information for the Salesforce connector. It specifies the icon, name, stage, and lists available and unavailable features.

```javascript
<ConnectorDetailsHeader icon="/public/images/connectors/salesforce.webp" name="Salesforce" stage="PROD" availableFeatures={["Metadata"]} unavailableFeatures={["Query Usage", "Data Profiler", "Data Quality", "dbt", "Lineage", "Column-level Lineage", "Stored Procedures", "Owners", "Tags", "Sample Data", "Auto-Classification"]} />
```

--------------------------------

### List Topics with Owners and Tags

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/topics/list

Fetches a list of up to 50 topics from the 'sample_kafka' service, including owner and tag information. It then iterates through the results to print topic names, owners, and tags.

```python
topics = Topics.list(
    service="sample_kafka",
    fields=["owners", "tags", "domain"],
    limit=50
)

for t in topics.data:
    print(f"{t.fullyQualifiedName}")
    if t.owners:
        print(f"  Owners: {[o.name for o in t.owners]}")
    if t.tags:
        print(f"  Tags: {[t.tagFQN for t in t.tags]}")
```

--------------------------------

### Establish OpenMetadata Server Connection

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/go

Configure connection details for the OpenMetadata server, including BaseURL, APIVersion, retry settings, and authentication token.

```go
// main.go
package main

import (
	"github.com/open-metadata/openmetadata-sdk/openmetadata-go-client/pkg/ometa"
)

func main() {
    restConfig := ometa.NewRestConfig(
		"http://localhost:8585",
		"", // APIVersion
		0, // Retry -> defaults to 3
		0, // RetryWait -> defaults to 30 seconds
		nil, // RetryCodes -> defaults to [429, 504]
		"JWTToken",
	)
}

```

--------------------------------

### Create Database (POST)

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/databases/create

Creates a new database. If a database with the same fullyQualifiedName already exists, a `409` conflict error will be returned.

```APIDOC
## Create Database (POST)

### Description
Creates a new database. If a database with the same `fullyQualifiedName` already exists, a `409` conflict error will be returned.

### Method
POST

### Endpoint
/api/v1/databases

### Parameters
#### Request Body
- **name** (string) - Required - Name of the database. Must be unique within the parent service.
- **service** (string) - Required - Fully qualified name of the parent DatabaseService.
- **displayName** (string) - Optional - Human-readable display name for the database.
- **description** (string) - Optional - Description of the database in Markdown format.
- **retentionPeriod** (string) - Optional - Data retention period in ISO 8601 duration format (e.g., `P365D`).
- **owners** (array) - Optional - Array of owner references (users or teams) to assign to the database.
  - **id** (string) - Required - UUID of the owner entity.
  - **type** (string) - Required - Type of owner entity (e.g., `user`, `team`).
  - **name** (string) - Required - Name of the owner entity.
- **domain** (string) - Optional - Fully qualified name of the domain to assign for governance purposes.
- **tags** (array) - Optional - Array of classification tags to apply to the database.
  - **tagFQN** (string) - Required - Fully qualified name of the tag.
  - **labelType** (string) - Optional - Type of label (e.g., `Manual`, `Derived`, `Propagated`).
  - **state** (string) - Optional - State of the tag (e.g., `Suggested`, `Confirmed`).
- **extension** (object) - Optional - Custom property values defined by your organization’s metadata schema.

### Response
#### Success Response (201)
Returns the created database object with all specified properties and system-generated fields.
- **id** (string) - Unique identifier for the database (UUID format).
- **name** (string) - Database name.
- **fullyQualifiedName** (string) - Fully qualified name in format `service.database`.
- **displayName** (string) - Human-readable display name.
- **description** (string) - Description of the database in Markdown format.
- **service** (object) - Reference to the parent database service.
  - **id** (string) - UUID of the database service.
  - **type** (string) - Type of entity (always `databaseService`).
  - **name** (string) - Name of the database service.
  - **serviceType** (string) - Type of database service (e.g., Snowflake, BigQuery, PostgreSQL).
- **retentionPeriod** (string) - Data retention period in ISO 8601 duration format.
- **owners** (array) - List of owners assigned to the database.
  - **id** (string) - UUID of the owner entity.
  - **type** (string) - Type of owner entity (e.g., `user`, `team`).
  - **name** (string) - Name of the owner entity.
- **domain** (string) - Fully qualified name of the assigned domain.
- **tags** (array) - Classification tags applied to the database.
  - **tagFQN** (string) - Fully qualified name of the tag.
  - **labelType** (string) - Type of label (e.g., `Manual`, `Derived`, `Propagated`).
  - **state** (string) - State of the tag (e.g., `Suggested`, `Confirmed`).
- **extension** (object) - Custom property values defined by your organization’s metadata schema.
- **version** (number) - Version number for the entity (starts at 0.1).
```

--------------------------------

### Implement Connector with Cursor

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/developing-a-new-connector/ai-assisted-development/build-with-ai

Use Cursor's Composer to implement TODO items by referencing context and reference connector files. Work file-by-file starting with client.py.

```bash
@CONNECTOR_CONTEXT.md Implement all the TODO items in the scaffolded connector files.
Use the metabase connector as a reference pattern.
Follow the standards in .cursor/skills/
```

--------------------------------

### Set Environment Variables for Kafka Plugin

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/ingestion-framework

Environment variables to set if the kafka plugin installation still fails after installing librdkafka. These variables help the build process locate the library.

```bash
export C_INCLUDE_PATH=/opt/homebrew/include
```

```bash
export LIBRARY_PATH=/opt/homebrew/lib
```

--------------------------------

### Create Test Suite using Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-quality/test-suites/create

Use the Python SDK to create logical and executable test suites. Ensure the SDK is configured with your OpenMetadata instance host and JWT token.

```python
from metadata.sdk import configure
from metadata.sdk.entities import TestSuites
from metadata.generated.schema.api.tests.createTestSuite import CreateTestSuiteRequest

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# Create a logical test suite
request = CreateTestSuiteRequest(
    name="critical_data_quality_checks",
    displayName="Critical Data Quality Checks",
    description="Groups all critical data quality test cases across production tables",
    executable=False
)

test_suite = TestSuites.create(request)
print(f"Created: {test_suite.name}")

# Create an executable test suite
request = CreateTestSuiteRequest(
    name="dim_address_test_suite",
    displayName="Data Contract - dim_address",
    description="Executable test suite for dim_address table",
    executable=True
)

test_suite = TestSuites.create(request)
print(f"Created: {test_suite.fullyQualifiedName}")

```

--------------------------------

### Run Connector Scaffold in Interactive Mode

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/developing-a-new-connector/ai-assisted-development/scaffold-connector

Activate your virtual environment and run the `metadata scaffold-connector` command without arguments to enter interactive mode. The tool will prompt you for details about the connector.

```bash
source env/bin/activate
metadata scaffold-connector

```

--------------------------------

### Example Custom SQL Query for Table Test

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/data-quality-observability/quality/tests-yaml

An example of a SQL query to be used with the 'tableCustomSQLQuery' test definition. This query selects customer IDs based on a lifetime value condition.

```sql
SELECT
customer_id
FROM DUAL
WHERE lifetime_value < 0;
```

--------------------------------

### Databricks Initialization Script for Spark Agent

Source: https://docs.open-metadata.org/v1.12.x/connectors/ingestion/lineage/spark-lineage

This script prepares the Databricks environment by copying the OpenLineage Spark Listener JAR and configuring Spark driver settings. Ensure the STAGE_DIR_JAR path is correctly set to your uploaded JAR.

```bash
#!/bin/bash

STAGE_DIR_JAR="<path to jar copied from step 1>"

echo "BEGIN: Upload Spark Listener JARs"
cp -f $STAGE_DIR_JAR /mnt/driver-daemon/jars || { echo "Error copying Spark Listener library file"; exit 1;}
echo "END: Upload Spark Listener JARs"

echo "BEGIN: Modify Spark config settings"
cat << 'EOF' > /databricks/driver/conf/openlineage-spark-driver-defaults.conf
[driver] {
  "spark.extraListeners" = "io.openlineage.spark.agent.OpenLineageSparkListener"
}
EOF
echo "END: Modify Spark config settings"

```

--------------------------------

### Version Matrix Usage

Source: https://docs.open-metadata.org/v1.12.x/deployment/upgrade/bare-metal

This code demonstrates how to use the VersionMatrix component by passing the version data to it.

```javascript
<VersionMatrix data={VERSION_MATRIX_DATA_WITH_UPDATES} />
```

--------------------------------

### Troubleshoot MySQL Pod Startup Failures

Source: https://docs.open-metadata.org/v1.12.x/deployment/upgrade/kubernetes-troubleshooting

Steps to resolve MySQL pod startup failures after upgrading the OpenMetadata Dependencies Helm Chart to versions 0.0.49 or 0.0.50. This involves backing up the database, uninstalling and reinstalling the dependencies chart, and restoring the database.

```bash
kubectl delete pvc data-mysql-0
```

--------------------------------

### Sampler Constructor Parameters

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/codebase-deep-dives/sampler

Defines the parameters required to initialize the SamplerInterface, including connection details, entity information, sampling configuration, and optional parameters for partitions, custom queries, columns, and storage.

```python
SamplerInterface(
    service_connection_config,    # Database connection config
    ometa_client,                 # OpenMetadata API client
    entity,                       # Table entity being sampled
    sample_config,                # SampleConfig (percentage, rows, method)
    partition_details,            # PartitionProfilerConfig (optional)
    sample_query,                 # Custom SQL query (optional)
    include_columns,              # Columns to include (optional)
    exclude_columns,              # Columns to exclude (optional)
    sample_data_count,            # Number of rows to fetch (default: 100)
    storage_config,               # External storage for sample data (optional)
)

```

--------------------------------

### List All Database Services with Auto-Pagination (Python)

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/database-services/list

The `DatabaseServices.list_all` method simplifies fetching all database services by handling pagination automatically. You can control the `batch_size` for fetching.

```python
from metadata.sdk import configure
from metadata.sdk.entities import DatabaseServices

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# List all with auto-pagination
all_services = DatabaseServices.list_all(batch_size=100)
for service in all_services:
    print(f"{service.fullyQualifiedName}")
```

--------------------------------

### Configure OpenMetadata Server for SSL

Source: https://docs.open-metadata.org/v1.12.x/deployment/security/enable-ssl/openmetadata-server

Add this section to your `openmetadata.yaml` file to configure the server to use HTTPS. Ensure you replace `test12` with your actual keystore password.

```yaml
server:
  rootPath: '/api/*'
  applicationConnectors:
    - type: https
      port: ${SERVER_PORT:-8585}
      keyStorePath: ./conf/openmetadata.keystore.jks
      keyStorePassword: test12
      keyStoreType: JKS
      supportedProtocols: [TLSv1.2, TLSv1.5]
      excludedProtocols: [SSL, SSLv2, SSLv2Hello, SSLv3]

```

--------------------------------

### Download Docker Compose for MySQL (wget)

Source: https://docs.open-metadata.org/latest/quick-start/local-docker-deployment

Downloads the docker-compose.yml file for deploying OpenMetadata with a MySQL backend using wget.

```bash
wget https://github.com/open-metadata/OpenMetadata/releases/download/1.12.6-release/docker-compose.yml

```

--------------------------------

### Add MCP Server using JSON Configuration

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/mcp/claude-code

Adds the OpenMetadata MCP Server using a JSON configuration, including PAT authentication. Replace `<YOUR-OpenMetadata-SERVER>` and `<YOUR-OpenMetadata-PAT>`.

```bash
claude mcp add-json openmetadata '{ "type": "http", "url": "https://<YOUR-OpenMetadata-SERVER>/mcp", "headers": { "Authorization": "Bearer <YOUR-OpenMetadata-PAT>" } }'
```

--------------------------------

### Example Custom SQL Query with Join for Table Test

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/data-quality-observability/quality/tests-yaml

Another example of a SQL query for the 'tableCustomSQLQuery' test, demonstrating the use of a JOIN clause to combine data from multiple tables before applying the filter.

```sql
SELECT
customer_id
FROM DUAL d
INNER JOIN OTHER o ON d.id = o.id
WHERE lifetime_value < 0;
```

--------------------------------

### Python SDK for Database Service Import/Export

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/database-services/import-export

Demonstrates how to use the Python SDK to export database services to CSV and import them back. Includes examples for synchronous and asynchronous operations, as well as dry-run functionality for imports.

```python
from metadata.sdk import configure
from metadata.sdk.entities import DatabaseServices

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# Synchronous export
csv_data = DatabaseServices.export_csv("snowflake_prod").execute()
print(csv_data)

# Async export
job = DatabaseServices.export_csv("snowflake_prod").execute_async()
print(f"Export job: {job}")

# Synchronous import (dry run first)
result = (
    DatabaseServices.import_csv("snowflake_prod")
    .with_data(csv_data)
    .set_dry_run(True)
    .execute()
)
print(f"Dry run result: {result}")

# Apply the import
result = (
    DatabaseServices.import_csv("snowflake_prod")
    .with_data(csv_data)
    .set_dry_run(False)
    .execute()
)

# Async import
result = (
    DatabaseServices.import_csv("snowflake_prod")
    .with_data(csv_data)
    .set_dry_run(False)
    .execute_async()
)

```

--------------------------------

### utils.get_entity_type

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/api-reference

Get the type of an entity.

```APIDOC
## get_entity_type

### Description
Given an Entity T, return its type.

### Method
utils.get_entity_type(entity: T)
```

--------------------------------

### Sample Domo Dashboard YAML Configuration

Source: https://docs.open-metadata.org/v1.12.x/connectors/dashboard/domo-dashboard/yaml

A sample YAML configuration file for connecting to Domo Dashboard. This configuration includes source details, client ID, secret token, access token, API host, and instance domain.

```yaml
source:
  type: domoDashboard
  serviceName: "domo_dashboard_service"
  # Client ID to Connect to DOMO Dashboard
  clientId: "YOUR_CLIENT_ID"
  # Secret Token to Connect DOMO Dashboard
  secretToken: "YOUR_SECRET_TOKEN"
  # Access Token to Connect to DOMO Dashboard
  accessToken: "YOUR_ACCESS_TOKEN"
  # API Host to Connect to DOMO Dashboard instance
  apiHost: "api.domo.com"
  # URL to connect to your Domo instance UI. For example https://<your>.domo.com
  instanceDomain: "https://<your>.domo.com"
sourceConfig:
  config:
    type: dashboard
```

--------------------------------

### List Available Tools Response

Source: https://docs.open-metadata.org/v1.12.x/how-to-guides/mcp/connect

Sample JSON-RPC response detailing the tools available on the MCP server. Each tool includes its name, description, and input schema.

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "search_metadata",
        "description": "Find your data and business terms in OpenMetadata. For example if the user asks to 'find tables that contain customers information', then 'customers' should be the query, and the entity_type should be 'table'. Here make sure to use 'Href' is available in result to create a hyperlink to the entity in OpenMetadata.",
        "inputSchema": {
          "type": "object",
          "properties": {
            "query": {
              "type": "string",
              "description": "Keywords to use for searching."
            },
            "entity_type": {
              "type": "string",
              "description": "Optional entity type to filter results..."
            },
            "limit": {
              "type": "integer",
              "description": "Maximum number of results to return. Default is 10."
            },
            "fields": {
              "type": "string",
              "description": "Comma-separated list of additional fields to include..."
            }
          },
          "required": ["query"]
        }
      },
      {
        "name": "get_entity_details",
        "description": "Get detailed information about a specific entity",
        "inputSchema": {
          "type": "object",
          "properties": {
            "entity_type": {
              "type": "string",
              "description": "Type of entity"
            },
            "fqn": {
              "type": "string",
              "description": "Fully qualified name of the entity"
            }
          },
          "required": ["entity_type", "fqn"]
        }
      }
    ]
  }
}
```

--------------------------------

### Athena Connector Header Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/athena

Example usage of the ConnectorDetailsHeader component for the Athena connector. This demonstrates how to pass the necessary props to display Athena's specific information, including its icon, stage, and feature availability.

```javascript
<ConnectorDetailsHeader
  icon="/public/images/connectors/athena.webp"
  name="Athena"
  stage="PROD"
  availableFeatures={[
"Metadata",
"Query Usage",
"Lineage",
"Column-level Lineage",
"Data Profiler",
"Data Quality",
"dbt"
]}/
  unavailableFeatures={[
"Owners",
"Stored Procedures"
]} />
```

--------------------------------

### Initialize No Auth Provider

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/api-reference/provider-registry

Initializes the system without any specific authentication provider. This is typically used when no authentication is required or configured.

```python
no_auth_init(config: OpenMetadataConnection) → AuthenticationProvider
```

--------------------------------

### Multi-Table Checkpoint Example with Great Expectations

Source: https://docs.open-metadata.org/v1.12.x/connectors/ingestion/great-expectations

Validate multiple tables within a single Great Expectations checkpoint run. This example demonstrates setting up separate validations for 'users' and 'orders' tables using a PostgreSQL data source.

```python
import great_expectations as gx
from great_expectations.checkpoint import Checkpoint

context = gx.get_context()
conn_string = "postgresql+psycopg2://user:pw@host:port/db"

data_source = context.sources.add_postgres(
  name="my_datasource",
  connection_string=conn_string,
)

# Set up users table validation
users_asset = data_source.add_table_asset(
  name="users_asset",
  table_name="users",
  schema_name="public",
)
users_suite = "users_suite"
context.add_or_update_expectation_suite(expectation_suite_name=users_suite)
users_validator = context.get_validator(
  batch_request=users_asset.build_batch_request(),
  expectation_suite_name=users_suite,
)
users_validator.expect_column_values_to_not_be_null(column="email")
users_validator.save_expectation_suite(discard_failed_expectations=False)

# Set up orders table validation
orders_asset = data_source.add_table_asset(
  name="orders_asset",
  table_name="orders",
  schema_name="public",
)
orders_suite = "orders_suite"
context.add_or_update_expectation_suite(expectation_suite_name=orders_suite)
orders_validator = context.get_validator(
  batch_request=orders_asset.build_batch_request(),
  expectation_suite_name=orders_suite,
)
orders_validator.expect_column_values_to_be_between(column="amount", min_value=0, max_value=1000000)
orders_validator.save_expectation_suite(discard_failed_expectations=False)
```

--------------------------------

### Create Domain using Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/governance/domains/create

Use the OpenMetadata Python SDK to create a new domain. Ensure you have configured the SDK with your host and JWT token.

```python
from metadata.sdk import configure
from metadata.sdk.entities import Domains
from metadata.generated.schema.api.domains.createDomain import CreateDomainRequest

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

request = CreateDomainRequest(
    name="TestDomain",
    displayName="Test Domain",
    domainType="Aggregate",
    description="Lorem ipsum..."
)

domain = Domains.create(request)
print(f"Created: {domain.fullyQualifiedName}")

```

--------------------------------

### Create OpenMetadata Gateway

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/go

Instantiate the OpenMetadata Gateway using the configured connection details.

```go
// main.go
...

func main() {
    ...
    rest := ometa.NewRest(restConfig)
}

```

--------------------------------

### Start OpenMetadata Docker Compose with Cognito

Source: https://docs.open-metadata.org/v1.12.x/deployment/security/amazon-cognito-sso/docker

Use the Docker Compose command with the --env-file flag to start your OpenMetadata services using the previously created Cognito environment configuration. This command runs the services in detached mode.

```bash
docker compose --env-file ~/openmetadata_cognito.env up -d

```

--------------------------------

### List All Databases with Auto-Pagination

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/databases/list

Employ the `Databases.list_all` method for seamless retrieval of all databases, handling pagination automatically. Configure the `batch_size` to manage the number of items fetched per request. This is useful for processing large numbers of databases without manual pagination logic.

```Python
from metadata.sdk import configure
from metadata.sdk.entities import Databases

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# List all with auto-pagination
all_databases = Databases.list_all(batch_size=100)
for database in all_databases:
    print(f"{database.fullyQualifiedName}")
```

--------------------------------

### List and Retrieve Database Versions in Python

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/databases/versions

Use the `Databases.get_versions` method to list all versions of a database and `Databases.get_specific_version` to retrieve a particular version. Ensure the SDK is configured with your host and JWT token.

```python
from metadata.sdk import configure
from metadata.sdk.entities import Databases

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# List all versions
versions = Databases.get_versions("550e8400-e29b-41d4-a716-446655440000")
for v in versions:
    print(f"Version {v.version}: {v.description}")

# Get a specific version
database_v1 = Databases.get_specific_version(
    "550e8400-e29b-41d4-a716-446655440000",
    "0.1"
)
print(f"Original description: {database_v1.description}")

```

--------------------------------

### Get Columns

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/tables/relationships

Retrieve column information with optional pagination.

```APIDOC
## GET /v1/tables/{id}/columns

### Description
Retrieve column information with optional pagination.

### Method
GET

### Endpoint
/v1/tables/{id}/columns

### Parameters
#### Path Parameters
- **id** (string) - Required - UUID of the table.

#### Query Parameters
- **limit** (integer) - Optional - Maximum number of columns to return. Defaults to "10".
- **offset** (integer) - Optional - Offset for pagination. Defaults to "0".

### Response
#### Success Response (200)
- Returns a paginated list of column definitions.
```

--------------------------------

### Upload dbt Artifacts to Azure Blob Storage

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/dbt/storage-azure-guide

Python function to upload dbt artifacts to Azure Blob Storage using the azure-storage-blob library. Requires installation via 'pip install azure-storage-blob'. Handles authentication via connection string or account key.

```python
def upload_artifacts_to_azure(**context):
    """
    Upload dbt artifacts to Azure Blob Storage.

    Uses azure-storage-blob library.
    Install with: pip install azure-storage-blob
    """
    from azure.storage.blob import BlobServiceClient

    target_dir = os.path.join(DBT_PROJECT_DIR, "target")

    # Initialize Azure Blob Service Client
    if AZURE_CONNECTION_STRING:
        blob_service_client = BlobServiceClient.from_connection_string(
            AZURE_CONNECTION_STRING
        )
    else:
        account_url = f"https://{AZURE_STORAGE_ACCOUNT}.blob.core.windows.net"
        blob_service_client = BlobServiceClient(
            account_url=account_url,
            credential=AZURE_STORAGE_KEY
        )

    container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

    # Files to upload
    artifacts = [
        ("manifest.json", True),      # Required
        ("catalog.json", False),      # Optional but recommended
        ("run_results.json", False),  # Optional
        ("sources.json", False),      # Optional
    ]

    uploaded = []
    failed = []

    for filename, required in artifacts:
        local_path = os.path.join(target_dir, filename)

        if os.path.exists(local_path):
            try:
                blob_client = container_client.get_blob_client(filename)
                with open(local_path, "rb") as data:
                    blob_client.upload_blob(data, overwrite=True)

                uploaded.append(filename)
                print(f"✓ Uploaded {filename} to Azure Blob Storage")
            except Exception as e:
                error_msg = f"✗ Failed to upload {filename}: {e}"
                print(error_msg)
                if required:
                    raise Exception(error_msg)
                failed.append(filename)
        else:
            if required:
                raise FileNotFoundError(
                    f"Required artifact not found: {local_path}\n"
                    f"Make sure 'dbt run' completed successfully."
                )
            else:
                print(f"⊘ Skipping {filename} (not found - optional)")

    # Log summary
    print(f"\n{'='*50}")
    print(f"Upload Summary:")
    print(f"  Uploaded: {', '.join(uploaded) or 'None'}")
    print(f"  Skipped:  {', '.join(failed) or 'None'}")
    print(f"  Azure Location: {AZURE_STORAGE_ACCOUNT}/{AZURE_CONTAINER_NAME}/")
    print(f"{ '='*50}")

    return {
        "uploaded": uploaded,
        "storage_account": AZURE_STORAGE_ACCOUNT,
        "container": AZURE_CONTAINER_NAME
    }
```

--------------------------------

### Configure Workflow and OpenMetadata Server

Source: https://docs.open-metadata.org/v1.12.x/connectors/api/rest/yaml

Set up workflow logging levels and OpenMetadata server connection details, including host, authentication, and JWT token. Optionally configure service connection storage and SSL verification.

```yaml
workflowConfig:
  loggerLevel: INFO  # DEBUG, INFO, WARNING or ERROR
  openMetadataServerConfig:
    hostPort: "http://localhost:8585/api"
    authProvider: openmetadata
    securityConfig:
      jwtToken: "{bot_jwt_token}"
    ## Store the service Connection information
    storeServiceConnection: true  # false
    ## Secrets Manager Configuration
    # secretsManagerProvider: aws, azure or noop
    # secretsManagerLoader: airflow or env
    ## If SSL, fill the following
    # verifySSL: validate  # or ignore
    # sslConfig:
    #   caCertificate: /local/path/to/certificate
# ingestionPipelineFQN: <service name>.<ingestion name> ## e.g., "my_redshift.metadata"
```

--------------------------------

### Creating a Tag

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/ingestion/tags

Example of creating a tag within an existing classification.

```APIDOC
## Creating the Tag

Once there is an existing classification, we create tags within that given classification:

```python
tag_request=CreateTagRequest(
    classification=classification_request.name,
    name="TestTag",
    description="Sample Tag.",
)

metadata.create_or_update(tag_request)
```
```

--------------------------------

### Redshift SSL Configuration Example

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/redshift

To integrate SSL, add the SSL configuration under connectionArguments in the source configuration. The 'sslmode' parameter determines the SSL behavior.

```yaml
source:
  type: redshift
  connectionArguments:
    sslmode: prefer
    # Other connection arguments can be added here
```

--------------------------------

### Configure Lineage with Dictionary Inlets/Outlets

Source: https://docs.open-metadata.org/v1.12.x/connectors/pipeline/airflow/configuring-lineage

Use dictionaries to define inlets and outlets for tasks, specifying entity type, FQN, and grouping keys. This approach does not require the openmetadata-ingestion package.

```python
from datetime import timedelta

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=1),
}


with DAG(
    "test-lineage",
    default_args=default_args,
    description="An example DAG which runs a lineage test",
    start_date=days_ago(1),
    is_paused_upon_creation=False,
    catchup=False,
) as dag:


    t0 = DummyOperator(
        task_id='task0',
        inlets=[
            {"entity": "container", "fqn": "Container A", "key": "group_A"},
            {"entity": "table", "fqn": "Table X", "key": "group_B"},
        ]
    )

    t1 = DummyOperator(
        task_id='task10',
        outlets=[
            {"entity": "table", "fqn": "Table B", "key": "group_A"},
            {"entity": "table", "fqn": "Table Y", "key": "group_B"},
        ]
    )

    t0 >> t1

```

--------------------------------

### Creating a Classification

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/ingestion/tags

Example of creating a classification to group tag definitions.

```APIDOC
## Creating a Classification

Classifications are the entities we use to group tag definitions. Let’s create a sample one:

```python
from metadata.generated.schema.api.classification.createClassification import (
    CreateClassificationRequest,
)
from metadata.generated.schema.api.classification.createTag import CreateTagRequest

classification_request=CreateClassificationRequest(
    name="TestClassification",
    description="Sample classification.",
)

metadata.create_or_update(classification_request)
```
```

--------------------------------

### Get User by ID

Source: https://docs.open-metadata.org/v1.12.x/api-reference/teams-and-users/users

Retrieves a specific user by their unique identifier.

```APIDOC
## GET /v1/users/{id}

### Description
Get user by ID.

### Method
GET

### Endpoint
/v1/users/{id}

### Parameters
#### Path Parameters
- **id** (string) - Required - The unique identifier of the user.
```

--------------------------------

### Create OpenMetadata Directory

Source: https://docs.open-metadata.org/v1.12.x/quick-start/local-docker-deployment

Create a dedicated directory for the OpenMetadata Docker deployment and navigate into it.

```bash
mkdir openmetadata-docker && cd openmetadata-docker
```

--------------------------------

### Get Specific Domain Version

Source: https://docs.open-metadata.org/v1.12.x/api-reference/governance/domains

Retrieves a specific version of a domain.

```APIDOC
## GET /v1/domains/{id}/versions/{version}

### Description
Retrieves a specific version of a domain.

### Method
GET

### Endpoint
/v1/domains/{id}/versions/{version}

### Parameters
#### Path Parameters
- **id** (string) - Required - The unique identifier of the domain.
- **version** (string) - Required - The version number of the domain.
```

--------------------------------

### Display Help Message for openmetadata-ops.sh

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/openmetadata-ops

Use the --help option to display the help message and see all available options and commands for the openmetadata-ops.sh script.

```bash
sh bootstrap/openmetadata-ops.sh --help
```

--------------------------------

### Tagging a Column

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/ingestion/tags

Example of applying a tag to a specific column within a table.

```APIDOC
## Tagging a Column

The same idea can be replicated to tag a column:

```python
metadata.patch_column_tag(
    entity_id=table.id,
    tag_fqn="TestClassification.TestTag",
    column_name="id",
)
```
```

--------------------------------

### Go SDK Post Method

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/go-api-methods

Use the Post method to create new resources. The data payload must be a map[string]interface{} matching the expected schema for the resource.

```go
// main.go
... 
func main() {
    ...
    path := "tables"
    data := map[string]interface{}{
        "name":           "goClientTestTable",
        "databaseSchema": "sample_data.ecommerce_db.shopify",
        "columns": []map[string]interface{}{
            {
                "name":     "columnOne",
                "dataType": "NUMBER",
            },
            {
                "name":     "columnTwo",
                "dataType": "NUMBER",
            },
        },
    }
	body, err := rest.Post(path, data, nil, nil, nil)
}
```

--------------------------------

### Get Test Definitions

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/ai-sdk

List all available data quality test definitions.

```APIDOC
## Get Test Definitions

### Description
Retrieves a list of all predefined data quality test definitions available in the system.

### Method
`client.mcp.call_tool("get_test_definitions", params)`

### Parameters
#### Request Body
- **entity_type** (string) - Optional - Filter definitions by entity type.

### Response
- **data** (list): A list of test definition objects.
```

--------------------------------

### Delete Database using Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/databases/delete

Demonstrates how to delete databases by ID or name using the Python SDK. Supports soft delete, hard delete, and recursive deletion. Also shows how to restore a soft-deleted database.

```python
from metadata.sdk import configure
from metadata.sdk.entities import Databases

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# Soft delete by ID
Databases.delete("550e8400-e29b-41d4-a716-446655440000")

# Hard delete with recursive
Databases.delete(
    "550e8400-e29b-41d4-a716-446655440000",
    recursive=True,
    hard_delete=True
)

# Delete by name
Databases.delete_by_name("snowflake_prod.analytics")

# Delete by name with options
Databases.delete_by_name(
    "snowflake_prod.analytics",
    recursive=True,
    hard_delete=True
)

# Restore a soft-deleted database
Databases.restore("550e8400-e29b-41d4-a716-446655440000")

```

--------------------------------

### Get Entity Lineage

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/ai-sdk

Retrieve upstream and downstream lineage for a given entity.

```APIDOC
## Get Entity Lineage

### Description
Retrieves the upstream and downstream data lineage for a specified entity.

### Method
`client.mcp.call_tool("get_entity_lineage", params)`

### Parameters
#### Request Body
- **entity_id** (string) - Required - The unique identifier of the entity.
- **upstream_depth** (integer) - Optional - The depth to explore upstream lineage. Defaults to 1.
- **downstream_depth** (integer) - Optional - The depth to explore downstream lineage. Defaults to 1.

### Response
- **data** (object): An object containing lineage information.
```

--------------------------------

### Get Tag by ID

Source: https://docs.open-metadata.org/v1.12.x/api-reference/governance/tags

Retrieves a specific tag using its unique identifier.

```APIDOC
## GET /v1/tags/{id}

### Description
Gets a tag by its ID.

### Method
GET

### Endpoint
/v1/tags/{id}

### Parameters
#### Path Parameters
- **id** (string) - Required - The unique identifier of the tag.
```

--------------------------------

### Create Azure Resource Group and Storage Account

Source: https://docs.open-metadata.org/v1.12.x/connectors/database/dbt/storage-azure-guide

Sets up necessary Azure resources including a resource group and a unique storage account. Ensure your storage account name is globally unique.

```bash
# Set your variables
export RESOURCE_GROUP="dbt-metadata-rg"
export LOCATION="eastus"
export STORAGE_ACCOUNT="dbtartifacts${RANDOM}"  # Must be globally unique
export CONTAINER_NAME="dbt-artifacts"

# Login to Azure
az login

# Create resource group
az group create \
    --name ${RESOURCE_GROUP} \
    --location ${LOCATION}

# Create storage account
az storage account create \
    --name ${STORAGE_ACCOUNT} \
    --resource-group ${RESOURCE_GROUP} \
    --location ${LOCATION} \
    --sku Standard_LRS \
    --kind StorageV2

# Verify creation
az storage account show \
    --name ${STORAGE_ACCOUNT} \
    --resource-group ${RESOURCE_GROUP} \
    --query "name" -o tsv
```

--------------------------------

### Configure SDK Client

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/ingestion/lineage

Configure the OpenMetadata SDK client with the server host and authentication token.

```APIDOC
from metadata.sdk import configure

configure(
    host="http://localhost:8585/api",
    jwt_token="<token>",
)
```

--------------------------------

### Get Glossary by ID

Source: https://docs.open-metadata.org/v1.12.x/api-reference/governance/glossaries

Retrieve a specific glossary using its unique identifier.

```shell
GET /v1/glossaries/{id}
```

--------------------------------

### Get Domain by ID

Source: https://docs.open-metadata.org/v1.12.x/api-reference/governance/domains

Retrieves a specific domain using its unique identifier.

```APIDOC
## GET /v1/domains/{id}

### Description
Retrieves a domain by its ID.

### Method
GET

### Endpoint
/v1/domains/{id}

### Parameters
#### Path Parameters
- **id** (string) - Required - The unique identifier of the domain.
```

--------------------------------

### List and Retrieve Topic Versions using Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/topics/versions

Demonstrates how to list all versions of a topic and retrieve a specific version using the OpenMetadata Python SDK. Ensure the SDK is configured with your host and JWT token.

```python
from metadata.sdk import configure
from metadata.sdk.entities import Topics

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

# List all versions
versions = Topics.get_versions("0a021819-982e-4ee4-a5a2-4af30eaa3016")
for v in versions:
    print(f"Version {v.version}: {v.description}")

# Get a specific version
topic_v1 = Topics.get_specific_version(
    "0a021819-982e-4ee4-a5a2-4af30eaa3016",
    "0.1"
)
print(f"Original description: {topic_v1.description}")

```

--------------------------------

### Get Classification by ID

Source: https://docs.open-metadata.org/v1.12.x/api-reference/governance/classifications

Retrieve a specific classification using its unique identifier.

```APIDOC
## GET /v1/classifications/{id}

### Description
Get a classification by its ID.

### Method
GET

### Endpoint
/v1/classifications/{id}

### Parameters
#### Path Parameters
- **id** (string) - Required - The unique identifier of the classification.
```

--------------------------------

### Get Classification by ID

Source: https://docs.open-metadata.org/v1.12.x/api-reference/governance/classifications

Retrieve a specific classification using its unique identifier.

```http
GET /v1/classifications/{id}
```

--------------------------------

### Get Specific Topic Version

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/topics/versions

Retrieves a specific historical version of a topic.

```APIDOC
## GET /v1/topics/{id}/versions/{version}

### Description
Retrieves a specific historical version of a topic.

### Method
GET

### Endpoint
/v1/topics/{id}/versions/{version}

### Parameters
#### Path Parameters
- **id** (string) - Required - UUID of the topic.
- **version** (string) - Required - Version number to retrieve (e.g., `0.2`).

### Response
#### Success Response (200)
- Returns the full topic object as it existed at the specified version.

### Response Example
(Example response for a specific version would be a full topic object, similar to the serialized snapshots in the list versions response but not serialized within a string.)
```

--------------------------------

### Build and Run Local Docker Environment (Fast Rebuild)

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/developing-a-new-connector/ai-assisted-development/build-with-ai

Perform a fast rebuild of the OpenMetadata stack in Docker, skipping Maven and UI builds. This is ideal for quick iteration on ingestion-only code changes.

```bash
./docker/run_local_docker.sh -m ui -d mysql -s true -i true -r false

```

--------------------------------

### Get Sample Data

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/tables/sample-data

Retrieves the sample data rows for a specific table.

```APIDOC
## GET /v1/tables/{id}/sampleData

### Description
Retrieves the sample data rows for a specific table.

### Method
GET

### Endpoint
/v1/tables/{id}/sampleData

#### Path Parameters
- **id** (string) - Required - UUID of the table.
```

--------------------------------

### Automated SQL Lineage via CLI Execution

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/ingestion/lineage

Execute the lineage ingestion process using the CLI with a prepared configuration file.

```bash
metadata lineage -c path/to/your_config_yaml.yaml
```

--------------------------------

### Get Profiler Config

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/databases/advanced

Retrieves the profiler configuration for a specific database entity.

```APIDOC
## Get Profiler Config

### Description
Retrieves the profiler configuration for a specific database entity.

### Method
GET

### Endpoint
/v1/databases/{id}/profilerConfig
```

--------------------------------

### Retrieve a Database Schema

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/database-schemas/create

Get the details of a specific database schema by its ID.

```APIDOC
## GET /api/v1/databaseSchemas/{id}

### Description
Get a database schema by the Id.

### Method
GET

### Endpoint
/api/v1/databaseSchemas/{id}

### Parameters
#### Path Parameters
- **id** (uuid) - Required - The database schema Id you want to get.

#### Query Parameters
- **fields** (string) - Optional - Comma-separated list of fields to include in the response.

### Response
#### Success Response (200 OK)
- **body** (object) - Database schema object

#### Response Example
{
  "example": "{\n  \"id\": \"00000000-0000-0000-0000-000000000000\",\n  \"name\": \"my_schema\",\n  \"displayName\": \"My Schema\",\n  \"description\": \"This is my database schema.\",\n  \"database\": {\n    \"id\": \"a1b2c3d4-e5f6-7890-1234-567890abcdef\",\n    \"type\": \"database\"\n  },\n  \"fullyQualifiedName\": \"my_database.my_schema\",\n  \"version\": 0,\n  \"updatedAt\": \"2023-10-27T10:00:00.000Z\",\n  \"updatedBy\": \"user@example.com\",\n  \"href\": \"http://localhost:8585/api/v1/databaseSchemas/00000000-0000-0000-0000-000000000000\"\n}"
```

--------------------------------

### Get Specific Chart Version

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/charts

Retrieves a specific historical version of a chart.

```APIDOC
## GET /v1/charts/{id}/versions/{version}

### Description
Get a specific version of a chart.

### Method
GET

### Endpoint
/v1/charts/{id}/versions/{version}

### Parameters
#### Path Parameters
- **id** (string) - Required - The unique identifier of the chart.
- **version** (string) - Required - The version number of the chart to retrieve.
```

--------------------------------

### Ingest Sample Usage Data

Source: https://docs.open-metadata.org/v1.12.x/developers/contribute/build-code-and-run-tests/openmetadata-server

Load sample usage data into the database using the metadata usage command with a specified configuration file.

```bash
metadata usage -c ./pipelines/sample_usage.json
```

--------------------------------

### Install OpenMetadata Dependencies Helm Chart

Source: https://docs.open-metadata.org/v1.12.x/deployment/kubernetes/eks/airflow

Deploy the openmetadata-dependencies Helm chart using a custom values file to configure EFS persistent volumes for Airflow.

```bash
helm install openmetadata-dependencies open-metadata/openmetadata-dependencies --values values-dependencies.yaml

```

--------------------------------

### Update Entities

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/overview

Example of updating an existing entity by retrieving it, modifying its properties, and then updating it.

```APIDOC
from metadata.sdk import Tables

table = Tables.retrieve_by_name("service.database.schema.table")
table.description = "Updated description"
updated = Tables.update(str(table.id), table)
```

--------------------------------

### Tagging a Table

Source: https://docs.open-metadata.org/v1.12.x/api-reference/sdk/python/ingestion/tags

Example of applying a tag to an existing table using the `patch_tag` method.

```APIDOC
## Tagging a Table

Now that we have the Tag, we can proceed and tag a specific asset. In this example, we’ll tag the Table we created above. For that, the API uses a PATCH request, but the Python SDK has a helper method that handles most of the work:

```python
from metadata.generated.schema.entity.data.table import Table

metadata.patch_tag(
    entity=Table,
    entity_id=table.id,
    tag_fqn="TestClassification.TestTag",
)
```

If we now check the tags for the Table, the new tag will be appearing in there. Note that we now used the `patch_tag` method because the Table already existed. If we can control the Tag creation process when the Table metadata is generated, we can assign the tags in the `tags` property of `CreateTableRequest`.
```

--------------------------------

### List Data Product Versions

Source: https://docs.open-metadata.org/v1.12.x/api-reference/governance/data-products

Retrieve a list of all historical versions for a specific data product.

```bash
GET /v1/dataProducts/{id}/versions
```

--------------------------------

### Response for Adding a Follower

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/dashboards/followers-votes

This is an example JSON response when a follower is successfully added to a dashboard.

```json
{
  "id": "03fb5cc3-de48-423f-9926-8e192e5de59d",
  "name": "10",
  "displayName": "deck.gl Demo",
  "fullyQualifiedName": "sample_superset.10",
  "description": "",
  "version": 0.1,
  "updatedAt": 1769982666437,
  "updatedBy": "admin",
  "sourceUrl": "http://localhost:808/superset/dashboard/10/",
  "service": {
    "id": "b1e6a71d-7f47-4e5f-8ce0-e6e8a88ec97a",
    "type": "dashboardService",
    "name": "sample_superset",
    "fullyQualifiedName": "sample_superset"
  },
  "serviceType": "Superset",
  "deleted": false,
  "followers": [
    {
      "id": "user-uuid-here",
      "type": "user",
      "name": "john.doe"
    }
  ],
  "owners": [],
  "tags": [],
  "domains": []
}

```

--------------------------------

### Get User by FQN

Source: https://docs.open-metadata.org/v1.12.x/api-reference/teams-and-users/users

Retrieves a specific user by their Fully Qualified Name (FQN).

```APIDOC
## GET /v1/users/name/{fqn}

### Description
Get user by FQN.

### Method
GET

### Endpoint
/v1/users/name/{fqn}

### Parameters
#### Path Parameters
- **fqn** (string) - Required - The Fully Qualified Name of the user.
```

--------------------------------

### Create Database using Python SDK

Source: https://docs.open-metadata.org/v1.12.x/api-reference/data-assets/databases/create

Use this snippet to create a new database by providing its name, display name, associated service, description, and retention period. Ensure the SDK is configured with your API host and JWT token.

```python
from metadata.sdk import configure
from metadata.sdk.entities import Databases
from metadata.generated.schema.api.data.createDatabase import CreateDatabaseRequest

configure(
    host="https://your-company.open-metadata.org/api",
    jwt_token="your-jwt-token"
)

request = CreateDatabaseRequest(
    name="analytics",
    displayName="Analytics Database",
    service="snowflake_prod",
    description="Central analytics data warehouse",
    retentionPeriod="P365D"
)

database = Databases.create(request)
print(f"Created: {database.fullyQualifiedName}")

```