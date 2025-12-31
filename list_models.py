import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

for model in genai.list_models():
    print(model)



from google.genai import Client

client = Client(api_key="YOUR_API_KEY_HERE")

models = client.models.list()

print("Available models:")
for m in models:
    print(m.name)