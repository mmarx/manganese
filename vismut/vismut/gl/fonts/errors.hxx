
#ifndef VISMUT_GL_FONTS_ERRORS_HXX
#define VISMUT_GL_FONTS_ERRORS_HXX

#include <map>
#include <string>

#include <ft2build.h>
#include FT_FREETYPE_H

namespace bi
{
  using std::map;
  using std::string;

  extern
  map<FT_Error, string> error_map;

  void
  build_error_map ();
}

#endif // VISMUT_GL_FONTS_ERRORS_HXX
