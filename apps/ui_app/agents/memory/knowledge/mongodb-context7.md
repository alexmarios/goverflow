# MongoDB Documentation Repository

MongoDB's official documentation monorepo is a comprehensive collection of technical documentation, code examples, and reference materials for the entire MongoDB ecosystem. It covers MongoDB Atlas (cloud database service), self-managed MongoDB deployments, official drivers for 15+ programming languages, CLI tools, integrations with AI platforms, and specialized products like MongoDB Vector Search, Atlas Stream Processing, and the MCP Server for AI assistants. The repository uses Snooty, MongoDB's custom documentation toolchain built on reStructuredText, to generate and publish documentation across multiple versioned products.

The repository structure organizes documentation by product under the `/content/` directory, with each product having its own versioned subdirectories (e.g., `current/`, `upcoming/`, `v1.x/`). Code examples are maintained in `/code-example-tests/` with automated testing to ensure accuracy, while the `/platform/` directory contains the Next.js-based documentation platform infrastructure. This architecture enables MongoDB to maintain consistent documentation across dozens of products while supporting multiple simultaneous versions for enterprise customers.

## MongoDB Shell (mongosh) - Database Operations

The MongoDB Shell provides an interactive JavaScript interface to MongoDB. It supports all CRUD operations, aggregation pipelines, administrative commands, and database management tasks with auto-completion and syntax highlighting.

```javascript
// Connect to MongoDB and perform basic operations
const { MongoClient } = require("mongodb");

const uri = "mongodb+srv://user:password@cluster.mongodb.net/";
const client = new MongoClient(uri);

async function run() {
  try {
    const database = client.db('sample_mflix');
    const movies = database.collection('movies');

    // Insert a single document
    const insertResult = await movies.insertOne({
      title: "The Matrix",
      year: 1999,
      genres: ["Action", "Sci-Fi"],
      directors: ["Lana Wachowski", "Lilly Wachowski"]
    });
    console.log(`Inserted document with _id: ${insertResult.insertedId}`);

    // Query for a document
    const query = { title: 'Back to the Future' };
    const movie = await movies.findOne(query);
    console.log(movie);

    // Update with upsert
    const updateResult = await movies.updateOne(
      { title: 'New Movie' },
      { $set: { title: 'New Movie', year: 2024, genres: ['Drama'] } },
      { upsert: true }
    );
    console.log(`Modified ${updateResult.modifiedCount} document(s)`);

    // Aggregation pipeline
    const pipeline = [
      { $match: { directors: { $exists: true, $ne: null } } },
      { $unwind: "$directors" },
      { $group: { _id: "$directors", movieCount: { $sum: 1 } } },
      { $sort: { movieCount: -1 } },
      { $limit: 3 }
    ];
    const aggCursor = movies.aggregate(pipeline);
    for await (const doc of aggCursor) {
      console.log(doc);
    }
    // Output: { _id: 'Woody Allen', movieCount: 40 }
    //         { _id: 'John Ford', movieCount: 27 }
    //         { _id: 'Martin Scorsese', movieCount: 26 }

  } finally {
    await client.close();
  }
}
run().catch(console.dir);
```

## PyMongo - Python Driver

PyMongo is the official synchronous Python driver for MongoDB, providing a Pythonic interface to interact with MongoDB databases. It supports connection pooling, authentication mechanisms, GridFS for large files, and full aggregation framework capabilities.

```python
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, ConnectionFailure

# Connection with authentication and options
uri = "mongodb+srv://user:password@cluster.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

try:
    # Verify connection
    client.admin.command('ping')
    print("Connected to MongoDB!")

    db = client["sample_mflix"]
    movies = db["movies"]

    # Insert documents
    new_movie = {
        "title": "Inception",
        "year": 2010,
        "director": "Christopher Nolan",
        "genres": ["Action", "Sci-Fi", "Thriller"],
        "imdb": {"rating": 8.8, "votes": 2000000},
        "created_at": datetime.utcnow()
    }
    result = movies.insert_one(new_movie)
    print(f"Inserted with _id: {result.inserted_id}")

    # Find with projection and sorting
    cursor = movies.find(
        {"year": {"$gte": 2000}},
        {"title": 1, "year": 1, "imdb.rating": 1, "_id": 0}
    ).sort("imdb.rating", -1).limit(5)

    for doc in cursor:
        print(doc)
    # Output: {'title': 'The Dark Knight', 'year': 2008, 'imdb': {'rating': 9.0}}

    # Aggregation pipeline for analytics
    pipeline = [
        {"$match": {"year": {"$gte": 2000}}},
        {"$unwind": "$genres"},
        {"$group": {
            "_id": "$genres",
            "count": {"$sum": 1},
            "avg_rating": {"$avg": "$imdb.rating"}
        }},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]

    results = list(movies.aggregate(pipeline))
    for r in results:
        print(f"{r['_id']}: {r['count']} movies, avg rating: {r['avg_rating']:.2f}")

except ConnectionFailure as e:
    print(f"Connection failed: {e}")
finally:
    client.close()
```

## Atlas CLI - Command Line Interface

The Atlas CLI provides command-line access to manage MongoDB Atlas clusters, projects, organizations, database users, and network access. It supports automation workflows, CI/CD integration, and local development environments.

```bash
# Installation
brew install mongodb-atlas

# Authentication and profile setup
atlas auth login
atlas config init

# Create a free-tier cluster
atlas clusters create myCluster \
  --provider AWS \
  --region US_EAST_1 \
  --tier M0 \
  --projectId 60d5f1234567890abcdef123

# List clusters with JSON output
atlas clusters list --output json
# Output:
# {
#   "results": [
#     {
#       "name": "myCluster",
#       "stateName": "IDLE",
#       "mongoDBVersion": "7.0.12",
#       "providerSettings": {
#         "providerName": "TENANT",
#         "regionName": "US_EAST_1"
#       }
#     }
#   ]
# }

# Create database user with SCRAM authentication
atlas dbusers create atlasAdmin \
  --username myAppUser \
  --password 'SecureP@ssw0rd!' \
  --role readWriteAnyDatabase \
  --projectId 60d5f1234567890abcdef123

# Configure IP access list
atlas accessLists create 0.0.0.0/0 \
  --comment "Allow all IPs (dev only)" \
  --projectId 60d5f1234567890abcdef123

# Get connection string
atlas clusters connectionStrings describe myCluster
# Output: mongodb+srv://myCluster.abcd1.mongodb.net

# Run local Atlas deployment for development
atlas local deployments start
atlas local deployments logs myLocalCluster

# Create a search index
atlas clusters search indexes create \
  --clusterName myCluster \
  --file search-index.json
```

## MongoDB MCP Server - AI Integration

The MongoDB MCP Server enables AI assistants (Cursor, Windsurf, VS Code Copilot) to interact with MongoDB databases using natural language. It provides tools for Atlas management, local deployments, CRUD operations, and vector search capabilities.

```json
// MCP Server Configuration (mcp.json)
{
  "mcpServers": {
    "mongodb": {
      "command": "npx",
      "args": ["mongodb-mcp-server@latest"],
      "env": {
        "MDB_MCP_CONNECTION_STRING": "mongodb+srv://user:pass@cluster.mongodb.net/",
        "MDB_MCP_ATLAS_CLIENT_ID": "mdb_sa_id_64abc...",
        "MDB_MCP_ATLAS_CLIENT_SECRET": "mdb_sa_sk_...",
        "MDB_MCP_READ_ONLY": "false",
        "MDB_MCP_VOYAGE_API_KEY": "pa-..."
      }
    }
  }
}
```

```bash
# Setup MCP Server interactively
npx mongodb-mcp-server@latest setup

# Available MCP Tools and natural language prompts:

# Atlas Management Tools:
# - "List all my Atlas projects"          -> atlas-list-projects
# - "Create a free cluster in AWS"        -> atlas-create-free-cluster
# - "Show me alerts for my project"       -> atlas-list-alerts
# - "Get performance recommendations"     -> atlas-get-performance-advisor

# Database Tools:
# - "Connect to my production database"   -> connect
# - "Find all users older than 30"        -> find
# - "Run an aggregation on orders"        -> aggregate
# - "Insert these documents..."           -> insert-many
# - "Create an index on email field"      -> create-index

# Vector Search Tools:
# - "Create a vector search index on the products collection"
# - "Search for documents similar to 'machine learning concepts'"
# - "Insert documents and generate embeddings for descriptions"

# Example prompts with expected responses:
# Prompt: "Show me the top 5 most expensive products"
# Tool called: find
# Query: { sort: { price: -1 }, limit: 5 }

# Prompt: "Create a vector search index on plot_embedding field"
# Tool called: create-index
# Index definition: {
#   "name": "vector_index",
#   "type": "vectorSearch",
#   "definition": {
#     "fields": [{
#       "type": "vector",
#       "path": "plot_embedding",
#       "numDimensions": 1536,
#       "similarity": "cosine"
#     }]
#   }
# }
```

## MongoDB Vector Search

MongoDB Vector Search enables semantic search on vector embeddings stored in Atlas. It supports approximate nearest neighbor (ANN) search using HNSW algorithm, pre-filtering, and hybrid search combining vector and full-text queries.

```javascript
// Create a vector search index via Atlas UI, CLI, or driver
// Index definition (search-index.json):
{
  "name": "vector_index",
  "type": "vectorSearch",
  "definition": {
    "fields": [
      {
        "type": "vector",
        "path": "plot_embedding",
        "numDimensions": 1536,
        "similarity": "cosine"
      },
      {
        "type": "filter",
        "path": "genres"
      },
      {
        "type": "filter",
        "path": "year"
      }
    ]
  }
}
```

```python
from pymongo import MongoClient
import openai

client = MongoClient("mongodb+srv://user:pass@cluster.mongodb.net/")
db = client["sample_mflix"]
movies = db["embedded_movies"]

# Generate embedding for search query
def get_embedding(text):
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# Vector search with pre-filtering
query_text = "A movie about time travel and adventure"
query_embedding = get_embedding(query_text)

pipeline = [
    {
        "$vectorSearch": {
            "index": "vector_index",
            "path": "plot_embedding",
            "queryVector": query_embedding,
            "numCandidates": 150,
            "limit": 10,
            "filter": {
                "year": {"$gte": 1990},
                "genres": "Sci-Fi"
            }
        }
    },
    {
        "$project": {
            "title": 1,
            "year": 1,
            "plot": 1,
            "genres": 1,
            "score": {"$meta": "vectorSearchScore"}
        }
    }
]

results = list(movies.aggregate(pipeline))
for movie in results:
    print(f"{movie['title']} ({movie['year']}) - Score: {movie['score']:.4f}")
    print(f"  Plot: {movie['plot'][:100]}...")
# Output:
# Back to the Future (1985) - Score: 0.9234
#   Plot: Marty McFly, a 17-year-old high school student, is accidentally sent 30 years into the past...
# The Terminator (1984) - Score: 0.8876
#   Plot: A cyborg assassin is sent back in time from 2029 to 1984 to kill Sarah Connor...

# Hybrid search combining vector and full-text search
hybrid_pipeline = [
    {
        "$vectorSearch": {
            "index": "vector_index",
            "path": "plot_embedding",
            "queryVector": query_embedding,
            "numCandidates": 100,
            "limit": 20
        }
    },
    {
        "$match": {
            "$text": {"$search": "adventure hero"}
        }
    },
    {"$limit": 5},
    {
        "$project": {
            "title": 1,
            "vectorScore": {"$meta": "vectorSearchScore"},
            "textScore": {"$meta": "textScore"}
        }
    }
]
```

## Aggregation Framework

The MongoDB Aggregation Framework provides powerful data processing capabilities through a pipeline of stages. It supports transformations, grouping, lookups (joins), window functions, and specialized operations for time series and geospatial data.

```javascript
// mongosh - Complex aggregation pipeline
db.orders.aggregate([
  // Stage 1: Filter recent orders
  {
    $match: {
      orderDate: { $gte: ISODate("2024-01-01") },
      status: "completed"
    }
  },

  // Stage 2: Lookup customer details
  {
    $lookup: {
      from: "customers",
      localField: "customerId",
      foreignField: "_id",
      as: "customer"
    }
  },
  { $unwind: "$customer" },

  // Stage 3: Unwind line items
  { $unwind: "$items" },

  // Stage 4: Lookup product details
  {
    $lookup: {
      from: "products",
      localField: "items.productId",
      foreignField: "_id",
      as: "product"
    }
  },
  { $unwind: "$product" },

  // Stage 5: Group by customer and product category
  {
    $group: {
      _id: {
        customerId: "$customerId",
        customerName: "$customer.name",
        category: "$product.category"
      },
      totalSpent: { $sum: { $multiply: ["$items.quantity", "$items.price"] } },
      orderCount: { $sum: 1 },
      avgOrderValue: { $avg: { $multiply: ["$items.quantity", "$items.price"] } }
    }
  },

  // Stage 6: Reshape output
  {
    $project: {
      _id: 0,
      customer: "$_id.customerName",
      category: "$_id.category",
      totalSpent: { $round: ["$totalSpent", 2] },
      orderCount: 1,
      avgOrderValue: { $round: ["$avgOrderValue", 2] }
    }
  },

  // Stage 7: Sort by spending
  { $sort: { totalSpent: -1 } },

  // Stage 8: Limit results
  { $limit: 10 }
])

// Output:
// { customer: "John Smith", category: "Electronics", totalSpent: 4599.99, orderCount: 3, avgOrderValue: 1533.33 }
// { customer: "Jane Doe", category: "Books", totalSpent: 289.50, orderCount: 12, avgOrderValue: 24.13 }
```

## Atlas Administration API

The Atlas Administration API provides RESTful endpoints for programmatically managing MongoDB Atlas resources including clusters, database users, network access, alerts, and backups.

```bash
# Get API keys from Atlas UI: Organization Settings > API Keys
# Base URL: https://cloud.mongodb.com/api/atlas/v2

# List all projects in organization
curl -s --user "${PUBLIC_KEY}:${PRIVATE_KEY}" \
  --digest \
  --header "Accept: application/vnd.atlas.2024-08-05+json" \
  "https://cloud.mongodb.com/api/atlas/v2/groups" | jq '.results[] | {id, name}'

# Output:
# {"id": "60d5f1234567890abcdef123", "name": "Production"}
# {"id": "60d5f1234567890abcdef456", "name": "Development"}

# Create a new cluster
curl -s --user "${PUBLIC_KEY}:${PRIVATE_KEY}" \
  --digest \
  --header "Content-Type: application/json" \
  --header "Accept: application/vnd.atlas.2024-08-05+json" \
  --request POST \
  "https://cloud.mongodb.com/api/atlas/v2/groups/${PROJECT_ID}/clusters" \
  --data '{
    "name": "production-cluster",
    "clusterType": "REPLICASET",
    "replicationSpecs": [{
      "regionConfigs": [{
        "providerName": "AWS",
        "regionName": "US_EAST_1",
        "priority": 7,
        "electableSpecs": {
          "instanceSize": "M30",
          "nodeCount": 3
        }
      }]
    }],
    "backupEnabled": true,
    "mongoDBMajorVersion": "7.0"
  }'

# Create database user with SCRAM authentication
curl -s --user "${PUBLIC_KEY}:${PRIVATE_KEY}" \
  --digest \
  --header "Content-Type: application/json" \
  --request POST \
  "https://cloud.mongodb.com/api/atlas/v2/groups/${PROJECT_ID}/databaseUsers" \
  --data '{
    "databaseName": "admin",
    "roles": [{"roleName": "readWrite", "databaseName": "myapp"}],
    "username": "app_user",
    "password": "SecureP@ss123!"
  }'

# Configure IP access list
curl -s --user "${PUBLIC_KEY}:${PRIVATE_KEY}" \
  --digest \
  --header "Content-Type: application/json" \
  --request POST \
  "https://cloud.mongodb.com/api/atlas/v2/groups/${PROJECT_ID}/accessList" \
  --data '[{"ipAddress": "192.168.1.100", "comment": "Office IP"}]'

# Get cluster metrics
curl -s --user "${PUBLIC_KEY}:${PRIVATE_KEY}" \
  --digest \
  "https://cloud.mongodb.com/api/atlas/v2/groups/${PROJECT_ID}/processes/${HOSTNAME}:27017/measurements?granularity=PT1H&period=P1D&m=CONNECTIONS"
```

## Schema Validation

MongoDB supports JSON Schema validation to enforce document structure, data types, and business rules at the database level. Validation can be configured on collection creation or modified afterward.

```javascript
// Create collection with schema validation
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "name", "role", "createdAt"],
      properties: {
        email: {
          bsonType: "string",
          pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
          description: "Must be a valid email address"
        },
        name: {
          bsonType: "object",
          required: ["first", "last"],
          properties: {
            first: { bsonType: "string", minLength: 1, maxLength: 50 },
            last: { bsonType: "string", minLength: 1, maxLength: 50 }
          }
        },
        role: {
          enum: ["admin", "user", "guest"],
          description: "Role must be admin, user, or guest"
        },
        age: {
          bsonType: "int",
          minimum: 0,
          maximum: 150,
          description: "Age must be between 0 and 150"
        },
        address: {
          bsonType: "object",
          properties: {
            street: { bsonType: "string" },
            city: { bsonType: "string" },
            zip: { bsonType: "string", pattern: "^[0-9]{5}(-[0-9]{4})?$" }
          }
        },
        tags: {
          bsonType: "array",
          items: { bsonType: "string" },
          maxItems: 10
        },
        createdAt: { bsonType: "date" }
      },
      additionalProperties: false
    }
  },
  validationLevel: "strict",
  validationAction: "error"
})

// Valid insert
db.users.insertOne({
  email: "john@example.com",
  name: { first: "John", last: "Doe" },
  role: "user",
  age: NumberInt(30),
  createdAt: new Date()
})

// Invalid insert - throws MongoServerError
db.users.insertOne({
  email: "invalid-email",  // Fails pattern validation
  name: { first: "Jane" }, // Missing required "last"
  role: "superadmin"       // Not in enum
})
// Error: Document failed validation
```

## Change Streams

Change Streams allow applications to subscribe to real-time data changes in MongoDB collections, databases, or entire deployments. They provide an event-driven architecture for building reactive applications.

```python
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import threading

client = MongoClient("mongodb+srv://user:pass@cluster.mongodb.net/")
db = client["myapp"]
orders = db["orders"]

def watch_orders():
    """Watch for changes in the orders collection"""
    pipeline = [
        {
            "$match": {
                "operationType": {"$in": ["insert", "update", "replace"]},
                "fullDocument.status": "pending"
            }
        },
        {
            "$project": {
                "operationType": 1,
                "documentKey": 1,
                "fullDocument.orderId": 1,
                "fullDocument.customerId": 1,
                "fullDocument.total": 1,
                "fullDocument.status": 1,
                "updateDescription": 1
            }
        }
    ]

    try:
        with orders.watch(
            pipeline,
            full_document="updateLookup",
            full_document_before_change="whenAvailable"
        ) as stream:
            print("Watching for order changes...")
            for change in stream:
                print(f"Change detected: {change['operationType']}")
                print(f"  Order ID: {change['fullDocument'].get('orderId')}")
                print(f"  Status: {change['fullDocument'].get('status')}")
                print(f"  Total: ${change['fullDocument'].get('total', 0):.2f}")

                if change['operationType'] == 'update':
                    updated = change.get('updateDescription', {}).get('updatedFields', {})
                    print(f"  Updated fields: {list(updated.keys())}")
                print("-" * 40)

    except PyMongoError as e:
        print(f"Change stream error: {e}")

# Start watching in background thread
watcher = threading.Thread(target=watch_orders, daemon=True)
watcher.start()

# Trigger changes (in another part of your application)
orders.insert_one({
    "orderId": "ORD-001",
    "customerId": "CUST-123",
    "items": [{"product": "Widget", "qty": 2, "price": 29.99}],
    "total": 59.98,
    "status": "pending"
})

# Output:
# Watching for order changes...
# Change detected: insert
#   Order ID: ORD-001
#   Status: pending
#   Total: $59.98
# ----------------------------------------

# Resume token for fault tolerance
resume_token = None
with orders.watch() as stream:
    for change in stream:
        resume_token = stream.resume_token
        # Process change...
        break

# Resume from last position after reconnection
with orders.watch(resume_after=resume_token) as stream:
    for change in stream:
        print("Resumed:", change)
```

## Indexes and Query Optimization

MongoDB indexes improve query performance by reducing the number of documents scanned. The database supports various index types including single-field, compound, multikey, text, geospatial, and wildcard indexes.

```javascript
// Create various index types
const db = client.db('myapp');
const products = db.collection('products');

// Single-field index
await products.createIndex({ sku: 1 }, { unique: true });

// Compound index (supports queries on name, or name+category)
await products.createIndex({ name: 1, category: 1, price: -1 });

// Text index for full-text search
await products.createIndex(
  { name: "text", description: "text" },
  { weights: { name: 10, description: 5 }, default_language: "english" }
);

// Geospatial 2dsphere index
await products.createIndex({ location: "2dsphere" });

// TTL index for automatic document expiration
await products.createIndex(
  { createdAt: 1 },
  { expireAfterSeconds: 86400 } // 24 hours
);

// Partial index (only index documents matching filter)
await products.createIndex(
  { price: 1 },
  { partialFilterExpression: { status: "active", price: { $gt: 0 } } }
);

// Wildcard index for dynamic schemas
await products.createIndex({ "attributes.$**": 1 });

// Analyze query performance with explain
const explanation = await products.find({
  category: "Electronics",
  price: { $lt: 500 }
}).explain("executionStats");

console.log("Index used:", explanation.queryPlanner.winningPlan.inputStage.indexName);
console.log("Documents examined:", explanation.executionStats.totalDocsExamined);
console.log("Keys examined:", explanation.executionStats.totalKeysExamined);
console.log("Execution time:", explanation.executionStats.executionTimeMillis, "ms");

// Output:
// Index used: name_1_category_1_price_-1
// Documents examined: 42
// Keys examined: 42
// Execution time: 2 ms

// Get index statistics
const stats = await products.aggregate([
  { $indexStats: {} }
]).toArray();
stats.forEach(idx => {
  console.log(`${idx.name}: ${idx.accesses.ops} operations since ${idx.accesses.since}`);
});
```

## Transactions

MongoDB multi-document transactions provide ACID guarantees across multiple documents and collections. They support read concern, write concern, and causal consistency configurations.

```python
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

client = MongoClient("mongodb+srv://user:pass@cluster.mongodb.net/")

def transfer_funds(from_account: str, to_account: str, amount: float):
    """Transfer funds between accounts with transaction guarantees"""

    with client.start_session() as session:
        try:
            # Start transaction with write concern majority
            with session.start_transaction(
                read_concern=pymongo.ReadConcern("snapshot"),
                write_concern=pymongo.WriteConcern("majority"),
                read_preference=pymongo.ReadPreference.PRIMARY
            ):
                accounts = client.bank.accounts
                transactions = client.bank.transactions

                # Verify source account has sufficient funds
                source = accounts.find_one(
                    {"account_id": from_account},
                    session=session
                )
                if not source or source["balance"] < amount:
                    raise ValueError("Insufficient funds")

                # Debit source account
                accounts.update_one(
                    {"account_id": from_account},
                    {"$inc": {"balance": -amount}},
                    session=session
                )

                # Credit destination account
                accounts.update_one(
                    {"account_id": to_account},
                    {"$inc": {"balance": amount}},
                    session=session
                )

                # Record transaction
                transactions.insert_one({
                    "from": from_account,
                    "to": to_account,
                    "amount": amount,
                    "timestamp": datetime.utcnow(),
                    "status": "completed"
                }, session=session)

                # Transaction commits automatically when exiting the with block
                print(f"Transferred ${amount} from {from_account} to {to_account}")
                return True

        except (ConnectionFailure, OperationFailure) as e:
            # Transaction aborts automatically on exception
            print(f"Transaction failed: {e}")
            return False

# Usage with retry logic
from pymongo.errors import PyMongoError

def transfer_with_retry(from_acc, to_acc, amount, max_retries=3):
    for attempt in range(max_retries):
        try:
            return transfer_funds(from_acc, to_acc, amount)
        except PyMongoError as e:
            if attempt < max_retries - 1:
                print(f"Retry {attempt + 1}/{max_retries}")
                continue
            raise

# Execute transfer
transfer_with_retry("ACC-001", "ACC-002", 500.00)
# Output: Transferred $500.0 from ACC-001 to ACC-002
```

## Time Series Collections

MongoDB Time Series collections are optimized for storing and querying time-stamped data like IoT sensor readings, financial data, and application metrics with automatic bucketing and compression.

```python
from pymongo import MongoClient
from datetime import datetime, timedelta
import random

client = MongoClient("mongodb+srv://user:pass@cluster.mongodb.net/")
db = client["iot_data"]

# Create time series collection
db.create_collection(
    "sensor_readings",
    timeseries={
        "timeField": "timestamp",
        "metaField": "sensor",
        "granularity": "seconds"
    },
    expireAfterSeconds=2592000  # 30 days TTL
)

sensors = db["sensor_readings"]

# Insert time series data
readings = []
base_time = datetime.utcnow()

for i in range(1000):
    readings.append({
        "timestamp": base_time + timedelta(seconds=i),
        "sensor": {
            "id": f"SENSOR-{i % 10:03d}",
            "location": random.choice(["Building-A", "Building-B"]),
            "type": "temperature"
        },
        "value": round(20 + random.uniform(-5, 5), 2),
        "unit": "celsius"
    })

result = sensors.insert_many(readings)
print(f"Inserted {len(result.inserted_ids)} readings")

# Query with time range
recent = list(sensors.find({
    "timestamp": {
        "$gte": base_time,
        "$lt": base_time + timedelta(minutes=5)
    },
    "sensor.location": "Building-A"
}).sort("timestamp", 1).limit(10))

# Aggregation for time-based analytics
pipeline = [
    {
        "$match": {
            "timestamp": {"$gte": base_time - timedelta(hours=1)}
        }
    },
    {
        "$group": {
            "_id": {
                "sensor": "$sensor.id",
                "hour": {"$dateToString": {
                    "format": "%Y-%m-%d %H:00",
                    "date": "$timestamp"
                }}
            },
            "avgValue": {"$avg": "$value"},
            "minValue": {"$min": "$value"},
            "maxValue": {"$max": "$value"},
            "readings": {"$sum": 1}
        }
    },
    {"$sort": {"_id.hour": -1, "avgValue": -1}},
    {"$limit": 10}
]

stats = list(sensors.aggregate(pipeline))
for s in stats:
    print(f"Sensor {s['_id']['sensor']} @ {s['_id']['hour']}: "
          f"avg={s['avgValue']:.2f}, min={s['minValue']:.2f}, "
          f"max={s['maxValue']:.2f}, count={s['readings']}")

# Output:
# Sensor SENSOR-003 @ 2024-01-15 14:00: avg=21.34, min=15.23, max=24.89, count=360
# Sensor SENSOR-007 @ 2024-01-15 14:00: avg=20.98, min=16.12, max=24.56, count=360
```

## Summary

The MongoDB documentation repository serves as the authoritative source for developers building applications with MongoDB across cloud (Atlas) and self-managed deployments. The core use cases span from simple CRUD operations with official drivers (Node.js, Python, Java, C#, Go, Ruby, Rust, PHP, and more) to advanced features like vector search for AI applications, change streams for real-time data processing, time series analytics for IoT workloads, and multi-document transactions for financial applications. The repository's tested code examples ensure accuracy while the MCP Server integration brings MongoDB capabilities directly into AI-assisted development workflows.

Integration patterns documented in this repository support modern application architectures including microservices with event-driven communication via change streams, serverless functions with Atlas triggers, AI/ML pipelines using vector embeddings and RAG architectures, and hybrid deployments combining cloud Atlas clusters with local development environments. The documentation emphasizes security best practices including network access controls, authentication mechanisms (SCRAM, X.509, LDAP, OIDC), field-level encryption, and comprehensive audit logging. Developers can leverage the Atlas CLI and Administration API for infrastructure-as-code workflows, enabling GitOps practices and CI/CD integration for database provisioning and management.
