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

import os
import re
import errno
import caatinga.core.functions as fn
import caatinga.caat.backup as backup
import caatinga.caat.maintenance as maint
from time import strftime
from caatinga.core.args import getArgs
from caatinga.caat.organizer import organize
from caatinga.core.validation import SettingsValidator, ValidationException

__version__ = "1.1.1"


class CleanExitException(Exception):
    """
    This exception is used to exit the program cleanly and allows for any
    further maintenance calls to be performed first.  Throwing this exception
    does not indicate an error.
    """
    pass


def main():
    """
    Application entry point.
    """
    try:
        run_backup()
        exit(0)
    except OSError as er:
        if er.errno == errno.ENOSPC:
            print("Backup drive is full")
        elif er.errno == errno.EACCES:
            print("Permission Denied")
        else:
            print("Operation not permitted on the mounted backup file system")
        exit(er.errno)
    except KeyboardInterrupt:
        exit(1)
    except CleanExitException:
        exit(0)
    except Exception as ex:
        print(str(ex).strip("'"))
        exit(1)


def run_backup():
    """
    Main method that performs the backup.
    """
    commandArgs = getArgs()
    if commandArgs.version:
        print("caatinga version: " + __version__)
        exit(0)

    settings = fn.getSettingsInstance(commandArgs)
    lockFileName = settings.hostName + "-" + os.path.basename(__file__)
    SettingsValidator().validate(settings)
    bkHome = fn.getBackupHome(settings.backupLocation, settings.hostName)
    lockFile = backup.getLockFile("/tmp", lockFileName)
    outWriter = fn.getOutputWriter(commandArgs.verbose)
    previousBackup = os.path.realpath(fn.getLatestLink(bkHome))

    fn.runHooks(settings.preBackupHooksDir)
    checkForRegisterOption(settings, commandArgs, bkHome)
    insureBackupLocationIsRegistered(
        settings.backupLocation,
        settings.hostName)
    lock(lockFile)
    runNonBackupFunctions(bkHome, settings, commandArgs, outWriter, lockFile)
    executeBackup(bkHome, previousBackup, settings, outWriter, lockFile)
    runMaintenanceFunctions(bkHome, settings, outWriter)
    fn.runHooks(settings.postBackupHooksDir)


def checkForRegisterOption(settings, commandArgs, bkHome):
    """
    Check the command args for the register option and register the backup
    device if provided.  This will exit with a status 0 if a device was
    registered.
    """
    if commandArgs.register:
        fn.registerBackupLocation(
            settings.backupLocation,
            settings.backupgid,
            bkHome)
        print("The backup location {0} is now registered.".format(
            settings.backupLocation))
        raise CleanExitException()


def insureBackupLocationIsRegistered(backupLocation, hostName):
    """
    Raises a ValidationException if the backup location isn't registered.
    """
    backupPath = backupLocation + os.sep + \
        "Backups.backupdb" + os.sep + hostName
    if os.path.exists(backupPath) is False:
        raise ValidationException(
            "Backup location isn't registered.  Use " +
            "'caat -g' to register.")


def lock(lockFile):
    """
    Creates a lock file if one is not present.  If a lock file already exists,
    an exception will be thrown.
    """
    if os.path.exists(lockFile):
        with open(lockFile) as lock:
            pid = lock.readline()
        if not re.match(r"^[0-9]+$", pid):
            os.remove(lockFile)
        elif _isPidRunning(pid):
            raise Exception("A backup is currently running [{}]".format(pid))
        else:
            os.remove(lockFile)
    backup.createLockFile(lockFile)


def _isPidRunning(pid):
    """
    Returns True if the provided pid is currently running.  This is used when
    checking the pid that is written to the lock file to find out if another
    backup is running.
    """
    try:
        os.kill(int(pid), 0)
        return True
    except OSError as e:
        return e.errno == errno.EPERM


def runNonBackupFunctions(bkHome, settings, commandArgs, outWriter, lockFile):
    """
    Execute functions that do not pertain to actually performing a backup and
    are more intended on pre-backup conditions.
    """
    try:
        checkForDeleteOldest(commandArgs, bkHome)
        markPartialBackupForDeletion(bkHome)
        checkForClean(commandArgs, bkHome, outWriter)
    except CleanExitException:
        fn.runHooks(settings.postBackupHooksDir)
        backup.removeLockFile(lockFile)
        raise


def checkForDeleteOldest(commandArgs, bkHome):
    """
    Check if the option to delete the oldest backup was provided, and delete
    the oldest backup.
    """
    if commandArgs.deleteOldest:
        if len(fn.getBackups(bkHome)) > 1:
            fn.deleteBackup(bkHome, fn.getOldestBackup(bkHome))
        raise CleanExitException()


def markPartialBackupForDeletion(bkHome):
    """
    Looks for any partial backups and marks them for deletion.
    """
    if not os.path.exists(bkHome):
        return
    partials = fn.getPartialBackups(bkHome)
    for partial in partials:
        partialBackup = os.path.join(bkHome, partial)
        os.rename(partialBackup, partialBackup.replace(".part", ".delete"))


def checkForClean(commandArgs, bkHome, writer):
    """
    If the clean option is given, delete any backups marked for deletion,
    then exit.
    """
    if commandArgs.clean:
        maint.deleteBackupsMarkedForDeletion(bkHome, writer)
        raise CleanExitException()


def executeBackup(bkHome, previousBackup, settings, outWriter, lockFile):
    """
    Perform the backup using the settings provided by the user.
    """
    try:
        backupRoot = backup.createBackupRoot(
            bkHome,
            strftime("%Y-%m-%d-%H%M%S") + ".part",
            settings.backupgid)

        backup.backupDirectory(
            backupRoot,
            previousBackup,
            settings.root,
            settings,
            outWriter)
        os.rename(backupRoot, backupRoot.replace(".part", ""))
        fn.updateLatestLink(bkHome)
    finally:
        backup.removeLockFile(lockFile)


def runMaintenanceFunctions(bkHome, settings, outputWriter):
    """
    Execute maintenance functions that are intended to be ran after a
    successful backup has been performed.
    """
    settings.reduceBackups and organize(bkHome)
    settings.keepDays and maint.checkForKeepDays(bkHome, settings.keepDays)
    settings.maxImages and maint.checkMaxImages(bkHome, settings.maxImages)
    maint.deleteBackupsMarkedForDeletion(bkHome, outputWriter)

if __name__ == "__main__":
    main()
