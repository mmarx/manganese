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


#ifndef VISMUT_VIDEO_VIDEO_HXX
#define VISMUT_VIDEO_VIDEO_HXX

#include <boost/python.hpp>

#include <SDL.h>

namespace bi
{
  class SDLContext
  {
  public:
    SDLContext ();
    ~SDLContext ();

    unsigned int
    users ()
    {
      return users_;
    }

    void
    set_mode (boost::python::object mode);

    char const*
    error_string () const;

    bool
    have_error () const
    {
      return error_;
    }

    void
    flag_error ()
    {
      error_ = true;
    }

    void
    call (int ret);

  private:
    static bool error_;
    static unsigned int users_;
    SDL_Surface* surface_;
  };
}

#endif // VISMUT_VIDEO_VIDEO_HXX
