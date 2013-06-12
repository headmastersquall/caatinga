#!/usr/bin/env python

# Copyright 2013 Chris Taylor
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

import os
import sys
import caatinga.core.functions as fn


def restore(args, settings):
    """
    Main function for the restore option.
    """
    wordArgs = fn.parseWordArgs(args)
    _validateArgs(wordArgs)
    home = fn.getBackupHome(settings.backupLocation, settings.hostName)
    fn.insureBackupHomeExists(home)
    backup = fn.getBackupOrLatest(wordArgs, home)
    cwd = os.getcwd()
    backupWd = fn.removeAltRoot(settings.root, cwd)
    items = fn.expandGlob(home, backup, backupWd, wordArgs["glob"])
    _validateItems(items, wordArgs)
    for item in items:
        _restoreItem(item, cwd, wordArgs["as"])


def _validateArgs(wordArgs):
    """
    Insures that the user cannot restore from 'all' backups.
    """
    if wordArgs["id"] == "all":
        raise Exception("Cannot restore from 'all' backups.")


def _validateItems(items, wordArgs):
    """
    Insures one or more item is provided to be restored and restricts the use
    of the 'as' keyword to only be used if restoring a single item.
    """
    if not items:
        raise Exception("No items found to restore.")
    if len(items) > 1 and wordArgs["as"]:
        raise Exception("Can't restore multiple items when using 'as' alias.")


def _restoreItem(item, cwd, as_):
    """
    Restores the provided item to the current working directory.  If the 'as'
    is not provided, the original file name is preserved.
    """
    if as_:
        restoreAs = os.path.join(cwd, as_)
    else:
        restoreAs = os.path.join(cwd, os.path.basename(item))

    if os.path.exists(restoreAs):
        if _confirmOverwrite(restoreAs):
            fn.copy(item, restoreAs)
    else:
        fn.copy(item, restoreAs)


def _confirmOverwrite(item):
    """
    Prompt the user to confirm a file to be overwritten.
    """
    if os.path.exists(item):
        val = _getInput("Overwrite: {0}? [y/n] ".format(item)).lower()
        return val == "y"


def _getInput(prompt):
    """
    Get the input function to prompt for input according to the Python version.
    This is only here for Python 2 and 3 compatibility.
    """
    if sys.hexversion > 0x03000000:
        return input(prompt)
    else:
        return raw_input(prompt)
