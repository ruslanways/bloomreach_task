import pandas as pd
import pandas_gbq
from google.oauth2 import service_account
from pathlib import Path
import functions_framework


"""Your colleague finds out that the parameter 'number of employees' in the data set
is not up-to-date. The requirement is to increase 'number of employees' by 20% for all
companies in the dataset. Write a script in python which updates 'number of
employees' accordingly, and upserts the data to bigquery only for companies with
non-null number of employees.
"""

CREDENTIALS_GCP_JSON_FILE = "credentials_gcp.json"
PROJECT_ID = "wisdom-dev-340814"
DATASET_ID = "Ruslan_Mansurov_coding_exercise"
TABLE_ID = "bloomreach_task"


@functions_framework.http
def taks_2(request):
    main(CREDENTIALS_GCP_JSON_FILE, PROJECT_ID, DATASET_ID, TABLE_ID)
    return "THe data was successfully updated in BigQuery"

def main(user, pwd, credentials, project, dataset, table):
    """Get data from BigQuery,
    modificate it and send it to BigQuery.
    """
    # Get authentication credentials for BigQuery connection.
    credentials_gcp = service_account.Credentials.from_service_account_file(
        Path(__file__).resolve().parent/credentials,
    )
    df = read_from_bigquery(credentials_gcp, project, dataset, table)
    update_data(df)
    send_to_bigquery(df)

def read_from_bigquery(credentials_gcp, project, dataset, table):
    """Get data from BigQuery
    and transform it to pandas.DataFrame.
    """
    # Generate a query for the BigQuery table.
    sql = f"SELECT * FROM `{project}.{dataset}.{table}`"
    # Get data from the BigQuery table.
    return pandas_gbq.read_gbq(sql, project_id=project, credentials=credentials_gcp)

def update_data(df):
    """Update data within pandas.DataFrame"""
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
    return df

def send_to_bigquery(df, credentials_gcp, project, dataset, table):
    """Connect to BigQuery
    and send the data to it.
    """
    # Cast all columns of DataFrame to string data types for exporting to BigQuery.
    df = df.astype(str)
    # Send data from DataFrame to BigQuery table by chunks of 20 lines.
    df.to_gbq(
        f"{dataset}.{table}",
        f"{project}",
        if_exists="replace",
        chunksize=20,
        credentials=credentials_gcp,
    )
