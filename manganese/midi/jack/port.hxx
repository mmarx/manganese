
#ifndef MANGANESE_MIDI_JACK_PORT_HXX
#define MANGANESE_MIDI_JACK_CLIENT_HXX

#include <string>

#include <boost/shared_ptr.hpp>
#include <boost/python.hpp>

#include <jack/jack.h>

#include "jack_ptr.hxx"
#include "midi_event.hxx"
#include "bounded_buffer.hxx"

namespace mn
{
  using std::string;

  class
  JackPort
  {
  public:
    explicit
    JackPort (string name)
      : name_(name) {}

    virtual
    ~JackPort () = 0;

    string const&
    name ()
    {
      return name_;
    }

  protected:
    string name_;
  };
}

#endif // MANGANESE_MIDI_JACK_CLIENT_HXX
