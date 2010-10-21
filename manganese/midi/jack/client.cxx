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

#include "client.hxx"

namespace mn
{
  int
  process (jack_nframes_t nframes,
	   void* arg)
  {
    return static_cast<JackClient*> (arg)->process (nframes);
  }
  
  void
  JackClient::init ()
  {
    jack_status_t status;
    jack_client_t* client = jack_client_open ("manganese",
					      JackNullOption,
					      &status);

    jack_port_t* port = jack_port_register (client,
					    "midi in",
					    JACK_DEFAULT_MIDI_TYPE,
					    JackPortIsInput | JackPortIsTerminal,
					    0);
    
    jack_port_t* port_ = jack_port_register (client,
					     "midi out",
					     JACK_DEFAULT_MIDI_TYPE,
					     JackPortIsOutput | JackPortIsTerminal,
					     0);

    jack_set_process (client, ::mn::process, this);
  
  }
}
