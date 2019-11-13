#
# Copyright 2019 Delphix
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
"""This module contains the "sdb.Command" class."""

import argparse
import inspect
from typing import Iterable, List, Optional

import drgn
import sdb


class Command:
    """
    This is the superclass of all SDB command classes.

    This class intends to be the superclass of all other SDB command
    classes, and is responsible for implementing all the logic that is
    required to integrate the command with the SDB REPL.
    """

    # pylint: disable=too-few-public-methods

    #
    # names:
    #    The potential names that can be used to invoke
    #    the command.
    #
    names: List[str] = []

    input_type: Optional[str] = None

    def __init__(self, prog: drgn.Program, args: str = "",
                 name: str = "_") -> None:
        self.prog = prog
        self.name = name
        self.islast = False
        self.ispipeable = False

        if inspect.signature(
                self.call).return_annotation == Iterable[drgn.Object]:
            self.ispipeable = True

        self.parser = argparse.ArgumentParser(prog=name)
        docstr = inspect.getdoc(type(self))
        self.parser.description = docstr.splitlines()[0].strip()
        self._init_argparse(self.parser)
        self.args = self.parser.parse_args(args.split())

    def __init_subclass__(cls, **kwargs):
        """
        This method will automatically register the subclass command,
        such that the command will be automatically integrated with the
        SDB REPL.
        """
        super().__init_subclass__(**kwargs)
        for name in cls.names:
            sdb.register_command(name, cls)

    def _init_argparse(self, parser: argparse.ArgumentParser) -> None:
        pass

    def call(self,
             objs: Iterable[drgn.Object]) -> Optional[Iterable[drgn.Object]]:
        # pylint: disable=missing-docstring
        raise NotImplementedError

    @classmethod
    def help(cls, name: str, verbose: bool = False, obj = None):
        """
        Print a help message for the command based on the documentation
        string for the class. This assumes the documentation uses the form:
        <one line description of command>
        <optional, and possibly multi-line description of command>
        :type name: bool
        """
        docstr = inspect.getdoc(cls)
        summary = docstr.splitlines()[0]
        description = docstr.splitlines()[1:]

        if not verbose:
            print("{} - {}".format(name, summary))
        else:
            print("SUMMARY")
            for line in obj.parser.format_help().split('\n')[:-1]:
                print("    {}".format(line.replace('usage: ', '')))

            if len(cls.names) > 1:
                print("\nALIASES")
                print("    {}".format(", ".join(cls.names)))

            if description:
                #
                # The first line of the description should be a blank line,
                # so we skip it, unless it's (unconventionally) not blank.
                #
                if not description[0]:
                    print("{}".format(description[0]))

                for line in description[1:]:
                    print("{}".format(line))
