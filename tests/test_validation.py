#!/usr/bin/env python

# Copyright 2014 Chris Taylor
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
from shutil import rmtree
from caatinga.core.validation import SettingsValidator, ValidationException

BACKUP_HOME = "bk"
BACKUP_DB = BACKUP_HOME + os.sep + "Backups.backupdb"
NONEXISTING_DIR = "/foo/bar"


class MockSettings():
    def __init__(self):
        self.backupLocation = BACKUP_HOME
        self.root = "/"
        self.preBackupHooksDir = "/"
        self.postBackupHooksDir = "/"
        self.preRestoreHooksDir = "/"
        self.postRestoreHooksDir = "/"


class SettingsValidatorTestCase(unittest.TestCase):
    """
    Test suite for testing the settings validation class.
    """

    def setUp(self):
        if not os.path.exists(BACKUP_HOME):
            os.mkdir(BACKUP_HOME)
        if not os.path.exists(BACKUP_DB):
            os.mkdir(BACKUP_DB)
        self.settings = MockSettings()
        self.validator = SettingsValidator()

    def tearDown(self):
        rmtree(BACKUP_HOME)

    def test_hasBackupLocation(self):
        self.settings.backupLocation = ""
        self.assertValidateRaisesException()

    def test_doesBackupLocationExist(self):
        self.settings.backupLocation = NONEXISTING_DIR
        self.assertValidateRaisesException()

    def test_doesRootDirectoryExist(self):
        self.settings.root = NONEXISTING_DIR
        self.assertValidateRaisesException()

    def test_doesPreBackupHooksDirectoryExits(self):
        self.settings.preBackupHooksDir = NONEXISTING_DIR
        self.assertValidateRaisesException()

    def test_doesPostBackupHooksDirectoryExits(self):
        self.settings.postBackupHooksDir = NONEXISTING_DIR
        self.assertValidateRaisesException()

    def test_doesPreRestoreHooksDirectoryExits(self):
        self.settings.preRestoreHooksDir = NONEXISTING_DIR
        self.assertValidateRaisesException()

    def test_doesPostRestoreHooksDirectoryExits(self):
        self.settings.postRestoreHooksDir = NONEXISTING_DIR
        self.assertValidateRaisesException()

    def assertValidateRaisesException(self):
        self.assertRaises(
            ValidationException,
            self.validator.validate,
            self.settings)

if __name__ == '__main__':
    unittest.main()
