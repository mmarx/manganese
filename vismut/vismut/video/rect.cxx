/* vismut - mutabor-ng platform visualization
 * Copyright (c) 2010, Maximilian Marx <mmarx@wh2.tu-dresden.de>
 *
 * Permission to use, copy, modify, and/or distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */

#include <boost/format.hpp>
#include <boost/lexical_cast.hpp>

#include "rect.hxx"

using std::ostream;

ostream&
operator<< (ostream& stream, SDL_Rect rect)
{
  using boost::format;

  stream << (format ("<SDLRect %dx%d+%d+%d>")
	     % rect.w % rect.h % rect.x % rect.y);

  return stream;
}

namespace bi
{
  namespace rect
  {
    using std::string;
    using boost::lexical_cast;

    string
    rect_repr (SDL_Rect rect)
    {
      return lexical_cast<string> (rect);
    }

    int
    rect_size (SDL_Rect rect)
    {
      return rect.w * rect.h;
    }
  }
}
