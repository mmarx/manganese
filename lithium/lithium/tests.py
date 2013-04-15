########################################################################
# manganese - midi analysis & visualization platform
# Copyright (c) 2010, 2011, 2013 Maximilian Marx <mmarx@wh2.tu-dresden.de>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA.
########################################################################



import unittest


from lindenmayer.rule import Rule
from lindenmayer import LSystem


class LTest(unittest.TestCase):
    def _it(self, iteration, output):
        assert self.L.iterate(iteration) == output


class AlgaeTest(LTest):
    def setUp(self):
        self.L = LSystem("a", [Rule("a", "ab"),
                               Rule("b", "a")])

    def test0(self):
        self._it(0, "a")

    def test1(self):
        self._it(1, "ab")

    def test2(self):
        self._it(2, "aba")

    def test3(self):
        self._it(3, "abaab")

    def test4(self):
        self._it(4, "abaababa")

    def test5(self):
        self._it(5, "abaababaabaab")


class FiboTest(LTest):
    def setUp(self):
        self.L = LSystem("a", [Rule("a", "b"),
                               Rule("b", "ab")])

    def test0(self):
        self._it(0, "a")

    def test1(self):
        self._it(1, "b")

    def test2(self):
        self._it(2, "ab")

    def test3(self):
        self._it(3, "bab")

    def test4(self):
        self._it(4, "abbab")

    def test5(self):
        self._it(5, "bababbab")

algae_suite = unittest.makeSuite(AlgaeTest, "test")
fibo_suite = unittest.makeSuite(FiboTest, "test")
suites = unittest.TestSuite([algae_suite, fibo_suite])

if __name__ == "__main__":
    unittest.main()
