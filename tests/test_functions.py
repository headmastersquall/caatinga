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
import caatinga.core.functions as fn
from os import sep
from shutil import rmtree
from os.path import join, exists
from datetime import datetime
from testutils import touch


class FunctionsTestCase(unittest.TestCase):
    """
    Test case for testing the core functions.
    """

    _backupHome = "backups_test"

    def setUp(self):
        os.mkdir(self._backupHome)
        os.mkdir(join(self._backupHome, "2012-01-25-120729"))
        os.mkdir(join(self._backupHome, "2012-03-30-160006"))
        os.mkdir(join(self._backupHome, "2012-05-18-160013"))
        os.symlink("2012-05-18-160013", join(self._backupHome, "Latest"))
        os.mkdir(join(self._backupHome, "2012-03-30-160006/foo"))
        self.touch(join(self._backupHome, "2012-03-30-160006/foo/bar.gz"))
        self.touch(join(self._backupHome, "2012-03-30-160006/foo/bed.py"))
        self.touch(join(self._backupHome, "2012-03-30-160006/foo/cat.foo"))

    def tearDown(self):
        rmtree(self._backupHome)

    def touch(self, fileName):
        with open(fileName, 'w'):
            pass

    def test_getBackups(self):
        backups = fn.getBackups(self._backupHome)
        self.assertEqual(
            len(backups),
            3,
            "Incorrect number of backups returned: {0}".format(len(backups)))

    def test_insureBackupHomeExists_throwsException(self):
        self.assertRaises(Exception, fn.insureBackupHomeExists, "asdf")

    def test_insureBackupHomeExists_noException(self):
        fn.insureBackupHomeExists(self._backupHome)

    def test_getBackupHome(self):
        backupHome = fn.getBackupHome("/mnt/foo", "choco")
        self.assertEqual(
            backupHome,
            "/mnt/foo/Backups.backupdb/choco",
            "Incorrect backup home returned: {0}".format(backupHome))

    def test_getLatestBackup(self):
        latest = fn.getLatestBackup(self._backupHome)
        self.assertEqual(
            latest,
            "2012-05-18-160013",
            "Incorrect latest backup returned: {0}".format(latest))

    def test_getLatestLink(self):
        latest = fn.getLatestLink(self._backupHome)
        self.assertEqual(
            latest,
            "backups_test/Latest",
            "Incorrect latest link returned: {0}".format(latest))

    def test_getMostRecentBackup(self):
        recentBackup = fn.getMostRecentBackup(self._backupHome)
        self.assertEqual(
            recentBackup,
            "2012-05-18-160013",
            "Incorrect most recent backup: {0}".format(recentBackup))

    def test_getOldestBackup(self):
        oldest = fn.getOldestBackup(self._backupHome)
        self.assertEqual(
            oldest,
            "2012-01-25-120729",
            "Incorrect oldest backup returned: {0}".format(oldest))

    def test_deleteBackup(self):
        backup = "2012-02-27-120728"
        backupPath = join(self._backupHome, backup)
        os.makedirs(backupPath + "/foo/bar")
        fn.deleteBackup(self._backupHome, backup)
        self.assertFalse(os.path.exists(backupPath))

    def test_markBackupForDeletion(self):
        backup = "2012-01-28-120628"
        backupPath = join(self._backupHome, backup)
        os.makedirs(backupPath)
        fn.markBackupForDeletion(self._backupHome, backup)
        self.assertTrue(os.path.exists(backupPath + ".delete"))

    def test_getBackupsMarkedForDeletion(self):
        backup = join(self._backupHome, "2010-01-25-120729.delete")
        os.makedirs(backup)
        backups = fn.getBackupsMarkedForDeletion(self._backupHome)
        self.assertTrue(len(backups) == 1)

    def test_getPartialBackups(self):
        backup = join(self._backupHome, "2009-01-24-120729.part")
        os.makedirs(backup)
        backups = fn.getPartialBackups(self._backupHome)
        self.assertTrue(len(backups) == 1)

    def test_toDateTime(self):
        dt = fn.toDateTime("2012-05-18-160013")
        self.assertEqual(dt.year, 2012)
        self.assertEqual(dt.month, 5)
        self.assertEqual(dt.day, 18)
        self.assertEqual(dt.hour, 16)
        self.assertEqual(dt.minute, 0)
        self.assertEqual(dt.second, 13)

    def test_expandGlob(self):
        backup = "2012-03-30-160006"
        cwd = "/foo"
        items = fn.expandGlob(self._backupHome, backup, cwd, "b*")
        expected = [
            join(self._backupHome, backup) + cwd + sep + "bar.gz",
            join(self._backupHome, backup) + cwd + sep + "bed.py"]
        items.sort()
        expected.sort()
        for i in range(len(items)):
            self.assertEqual(items[i], expected[i])

    def test_getGroup(self):
        group = fn.getGroup(0)
        self.assertEqual(
            group,
            "root",
            "Incorrect group returned: {0}".format(group))

    def test_getUser(self):
        user = fn.getUser(0)
        self.assertEqual(
            user,
            "root",
            "Incorrect user returned: {0}".format(user))

    def test_getInfo(self):
        fileName = "/etc/passwd"
        info = fn.getInfo(fileName)
        self.assertEqual(info["type"], "F")
        self.assertEqual(info["size"], os.path.getsize(fileName))
        self.assertEqual(info["modified"],
                         datetime.fromtimestamp(os.path.getmtime(fileName)))
        self.assertEqual(info["name"], "passwd")
        self.assertEqual(info["owner"], "root")
        self.assertEqual(info["group"], "root")

    def test_getArgs_allParameters(self):
        args = fn.parseWordArgs(["asdf", "from", "backup", "43", "as", "bar"])
        self.assertEqual(args["glob"], "asdf")
        self.assertEqual(args["id"], "43")
        self.assertEqual(args["as"], "bar")

    def test_getArgs_idAndAs(self):
        args = fn.parseWordArgs(["from", "backup", "43", "as", "bar"])
        self.assertEqual(args["glob"], "*")
        self.assertEqual(args["id"], "43")
        self.assertEqual(args["as"], "bar")

    def test_getArgs_id(self):
        args = fn.parseWordArgs(["from", "backup", "43"])
        self.assertEqual(args["glob"], "*")
        self.assertEqual(args["id"], "43")
        self.assertEqual(args["as"], None)

    def test_getArgs_glob(self):
        args = fn.parseWordArgs(["foo"])
        self.assertEqual(args["glob"], "foo")
        self.assertEqual(args["id"], None)
        self.assertEqual(args["as"], None)

    def test_getArgs_fromAll(self):
        args = fn.parseWordArgs(["from", "all"])
        self.assertEqual(args["glob"], "*")
        self.assertEqual(args["id"], "all")
        self.assertEqual(args["as"], None)

    def test_getBackupsForArgs_oneId(self):
        args = fn.parseWordArgs(["from", "backup", "2"])
        backups = fn.getBackupsForArgs(args, fn.getBackups(self._backupHome))
        self.assertEqual(backups[2], "2012-05-18-160013")

    def test_getBackupsForArgs_all(self):
        args = fn.parseWordArgs(["from", "all"])
        backups = fn.getBackupsForArgs(args, fn.getBackups(self._backupHome))
        self.assertEqual(
            len(backups),
            3,
            "Incorrect number of backups returned: {0}".format(len(backups)))

    def test_getBackupOrLastest_usingWordArgs(self):
        args = fn.parseWordArgs(["from", "backup", "1"])
        backup = fn.getBackupOrLatest(args, self._backupHome)
        self.assertEqual(
            backup,
            "2012-03-30-160006",
            "Incorrect backup returned: {0}".format(backup))

    def test_getBackupOrLastest_expectingLatest(self):
        args = fn.parseWordArgs([])
        backup = fn.getBackupOrLatest(args, self._backupHome)
        self.assertEqual(
            backup,
            "2012-05-18-160013",
            "Incorrect backup returned: {0}".format(backup))

    def test_copyFile(self):
        src = join(self._backupHome, "foo")
        dest = join(self._backupHome, "bar")
        self.touch(src)
        fn.copyFile(src, dest)
        self.assertTrue(exists(dest))
        os.remove(src)
        os.remove(dest)

    def test_copyLink(self):
        src = join(self._backupHome, "foo")
        link = join(self._backupHome, "bar")
        dest = join(self._backupHome, "baz")
        self.touch(src)
        os.link(src, link)
        fn.copyFile(link, dest)
        self.assertTrue(exists(dest))
        os.remove(link)
        os.remove(src)
        os.remove(dest)

    def test_copyDir(self):
        src = join(self._backupHome, "foo")
        dest = join(self._backupHome, "bar")
        deepDir = src + sep + "cheese" + sep + "beef"
        os.makedirs(deepDir)
        self.touch(deepDir + sep + "hotdog")
        fn.copyDir(src, dest)
        self.assertTrue(exists(deepDir + sep + "hotdog"))
        fn.shutil.rmtree(src)
        fn.shutil.rmtree(dest)

    def test_removeAltRoot_noAlt(self):
        testFile = "/mnt/foo/bar"
        newRoot = fn.removeAltRoot("/", testFile)
        self.assertEqual(
            newRoot,
            testFile,
            "Original root was modified: {0}".format(newRoot))

    def test_removeAltRoot_withAlt(self):
        testFile = "/mnt/foo/bar"
        newRoot = fn.removeAltRoot("/mnt", testFile)
        self.assertEqual(
            newRoot,
            "/foo/bar",
            "Invalid alt root returned: {0}".format(newRoot))

    def test_checkingIfFileIsExcetutable(self):
        executableFile = join(self._backupHome, "exeFile")
        touch(executableFile)
        os.chmod(executableFile, 755)
        self.assertTrue(fn.isExecutable(executableFile))
        os.remove(executableFile)

    def test_getExecutableFiles_returnsProperFileList(self):
        directory = "fileList"
        os.mkdir(directory)
        touch(join(directory, "a"), 755)
        touch(join(directory, "c"), 755)
        touch(join(directory, "b"), 755)
        expected = [
            join(directory, "a"),
            join(directory, "b"),
            join(directory, "c")]
        self.assertEqual(fn.getExecutableFiles(directory), expected)
        os.remove(join(directory, "a"))
        os.remove(join(directory, "b"))
        os.remove(join(directory, "c"))
        os.rmdir(directory)

if __name__ == '__main__':
    unittest.main()
