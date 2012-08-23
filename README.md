caatinga
========

Backup program written in python.

Thank you for downloading the caatinga backup and restore program.  This program is
written in python and is compatible with version 2.6 or newer, including 3.x.
caatinga is used to perform complete system backups and keeps old backups to 
maintain history of your file system changes.  The backups execute quicky and
use a small amount of disk space.  The lscaat program is used to view, restore
and manage files that have been backed up.


Quick Setup:

  1.  As root, run the command 'python setup.py install' to install the program.

  2.  Rename the sample configuration file

      cd /etc/caatinga
      mv caatinga.conf.sample caatinga.conf

  3.  Edit the configuration file and set the backup_location.

  4.  Optionally set the backup_group to allow normal users to access their 
      backed up files

  5.  Make sure your backup drive is mounted.

  6.  Register the backup_location, found in caatinga.conf, as a backup device to 
      be used by caatinga.

      caat -g

  7.  Run caat from the console.


Further help and documentation can be found in several man pages as well as the
built in help system found in lscaat:

  man caat(1)
  man lscaat(1)
  man caat.conf(5)
  caat -h
  lscaat help


I hope you enjoy this program as much as I have enjoyed writing it.
If you find any bugs or have any comments or suggestions, please email
me at headmastersquall@gmail.com and include caatinga in the subject line.
