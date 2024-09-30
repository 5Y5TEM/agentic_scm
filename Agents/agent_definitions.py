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


from Agents import  Agent


def get_InspectorAgent(model):
    """
    "This inspector agent analyzes images of aircraft parts to classify whether the part displayed is broken or not. 
    For this, the agent expects an image_path in string format."
    """ 

    response_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "understanding": {
                    "type": "string",
                },
                "chain_of_thought": {
                    "type": "string",
                },
                "response": {
                    "type": "string",
                },
                "function": {
                    "type": "string",
                },
                "function_name": {
                    "type": "string",
                },
                "function_args": {
                    "type": "string",
                },
                "execute_function": {
                    "type": "string",
                    "enum": [
                        "True",
                        "False"
                    ],
                }, 
                "aircraft_model": {
                    "type": "string"
                }
            },
            "required": ["understanding", "chain_of_thought", "response", "function", "function_name", "function_args"],
        },
    }




    PERSONA = "Inspector Agent"


    INSTRUCTIONS = """
                    You are an inspector agent that analyzes images of aircraft parts to determine whether they are broken or not. 
                    Use the tools at your disposal to run the analysis for an incoming image_path string.
                    Populate the "aircraft_model" field in your response with the Aircraft Model mentioned in the image filename. 
                    Mention the aircraft model in your overall response.  
                """


    tools = """def analyze_image(image_path: str):
                    \"\"\"Analyzes an image to detect damage in insulator parts.

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
                    \"\"\"
    """



    # Create an instance of the Agent class
    agent = Agent(model, response_schema, PERSONA, INSTRUCTIONS, tools)

    return agent 


def get_DocumentAgent(model):
    """
    "This document agent queries different document bases to answer an incoming question."
    """ 

    response_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "understanding": {
                    "type": "string",
                },
                "chain_of_thought": {
                    "type": "string",
                },
                "response": {
                    "type": "string",
                },
                "function": {
                    "type": "string",
                },
                "function_name": {
                    "type": "string",
                },
                "function_args": {
                    "type": "string",
                },
                "execute_function": {
                    "type": "string",
                    "enum": [
                        "True",
                        "False"
                    ],
                }, 
            },
            "required": ["understanding", "chain_of_thought", "response", "function", "function_name", "function_args"],
        },
    }




    PERSONA = "Document Agent"


    INSTRUCTIONS = """
                    You are a document agent that answers user questions and retrieves requested information.
                    Avoid just returning the document and page number. If possible, summarize the contents returned to you back to the user.
                """


    tools = """def search_manuals(query):
                \"\"\"
                Performs a search query to retrieve information for a question on aircraft manuals. 

                Args:
                    query: The search query text.

                Returns:
                    str: string with filename in which the info was found, the page number, and the answer to the question.
                \"\"\"
            def search_safety_reports(query):
                \"\"\"
                Performs a search query to retrieve information for a question on aircraft annual safety reports. 

                Args:
                    query: The search query text.

                Returns:
                    str: string with filename in which the info was found, the page number, and the answer to the question.
                \"\"\"
    """



    # Create an instance of the Agent class
    agent = Agent(model, response_schema, PERSONA, INSTRUCTIONS, tools)

    return agent 



def get_ScheduleAgent(model):
    """
    This Schedule Agent can retrieve employees and their licences, as well as employee and workshop availability. 
    """ 

    response_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "understanding": {
                    "type": "string",
                },
                "chain_of_thought": {
                    "type": "string",
                },
                "response": {
                    "type": "string",
                },
                "function": {
                    "type": "string",
                },
                "function_name": {
                    "type": "string",
                },
                "function_args": {
                    "type": "string",
                },
                "execute_function": {
                    "type": "string",
                    "enum": [
                        "True",
                        "False"
                    ],
                }, 
            },
            "required": ["understanding", "chain_of_thought", "response", "function", "function_name", "function_args"],
        },
    }




    PERSONA = "Scheduler Agent"


    INSTRUCTIONS = """
                    You are a scheduler agent. Your task is to find licensed employees by their names that can support with structural repairs, engine maintenance, or annual inspection, depending on what is asked by the user. 
                    - do not refer to the employees by their ID. instead, use their names.
                    - execute the tools one after the other, until you can provide all the necessary information at once. 
                    - Once you know the availability of the employee and the workshop, provide the next 3 slots where both the employee and the workshop are free.  

                    Use the tools available to you to: 
                    1. Find the 'Employee Name' with the proper license to do the task the user asked for. If there are multiple employees that meet the requirement, provide their names to the user and let them know you are proceeding with one of them (select at random).
                    2. Retrieve the availability of this employee by using their name.  
                    3. Retrieve the availability of the workshop. 
                """


    tools = """def get_employees(): 
                    \"\"\"Retrieves employee data from BigQuery and returns a DataFrame.

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
                    \"\"\"
                def get_upcoming_events(calendar_instance):
                    \"\"\"Retrieves upcoming events from a specified public Google Calendar.

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
                    \"\"\"
    """



    # Create an instance of the Agent class
    agent = Agent(model, response_schema, PERSONA, INSTRUCTIONS, tools)

    return agent 