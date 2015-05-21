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

import argparse
from argparse import RawTextHelpFormatter as formatter

__all__ = ["getArgParser", "getArgs"]
_EPILOG = """Caatinga is a backup and restore suite that uses the
caat and lscaat commands for creating backups and restoring data.
See https://www.github.com/headmastersquall/caatinga for more information."""


def getArgParser():
    _DESCRIPTION = "These options are also available in lscaat."

    parser = argparse.ArgumentParser(description=_DESCRIPTION,
                                     formatter_class=formatter,
                                     epilog=_EPILOG)
    parser.add_argument("-b", "--backup-location",
                        metavar="LOCATION",
                        dest="backupLocation",
                        default="",
                        help="Alternate backup location.")
    parser.add_argument("--clean",
                        action="store_true",
                        help="Manually remove backups marked for deletion.")
    parser.add_argument("-c", "--config",
                        metavar="FILE",
                        default="",
                        help="Specify an alternate configuration file.")
    parser.add_argument("-d", "--delete-oldest",
                        dest="deleteOldest",
                        action="store_true",
                        help="Delete the oldest backup image.")
    parser.add_argument("-g", "--register",
                        action="store_true",
                        help="Register the backup location as backup device.")
    parser.add_argument("-n", "--hostname",
                        default="",
                        dest="hostName",
                        help="Alternate hostname.")
    parser.add_argument("-r", "--root",
                        metavar="PATH",
                        default="",
                        help="Alternate root directory to be backed up.")
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="Verbose mode.  Display backup activity.")
    parser.add_argument("-V", "--version",
                        action="store_true",
                        help="Displays version information and exits.")
    return parser


def getArgs():
    return getArgParser().parse_args()
