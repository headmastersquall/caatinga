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

import unittest
import context
from caatinga.lscaat import help as lscaatHelp


class HelpTestCase(unittest.TestCase):

    def test_listHelp(self):
        self.assertTrue(self.isListHelp(lscaatHelp._list))

    def isListHelp(self, method):
        return method([]).count("list") > 0

    def test_removeHelp(self):
        self.assertTrue(self.isRemoveHelp(lscaatHelp._remove))

    def isRemoveHelp(self, method):
        return method([]).count("remove") > 0

    def test_restoreHelp(self):
        self.assertTrue(self.isRestoreHelp(lscaatHelp._restore))

    def isRestoreHelp(self, method):
        return method([]).count("restore") > 0

    def test_infoHelp(self):
        self.assertTrue(self.isInfoHelp(lscaatHelp._info))

    def isInfoHelp(self, method):
        return method([]).count("info") > 0

    def test_changes(self):
        self.assertTrue(self.isChangesHelp(lscaatHelp._changes))

    def isChangesHelp(self, method):
        return method([]).count("changes") > 0

    def test_diff(self):
        self.assertTrue(self.isDiffHelp(lscaatHelp._diff))

    def isDiffHelp(self, method):
        return method([]).count("diff") > 0

    def test_unknown(self):
        self.assertTrue(self.isUnknown(lscaatHelp._unknown))

    def isUnknown(self, command):
        return command(["foo"]) == '"foo": unknown command.'

    def test_usage(self):
        self.assertTrue(self.isUsage(lscaatHelp._usage))

    def isUsage(self, method):
        return method([]).count("usage") > 0

    def test_getHelpMethodFor_list(self):
        self.assertTrue(self.isListHelp(lscaatHelp._getHelpMethod("list")))

    def test_getHelpMethodFor_ls(self):
        self.assertTrue(self.isListHelp(lscaatHelp._getHelpMethod("ls")))

    def test_getHelpMethodFor_remove(self):
        self.assertTrue(self.isRemoveHelp(lscaatHelp._getHelpMethod("remove")))

    def test_getHelpMethodFor_rm(self):
        self.assertTrue(self.isRemoveHelp(lscaatHelp._getHelpMethod("rm")))

    def test_getHelpMethodFor_restore(self):
        self.assertTrue(
            self.isRestoreHelp(lscaatHelp._getHelpMethod("restore")))

    def test_getHelpMethodFor_info(self):
        self.assertTrue(self.isInfoHelp(lscaatHelp._getHelpMethod("info")))

    def test_getHelpMethodFor_changes(self):
        self.assertTrue(
            self.isChangesHelp(lscaatHelp._getHelpMethod("changes")))

    def test_getHelpMethodFor_diff(self):
        self.assertTrue(self.isDiffHelp(lscaatHelp._getHelpMethod("diff")))

    def test_getHelpMethodFor_usage(self):
        self.assertTrue(self.isUsage(lscaatHelp._getHelpMethod("")))

    def test_getHelpMethodFor_unknown(self):
        self.assertTrue(self.isUnknown(lscaatHelp._getHelpMethod("foo")))

if __name__ == '__main__':
    unittest.main()
