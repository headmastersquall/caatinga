Caatinga
========

## Introduction
Backup program written in python.

A backup program used for making full system backups to locally mounted media.
Each time a backup is performed, a new snapshot of the file system is created.
This creates a history of all files on your system allowing you to restore
files from any point in time.  Snapshots are created using hard links, making
each backup takes a minimal amount of disk space and time to execute.  This
efficiency allows backups to be ran frequently in a command scheduler to
insure current data is always backed up.

If remote backups are desired, a filesystem from a remote computer can be
mounted locally using http://fuse.sourceforge.net/sshfs.html.  This requires
a remote machine to have ssh running and a user account defined that will be
used for backup purposes.

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

  * man mime(1)
  * man lsmime(1)
  * man mime.conf(5)
  * mime --help
  * lsmime help


I hope you enjoy this program as much as I have enjoyed writing it.
If you find any bugs or have any comments or suggestions, please email
me at (headmastersquall at gmail dot com) and include caatinga in the subject line.
