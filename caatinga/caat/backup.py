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
import shutil
import caatinga.core.functions as fn
from os.path import join, exists


def createLockFile(lockFile):
    """
    Create a new file with the provided name that contains the pid of the
    current process.
    """
    with open(lockFile, 'w') as lock:
        lock.write(str(os.getpid()))


def removeLockFile(lockFile):
    """
    Removes the provided lock file.
    """
    if os.path.exists(lockFile):
        os.remove(lockFile)


def createBackupRoot(backupHome, backup, gid):
    """
    Creates the root directory for a backup and assigns the
    provided gid.  Permissions are set as 770.
    """
    root = join(backupHome, backup)
    os.makedirs(root)
    os.chmod(root, 0o0770)
    fn.tryToSetOwnership(root, os.getuid(), gid)
    return root


def backupDirectory(backupRoot, previousBackup, directory, settings, writer):
    """
    Primary function to perform a system backup.
    """
    if directory in settings.ignoredDirectories:
        writer("Ignore: {0}".format(directory))
        return

    altRootDir = fn.removeAltRoot(settings.root, directory)
    destination = backupRoot + altRootDir
    createDestination(directory, destination)

    for item in (join(directory, f) for f in os.listdir(directory)):
        if os.path.islink(item):
            backupLink(backupRoot, item, settings.root)
        elif os.path.isdir(item):
            backupDirectory(backupRoot, previousBackup, item, settings, writer)
        elif os.path.isfile(item):
            if skipFile(item, settings.ignoredFiles, settings.maxFileSize):
                writer("Ignore: {0}".format(item))
            else:
                backupFile(
                    backupRoot, previousBackup, item, settings.root, writer)

    os.utime(
        destination,
        (os.path.getatime(directory), os.path.getmtime(directory)))


def skipFile(file_, ignoreList, maxSize):
    """
    Returns True if the provided file should not be backed up.
    """
    if file_ in ignoreList:
        return True
    if maxSize > 0:
        if os.path.getsize(file_) > maxSize:
            return True
    return False


def createDestination(localDir, backupDir):
    """
    Create a backup directory with the same stat and ownership
    as the local directory.
    """
    if exists(backupDir) is False:
        os.mkdir(backupDir)
        shutil.copystat(localDir, backupDir)
        fn.copyOwnership(localDir, backupDir)


def backupLink(backupRoot, symbolicLink, altRoot):
    """
    Backup a symbolic link.
    """
    realValue = os.readlink(symbolicLink)
    newLinkDest = backupRoot + fn.removeAltRoot(altRoot, symbolicLink)
    os.symlink(realValue, newLinkDest)


def backupFile(backupRoot, previousBackup, file_, altRoot, writer):
    """
    Backup a file to according to the files state.  If it's new or modified,
    it's copied otherwise a hard link is created pointing to the file found
    in the previous backup.
    """
    previousFileName = previousBackup + fn.removeAltRoot(altRoot, file_)
    backupFileName = backupRoot + fn.removeAltRoot(altRoot, file_)

    if isFileModifiedOrNew(previousFileName, file_):
        writer("Copying: {0}".format(file_))
        fn.copy(file_, backupFileName)
    else:
        writer("Linking: {0}".format(file_))
        os.link(previousFileName, backupFileName)


def isFileModifiedOrNew(previousFile, localFile):
    """
    Returns true if the local file is a new file or if it has been modified
    since the last backup was ran.
    """
    if os.path.exists(previousFile) is False:
        return True
    return fn.isModified(localFile, previousFile)
