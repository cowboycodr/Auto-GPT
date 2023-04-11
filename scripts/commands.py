import json
from memory import get_memory
from config import Config
from json_parser import fix_and_parse_json
from browser import Browser

from file_operations import (
    read_file,
    write_to_file,
    append_to_file,
    delete_file,
    search_files
)

cfg = Config()
browser = Browser()

def is_valid_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def get_command(response):
    """Parse the response and return the command name and arguments"""
    try:
        response_json = fix_and_parse_json(response)

        if "command" not in response_json:
            return "Error:" , "Missing 'command' object in JSON"

        command = response_json["command"]

        if "name" not in command:
            return "Error:", "Missing 'name' field in 'command' object"

        command_name = command["name"]

        # Use an empty dictionary if 'args' field is not present in 'command' object
        arguments = command.get("args", {})

        if not arguments:
            arguments = {}

        return command_name, arguments
    except json.decoder.JSONDecodeError:
        return "Error:", "Invalid JSON"
    # All other errors, return "Error: + error message"
    except Exception as e:
        return "Error:", str(e)


def execute_command(command_name, arguments):
    """Execute the command and return the result"""
    memory = get_memory(cfg)

    try:
        if command_name == "do_nothing":
            pass

        elif command_name == "read_file":
            return read_file(arguments["file"])
        
        elif command_name == "write_to_file":
            return write_to_file(arguments["file"], arguments["text"])
        
        elif command_name == "append_to_file":
            return append_to_file(arguments["file"], arguments["text"])
        
        elif command_name == "delete_file":
            return delete_file(arguments["file"])
        
        elif command_name == "search_files":
            return search_files(arguments["directory"])
        
        elif command_name == "open_url":
            return browser.open(arguments["url"])
        
        elif command_name == "get_url":
            return browser.url
        
        elif command_name == "get_title":
            return browser.title
        
        elif command_name == "get_content":
            return browser.get_content()
        
        elif command_name == "fill_input":
            selector = arguments["selector"]
            text = arguments["text"]

            return browser.fill_input(selector, text)

        elif command_name == "get_interactive":
            return browser.get_interactive_elements()
        
        elif command_name == "click_element":
            return browser.click(arguments["selector"])
        
        elif command_name == "task_complete":
            while True:
                pass

    except Exception as e:
        return "Error: " + str(e)