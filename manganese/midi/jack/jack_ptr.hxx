/***********************************************************************
 * manganese - midi analysis & visualization platform
 * Copyright (c) 2010, 2011, 2013 Maximilian Marx <mmarx@wh2.tu-dresden.de>
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
 **********************************************************************/

#ifndef MANGANESE_MIDI_JACK_PTR_HXX
#define MANGANESE_MIDI_JACK_PTR_HXX

#include <boost/shared_ptr.hpp>

#include <jack/jack.h>

namespace mn
{
  template<typename T>
  struct
  jack_deleter
  {
    jack_deleter () throw () {}
    jack_deleter (jack_deleter const& other) throw () {}
    ~jack_deleter () throw () {}

    void
    operator () (T* ptr) throw ()
    {
      jack_free (ptr);
    }
  };

  template<typename T>
  boost::shared_ptr<T>
  shared_jack_ptr (T* ptr)
  {
    return boost::shared_ptr<T> (ptr, jack_deleter<T> ());
  };
}

#endif // MANGANESE_MIDI_JACK_PTR_HXX
