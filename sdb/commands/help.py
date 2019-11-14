#
# Copyright 2019 Chuck Tuffli
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# pylint: disable=missing-docstring

import argparse
from typing import Iterable

import drgn
import sdb


class Help(sdb.Command):
    # pylint: disable=too-few-public-methods

    "Print command usage"

    names = ["help"]

    @classmethod
    def _init_parser(cls, name: str) -> argparse.ArgumentParser:
        parser = super(Help, cls)._init_parser(name)
        parser.add_argument('cmd', nargs='?')
        return parser

    def call(self, objs: Iterable[drgn.Object]) -> None:
        if self.args.cmd:
            if self.args.cmd in sdb.all_commands:
                cmd_list = [self.args.cmd]
            else:
                print('Unknown command: ' + self.args.cmd)
                return
        else:
            # If command isn't specified, add commands from all_commands
            # to the list. Note that all_commands includes commands and
            # aliases. Filter out the aliases when listing the commands
            cmd_list = []
            aliases = []
            for cmd in sdb.all_commands:
                if cmd in aliases:
                    aliases.remove(cmd)
                else:
                    cmd_list.append(cmd)
                    # Add names to aliases but remove the current one
                    aliases.extend(sdb.all_commands[cmd].names)
                    aliases.remove(cmd)

        for cmd in cmd_list:
            sdb.all_commands[cmd].help(cmd)
