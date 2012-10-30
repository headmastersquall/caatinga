Caatinga
========

## Introduction
Backup program written in python.

This program creates full system backups to locally mounted media.  Each backup
that is performed creates a new snapshot of the filesystem.  This will build a
history of all your files and allows you to restore data from any point in
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

### Source
Installing from source will insure you have the most current code base.  First
clone the git repository.

`# git clone https://www.github.com/headmastersquall/caatinga`

Change to the caatinga directory that was just created, then run the install as
root.

`$ python setup.py install`

### Download
If you don't have git installed on your computer, download the repository as a
zip file located at the top of the main page.  After the download completes,
unzip the archive and cd into the extracted directory.  Then run the install
program.

`$ python setup.py install`

After you have installed the package from one of the previous methods, it will
need to be configured before you make your first backup.  The next section will
walk you though configuring caatinga to backup your system.


## Quick Setup
This section walks you through the minimal configuration steps you will need to
perform before creating your first backup.

  1.  Install the caatinga using one of the methods mentioned above.

  2.  Rename the sample configuration file located in /etc/caatinga.

      `$ mv caatinga.conf.sample caatinga.conf`

  3.  Edit the configuration file and set the `backup_location` to where you
      want your snapshots to be stored.  This must be a mounted filesystem such
      as an internal drive for backup use, or an external usb drive.

  4.  Optionally set the `backup_group` to allow normal users to access their
      backed up files.  Remember to add the users to this group as well.

  5.  Make sure your backup drive is mounted.

  6.  Register the `backup_location`, found in caatinga.conf, as a backup device to
      be used by caatinga.

      `caat -g`

  7.  Run `caat` from the console to create your first backup.


## Documentation
Further help and documentation can be found in several man pages as well as the
built in help system found in lscaat:

  * man caat(1)
  * man lscaat(1)
  * man caat.conf(5)
  * caat --help
  * lscaat help


I hope you enjoy this program as much as I have enjoyed writing it.
If you find any bugs or have any comments or suggestions, please post them at
https://github.com/headmastersquall/caatinga/issues.
