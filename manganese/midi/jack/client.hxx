/* manganese - mutabor-ng platform
 * Copyright (c) 2010, 2011, Maximilian Marx <mmarx@wh2.tu-dresden.de>
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

#ifndef MANGANESE_MIDI_JACK_CLIENT_HXX
#define MANGANESE_MIDI_JACK_CLIENT_HXX

#include <boost/shared_ptr.hpp>
#include <boost/python.hpp>

#include <jack/jack.h>

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
