# lithium - mutabor-ng platform l-systems generator
# Copyright (c) 2010, Maximilian Marx <mmarx@wh2.tu-dresden.de>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

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
