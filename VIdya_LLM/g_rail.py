# For running the program without CLI
from dotenv import load_dotenv
import os
import asyncio
from nemoguardrails import LLMRails, RailsConfig
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "../secrets/pvtKey.json"

from vertexai.preview.generative_models import GenerativeModel, ChatSession

model = GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

load_dotenv()

client = model.start_chat()

config = RailsConfig.from_path("./config")
rails = LLMRails(config)
rails = LLMRails(config=config)


# API call to get answer from gpt-3.5
async def get_api_response(prompt: str) -> str | None:
    text: str | None = None

    try:
        response = await rails.generate_async(
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        text = response["content"]
    
        #Troubleshooting
        
        
        print('---------------------------- \n')

        print('(2)\n')
        info = rails.explain()
        info.print_llm_calls_summary()

        print('(3) \n')
        print(info.colang_history)

        if len(info.llm_calls) > 1:
            print('(4) \n')
            print(info.llm_calls[1].completion)
        else:
            print('(4) \n')

            
        print('---------------------------- \n')


    except Exception as e:
        print('ERROR: ', e)
    
    return text 
   
# To append the new prompt to last to retain history
def update_list(message: str, pl: list[str]):
    pl.append(message)
def create_prompt(message: str, pl: list[str]) -> str:
    p_message : str = f'\n{message}'
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt

async def get_bot_response(message: str, pl: list[str]) -> str:
    prompt: str = create_prompt(message,pl)
    bot_response: str = asyncio.create_task(get_api_response(prompt))
    update_bot_response  = await bot_response

    if update_bot_response:
        update_list(update_bot_response,pl)
    
    else:   #Incase of error in API call to gpt
        update_bot_response = 'Something went wrong...'

    return update_bot_response    

async def main():
    prompt_list = ['']  #History of prompts for comtext
    
    while True:
        user_input: str = input('You: ')
        if user_input.lower() == 'mischeif managed':
            break
        response: str = asyncio.create_task(get_bot_response(user_input, prompt_list))
        value = await response
        print(f'Bot:  {value}')

        if user_input.lower() in ['quit', 'exit', 'bye']:
            break

        if response=='Something went wrong...' or response=='I cannot answer such questions, please read the guidlines...':
            break

if __name__ == '__main__':
    asyncio.run(main())