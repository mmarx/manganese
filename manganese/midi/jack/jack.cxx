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

#include <memory>

#include <boost/python.hpp>
#include <boost/thread.hpp>

#include "client.hxx"

namespace mn
{
  JackClient*
  create_client ()
  {
    return new JackClient;
  }

  void
  destroy_client (std::auto_ptr<JackClient> client)
  {
    client.reset ();
  };

  BOOST_PYTHON_MODULE (_jack)
  {
    using namespace boost::python;

    def ("create_client",
	 create_client,
	 return_value_policy<manage_new_object> ());
    def ("destroy_client",
	 destroy_client);
    class_<JackClient> ("JackClient")
      .def_readonly ("have_events", &JackClient::have_events)
      .def ("next_event", &JackClient::next_event,
	    return_value_policy<return_by_value> ());

    class_<midi_event> ("midi_event",
			init<unsigned char, unsigned char,
			     unsigned char, unsigned char> ())
      .def (init<midi_event const&> ())
      .def_readwrite ("type", &midi_event::type_)
      .def_readwrite ("channel", &midi_event::channel_)
      .def_readwrite ("key", &midi_event::key_)
      .def_readwrite ("value", &midi_event::value_);
  }
}
