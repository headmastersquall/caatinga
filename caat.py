#!/usr/bin/env python

# Copyright 2012 Chris Taylor
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
import caatinga.core.errorcodes as errorcodes
import caatinga.core.functions as fn
import caatinga.caat.backup as backup
from sys import argv
from time import strftime
from caatinga.caat.organizer import organize
from caatinga.core.CommandArgs import CommandArgs
from caatinga.core.SettingsValidator import SettingsValidator

__version__ = "caatinga version: 1.0.0"
usage = """Usage: caat [options]

These options are also available in lscaat.

Options:

    -b location, --backup-location=<location>
        Backup location to use.  This will override the setting in caatinga.conf.

    -c file, --config=<file>
        Specify an alternate configuration file.

    -d, --delete-oldest
        Delete the oldest backup that caat has created.

    -g, --register-backup
        Register the backup location as a backup device.

    -h, --help
        Displays this help message.

    -n hostname, --hostname=<hostname>
        Use this hostname instead of what is defined for the local system.

    -r path, --root=<path>
        Use this as the root directory to be backed up.

    -v, --verbose
        Verbose mode.  Display backup activity.

    -V, --version
        Displays version information and exits.
"""


def main(args):
    """
    Application entry point.
    """
    try:
        run_caat(args)
        exit(0)
    except OSError as er:
        if er.errno == errorcodes.FILESYSTEM_FULL:
            print("Backup drive is full")
        elif er.errno == errorcodes.PERMISSION_DENIED:
            print("Permission Denied")
        else:
            print("Operation not permitted on the mounted backup file system")
        exit(er.errno)
    except KeyboardInterrupt:
        exit(1)
    except Exception as ex:
        print(str(ex).strip("'"))
        exit(1)


def run_caat(args):
    """
    Main method for caat.
    """
    commandArgs = CommandArgs(args)
    if commandArgs.help:
        print(usage)
        exit(0)
    if commandArgs.version:
        print(__version__)
        exit(0)

    settings = fn.getSettingsInstance(commandArgs)
    checkForRegisterOption(settings, commandArgs)
    SettingsValidator().validate(settings)
    writer = fn.getOutputWriter(commandArgs.verbose)
    backupHome = fn.getBackupHome(settings.backupLocation, settings.hostName)
    previousBackup = os.path.realpath(fn.getLatestLink(backupHome))
    checkForDeleteOldest(commandArgs, backupHome)
    checkForIncompleteBackup(backupHome, writer)
    backupRoot = backup.createBackupRoot(
        backupHome,
        strftime("%Y-%m-%d-%H%M%S"),
        settings.backupgid)
    backup.createIncompleteBackupFile(
        backup.getIncompleteBackupFile(backupHome),
        backupRoot)
    backup.backupDirectory(
        backupRoot,
        previousBackup,
        settings.root,
        settings,
        writer)
    fn.updateLatestLink(backupHome)
    backup.deleteIncompleteBackupFile(backupHome)
    checkForReduceBackups(settings.reduceBackups, backupHome, writer)
    checkDrivePercentage(backupHome, settings.drivePercentage, writer)


def checkForRegisterOption(settings, commandArgs):
    """
    Check the command args for the register option and register the backup
    device if provided.  This will exit with a status 0 if a device was
    registered.
    """
    if commandArgs.register:
        fn.registerBackupDevice(
            settings.backupLocation,
            settings.backupgid)
        print(("The device mounted at {0} is now registered as a " +
              "backup device.").format(settings.backupLocation))
        exit(0)


def checkForDeleteOldest(commandArgs, backupHome):
    """
    Check if the option to delete the oldest backup was provided, and delete
    the oldest backup.
    """
    if commandArgs.deleteOldest:
        fn.deleteBackup(backupHome, fn.getOldestBackup(backupHome))
        exit(0)


def checkForIncompleteBackup(backupHome, writer):
    """
    Check to see if an incomplete backup file exists.  If so, delete that
    backup.
    """
    if os.path.exists(backup.getIncompleteBackupFile(backupHome)):
        writer("Incomplete backup detected")
        backup.deleteIncompleteBackup(
            backupHome,
            backup.getIncompleteBackupFile(backupHome))


def checkForReduceBackups(reduceBackups, backupHome, writer):
    """
    Reduce the backups if the reduce backups option is provided.
    """
    if reduceBackups:
        organize(backupHome, writer)


def checkDrivePercentage(backupHome, drivePercentage, outputWriter):
    '''
    Compares drive usage with user settings and deletes old backups as
    necessary.
    '''
    while drivePercentage < fn.getDriveUsagePercentage(backupHome):
        if len(fn.getBackups(backupHome)) <= 1:
            break
        oldest = fn.getOldestBackup(backupHome)
        outputWriter("Deleting: {0}".format(oldest))
        fn.deleteBackup(backupHome, oldest)

if __name__ == "__main__":
    main(argv)
