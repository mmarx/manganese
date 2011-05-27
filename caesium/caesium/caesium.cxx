
#include <map>
#include <vector>
#include <cstring>
#include <iostream>

#include <boost/python.hpp>

#include <jack/jack.h>
#include <jack/midiport.h>

namespace cs
{
  namespace py = boost::python;

  int const mark_channel = 0;
  int const time_channel = 1;
  //int const mark_offset = 21;
  int mark_offset = 21;

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
  jack_nframes_t per_callback;
  jack_nframes_t sample_rate;
  jack_nframes_t base_interval;

  int const window_size = 4;
  int const target_bpm = 120;

  jack_nframes_t window[window_size];
  int index;

  bool first;
  bool have_window;
  bool running;

  char hh;
  char mm;
  char ss;
  char fr;
  char sf;
  char lp;

  struct timestamp
  {
    timestamp () {}
    timestamp (char hours, char minutes, char seconds, char frames)
      : hh (hours), mm (minutes), ss (seconds), fr (frames) {}

    int
    as_frames () const
    {
      return fr + 30 * (ss + 60 * (mm + 60 * hh));
    }

    bool
    operator< (timestamp const& rhs)
    {
      return as_frames () < rhs.as_frames ();
    }

    bool
    operator<= (timestamp const& rhs)
    {
      return as_frames () <= rhs.as_frames ();
    }

    char hh;
    char mm;
    char ss;
    char fr;
  };

  std::size_t stamp = 0;
  std::size_t stamp_count = 0;

  std::vector<timestamp> stamps;
  std::map<std::string, char> controllers;

  void
  set_range (double factor);

  void
  set_running (bool run);

  void
  update_speed ();

  void
  jump (void* port_buffer,
	jack_nframes_t frame,
	timestamp const& stamp)
  {
    hh = stamp.hh;
    mm = stamp.mm;
    ss = stamp.ss;
    fr = stamp.fr;

#if 0
    std::cerr << "jumping: "
	      << static_cast<unsigned int> (hh) << " "
	      << static_cast<unsigned int> (mm) << " "
	      << static_cast<unsigned int> (ss) << " "
	      << static_cast<unsigned int> (fr)
	      << std::endl;
#endif

    lp = 0;
    sf = -1;

    jack_midi_data_t* event = jack_midi_event_reserve (port_buffer,
						       frame,
						       10);
    std::memcpy (event, tc_header, 5);
    event[5] = 0x10 | hh;
    event[6] = mm;
    event[7] = ss;
    event[8] = fr;
    event[9] = 0xF7;

#if 0
    std::cerr << "-@- now at stamp " << cs::stamp << std::endl;
#endif
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

    timestamp now = timestamp(hh, mm, ss, fr);

    while ((stamp < stamp_count - 1) && (stamps[stamp] <= now))
      {
	++stamp;
      }

#if 0
    std::cerr << "-:- now at stamp " << stamp << std::endl;
#endif

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
    void* input_buffer = jack_port_get_buffer (input_port, nframes);
    jack_nframes_t count = jack_midi_get_event_count (input_buffer);

    per_callback = nframes;

    for (int i = 0; i < window_size; ++i)
      {
	window[i] += sample_rate;
      }

    void* port_buffer = jack_port_get_buffer (output_port, nframes);
    jack_midi_clear_buffer (port_buffer);

    for (jack_nframes_t i = 0; i < count; ++i)
      {
	jack_midi_event_t event;
	jack_midi_event_get (&event, input_buffer, i);

	if ((event.buffer[0] & 0xF0) == 0xE0)
	  {
	    // pitch bend
	    short pitch = event.buffer[2];
	    pitch <<= 7;
	    pitch |= event.buffer[1];

	    pitch -= 8192;
	    scale = base_scale + range * (pitch / 8192.);
	  }
	else if (running && (event.buffer[0] & 0xF0) == 0x90)
	  {
	    // note on

	    int channel = event.buffer[0] & 0x0F;

	    if (channel == mark_channel)
	      {
		size_t target = event.buffer[1] - mark_offset;

		if ((target >= 0) && (target < stamp_count))
		  {
		    stamp = event.buffer[1] - mark_offset;
		    jump (port_buffer, 0, stamps[stamp]);
		  }
	      }
	    else if (channel == time_channel)
	      {
		++index;

		if (!have_window && index >= window_size)
		  {
		    have_window = true;
		  }

		index %= window_size;

		window[index] = event.time;

		if (have_window)
		  {
		    update_speed ();
		  }
	      }
	  }
	else if ((event.buffer[0] & 0xF0) == 0xB0)
	  {
	    // controller change
	    char controller = event.buffer[1];
	    char value = event.buffer[2];

	    if (controller == controllers["range"])
	      {
		set_range (0.1 + 0.9 * (value / 127.0));
	      }
	    else
	      {
		if (controller == controllers["stop"])
		  {
		    set_running (false);
		  }
		else if (controller == controllers["start"])
		  {
		    set_running (true);
		  }
		else if (controller == controllers["reset"])
		  {
		    index = -1;
		    first = true;
		    have_window = false;
		  }
		else if (controller == controllers["next"])
		  {
		    if (stamp < stamp_count - 1)
		      {
			jump (port_buffer, 0, stamps[++stamp]);
		      }
		  }
		else if (controller = controllers["prev"])
		  {
		    if (stamp > 1)
		      {
			stamp -= 2;
		      }
		    else if (stamp > 0)
		      {
			--stamp;
		      }

		    jump (port_buffer, 0, stamps[stamp]);
		  }
	      }
	  }
      }

    if (!running || !have_window)
      {
	return 0;
      }

    //std::cerr << "-!-" << std::endl;

    if (first)
      {
	first = false;
	stamp = 0;
	jump (port_buffer, 0, timestamp (0, 0, 0, 0));
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
  create (double speed, double range, int offset, py::list markers,  py::dict controls)
  {
    mark_offset = offset;

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
    index = -1;
    first = true;
    have_window = false;

    set_range (range);
    set_speed (speed);
    set_running (false);

    jack_activate (client);

    sample_rate = jack_get_sample_rate (client);
    base_interval = sample_rate / 120.0;

    py::ssize_t n = py::len (markers);

    stamps.resize (n);

    for (py::ssize_t i = 0; i < n; ++i)
      {
	py::object obj = markers[i];
	py::dict stamp = py::extract<py::dict> (obj);

	stamps[i] = timestamp(py::extract<unsigned long> (stamp["hours"]),
			      py::extract<unsigned long> (stamp["minutes"]),
			      py::extract<unsigned long> (stamp["seconds"]),
			      py::extract<unsigned long> (stamp["frames"]));

	++stamp_count;
      }

    unsigned int i = 0;

    for (std::vector<timestamp>::iterator it = stamps.begin ();
	 it != stamps.end ();
	 ++it, ++i)
      {
	std::cout << "-#- marker " << i << ": "
		  << static_cast<unsigned long> (it->hh) << " "
		  << static_cast<unsigned long> (it->mm) << " "
		  << static_cast<unsigned long> (it->ss) << " "
		  << static_cast<unsigned long> (it->fr)
		  << std::endl;
      }

    py::list keys = controls.keys ();
    n = py::len (keys);

    for (py::ssize_t i = 0; i < n; ++i)
      {
	py::object key = keys[i];
	std::string k = py::extract<std::string> (key);
	char c = py::extract<unsigned long> (controls[key]);

	controllers[k] = c;

	std::cout << "-#- controller: " << k
		  << ": " << static_cast<unsigned long> (c)
		  << std::endl;
      }
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

  jack_nframes_t
  interval (int i)
  {
    int prev = (i ? i - 1 : window_size - 1);

    int callbacks_curr = 1;
    int callbacks_prev = 1;

    jack_nframes_t offset = 0;

    if (window[i] > sample_rate)
      {
	callbacks_curr = window[i] / sample_rate;
	window[i] %= sample_rate;
      }

    if (window[prev] > sample_rate)
      {
	callbacks_prev = window[prev] / sample_rate;
	window[prev] %= sample_rate;
      }

    if (callbacks_curr <= callbacks_prev)
      {
	offset = (callbacks_prev - callbacks_curr) * per_callback;
      }
    else
      {
	offset = (callbacks_curr - callbacks_prev) * per_callback;
      }

    if (window[i] < window[prev])
      {
	return offset + window[prev] - window[i];
      }
    else
      {
	return offset + window[i] - window[prev];
      }
  }

  void
  update_speed ()
  {
    jack_nframes_t acc = 0;

    for (int i = index; i < window_size; ++i)
      {
	jack_nframes_t ts = interval (i);
	acc += ts;
      }

    for (int i = 0; i < index; ++i)
      {
	jack_nframes_t ts = interval (i);
	acc += ts;
      }

    double bpm = sample_rate * window_size * 60.0d / acc;

    double rescale = bpm / target_bpm;

    std::cerr << "-#- bpm: "
	      << bpm
	      << " rescale: "
	      << rescale
	      << std::endl;

    set_speed (rescale);
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
