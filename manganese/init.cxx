/* manganese - mutabor-ng platform runner
 * Copyright (c) 2010, Maximilian Marx <mmarx@wh2.tu-dresden.de>
 *
 * Permission to use, copy, modify, and/or distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */

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
