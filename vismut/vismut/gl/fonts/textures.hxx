
#ifndef VISMUT_GL_FONTS_TEXTURES_HXX
#define VISMUT_GL_FONTS_TEXTURES_HXX

#include <string>

#include <boost/python.hpp>

#include "faces.hxx"

namespace bi
{
  namespace py = boost::python;

  void
  init_numpy ();

  py::object
  make_font_texture (FT_Library library,
		     std::string filename,
		     unsigned long face,
		     unsigned int size);
}

#endif // VISMUT_GL_FONTS_TEXTURES_HXX
