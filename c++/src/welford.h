//
// Implementation of Welford's streaming algorithm to compute the variance
// Created by seb on 5/19/18.
//

#ifndef MERGESORTS_WELFORD_H
#define MERGESORTS_WELFORD_H

#include <iostream>
#include <cmath>

/**
 * Simple implementation of Welford's algorithm for
 * online-computation of the variance of a stream.
 *
 * see http://jonisalonen.com/2013/deriving-welfords-method-for-computing-variance/
 *
 * @author Sebastian Wild (wild@uwaterloo.ca)
 */
class welford_variance
{
private:
	int _nSamples = 0;
	double _mean = 0, _squaredError = 0;

public:
	void add_sample(double x)
	{
		++_nSamples;
		double oldMean = _mean;
		_mean += (x - _mean) / _nSamples;
		_squaredError += (x - _mean) * (x - oldMean);
	}

	double mean() const {
		return _mean;
	}

	int nSamples() const {
		return _nSamples;
	}

	double variance() const {
		return _squaredError / (_nSamples - 1);
	}

	double stdev() const {
		return std::sqrt(variance());
	}

	friend std::ostream & operator<< (std::ostream & out, const welford_variance & welford) {
		out << "(n=" << welford._nSamples <<
		       ", µ=" << (float) welford.mean() <<
		       ", σ=" << (float) welford.stdev() << ')';
		return out;
	}

};

#endif //MERGESORTS_WELFORD_H
