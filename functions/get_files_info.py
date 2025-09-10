import os

def get_files_info(working_directory, directory="."):
    
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, directory))

    if not target_dir.startswith(abs_working_dir):
        return f'Error: "Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    try :
        if directory == ".":
            print(f"Result for current directory:")
        else:
            print(f"Result for '{directory}' directory:")

        files_info = []
        for file in os.listdir(target_dir):
            if not file.startswith("_") and not file.startswith("."):
                file_path = os.path.join(target_dir, file)
                file_size = os.path.getsize(file_path)
                is_dir = os.path.isdir(file_path)
                files_info.append(f" - {file}: file_size={file_size}, is_dir={is_dir}")
        return "\n".join(files_info)
    
    except Exception as e:
        return f"Error: {e}"
    