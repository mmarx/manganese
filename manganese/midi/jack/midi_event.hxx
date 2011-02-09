/* manganese - mutabor-ng platform
 * Copyright (c) 2010, 2011, Maximilian Marx <mmarx@wh2.tu-dresden.de>
 *
 * Permission to use, copy, modify, and/or distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
n * MERCHANTABILITY AND FITNESS.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
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
    midi_event ()
      : size_ (0),
	continued_ (false),
	continuation_ (false)
    {
    }

    midi_event (unsigned char* data,
		size_t size,
		bool continued = false,
		bool continuation = false)
      : size_ (size),
	continued_ (continued),
	continuation_ (continuation)
    {
      for (size_t i = 0; i < size; ++i)
	{
	  data_[i] = data[i];
	}
    }

    unsigned char data_[3];
    size_t size_;
    bool continued_;
    bool continuation_;
  };
}

#endif // MANGANESE_MIDI_JACK_MIDI_EVENT_HXX
