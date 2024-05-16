import os
import json
import argparse
import asyncio
from openai import AsyncOpenAI

config = json.load(open('config.json'))
client = AsyncOpenAI(api_key=config["api_key"])

user_prefix = config.get("user_prefix", "A")
ai_prefix = config.get("ai_prefix", "B")

def load_chat_history(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as log_file:
            return json.load(log_file)
    return []

def save_chat_history(file_path, messages):
    with open(file_path, 'w') as log_file:
        json.dump(messages, log_file, indent=4)

def clean_log(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"> {file_path} has been removed.")
    else:
        print(f"> {file_path} does not exist.")

def print_log(file_path, count=50):
    if not os.path.exists(file_path):
        print(f"> no log file found at {file_path}.")
        return
    messages = load_chat_history(file_path)
    total_msgs = len(messages)
    if total_msgs == 0:
        print("> log is empty.")
        return
    if count < 1:
        return
    user_word_count = 0
    ai_word_count = 0
    if count > total_msgs or count == -1:
        count = total_msgs
    for idx, message in enumerate(messages[-count:], start=total_msgs - count + 1):
        role = user_prefix if message["role"] == "user" else ai_prefix
        print(f"{idx}. {role}: {message['content']}")
        
        word_count = len(message['content'].split())
        if message["role"] == "user":
            user_word_count += word_count
        else:
            ai_word_count += word_count
    total_words = user_word_count + ai_word_count
    user_percentage = (user_word_count / total_words) * 100 if total_words else 0
    ai_percentage = (ai_word_count / total_words) * 100 if total_words else 0
    
    print(f"> Stored {total_msgs} messages in total")
    print(f"> Showed for user: {user_word_count} ({user_percentage:.2f}%), for bot: {ai_word_count} ({ai_percentage:.2f}%)")

def update_config(key, value):
    config[key] = value
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)
    print(f"> {key} has been updated to {value} in config.json")

async def chat():
    try:
        log_file_path = 'log.json'
        messages = load_chat_history(log_file_path)
        while True:
            user_input = input(f"{user_prefix}: ")
            messages.append({"role": "user", "content": user_input})

            response_stream = await client.chat.completions.create(
                model=config["model_id"],
                messages=messages,
                stream=True,
            )

            full_reply = ""
            print(f"{ai_prefix}: ", end="", flush=True)
            async for chunk in response_stream:
                chunk_content = chunk.choices[0].delta.content or ""
                full_reply += chunk_content
                print(chunk_content, end="", flush=True)
            print()
            
            messages.append({"role": "assistant", "content": full_reply})
            save_chat_history(log_file_path, messages)

    except Exception as e:
        print(f"> an error occurred: {e}")

async def list_models():
    try:
        models = await client.models.list()
        for model in models.data:
            print(model.id)
    except Exception as e:
        print(f"> an error occurred while listing models: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OpenAI CLI Chat")
    parser.add_argument('--chat', action='store_true', help='Run chat')
    parser.add_argument('--clean', action='store_true', help='Clean log file')
    parser.add_argument('--log', action='store_true', help='Print log file')
    parser.add_argument('-n', type=int, default=50, help='Number of log entries to show')
    parser.add_argument('--api-key', type=str, help='Set API key in config.json')
    parser.add_argument('--model', type=str, help='Set model in config.json')
    parser.add_argument('--models-list', action='store_true', help='List available models')

    args = parser.parse_args()

    if args.chat:
        asyncio.run(chat())
    elif args.clean:
        clean_log('log.json')
    elif args.log:
        print_log('log.json', args.n)
    elif args.api_key:
        update_config('api_key', args.api_key)
    elif args.model:
        update_config('model_id', args.model)
    elif args.models_list:
        asyncio.run(list_models())
