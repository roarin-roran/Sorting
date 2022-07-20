//
// Created by seb on 5/20/18.
//

#include <cmath>
#include <sorts/peeksort.h>
#include <sorts/powersort.h>
#include <sorts/timsort.h>
#include <sorts/trotsort.h>
#include <boustrophedonic_mergesort.h>
#include <sorts/quicksort.h>
#include "gtest/gtest.h"
#include "merging.h"
#include "insertionsort.h"
#include "top_down_mergesort.h"
#include "bottom_up_mergesort.h"
#include "sorter_harness.h"
#include "checked_vector.h"
#include "optimal_bottom_up_mergesort.h"

std::random_device rd;
inputs::RNG rng(rd());

template<typename Container>
void print(Container const & c) {
	std::cout << "[ ";
	for (auto && x : c) std::cout << x << " ";
	std::cout << "]" << std::endl;
}
template<typename Iter>
void print(Iter start, Iter end) {
	std::cout << "[ ";
	for (Iter i = start; i != end; ++i) std::cout << *i << " ";
	std::cout << "]" << std::endl;
}


struct MergingTest : public ::testing::Test {
	//                                       0  1   2   3   4   5  6  7  8  9    10
	checked_vector<int> v{std::vector<int> {10, 20, 30, 40, 50, 5, 6, 7, 8, 100, 120}};
	checked_vector<int> buffer{std::vector<int>(11)};

	checked_vector<int> v_sorted{std::vector<int> {5, 6, 7, 8, 10, 20, 30, 40, 50, 100, 120}};
};

TEST_F(MergingTest, bitonicMergeExample) {
	auto a = v.begin();
	auto b = buffer.begin();
	algorithms::merge_runs(a, a + 5, a + 10, b);
	ASSERT_TRUE(std::is_sorted(v.begin(),v.end()));
	ASSERT_EQ(v, v_sorted);
}

TEST_F(MergingTest, bitonicBranchlessMergeExample) {
	auto a = v.begin();
	auto b = buffer.begin();
	algorithms::merge_runs_branchless(a, a + 5, a + 10, b);
	ASSERT_TRUE(std::is_sorted(v.begin(),v.end()));
	ASSERT_EQ(v, v_sorted);
}

TEST_F(MergingTest, bitonicManualCopyMergeExample) {
	auto a = v.begin();
	auto b = buffer.begin();
	algorithms::merge_runs_manual_copy(a, a + 5, a + 10, b);
	ASSERT_TRUE(std::is_sorted(v.begin(),v.end()));
	ASSERT_EQ(v, v_sorted);
}


TEST_F(MergingTest, weaklyIncreasingLeft) {
	auto runEnd = algorithms::weaklyIncreasingPrefix(v.begin(), v.end());
	ASSERT_EQ(runEnd, v.begin()+5);
	auto runStart = algorithms::weaklyIncreasingSuffix(v.begin(), v.end());
	ASSERT_EQ(runStart, v.begin()+5);
	auto decEnd = algorithms::strictlyDecreasingPrefix(v.begin(), v.end());
	ASSERT_EQ(decEnd, v.begin()+1);
	auto decBeg = algorithms::strictlyDecreasingSuffix(v.begin(), v.end());
	ASSERT_EQ(decBeg, v.end()-1);

	std::reverse(v.begin(), v.end());
	// 0    1    2  3  4  5   6   7   8   9   10
	// 120, 100, 8, 7, 6, 5 , 50, 40, 30, 20, 10
	decEnd = algorithms::strictlyDecreasingPrefix(v.begin(), v.end());
	ASSERT_EQ(decEnd, v.begin()+6);
	decBeg = algorithms::strictlyDecreasingSuffix(v.begin(), v.end());
	ASSERT_EQ(decBeg, v.begin()+6);

	std::sort(v.begin(), v.end());
	ASSERT_EQ(algorithms::weaklyIncreasingPrefix(v.begin(), v.end()), v.end());
	ASSERT_EQ(algorithms::weaklyIncreasingSuffix(v.begin(), v.end()), v.begin());
}











TEST(insertionsort, example) {
	checked_vector<long> v { std::vector<long> {5,8,0,3,2,-2,4,7,9} };
	algorithms::insertionsort(v.begin(), v.end(), 2);
	ASSERT_TRUE(std::is_sorted(v.begin(),v.end()));
}


TEST(insertionsort, exampleBinary) {
	checked_vector<long> v { std::vector<long> {5,8,0,3,2,-2,4,7,9} };
	algorithms::binary_insertionsort(v.begin(), v.end(), 2);
	ASSERT_TRUE(std::is_sorted(v.begin(),v.end()));
}



























using vec_iter = typename checked_vector<int>::iterator;



TEST(inputs, testNewRandomPerm) {
	int n = 10;
	int *pInt = inputs::new_random_permutation<int>(n, rng);
	std::sort(pInt, pInt + n);
	ASSERT_TRUE(is_one_up_to_n(pInt, pInt+n));
	delete[] pInt;
}

TEST(inputs, testSortUpAndDown) {
	std::vector<float> v (20) ;
	std::vector<int> l {5,4,2,2,7} ;
	inputs::fill_with_up_and_down_runs(v.begin(), v.end(), l, 1, rng);
	auto a = v.begin();
	ASSERT_TRUE(std::is_sorted(a,a+5));
	ASSERT_TRUE(std::is_sorted(a+5,a+5+4, std::greater<>()));
	ASSERT_TRUE(std::is_sorted(a+9,a+9+2));
	ASSERT_TRUE(std::is_sorted(a+11,a+11+2, std::greater<>()));
	ASSERT_TRUE(std::is_sorted(a+13,a+20));
}

TEST(inputs, testTimsortDragLens) {
	std::vector<int> lens {};
	inputs::compute_timsort_drag_run_lengths(
			[&](int x)->void{lens.push_back(x);}, 16);

	std::vector<int> RTim16 {2, 1, 1, 3, 1, 3, 2, 2, 1};
	ASSERT_EQ(lens, RTim16);
}

TEST(inputs, testTimsortDragGenerator) {
	inputs::timsort_drag_generator<int> td (2);
	int *a = td.newInstance(32, rng);
	ASSERT_TRUE(std::is_sorted(a,a+4));
	ASSERT_TRUE(std::is_sorted(a+4,a+4+2, std::greater<>()));
	ASSERT_TRUE(std::is_sorted(a+6,a+6+2));
	ASSERT_TRUE(std::is_sorted(a+8,a+8+6, std::greater<>()));
	ASSERT_TRUE(std::is_sorted(a+14,a+14+2));
	ASSERT_TRUE(std::is_sorted(a+16,a+16+6, std::greater<>()));
	ASSERT_TRUE(std::is_sorted(a+22,a+22+4));
	ASSERT_TRUE(std::is_sorted(a+26,a+26+4, std::greater<>()));
	ASSERT_TRUE(std::is_sorted(a+30,a+30+2));
}












TEST(harness, testHarness){
	algorithms::std_sort<vec_iter> ss;
	ASSERT_TRUE(harness_sorter(ss));
}

TEST(harness, harnessTopDownMergesort) {
	algorithms::top_down_mergesort<vec_iter , 1, false> tdmp;
	ASSERT_TRUE(harness_sorter(tdmp));
	algorithms::top_down_mergesort<vec_iter , 1, true> tdmp2;
	ASSERT_TRUE(harness_sorter(tdmp2));
	algorithms::top_down_mergesort<vec_iter> tdmp3;
	ASSERT_TRUE(harness_sorter(tdmp3));
}

TEST(harness, harnessBottonUpMergesort) {
	algorithms::bottom_up_mergesort<vec_iter, 1, false> basic;
	ASSERT_TRUE(harness_sorter(basic));
	algorithms::bottom_up_mergesort<vec_iter,7, false> withMinRunLen;
	ASSERT_TRUE(harness_sorter(withMinRunLen));
	algorithms::bottom_up_mergesort<vec_iter,1, true> withCheck;
	ASSERT_TRUE(harness_sorter(withCheck));
}

TEST(harness, harnessPeeksort) {
	algorithms::peeksort<vec_iter, 1, false> basic;
//	checked_vector<int> v { std::vector<int> {6, 4, 3, 1, 2, 5} };
//	basic(v.begin(), v.end());
	ASSERT_TRUE(harness_sorter(basic));
	algorithms::peeksort<vec_iter, 8, false> basic8;
	ASSERT_TRUE(harness_sorter(basic8));
	algorithms::peeksort<vec_iter, 1, true> basicInc;
	ASSERT_TRUE(harness_sorter(basicInc));
}


TEST(harness, harnessPowersort) {
	algorithms::powersort<vec_iter> def;
	ASSERT_TRUE(harness_sorter(def));
	algorithms::powersort<vec_iter, 1, false, algorithms::TRIVIAL> basic {};
	ASSERT_TRUE(harness_sorter(basic));
//	checked_vector<int> v { std::vector<int> {6, 4, 3, 1, 2, 5} };
//	basic(v.begin(), v.end());
	algorithms::powersort<vec_iter, 8, false, algorithms::MOST_SIGNIFICANT_SET_BIT> msb {};
	ASSERT_TRUE(harness_sorter(msb));
	algorithms::powersort<vec_iter, 1, true, algorithms::BITWISE_LOOP> inc {};
	ASSERT_TRUE(harness_sorter(inc));

}

TEST(harness, harnessTimsort) {
	algorithms::timsort<vec_iter> tim;
	ASSERT_TRUE(harness_sorter(tim));
}


TEST(harness, harnessTrotsort) {
	algorithms::trotsort<vec_iter> tim;
	ASSERT_TRUE(harness_sorter(tim));
	algorithms::trotsort<vec_iter,true> timBin;
	ASSERT_TRUE(harness_sorter(timBin));
}


TEST(harness, harnessBoustrophedonicMergesort) {
	algorithms::boustrophedonic_mergesort<vec_iter, 1, false> basic;
	for (int n = 11; n>0; n=0) {
//	for (int n = 1; n < 256; ++n) {
		auto *a = inputs::new_random_permutation<int>(n, rng);
		checked_vector<int> v{std::vector<int> {a, a + n}};
		basic(v.begin(), v.end());
		ASSERT_TRUE(std::is_sorted(v.begin(), v.end()));
		delete[] a;
//		std::cout << "mergecosts = " << algorithms::totalMergeCosts << std::endl;
	}


	ASSERT_TRUE(harness_sorter(basic));
	algorithms::boustrophedonic_mergesort<vec_iter,7, false> withMinRunLen;
	ASSERT_TRUE(harness_sorter(withMinRunLen));
	algorithms::boustrophedonic_mergesort<vec_iter,1, true> withCheck;
	ASSERT_TRUE(harness_sorter(withCheck));
}

TEST(harness, harnessOptimalBottomUpMergesort) {
	algorithms::optimal_bottom_up_mergesort<vec_iter, 1, false> basic;
	for (int n = 11; n>0; n=0) {
//	for (int n = 1; n < 256; ++n) {
		auto *a = inputs::new_random_permutation<int>(n, rng);
		checked_vector<int> v{std::vector<int> {a, a + n}};
		basic(v.begin(), v.end());
		ASSERT_TRUE(std::is_sorted(v.begin(), v.end()));
		delete[] a;
//		std::cout << "mergecosts = " << algorithms::totalMergeCosts << std::endl;
	}

	ASSERT_TRUE(harness_sorter(basic));
	algorithms::optimal_bottom_up_mergesort<vec_iter,7, false> withMinRunLen;
	ASSERT_TRUE(harness_sorter(withMinRunLen));
	algorithms::optimal_bottom_up_mergesort<vec_iter,1, true> withCheck;
	ASSERT_TRUE(harness_sorter(withCheck));
}



TEST(harness, harnessQuicksort) {
	algorithms::quicksort<vec_iter, 1, 1000000000, false> basic;
	for (int n = 10; n>0; n=0) {
//	for (int n = 1; n < 256; ++n) {
		auto *a = inputs::new_random_permutation<int>(n, rng);
		checked_vector<int> v{std::vector<int> {a, a + n}};
		basic(v.begin(), v.end());
		ASSERT_TRUE(std::is_sorted(v.begin(), v.end()));
		delete[] a;
//		std::cout << "mergecosts = " << algorithms::totalMergeCosts << std::endl;
	}

	ASSERT_TRUE(harness_sorter(basic));
	algorithms::quicksort<vec_iter,7, 20, false> withMinRunLen;
	ASSERT_TRUE(harness_sorter(withMinRunLen));
	algorithms::quicksort<vec_iter,1, 1000000000, true> withCheck;
	ASSERT_TRUE(harness_sorter(withCheck));
}




TEST(nodePowers, nodePowersExamples) {
	ASSERT_EQ(algorithms::node_power_trivial(1, 100 + 1, 10, 20, 25 + 1), 4);
	ASSERT_EQ(algorithms::node_power_trivial(0, 21 + 1, 8, 12, 13 + 1), 1);
	ASSERT_EQ(algorithms::node_power_trivial(0, 21 + 1, 19, 20, 20 + 1), 5);
	ASSERT_EQ(algorithms::node_power_trivial(0, 100 * 1000 * 1000 + 1, 55555555, 55555666, 55556666 + 1), 16);

	ASSERT_EQ(algorithms::node_power_bitwise(1, 100 + 1, 10, 20, 25 + 1), 4);
	ASSERT_EQ(algorithms::node_power_bitwise(0, 21 + 1, 8, 12, 13 + 1), 1);
	ASSERT_EQ(algorithms::node_power_bitwise(0, 21 + 1, 19, 20, 20 + 1), 5);
	ASSERT_EQ(algorithms::node_power_bitwise(0, 100 * 1000 * 1000 + 1, 55555555, 55555666, 55556666 + 1), 16);

	ASSERT_EQ(algorithms::node_power_clz(1, 100 + 1, 10, 20, 25 + 1), 4);
	ASSERT_EQ(algorithms::node_power_clz(0, 21 + 1, 8, 12, 13 + 1), 1);
	ASSERT_EQ(algorithms::node_power_clz(0, 21 + 1, 19, 20, 20 + 1), 5);
	ASSERT_EQ(algorithms::node_power_clz(0, 100 * 1000 * 1000 + 1, 55555555, 55555666, 55556666 + 1), 16);

	ASSERT_EQ(algorithms::node_power_div(1, 100 + 1, 10, 20, 25 + 1), 4);
	ASSERT_EQ(algorithms::node_power_div(0, 21 + 1, 8, 12, 13 + 1), 1);
	ASSERT_EQ(algorithms::node_power_div(0, 21 + 1, 19, 20, 20 + 1), 5);
	ASSERT_EQ(algorithms::node_power_div(0, 100 * 1000 * 1000 + 1, 55555555, 55555666, 55556666 + 1), 16);

}