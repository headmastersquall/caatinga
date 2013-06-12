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
import unittest
import context
import caatinga.caat.backup as backup
from os.path import join
from shutil import rmtree
from testutils import touch


class BackupTestCase(unittest.TestCase):
    """
    Test case for testing the backup functions of caat.
    """

    _backupHome = "backup_test"

    def setUp(self):
        os.mkdir(self._backupHome)

    def tearDown(self):
        rmtree(self._backupHome)

    def test_createLockFile(self):
        lockFile = join(self._backupHome, "test.lock")
        backup.createLockFile(lockFile)
        self.assertTrue(os.path.exists(lockFile))
        os.remove(lockFile)

    def test_removeLockFile(self):
        lockFile = join(self._backupHome, "test.lock")
        backup.createLockFile(lockFile)
        backup.removeLockFile(lockFile)
        self.assertFalse(os.path.exists(lockFile))

    def test_createBackupRoot(self):
        backupName = "FOO-123"
        gid = os.getgid()
        backup.createBackupRoot(self._backupHome, backupName, gid)
        root = join(self._backupHome, backupName)
        self.assertTrue(
            os.path.exists(root),
            "Backup root does not exist.")

    def test_shouldFileBeSkipped(self):
        testFile = join(self._backupHome, "cheese")
        largeFile = join(self._backupHome, "big-cheese")
        self._addLargeFileContent(largeFile)
        ignored = ["/foo/bar", "/bar/baz", testFile]
        self.assertTrue(
            backup.skipFile(testFile, ignored, 0),
            "File was not skipped.")
        self.assertFalse(
            backup.skipFile("/etc/fstab", ignored, 0),
            "File was skipped.")
        self.assertTrue(
            backup.skipFile(largeFile, ignored, 100),
            "Large file was not skipped.")

    def _addLargeFileContent(self, file_):
        with open(file_, 'w') as f:
            f.write("0" * 1000)

    def test_backupLink(self):
        linkSource = join(self._backupHome, "Foo")
        fullLinkName = join(join(os.getcwd(), self._backupHome), "Bar")
        linkName = join(self._backupHome, "Bar")
        backupDir = join(self._backupHome, "backup")
        os.makedirs(join(backupDir, self._backupHome))
        os.symlink(linkSource, fullLinkName)
        backup.backupLink(backupDir, fullLinkName, os.getcwd())
        self.assertTrue(os.path.lexists(join(backupDir, linkName)))
        rmtree(backupDir)

    def test_isFileModifiedOrNew_fileIsNew(self):
        newFile = join(self._backupHome, "newFile")
        touch(newFile)
        self.assertTrue(backup.isFileModifiedOrNew("Blah", newFile))
        os.remove(newFile)

    def test_isFileModifiedOrNew_fileIsModified(self):
        previousFile = join(self._backupHome, "oldFile")
        newFile = join(self._backupHome, "newFile")
        touch(previousFile)
        touch(newFile)
        os.utime(previousFile, (1340664089, 1320861443))
        self.assertTrue(backup.isFileModifiedOrNew(previousFile, newFile))
        os.remove(previousFile)
        os.remove(newFile)

    def test_isFileModifiedOrNew_fileHasNoChanges(self):
        previousFile = join(self._backupHome, "oldFile")
        newFile = join(self._backupHome, "newFile")
        touch(previousFile)
        touch(newFile)
        self.assertFalse(backup.isFileModifiedOrNew(previousFile, newFile))
        os.remove(previousFile)
        os.remove(newFile)

if __name__ == '__main__':
    unittest.main()
