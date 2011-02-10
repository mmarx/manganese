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
