//
// Created by seb on 6/15/18.
//

#ifndef MERGESORTS_OPTIMAL_BOTTOM_UP_MERGESORT_H
#define MERGESORTS_OPTIMAL_BOTTOM_UP_MERGESORT_H


#include "../algorithms.h"
#include "insertionsort.h"
#include "merging.h"

//#define DEBUG_SORTING


/**
 * Refined bottom-up mergesort implementation that combines the last run with
 * the second-to-last if it is smaller.
 *
 * Merging starts after forming runs of length minRunLen.
 * If doSortedCheck is true, we check if two runs are by chance already
 * in sorted order before two runs are merged (compare last of left run with
 * first of right run)
 *
 * @author Sebastian Wild (wild@uwaterloo.ca)
 */
namespace algorithms {

	template<typename Iterator, unsigned int minRunLen = 24, bool doSortedCheck = true>
	class optimal_bottom_up_mergesort final : public sorter<Iterator> {
	private:
		using typename sorter<Iterator>::elem_t;
		using typename sorter<Iterator>::diff_t;
		std::vector<elem_t> _buffer;
	public:

		void sort(Iterator begin, Iterator end) override {
			_buffer.resize(end - begin);
			mergesort(begin, end);
		}

		bool even(long n) {
			return (n & 1) == 0;
		}


		void debug(Iterator begin, Iterator end, Iterator l, Iterator m, Iterator r) {
#ifdef DEBUG_SORTING
			std::cout << " ";
			for (Iterator j = begin; j < end; ++j) {
				std::cout << (j - begin) << "\t";
			}
			std::cout << " \n";

			std::cout << "[";
			for (Iterator j = begin; j < end; ++j) {
				std::cout << *j << "\t";
			}
			std::cout << "]\n";

			std::cout << " ";
			for (Iterator j = begin; j < end; ++j) {
				if (l <= j && j < m)
					std::cout << "L" << "\t";
				else if (m <= j && j < r)
					std::cout << "R" << "\t";
				else std::cout << "  \t";
			}
			std::cout << " \n\n";
#endif
		}


	/** the actual sort; uses [begin,end) */
		void mergesort(Iterator begin, Iterator end) {
			size_t n = end - begin;
			size_t lastRunLen = minRunLen;
			if (minRunLen != 1) {
				Iterator i = begin;
				for (size_t len = minRunLen; i < end; i += len) {
					Iterator runEnd = std::min(i + len, end);
					insertionsort(i, runEnd);
					lastRunLen = runEnd - i;
				}
			}
			for (size_t len = minRunLen; len < n; len *= 2) {
				assert( (n-lastRunLen) % len == 0 );
				long nOrdRuns = (n-lastRunLen) / len;
				if (nOrdRuns == 0) break;
				Iterator beginTail;
#ifdef DEBUG_SORTING
				std::cout << "len = " << len << std::endl;
				std::cout << "nOrdRuns = " << nOrdRuns << std::endl;
				std::cout << "lastRunLen = " << lastRunLen << std::endl;
#endif
				if (even(nOrdRuns)) { // last small run would remain lonely
					beginTail = end - lastRunLen - 2*len;
					if (lastRunLen < len) { // merge last 3 runs
						//  ...|########|########|######
						//               i1       m1    end
						//      i2       m2             end
						Iterator i1 = beginTail + len, m1 = i1 + len;
						debug(begin,end,i1,m1,end);
						if (!doSortedCheck || *(m1 - 1) > *m1)
							merge_runs(i1, m1, end, _buffer.begin());
						Iterator i2 = beginTail, m2 = i1;
						debug(begin,end,i2,m2,end);
						if (!doSortedCheck || *(m2 - 1) > *m2)
							merge_runs(i2, m2, end, _buffer.begin());
						lastRunLen += 2 * len;
					} else { // last run can stay as is, only merge last two ordinary runs
						//  ...|########|########|######
						//      i        m        end
						Iterator i = beginTail, m = i + len;
						debug(begin,end,i,m,i+2*len);
						if (!doSortedCheck || *(m - 1) > *m)
							merge_runs(i, m, i + 2*len, _buffer.begin());
					}
				} else { // last run not lonely -> merge with last ordinary run
					beginTail = end - lastRunLen - len;
					//  ...|########|######
					//      i        m     end
					Iterator i = beginTail, m = i + len;
					debug(begin,end,i,m,end);
					if (!doSortedCheck || *(m - 1) > *m)
						merge_runs(i, m, end, _buffer.begin());
					lastRunLen += len;
				}
				// do the ordinary merges
				for (Iterator i = begin; i < beginTail; i += len + len) {
					Iterator m = i + len;
					debug(begin,end,i,m,i+2*len);
					if (!doSortedCheck || *(m - 1) > *m)
						merge_runs(i, m, i + 2*len, _buffer.begin());
				}
			}
		}

		std::string name() const override {
			return "OptimalBottomUpMergesort+minRunLen=" + std::to_string(minRunLen) +
			       "+checkSorted=" + std::to_string(doSortedCheck);
		}
	};

}


#endif //MERGESORTS_OPTIMAL_BOTTOM_UP_MERGESORT_H
