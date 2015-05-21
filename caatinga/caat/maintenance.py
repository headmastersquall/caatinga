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

from datetime import datetime, timedelta
import caatinga.core.functions as fn


def checkMaxImages(backupHome, maxImages):
    """
    When the number of backup images are greater than the max provided in
    settings, mark the extra images to be deleted.
    """
    backups = fn.getBackups(backupHome)
    if len(backups.keys()) > maxImages:
        toRemove = list(backups.keys())[:len(backups.keys()) - maxImages]
        for id in toRemove:
            fn.markBackupForDeletion(backupHome, backups[id])


def deleteBackupsMarkedForDeletion(backupHome, writer):
    """
    Delete backups that are marked to be deleted.
    """
    for backup in fn.getBackupsMarkedForDeletion(backupHome):
        writer("Deleting: {}".format(backup))
        fn.deleteBackup(backupHome, backup)


def checkForKeepDays(backupHome, keepDays):
    """
    When the number of days a backup exists is greater than keepDays, those
    older backups are deleted.  Do not delete any backups if keepDays is zero.
    """
    def isOld(backup):
        dt = fn.toDateTime(backup)
        expire = datetime.now() - timedelta(days=keepDays)
        return dt <= expire

    backups = fn.getBackups(backupHome).values()
    toRemove = filter(isOld, backups)
    for backup in toRemove:
        fn.markBackupForDeletion(backupHome, backup)
