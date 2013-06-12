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

import caatinga.core.functions as fn


def info(args, settings):
    """
    Main function for the info option.
    """
    backupHome = fn.getBackupHome(settings.backupLocation, settings.hostName)
    backupCount = len(fn.getBackups(backupHome))
    dtFormat = "%m/%d/%Y %H:%M:%S"
    lastBackupRan = fn.toDateTime(
        fn.getLatestBackup(backupHome)).strftime(dtFormat)
    driveUsagePercentage = fn.getDriveUsagePercentage(backupHome)
    fmt = "{0:<20} {1}"

    print(fmt.format("Backup location:", settings.backupLocation))
    print(fmt.format("Host Name:", settings.hostName))
    print(fmt.format("Number of Backups:", backupCount))
    print(fmt.format("Last Backup Ran:", lastBackupRan))
    print(fmt.format("Drive Capacity:", "{0}%".format(driveUsagePercentage)))
