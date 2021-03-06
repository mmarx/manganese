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

#include <boost/python.hpp>

#include "runtime.hxx"
#include "execute.hxx"
#include "midikern.hxx"

#include "utabor.hxx"

// cannibalised from InMidiPort::ProceedRoute ()
void
handle_midi (DWORD midiCode)
{
  int Box = 0;
  BYTE MidiChannel = midiCode & 0x0F;
  BYTE MidiStatus = midiCode & 0xF0;

  switch (MidiStatus)
    {
    case 0x90: // Note On
      if ((midiCode & 0x7f0000) > 0)
	{
	  AddKey (Box, (midiCode >> 8) & 0xff, 0);
	  break;
	}

    case 0x80: // Note Off
      DeleteKey (Box, (midiCode >> 8) & 0xff, 0);
      break;

    default: // something else
      // do nothing
      break;
    }

  // Midianalyse
  int lMidiCode[8] =
    {3, 3, 3, 3, 2, 2, 3, 1
    };

  for (int i = 0; i < lMidiCode[MidiStatus >> 5]; ++i)
    {
      MidiAnalysis (Box,midiCode & 0xff);
      midiCode >>= 8;
    }

  FlushUpdateUI ();
}

namespace ut
{
  namespace py = boost::python;

  uTabor* uTabor::self_ = 0;

  void
  ui_callback ()
  {
    uTabor::get ()->need_update (true);
  }

  void
  key_callback (int box)
  {
    uTabor::get ()->keys (true);
  }

  void
  anchor_callback (int, int anchor)
  {
    uTabor::get ()->anchor (anchor);
  }

  void
  width_callback (int, int width)
  {
    uTabor::get ()->width (width);
  }

  void
  uTabor::handle_midi (uint32_t data)
  {
    if (!have_logic_ || !ready_)
      {
	std::cerr << "-!- tried to handle midi data while no logic was active."
		  << std::endl;
	return;
      }

    ::handle_midi (data);
  }

  void
  uTabor::select_action (char key, bool logic)
  {
    if (!have_logic_)
      {
	std::cerr << "-!- tried to select an action while no logic was active."
		  << std::endl;
	return;
      }

    ::KeyboardAnalyse (0, key, logic);

    if (logic)
      {
	// we changed the logic, so update anchor & width
	ton_system* ts = tonsystem[0];
	anchor_ = ts->anker;
	width_ = ts->breite;
      }

    ready_ = logic;
  }

  bool
  uTabor::load_logic (std::string logic)
  {
    if (!Compile (0, logic.c_str()))
      {
	return false;
      }

    Activate (false, ui_callback, key_callback,
	      anchor_callback, width_callback);

    have_logic_ = true;
    ready_ = false;

    return true;
  }

  py::object
  uTabor::keys ()
  {
    keys_changed_ = false;

    py::list the_keys;

    for (int i = 0; i < liegende_tasten_max[0]; ++i)
      {
	the_keys.append (liegende_tasten[0][i]);
      }

    return the_keys;
  }

  // adapted from protokoll_aktuelles_tonsystem ()
  py::object
  uTabor::tone_system ()
  {
    using namespace py;

    dict the_tone_system;

    ton_system* ts = tonsystem[0];
    long freq;
    unsigned char* ptr = reinterpret_cast<unsigned char*> (&freq);

    the_tone_system["width"] = width ();
    the_tone_system["anchor"] = anchor ();
    the_tone_system["period"] = LONG_TO_CENT (ts->periode);
    the_tone_system["system"] = dict ();

    for (int i = 0; i < width (); ++i)
      {
	if ((freq = ts->ton[i]) == 0)
	  {
	    the_tone_system["system"][i] = make_tuple ();
	  }
	else
	  {
	    the_tone_system["system"][i]
	      = make_tuple (LONG_TO_HERTZ (freq),
			    ptr[3] + (static_cast<float> (ptr[2] / 256.0)));
	  }
      }

    return the_tone_system;
  }

  BOOST_PYTHON_MODULE (_utabor)
  {
    using namespace boost::python;

    def ("get_uTabor", &uTabor::get,
	 return_value_policy<reference_existing_object> ());
    def ("destroy_uTabor", &uTabor::destroy);

    class_<uTabor, boost::noncopyable> ("uTabor", no_init)
      .def_readonly ("keys_changed", &uTabor::keys_changed)
      .def_readonly ("anchor_changed", &uTabor::anchor_changed)
      .def_readonly ("width_changed", &uTabor::width_changed)
      .def_readonly ("ready", &uTabor::ready)
      .def_readonly ("anchor",
		     static_cast<int (uTabor::*) ()> (&uTabor::anchor))
      .def_readonly ("width",
		     static_cast<int (uTabor::*) ()> (&uTabor::width))
      .def_readonly ("keys",
		     static_cast<object (uTabor::*) ()> (&uTabor::keys))
      .def_readonly ("tone_system", &uTabor::tone_system)
      .add_property ("need_update",
		     static_cast<bool (uTabor::*) ()> (&uTabor::need_update),
		     static_cast<void (uTabor::*) (bool)> (&uTabor::
							   need_update))
      .def ("load_logic", &uTabor::load_logic)
      .def ("select_action", &uTabor::select_action)
      .def ("handle_midi", &uTabor::handle_midi);
  }
}
