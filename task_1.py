import base64
import requests
import pandas as pd
from google.oauth2 import service_account
from pathlib import Path
import functions_framework
import os
from dotenv import load_dotenv


"""Write a script in python which exports all customers in chunks of MAXIMUM 20
lines per insert from the above mentioned Bloomreach Engagement project to a
GCP bigquery table under dataset <<your first name>>_<<your last
name>>_coding_exercise. For creating infrastructure in GCP, please use terraform.
Use supplied system account credentials when authenticating with GCP APIs in
both cases.
"""

# Use .env file to load environmental variables which contain credentials for bloomreach engagement API.
load_dotenv()

USER = os.environ.get('USER')
PWD = os.environ.get('PWD')
PROJECT_ID = os.environ.get('PROJECT_ID')
DATASET_ID = os.environ.get('DATASET_ID')
TABLE_ID = os.environ.get('TABLE_ID')
CREDENTIALS_GCP_JSON_FILE = str(Path(__file__).resolve().parent / "credentials_gcp.json")


@functions_framework.http
def taks_1(request):
    main(USER, PWD, CREDENTIALS_GCP_JSON_FILE, PROJECT_ID, DATASET_ID, TABLE_ID)
    return "THe data was successfully sent to BigQuery"


def main(user, pwd, credentials, project, dataset, table):
    """Get data from Bloomreach Engagement api
    and send it to BigQuery.
    """
    df = read_from_bloomreach(user, pwd)
    send_to_bigquery(df, credentials, project, dataset, table)


def read_from_bloomreach(user, pwd):
    """Make a HTTP-request to get the data
    and transform it to Pandas.DataFrame.
    """
    # Get a base64 encoded string needs as credential token to Bloomreach Engagement.
    credentials = f"{user}:{pwd}"
    credentials_bytes = credentials.encode()
    credentials_base64 = base64.b64encode(credentials_bytes)
    credentials_base64_str = credentials_base64.decode()

    url = "https://api.exponea.com/data/v2/projects/962d1b9a-481b-11ea-9329-6a9665f4e6e6/customers/export"
    payload = {"format": "table_json"}
    headers = {
        "accept": "application/json",
        "authorization": f"Basic {credentials_base64_str}",
    }
    response = requests.post(url, json=payload, headers=headers)
    response_dict = response.json()  # Get python dict from response json.

    # Create pandas DataFrame from the dict.
    return pd.DataFrame(data=response_dict["rows"], columns=response_dict["header"])


def send_to_bigquery(df, credentials, project, dataset, table):
    """Connect to BigQuery
    and send the data to it.
    """
    # Cast all columns of DataFrame to string data types for exporting to BigQuery.
    df = df.astype(str)
    # Get authentication credentials for BigQuery connection.
    credentials_gcp = service_account.Credentials.from_service_account_file(
        credentials,
    )
    # Send data from DataFrame to BigQuery table by chunks of 20 lines.
    df.to_gbq(
        f"{dataset}.{table}",
        f"{project}",
        if_exists="replace",
        chunksize=20,
        credentials=credentials_gcp,
    )


# # # # #
# Sending data to BigQuery in chunks method 2.
#
# step = 20
# start = 0
# stop = step

# while True:
#    chunk_df = df[start:stop]
#    if chunk_df.empty:
#       break
#    df.to_gbq('dataset1.table1', 'refined-analogy-371811', if_exists='replace')
#    start += step
#    stop += step
