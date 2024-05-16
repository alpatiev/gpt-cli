# Installation
```
pip install -r requirements.txt
```

# Usage
```
python app.py [command]
```

#### --chat: Runs the chat functionality. This is the primary mode.

--clean: Cleans the log file. This parameter triggers the script to remove the existing log file (`log.json`), effectively clearing any saved chat history. This is useful for starting a fresh session without previous interactions.

--log: Prints the log file. When this parameter is used, the script outputs the content of the log file to the console.

-n: Specifies the number of log entries to show (default is 50). This parameter is used in conjunction with `--log` to control how many entries from the log file are displayed. Setting `-n` to `-1` will show all entries, while any other number will limit the output to that many most recent entries.

--api-key: Sets the API key in `config.json`.

--model: Sets the model in `config.json`.

--models-list: Lists available models. When this parameter is specified, it will display a list of available OpenAI models. 

# Hit ⭐️ button
