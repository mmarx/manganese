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


#ifndef MANGANESE_MIDI_JACK_CLIENT_HXX
#define MANGANESE_MIDI_JACK_CLIENT_HXX

#include <boost/shared_ptr.hpp>
#include <boost/python.hpp>

#include <jack/jack.h>

#include "port.hxx"
#include "midi_event.hxx"
#include "bounded_buffer.hxx"

namespace mn
{
  namespace py = boost::python;

  class
  JackClient
  {
  public:
    JackClient ();
    ~JackClient ();

    int
    process (jack_nframes_t nframes);

    bool
    have_events ();

    py::object
    next_event ();

  private:
    jack_client_t* client_;
    jack_port_t* in_port_;

    boost::shared_ptr<inbounded_buffer<midi_event> > in_queue_;
  };
}

#endif // MANGANESE_MIDI_JACK_CLIENT_HXX
