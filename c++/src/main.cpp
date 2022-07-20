#include <iostream>
#include <vector>
#include <memory>
#include <iomanip>
#include <fstream>
#include <chrono>

#include "algorithms.h"
#include "inputs.h"
#include "welford.h"
#include "sorts/top_down_mergesort.h"
#include "sorts/bottom_up_mergesort.h"
#include "sorts/peeksort.h"
#include "sorts/powersort.h"
#include "sorts/timsort.h"
#include "sorts/trotsort.h"
#include "sorts/boustrophedonic_mergesort.h"
#include "sorts/optimal_bottom_up_mergesort.h"
#include "sorts/quicksort.h"

static bool ABORT_IF_RESULT_NOT_SORTED = true;

long long volatile totalComparisons = 0ll;

class comp_counter {
	int _value;
public:
	comp_counter(int _value = 0) : _value(_value) {}

	comp_counter(comp_counter const & other) = default;
	comp_counter(comp_counter && other) = default;
	comp_counter & operator=(comp_counter const & rhs) = default;

	bool operator<(const comp_counter &rhs) const {
		++totalComparisons;
		return _value < rhs._value;
	}

	bool operator==(const comp_counter &rhs) const { return _value == rhs._value; }
	bool operator!=(const comp_counter &rhs) const { return !(rhs == *this); }

	bool operator>(const comp_counter &rhs) const { return rhs < *this; }
	bool operator<=(const comp_counter &rhs) const { return !(rhs < *this); }
	bool operator>=(const comp_counter &rhs) const { return !(*this < rhs); }


	friend std::ostream &operator<<(std::ostream &os, const comp_counter &counter) {
		os << counter._value; return os;
	}

	comp_counter & operator+=(comp_counter const &rhs) {
		_value += rhs._value; return *this;
	}

};


template<typename Iterator>
std::vector<std::unique_ptr<algorithms::sorter<Iterator>>> contestants() {
	std::vector<std::unique_ptr<algorithms::sorter<Iterator>>> algos;

	algos.push_back(std::make_unique<algorithms::quicksort<Iterator, 24, 128, false>>());
	algos.push_back(std::make_unique<algorithms::quicksort<Iterator, 24, 100000000, false>>());
	algos.push_back(std::make_unique<algorithms::quicksort<Iterator, 24, 128, true>>());

	algos.push_back(std::make_unique<algorithms::powersort<Iterator, 24, false, algorithms::MOST_SIGNIFICANT_SET_BIT>>());


//	algos.push_back(std::make_unique<algorithms::optimal_bottom_up_mergesort<Iterator, 1, false>>());
//	algos.push_back(std::make_unique<algorithms::top_down_mergesort<Iterator, 1, false>>());
//	algos.push_back(std::make_unique<algorithms::boustrophedonic_mergesort<Iterator, 1, false>>());

	algos.push_back(std::make_unique<algorithms::boustrophedonic_mergesort<Iterator, 24, true>>());
//	algos.push_back(std::make_unique<algorithms::boustrophedonic_mergesort<Iterator, 12, true>>());
	algos.push_back(std::make_unique<algorithms::boustrophedonic_mergesort<Iterator, 1, false>>());

	algos.push_back(std::make_unique<algorithms::top_down_mergesort<Iterator, 24, true>>());
	algos.push_back(std::make_unique<algorithms::top_down_mergesort<Iterator, 1, true>>());
	algos.push_back(std::make_unique<algorithms::top_down_mergesort<Iterator, 1, false>>());

	algos.push_back(std::make_unique<algorithms::bottom_up_mergesort<Iterator, 24, true>>());
//	algos.push_back(std::make_unique<algorithms::bottom_up_mergesort<Iterator, 12, true>>());
	algos.push_back(std::make_unique<algorithms::bottom_up_mergesort<Iterator, 1, true>>());
	algos.push_back(std::make_unique<algorithms::bottom_up_mergesort<Iterator, 1, false>>());

	algos.push_back(std::make_unique<algorithms::optimal_bottom_up_mergesort<Iterator, 24, true>>());
//	algos.push_back(std::make_unique<algorithms::optimal_bottom_up_mergesort<Iterator, 12, true>>());
	algos.push_back(std::make_unique<algorithms::optimal_bottom_up_mergesort<Iterator, 1, true>>());
	algos.push_back(std::make_unique<algorithms::optimal_bottom_up_mergesort<Iterator, 1, false>>());

	algos.push_back(std::make_unique<algorithms::peeksort<Iterator, 24>>());
	algos.push_back(std::make_unique<algorithms::peeksort<Iterator, 1>>());

	algos.push_back(std::make_unique<algorithms::powersort<Iterator, 24, false, algorithms::MOST_SIGNIFICANT_SET_BIT>>());
//	algos.push_back(std::make_unique<algorithms::powersort<Iterator, 12, false, algorithms::MOST_SIGNIFICANT_SET_BIT>>());
//	algos.push_back(std::make_unique<algorithms::powersort<Iterator, 1, false, algorithms::TRIVIAL>>());
//	algos.push_back(std::make_unique<algorithms::powersort<Iterator, 1, false, algorithms::DIVISION_LOOP>>());
//	algos.push_back(std::make_unique<algorithms::powersort<Iterator, 1, false, algorithms::BITWISE_LOOP>>());
	algos.push_back(std::make_unique<algorithms::powersort<Iterator, 1, false, algorithms::MOST_SIGNIFICANT_SET_BIT>>());

	algos.push_back(std::make_unique<algorithms::trotsort<Iterator, false>>());
	algos.push_back(std::make_unique<algorithms::trotsort<Iterator, true>>());

	algos.push_back(std::make_unique<algorithms::timsort<Iterator>>());

	algos.push_back(std::make_unique<algorithms::std_sort<Iterator>>());
	algos.push_back(std::make_unique<algorithms::std_stable_sort<Iterator>>());

	algos.push_back(std::make_unique<algorithms::nop<Iterator>>());

	for (const auto &algo : algos) {
		std::cout << "algo = " << *algo << std::endl;
	}

	return algos;

}

template<typename Elem>
void timeSorts(int reps, std::vector<int> sizes, unsigned long seed, inputs::input_generator<Elem> & inputs,
               std::string outFileName) {
	std::ofstream csv;
	std::string filename;
	{ // Construct filename
		std::ostringstream longFilename;
		std::time_t now = std::time(nullptr);
		std::tm tm = *std::localtime(&now);
		longFilename << outFileName;
		longFilename << std::put_time(&tm, "-%Y-%m-%d_%H-%M-%S");
		longFilename << "-reps" << reps;
		longFilename << "-ns";
		for (int n : sizes) longFilename << "-" << n;
		longFilename << "-seed" << seed;
		longFilename << "-elemT" << typeid(Elem).name();
		longFilename << ".csv";
		filename = longFilename.str();
	}
	csv.open(filename);

	if (typeid(Elem).hash_code() == typeid(comp_counter).hash_code()) {
		csv << "algo,ms,n,input,input-num,merge-cost,comparisons" << std::endl;
		std::cout << "Counting comparisons." << std::endl;
	} else {
		csv << "algo,ms,n,input,input-num,merge-cost" << std::endl;
		std::cout << "Not counting comparisons." << std::endl;
	}
	std::cout << "Counting merge costs." << std::endl;
	if (!csv.is_open()) {
		std::cout << "Could not open file " << filename << " for writing! Exiting." << std::endl;
		exit(1);
	}


	auto algos = contestants<Elem *>();

	// Dump config
	std::cout << "algos = [ ";
	for (auto &&algo : algos) std::cout << algo->name() << " ";
	std::cout << "]" << std::endl;
	std::cout << "sizes = [";
	for (int size : sizes) std::cout << size << " ";
	std::cout << "]" << std::endl;
	std::cout << "reps = " << reps << std::endl;
	std::cout << "seed = " << seed << std::endl;
	std::cout << "inputs = " << inputs << std::endl;
	std::cout << "Writing to " << filename << std::endl;
	std::cout << "Sorting " << typeid(Elem).name() << "s" << std::endl;


	std::cout << "\nRuns with individual timing (skips first run):" << std::endl;

	for (auto &&algo : algos) {
		inputs::RNG rng(seed);
		for (int size : sizes) {
			welford_variance samples;
			Elem total = 0;
			Elem *input = inputs.next(size, rng, nullptr);
			for (int r = 0; r < reps; ++r) {
				if (r != 0) input = inputs.next(size, rng, input);
				algorithms::totalMergeCosts = 0;
				totalComparisons = 0;

				auto begin = std::chrono::high_resolution_clock::now();
//			    (*algo)(input, input + n-1);
				algo->sort(input, input + size);
				auto end = std::chrono::high_resolution_clock::now();
				long long int nCmps = totalComparisons;
				total += input[size/2];
				if (algo->is_real_sort()) {
					if (!std::is_sorted(input, input + size)) {
						std::cerr << "Input not sorted! " << algo->name() << std::endl;
						exit(3);
					}
				}
				double msDiff = std::chrono::duration_cast<std::chrono::nanoseconds>(end-begin).count() / 1e6;
				if (r != 0) {
					// Skip first iteration, slower because of cold cache.
					samples.add_sample(msDiff);
					csv << algo->name() << "," << msDiff << "," << size << "," << inputs.name() << "," << r << "," << algorithms::totalMergeCosts;
					if (typeid(Elem).hash_code() == typeid(comp_counter).hash_code()) {
						csv << "," << nCmps;
					}
					csv << std::endl;
					csv.flush();
				}
			}
			std::cout << "avg-ms=" << (float) (samples.mean()) << ",\t algo=" << algo->name() << ", n=" << size << "     (" << total<<")\t" << samples << std::endl;

			delete[] input;
		}

	}

	std::time_t now = std::time(nullptr);
	std::tm tm = *std::localtime(&now);
	csv << "#finished: "<< std::put_time(&tm, "-%Y-%m-%d_%H-%M-%S") << std::endl;
	csv.close();
}

#ifndef ELEM_T
#define ELEM_T int
#endif

typedef ELEM_T elem_t;

int main(int argc, char **argv) {
	if (argc == 1) {
		std::cout << "Usage: mergesorts [reps] [n1,n2,n3] [seed] [inputs] [outfile] [elem_t]" << std::endl;
	}

	int reps = 51;
	if (argc >= 2) {
		reps = std::atoi(argv[1]);
	}
	std::vector<int> sizes{100000};
	if (argc >= 3) {
		sizes.clear();
		std::stringstream ns { argv[2] };
		while (ns.good()) {
			std::string substr;
			std::getline( ns, substr, ',' );
			sizes.push_back( std::stoi(substr) );
		}
	}
	unsigned long seed = 4242424242ul;
	if (argc >= 4) {
		seed = std::atol(argv[3]);
	}
	inputs::input_generator<elem_t> *inputs =
			new inputs::random_permutations_generator<elem_t>{};
	if (argc >= 5) {
		std::string ins {argv[4]};
		delete inputs;
		if (ins == "rp" || ins == "random-permutations")
			inputs = new inputs::random_permutations_generator<elem_t> {};
		if (ins.substr(0,4) == "runs")
			inputs = new inputs::random_runs_generator<elem_t> (
					std::stoi(ins.substr(4)) );
		if (ins.substr(0,7) == "timdrag")
			inputs = new inputs::timsort_drag_generator<elem_t>(
					std::stoi(ins.substr(7)));

	}
	std::string filename("times");
	if (argc >= 6) {
		filename = std::string(argv[5]);
	}
	timeSorts<elem_t>(reps, sizes, seed, *inputs, filename);

	delete inputs;

	return 0;
}
