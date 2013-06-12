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


def listFiles(args, settings):
    """
    Main function for the list option.
    """
    wordArgs = fn.parseWordArgs(args)
    home = fn.getBackupHome(settings.backupLocation, settings.hostName)
    backups = fn.getBackupsForArgs(wordArgs, fn.getBackups(home))
    backupWd = fn.removeAltRoot(settings.root, os.getcwd())
    for id_ in backups.keys():
        items = fn.expandGlob(home, backups[id_], backupWd, wordArgs["glob"])
        for item in items:
            _outputItemInfo(id_, fn.getInfo(item))


def _outputItemInfo(index, info):
    """
    Format and output the provided info to the console.
    """
    fmt = "{0:<4} {type} {owner} {group} {size:>10} " + \
          "{modified:%Y-%m-%d %H:%M} {name}"
    print(fmt.format(index, **info))
