# Open the text file
with open('static/file1.txt', 'r') as file:
    # Read the contents of the file into a string variable
    text = file.read()

# Import the necessary packages for ChatGPT
import openai
import json

# Set up the OpenAI API key
openai.api_key = 'YOUR_API_KEY'

# Set up the prompt for ChatGPT
prompt = 'YOUR_PROMPT'

# Set up the parameters for the completion API call
parameters = {
    'model': 'text-davinci-002',
    'prompt': prompt,
    'temperature': 0.5,
    'max_tokens': 100,
    'n:': 1,
    'stop': '\n'
}

# Call the completion API and get the response
response = openai.Completion.create(parameters)
result = response.choices[0].text.strip()

# Print the result
print(result)
