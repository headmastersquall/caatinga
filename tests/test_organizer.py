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
from datetime import datetime
from shutil import rmtree
from caatinga.caat import organizer


class OrganizerTestCase(unittest.TestCase):
    """
    Test case for testing organizer module.
    """

    _backupHome = "organizer_test"
    _today = datetime(2012, 5, 27)

    def setUp(self):
        os.mkdir(self._backupHome)
        self._backups = [
            "2012-04-03-120728",
            "2012-04-10-120728",
            "2012-04-12-120728",
            "2012-04-19-120728",  # Start of weekly
            "2012-04-26-120728",
            "2012-05-17-120728",
            "2012-05-22-120728",
            "2012-05-23-120728",
            "2012-05-24-100728",
            "2012-05-24-120728",
            "2012-05-25-120728",
            "2012-05-26-180728",  # Start of daily
            "2012-05-27-120528",
            "2012-05-27-120628",
            "2012-05-27-120728"]

    def tearDown(self):
        rmtree(self._backupHome)

    def test_catagorize(self):
        catagorized = organizer._catagorize(self._backups, self._today)
        todayCount = len(catagorized["today"])
        self.assertEqual(
            todayCount,
            4,
            "Incorrect today returned: {0}".format(todayCount))
        dailyCount = len(catagorized["daily"])
        self.assertEqual(
            dailyCount,
            7,
            "Incorrect daily returned: {0}".format(dailyCount))
        weeklyCount = len(catagorized["weekly"])
        self.assertEqual(
            weeklyCount,
            4,
            "Incorrect weekly returned: {0}".format(weeklyCount))

    def test_getExtraDailyBackups(self):
        backups = organizer._catagorize(self._backups, self._today)["daily"]
        extra = organizer._getExtraDailyBackups(backups)
        self.assertEqual(
            len(extra),
            1,
            "Incorrect extra daily: {0}".format(len(extra)))

    def test_getExtraWeeklyBackups(self):
        backups = organizer._catagorize(self._backups, self._today)["weekly"]
        extra = organizer._getExtraWeeklyBackups(backups)
        self.assertEqual(
            len(extra),
            1,
            "Incorrect extra weekly: {0}".format(len(extra)))

    def test_firstBackupDosntThrowError(self):
        backups = {
            "today": [],
            "daily": [],
            "weekly": []}
        organizer._getExtraDailyBackups(backups["daily"])
        organizer._getExtraWeeklyBackups(backups["weekly"])

if __name__ == '__main__':
    unittest.main()
