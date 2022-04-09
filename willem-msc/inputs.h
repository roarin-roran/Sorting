#ifndef INPUTS_H
#define INPUTS_H

#include <random>
#include <algorithm>
#include <iostream>

namespace inputs
{

    std::mt19937_64 RNG;

    std::vector<int> random_vector(int a, int b, int length)
    {

        std::vector<int> v;
        std::uniform_int_distribution<int> distribution(a, b);

        for (int i = 0; i < length; i++)
        {
            v.push_back(distribution(RNG));
        }
        return v;
    }



    void run_sort(std::vector<int>::iterator l, std::vector<int>::iterator r, int expRunLen)
    {

        //std::default_random_engine generator;
        //std::normal_distribution<double> distribution(expRunLen, 600);
        std::geometric_distribution<int> distribution(1.0/expRunLen);
        

        while (l < r)
        {
            int len = floor(distribution(RNG)) + 1;
            //std::cout << len << std::endl;
            if (l + len > r)
            {
                len = r - l;
            }
            std::stable_sort(l, l + len);
            l = l + len;
        }
    }
    

    



}

#endif //INPUTS_H
