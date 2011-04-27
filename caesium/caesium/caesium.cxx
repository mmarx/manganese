
#include <cstring>
#include <iostream>

#include <boost/python.hpp>

#include <jack/jack.h>
#include <jack/midiport.h>

namespace cs
{
  namespace py = boost::python;

  jack_client_t* client;
  jack_port_t* input_port;
  jack_port_t* output_port;

  unsigned char tc_header[] = {0xF0,
			       0x7F,
			       0x7F,
			       0x01,
			       0x01};
  
  double range;
  double scale;
  double base_scale;
  jack_nframes_t last;
  jack_nframes_t base_interval;

  bool first;
  bool running;

  char hh;
  char mm;
  char ss;
  char fr;
  char sf;
  char lp;
  
  void
  jump (void* port_buffer,
	jack_nframes_t frame)
  {
    jack_midi_data_t* event = jack_midi_event_reserve (port_buffer,
						       frame,
						       10);
    std::memcpy (event, tc_header, 5);
    event[5] = 0x10 | hh;
    event[6] = mm;
    event[7] = ss;
    event[8] = fr;
    event[9] = 0xF7;
  }

  void
  tick (void* port_buffer,
	jack_nframes_t frame)
  {
    if (++sf == 4)
      {
	sf = 0;
	if (++fr == 30)
	  {
	    fr = 0;
	    if (++ss == 60)
	      {
		ss = 0;
		if (++mm == 60)
		  {
		    mm = 0;
		    if (++hh == 24)
		      {
			hh = 0;
		      }
		  }
	      }
	  }
      }

    jack_midi_data_t* event = jack_midi_event_reserve (port_buffer,
						       frame,
						       2);
    
    event[0] = 0xF1;
    event[1] = (lp << 4);

    switch (sf)
      {
      case 0:
	if (lp == 0)
	  {
	    event[1] |= fr & 0x0f;
	  }
	else if (lp == 4)
	  {
	    event[1] |= mm & 0x0f;
	  }
	break;

      case 1:
	if (lp == 1)
	  {
	    event[1] |= (fr & 0x10) >> 4;
	  }
	else if (lp == 5)
	  {
	    event[1] |= (mm & 0x30) >> 4;
	  }
	break;

      case 2:
	if (lp == 2)
	  {
	    event[1] |= ss & 0x0f;
	  }
	else if (lp == 6)
	  {
	    event[1] |= hh & 0x0f;
	  }
	break;

      case 3:
	if (lp == 3)
	  {
	    event[1] |= (ss & 0x30) >> 4;
	  }
	else if (lp == 7)
	  {
	    event[1] |= 0x06 | (hh & 0x10) >> 4;
	  }
	break;

      default:
	break;
      }

    if (++lp == 8)
      {
	lp = 0;
      }
  }

  int
  process (jack_nframes_t nframes,
	   void* arg)
  {
    if (!running)
      {
	return 0;
      }

    void* port_buffer = jack_port_get_buffer (output_port, nframes);
    jack_midi_clear_buffer (port_buffer);

    void* input_buffer = jack_port_get_buffer (input_port, nframes);
    jack_nframes_t count = jack_midi_get_event_count (input_buffer);

    for (jack_nframes_t i = 0; i < count; ++i)
      {
	jack_midi_event_t event;
	jack_midi_event_get (&event, input_buffer, i);

	if ((event.buffer[0] & 0xF0) == 0xE0)
	  {
	    short pitch = event.buffer[2];
	    pitch <<= 7;
	    pitch |= event.buffer[1];
	    
	    pitch -= 8192;
	    scale = base_scale + range * (pitch / 8192.);
	  }
      }
    
    if (first)
      {
	first = false;

	hh = mm = ss = fr = lp = 0;
	sf = -1;

	jump (port_buffer, 0);
      }

    jack_nframes_t interval = base_interval / scale;
    if (interval <= 0)
      {
	interval = 1;
      }

    if (last > interval)
      {
	last = interval;
      }

    jack_nframes_t frame = interval - last;

    while (frame < nframes)
      {
	tick (port_buffer, frame);

	frame += interval;
      }

    if (frame >= nframes)
      {
	last = nframes - frame + interval;
      }
    else
      {
	last += nframes;
      }

    return 0;
  };

  void
  set_running (bool run)
  {
    running = run;
  }

  void
  set_speed (double speed)
  {
    base_scale = scale = speed;
  }

  void
  set_range (double factor)
  {
    range = factor;
  }

  void
  create (double speed, double range)
  {
    client = jack_client_open ("caesium", JackNullOption, 0);
  
    jack_set_process_callback (client, process, 0);

    output_port = jack_port_register (client,
				      "clock out",
				      JACK_DEFAULT_MIDI_TYPE,
				      JackPortIsOutput,
				      0);

    input_port = jack_port_register (client,
				     "control in",
				     JACK_DEFAULT_MIDI_TYPE,
				     JackPortIsInput,
				     0);

    last = 0;
    first = true;
    
    set_range (range);
    set_speed (speed);
    set_running (false);

    jack_activate (client);

    base_interval = jack_get_sample_rate (client) / 120.0;
  }

  void
  destroy ()
  {
    if (client)
      {
	if (output_port)
	  {
	    jack_port_unregister (client, output_port);
	  }

	jack_client_close (client);
      }
  }

  BOOST_PYTHON_MODULE (_caesium)
  {
    using namespace boost::python;

    def ("set_speed", set_speed);
    def ("set_running", set_running);
    def ("create_caesium", create);
    def ("destroy_caesium", destroy);
  }
}
