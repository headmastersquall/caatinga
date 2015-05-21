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

__all__ = ["SettingsValidator", "ValidationException"]


class ValidationException(Exception):
    pass


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
        self._doesRootDirectoryExist(settings.root)
        self._doesHooksDirectoryExits(settings.preBackupHooksDir)
        self._doesHooksDirectoryExits(settings.postBackupHooksDir)
        self._doesHooksDirectoryExits(settings.preRestoreHooksDir)
        self._doesHooksDirectoryExits(settings.postRestoreHooksDir)

    def _hasBackupLocation(self, home):
        if home == "":
            raise ValidationException(
                "No backup location specified.  This can be set " +
                "in caatinga.conf or by providing " +
                "--backup-location.")

    def _doesBackupLocationExist(self, home):
        if os.path.exists(home) is False:
            raise ValidationException("Backup location doesn't exist.")

    def _doesRootDirectoryExist(self, root):
        if os.path.exists(root) is False:
            raise ValidationException("Root directory doesn't exist.")

    def _doesHooksDirectoryExits(self, directory):
        if len(directory) > 1 and os.path.exists(directory) is False:
            raise ValidationException("Hook directory does not exist.")
