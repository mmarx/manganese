/* manganese - mutabor-ng platform
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

#ifndef MANGANESE_MIDI_JACK_BOUNDED_BUFFER_HXX
#define MANGANESE_MIDI_JACK_BOUNDED_BUFFER_HXX

#include <iostream>

#include <boost/circular_buffer.hpp>
#include <boost/thread/mutex.hpp>
#include <boost/thread/condition.hpp>
#include <boost/thread/thread.hpp>
#include <boost/call_traits.hpp>
#include <boost/noncopyable.hpp>
#include <boost/bind.hpp>

namespace mn
{
  /**
   * A bounded, circular buffer, suitable for a producer-consumer environment.
   * Based upon an example from the boost::circular_buffer documentation.
   */

  template<typename T>
  class basic_bounded_buffer : public boost::noncopyable
  {
  public:
    typedef boost::circular_buffer<T> container_type;
    typedef typename container_type::size_type size_type;
    typedef typename container_type::value_type value_type;
    typedef typename boost::call_traits<value_type>::param_type param_type;

    explicit basic_bounded_buffer (size_type capacity_)
      : capacity (capacity_), unread (0), container (capacity_)
    {
    }

    void
    push_front (param_type item)
    {
      container.push_front (item);
      ++unread;
    }

    void
    pop_back (value_type* item)
    {
      *item = container[--unread];
    }

    bool
    is_not_empty () const
    {
      return unread > 0;
    }

    bool
    is_not_full () const
    {
      return unread < capacity;
    }

  protected:
    size_type unread;
    size_type capacity;
    container_type container;

    boost::mutex mutex;
  };

  template<typename T>
  class inbounded_buffer : public basic_bounded_buffer<T>
  {
  public:
    explicit inbounded_buffer (typename basic_bounded_buffer<T>::size_type
			       capacity)
      : basic_bounded_buffer<T>::basic_bounded_buffer (capacity)
    {
    }

    void
    push_front (typename basic_bounded_buffer<T>::param_type item)
    {
      boost::mutex::scoped_lock lock (basic_bounded_buffer<T>::mutex);

      if (basic_bounded_buffer<T>::is_not_full ())
	{
	  basic_bounded_buffer<T>::push_front (item);
	}
      else
	{
	  std::cerr << "Over capacity, dropping item." << std::endl;
	}

      lock.unlock ();
    }

    void
    pop_back (typename basic_bounded_buffer<T>::value_type* item)
    {
      boost::mutex::scoped_lock lock (basic_bounded_buffer<T>::mutex);
      not_empty.wait (lock,
		      boost::bind (&basic_bounded_buffer<T>::is_not_empty,
				   this));

      basic_bounded_buffer<T>::pop_back (item);

      lock.unlock ();
    }

  protected:
    boost::condition not_empty;
  };

  template<typename T>
  class outbounded_buffer : public basic_bounded_buffer<T>
  {
  public:
    explicit outbounded_buffer (typename basic_bounded_buffer<T>::size_type
				capacity)
      : basic_bounded_buffer<T>::basic_bounded_buffer (capacity)
    {
    }

    void
    push_front (typename basic_bounded_buffer<T>::param_type item)
    {
      boost::mutex::scoped_lock lock (basic_bounded_buffer<T>::mutex);
      not_full.wait (lock,
		     boost::bind (&basic_bounded_buffer<T>::is_not_full,
				  this));

      basic_bounded_buffer<T>::push_front (item);

      lock.unlock ();
    }

    void
    pop_back (typename basic_bounded_buffer<T>::value_type* item)
    {
      boost::mutex::scoped_lock lock (basic_bounded_buffer<T>::mutex);

      if (basic_bounded_buffer<T>::is_not_empty ())
	{
	  basic_bounded_buffer<T>::push_back (item);
	}
      else
	{
	  std::cerr << "trying to pop an empty buffer." << std::endl;
	  item = 0;
	}

      lock.unlock ();

      if (item)
	{
	  not_full.notify_one ();
	}
    }

  protected:
    boost::condition not_full;
  };
}

#endif // MANGANESE_MIDI_JACK_BOUNDED_BUFFER_HXX
