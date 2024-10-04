
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.cloud import aiplatform
import os
import yaml
import requests
import subprocess
import json
from google.cloud import bigquery

def load_config():
    """Loads configuration parameters from settings.yaml in the root directory."""
    config_file = "settings.yaml"
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    return config

# Load the configuration
config = load_config()

# Access the project_id
project_id = config["project_id"]
location = config["location"]
# app_id_manuals = config["app_id_manuals"]
# app_id_safety_reports = config["app_id_safety_reports"]
# gcal_api_key = config["gcal_api_key"]
# workshop_gcal_ID = config["workshop_gcal_ID"]
# janeDoe_gcal_ID = config["janeDoe_gcal_ID"]
# johnSmith_gcal_ID = config["johnSmith_gcal_ID"]


########################################################################################################################
# Load Employees table into BigQuery 
########################################################################################################################

def csv_to_bigquery():
    """
    Loads data from a CSV file into a BigQuery table.

    Args:
    csv_file_path: The path to the CSV file.
    """

    csv_file_path = 'Files/employees.csv'

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # Set dataset_id to the ID of the dataset to create.
    dataset_id = "ascm"

    # Create the dataset
    dataset = bigquery.Dataset(client.project + "." + dataset_id)
    dataset.location = location # Set the geographic location
    dataset = client.create_dataset(dataset, timeout=30)  
    print("Created dataset {}.{}".format(client.project, dataset.dataset_id)) 

    # Set table_id to the ID of the table to create.
    table_id = "employees"

    # Set the fully-qualified table ID.
    table_ref = dataset.table(table_id)

    job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    autodetect=True,
    )

    with open(csv_file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

    job.result()  # Waits for the job to complete.   

    print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))


csv_to_bigquery()