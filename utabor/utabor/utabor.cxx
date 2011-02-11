
#include <boost/python.hpp>

#include "runtime.hxx"

namespace ut
{
  namespace py = boost::python;

  py::object
  test ()
  {
    if (Compile (0, "/home/mmarx/proj/remote/mutabor/MUT_GER/Demo.mut"))
      {
	// success
	return py::str ("success");
      }

    return py::str ("failure");
  }

  BOOST_PYTHON_MODULE (_utabor)
  {
    using namespace boost::python;

    def ("test", test);
  }
}
