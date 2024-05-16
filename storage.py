import os
import json

config = json.load(open('config.json'))
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
        timestamp = message.get("timestamp", "no timestamp")
        print(f"> {idx}. {role} [{timestamp}]")
        print(f"  {message['content']}")
        
        word_count = len(message['content'].split())
        if message["role"] == "user":
            user_word_count += word_count
        else:
            ai_word_count += word_count
    
    total_words = user_word_count + ai_word_count
    user_percentage = (user_word_count / total_words) * 100 if total_words else 0
    ai_percentage = (ai_word_count / total_words) * 100 if total_words else 0
    
    print(f"> Stored {total_msgs} messages in total")
    print(f"> Words by user: {user_word_count} ({user_percentage:.2f}%), for bot: {ai_word_count} ({ai_percentage:.2f}%)")

def update_config(key, value):
    config[key] = value
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)
    print(f"> {key} has been updated to {value} in config.json")