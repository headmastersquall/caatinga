#!/usr/bin/env python

# Copyright 2015 Chris Taylor
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
import caatinga.caat_main

try:
    from setuptools import setup
except ImportError:
    print("setuptools module not found.  Run python ez_setup.py first.")
    from sys import exit
    exit(1)


os.system("gzip docs/*.[15]")

setup(
    author="Chris Taylor",
    author_email="headmastersquall@gmail.com",
    url="https://github.com/headmastersquall/caatinga",
    description="A backup program that creates multiple snapshots of a file system.",
    long_description="",
    fullname="caatinga",
    keywords=["backup", "restore", "Linux", "FreeBSD",
              "snapshot", "history", "python"],
    name="caatinga",
    platforms=["Linux", "FreeBSD"],
    version=caatinga.caat_main.__version__,
    license="GNU GENERAL PUBLIC LICENSE Version 3",
    entry_points={
        'console_scripts': [
            'caat = caatinga.caat_main:main',
            'lscaat = caatinga.lscaat_main:main']},
    packages=['caatinga', 'caatinga.core', 'caatinga.caat', 'caatinga.lscaat'],
    data_files=[('/etc/caatinga', ['caatinga.conf.sample']),
                ('/etc/caatinga/pre_backup_hooks', []),
                ('/etc/caatinga/post_backup_hooks', []),
                ('/etc/caatinga/pre_restore_hooks', []),
                ('/etc/caatinga/post_restore_hooks', []),
                ('/usr/share/man/man1', ["docs/lscaat.1.gz", "docs/caat.1.gz"]),
                ("/usr/share/man/man5", ["docs/caatinga.conf.5.gz"])],
    test_suite="caatinga.tests",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Archiving :: Backup"])

os.system("gunzip docs/*.[15].gz")

