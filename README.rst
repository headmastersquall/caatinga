Caatinga is a command line backup tool that creates multiple snapshots of your
file system to preserve the history of your data.

To make a backup of your system simply run:

   ``$ caat``


To view data in your backups, use the lscaat utility:

    ``$ lscaat ls``

To Restore a backed up file from a specific backup:

    ``$ lscaat restore hello.clj from backup 1``

To restore from the most recent backup:

    ``$ lscaat restore hello.clj``


**Features:**

* Settings are read from a configuration file for ease of use.

* Backups are fast and consume a small amount of space by using hard links.

* Backup images can be stored on any mounted media that contains a file system
  which supports hard links (eg. ext4).

* Remote file systems can be used via sshfs for pushing backups to a remote
  server.

* Manage, view, and restore data using a single freindly command.

* Data is stored in raw format just as it appeared on the original file system
  allowing you to browse or copy data without using a special tool.

* Permissions, ownership and access times are preserved.

* Pre/Post Backup/Restore hooks can be put in place for more advanced needs.

* Finding help is available within the commands and via standard man pages.


**Installation:**

    ``pip install caatinga``


**Contribute:**

* Issue Tracker: https://github.com/headmastersquall/caatinga/issues
* Source Code: https://github.com/headmastersquall/caatinga


**Support:**

* If you are having issues, please create an item in the issue tracker.  To
  reach me via email, my address can be found within the man pages.


**License:**

* The project is licensed under the GNU General Public License Version 3.
