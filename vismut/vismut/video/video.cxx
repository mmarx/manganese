/* vismut - mutabor-ng platform visualization
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

#include <boost/python.hpp>

#include "rect.hxx"
#include "video.hxx"

namespace bi
{
  namespace py = boost::python;

  bool SDLContext::error_ = false;
  unsigned int SDLContext::users_ = 0;

  SDLContext::SDLContext ()
  {
    if (!users_++)
      {
	surface_ = NULL;
	call (SDL_Init (SDL_INIT_VIDEO));
      }
  }

  SDLContext::~SDLContext ()
  {
    if (!--users_)
      {
	SDL_Quit ();
	surface_ = NULL;
      }
  }

  void
  SDLContext::call (int ret)
  {
    if (ret < 0)
      {
	flag_error ();
      }
  }

  char const*
  SDLContext::error_string () const
  {
    return SDL_GetError ();
  }

  py::object
  list_video_modes ()
  {
    SDL_Rect** modes = SDL_ListModes (NULL, SDL_OPENGL|SDL_FULLSCREEN);

    if (!modes)
      {
	return py::object ();
      }

    if (modes == reinterpret_cast<SDL_Rect**> (-1))
      {
	return py::list ();
      }

    py::list the_modes;

    for (int i = 0; modes[i]; ++i)
      {
	   the_modes.append (*modes[i]);
      }

    return the_modes;
  }

  void
  SDLContext::set_mode (py::object mode)
  {
    using namespace boost::python;

    SDL_Rect& rect = extract<SDL_Rect&> (mode);

    surface_ = SDL_SetVideoMode (rect.w, rect.h, 32, SDL_OPENGL);

    if (!surface_)
      {
	flag_error ();
      }
  }

  BOOST_PYTHON_MODULE (_video)
  {
    using namespace boost::python;

    class_<SDLContext> ("SDLContext")
      .add_property ("users", &SDLContext::users)
      .add_property ("have_error", &SDLContext::have_error)
      .add_property ("error_string", &SDLContext::error_string)
      .def ("set_mode", &SDLContext::set_mode);

    class_<SDL_Rect> ("SDLRect")
      .def_readwrite ("x", &SDL_Rect::x)
      .def_readwrite ("y", &SDL_Rect::y)
      .def_readwrite ("w", &SDL_Rect::w)
      .def_readwrite ("h", &SDL_Rect::h)
      .def (self_ns::str (self))
      .def ("__repr__", rect::rect_repr)
      .add_property ("size", rect::rect_size);

    def ("list_video_modes", list_video_modes);
  }
}
