import asyncio
from openai import AsyncOpenAI
from datetime import datetime
from storage import *

client = AsyncOpenAI(api_key=config["api_key"])

async def chat():
    try:
        log_file_path = 'log.json'
        messages = load_chat_history(log_file_path)
        while True:
            user_input = input(f"{user_prefix}: ")
            timestamp = datetime.now().isoformat()
            messages.append({"role": "user", "content": user_input, "timestamp": timestamp})

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

            timestamp = datetime.now().isoformat()
            messages.append({"role": "assistant", "content": full_reply, "timestamp": timestamp})
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