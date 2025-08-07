from langchain.tools import Tool
import subprocess
import os

def run_gcloud_command(command: str, credential_path: str, project_id: str) -> str:
    """Runs a gcloud command with the specified credentials and project."""
    try:
        env = os.environ.copy()
        env['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
        env['CLOUDSDK_CORE_PROJECT'] = project_id
        safe_command = sanitize_gcloud_command(command)
        full_command = f"gcloud {safe_command}"
        result = subprocess.check_output(full_command, shell=True, env=env, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.output.decode()}"
    return result.decode("utf-8")

def sanitize_gcloud_command(command: str) -> str:
    return command.replace("'", "").replace('"', '')

# MCP Tool for Gcloud Commands
def mcp_tool_gcloud(credential_path: str, project_id: str) -> Tool:
    """Creates a MCP tool for executing gcloud commands."""
    
    def _tool_function(command: str) -> str:
        return run_gcloud_command(command, credential_path, project_id)
    
    return Tool(
        name="mcp_tool_gcloud",
        func=_tool_function,
        description="A tool to execute gcloud commands with specified credentials and project."
    )