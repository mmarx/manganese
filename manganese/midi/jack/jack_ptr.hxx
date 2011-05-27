
#ifndef MANGANESE_MIDI_JACK_PTR_HXX
#define MANGANESE_MIDI_JACK_PTR_HXX

#include <boost/shared_ptr.hpp>

#include <jack/jack.h>

namespace mn
{
  template<typename T>
  struct
  jack_deleter
  {
    jack_deleter () throw () {}
    jack_deleter (jack_deleter const& other) throw () {}
    ~jack_deleter () throw () {}

    void
    operator () (T* ptr) throw ()
    {
      jack_free (ptr);
    }
  };

  template<typename T>
  boost::shared_ptr<T>
  shared_jack_ptr (T* ptr)
  {
    return boost::shared_ptr<T> (ptr, jack_deleter<T> ());
  };
}

#endif // MANGANESE_MIDI_JACK_PTR_HXX
