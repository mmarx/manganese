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

class LSystem(object):

    def __init__(self, axiom, productions):
        self.axiom = axiom
        self.productions = productions

    def __repr__(self):
        return ("<L-System with Axiom %s "
                "and Productions %s>" % (self.axiom, self.productions))

    def _iterate(self, string):
        output = ''
        for position in range(0, len(string)):
            for rule in self.productions:
                if string.startswith(rule.lhs, position):
                    output += rule.rhs
                    break
            else:
                # no rule applicable, just copy
                output += string[position]
            
        return output

    def iterate(self, depth):
        string = self.axiom
        for i in range(0, depth):
            string = self._iterate(string)
            
        return string
