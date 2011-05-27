
#ifndef VISMUT_GL_FONTS_FACES_HXX
#define VISMUT_GL_FONTS_FACES_HXX

#include <string>

#include <ft2build.h>
#include FT_FREETYPE_H

#include "fonts.hxx"
#include "textures.hxx"

namespace bi
{
  class Face
  {
  public:
    Face (FT_Library library,
	  std::string filename,
	  unsigned long face = 0)
    {
      check (FT_New_Face (library,
			  filename.c_str (),
			  face,
			  &face_));
    }

    ~Face()
    {
      check (FT_Done_Face (face_));
    }

    FT_Face
    get ()
    {
      return face_;
    }

    void
    size (long height,
	  long width = 0)
    {
      check (FT_Set_Pixel_Sizes (face_,
				 width,
				 height));
    }

  protected:
    FT_Face face_;
  };
}

#endif // VISMUT_GL_FONTS_FACES_HXX
