import argparse
import asyncio
from network import chat, list_models
from storage import *

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
        