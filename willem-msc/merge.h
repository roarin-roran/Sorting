//merge.h
#ifndef MERGE_H
#define MERGE_H

#include <math.h>
typedef std::vector<int>::iterator Iter;
namespace algorithms
{
    void merge_run2(Iter l, Iter m, Iter r, Iter B)
    {
        std::copy(l, m, B);
        *(B + (m - l)) = INT_MAX;
        std::copy(m, r, B + (m - l + 1));
        *(B + (r - l) + 1) = INT_MAX;
        Iter i, j;
        i = B;
        j = B + (m - l + 1);
        for (Iter k = l; k < r; ++k)
        {
            if (*i <= *j)
            {
                *k = *i;
                i++;
            }
            else
            {
                *k = *j;
                j++;
            }
        }
    }

    void merge4way3(Iter l, Iter g1, Iter g2, Iter g3, Iter r, Iter B)
    {

        std::copy(l, g1, B);
        *(B + (g1 - l)) = INT_MAX;
        std::copy(g1, g2, B + (g1 - l) + 1);
        *(B + (g2 - l) + 1) = INT_MAX;
        std::copy(g2, g3, B + (g2 - l) + 2);
        *(B + (g3 - l) + 2) = INT_MAX;
        std::copy(g3, r, B + (g3 - l) + 3);
        *(B + (r - l) + 3) = INT_MAX;
        int size = r - l;
        Iter a, b, c, d;
        a = B, b = B + (g1 - l) + 1, c = B + (g2 - l) + 2, d = B + (g3 - l) + 3;
        std::pair<int, int> x, y, z;
        if (*a <= *b)
        {
            x = {*a, 1};
            a++;
        }
        else
        {
            x = {*b, 1};
            b++;
        }
        if (*c <= *d)
        {
            y = {*c, 2};
            c++;
        }
        else
        {
            y = {*d, 2};
            d++;
        }
        if (x.first <= y.first)
        {
            z = x;
        }
        else
        {
            z = y;
        }
        *l = z.first;
        l++;
        for (auto i = 1; i < size; i++)
        {
            switch (z.second)
            {
            case 1:
                if (*a <= *b)
                {
                    x = {*a, 1};
                    a++;
                }
                else
                {
                    x = {*b, 1};
                    b++;
                }
                break;

            case 2:
                if (*c <= *d)
                {
                    y = {*c, 2};
                    c++;
                }
                else
                {
                    y = {*d, 2};
                    d++;
                }
                break;
            }
            if (x.first <= y.first)
            {
                z = {x.first, x.second};
            }
            else
            {
                z = {y.first, y.second};
            }
            *l = z.first;
            l++;
        }
    }

}

#endif