"""
Example of loading data from a MongoDB collection into an in-memory SQLContext table and running SQL queries against it.
This script uses the MongoDB Spark Connector to pull data from MongoDB.
"""

from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
import sys

# Define constants
LINE_LENGTH = 80

# Function to print horizontal line
def print_horizontal():
    print('-' * LINE_LENGTH)

# Initialize Spark session with MongoDB configuration
try:
    spark = SparkSession.builder \
        .appName("MongoDB Integration") \
        .config("spark.mongodb.input.uri", "mongodb://your_mongodb_uri/database.collection") \
        .config("spark.mongodb.output.uri", "mongodb://your_mongodb_uri/database.collection") \
        .getOrCreate()

    sqlContext = SQLContext(spark)
    print("Successfully connected to MongoDB via Spark")
    print_horizontal()
except Exception as e:
    print(f"Error initializing Spark or MongoDB connection: {e}")
    sys.exit(1)

# Load data from MongoDB into a DataFrame
mongo_df = spark.read.format("mongo").load()

# Register the DataFrame as a temporary SQL table
mongo_df.createOrReplaceTempView("mongoData")

# Run SQL query on the MongoDB data
all_data_sql = sqlContext.sql("SELECT * FROM mongoData")

# Print results of the SQL query
print("All data from MongoDB -- `SELECT * FROM mongoData`")
print_horizontal()
for row in all_data_sql.collect():
    print(f"UWI: {row['name']:15} Comment: {row['comment_col']}")

# Run a filtered SQL query to get specific rows
filtered_data_sql = sqlContext.sql("SELECT name FROM mongoData WHERE name LIKE '%UWI%'")

# Print filtered results
print_horizontal()
print("Filtered Data -- `SELECT name FROM mongoData WHERE name LIKE '%UWI%'`")
print_horizontal()
for row in filtered_data_sql.collect():
    print(f"UWI: {row['name']:20}")
