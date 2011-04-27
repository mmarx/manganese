
#include "errors.hxx"

namespace bi
{
  map<FT_Error, string> error_map;

  void
  build_error_map ()
  {
#undef __FTERRORS_H__
#define FT_ERRORDEF(e, v, s) error_map[ v ] = s ;
#define FT_ERROR_START_LIST {
#define FT_ERROR_END_LIST }
#include FT_ERRORS_H
  }
}
