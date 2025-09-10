import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


if len(sys.argv) > 1:
    prompt = sys.argv[1]
else:
    print("what the hell dude! You didn't give a prompt!")
    exit(1)
# print(sys.argv[2])

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

def main():
    print("Hello from agent!")
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages)

    print(response.text)
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
