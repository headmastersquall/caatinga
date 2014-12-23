Caatinga
========

## Introduction
Backup program written in python.

Have you ever accidentally deleted a file or unintentionally saved changes
you didn't want to save?  Or maybe you would like to look back in time to
find a particular version of a file you once had.  Caatinga is an easy to use
command line backup and restore tool that creates snapshots of your filesystem
and allows easy recovery of your precious data.

When new snapshots are created, Caatinga uses hard links instead of copying
files that have not changed since the last backup.  This makes each backup
take a minimal amount of disk space and they execute very quickly.  Since a
new snapshot can be created efficiently, frequent backups can be performed
using a command scheduler, such as cron, to insure current data is always
backed up.

If remote backups are desired, a filesystem from a remote computer can be
mounted locally using http://fuse.sourceforge.net/sshfs.html.  This requires
a remote machine to have an SSH daemon running and a user account available
for backup purposes.

Caatinga is compatible with python versions 2.6 or newer, including 3.x.


## Installation

### PyPI
Installing from the Python Package Index can be done by using the pip command.
This is the recommended way to install Caatinga.

`$ pip install caatinga`

### Archlinux
If you are using Archlinux there's an AUR package available:
https://aur.archlinux.org/packages/caatinga/

### Source
Installing from source will insure you have the most current code base.  In
order to run the installer, you must first have the python setuptools package
installed.  To get the latest source code, clone the git repository with this
command.

`# git clone https://www.github.com/headmastersquall/caatinga`

Change to the caatinga directory that was just created, then run the install
as root.

`$ python setup.py install`

After Caatinga has been installed, it will need to be configured before you
make your first backup.  Lets walk through a few items in the configuration
file to prepare for your first backup.


## Quick Setup
This section walks you through the minimal configuration steps you will need
to perform before creating your first backup.

  1.  Install the caatinga using one of the methods mentioned above.

  2.  Rename the sample configuration file located in /etc/caatinga.
      ```
      $ cd /etc
      $ mv caatinga.conf.sample caatinga.conf
      ```

  3.  Edit the configuration file and set the `backup_location` to where you
      want your snapshots to be stored.  This can be any location on your
      filesystem, but is highly recommended to be a mounted filesystem such
      as an internal drive for backup use, or an external usb drive.

  4.  Optionally set the `backup_group` to a group defined on your system for
      use as the backup group.  Backups will be owned by this group to allow
      normal users to access their backed up files.  Remember to add the users
      to this group as well.

  5.  Make sure your backup location is mounted and ready.

  6.  Register the `backup_location`, found in caatinga.conf, as a backup
      device to be used by caatinga.

      `caat -g`

  7.  Run `caat` from the console to create your first backup.

Note: The first backup that is performed will take the most time since it has to
copy all your data to the backup location.  After the first backup is
completed, subsequent backups will complete much quicker.


## Documentation
Full docs are available at https://github.com/headmastersquall/caatinga/wiki.
Don't forget about your trusty docs that are installed with the application,
such as man pages and the built in help system found in lscaat:

  * man caat(1)
  * man lscaat(1)
  * man caat.conf(5)
  * caat --help
  * lscaat help


I hope you enjoy this program as much as I have enjoyed writing it.
If you find any bugs or have any comments or suggestions, please post them at
https://github.com/headmastersquall/caatinga/issues.

