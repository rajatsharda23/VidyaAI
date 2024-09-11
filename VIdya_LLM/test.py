import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "../secrets/pvtKey.json"

from vertexai.preview.generative_models import GenerativeModel, ChatSession

model = GenerativeModel("gemini-1.0-pro")
chat = model.start_chat()

def get_chat_response(chat: ChatSession, prompt: str):
    response = chat.send_message(prompt)
    return response.text

prompts = [
    "Hi, who are you?",
    "What can you tell me about the United States?",
    "Where was its 44th president born?",
]

for prompt in prompts:
    print("User:", prompt)
    print("Gemini:", get_chat_response(chat, prompt))
    print("------")