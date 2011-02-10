
#include <boost/python.hpp>

namespace ut
{
  namespace py = boost::python;

  py::object
  test ()
  {
    return py::string ("Hello, World!");
  }

  BOOST_PYTHON_MODUILE (_utabor)
  {
    using namespace boost::python;

    def ("test", test);
  }
}
