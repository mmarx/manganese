
#include <boost/python.hpp>

#include "fonts.hxx"
#include "faces.hxx"

namespace bi
{
  FreeType*
  init_freetype ()
  {
    build_error_map ();
    return new FreeType ();
  }

  void
  destroy_freetype (std::auto_ptr<FreeType> library)
  {
    library.reset ();
  }

  BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(face_size_overloads,
					 size, 1, 2);

  BOOST_PYTHON_MODULE (_fonts)
  {
    using namespace boost::python;

    init_numpy ();

    def ("init_freetype",
	 init_freetype,
	 return_value_policy<manage_new_object> ());
    def ("destroy_freetype",
	 destroy_freetype);

    class_<FreeType> ("FreeType", no_init)
      .def ("make_font_texture", &FreeType::font_texture);
  }
}
