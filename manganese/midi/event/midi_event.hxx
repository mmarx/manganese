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

#ifndef MANGANESE_MIDI_JACK_MIDI_EVENT_HXX
#define MANGANESE_MIDI_JACK_MIDI_EVENT_HXX

namespace mn
{
  struct midi_event
  {
    midi_event () : type_ (0),
		    channel_ (0),
		    key_ (0),
		    value_ (0)
    {
    }

    midi_event (unsigned char type,
		unsigned char channel,
		unsigned char key,
		unsigned char value)
      : type_ (type),
	channel_ (channel),
	key_ (key),
	value_ (value)
    {
    }

    unsigned char type_;
    unsigned char channel_;
    unsigned char key_;
    unsigned char value_;
  };
}

#endif // MANGANESE_MIDI_JACK_MIDI_EVENT_HXX
