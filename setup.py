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
from setuptools import setup

os.system("gzip docs/*")

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
    version="1.0.2",
    license="GNU GENERAL PUBLIC LICENSE Version 3",
    scripts=["caat", "lscaat"],
    packages=['caatinga', 'caatinga.core', 'caatinga.caat', 'caatinga.lscaat'],
    data_files=[('/etc/caatinga', ['caatinga.conf.sample']),
			    ('/etc/caatinga/pre_hooks', []),
			    ('/etc/caatinga/post_hooks', []),
                ('/usr/share/man/man1', ["docs/lscaat.1.gz", "docs/caat.1.gz"]),
                ("/usr/share/man/man5", ["docs/caatinga.conf.5.gz"])],
    package_data={'caatinga': ['README.md', 'COPYING']})

os.system("gunzip docs/*")
