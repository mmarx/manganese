######################################################################
# manganese - midi analysis & visualization platform
# Copyright (c) 2010, 2011 Maximilian Marx <mmarx@wh2.tu-dresden.de>
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
######################################################################



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
