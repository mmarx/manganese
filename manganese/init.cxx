/***********************************************************************
 * manganese - midi analysis & visualization platform
 * Copyright (c) 2010, 2011, 2013 Maximilian Marx <mmarx@wh2.tu-dresden.de>
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
 **********************************************************************/


#include <boost/python.hpp>

#include "config.hxx"
#include "init.hxx"

namespace mn
{
  using std::string;

  static char const* py_argv[] = {"mng"};

  void
  init_python ()
  {
    Py_InitializeEx (0);
    PySys_SetArgv (1, const_cast<char**> (py_argv));

    // remove the current working directory from sys.path
    exec_python ("import sys; sys.path.pop(0)");
    // ... and add python_prefix to it
    exec_python (string ("import sys; sys.path.append('")
		 + config::python_prefix + "')");
  }

  void
  exec_python (string const& code)
  {
    using namespace boost::python;

    try
      {
	object main = import ("__main__");
	object dict = main.attr ("__dict__");
	object ignored = exec (code.c_str(), dict, dict);
      }
    catch (error_already_set const&)
      {
	PyErr_Print ();
      }
  }

  void
  bootstrap (int argc, char** argv)
  {
    using namespace boost::python;

    list args;
    string app = argv[1];

    for (int i = 1; i < argc; ++i)
      {
	args.append (string (argv[i]));
      }

    try
      {
	object main = import ("__main__");
	object dict = main.attr ("__dict__");
	dict["args"] = args;
      }
    catch (error_already_set const&)
      {
	PyErr_Print ();
      }

    exec_python (string ("import manganese.apps.") + app + " as app\n"
		 "the_app = app.Application(args)\n"
		 "the_app.run()");
  }
};
