# This file is part of Viper - https://github.com/viper-framework/viper
# See the file 'LICENSE' for copying permission.

import os
import sys
import glob
import atexit
import readline
import traceback
import requests
import json
import argparse

from viper.common.out import print_error
from viper.common.colors import cyan, magenta, white, bold, blue
from viper.core.plugins import __modules__
from viper.core.ui.commands import Commands
from viper.core.database import Database
from viper.core.config import Config
from requests_toolbelt.multipart.encoder import MultipartEncoder


cfg = Config()
post_headers = {'Accept': 'application/json',
                'Content-Type': 'application/json'}

try:
    input = raw_input
except NameError:
    pass

def logo():
    print("""         _
        (_)
   _   _ _ ____  _____  ____
  | | | | |  _ \| ___ |/ ___)
   \ V /| | |_| | ____| |
    \_/ |_|  __/|_____)_| v1.3-dev
          |_|  api console
    """)


def viperCommand(sha256, command):
    # POST method to run a module/command on Viper
    # We're using the sha256 and not the project name
    # for the indicator.

    multipart_data = MultipartEncoder(
    fields={
            'sha256': sha256, 
            'cmdline': command,
           }
    )

    resp = requests.post('http://' + host + ':' + port + '/modules/run', data=multipart_data,
                      headers={'Content-Type': multipart_data.content_type})
    resp.raise_for_status()
    result = resp.json()
    print json.dumps(result['results'], indent=4, sort_keys=True)

class Console(object):

    def __init__(self,):
        # This will keep the main loop active as long as it's set to True.
        self.active = True
        self.cmd = Commands()


    def stop(self):
        # Stop main loop.
        self.active = False

    def start(self, sha256):
        # Logo.
        logo()

        # Setup shell auto-complete.
        def complete(text, state):
            # Try to autocomplete commands.
            cmds = [i for i in self.cmd.commands if i.startswith(text)]
            if state < len(cmds):
                return cmds[state]

            # Try to autocomplete modules.
            mods = [i for i in __modules__ if i.startswith(text)]
            if state < len(mods):
                return mods[state]

            # Then autocomplete paths.
            if text.startswith("~"):
                text = "{0}{1}".format(os.getenv("HOME"), text[1:])
            return (glob.glob(text+'*')+[None])[state]

        # Auto-complete on tabs.
        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind('tab: complete')
        readline.set_completer(complete)

        # Save commands in history file.
        def save_history(path):
            readline.write_history_file(path)

        # If there is an history file, read from it and load the history
        # so that they can be loaded in the shell.
        # Now we are storing the history file in the local project folder
        history_path = os.path.join(os.getenv("HOME"), '.viperHistory')

        if os.path.exists(history_path):
            readline.read_history_file(history_path)

        # Register the save history at program's exit.
        atexit.register(save_history, path=history_path)

        # Main loop.
        while self.active:
            # It's a prompt. There it is.
            prompt = cyan('viper > ', True)

            # Wait for input from the user.
            try:
                data = input(prompt).strip()
            except KeyboardInterrupt:
                print("")
            # Terminate on EOF.
            except EOFError:
                self.stop()
                print("")
                continue
            # Parse the input if the user provided any.
            else:
                # Skip if the input is empty.
                if not data:
                    continue

                # Check for output redirection
                # If there is a > in the string, we assume the user wants to output to file.
                filename = False
                if '>' in data:
                    data, filename = data.split('>')

                # If the input starts with an exclamation mark, we treat the
                # input as a bash command and execute it.
                # At this point the keywords should be replaced.
                if data.startswith('!'):
                    os.system(data[1:])
                    continue

                # !!!!THIS IS THE LAZY COMMAND
                # If the input starts with a period it's an API call
                # so we shell out(this is a client, who gives a fuck) 
                # to curl and jq in this format: viper > .find tag=elf
                # Also the trigger to switch hashes: .use sha256hashhere
                if data.startswith('.'):
                    if data[1:].find('find') != -1:
                        tag = data.split(' ')
                        os.system('curl -F ' + str(tag[1]) + ' http://' + host + ':' + port + '/file/find | jq .')
                    if data[1:].find('use') != -1:
                        sha256 = data.split(' ')[1]
                    continue

                # Try to split commands by ; so that you can sequence multiple
                # commands at once.
                # For example:
                # viper > find name *.pdf; open --last 1; pdf id
                # This will automatically search for all PDF files, open the first entry
                # and run the pdf module against it.
                split_commands = data.split(';')
                for split_command in split_commands:
                    split_command = split_command.strip()
                    if not split_command:
                        continue

                    # Check if the command instructs to terminate.
                    if split_command in ('exit', 'quit'):
                        self.stop()
                        continue

                    try:
                        # call the Viper API POST method for cmdline
                        viperCommand(sha256=sha256, command=split_command)

                    except KeyboardInterrupt:
                        pass
                    except Exception:
                        print_error("The command {0} raised an exception:".format(bold(root)))
                        traceback.print_exc()

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sha256', help='sha256 hash to work on pls', action='store', required=True)
    parser.add_argument('-H', '--host', help='Viper API hostname', default='localhost', action='store', required=False)
    parser.add_argument('-p', '--port', help='Viper API port', default='5556', action='store', required=False)

    global arg
    arg = parser.parse_args()
    host = arg.host
    port = arg.port
    c = Console()
    c.start(sha256=arg.sha256)