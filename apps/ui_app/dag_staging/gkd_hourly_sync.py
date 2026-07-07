"""
GKD Hourly Sync DAG - Extract GDELT Global Knowledge Graph (GKG) data from PostgreSQL and sync to MongoDB.
Runs hourly to extract data from the previous hour window.
Creates MongoDB database and collection with proper GKG schema if they don't exist.
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
import psycopg2
import json
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure


# GDELT Global Knowledge Graph (GKG) schema definition
GKG_SCHEMA = {
    "GKGRECORDID": str,           # Unique record identifier
    "DATE": str,                  # Timestamp in format YYYYMMDDHHMMSS
    "SourceCollectionIdentifier": int,  # Source collection ID
    "SourceCommonName": str,      # Common source name
    "DocumentIdentifier": str,    # Document URL/identifier
    "Counts": str,                # Semicolon-separated count information
    "V2Counts": str,              # V2 count information
    "Themes": str,                # Semicolon-separated themes
    "V2Themes": str,              # V2 themes
    "Locations": str,             # Semicolon-separated locations
    "V2Locations": str,           # V2 locations
    "Persons": str,               # Semicolon-separated persons
    "V2Persons": str,             # V2 persons
    "Organizations": str,         # Semicolon-separated organizations
    "V2Organizations": str,       # V2 organizations
    "V2Tone": str,                # V2 tone scores
    "Dates": str,                 # Semicolon-separated dates
    "GCAM": str,                  # GCAM codes
    "SharingImage": str,          # Primary sharing image URL
    "RelatedImages": str,         # Semicolon-separated related images
    "SocialImageEmbeds": str,     # Social image embeds
    "SocialVideoEmbeds": str,     # Social video embeds
    "Quotations": str,            # Semicolon-separated quotations
    "AllNames": str,              # All names mentioned
    "Amounts": str,               # Semicolon-separated amounts
    "TranslationInfo": str,       # Translation information
    "Extras": str,                # Extra metadata
}


def get_previous_hour_window(data_interval_start):
    """
    Calculate the previous hour window based on data_interval_start.
    Handles both datetime objects and ISO format strings.
    """
    # Ensure data_interval_start is a datetime object
    if isinstance(data_interval_start, str):
        # Handle both 'T' and space separators
        dt_str = data_interval_start.replace('Z', '+00:00')
        formats_to_try = [
            '%Y-%m-%dT%H:%M:%S.%f%z',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%dT%H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d %H:%M:%S.%f',
            '%Y-%m-%d %H:%M:%S',
        ]
        parsed_dt = None
        for fmt in formats_to_try:
            try:
                parsed_dt = datetime.strptime(dt_str, fmt)
                break
            except ValueError:
                continue
        if parsed_dt is None:
            raise ValueError(f"Unable to parse datetime string '{data_interval_start}'")
        data_interval_start = parsed_dt
    
    # Remove timezone info for naive datetime operations if needed
    if data_interval_start.tzinfo is not None:
        data_interval_start = data_interval_start.replace(tzinfo=None)
    
    current_hour_start = data_interval_start.replace(minute=0, second=0, microsecond=0)
    prev_hour_start = current_hour_start - timedelta(hours=1)
    
    return prev_hour_start, current_hour_start


@task
def extract_from_postgres(context):
    """Extract GDELT GKG data from PostgreSQL for the previous hour window."""
    data_interval_start = context.get('data_interval_start', context.get('execution_date'))
    prev_hour_start, current_hour_start = get_previous_hour_window(data_interval_start)
    
    print(f"Extracting data from {prev_hour_start} to {current_hour_start}")
    
    # Database connection parameters (use Airflow Connections in production)
    conn_params = {
        'host': 'localhost',
        'database': 'gkd_db',
        'user': 'airflow',
        'password': 'airflow',
        'port': 5432
    }
    
    # Query for GDELT GKG data - adjust table/column names as needed
    query = """
    SELECT * FROM gkg_events
    WHERE event_time >= %s AND event_time < %s
    ORDER BY event_time
    """
    
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        cursor.execute(query, (prev_hour_start, current_hour_start))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
        
        print(f"Fetched {len(rows)} rows from PostgreSQL")
        print(f"Columns: {columns}")
        
        # Convert to list of dicts
        result = [dict(zip(columns, row)) for row in rows]
        
        # Serialize datetime objects to ISO format
        for record in result:
            for key, value in record.items():
                if isinstance(value, datetime):
                    record[key] = value.isoformat()
        
        return json.dumps(result)
    
    except psycopg2.Error as e:
        print(f"PostgreSQL error: {e}")
        raise


@task
def process_data(data_json):
    """Process and validate the extracted GKG data."""
    data = json.loads(data_json)
    print(f"Processing {len(data)} GKG records")
    
    # Validate and transform data to match GKG schema
    processed_records = []
    for record in data:
        processed_record = {}
        for field, field_type in GKG_SCHEMA.items():
            # Map from PostgreSQL column names to GKG field names
            # Adjust mapping based on your actual PostgreSQL schema
            value = record.get(field, record.get(field.lower(), ''))
            if value is None:
                value = ''
            # Ensure type compatibility
            if field_type == int:
                try:
                    value = int(value) if value else 0
                except (ValueError, TypeError):
                    value = 0
            else:
                value = str(value)
            processed_record[field] = value
        processed_records.append(processed_record)
    
    print(f"Processed {len(processed_records)} records with GKG schema")
    return json.dumps(processed_records)


@task
def load_to_mongodb(data_json, context):
    """Load processed GKG data to MongoDB, creating database and collection if needed."""
    data = json.loads(data_json)
    
    # MongoDB connection parameters (use Airflow Connections in production)
    mongo_uri = "mongodb://localhost:27017/"
    db_name = "gdelt_gkg"
    collection_name = "gkg_events"
    
    print(f"Connecting to MongoDB: {mongo_uri}")
    print(f"Database: {db_name}, Collection: {collection_name}")
    
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ping')
        print("MongoDB connection successful")
        
        # Get database (creates if not exists)
        db = client[db_name]
        print(f"Database '{db_name}' ready (created if not exists)")
        
        # Get collection (creates if not exists)
        collection = db[collection_name]
        print(f"Collection '{collection_name}' ready (created if not exists)")
        
        # Create indexes for better query performance
        print("Creating indexes...")
        collection.create_index([("GKGRECORDID", 1)], unique=True, name="idx_gkgrecordid")
        collection.create_index([("DATE", 1)], name="idx_date")
        collection.create_index([("SourceCommonName", 1)], name="idx_source")
        collection.create_index([("V2Themes", 1)], name="idx_themes")
        print("Indexes created successfully")
        
        # Get collection info
        stats = db.command("collstats", collection_name)
        print(f"Collection stats before insert: {stats.get('count', 0)} documents")
        
        # Insert documents (skip duplicates based on GKGRECORDID)
        if data:
            inserted_count = 0
            for record in data:
                try:
                    collection.replace_one(
                        {"GKGRECORDID": record.get("GKGRECORDID", "")},
                        record,
                        upsert=True
                    )
                    inserted_count += 1
                except Exception as e:
                    print(f"Error inserting record: {e}")
                    continue
            
            print(f"Inserted/Updated {inserted_count} documents in MongoDB")
            
            # Verify insertion
            final_count = collection.count_documents({})
            print(f"Collection stats after insert: {final_count} documents")
        else:
            print("No data to insert")
        
        client.close()
        print("MongoDB connection closed")
        
        return {"status": "success", "inserted": len(data), "total_in_collection": final_count if data else 0}
    
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        raise
    except OperationFailure as e:
        print(f"MongoDB operation failed: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error loading to MongoDB: {e}")
        raise


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


with DAG(
    dag_id='gkd_hourly_sync',
    default_args=default_args,
    schedule='@hourly',
    catchup=False,
    tags=['gkd', 'gdelt', 'gkg', 'hourly', 'postgres', 'mongodb'],
) as dag:
    
    extract = extract_from_postgres()
    process = process_data(extract)
    load = load_to_mongodb(process)
    
    extract >> process >> load
