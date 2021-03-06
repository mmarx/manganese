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

#ifndef UTABOR_UTABOR_HXX
#define UTABOR_UTABOR_HXX

#include <string>
#include <stdint.h>

#include <boost/python.hpp>
#include <boost/utility.hpp>

namespace ut
{
  namespace py = boost::python;

  class uTabor
    : public boost::noncopyable
  {
  public:
    static uTabor*
    get ()
    {
      if (!self_)
	{
	  self_ = new uTabor ();
	}

      return self_;
    }

    static void
    destroy ()
    {
      delete self_;
      self_ = 0;
    }

    void
    handle_midi (uint32_t data);

    void
    select_action (char key, bool logic);

    bool
    load_logic (std::string logic);

    int
    anchor ()
    {
      anchor_changed_ = false;
      return anchor_;
    }

    void
    need_update (bool update)
    {
      need_update_ = update;
    }

    bool
    need_update ()
    {
      return need_update_;
    }

    void
    keys (bool changed)
    {
      keys_changed_ = changed;
    }

    bool
    keys_changed ()
    {
      return keys_changed_;
    }

    py::object
    keys ();

    void
    anchor (int anchor)
    {
      anchor_changed_ = (anchor != anchor_);
      anchor_ = anchor;
    }

    bool
    anchor_changed ()
    {
      return anchor_changed_;
    }

    int
    width ()
    {
      width_changed_ = false;
      return width_;
    }

    void
    width (int width)
    {
      width_ = width;
      width_changed_ = true;
    }

    bool
    width_changed ()
    {
      return width_changed_;
    }

    bool ready ()
    {
      return have_logic_ && ready_;
    }

    py::object
    tone_system ();

  private:
    uTabor ()
      : ready_ (false),
	have_logic_ (false),
	need_update_ (false),
	keys_changed_ (false),
	anchor_ (-1),
	anchor_changed_ (false),
	width_ (-1),
	width_changed_ (false)
    {
    }

    ~uTabor () {}

    bool ready_;
    bool have_logic_;
    bool need_update_;
    bool keys_changed_;

    int anchor_;
    bool anchor_changed_;

    int width_;
    bool width_changed_;

    static uTabor* self_;
  };
}

#endif // UTABOR_UTABOR_HXX
