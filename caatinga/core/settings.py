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

import os
import grp
from os.path import join
from glob import iglob
from sys import argv

__all__ = ["Settings"]

HOST_NAME_INDEX = 1


class Settings:
    """
    Loads settings from the applications conf file and provides properties
    of it's contents.
    """

    def __init__(self):
        self._confFileName = "caatinga.conf"
        self._confPath = [
            ".",
            os.path.dirname(argv[0]),
            "/etc/caatinga",
            "/usr/local/etc/caatinga",
        ]
        self.backupLocation = ""
        self.hostName = os.uname()[HOST_NAME_INDEX]
        self.ignoredDirectories = []
        self.ignoredFiles = []
        self.maxFileSize = 0
        self.maxImages = 0
        self.keepDays = 0
        self.backupgid = os.getgid()
        self.reduceBackups = False
        self.root = ""
        self.preBackupHooksDir = ""
        self.postBackupHooksDir = ""
        self.preRestoreHooksDir = ""
        self.postRestoreHooksDir = ""

    def loadSettings(self, conf=""):
        """
        Loads all settings from the applications conf file.
        """
        try:
            self._loadSettingsFromFile(conf)
        except (IndexError, IOError):
            err = "Unable to locate configuration file (see man caatinga.conf)"
            raise AttributeError(err)

    def _loadSettingsFromFile(self, conf=""):
        with open(self._getConfFile(conf)) as confFile:
            for line in confFile:
                line = line.strip()
                if self._hasContent(line):
                    self._parseAndSet(line)

    def _getConfFile(self, conf=""):
        if os.path.exists(conf):
            return conf
        confFiles = [join(d, f)
                     for d in self._confPath
                     for f in [conf, self._confFileName]]
        return [f for f in confFiles
                if (f.endswith("conf") and os.path.exists(f))][0]

    def _hasContent(self, line):
        return not (line == "" or line[0] == "#")

    def _parseAndSet(self, line):
        try:
            data = line.split("=")
            option = data[0].strip()
            value = data[1].strip()
            self._setOption(option, value)
        except IndexError:
            print("Warning: Incomplete or invalid setting: '{0}'".format(line))

    def _setOption(self, option, value):
        if option == "root":
            self.root = value
        elif option == "hostname":
            self.hostName = value
        elif option == "max_file_size":
            # Convert to bytes
            self.maxFileSize = int(value) * 1024 * 1024
        elif option == "max_images":
            self.maxImages = int(value)
        elif option == "keep_days":
            self.keepDays = int(value)
        elif option == "backup_location":
            self.backupLocation = value
            self.ignoredDirectories.append(value)
        elif option == "ignore":
            self._setIgnoreItem(value)
        elif option == "backup_group":
            self.backupgid = self._extractGroupIdFromGroup(value)
        elif option == "reduce_backups":
            self.reduceBackups = True
        elif option == "pre_backup_hooks":
            self.preBackupHooksDir = value
        elif option == "post_backup_hooks":
            self.postBackupHooksDir = value
        elif option == "pre_restore_hooks":
            self.preRestoreHooksDir = value
        elif option == "post_restore_hooks":
            self.postRestoreHooksDir = value
        else:
            msg = "Warning: Unknown setting in configuration file '{0}'"
            print(msg.format(option))

    def _setIgnoreItem(self, value):
        for item in iglob(value):
            if os.path.isdir(item):
                self.ignoredDirectories.append(item)
            elif os.path.isfile(item):
                self.ignoredFiles.append(item)

    def _extractGroupIdFromGroup(self, group):
        return grp.getgrnam(group).gr_gid
