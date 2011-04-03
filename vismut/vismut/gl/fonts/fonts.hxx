
#ifndef VISMUT_GL_FONTS_FONTS_HXX
#define VISMUT_GL_FONTS_FONTS_HXX

#include <memory>
#include <string>
#include <exception>

#include <boost/python.hpp>

#include <ft2build.h>
#include FT_FREETYPE_H

#include "errors.hxx"

namespace bi
{
  namespace py = boost::python;

  inline void
  check (FT_Error error)
    throw (std::runtime_error)
  {
    if (!error)
      {
	return;
      }

    throw std::runtime_error ("FreeType error: " + error_map[error]);
  }


  py::object
  make_font_texture (FT_Library library,
		     std::string filename,
		     unsigned long face,
		     unsigned int size);

  class
  FreeType
  {
  public:
    FreeType ()
    {
      check (FT_Init_FreeType (&library_));
    }

    ~FreeType ()
    {
      check (FT_Done_FreeType (library_));
    }

    FT_Library
    get ()
    {
      return library_;
    }

    py::object
    font_texture (std::string filename,
		  unsigned long face,
		  unsigned int size)
    {
      return make_font_texture (library_, filename, face, size);
    }

  private:
    FT_Library library_;
  };
}

#endif // VISMUT_GL_FONTS_FONTS_HXX
