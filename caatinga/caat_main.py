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
import errno
import caatinga.core.functions as fn
import caatinga.caat.backup as backup
import caatinga.caat.maintenance as maint
from time import strftime
from caatinga.core.args import getArgs
from caatinga.caat.organizer import organize
from caatinga.core.validation import SettingsValidator, ValidationException

__version__ = "1.0.3"


class CleanExitException(Exception):
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
    SettingsValidator().validate(settings)
    bkHome = fn.getBackupHome(settings.backupLocation, settings.hostName)
    lockFile = backup.getLockFile(bkHome, os.path.basename(__file__))
    outputWriter = fn.getOutputWriter(commandArgs.verbose)
    previousBackup = os.path.realpath(fn.getLatestLink(bkHome))

    checkForRegisterOption(settings, commandArgs, bkHome)
    insureBackupLocationIsRegistered(settings.backupLocation)

    lock(lockFile)
    fn.runHooks(settings.preBackupHooksDir)
    runNonBackupFunctions(bkHome, settings, commandArgs, outputWriter)
    executeBackup(bkHome, previousBackup, settings, outputWriter, lockFile)
    runMaintenanceFunctions(bkHome, settings, outputWriter)
    fn.runHooks(settings.postBackupHooksDir)


def runNonBackupFunctions(bkHome, settings, commandArgs, outputWriter):
    try:
        checkForDeleteOldest(commandArgs, bkHome)
        markPartialBackupForDeletion(bkHome)
        checkForClean(commandArgs, bkHome, outputWriter)
    except CleanExitException:
        fn.runHooks(settings.postBackupHooksDir)
        raise


def executeBackup(bkHome, previousBackup, settings, outWriter, lockFile):
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
    settings.reduceBackups and organize(bkHome)
    settings.keepDays and maint.checkForKeepDays(bkHome, settings.keepDays)
    settings.maxImages and maint.checkMaxImages(bkHome, settings.maxImages)
    maint.deleteBackupsMarkedForDeletion(bkHome, outputWriter)


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
        print(("The backup location {0} is now registered.").format(
            settings.backupLocation))
        raise CleanExitException()


def insureBackupLocationIsRegistered(backupLocation):
    if os.path.exists(backupLocation + os.sep + "Backups.backupdb") is False:
        raise ValidationException(
            "Backup location isn't registered.  Use " +
            "'caat -g' to register.")


def checkForDeleteOldest(commandArgs, bkHome):
    """
    Check if the option to delete the oldest backup was provided, and delete
    the oldest backup.
    """
    if commandArgs.deleteOldest:
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


def _isPidRunning(pid):
    try:
        os.kill(pid, 0)
        return True
    except OSError as e:
        return e.errno == errno.EPERM


def lock(lockFile):
    """
    Creates a lock file if one is not present.  If a lock file already exists,
    an exception will be thrown.
    """
    if os.path.exists(lockFile):
        with open(lockFile) as lock:
            pid = int(lock.readline())
        if _isPidRunning(pid):
            raise Exception("A backup is currently running [{}]".format(pid))
        else:
            os.remove(lockFile)
    backup.createLockFile(lockFile)

if __name__ == "__main__":
    main()