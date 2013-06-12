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

import unittest
import context
from caatinga.core.CommandArgs import CommandArgs


class CommandArgsTestCase(unittest.TestCase):
    """
    Test suite for testing the CommandArgs class.
    """

    def test_ShortBackupDestionationGetsSet(self):
        a = CommandArgs(["-b", "/Foo"])
        self.assertEqual(
            a.backupLocation,
            "/Foo")

    def test_LongBackupDestionationGetsSet(self):
        a = CommandArgs(["--backup-location=/Foo"])
        self.assertEqual(
            a.backupLocation,
            "/Foo")

    def test_ShortConfigOptionGetsSet(self):
        a = CommandArgs(["-c", "/foo"])
        self.assertEqual(
            a.config,
            "/foo")

    def test_LongConfigOptionGetsSet(self):
        a = CommandArgs(["--config=/foo"])
        self.assertEqual(
            a.config,
            "/foo")

    def test_ShortDeleteOldestGetsSet(self):
        a = CommandArgs(["-d"])
        self.assertEqual(
            a.deleteOldest,
            True)

    def test_CleanOptionGetsSet(self):
        a = CommandArgs(["--clean"])
        self.assertEqual(
            a.clean,
            True)

    def test_LongDeleteOldestGetsSet(self):
        a = CommandArgs(["--delete-oldest"])
        self.assertEqual(
            a.deleteOldest,
            True)

    def test_ShortRegisterOptionGetsSet(self):
        a = CommandArgs(["-g"])
        self.assertEqual(
            a.register,
            True)

    def test_LongRegisterOptionGetsSet(self):
        a = CommandArgs(["--register-backup"])
        self.assertEqual(
            a.register,
            True)

    def test_ShortHelpOptionGetsSet(self):
        a = CommandArgs(["-h"])
        self.assertEqual(
            a.help,
            True)

    def test_LongHelpOptionGetsSet(self):
        a = CommandArgs(["--help"])
        self.assertEqual(
            a.help,
            True)

    def test_ShortHostNameOptionGetsSet(self):
        a = CommandArgs(["-n", "Cheese"])
        self.assertEqual(
            a.hostName,
            "Cheese")

    def test_LongHostNameOptionGetsSet(self):
        a = CommandArgs(["--hostname=Cheese"])
        self.assertEqual(
            a.hostName,
            "Cheese")

    def test_ShortRootOptionGetsSet(self):
        a = CommandArgs(["-r", "/mnt/foo"])
        self.assertEqual(
            a.root,
            "/mnt/foo")

    def test_LongRootOptionGetsSet(self):
        a = CommandArgs(["--root=/mnt/foo"])
        self.assertEqual(
            a.root,
            "/mnt/foo")

    def test_ShortVerboseOptionGetsSet(self):
        a = CommandArgs(["-v"])
        self.assertEqual(
            a.verbose,
            True)

    def test_LongVerboseOptionGetsSet(self):
        a = CommandArgs(["--verbose"])
        self.assertEqual(
            a.verbose,
            True)

    def test_ShortVersionOptionGetsSet(self):
        a = CommandArgs(["-V"])
        self.assertEqual(
            a.version,
            True)

    def test_LongVersionOptionGetsSet(self):
        a = CommandArgs(["--version"])
        self.assertEqual(
            a.version,
            True)

    def test_InvalidCommandThrowsException(self):
        self.assertRaises(Exception, CommandArgs, ["--foo"])

    def test_ShortBackupLocationRequiresValue(self):
        self.assertRaises(Exception, CommandArgs, ["-b"])

    def test_LongBackupLocationRequiresValue(self):
        self.assertRaises(Exception, CommandArgs, ["--backup-location"])

    def test_ShortConfigRequiresValue(self):
        self.assertRaises(Exception, CommandArgs, ["-c"])

    def test_LongConfigRequiresValue(self):
        self.assertRaises(Exception, CommandArgs, ["--config"])

    def test_ShortHostNameRequiresValue(self):
        self.assertRaises(Exception, CommandArgs, ["-n"])

    def test_LongHostNameRequiresValue(self):
        self.assertRaises(Exception, CommandArgs, ["--hostname"])

    def test_ShortRootRequiresValue(self):
        self.assertRaises(Exception, CommandArgs, ["-r"])

    def test_LongRootRequiresValue(self):
        self.assertRaises(Exception, CommandArgs, ["--root"])

if __name__ == '__main__':
    unittest.main()
