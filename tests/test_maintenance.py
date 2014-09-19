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
import caatinga.caat.maintenance as maint
from os.path import join
from datetime import datetime as dt
from datetime import timedelta as delta
from shutil import rmtree


class MaintenanceTestCase(unittest.TestCase):
    """
    Test case for testing the maintenance functions of caat.
    """

    _format = "%Y-%m-%d-%H%M%S"
    _backupHome = "backup_test"

    def setUp(self):
        os.mkdir(self._backupHome)
        date = dt.now()
        os.mkdir(join(self._backupHome, date.strftime(self._format)))
        date = date - delta(days=1)
        os.mkdir(join(self._backupHome, date.strftime(self._format)))
        date = date - delta(hours=1)
        os.mkdir(join(self._backupHome, date.strftime(self._format)))

    def tearDown(self):
        rmtree(self._backupHome)

    def getNonDeleteCount(self):
        return len([d for d in os.listdir(self._backupHome)
                    if not d.endswith(".delete")])

    def test_checkMaxImages(self):
        max = 2
        maint.checkMaxImages(self._backupHome, max)
        self.assertEqual(
            self.getNonDeleteCount(),
            max,
            "Wrong number of backups remaining.")

    def test_deleteBackupsMarkedForDeletion(self):
        fst = join(self._backupHome, os.listdir(self._backupHome)[0])
        os.rename(fst, fst + ".delete")
        maint.deleteBackupsMarkedForDeletion(
            self._backupHome,
            lambda x: x)
        self.assertEqual(
            self.getNonDeleteCount(),
            2,
            "Wrong number of backups deleted.")

    def test_checkForKeepDays(self):
        keep = 1
        maint.checkForKeepDays(self._backupHome, keep)
        self.assertEqual(
            self.getNonDeleteCount(),
            keep,
            "Wrong number of backup images kept.")

if __name__ == '__main__':
    unittest.main()
