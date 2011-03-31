
#ifndef VISMUT_GL_FONTS_FONTS_HXX
#define VISMUT_GL_FONTS_FONTS_HXX

namespace bi
{
  class
  FreeType
  {
  public:
    FreeType ()
    {
      FT_Init_FreeType (&library_);
    }

    ~FreeType ()
    {
      FT_Done_FreeType (library_);
    }

    FT_Library
    get ()
    {
      return library_;
    }

  private:
    FT_Library library_;
  };
}

#endif // VISMUT_GL_FONTS_FONTS_HXX
