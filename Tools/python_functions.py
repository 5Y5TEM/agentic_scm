
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


def load_config():
    """Loads configuration parameters from settings.yaml in the root directory."""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_file = os.path.join(root_dir, "settings.yaml")
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    return config

# Load the configuration
config = load_config()

# Access the project_id
project_id = config["project_id"]
location = config["location"]
app_id_manuals = config["app_id_manuals"]
app_id_safety_reports = config["app_id_safety_reports"]
gcal_api_key = config["gcal_api_key"]
workshop_gcal_ID = config["workshop_gcal_ID"]
janeDoe_gcal_ID = config["janeDoe_gcal_ID"]
johnSmith_gcal_ID = config["johnSmith_gcal_ID"]


########################################################################################################################
# ANALYZE IMAGE 
########################################################################################################################

def analyze_image(image_path: str):
    """Analyzes an image to detect damage in insulator parts.

    This function uses the Gemini Pro model to analyze an image and determine 
    if the insulator parts within the image are damaged. It expects the model 
    to return a JSON array with image descriptions and damage information.

    Args:
        image_path (str): The path to the image file to be analyzed.

    Returns:
        tuple: A tuple containing the image description and a boolean value 
               indicating whether damage was detected.

    Raises:
        JSONDecodeError: If the model output is not a valid JSON array.
        IndexError: If the JSON array is empty or does not contain the expected fields.
    """
    from vertexai.generative_models import GenerativeModel, Content, Part, GenerationConfig, Image
    import json 

    model = GenerativeModel("gemini-1.5-flash-001")

    # text_part = Part.from_text("Why is sky blue?")
    image_part = Part.from_image(Image.load_from_file(image_path))

    instructions= """
                Tell me if the aircraft parts in the image are broken.
                Respond with a valid JSON array of objects in this format:
                {image_description: "", damaged: ""}. Where 'damaged' is a boolean variable.
                Don't append anything other than the objects in response like "```json" etc.}
                """

    # Now construct the content with the image bytes
    contents = [
        instructions,
        image_part 
    ]

    output = model.generate_content(contents, stream=False).text

    outputjson=json.loads(output)
    first_item = outputjson[0]
    image_description = first_item['image_description']
    damaged = first_item['damaged']
    return image_description, damaged




########################################################################################################################
# SEARCH MANUALS AND REPORTS 
########################################################################################################################

def search_manuals(query):
    """
    Performs a search query to retrieve information for a question on aircraft manuals. 

    Args:
        query: The search query text.

    Returns:
        str: string with filename in which the info was found, the page number, and the answer to the question.
    """
    # Get access token
    access_token = (
        subprocess.check_output("gcloud auth print-access-token", shell=True)
        .decode("utf-8")
        .strip()
    )

    # Construct API URL
    url = f"https://discoveryengine.googleapis.com/v1/projects/{project_id}/locations/global/collections/default_collection/engines/{app_id_manuals}/servingConfigs/default_search:search"

    # Prepare request headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Prepare request body
    request_body = {
        "query": query

    }

    # Make API request
    response = requests.post(url, headers=headers, data=json.dumps(request_body))

    # Check for errors
    response.raise_for_status()

    # Return response
    search_results = response.json()
    title = search_results["results"][0]["document"]["derivedStructData"]["title"]
    pageNumber = search_results["results"][0]["document"]["derivedStructData"]["extractive_answers"][0]["pageNumber"]
    content = search_results["results"][0]["document"]["derivedStructData"]["extractive_answers"][0]["content"]
    return (f"Filename: {title}, pageNumber: {pageNumber}, searchResult: {content}")


def search_safety_reports(query):
    """
    Performs a search query to retrieve information for a question on aircraft annual safety reports. 

    Args:
        query: The search query text.

    Returns:
        str: string with filename in which the info was found, the page number, and the answer to the question.
    """
    # Get access token
    access_token = (
        subprocess.check_output("gcloud auth print-access-token", shell=True)
        .decode("utf-8")
        .strip()
    )

    # Construct API URL
    url = f"https://discoveryengine.googleapis.com/v1/projects/{project_id}/locations/global/collections/default_collection/engines/{app_id_safety_reports}/servingConfigs/default_search:search"

    # Prepare request headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Prepare request body
    request_body = {
        "query": query

    }

    # Make API request
    response = requests.post(url, headers=headers, data=json.dumps(request_body))

    # Check for errors
    response.raise_for_status()

    # Return response
    search_results = response.json()
    title = search_results["results"][0]["document"]["derivedStructData"]["title"]
    pageNumber = search_results["results"][0]["document"]["derivedStructData"]["extractive_answers"][0]["pageNumber"]
    content = search_results["results"][0]["document"]["derivedStructData"]["extractive_answers"][0]["content"]
    return (f"Filename: {title}, pageNumber: {pageNumber}, searchResult: {content}")



########################################################################################################################
# JOE SYSTEMS API 
########################################################################################################################

def joe_systems_determination(csv_file_path):
    """
    Uploads a CSV file to joe.systems and runs the product origin determination.

    Args:
        csv_file_path (str): The path to the CSV file.

    Returns:
        str: The query ID of the uploaded file, or an error message.
    """
    BASE_URL = "https://stage-app.joe.systems"
    auth_response = joe_systems_authorize("", "")
    if "security" in auth_response and "token" in auth_response["security"]:
        token = auth_response["security"]["token"]
        userid = auth_response["id"]
    else:
        return "Error: Could not authenticate with joe.systems API."

    url = f"{BASE_URL}/api/v0.3/Determination/UploadAndRunDetermination?Userid={userid}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        with open(csv_file_path, 'rb') as file:
            files = {'uploadedFile': ('file.csv', file, 'text/csv')}
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.text  # Return the query ID
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    except FileNotFoundError:
        return f"Error: CSV file not found at {csv_file_path}"

def joe_systems_authorize(login, password):
    """
    Authenticates with the joe.systems API and returns an auth token.

    Args:
        login (str): The user's login.
        password (str): The user's password.

    Returns:
        dict: The API response containing the auth token, or an error message.
    """
    BASE_URL = "https://stage-app.joe.systems"
    url = f"{BASE_URL}/api/v0.3/Authorization/External/Authorize?login={login}&password={password}"
    headers = {"accept": "text/plain"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:  
        return f"Error: {e}"
    

# okok= joe_systems_determination('/Users/msubasioglu/Desktop/PhD/Code/ascm_raw/Files/guidebushBOM.csv')
# print(okok)




########################################################################################################################
# GET EMPLOYEES FROM BIGQUERY TABLE  
########################################################################################################################

from google.cloud import bigquery
import pandas as pd

def read_bigquery_table(project_id, dataset_id, table_id):
  """Reads a BigQuery table into a Pandas DataFrame.

  Args:
    project_id: The ID of the Google Cloud project.
    dataset_id: The ID of the BigQuery dataset.
    table_id: The ID of the BigQuery table.

  Returns:
    A Pandas DataFrame containing the data from the BigQuery table.
  """

  client = bigquery.Client(project=project_id)
  table_ref = client.dataset(dataset_id).table(table_id)
  table = client.get_table(table_ref) 

  df = client.list_rows(table).to_dataframe()
  return df


def get_employees(): 
    """Retrieves employee data from BigQuery and returns a DataFrame.

    Fetches employee information, including their specializations and licenses,
    from the 'employees' table in the 'ascm' dataset in BigQuery.

    Args:
        project_id: The ID of the Google Cloud project where the BigQuery dataset
                    is located. This should be provided as an argument to the
                    function or set as an environment variable.

    Returns:
        A Pandas DataFrame containing the employee data, including the following
        columns:
        - Employee ID
        - Employee Name
        - License Held
        - License Expiration Date
        - Contact Number
        - Specialization
    """
    dataset_id = 'ascm'
    table_id = 'employees'
    df = read_bigquery_table(project_id, dataset_id, table_id)

    return df 


########################################################################################################################
# GET CALENDARS 
########################################################################################################################

from googleapiclient.discovery import build
import datetime

def get_upcoming_events(calendar_instance):
    """Retrieves upcoming events from a specified public Google Calendar.

    This function fetches events for the next 30 days from a given public 
    Google Calendar. It uses the Google Calendar API with an API key 
    for access.

    Args:
        calendar_instance: A string identifier for the calendar. Valid options are:
                            - 'workshop'
                            - 'Jane Doe'
                            - 'John Smith'

    Returns:
        A list of event objects from the specified calendar, or a string error 
        message if the provided `calendar_instance` is invalid.
    """

    if calendar_instance == 'workshop':
        calendar_id = workshop_gcal_ID

    elif calendar_instance == 'Jane Doe':
        calendar_id = janeDoe_gcal_ID

    elif calendar_instance == 'John Smith':
        calendar_id = johnSmith_gcal_ID

    else: 
        return "You did not provide a valid calendar instance."
    

    API_KEY = gcal_api_key

    service = build('calendar', 'v3', developerKey=API_KEY)  # No credentials needed

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    time_max = (datetime.datetime.utcnow() + datetime.timedelta(days=30)).isoformat()  + 'Z'

    events_result = service.events().list(
        calendarId=calendar_id, timeMin=now, timeMax=time_max,
        singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items',  [])

    return events

