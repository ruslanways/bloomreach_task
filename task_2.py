import pandas as pd
import pandas_gbq
from google.oauth2 import service_account
from pathlib import Path


"""Your colleague finds out that the parameter 'number of employees' in the data set
is not up-to-date. The requirement is to increase 'number of employees' by 20% for all
companies in the dataset. Write a script in python which updates 'number of
employees' accordingly, and upserts the data to bigquery only for companies with
non-null number of employees.
"""

# Get authentication credentials for BigQuery connection.
credentials_gcp = service_account.Credentials.from_service_account_file(
   Path(__file__).resolve().parent/"credentials_gcp.json",
)

# Generate a query for the BigQuery table.
sql = """
SELECT *
FROM `wisdom-dev-340814.Ruslan_Mansurov_coding_exercise.bloomreach_task`
"""
# Get data from the BigQuery table.
df = pandas_gbq.read_gbq(sql, project_id="wisdom-dev-340814", credentials=credentials_gcp)

# Filter data from 'employees' column that doesn't contain empty str.
# Then cast filtered dataset(pandas series) to 32 bits integer.
# Then increasing all entries from mentioned data by 20%.
# Here I use floor division 6//5 to avoid remainder. 
# It allows us stay in integer type as that data represents number of people. 
dfs = df.loc[df["employees"] != "", "employees"]
dfs = dfs.astype("int32")
dfs = dfs * 6 // 5

# Update dataset(series) with modified data.
df.loc[df["employees"] != "", "employees"] = dfs

# Cast all columns of DataFrame to string data types for exporting to BigQuery.
df = df.astype(str)

# Send data from DataFrame to BigQuery table by chunks of 20 lines.
df.to_gbq(
    "Ruslan_Mansurov_coding_exercise.bloomreach_task",
    "wisdom-dev-340814",
    if_exists="replace",
    chunksize=20,
    credentials=credentials_gcp,
)