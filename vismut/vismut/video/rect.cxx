/*********************************************************************
 * manganese - midi analysis & visualization platform
 * Copyright (c) 2010, 2011 Maximilian Marx <mmarx@wh2.tu-dresden.de>
 * 
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2 of
 * the License, or (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
 * 02110-1301 USA.
 ********************************************************************/


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
