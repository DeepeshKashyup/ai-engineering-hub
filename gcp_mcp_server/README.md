# MCP Tool for Gcloud Commands

## Overview
The MCP tool is designed to facilitate the execution of gcloud CLI commands in a programmatic way, enabling users to interact with Google Cloud Platform (GCP) services efficiently. It addresses the need for a streamlined approach to manage GCP resources, run SQL queries on BigQuery datasets, and handle large datasets/results.

## Features
- Execute gcloud CLI commands programmatically.
- Run SQL queries on Google BigQuery datasets.
- Download large datasets/results from BigQuery.
- Containerized environment for easy setup and deployment.
- Chart generation using Matplotlib to visualize data analysis results.
- Supports authentication and configuration management for GCP.
- Supports guarded execution of commands to ensure reliability.

## Tech Stack
- **Python**: The primary programming language for the tool.
- **MCP**: The Multi-Cloud Platform framework for executing gcloud commands.
- **gcloud**: The Google Cloud SDK for interacting with Google Cloud services.
- **BigQuery**: A serverless, highly scalable, and cost-effective multi-cloud data warehouse.
- **Docker**: For containerization and environment setup.

## Framework
- **FastMCP**: A framework for building multi-cloud applications, providing a structured way to manage cloud resources and execute commands.
- **google-cloud-sdk**: The official SDK for Google Cloud, used to interact with GCP services.
- **google-cloud-bigquery**: A client library for accessing BigQuery services.
- **Matplotlib**: A plotting library for creating static, animated, and interactive visualizations in Python.
- **Pandas**: A data manipulation and analysis library for Python.

## folder structure
```
gcp_mcp_server/
├── Dockerfile
├── README.md
├── requirements.txt
├── main.py
├── controller/
│   ├── __init__.py
│   ├── gcp_mcp_controller.py
│   └── utils.py
├── repository/
│   ├── __init__.py
│   ├── gcp_mcp_service.py
│   └── bigquery_service.py
└── models/
    ├── __init__.py
    └── gcp_models.py
```

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd gcp_mcp_server
   ```
2. Build the Docker image:
   ```bash
   docker build -t gcp_mcp_server .
   ```
3. Run the Docker container:
   ```bash
   docker run -it gcp_mcp_server
   ```