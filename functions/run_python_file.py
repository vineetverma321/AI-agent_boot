import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory,file_path))
    
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    
    try:
        commands = ["python", abs_file_path]

        if args:
            commands.extend(args)

        result = subprocess.run(commands, capture_output=True, cwd=abs_working_dir, timeout=30, text=True)

        # if not result.stdout and not result.stderr :
        #     return f"No output produced."
        # if result.returncode != 0:
        #     return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}\nProcess exited with code {result.returncode}"
        # else:
        #     return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"

        output = []
        if result.stdout:
            output.append(f"STDOUT: \n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR: \n{result.stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced."

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
name="run_python_file",
description="Run a python file at a specified file path, using a set of arguments (if provided).",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="The path of the file which needs to be run, relative to the working directory."),
        "args": types.Schema(
            type=types.Type.STRING,
            description="The optional list of arguments which need to be provided while running the python file."
        ),
    },
    required=["file_path"],
),
)