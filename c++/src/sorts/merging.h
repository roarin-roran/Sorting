//
// Several merging implementations.
//

#ifndef MERGESORTS_MERGING_H
#define MERGESORTS_MERGING_H

namespace algorithms{

	bool COUNT_MERGE_COSTS = true;
	long long volatile totalMergeCosts = 0;


	/**
	 * Merges runs [l..m-1] and [m..r) in-place into [l..r)
	 * based on Sedgewick's bitonic merge (Program 8.2 in Algorithms in C++)
	 * using b as temporary storage.
	 * buffer space at b must be at least r-l.
	 *
	 * This method is not stable as is;
	 * it could be made so using an infinity-sentinel between the runs.
	 *
	 * Micro-benchmark:
	 * http://quick-bench.com/bKOldAZAcD8aWAOaYvBYuVOcM7s
	 */
	template<typename Iter, typename Iter2>
	void merge_runs(Iter l, Iter m, Iter r, Iter2 B) {
		if (COUNT_MERGE_COSTS) totalMergeCosts += (r-l);
		std::copy_backward(l,m,B+(m-l));
		std::reverse_copy(m,r,B+(m-l));
		Iter2 i = B, j = B+(r-l-1);
		for (Iter k = l; k < r; ++k)
			*k = *j < *i ? *j-- : *i++;
	}

	/**
	 * Merges runs [l..m-1] and [m..r) in-place into [l..r)
	 * based on Sedgewick's bitonic merge (Program 8.2 in Algorithms in C++)
	 * using b as temporary storage.
	 * buffer space at b must be at least r-l.
	 *
	 * (same as above, but with manual copy in loops; slightly slower than above)
	 */
	template<typename Iter, typename Iter2>
	void merge_runs_manual_copy(Iter l, Iter m, Iter r, Iter2 B) {
		Iter i1, j1; Iter2 b;
		if (COUNT_MERGE_COSTS) totalMergeCosts += (r-l);
		for (i1 = m-1, b = B+(m-1-l); i1 >= l;) *b-- = *i1--;
		for (j1 = r, b = B+(m-l); j1 > m;) *b++ = *--j1;
		Iter2 i = B, j = B+(r-l-1);
		for (Iter k = l; k < r; ++k)
			*k = *j < *i ? *j-- : *i++;
	}

	/**
	 * Merges runs [l..m-1] and [m..r) in-place into [l..r)
	 * based on Sedgewick's bitonic merge (Program 8.2 in Algorithms in C++)
	 * using b as temporary storage.
	 * buffer space at b must be at least r-l.
	 *
	 * (same as above but with branchless assignments; a good bit slower,
	 * and apparently not needed; recent compilers seem to compile above
	 * to branchless code, as well.)
	 */
	template<typename Iter, typename Iter2>
	void merge_runs_branchless(Iter l, Iter m, Iter r, Iter2 B) {
		if (COUNT_MERGE_COSTS) totalMergeCosts += (r-l);
		std::copy_backward(l,m,B+(m-l));
		std::reverse_copy(m,r,B+(m-l));
		Iter2 i = B, j = B+(r-l-1);
		for (Iter k = l; k < r; ++k) {
			bool const cmp = *j < *i;
			*k = cmp ? *j : *i;
			j -= cmp ? 1 : 0;
			i += cmp ? 0 : 1;
		}
	}

	/**
	 * Merges runs A[l..m-1] and A[m..r] in-place into A[l..r]
	 * by copying the shorter run into temporary storage B and
	 * merging back into A.
	 * B must have space at least min(m-l,r-m+1)
	 */
	template<typename Iter, typename Iter2>
	void merge_runs_copy_half(Iter l, Iter m, Iter r, Iter2 B) {
		int n1 = m-l, n2 = r-m+1;
		if (COUNT_MERGE_COSTS) totalMergeCosts += (n1+n2);
//		if (n1 <= n2) {
//
//			System.arraycopy(A, l, B, 0, n1);
//			int i1 = 0, i2 = m, o = l;
//			while (i1 < n1 && i2 <= r)
//				A[o++] = B[i1] <= A[i2] ? B[i1++] : A[i2++];
//			while (i1 < n1) A[o++] = B[i1++];
//		} else {
//			System.arraycopy(A, m, B, 0, n2);
//			int i1 = m-1, i2 = n2-1, o = r;
//			while (i1 >= l && i2 >= 0)
//				A[o--] = A[i1] <= B[i2] ? B[i2--] : A[i1--];
//			while (i2 >= 0) A[o--] = B[i2--];
//		}
	}

	/** returns maximal i <= end s.t. [begin,i) is weakly increasing */
	template<typename Iterator>
	Iterator weaklyIncreasingPrefix(Iterator begin, Iterator end) {
		while (begin + 1 < end)
			if (*begin <= *(begin + 1)) ++begin;
			else break;
		return begin + 1;
	}

	/** returns minimal i >= begin s.t. [i, end) is weakly increasing */
	template<typename Iterator>
	Iterator weaklyIncreasingSuffix(Iterator begin, Iterator end) {
		while (end - 1 > begin)
			if (*(end - 2) <= *(end - 1)) --end;
			else break;
		return end - 1;
	}

	template<typename Iterator>
	Iterator strictlyDecreasingPrefix(Iterator begin, Iterator end) {
		while (begin + 1 < end)
			if (*begin > *(begin + 1)) ++begin;
			else break;
		return begin + 1;
	}

	template<typename Iterator>
	Iterator strictlyDecreasingSuffix(Iterator begin, Iterator end) {
		while (end - 1 > begin)
			if (*(end - 2) > *(end - 1)) --end;
			else break;
		return end - 1;
	}

	template<typename Iterator>
	Iterator extend_and_reverse_run_right(Iterator begin, Iterator end) {
		Iterator j = begin;
		if (j == end) return j;
		if (j+1 == end) return j+1;
		if (*j > *(j+1)) {
			j = strictlyDecreasingPrefix(begin, end);
			std::reverse(begin, j);
		} else {
			j = weaklyIncreasingPrefix(begin, end);
		}
		return j;
	}




}

#endif //MERGESORTS_MERGING_H
