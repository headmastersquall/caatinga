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

import grp
import os
import unittest
import context
from caatinga.core import Settings


class SettingsTestCase(unittest.TestCase):
    """
    Test suite for testing the settings class.
    """
    _confFile = "caatinga.conf"

    def setUp(self):
        confFile = open(self._confFile, 'w')
        confFile.write("root = /foo\n")
        confFile.write("# A comment\n")
        confFile.write("hostname = foobar\n")
        confFile.write("max_file_size = 10\n")
        confFile.write("drive_percentage = 20\n")
        confFile.write("backup_location = /home\n")
        confFile.write("ignore = /var\n")
        confFile.write("ignore = /etc/group\n")
        confFile.write("ignore = /etc/passwd\n")
        confFile.write("backup_group = {0}\n".format(
            self._getFirstGroupName()))
        confFile.write("reduce_backups = yes\n")
        confFile.write("pre_hooks = /etc/caatinga/pre_hooks\n")
        confFile.write("post_hooks = /etc/caatinga/post_hooks\n")
        confFile.close()
        self.settings = Settings.Settings()
        self.settings.loadSettings()

    def _getFirstGroupName(self):
        return grp.getgrall()[0].gr_name

    def tearDown(self):
        os.remove(self._confFile)

    def test_Root(self):
        self.assertEqual(
            self.settings.root,
            "/foo",
            "Invalid value returned for root: {0}".format(self.settings.root))

    def test_HostName(self):
        self.assertEqual(
            self.settings.hostName,
            "foobar",
            "Invalid hostname returned: {0}".format(self.settings.hostName))

    def test_MaxFileSize(self):
        self.assertEqual(
            self.settings.maxFileSize,
            10485760,
            "Max file size not valid.")

    def test_DrivePercentage(self):
        self.assertEqual(
            self.settings.drivePercentage,
            20,
            "Drive percentage not valid.")

    def test_BackupLocation(self):
        self.assertEqual(
            self.settings.backupLocation,
            "/home",
            "Backup location not valid.")

    def test_IgnoreDirectories(self):
        for d in ["/home", "/var"]:
            self.assertTrue(
                self.settings.ignoredDirectories.count(d) == 1,
                "Ignore directory list has an invalid entry.")

    def test_IgnoreFiles(self):
        for f in ["/etc/group", "/etc/passwd"]:
            self.assertTrue(
                self.settings.ignoredFiles.count(f) == 1,
                "Ignore file list has an invalid entry.")

    def test_BackupGroup(self):
        self.assertEqual(
            self.settings.backupgid,
            self._getFirstGroupId(),
            "Backup Group Id was not set, or group doesn't exist.")

    def _getFirstGroupId(self):
        return grp.getgrall()[0].gr_gid

    def test_ReduceBackupsGetsSet(self):
        self.assertEqual(
            self.settings.reduceBackups,
            True,
            "Reduce Backups was not set")

    def test_PreHooksDir(self):
        self.assertEqual(
            self.settings.preHooksDir,
            "/etc/caatinga/pre_hooks",
            "Pre hooks dir was not set")

    def test_PostHooksDir(self):
        self.assertEqual(
            self.settings.postHooksDir,
            "/etc/caatinga/post_hooks",
            "Post hooks dir was not set")

if __name__ == '__main__':
    unittest.main()
