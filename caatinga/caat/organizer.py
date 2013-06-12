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

from datetime import datetime, timedelta
import caatinga.core.functions as fn


def organize(backupHome):
    """
    Reduce the backups to a frequency of daily for those that are
    older than one day, and to weekly for those that are older
    than 31 days.
    """
    catagorized = _catagorize(fn.getBackups(backupHome).values())
    for backup in _getExtraDailyBackups(catagorized["daily"]):
        fn.markBackupForDeletion(backupHome, backup)
    for backup in _getExtraWeeklyBackups(catagorized["weekly"]):
        fn.markBackupForDeletion(backupHome, backup)


def _catagorize(backups, now=datetime.now()):
    """
    Returns the backups in their respective categories of today,
    daily and weekly.
    """
    oneDay = timedelta(1)
    thirtyOneDays = timedelta(31)
    items = {
        "today": [],
        "daily": [],
        "weekly": []}

    for backup in backups:
        backupDate = fn.toDateTime(backup)
        diff = now - backupDate

        if diff > oneDay and diff < thirtyOneDays:
            items["daily"].append(backup)
        elif diff > thirtyOneDays:
            items["weekly"].append(backup)
        else:
            items["today"].append(backup)
    return items


def _getExtraDailyBackups(backups):
    """
    Returns the extra backups that appear more than once in the
    same day.
    """
    sortedBackups = [b for b in reversed(sorted(backups))]
    previous = None
    current = None
    index = 0
    results = []

    while index < len(sortedBackups):
        current = fn.toDateTime(sortedBackups[index])
        if previous is not None:
            if current.day == previous.day:
                results.append(sortedBackups[index])
        previous = fn.toDateTime(sortedBackups[index])
        index += 1
    return results


def _getExtraWeeklyBackups(backups):
    """
    Returns the backups that appear within one week of each other.
    """
    oneWeek = timedelta(7)
    previous = datetime.now().date()
    results = []

    for backup in sorted(backups):
        current = fn.toDateTime(backup).date()
        diff = current - previous

        # If the difference is a negative number, it's the first
        # backup and we can skip it
        if diff.days < 0:
            previous = current
            continue

        if diff < oneWeek:
            results.append(backup)
        else:
            previous = current
    return results
