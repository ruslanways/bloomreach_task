import base64
import copy
import requests
from pathlib import Path
import os
import ndjson
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud import bigquery
import functions_framework


"""Write a script in python which exports all customers in chunks of MAXIMUM 20
lines per insert from the above mentioned Bloomreach Engagement project to a
GCP bigquery table under dataset <<your first name>>_<<your last
name>>_coding_exercise. For creating infrastructure in GCP, please use terraform.
Use supplied system account credentials when authenticating with GCP APIs in
both cases.
"""

# Use .env file to load environmental variables which contain credentials for bloomreach engagement API.
load_dotenv()

USER = os.environ.get("USER")
PWD = os.environ.get("PWD")
PROJECT_ID = os.environ.get("PROJECT_ID")
DATASET_ID = os.environ.get("DATASET_ID")
TABLE_ID = os.environ.get("TABLE_ID")
CREDENTIALS_GCP_JSON_FILE = Path(__file__).resolve().parent / "credentials_gcp.json"


@functions_framework.http
def taks_1():
    main(USER, PWD, CREDENTIALS_GCP_JSON_FILE, PROJECT_ID, DATASET_ID, TABLE_ID)
    return "The data was successfully sent to BigQuery"


def main(user, pwd, credentials, project, dataset, table):
    """Get data from Bloomreach Engagement api
    and send it to BigQuery.
    """
    data = read_from_bloomreach(user, pwd)
    send_to_bigquery(data, credentials, project, dataset, table)


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
    return response.json()  # Get python dict from response json.


def send_to_bigquery(data, credentials, project, dataset, table):
    """Connect to BigQuery
    and send the data to it.
    """
    # Get authentication credentials for BigQuery connection.
    credentials_gcp = service_account.Credentials.from_service_account_file(
        credentials,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    # Create connection to BigQuery
    client = bigquery.Client(
        credentials=credentials_gcp,
        project=project,
    )

    # Tranform received data to conrofm json for sending to BigQuery.
    def reshape_json_gen(data):
        """
        Created new json with right schema to ingest to BigQuery.
        Make it in form of generator to save memory.
        The generator will returns data by 20 lines per iteration.
        """
        adapted_data = []
        tmp = {}
        for row in data["rows"]:
            for count, entry in enumerate(row):
                tmp[data["header"][count]] = entry
            adapted_data.append(copy.deepcopy(tmp))
            if len(adapted_data) == 20:
                yield adapted_data
                adapted_data.clear()
        yield adapted_data

    # Configuring the loading job with schema and type of data.
    job_config = bigquery.LoadJobConfig(
        schema=[bigquery.SchemaField(header, "STRING") for header in data["header"]],
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )

    # Invoke a job (loading data to DigQuery) by iterations of 20 lines.
    for chunk in reshape_json_gen(data):
        client.load_table_from_json(
            ndjson.loads(ndjson.dumps(chunk)),
            f"{project}.{dataset}.{table}",
            job_config=job_config,
        ).result()
