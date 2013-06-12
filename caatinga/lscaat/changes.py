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
import caatinga.core.functions as fn
from os.path import join, basename


def changes(args, settings):
    """
    Main function for the changes option.
    """
    wordArgs = fn.parseWordArgs(args)
    _validateArgs(wordArgs)
    home = fn.getBackupHome(settings.backupLocation, settings.hostName)
    fn.insureBackupHomeExists(home)
    backup = fn.getBackupOrLatest(wordArgs, home)
    cwd = os.getcwd()
    backupWd = fn.removeAltRoot(settings.root, cwd)
    backedUpFiles = fn.expandGlob(home, backup, backupWd, "*")
    backupDir = join(home, backup) + backupWd
    allFiles = set(os.listdir(cwd)).union(map(basename, backedUpFiles))

    for item in allFiles:
        status = _getStatus(join(cwd, item), join(backupDir, item))
        if status:
            _outputItem(item, status)


def _validateArgs(wordArgs):
    """
    Insure the word args that were provided are valid.
    """
    if wordArgs["id"] == "all":
        raise Exception("Cannot show changes from 'all' backups.")


def _getStatus(localFile, backedUpFile):
    """
    Return the status of the item provided compared to the version that is
    found in the backup.  Status can be "New", "Deleted" or "Modified".
    """
    if os.path.exists(localFile) and os.path.exists(backedUpFile) is False:
        return "New"
    elif os.path.exists(localFile) is False and os.path.exists(backedUpFile):
        return "Deleted"
    elif fn.isModified(localFile, backedUpFile):
        return "Modified"
    else:
        return None


def _outputItem(item, status):
    """
    Output the formatted information to the console.
    """
    print("{0:<9} {1}".format(status, item))
