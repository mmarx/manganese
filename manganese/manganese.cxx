/*********************************************************************
 * manganese - midi analysis & visualization platform
 * Copyright (c) 2010, 2011 Maximilian Marx <mmarx@wh2.tu-dresden.de>
 * 
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2 of
 * the License, or (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
 * 02110-1301 USA.
 ********************************************************************/


#include <string>
#include <iostream>

#include "config.hxx"
#include "init.hxx"

int
main (int argc, char** argv)
{
  using std::cerr;
  using std::endl;
  using std::string;

  if (argc < 2)
    {
      cerr << "usage: " << argv[0] << " COMPONENT [OPTION...]" << endl;
      return 1;
    }

  mn::init_python ();
  mn::exec_python (string ("print 'Hello, World (from embedded python)!'"));
  mn::bootstrap (argc, argv);

  return 0;
}
