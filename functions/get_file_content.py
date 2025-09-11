import os
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory,file_path))
    
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try :
        max_chars = 10000

        with open(target_dir,"r") as f:
            file_content_string = f.read()
            if len(file_content_string) > max_chars:
                file_content_string = file_content_string[:max_chars] + f' [...File "{file_path}"" truncated at 10000 characters]'
            return file_content_string
    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
name="get_file_content",
description="Lists contents of a specified file, subject to a maximum limit of characters.",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="The path of the file whose contents to list, relative to the working directory.",
        ),
    },
),
)