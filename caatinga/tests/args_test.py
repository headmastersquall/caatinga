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

import unittest
from caatinga.core.args import getArgParser


class ArgsTestCase(unittest.TestCase):
    """
    Test suite for testing the CommandArgs class.
    """

    def setUp(self):
        self.parser = getArgParser()

    def test_ShortBackupDestionationGetsSet(self):
        a = self.parser.parse_args(["-b", "/Foo"])
        self.assertEqual(
            a.backupLocation,
            "/Foo")

    def test_LongBackupDestionationGetsSet(self):
        a = self.parser.parse_args(["--backup-location=/Foo"])
        self.assertEqual(
            a.backupLocation,
            "/Foo")

    def test_ShortConfigOptionGetsSet(self):
        a = self.parser.parse_args(["-c", "/foo"])
        self.assertEqual(
            a.config,
            "/foo")

    def test_LongConfigOptionGetsSet(self):
        a = self.parser.parse_args(["--config=/foo"])
        self.assertEqual(
            a.config,
            "/foo")

    def test_ShortDeleteOldestGetsSet(self):
        a = self.parser.parse_args(["-d"])
        self.assertEqual(
            a.deleteOldest,
            True)

    def test_CleanOptionGetsSet(self):
        a = self.parser.parse_args(["--clean"])
        self.assertEqual(
            a.clean,
            True)

    def test_LongDeleteOldestGetsSet(self):
        a = self.parser.parse_args(["--delete-oldest"])
        self.assertEqual(
            a.deleteOldest,
            True)

    def test_ShortRegisterOptionGetsSet(self):
        a = self.parser.parse_args(["-g"])
        self.assertEqual(
            a.register,
            True)

    def test_LongRegisterOptionGetsSet(self):
        a = self.parser.parse_args(["--register"])
        self.assertEqual(
            a.register,
            True)

    def test_ShortHostNameOptionGetsSet(self):
        a = self.parser.parse_args(["-n", "Cheese"])
        self.assertEqual(
            a.hostName,
            "Cheese")

    def test_LongHostNameOptionGetsSet(self):
        a = self.parser.parse_args(["--hostname=Cheese"])
        self.assertEqual(
            a.hostName,
            "Cheese")

    def test_ShortRootOptionGetsSet(self):
        a = self.parser.parse_args(["-r", "/mnt/foo"])
        self.assertEqual(
            a.root,
            "/mnt/foo")

    def test_LongRootOptionGetsSet(self):
        a = self.parser.parse_args(["--root=/mnt/foo"])
        self.assertEqual(
            a.root,
            "/mnt/foo")

    def test_ShortVerboseOptionGetsSet(self):
        a = self.parser.parse_args(["-v"])
        self.assertEqual(
            a.verbose,
            True)

    def test_LongVerboseOptionGetsSet(self):
        a = self.parser.parse_args(["--verbose"])
        self.assertEqual(
            a.verbose,
            True)

    def test_ShortVersionOptionGetsSet(self):
        a = self.parser.parse_args(["-V"])
        self.assertEqual(
            a.version,
            True)

    def test_LongVersionOptionGetsSet(self):
        a = self.parser.parse_args(["--version"])
        self.assertEqual(
            a.version,
            True)

if __name__ == '__main__':
    unittest.main()
