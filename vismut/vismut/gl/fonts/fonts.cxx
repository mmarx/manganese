
#include <memory>

#include <boost/python.hpp>

#include <ft2build.h>
#include FT_FREETYPE_H

#include "fonts.hxx"

namespace bi
{
  FreeType*
  init_freetype ()
  {
    return new FreeType ();
  }

  void
  destroy_freetype (std::auto_ptr<FreeType> library)
  {
    library.reset ();
  }

  BOOST_PYTHON_MODULE (_fonts)
  {
    using namespace boost::python;

    def ("init_freetype",
	 init_freetype,
	 return_value_policy<manage_new_object> ());
    def ("destroy_freetype",
	 destroy_freetype);
  }
}
