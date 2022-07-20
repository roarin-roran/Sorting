//
// Created by seb on 5/26/18.
//

#ifndef MERGESORTS_POWERSORT_H
#define MERGESORTS_POWERSORT_H

#include <cassert>
#include "../algorithms.h"
#include "insertionsort.h"
#include "merging.h"

namespace algorithms {

	/**
	 * Different choices for how to compute node powers.
	 *
	 * Unclear which is better:
	 * http://quick-bench.com/k0dktXw6O9eJ0vz1_G-2KjyrKm0
	 *
	 */
	enum node_power_implementations {
		TRIVIAL,
		DIVISION_LOOP,
		BITWISE_LOOP,
		MOST_SIGNIFICANT_SET_BIT,
	};
	std::string to_string(node_power_implementations implementation) {
		switch (implementation) {
			case TRIVIAL: return "TRIVIAL";
			case DIVISION_LOOP: return "DIVISION_LOOP";
			case BITWISE_LOOP: return "BITWISE_LOOP";
			case MOST_SIGNIFICANT_SET_BIT: return "MOST_SIGNIFICANT_SET_BIT";
		}
		assert(false);
	};


	unsigned node_power_trivial(size_t begin, size_t end,
	                            size_t beginA, size_t beginB, size_t endB) {
		size_t n = end - begin;
		size_t n1 = beginB - beginA, n2 = endB - beginB;
		double a = (beginA - begin + 0.5*n1) / n;
		double b = (beginB - begin + 0.5*n2) / n;
		unsigned k = 0;
		while (true) {
			++k;
			unsigned long twoToK = 1u << k;
			if (floor(a * twoToK) < floor(b * twoToK)) break;
		}
		return k;
	}

	unsigned node_power_div(size_t begin, size_t end,
	                        size_t beginA, size_t beginB, size_t endB) {
		size_t twoN = 2*(end - begin); // 2*n
		size_t n1 = beginB - beginA, n2 = endB - beginB; // lengths of runs
		unsigned long a = 2*beginA + n1 - 2*begin;
		unsigned long b = 2*beginB + n2 - 2*begin;
		unsigned k = 0;
		while (b-a <= twoN && a / twoN == b / twoN) {
//		while (a / twoN == b / twoN) {
			++k;
			a *= 2;
			b *= 2;
		}
		return k;
	}

	unsigned node_power_bitwise(size_t begin, size_t end,
	                            size_t beginA, size_t beginB, size_t endB) {
		size_t n = end - begin;
		assert (n < (1L << 63));
		size_t l = beginA - begin + beginB - begin;
		size_t r = beginB - begin + endB - begin;
		// a and b are given by l/(2*n) and r/(2*n), both are in [0,1).
		// we have to find the number of common digits in the
		// binary representation in the fractional part.
		unsigned nCommonBits = 0;
		bool digitA = l >= n, digitB = r >= n;
		while (digitA == digitB) {
			++nCommonBits;
			if (digitA) { l-= n; r -=n; }
//			l -= digitA ? n : 0; r -= digitA ? n : 0;
			l *= 2; r *= 2;
			digitA = l >= n; digitB = r >= n;
		}
		return nCommonBits + 1;
	}

	unsigned node_power_clz(size_t begin, size_t end,
	                        size_t beginA, size_t beginB, size_t endB) {
		size_t n = end - begin;
		assert(n <= (1L << 31));
		unsigned long l2 = beginA + beginB - 2*begin; // 2*l
		unsigned long r2 = beginB + endB - 2*begin;   // 2*r
		auto a = static_cast<unsigned int>((l2 << 30) / n);
		auto b = static_cast<unsigned int>((r2 << 30) / n);
		return __builtin_clz(a ^ b);
	}

	// not precise enough for large powers ...
	unsigned node_power_clz_unconstrained(ptrdiff_t begin, ptrdiff_t end,
	                                      ptrdiff_t beginA, ptrdiff_t beginB, ptrdiff_t endB) {
		assert(begin <= beginA && beginA <= beginB && beginB <= endB && endB <= end);
		auto n = static_cast<size_t>(end - begin);
		assert(n < (1L << 63));
		auto l2 = static_cast<size_t>((beginA - begin) + (beginB - begin)); // 2*l
		auto r2 = static_cast<size_t>((beginB - begin) + (endB - begin));   // 2*r
		static_assert(sizeof(size_t) == 8, "assume 64bit size_t"); // can compute with 64 bits
		// compute low and high 32 bits separately
		if (n < (1L << 33)) {
			auto a = static_cast<unsigned int>((l2 << 31) / n);
			auto b = static_cast<unsigned int>((r2 << 31) / n);
			return __builtin_clz(a ^ b);
		} else {
			auto ah = static_cast<unsigned int>(l2 / (n >> 31));
			auto bh = static_cast<unsigned int>(r2 / (n >> 31));
			if (ah != bh) {
				return __builtin_clz(ah ^ bh);
			} else {
				size_t nPrime = (n >> 32) * ah;
				size_t ll2 = l2 - nPrime;
				size_t lr2 = r2 - nPrime;
				auto al = static_cast<unsigned int>((ll2 << 32) / (n >> 31));
				auto bl = static_cast<unsigned int>((lr2 << 32) / (n >> 31));
				return 32 + __builtin_clz(al ^ bl);
			}
		}
	}

	unsigned log2(unsigned int n) {
		if (n <= 0) return 0;
		return 31 - __builtin_clz( n );
	}

	unsigned log2(unsigned long n) {
		if (n <= 0) return 0;
		return 63 - __builtin_clzl( n );
	}


	/**
	 * Powersort implementation as described in the paper.
	 *
	 * Natural runs are extended to minRunLen if needed before we continue
	 * merging.
	 * Unless useMsbMergeType is false, node powers are computed using
	 * a most-significant-bit trick;
	 * otherwise a loop is used.
	 * If onlyIncreasingRuns is true, only weakly increasing runs are picked up.
	 *
	 * @author Sebastian Wild (wild@uwaterloo.ca)
	 */
	template<typename Iterator,
			unsigned int minRunLen = 24,
			bool onlyIncreasingRuns = false,
			node_power_implementations nodePowerImplementation = MOST_SIGNIFICANT_SET_BIT
	>
	class powersort final : public sorter<Iterator> {
	private:
		using typename sorter<Iterator>::elem_t;
		using typename sorter<Iterator>::diff_t;
		std::vector<elem_t> _buffer;
		Iterator globalBegin, globalEnd;
		struct run {
			Iterator begin; Iterator end;
			bool operator==(const run &rhs) const {
				return begin == rhs.begin && end == rhs.end;
			}
			bool operator!=(const run &rhs) const { return !(rhs == *this); }
		};
		run NULL_RUN {};
	public:

		void sort(Iterator begin, Iterator end) override {
			_buffer.resize(end - begin);
			globalBegin = begin; globalEnd = end;
			power_sort(begin, end);
		}


		inline unsigned node_power(size_t begin, size_t end,
		                    size_t beginA, size_t beginB, size_t endB) {
			switch (nodePowerImplementation) {
				case MOST_SIGNIFICANT_SET_BIT:
					return node_power_clz(begin, end, beginA, beginB, endB);
				case BITWISE_LOOP:
					return node_power_bitwise(begin, end, beginA, beginB, endB);
				case DIVISION_LOOP:
					return node_power_div(begin, end, beginA, beginB, endB);
				case TRIVIAL:
					return node_power_trivial(begin, end, beginA, beginB, endB);
			}
			assert(false);
			__builtin_unreachable();
		}


		/**
		 * sorts [begin,end), assuming that [begin,leftRunEnd) and
		 * [rightRunBegin,end) are sorted
		 */
		void power_sort(Iterator begin, Iterator end) {
			size_t n = end - begin;
			unsigned lgnPlus2 = log2(n) + 2;
			run runStack[lgnPlus2] = {};
			assert(runStack[0] == NULL_RUN && runStack[lgnPlus2-1] == NULL_RUN);
			unsigned top = 0;

			run runA = {begin, extend_and_reverse_run_right(begin, end)};
			//extend to minRunLen
			diff_t lenA = runA.end - runA.begin;
			if (lenA < minRunLen) {
				runA.end = std::min(end, runA.begin + minRunLen);
				insertionsort(runA.begin, runA.end, lenA);
			}

			while (runA.end < end) {
				run runB = {runA.end, extend_and_reverse_run_right(runA.end, end)};
				//extend to minRunLen
				size_t lenB = runB.end - runB.begin;
				if (lenB < minRunLen) {
					runB.end = std::min(end, runB.begin + minRunLen);
					insertionsort(runB.begin, runB.end, lenB);
				}
				unsigned k = node_power(0, n,
				                        (size_t) (runA.begin-begin),
				                        (size_t) (runB.begin-begin),
				                        (size_t) (runB.end-begin) );
				assert( k != top );
				for (unsigned l = top; l > k; --l) {
					if (runStack[l] == NULL_RUN) continue;
					merge_runs(runStack[l].begin, runStack[l].end, runA.end, _buffer.begin());
					runA.begin = runStack[l].begin;
					runStack[l] = NULL_RUN;
				}
				// store updated runA to be merged with runB at power k
				runStack[k] = runA;
				top = k;
				runA = runB;
			}
			assert(runA.end == end);
			for (unsigned l = top; l > 0; --l) {
				if (runStack[l] != NULL_RUN)
					merge_runs(runStack[l].begin, runStack[l].end, end, _buffer.begin());
			}
		}

		std::string name() const override {
			return "PowerSort+minRunLen=" + std::to_string(minRunLen) +
			       "+nodePowerImplementation=" + to_string(nodePowerImplementation) +
			       "+onlyIncRuns=" + std::to_string(onlyIncreasingRuns);
		}
	};




}

#endif //MERGESORTS_POWERSORT_H
