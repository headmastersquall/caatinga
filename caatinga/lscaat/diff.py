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
from os.path import join
from difflib import Differ


def diff(args, settings):
    """
    Main function for the diff option.
    """
    wordArgs = fn.parseWordArgs(args)
    _validateArgs(wordArgs)
    home = fn.getBackupHome(settings.backupLocation, settings.hostName)
    fn.insureBackupHomeExists(home)
    backup = fn.getBackupOrLatest(wordArgs, home)
    cwd = os.getcwd()
    backupWd = fn.removeAltRoot(settings.root, cwd)
    items = fn.expandGlob(home, backup, backupWd, wordArgs["glob"])
    _validateItems(items)
    localFile = _getLines(join(cwd, wordArgs["glob"]))
    backupFile = _getLines(items[0])
    diff = _getDiff()
    sys.stdout.writelines(diff(backupFile, localFile))


def _validateArgs(wordArgs):
    """
    Insure the word args that were provided are valid.
    """
    if wordArgs["id"] == "all":
        raise Exception("Cannot compare items from 'all' backups.")


def _validateItems(items):
    """
    Make sure we have proper items to compare.
    """
    if not items:
        raise Exception("No items found to compare.")
    if len(items) > 1:
        raise Exception("Cannot perform diff on more than one file.")


def _getLines(fileName):
    """
    Read and return all the lines from the provided file.
    """
    with open(fileName, 'U') as f:
        return f.readlines()


def _getDiff():
    """
    Get the program that will be used to perform the diff.
    """
    return Differ().compare
