# 🤖 Agentic Supply Chain Maintenance (ASCM)

**ASCM** is an application that leverages Large Language Models (LLMs) and the power of agents to streamline and enhance maintenance and logistics processes within a supply chain context.

![Architecture](Files/architecture.png)

## 📂 Repo Structure
Here's a breakdown of the repository's structure:

|Folder/File|Description|
|:---|:---|
|Agents/|Contains the definitions and implementations of all agents.|
|Files/|This folder stores various files, including images, templates, and other resources, serving as a placeholder for data and assets used by the agents.|
|Tools/|Includes utility scripts, helper functions, and external libraries that support the core functionalities of the agents and the application.|
|TL-2000_StingSport.jpg|An image file for testing purposes.|
|main.py|The primary entry point of the ASCM backend application. Good for testing.|
|settings.yaml|A configuration file storing settings and parameters for the application.|
|streamlit_frontend.py|Implements the user interface of the ASCM application using Streamlit.|
|.gitignore|Specifies files and folders to be excluded from version control.|
|session_handler.py|Provides a chat session manager for interacting with Gemini models.|
|tool_instructions.py|Contains functions to return tool instructions based on available tools.|
|agent_definitions.py|Defines the functionalities and behaviors of different agents.|
|core.py|Implements the core functionalities of the agent interactions.|
|orchestrator.py|Defines an orchestrator agent that manages and calls other agents.|
|python_functions.py|Contains various Python functions used by the agents.|
|__init__.py|Marks directories as Python packages.|
|__init__ copy.py|Implements utility functions for running Python functions and managing tool instructions.|
