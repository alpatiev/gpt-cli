# Installation
```
pip install -r requirements.txt
```

# Usage
```
python app.py [command]
```

#### --chat: Runs the chat functionality. When this parameter is specified, the script will initiate a chat session where the user can interact with the OpenAI model in real-time. This is the primary mode of operation for the script, allowing dynamic conversation.

--clean: Cleans the log file. This parameter triggers the script to remove the existing log file (`log.json`), effectively clearing any saved chat history. This is useful for starting a fresh session without previous interactions.

--log: Prints the log file. When this parameter is used, the script outputs the content of the log file to the console. It allows the user to review past conversations. 

-n: Specifies the number of log entries to show (default is 50). This parameter is used in conjunction with `--log` to control how many entries from the log file are displayed. Setting `-n` to `-1` will show all entries, while any other number will limit the output to that many most recent entries.

--api-key: Sets the API key in `config.json`. This parameter allows the user to update the OpenAI API key in the configuration file. It is useful for changing the key without directly modifying the file.

--model: Sets the model in `config.json`. This parameter allows the user to update the model ID in the configuration file. It is used to switch between different OpenAI models that the user might want to interact with.

--models-list: Lists available models. When this parameter is specified, the script will fetch and display a list of available OpenAI models. This helps users see which models they can choose from for their interactions.

# Hit ⭐️ button