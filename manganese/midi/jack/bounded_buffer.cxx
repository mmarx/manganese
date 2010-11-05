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
  class bounded_buffer : public boost::noncopyable
  {
    typedef boost::circular_buffer<T> container_type;
    typedef typename container_type::size_type size_type;
    typedef typename container_type::value_type value_type;
    typedef typename boost::call_traits<value_type> param_type;

    explicit bounded_buffer (size_type capacity)
      : unread (0), container (capacity)
    {
    }

    void
    push_front (param_type item)
    {
      if (unread < container.capacity ())
	{
	  ++unread;
	  not_empty.notify_one ();
	}
      else
	{
	  using std::cerr;
	  using std::endl;

	  cerr << "Over capacity, dropping item." << endl;
	}
    }

    void
    pop_back (value_type* item)
    {
      boost::mutex::scoped_lock lock (mutex);
      not_empty.wait (lock,
		      boost::bind (&bounded_buffer<value_type>::is_not_empty,
				   this));

      item = container[--unread];

      lock.unlock ();
    }

  private:
    bool
    is_not_empty () const
    {
      return unread > 0;
    }

    size_type unread;
    container_type container;

    boost::mutex mutex;
    boost::condition no_empty;
  }
}
