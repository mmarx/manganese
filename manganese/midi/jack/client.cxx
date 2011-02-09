/* manganese - mutabor-ng platform
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

  midi_event
  JackClient::next_event ()
  {
    midi_event event;

    in_queue_->pop_back (&event);

    return event;
  }

  int
  JackClient::process (jack_nframes_t nframes)
  {
    // do something
    void* port_buffer = jack_port_get_buffer (in_port_, nframes);
    jack_nframes_t count = jack_midi_get_event_count (port_buffer);

    if (count)
      {
	for (jack_nframes_t i = 0; i < count; ++i)
	{
	  jack_midi_event_t event;
	  jack_midi_event_get (&event, port_buffer, i);

	  unsigned char status_byte = event.buffer[0];
	  unsigned char channel = status_byte & 0x0f;
	  unsigned char event_type = status_byte & 0xf0;

	  midi_event the_event (event_type, channel, 0, 0);

	  switch (event_type)
	    {
	    case 0x80:
	      the_event.key_ = event.buffer[1];
	      in_queue_->push_front (the_event);
	      break;
	    case 0x90:
	      the_event.key_ = event.buffer[1];
	      the_event.value_ = event.buffer[2];
	      in_queue_->push_front (the_event);
	      break;
	    default:
	      break;
	    }
	}
      }

    return 0;
  }
}
