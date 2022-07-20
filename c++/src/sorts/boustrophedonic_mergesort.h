//
// Created by seb on 6/3/18.
//

#ifndef MERGESORTS_BOUSTROPHEDONIC_MERGESORT_H
#define MERGESORTS_BOUSTROPHEDONIC_MERGESORT_H

#include "../algorithms.h"
#include "insertionsort.h"
#include "merging.h"


//#define DEBUG_SORTING

/**
 * Simple boustrophedonic bottom-up mergesort implementation,
 * that alternatingly does merges forward and backward.
 * That avoids the deficiency of standard bottom-up mergesort
 * that the last run is potentially much shorter than all others.
 *
 * Note that this simple implementation does not produce optimal
 * merge trees (even when starting with length 1);
 * that would require a more complicated rule for exceptional merges;
 * see optimal_bottom_up_mergesort.
 *
 * Merging starts after forming runs of length minRunLen.
 * If doSortedCheck is true, we check if two runs are by chance already
 * in sorted order before two runs are merged (compare last of left run with
 * first of right run)
 *
 * @author Sebastian Wild (wild@uwaterloo.ca)
 */
namespace algorithms {

	template<typename Iterator,
			unsigned int minRunLen = 24,
			bool doSortedCheck = true
	>
	class boustrophedonic_mergesort final : public sorter<Iterator> {
	private:
		using typename sorter<Iterator>::elem_t;
		using typename sorter<Iterator>::diff_t;
		std::vector<elem_t> _buffer;
#ifdef DEBUG_SORTING
		Iterator globalBegin, globalEnd;
#endif
	public:
		void sort(Iterator begin, Iterator end) override {
			_buffer.resize(end - begin);
#ifdef DEBUG_SORTING
			globalBegin = begin; globalEnd = end; // for debug
#endif
			mergesort(begin, end);
		}

		void debug(Iterator begin, Iterator end, Iterator l, Iterator m, Iterator r) {
#ifdef DEBUG_SORTING
			std::cout << " ";
			for (Iterator j = globalBegin; j < globalEnd; ++j) {
				if (begin <= j && j < end)
					std::cout << (j-globalBegin) << "\t";
				else
					std::cout << "  \t";
			}
			std::cout << " \n";

			std::cout << "[";
			for (Iterator j = globalBegin; j < globalEnd; ++j) {
				if (begin <= j && j < end)
					std::cout << *j << "\t";
				else
					std::cout << "  \t";
			}
			std::cout << "]\n";

			std::cout << " ";
			for (Iterator j = globalBegin; j < globalEnd; ++j) {
				if (l <= j && j < m)
					std::cout << "L" << "\t";
				else if (m <= j && j < r)
					std::cout << "R" << "\t";
				else std::cout << "  \t";
			}
			std::cout << " \n\n";
#endif
		}


		void merge_forward(Iterator l, size_t len1, size_t len2, Iterator begin, Iterator end) {
			Iterator m = l + len1, r = std::min(m + len2, end);
			debug(begin, end, l, m, r);
			if (!doSortedCheck || *(m - 1) > *m)
				merge_runs(l, m, r, _buffer.begin());
		}

		void merge_backward(Iterator r, size_t len1, size_t len2, Iterator begin, Iterator end) {
			Iterator m = r - len2, l = std::max(m - len1, begin);
			debug(begin, end, l, m, r);
			if (!doSortedCheck || *(m - 1) > *m)
				merge_runs(l, m, r, _buffer.begin());
		}

		/** the actual sort; uses [begin,end) */
		void mergesort(Iterator begin, Iterator end) {
			size_t n = end - begin;
			if (minRunLen != 1) {
				Iterator i = begin;
				for (size_t len = minRunLen; i < end; i += len)
					insertionsort(i, std::min(i+len, end));
			}
			bool forward = true;
			size_t offsetLeft = 0, offsetRight = 0;
			for (size_t len = minRunLen; len < n; len *= 2) {
#ifdef DEBUG_SORTING
				std::cout << "offsetLeft = " << offsetLeft << std::endl;
				std::cout << "offsetRight = " << offsetRight << std::endl;
#endif
				if (offsetLeft + offsetRight == n) {// last merge
					debug(begin, end, begin, begin + offsetLeft, end);
					return merge_runs(begin, begin + offsetLeft, end, _buffer.begin());
				}
				if ((offsetLeft == 0 ? len : offsetLeft) + (offsetRight == 0 ? len : offsetRight) == n) {
					debug(begin, end, begin, begin + (offsetLeft == 0 ? len : offsetLeft), end);
					return merge_runs(begin, begin + (offsetLeft == 0 ? len : offsetLeft), end, _buffer.begin());
				}
				if (forward) {
					Iterator l = begin;
					if (offsetLeft > 0) { // anomalous first merge at left end
						merge_forward(begin, offsetLeft, len, begin, end);
						l += offsetLeft + len;
						offsetLeft += len;
					}
					for (; l + len < end; l += 2*len) merge_forward(l, len, len, begin, end);
					offsetRight = l <= end ? end - l : end - (l - 2*len);
//					offsetRight = (n-offsetLeft) % (2*minRunLen);
					// if we had an odd number of runs --> merge rightmost two
					size_t nRuns =   (offsetLeft > 0 ? 1 : 0)
					               + (offsetRight > 0 ? 1 : 0)
					               + (n - offsetLeft - offsetRight) / (2*len);
#ifdef DEBUG_SORTING
					std::cout << "nRuns = " << nRuns << std::endl;
					std::cout << "offsetLeft = " << offsetLeft << std::endl;
					std::cout << "offsetRight = " << offsetRight << std::endl;
#endif
					if (nRuns >= 3 && nRuns % 2 == 1) {
						merge_backward(end, 2*len, offsetRight, begin, end);
						offsetRight += 2*len;
					}
				} else {
					Iterator r = end;
					if (offsetRight > 0) { // anomalous first merge at right end
						merge_backward(end, len, offsetRight, begin, end);
						r -= len + offsetRight;
						offsetRight += len;
					}
					for (; r - len > begin; r -= 2*len) merge_backward(r, len, len, begin, end);
//					if ( (n % len == 0 && (n / len) % 2 == 1) || (n % len != 0 && (n / len) % 2 == 0)) {
					offsetLeft = r >= begin ? r - begin : r + 2*len - begin;
//					offsetLeft = (n-offsetRight) % (2*len);
					// if we had an odd number of runs --> merge rightmost two
					size_t nRuns =   (offsetLeft > 0 ? 1 : 0)
					                 + (offsetRight > 0 ? 1 : 0)
					                 + (n - offsetLeft - offsetRight) / (2*len);
					if (nRuns >= 3 && nRuns % 2 == 1) {
						merge_forward(begin, offsetLeft, 2*len, begin, end);
						offsetLeft += 2*len;
					}
				}
				forward = !forward;
			}
		}

		std::string name() const override {
			return std::string("BoustrophedonicMergesort") +
			       "+minRunLen=" + std::to_string(minRunLen) +
			       "+checkSorted=" + std::to_string(doSortedCheck);
		}
	};

}


#endif //MERGESORTS_BOUSTROPHEDONIC_MERGESORT_H
