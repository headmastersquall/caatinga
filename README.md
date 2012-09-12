Caatinga
========

## Introduction
Backup program written in python.

This program creates full system backups to locally mounted media.  Each backup
that is performed creates a new snapshot of the filesystem.  This will build a
history of all your files and allows you to restore files from any point in
time.  Snapshots are created using hard links.  This makes each backup take a
minimal amount of disk space and time to execute.  Since a new snapshot can be
created efficiently, they can be ran frequently in a command scheduler, such as
cron, to insure current data is always backed up.

If remote backups are desired, a filesystem from a remote computer can be
mounted locally using http://fuse.sourceforge.net/sshfs.html.  This requires
a remote machine to have an SSH daemon running and a user account available for
backup purposes.

This program is compatible with python versions 2.6 or newer, including 3.x.

## Installation

### Archlinux
If you are using Archlinux there's an aur package available:
https://aur.archlinux.org/packages.php?ID=62708

### Quick Setup
After downloading the package from the downloads page and extracting it, or
by cloning the repository, follow these instructions to get setup.

  1.  As root, run the command `python setup.py install` to install the program.

  2.  Rename the sample configuration file

      `cd /etc/caatinga`
      `mv caatinga.conf.sample caatinga.conf`

  3.  Edit the configuration file and set the `backup_location`.

  4.  Optionally set the `backup_group` to allow normal users to access their
      backed up files

  5.  Make sure your backup drive is mounted.

  6.  Register the `backup_location`, found in caatinga.conf, as a backup device to
      be used by caatinga.

      `caat -g`

  7.  Run caat from the console.


## Documentation
Further help and documentation can be found in several man pages as well as the
built in help system found in lscaat:

  * man caat(1)
  * man lscaat(1)
  * man caat.conf(5)
  * caat --help
  * lscaat help


I hope you enjoy this program as much as I have enjoyed writing it.
If you find any bugs or have any comments or suggestions, please email
me at (headmastersquall at gmail dot com) and include caatinga in the subject line.
