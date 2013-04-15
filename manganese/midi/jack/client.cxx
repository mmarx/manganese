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


#include <iostream>

#include <jack/midiport.h>

#include "client.hxx"

namespace mn
{
  int
  process (jack_nframes_t nframes,
	   void* arg)
  {
    return static_cast<JackClient*> (arg)->process (nframes);
  }

  JackClient::JackClient ()
    : client_ (0), in_port_ (0),
      in_queue_ (new inbounded_buffer<midi_event> (2048))
  {
    jack_status_t status;
    client_ = jack_client_open ("manganese",
				JackNullOption,
				&status);

    in_port_ = jack_port_register (client_,
				   "midi in",
				   JACK_DEFAULT_MIDI_TYPE,
				   JackPortIsInput | JackPortIsTerminal,
				   0);

    jack_set_process_callback (client_, ::mn::process, this);

    jack_activate (client_);
  }

  JackClient::~JackClient ()
  {
    if (client_)
      {
	if (in_port_)
	  {
	    jack_port_unregister (client_, in_port_);
	  }

	jack_client_close (client_);
      }
  }

  bool
  JackClient::have_events ()
  {
    return in_queue_->is_not_empty ();
  }

  py::object
  JackClient::next_event ()
  {
    py::list the_event = py::list();
    midi_event event;

    int j = 0;

    do
      {
	in_queue_->pop_back (&event);

	for (size_t i = 0; i < event.size_; ++i)
	  {
	    the_event.append (event.data_[i]);
	  }
      }
    while (event.continued_);

    return the_event;
  }

  int
  JackClient::process (jack_nframes_t nframes)
  {
    void* port_buffer = jack_port_get_buffer (in_port_, nframes);
    jack_nframes_t count = jack_midi_get_event_count (port_buffer);

    if (count)
      {
	for (jack_nframes_t i = 0; i < count; ++i)
	  {
	    jack_midi_event_t event;
	    jack_midi_event_get (&event, port_buffer, i);

	    size_t size = event.size;

	    if (size <= 3)
	      {
		// single-message event
		in_queue_->push_front (midi_event (event.buffer, size));
	      }
	    else
	      {
		// split it up
		in_queue_->push_front (midi_event (event.buffer, 3, true));

		size_t i = 3;
		for (; i < (size - 3); i += 3)
		  {
		    in_queue_->push_front (midi_event ((event.buffer + i),
						       3, true, true));
		  }

		in_queue_->push_front (midi_event ((event.buffer + i),
						   (size - i), false, true));
	      }
	  }
      }

    return 0;
  }
}
