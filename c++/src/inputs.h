//
// Created by seb on 5/19/18.
//

#ifndef MERGESORTS_INPUTS_H
#define MERGESORTS_INPUTS_H

#include <random>
#include <algorithm>
#include <cassert>

namespace inputs {

		typedef std::mt19937_64 RNG;

	int next_int(int m, RNG& rng) {
		return std::uniform_int_distribution<int>(0,m-1)(rng);
	}

	template<typename Iter>
	void shuffle(Iter A, int n, RNG & random) {
		std::random_shuffle(A, A + n, [&random](int m) {
			return next_int(m, random);
		});
	}

	template<typename Iter>
	void fill_with_iid_uary(Iter start, Iter end, int u, RNG & random) {
		std::uniform_int_distribution<int> dist(1,u);
		for (auto i = start; i != end ; ++i) *i = dist(random);
	}


	// Create a bigger data type to play with
	template<int size> class blob {
	public:
		int a[size];

		blob(int v) {
			a[0] = v;
			for (int i = 1; i < size; ++i) a[i] = v+i;
		}
		blob() {
			a[0] = 0;
			for (int i = 1; i < size; ++i) a[i] = i;
		}
		bool operator<(const blob &rhs) const { return a[0] < rhs.a[0]; }
		bool operator>(const blob &rhs) const { return a[0] > rhs.a[0]; }
		bool operator<=(const blob &rhs) const { return a[0] <= rhs.a[0]; }
		bool operator>=(const blob &rhs) const { return a[0] >= rhs.a[0]; }
		friend std::ostream &operator<<(std::ostream &os, const blob &blob1) { return os << "b" << blob1.a[0]; }
	};

	typedef blob<8> blob32b;
	typedef blob<32> blob128b;


	template<typename Elem>
	struct input_generator {
		virtual Elem * newInstance(int n, RNG & random) = 0;
		virtual Elem * next(int n, RNG & random, Elem * A) {
			return A == nullptr ?
			       newInstance(n, random) :
			       reuseInstance(n, A, random);
		}
		virtual Elem *reuseInstance(int n, Elem *A, RNG &random) {
			if (A != nullptr) delete[] A;
			return newInstance(n, random);
		}

		virtual std::string name() const = 0;

		friend std::ostream &operator<<(std::ostream &os, const input_generator &input_gen) {
			os << input_gen.name();
			return os;
		}

		virtual ~input_generator() = default;
	};

	/**
	 * Sorts segments of random lengths in [start..end)
	 * where each length is drawn iid Geo(expRunLen).
	 */
	template<typename Iter>
	void sort_random_runs(Iter begin, Iter end, int expRunLen, RNG & rng) {
		std::uniform_int_distribution<int> dis(0,expRunLen) ;
		for (Iter i = begin; i < end;) {
			Iter j = i + 1;
			while (dis(rng) != 0)
				if (j == end) break; else ++j;
			std::sort(i, j);
			i = j;
		}
	}

	/**
	 * Allocates a new array and fills it with a random permutation
	 * of [1..n].
	 * requires a conversion from int to Elem.
	 */
	template<typename Elem>
	Elem * new_random_permutation(int n, RNG & rng) {
		Elem * A = new Elem[n];
		for (int i = 1; i <= n; ++i) A[i-1] = i;
		shuffle(A, n, rng);
		return A;
	}


	/**
	 * uniformly generated random permutations of [1..n].
	 * requires an (implicit) conversion from int to Elem
	 **/
	template<typename Elem>
	struct random_permutations_generator final : input_generator<Elem> {

		Elem * newInstance(int n, RNG &random) override {
			return new_random_permutation<Elem>(n, random);
		}

		Elem * reuseInstance(int n, Elem *A, RNG &random) override {
			shuffle(A, n, random);
			return A;
		}

		std::string name() const override {
			return "random-permutations";
		}
	};

	/**
	 * random runs of a fixed expected run length.
	 *
	 * They are generated by first shuffling the array randomly and then
	 * sorting segments of random lengths, where the lengths of the
	 * segments are iid Geometric(1/runLen) distributed.
	 *
	 * requires an (implicit) conversion from int to Elem
	 **/
	template<typename Elem>
	struct random_runs_generator final : input_generator<Elem>
	{
		const int _runLen;

		explicit random_runs_generator(const int runLen) : _runLen(runLen) {}

		Elem *newInstance(int n, RNG &random) override {
			Elem * A = new_random_permutation<Elem>(n, random);
			sort_random_runs(A, A+n-1, _runLen, random);
			return A;
		}

		Elem *reuseInstance(int n, Elem *A, RNG &random) override {
			shuffle(A, n, random);
			sort_random_runs(A, A+n-1, _runLen, random);
			return A;
		}

		std::string name() const override {
			return std::string("runs-with-exp-len-") + std::to_string(_runLen);
		}
	};


	template<typename num>
	long total(std::vector<num> l) {
		long result = 0;
		for (auto &&x : l) result += x;
		return result;
	}

	/**
	 * Fills the given array A with a random input that runs of the given list of run
	 * lengths, alternating between ascending and descending runs.
	 * More precisely, the array is first filled with a random permutation
	 * of [1..n], and then for i=0..l-1 segments of runLengths.get(i) * runLenFactor
	 * are sorted ascending when i mod 2 == 0 and descending otherwise
	 * (where l = runLengths.size()).
	 *
	 * The sum of all lengths in runLengths times runLenFactor should be equal to the
	 * length of A.
	 */
	template<typename Iter>
	void fill_with_up_and_down_runs(Iter start, Iter end,
	                                std::vector<int> const & runLengths,
	                                int runLenFactor, RNG& random) {
		int n = end - start;
		assert( total<>(runLengths) * runLenFactor == n);
		for (int i = 0; i < n; ++i) start[i] = i+1;
		shuffle(start, n, random);
		bool reverse = false;
		Iter i = start;
		for (int l : runLengths) {
			int L = l * runLenFactor;
			std::sort(std::max(start,i-1), i+L);
			if (reverse) std::reverse(std::max(start,i-1), i+L);
			reverse = !reverse;
			i += L;
		}
	}



	/** Recursively computes R_Tim(n) (see Buss and Knop 2018) */
	template<typename Consumer>
	void compute_timsort_drag_run_lengths(Consumer out, int n) {
		if (n <= 3) {
			out(n);
			return;
		} else {
			int nPrime = n/2;
			int nPrimePrime = n - nPrime - (nPrime-1);
			compute_timsort_drag_run_lengths(out, nPrime);
			compute_timsort_drag_run_lengths(out, nPrime - 1);
			out(nPrimePrime);
		}
	}




	/**
	 * Arrays with run lengths given by the R_Tim (Buss and Knop 2018)
	 * sequence of run lengths that cause Timsort to do unbalanced merges.
	 *
	 * All run lengths are multiplied by minRunLen, which should be >= 32.
	 * Rationale: R_Tim contains only lengths {1,2,3}, but
	 * Timsort extends runs below a minimal length to that minimal length.
	 * JDK Timsort uses at most 32 here, see {@link Timsort#minRunLength(int)}.
	 *
	 * Even without explicit extension of runs (as in {@link TimsortStrippedDown},
	 * we always have runs of length >= 2 since descending is also allowed.
	 */
	template<typename Elem>
	struct timsort_drag_generator final : input_generator<Elem>
	{
		std::vector<int> _RTimCache;
		int _RTimCacheSize = 0;
		int _minRunLen;

		explicit timsort_drag_generator(const int minRunLen)
				: _minRunLen(minRunLen) {}

		Elem *newInstance(int n, RNG &random) override {
			Elem * A = new Elem[n];
			reuseInstance(n, A, random);
			return A;
		}

		Elem *reuseInstance(int n, Elem *A, RNG &random) override {
			int nn = n / _minRunLen;
			if (_RTimCacheSize != nn) {
				_RTimCache.clear();
				compute_timsort_drag_run_lengths(
						[&](int x)->void{_RTimCache.push_back(x);},
						nn
				);
				_RTimCacheSize = nn;
			}
			fill_with_up_and_down_runs(A, A + n, _RTimCache, _minRunLen, random);
			return A;
		}

		std::string name() const override {
			return std::string("timsort-drag-minRunLen-") + std::to_string(_minRunLen);
		}
	};

}

#endif //MERGESORTS_INPUTS_H
