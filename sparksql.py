%pyspark
# install the pyspark driver pip3.7
# call with ./spark from the cli if you
USAGE:
      spark [-h] VALUE,...

    EXAMPLES:
      spark 1 5 22 13 53
      ▁▁▃▂█
      spark 0,30,55,80,33,150
      ▁▂▃▄▂█
      echo 9 13 5 17 1 | spark
      ▄▆▂█▁

"""
Example of loading .parquet formatted files into a in-memory SQLContext table and running SQL queries against it.
This script is configured to run a Spark job inside a Jupyter notebook and pull a parquet file from
our Mapr Cluster

"""
import sys

LINE_LENGTH = 200
def print_horizontal():
    """
    Simple method to print horizontal line
    :return: None
    """
    for i in range(LINE_LENGTH):
        sys.stdout.write('-')
    print("")
try:
    from pyspark import SparkContext
    from pyspark import SQLContext

    print ("Successfully imported Spark Modules -- `SparkContext, SQLContext`")
    print_horizontal()
except ImportError as e:
    print ("Can not import Spark Modules", e)
    sys.exit(1)

sqlContext = SQLContext(sparkContext=sc)

# gets parquet file located on cluster
parquetFile = sqlContext.read.parquet("/mapr/maprcluster/data/WELL/114a54dc-a4c6-4ea4-8914-9aa518ad78f9.parquet/")

# Stores the DataFrame into an "in-memory temporary table"
parquetFile.registerTempTable("parquetFile")

# Run standard SQL queries against temporary table
wells_all_all_sql = sqlContext.sql("SELECT * FROM parquetFile")

# Print the result set
wells_all_all = wells_all_all_sql.map(lambda p: "UWI: {0:15} Comment: {1}".format(p.name, p.comment_col))

print("All wells_all and Comments -- `SELECT * FROM parquetFile`")
print_horizontal()
for wells in wells_all_all.collect():
    print(wells)

# Use standard SQL to filter
wells_all_filtered_sql = sqlContext.sql("SELECT name FROM parquetFile WHERE name LIKE '%UWI%'")

# Print the result set
wells_all_filtered = wells_all_filtered_sql.map(lambda p: "UWI: {0:20}".format(p.name))

print_horizontal()
print("wells Filtered -- `SELECT name FROM parquetFile WHERE name LIKE '%UWI%'`")
print_horizontal()
for wells in wells_all_filtered.collect():
    print(wells)
