//
// Created by seb on 7/19/18.
//

#ifndef MERGESORTS_GNU_STL_SORT_H
#define MERGESORTS_GNU_STL_SORT_H




// Algorithm implementation -*- C++ -*-

// Copyright (C) 2001-2017 Free Software Foundation, Inc.
//
// This file is part of the GNU ISO C++ Library.  This library is free
// software; you can redistribute it and/or modify it under the
// terms of the GNU General Public License as published by the
// Free Software Foundation; either version 3, or (at your option)
// any later version.

// This library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// Under Section 7 of GPL version 3, you are granted additional
// permissions described in the GCC Runtime Library Exception, version
// 3.1, as published by the Free Software Foundation.

// You should have received a copy of the GNU General Public License and
// a copy of the GCC Runtime Library Exception along with this program;
// see the files COPYING3 and COPYING.RUNTIME respectively.  If not, see
// <http://www.gnu.org/licenses/>.

/*
  *
  * Copyright (c) 1994
  * Hewlett-Packard Company
  *
  * Permission to use, copy, modify, distribute and sell this software
  * and its documentation for any purpose is hereby granted without fee,
  * provided that the above copyright notice appear in all copies and
  * that both that copyright notice and this permission notice appear
  * in supporting documentation.  Hewlett-Packard Company makes no
  * representations about the suitability of this software for any
  * purpose.  It is provided "as is" without express or implied warranty.
  *
  *
  * Copyright (c) 1996
  * Silicon Graphics Computer Systems, Inc.
  *
  * Permission to use, copy, modify, distribute and sell this software
  * and its documentation for any purpose is hereby granted without fee,
  * provided that the above copyright notice appear in all copies and
  * that both that copyright notice and this permission notice appear
  * in supporting documentation.  Silicon Graphics makes no
  * representations about the suitability of this software for any
  * purpose.  It is provided "as is" without express or implied warranty.
  */

/** @file bits/stl_algo.h
  *  This is an internal header file, included by other library headers.
  *  Do not attempt to use it directly. @headername{algorithm}
  */

#include <cstdlib>           // for rand
#include <bits/algorithmfwd.h>
#include <bits/stl_heap.h>
#include <bits/stl_tempbuf.h>  // for _Temporary_buffer
#include <bits/predefined_ops.h>

#if cplusplus >= 201103L
#include <bits/uniform_int_dist.h>
#endif

// See concept_check.h for the glibcxx_*_requires macros.

namespace mystd
{

	/// Swaps the median value of *a, *b and *c under comp to *result
	template<typename Iter, typename Cmp>
	void
	move_median_to_first(Iter result,Iter a, Iter b,
	                       Iter c, Cmp comp)
	{
		if (comp(a, b))
		{
			if (comp(b, c))
				std::iter_swap(result, b);
			else if (comp(a, c))
				std::iter_swap(result, c);
			else
				std::iter_swap(result, a);
		}
		else if (comp(a, c))
			std::iter_swap(result, a);
		else if (comp(b, c))
			std::iter_swap(result, c);
		else
			std::iter_swap(result, b);
	}

	/// This is a helper function for the sort routines.
	template<typename Iter, typename Cmp>
	void
	heap_select(Iter first,
	              Iter middle,
	              Iter last, Cmp comp)
	{
		std::make_heap(first, middle, comp);
		for (Iter i = middle; i < last; ++i)
			if (comp(i, first))
				std::pop_heap(first, middle, i, comp);
	}

	// partial_sort


	/// This is a helper function for the sort routine.
	template<typename Iter, typename Cmp>
	void
	unguarded_linear_insert(Iter last,
	                          Cmp comp)
	{
		typename std::iterator_traits<Iter>::value_type
				val = std::move(*last);
		Iter next = last;
		--next;
		while (comp(val, next))
		{
			*last = std::move(*next);
			last = next;
			--next;
		}
		*last = std::move(val);
	}

	/// This is a helper function for the sort routine.
	template<typename Iter, typename Cmp>
	void
	insertion_sort(Iter first,
	                 Iter last, Cmp comp)
	{
		if (first == last) return;

		for (Iter i = first + 1; i != last; ++i)
		{
			if (comp(i, first))
			{
				typename std::iterator_traits<Iter>::value_type
						val = std::move(*i);
				std::move_backward(first, i, i + 1);
				*first = std::move(val);
			}
			else
				mystd::unguarded_linear_insert(i,
				                               __gnu_cxx::__ops::__val_comp_iter(comp));
		}
	}

	/// This is a helper function for the sort routine.
	template<typename Iter, typename Cmp>
	inline void
	unguarded_insertion_sort(Iter first,
	                           Iter last, Cmp comp)
	{
		for (Iter i = first; i != last; ++i)
			mystd::unguarded_linear_insert(i,
			                               __gnu_cxx::__ops::__val_comp_iter(comp));
	}

	/**
    *  @doctodo
    *  This controls some aspect of the sort routines.
   */
	enum { _S_threshold = 16 };

	/// This is a helper function for the sort routine.
	template<typename Iter, typename Cmp>
	void
	final_insertion_sort(Iter first,
	                       Iter last, Cmp comp)
	{
		if (last - first > int(_S_threshold))
		{
			mystd::insertion_sort(first, first + int(_S_threshold), comp);
			mystd::unguarded_insertion_sort(first + int(_S_threshold), last,
			                                comp);
		}
		else
			mystd::insertion_sort(first, last, comp);
	}

	/// This is a helper function...
	template<typename Iter, typename Cmp>
	Iter
	unguarded_partition(Iter first,
	                      Iter last,
	                      Iter pivot, Cmp comp)
	{
		while (true)
		{
			while (comp(first, pivot))
				++first;
			--last;
			while (comp(pivot, last))
				--last;
			if (!(first < last))
				return first;
			std::iter_swap(first, last);
			++first;
		}
	}

	/// This is a helper function...
	template<typename Iter, typename Cmp>
	inline Iter
	unguarded_partition_pivot(Iter first,
	                            Iter last, Cmp comp)
	{
		Iter mid = first + (last - first) / 2;
		mystd::move_median_to_first(first, first + 1, mid, last - 1, comp);
		return mystd::unguarded_partition(first + 1, last, first, comp);
	}

	template<typename Iter, typename Cmp>
	inline void
	partial_sort(Iter first,
	               Iter middle,
	               Iter last,
	               Cmp comp)
	{
		mystd::heap_select(first, middle, last, comp);
		// TODO calling lib here!
		std::sort_heap(first, middle, comp);
	}

	/// This is a helper function for the sort routine.
	template<typename Iter, typename Size, typename Cmp>
	void
	introsort_loop(Iter first, Iter last, Size depth_limit, Cmp comp)
	{
		while (last - first > int(_S_threshold))
		{
			if (depth_limit == 0)
			{
				mystd::partial_sort(first, last, last, comp);
				return;
			}
			--depth_limit;
			Iter cut = mystd::unguarded_partition_pivot(first, last, comp);
			mystd::introsort_loop(cut, last, depth_limit, comp);
			last = cut;
		}
	}

	// sort

	template<typename Iter, typename Cmp>
	inline void
	sort(Iter first, Iter last,
	       Cmp comp)
	{
		if (first != last)
		{
			mystd::introsort_loop(first, last,
			                      std::__lg(last - first) * 2,
			                      comp);
			mystd::final_insertion_sort(first, last, comp);
		}
	}

	template<typename Iter, typename Size, typename Cmp>
	void
	introselect(Iter first, Iter nth,
	              Iter last, Size depth_limit,
	              Cmp comp)
	{
		while (last - first > 3)
		{
			if (depth_limit == 0)
			{
				mystd::heap_select(first, nth + 1, last, comp);
				// Place the nth largest element in its final position.
				std::iter_swap(first, nth);
				return;
			}
			--depth_limit;
			Iter cut = mystd::unguarded_partition_pivot(first, last, comp);
			if (cut <= nth)
				first = cut;
			else
				last = cut;
		}
		mystd::insertion_sort(first, last, comp);
	}

	// nth_element





	/**
    *  @brief Sort a sequence just enough to find a particular position.
    *  @ingroup sorting_algorithms
    *  @param  first   An iterator.
    *  @param  nth     Another iterator.
    *  @param  last    Another iterator.
    *  @return  Nothing.
    *
    *  Rearranges the elements in the range @p [first,last) so that @p *nth
    *  is the same element that would have been in that position had the
    *  whole sequence been sorted. The elements either side of @p *nth are
    *  not completely sorted, but for any iterator @e i in the range
    *  @p [first,nth) and any iterator @e j in the range @p [nth,last) it
    *  holds that *j < *i is false.
   */
	template<typename Iter>
	inline void
	nth_element(Iter first, Iter nth,
	            Iter last)
	{
		if (first == last || nth == last)
			return;

		mystd::introselect(first, nth, last,
		                   std::__lg(last - first) * 2,
		                   __gnu_cxx::__ops::__iter_less_iter());
	}

	/**
    *  @brief Sort a sequence just enough to find a particular position
    *         using a predicate for comparison.
    *  @ingroup sorting_algorithms
    *  @param  first   An iterator.
    *  @param  nth     Another iterator.
    *  @param  last    Another iterator.
    *  @param  comp    A comparison functor.
    *  @return  Nothing.
    *
    *  Rearranges the elements in the range @p [first,last) so that @p *nth
    *  is the same element that would have been in that position had the
    *  whole sequence been sorted. The elements either side of @p *nth are
    *  not completely sorted, but for any iterator @e i in the range
    *  @p [first,nth) and any iterator @e j in the range @p [nth,last) it
    *  holds that @p comp(*j,*i) is false.
   */
	template<typename Iter, typename Cmp>
	inline void
	nth_element(Iter first, Iter nth,
	            Iter last, Cmp comp)
	{

		if (first == last || nth == last)
			return;

		mystd::introselect(first, nth, last,
		                   std::__lg(last - first) * 2,
		                   __gnu_cxx::__ops::__iter_comp_iter(comp));
	}

	/**
    *  @brief Sort the elements of a sequence.
    *  @ingroup sorting_algorithms
    *  @param  first   An iterator.
    *  @param  last    Another iterator.
    *  @return  Nothing.
    *
    *  Sorts the elements in the range @p [first,last) in ascending order,
    *  such that for each iterator @e i in the range @p [first,last-1),
    *  *(i+1)<*i is false.
    *
    *  The relative ordering of equivalent elements is not preserved, use
    *  @p stable_sort() if this is needed.
   */
	template<typename Iter>
	inline void
	sort(Iter first, Iter last)
	{
		mystd::sort(first, last, __gnu_cxx::__ops::__iter_less_iter());
	}

	/**
    *  @brief Sort the elements of a sequence using a predicate for comparison.
    *  @ingroup sorting_algorithms
    *  @param  first   An iterator.
    *  @param  last    Another iterator.
    *  @param  comp    A comparison functor.
    *  @return  Nothing.
    *
    *  Sorts the elements in the range @p [first,last) in ascending order,
    *  such that @p comp(*(i+1),*i) is false for every iterator @e i in the
    *  range @p [first,last-1).
    *
    *  The relative ordering of equivalent elements is not preserved, use
    *  @p stable_sort() if this is needed.
   */
//	template<typename Iter, typename Cmp>
//	inline void
//	sort(Iter first, Iter last,
//	     Cmp comp)
//	{
//		mystd::sort(first, last, __gnu_cxx::__ops::__iter_comp_iter(comp));
//	}


} // namespace



#endif //MERGESORTS_GNU_STL_SORT_H
