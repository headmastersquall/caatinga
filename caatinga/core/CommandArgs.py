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

__all__ = ["CommandArgs"]


class CommandArgs:
    def __init__(self, args):
        self.backupLocation = ""
        self.config = ""
        self.clean = False
        self.deleteOldest = False
        self.register = False
        self.help = False
        self.hostName = ""
        self.root = ""
        self.verbose = False
        self.version = False

        for i in range(len(args)):
            option = args[i]
            value = ""
            if option.startswith("--"):
                self._setLongOption(option)
            elif option.startswith("-"):
                if i + 1 < len(args):
                    value = args[i + 1]
                self._setOption(option, value)

    def _setLongOption(self, longOption):
        if longOption.count("=") == 1:
            items = longOption.split("=")
            self._setOption(items[0], items[1])
        else:
            self._setOption(longOption, "")

    def _setOption(self, option, value):
        if option in ("-b", "--backup-location"):
            self._requireValue(option, value)
            self.backupLocation = value
        elif option == "--clean":
            self.clean = True
        elif option in ("-c", "--config"):
            self._requireValue(option, value)
            self.config = value
        elif option in ("-d", "--delete-oldest"):
            self.deleteOldest = True
        elif option in ("-g", "--register-backup"):
            self.register = True
        elif option in ("-h", "--help"):
            self.help = True
        elif option in ("-n", "--hostname"):
            self._requireValue(option, value)
            self.hostName = value
        elif option in ("-r", "--root"):
            self._requireValue(option, value)
            self.root = value
        elif option in ("-v", "--verbose"):
            self.verbose = True
        elif option in ("-V", "--version"):
            self.version = True
        else:
            raise Exception("Unknown option: {0}".format(option))

    def _requireValue(self, option, value):
        if not value:
            raise Exception(
                "Option '{0}' requires a value parameter.".format(option))
