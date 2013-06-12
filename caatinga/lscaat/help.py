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

_NAME = "NAME"
_SYNOPSIS = "SYNOPSIS"
_DESCRIPTION = "DESCRIPTION"
_OPTIONS = "OPTIONS"


def help_(args, settings):
    """
    Main function for the help option.
    """
    arg = ""
    if len(args) > 0:
        arg = args[0]
    command = _getHelpMethod(arg)
    print(command(args))


def _getHelpMethod(command):
    """
    Gets the help method for the provided command.
    """
    commandMethods = {
        "list": _list,
        "ls": _list,
        "remove": _remove,
        "rm": _remove,
        "restore": _restore,
        "info": _info,
        "changes": _changes,
        "diff": _diff,
        "": _usage
    }
    return commandMethods.get(command, _unknown)


def _usage(args):
    """
    Gets usage help content.
    """
    usage = [
        "usage: lscaat <subcommand> [args] [options]",
        "",
        "Type lscaat help <subcommand> for help on a specific subcommand.",
        "Type caat --help for help on command options.",
        "",
        "Available subcommands:",
        "",
        "  changes",
        "  diff",
        "  info",
        "  list (ls)",
        "  remove (rm)",
        "  restore",
        "",
        "Options:",
        "",
        "  Several command options exist that are the same as found in caat.",
        "  Consult the man pages for lscaat for details.",
        "",
        "lscaat is a part of the caat backup program and is used to restore,",
        "list and remove items from one or more backups.  Can also be used",
        "to display useful information about the status of your backups."]
    return "\n".join(usage)


def _list(args):
    """
    Gets help content for the list command.
    """
    return _formatHelp({
        _NAME:
        ["list -- list backed up items from the current directory"],

        _SYNOPSIS:
        ["list [item] <from backup> <id>"],

        _DESCRIPTION:
        ["Lists files and directories from the backup device that were ",
         "backed up from the current working directory.  Items listed ",
         "include the Backup id, owner, group, file size, last modified ",
         "date, and the name.  If a backup id is not provided, items are ",
         "listed from the most recent backup."],

        _OPTIONS:
        ["item         File or directory to be listed.  Can be glob pattern.",
         "from backup  Only list items from the specified backup id.",
         "id           Id number of a backup."]})


def _remove(args):
    """
    Gets help content for the remove command.
    """
    return _formatHelp({
        _NAME:
        ["remove -- delete items from the backup drive"],

        _SYNOPSIS:
        ["remove [item] [from all]",
         "remove [item] [from backup] [id]"],

        _DESCRIPTION:
        ["Remove backed up files or directories from the backup device.  ",
         "Items can be deleted from one or all backups."],

        _OPTIONS:
        ["item         File or directory to be removed.  Can be glob pattern.",
         "from all     Items are removed from all backups.",
         "from backup  Items are removed from a specified backup id.",
         "id           Id number of a backup."]})


def _restore(args):
    """
    Gets help content for the restore command.
    """
    return _formatHelp({
        _NAME:
        ["restore -- restore items from a backup"],

        _SYNOPSIS:
        ["restore [item] <from backup> <id>",
         "restore [item] <from backup> <id> <as> <filename>"],

        _DESCRIPTION:
        ["Restore files or directories from a backup to the current working",
         "directory.  If only one item is to be restored, an optional ",
         "destination file name can be provided using the as keyword.  If ",
         "no backup id is provided, items are restored from the most recent ",
         "backup."],

        _OPTIONS:
        ["item         File or directory to restore.  Can be glob pattern.",
         "from backup  Items are restored from a specified backup id.",
         "id           Id number of a backup.",
         "as           Used to restore an item as a different file name.",
         "filename     Restore as this name instead of the original."]})


def _info(args):
    """
    Gets help content for the info command.
    """
    return _formatHelp({
        _NAME:
        ["info -- display information about the backup device"],

        _SYNOPSIS:
        ["info"],

        _DESCRIPTION:
        ["Provides information about the backup device, such as: its ",
         "location, hostname the number of backups made for this system, ",
         "date of the last backup and the percentage of free space on the ",
         "drive."],

        _OPTIONS:
        ["none"]})


def _changes(args):
    """
    Gets help content for the changes command.
    """
    return _formatHelp({
        _NAME:
        ["changes -- show changes compared to the most recent backup"],

        _SYNOPSIS:
        ["changes <from backup> <id>"],

        _DESCRIPTION:
        ["Show files and directories that have changed, are new, or have ",
         "been deleted since the last backup was made.  An optional backup ",
         "id can be provided to compare against instead of the latest ",
         "backup."],

        _OPTIONS:
        ["from backup  Items are compared from a specified backup id.",
         "id           Id number of a backup."]})


def _diff(args):
    """
    Gets help content for the diff command.
    """
    return _formatHelp({
        _NAME:
        ["diff -- show the difference between two files"],

        _SYNOPSIS:
        ["diff [file] <from backup> <id>"],

        _DESCRIPTION:
        ["Show the differences between the provided file compared to the ",
         "version from the last backup.  An optional backup id can be ",
         "provided in order to compare against a specific backed up version."],
        #TODO: "An alternate diff program can also be defined in the caat.conf
        #configuration file."

        _OPTIONS:
        ["file         Name of the file to perform the comparison with",
         "from backup  Specify which backup id to look at to compare against",
         "id           Id number of a backup."]})


def _formatHelp(content):
    """
    Formats the help content for readable output.
    """
    def formatItem(header, content):
        return header + "\n" + "\n".join("  " + c for c in content) + "\n"

    sections = [
        formatItem(_NAME, content[_NAME]),
        formatItem(_SYNOPSIS, content[_SYNOPSIS]),
        formatItem(_DESCRIPTION, content[_DESCRIPTION]),
        formatItem(_OPTIONS, content[_OPTIONS])]
    return "\n".join(sections)


def _unknown(args):
    """
    Returns string indicating the provided command is unknown.
    """
    return '"{0}": unknown command.'.format(args[0])
