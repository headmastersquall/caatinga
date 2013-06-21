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
import re
import shutil
import stat
import sys
from datetime import datetime
from glob import glob
from os.path import join


def registerBackupDevice(backupLocation, gid):
    """
    Register this device as a backup device.
    """
    backupHome = join(backupLocation, "Backups.backupdb")

    if os.path.ismount(backupLocation) is False:
        message = "There is no mounted device at {0} to be registered"
        raise Exception(message.format(backupLocation))

    if os.path.exists(backupHome):
        message = "The device mounted at {0} is already registered."
        raise Exception(message.format(backupLocation))
    else:
        os.mkdir(backupHome)
        os.chmod(backupHome, 0o0770)
        tryToSetOwnership(backupHome, os.getuid(), gid)


def tryToSetOwnership(item, uid, gid):
    """
    Try to set the ownership of the provided item.  If it fails, just continue.
    """
    try:
        os.chown(item, uid, gid)
    except OSError:
        pass


def getSettingsInstance(commandArgs):
    """
    Build a settings instance and set the applicable values from the command
    args.
    """
    from caatinga.core.Settings import Settings
    settings = Settings()
    settings.loadSettings(commandArgs.config)

    if commandArgs.root:
        settings.root = commandArgs.root
    if commandArgs.hostName:
        settings.hostName = commandArgs.hostName
    if commandArgs.backupLocation:
        settings.backupLocation = commandArgs.backupLocation
    return settings


def getBackups(backupHome):
    """
    Returns a list of backups from the provided backup home.
    """
    insureBackupHomeExists(backupHome)
    index = 0
    backups = {}

    for backup in sorted(d for d in os.listdir(backupHome)
                         if re.match("^\d{4}-\d{2}-\d{2}-\d{6}$", d)):
        backups[index] = backup
        index += 1
    return backups


def insureBackupHomeExists(backupHome):
    """
    Raise exception if the backup home does not exist.
    """
    if not os.path.exists(backupHome):
        raise Exception("No backups have been made yet.")


def getBackupHome(backupLocation, hostName):
    """
    Gets the home location where all the backups will be stored
    for the provided host.
    """
    return "{1}{0}Backups.backupdb{0}{2}".format(
        os.sep,
        backupLocation,
        hostName)


def getLatestBackup(backupHome):
    """
    Gets the backup directory that the Latest link points to.
    """
    return os.readlink(join(backupHome, "Latest"))


def getLatestLink(backupHome):
    """
    Returns the path and file name of the Latest link.
    """
    return join(backupHome, "Latest")


def updateLatestLink(backupHome):
    """
    Removes the latest link if it exists, then creates a new one that points
    to the most recent backup.
    """
    latest = getLatestLink(backupHome)
    if os.path.lexists(latest):
        os.remove(latest)
    os.symlink(getMostRecentBackup(backupHome), latest)


def getDriveUsagePercentage(directory):
    """
    Gets the percentage of used space on the drive that
    directory lives on.
    """
    s = os.statvfs(directory)
    return 100 - int(((float(s.f_bavail) / s.f_blocks) * 100))


def getMostRecentBackup(backupHome):
    """
    Gets the most recent backup on the backup media.
    """
    backups = getBackups(backupHome)
    if len(backups) > 0:
        return backups[sorted(backups.keys())[-1]]


def getOldestBackup(backupHome):
    """
    Gets the directory name of the oldest backup on the backup media.
    """
    backups = getBackups(backupHome)
    if len(backups) > 0:
        return backups[0]


def getOutputWriter(verbose):
    """
    Returns an output writer based on the boolean value provided.  A console
    writer will be returned if True otherwise a silent writer is returned.
    """
    def _silentWriter(message):
        pass

    def _consoleWriter(message):
        print(message)

    if verbose:
        return _consoleWriter
    else:
        return _silentWriter


def deleteBackup(backupHome, backup):
    """
    Delete the provided backup.
    """
    shutil.rmtree(join(backupHome, backup))


def markBackupForDeletion(backupHome, backup):
    """
    Mark a backup to be deleted later.
    """
    fullBackupName = join(backupHome, backup)
    os.rename(fullBackupName, fullBackupName + ".delete")


def getBackupsMarkedForDeletion(backupHome):
    """
    Get backups that have the .delete extention.
    """
    return [d for d in os.listdir(backupHome) if d.endswith(".delete")]


def getPartialBackups(backupHome):
    """
    Get backups that have the .part extention.
    """
    return [d for d in os.listdir(backupHome)
            if d.endswith(".part")]


def toDateTime(backupDirectory):
    """
    Returns a datetime instance of a backup directory to be used
    in date calculations.
    """
    return datetime.strptime(backupDirectory, "%Y-%m-%d-%H%M%S")


def expandGlob(backupHome, backup, cwd, globPattern):
    """
    Returns a list of glob matches of files and/or directories
    found in the provided backup.  The items returned are absolute
    names.
    """
    backupWorkingDir = join(backupHome, backup) + cwd
    return glob(backupWorkingDir + os.sep + globPattern)


def getGroup(gid):
    """
    Get the group name that belongs to the provided gid.
    """
    return _getNameFromDb(gid, "/etc/group")


def getUser(uid):
    """
    Get the user name that belongs to the provided uid.
    """
    return _getNameFromDb(uid, "/etc/passwd")


def _getNameFromDb(nid, dbFile):
    """
    Gets the name that belongs to the provided id out of the provided system
    database file.
    """
    with open(dbFile, 'r') as f:
        for line in f:
            items = line.split(":")
            if items[2] == str(nid):
                return items[0]


def getInfo(fileSystemItem):
    """
    Takes a file, directory or link and returns its information.
    Items returned are 'size', 'type', 'modified', 'name', 'owner' and 'group'.
    """
    def getType(item):
        if os.path.islink(item):
            return "L"
        elif os.path.isdir(item):
            return "D"
        else:
            return "F"
    return {
        "type": getType(fileSystemItem),
        "size": os.path.getsize(fileSystemItem),
        "modified": datetime.fromtimestamp(os.path.getmtime(fileSystemItem)),
        "name": os.path.basename(fileSystemItem),
        "owner": getUser(os.stat(fileSystemItem).st_uid),
        "group": getGroup(os.stat(fileSystemItem).st_gid)}


def parseWordArgs(args):
    """
    Returns a dictionary of the args for use in lscaat.
    Items returned are 'id', 'glob', and 'as'.
    """
    return {
        "glob": _getGlob(args),
        "id": _getId(args),
        "as": _getAs(args)}


def _getGlob(args):
    """
    Extract the glob value from the args.  Items equal to 'from', or beginning
    with a dash are ignored.
    """
    if len(args) > 0 and args[0] != "from" and not args[0].startswith("-"):
        return args[0]
    else:
        return "*"


def _getId(args):
    """
    Extract the backup id from the args.  Returns the numeric id or the word
    'all' as was provided by the user.
    """
    try:
        index = args.index("from") + 1
        if args[index] == "all":
            return "all"
        elif re.match("^\d+$", args[index + 1]):
            return args[index + 1]
    except (ValueError, IndexError):
        return None


def _getAs(args):
    """
    Extract the 'as' alias as provided by the user.
    """
    try:
        return args[args.index("as") + 1]
    except (ValueError, IndexError):
        return None


def getBackupsForArgs(wordArgs, backups):
    """
    Returns the backups that are being requested from the args.
    """
    if wordArgs["id"] and wordArgs["id"] != "all":
        id_ = int(wordArgs["id"])
        if id_ not in backups:
            raise KeyError("Backup id of {0} not found.".format(id_))
        return {id_: backups[id_]}
    else:
        return backups


def getBackupOrLatest(wordArgs, backupHome):
    """
    Returns the backup provided by the args.  If this arg is
    not provided, the latest backup is returned.
    """
    if wordArgs["id"]:
        id_ = int(wordArgs["id"])
        backups = getBackups(backupHome)
        if id_ not in backups:
            raise KeyError("Backup id of {0} not found.".format(id_))
        return backups[id_]
    else:
        return getLatestBackup(backupHome)


def copy(src, dest):
    """
    Copies an item while preserving permissions and stat.
    """
    try:
        if os.path.islink(src):
            copyLink(src, dest)
        elif os.path.isdir(src):
            copyDir(src, dest)
        elif os.path.isfile(src):
            copyFile(src, dest)
    except OSError as ex:
        if ex.errno == 20:
            raise OSError("Permission Denied")
        else:
            raise ex


def copyLink(src, dest):
    """
    Copies a symbolic link.
    """
    os.symlink(os.readlink(src), dest)


def copyDir(src, dest):
    """
    Recursively copies a directory while preserving
    permissions and stat.
    """
    if os.path.exists(dest) is False:
        os.mkdir(dest)
        shutil.copystat(src, dest)
        copyOwnership(src, dest)
    for item in os.listdir(src):
        srcItem = src + os.sep + item
        destItem = dest + os.sep + item
        if os.path.islink(srcItem):
            copyLink(srcItem, destItem)
        elif os.path.isdir(srcItem):
            copyDir(srcItem, destItem)
        elif os.path.isfile(srcItem):
            copyFile(srcItem, destItem)
    os.utime(dest, (os.path.getatime(src), os.path.getmtime(src)))


def copyFile(src, dest):
    """
    Copies a file while preserving permissions and stat.
    """
    try:
        if stat.S_ISCHR(os.stat(src).st_mode) is False:
            shutil.copy2(src, dest)
            shutil.copystat(src, dest)
            copyOwnership(src, dest)
    except IOError:
        # Normally a permissions problem so the file can't be copied.
        sys.stderr.write("Permission denied: {0}\n".format(src))


def copyOwnership(src, dest):
    """
    Copies user and group information.
    """
    try:
        uid = os.stat(src).st_uid
        gid = os.stat(src).st_gid
        os.chown(dest, uid, gid)
    except OSError:
        # Ownership can't be changed unless you are root
        sys.stderr.write("Unable to copy ownership for {0}\n".format(dest))


def isModified(item1, item2):
    """
    Returns True if the modified date for both items are different.
    """
    item1ModifiedDate = datetime.fromtimestamp(os.path.getmtime(item1))
    item2ModifiedDate = datetime.fromtimestamp(os.path.getmtime(item2))
    return item1ModifiedDate.ctime() != item2ModifiedDate.ctime()


def removeAltRoot(altRoot, item):
    """
    Removes the alternate root path from the item provided.
    """
    if altRoot == "/":
        return item
    return "/" + item[len(altRoot) + 1:]


def isExecutable(file_):
    """
    Returns True if the file is executable.
    """
    return os.access(file_, os.X_OK)


def getExecutableFiles(directory):
    """
    Returns a list of file that include the absolute path.  Files are returned
    in alphabetical order.
    """
    files = []
    for item in os.listdir(directory):
        file_ = join(directory, item)
        if os.path.isfile(file_) and isExecutable(file_):
            files.append(file_)
    files.sort()
    return files
