#!/usr/bin/env python

# Copyright 2015 Chris Taylor
#
# This file is part of caatinga.
#
# Caatinga is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Caatinga is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with caatinga.  If not, see <http://www.gnu.org/licenses/>.

import caatinga.caat_main as caat
import caatinga.core.functions as fn
from caatinga.core.args import getArgParser
from caatinga.core.validation import SettingsValidator
from caatinga.lscaat.changes import changes
from caatinga.lscaat.diff import diff
from caatinga.lscaat.help import help_
from caatinga.lscaat.info import info
from caatinga.lscaat.listFiles import listFiles
from caatinga.lscaat.remove import remove
from caatinga.lscaat.restore import restore


def main():
    """
    Application entry point.
    """
    try:
        run_lscaat()
        exit(0)
    except IndexError:
        usage()
        exit(1)
    except KeyboardInterrupt:
        exit(1)
    except Exception as ex:
        print(str(ex).strip("'"))
        exit(1)


def run_lscaat():
    """
    Main method for lscaat.
    """
    (commandArgs, args) = getArgParser().parse_known_args()
    if commandArgs.version:
        print("lscaat version: " + caat.__version__)
        exit(0)
    settings = fn.getSettingsInstance(commandArgs)
    SettingsValidator().validate(settings)
    runOption(args, settings)


def usage():
    """
    Display the usage text.
    """
    print("Type 'lscaat help' for usage.")


def runOption(args, settings):
    """
    Execute the option provided by the user.
    """
    options = {
        "list": listFiles,
        "ls": listFiles,
        "remove": remove,
        "rm": remove,
        "restore": restore,
        "info": info,
        "changes": changes,
        "diff": diff,
        "help": help_,
    }
    m = options.get(args[0].lower())
    if m and m.__name__ != "help_":
        runWithHooks(m, args[1:], settings)
    elif m:
        m(args[1:], settings)
    else:
        unknownCommand(args)


def runWithHooks(optionFn, args, settings):
    """
    Wrap the provided option call with the pre and post restore hooks.
    """
    fn.runHooks(settings.preRestoreHooksDir)
    optionFn(args, settings)
    fn.runHooks(settings.postRestoreHooksDir)


def unknownCommand(args):
    """
    Display the unknown command text.
    """
    print("Unknown command: '{0}'".format(args[1]))
    usage()

if __name__ == '__main__':
    main()
