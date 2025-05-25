# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "54e08e8d-32ad-4604-ac3f-ffee6e20a81a",
# META       "default_lakehouse_name": "ActionBILakehouse",
# META       "default_lakehouse_workspace_id": "b668781b-f684-461d-a429-aec6fb6608cd",
# META       "known_lakehouses": [
# META         {
# META           "id": "54e08e8d-32ad-4604-ac3f-ffee6e20a81a"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!
# Welcome to your new notebook
# Type here in the cell editor to add code!
# phython module that lets you connect to the operating sytem for file operations etc
import os
from pyspark.sql import functions as F

# Incremental tables
csv_files = ["Customer.csv", "Sales.csv"]

# Schema name
schema_name = "raw"

# Create schema if it doesn't exist
#is spark iported implicity? yes!
#spark.sql runs the sql command in the spark context
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")

# Loop through each CSV files (4 in this case)
for csv_file in csv_files:
    # Get the table name from the file name
    #asking for zeroth index of the list, which is the first element, [1] would be, in this case ".csv"
    table_name = os.path.splitext(csv_file)[0]

    # Read the source table
    # option("header","true") means the first row of the csv file is the header
    # load(f"Files/raw/{csv_file}") means the file is in the Files/raw directory
    df = spark.read.format("csv").option("header","true").load(f"Files/Files/{csv_file}")

    # remove column name invalid chars
    # in sql you can't have spaces in the column names
    # so we are replacing spaces with empty strings
    # list expression is used to iterate over the columns of the dataframe
    #read from right to left
    #F.col says to take the column name from the dataframe
    #alias says to rename the column
    #replace is a string method that replaces the first argument with the second argument
    #so we are replacing the spaces with empty strings
    #df.columns is a list of the columns in the dataframe
    #reassign df which esenatial means we have all the same datea but the column names are changed
    df = df.select([F.col(col).alias(col.replace(' ', '')) for col in df.columns])
    # Write to the target schema, replacing the existing table
    # format("delta") means we are using the delta format, which is a format that allows for incremental updates
    # f stands for format string, which is a way to format strings in python
    # saveAsTable means we are saving the dataframe as a table in the database

    df.write.mode("overwrite").option("overwriteSchema", "true").format("delta").saveAsTable(f"{schema_name}.{table_name}")    
    #so at the end of this phython script we have 4 tables in the raw sql schema, stored in the lakehouse we created, within the workspace we created.
    # note this is a spark table, not a sql table
    # the tables are customer, sales, product and store


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

schema_name_post_ETL = "PostETL"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schema_name_post_ETL}")
df = spark.sql(f"""
            SELECT *, 
                CASE WHEN Quantity =1 THEN 0 
                    ELSE Quantity
                END AS AdjustedQuantity
            FROM {schema_name}.sales""")
df.write.mode("overwrite").option("overwriteSchema", "true").format("delta").saveAsTable(f"{schema_name_post_ETL}.sales")  

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
