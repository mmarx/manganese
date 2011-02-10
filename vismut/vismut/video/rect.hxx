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


#ifndef BI_RECT_HXX
#define BI_RECT_HXX

#include <string>
#include <ostream>

#include <SDL.h>

std::ostream&
operator<< (std::ostream&, SDL_Rect);

namespace bi
{
  namespace rect
  {
    std::string
    rect_repr (SDL_Rect rect);

    int
    rect_size (SDL_Rect rect);
  }
}

#endif // not BI_RECT_HXX
