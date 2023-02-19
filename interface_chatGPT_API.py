import openai_secret_manager

# Let's setup the API key
assert "openai" in openai_secret_manager.get_services()
secrets = openai_secret_manager.get_secrets("openai")

print(secrets)

# Let's install the required package
!pip install openai

# Now, let's generate some text
import openai
openai.api_key = secrets["api_key"]

prompt = (f"Write an article on ChatGPT API")

completions = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)

message = completions.choices[0].text
print(message)
