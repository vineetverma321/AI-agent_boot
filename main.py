import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


if len(sys.argv) > 1:
    prompt = sys.argv[1]
else:
    print("what the hell dude! You didn't give a prompt!")
    exit(1)
# print(sys.argv[2])

system_prompt = system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

FUNCTIONS = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

def call_function(function_call_part, verbose=False):

    function_name = function_call_part.name
    args_to_be_passed = dict(function_call_part.args)
    args_to_be_passed["working_directory"] = "./calculator"

    if verbose:
        print(f"Calling function: {function_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_name}")


    if function_name not in FUNCTIONS:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    function_result = FUNCTIONS[function_name](**args_to_be_passed)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )



def main():
    # print("Hello from agent!")
    
    verbose = (len(sys.argv)>=3 and sys.argv[2] == "--verbose")

    try:
        for _ in range (20):
            response = client.models.generate_content(
                model='gemini-2.0-flash-001', contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
               )

            found_call = False

            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)
            
                for part in candidate.content.parts:

                    if part.function_call:
                        # func = response.function_calls[0]
                        found_call = True

                        tool_message = call_function(part.function_call, verbose)
                        # print(f"Calling function: {func.name}({func.args})")

                        # FUNCTION_RESPONSE = function_call_response.parts[0].function_response

                        messages.append(
                                # types.Content(role="user", parts=[types.Part(function_response=FUNCTION_RESPONSE)]),
                                tool_message
                            )

                        # if not FUNCTION_RESPONSE.response:
                        #     raise Exception ("What is going on here?")
                        # elif verbose:
                        #     print(f"-> {FUNCTION_RESPONSE.response}")
                    
                if not found_call and response.text:
                    print(response.text)
                    break
                    
    except Exception as e:
        return "Something has gone wrong with the content generation"

    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")



if __name__ == "__main__":
    main()
