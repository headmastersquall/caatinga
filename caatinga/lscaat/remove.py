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
from shutil import rmtree


def remove(args, settings):
    """
    Main function for the remove option.
    """
    wordArgs = fn.parseWordArgs(args)
    _validateArgs(wordArgs)
    home = fn.getBackupHome(settings.backupLocation, settings.hostName)
    backups = fn.getBackupsForArgs(wordArgs, fn.getBackups(home))
    backupWd = fn.removeAltRoot(settings.root, os.getcwd())
    for id_ in backups.keys():
        items = fn.expandGlob(home, backups[id_], backupWd, wordArgs["glob"])
        for item in items:
            _delete(item)


def _validateArgs(wordArgs):
    """
    Make sure a backup id exists.
    """
    if not wordArgs["id"]:
        raise Exception("No from backup id provided.")


def _delete(item):
    """
    Delete the provided item.
    """
    if os.path.isdir(item):
        rmtree(item)
    else:
        os.remove(item)
