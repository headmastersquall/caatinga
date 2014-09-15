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

__all__ = ["SettingsValidator"]


class SettingsValidator:
    """
    Validates the contents of the applications settings file.
    """

    def validate(self, settings):
        """
        Validates the contents of the applications settings file.  An Exception
        will be raised if any problem is found.
        """
        self._hasBackupLocation(settings.backupLocation)
        self._doesBackupLocationExist(settings.backupLocation)
        self._isBackupLocationMounted(settings.backupLocation)
        self._isBackupLocationRegistered(settings.backupLocation)
        self._doesRootDirectoryExist(settings.root)
        self._doesPreHooksDirectoryExits(settings.preHooksDir)
        self._doesPostHooksDirectoryExits(settings.postHooksDir)

    def _hasBackupLocation(self, home):
        if home == "":
            raise Exception("No backup location specified.  This can be set " +
                            "in caatinga.conf or by providing " +
                            "--backup-location.")

    def _doesBackupLocationExist(self, home):
        if os.path.exists(home) is False:
            raise Exception("Backup location doesn't exist.")

    def _isBackupLocationMounted(self, home):
        if os.path.ismount(home) is False:
            raise Exception("Backup location is not mounted")

    def _isBackupLocationRegistered(self, home):
        if os.path.exists(home + os.sep + "Backups.backupdb") is False:
            raise Exception("Backup location isn't registered.  Use " +
                            "'caat -g' to register.")

    def _doesRootDirectoryExist(self, root):
        if os.path.exists(root) is False:
            raise Exception("Root directory doesn't exist.")

    def _doesPreHooksDirectoryExits(self, directory):
        if len(directory) > 1 and os.path.exists(directory) is False:
            raise Exception("Pre hook directory does not exist.")

    def _doesPostHooksDirectoryExits(self, directory):
        if len(directory) > 1 and  os.path.exists(directory) is False:
            raise Exception("Post hook directory does not exist.")
