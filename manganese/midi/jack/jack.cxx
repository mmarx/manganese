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
      .def ("next_event", &JackClient::next_event);
  }
}
