#include <iostream>
#include <math.h>
#include <cmath>
#include <stack>
#include <algorithm>
#include <iterator>
#include <chrono>
#include <vector>
#include <climits>

#include "inputs.h"
#include "merge.h"

typedef std::vector<int>::iterator Iter;
typedef std::vector<Iter>::iterator Iter2;
static long long mergeCost = 0;

void printVector(Iter l, Iter r)
{
    int size = r - l;
    for (auto i = 0; i < size; i++)
    {
        std::cout << *l << " ";
        l++;
    }
}

void insertionsort(Iter l, Iter r)
{
    Iter i, j;
    int k;

    for (i = l + 1; i < r; i++)
    {

        k = *i;
        j = i - 1;

        while (j >= l && *j > k)
        {
            *(j + 1) = *j;
            j--;
        }
        *(j + 1) = k;
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

Iter extendIncreasingRunRight(Iter l, Iter r)
{
    while (l < r - 1 && *l <= *(l + 1))
        l++;
    return l + 1;
}

Iter extendStrictlyDecreasingRunRight(Iter l, Iter r)
{
    while (l < r - 1 && *l > *(l + 1))
        l++;
    return l + 1;
}

Iter extendIncreasingRunLeft(Iter l, Iter r)
{
    while (l < r && *(r - 1) <= *r)
        r--;
    return r;
}

Iter extendStrictlyDecreasingRunLeft(Iter l, Iter r)
{
    while (l<r &&*(r - 1)> * r)
        r--;
    return r;
}

Iter findEandFlip(Iter l, Iter r)
{
    Iter b, c;
    b = extendIncreasingRunRight(l, r);
    c = extendStrictlyDecreasingRunRight(l, r);
    if (c > b)
    {
        std::reverse(l, c);
        return c;
    }
    else
        return b;
}

Iter findSandFlip(Iter l, Iter r)
{
    Iter b, c;
    b = extendIncreasingRunLeft(l, r);
    c = extendStrictlyDecreasingRunLeft(l, r);
    if (c < b)
    {
        std::reverse(c, r);
        return c;
    }
    else
        return b;
}

void reverseRange(Iter l, Iter r)
{
    r--;
    int t;
    while (l < r)
    {
        t = *l;
        *l = *r;
        *r = t;
        l++;
        r--;
    }
}


void peeksortInsertion(Iter l, Iter r, Iter e, Iter s, Iter b)
{
    
    if (s == l || r == e)
        return;

    if (r - l <= 24)
    {
        insertionsort(l, r);
        return;
    }

    Iter m = l + floor((r - l) / 2);

    if (m < e)
    { 
        peeksortInsertion(e, r, e, s, b);
        merge_run2(l, e, r, b);
        mergeCost += (r - l);
    }
    else if (m > s - 1) 
    {                   
        peeksortInsertion(l, s, e, s, b);
        merge_run2(l, s, r, b);
        mergeCost += (r - l);
    }
    else
    { 
        Iter i, j;

        if (*m <= *(m + 1))
        {
            i = extendIncreasingRunLeft(e, m);
            j = extendIncreasingRunRight(m, s);
        }
        else
        {
            i = extendStrictlyDecreasingRunLeft(e, m);
            j = extendStrictlyDecreasingRunRight(m, s);
            reverseRange(i, j);
        }
        if (i == l && j == r)
            return;

        if (m - i < j - m)
        {
            peeksortInsertion(l, i, e, i, b);
            peeksortInsertion(i, r, j, s, b);
            merge_run2(l, i, r, b);
            mergeCost += (r - l);
        }
        else
        {
            peeksortInsertion(l, j, e, i, b);
            peeksortInsertion(j, r, j, s, b);
            merge_run2(l, j, r, b);
            mergeCost += (r - l);
        }
    }
}

void peeksort4Insertion(Iter l, Iter r, Iter e, Iter s, Iter b)
{

    if (s == l || r == e)
        return;
    if (r - l <= 24)
    {
        insertionsort(l, r);
        return;
    }

    Iter m1 = l + floor((r - l) / 4);
    Iter m2 = l + floor((r - l) / 2);
    Iter m3 = m2 + floor((r - l) / 4);
    Iter i2, j2;
    if (*m2 <= *(m2 + 1))
    {
        i2 = extendIncreasingRunLeft(e, m2);
        j2 = extendIncreasingRunRight(m2, s);
    }
    else
    {
        i2 = extendStrictlyDecreasingRunLeft(e, m2);
        j2 = extendStrictlyDecreasingRunRight(m2, s);
        std::reverse(i2, j2);
    }
    if (i2 == l && j2 == r)
        return;
    Iter g2, g1, g3, i1, i3, j1, j3;
    (m2 - i2 < j2 - m2) ? (g2 = i2) : (g2 = j2);
    if (i2 <= m1)
    {
        g1 = i2;
    }
    else
    {

        if (*m1 >= *(m1 - 1))
        {
            i1 = extendIncreasingRunLeft(e, m1);
            j1 = extendIncreasingRunRight(m1, i2);
        }
        else
        {
            i1 = extendStrictlyDecreasingRunLeft(e, m1);
            j1 = extendStrictlyDecreasingRunRight(m1, i2);
            //left inclusive, right exlusive
            //have j as eclusive
            std::reverse(i1, j1);
        }
        (m1 - i1 < j1 - m1) ? (g1 = i1) : (g1 = j1);
    }

    if (j2 > m3)
    {
        g3 = j2;
    }
    else
    {

        if (*m3 <= *(m3 + 1))
        {
            i3 = extendIncreasingRunLeft(j2, m3);
            j3 = extendIncreasingRunRight(m3, s);
        }
        else
        {
            i3 = extendStrictlyDecreasingRunLeft(j2, m3);
            j3 = extendStrictlyDecreasingRunRight(m3, s);
            //left inclusive, right exlusive
            //have j as eclusive
            std::reverse(i3, j3);
        }
        (m3 - i3 < j3 - m3) ? (g3 = i3) : (g3 = j3);
    }
    peeksort4Insertion(l, g1, e, i1, b);
    peeksort4Insertion(g1, g2, j1, i2, b);
    peeksort4Insertion(g2, g3, j2, i3, b);
    peeksort4Insertion(g3, r, j3, r, b);
    merge4way3(l, g1, g2, g3, r, b);
    mergeCost += (r - l);
}


long int nodePower(Iter s1, Iter s2, Iter s3, Iter l, Iter r)
{
    double n = r - l;
    int n1 = s2 - s1;
    int n2 = s3 - s2;
    long double a = ((s1 - l + n1 / 2.0) / n);
    long double b = ((s2 - l + n2 / 2.0) / n);
    long i = 0;
    while (floor(a * (pow(2, i))) == floor(b * (pow(2, i))))
    {
        i++;
    }
    
    return i;
}

long int nodePower4(Iter s1, Iter s2, Iter s3, Iter l, Iter r)
{
    double n = r - l;
    int n1 = s2 - s1;
    int n2 = s3 - s2;
    long double a = ((s1 - l + n1 / 2.0) / n);
    long double b = ((s2 - l + n2 / 2.0) / n);
    long i = 0;
    while (floor(a * (pow(4, i))) == floor(b * (pow(4, i))))
    {
        i++;
    }

    return i;
}

unsigned node_power_div(long long int l, long long int r,
                        long long int s1, long long int s2, long long int s3)
{
    long long int twoN = 2 * (r - l);                 // 2*n
    long long int n1 = s2 - s1, n2 = s3 - s2; // lengths of runs
    unsigned long a = 2 * s1 + n1 - 2 * l;
    unsigned long b = 2 * s2 + n2 - 2 * l;
    unsigned k = 0;
    while (b - a <= twoN && a / twoN == b / twoN)
    {
        ++k;
        a *= 2;
        b *= 2;
    }
    return k;
}

int powercheck(std::stack<int> powers)
{
    int x = 1;
    int p = powers.top();
    powers.pop();
    while (!powers.empty())
    {
        if (powers.top() == p)
        {
            x++;
            powers.pop();
        }
        else
            break;
    }
    return x;
}

int powercheck2(Iter pow, Iter powStart)
{
    int x = 1;
    Iter p = pow - 1;
    while (p > powStart && pow - p < 3)
    {
        if (*p == *pow)
        {
            x++;
            p--;
        }
        else
            break;
    }
    return x;
}

void powersortBufferInserion(Iter l, Iter r, Iter B)
{
    int cost = 0;
    int n = r - l;
    std::stack<Iter> leftRunStart;
    std::stack<int> powers;
    Iter s1, s2, s3, x;
    s1 = l;
    if (*s1 <= *(s1 + 1))
    {
        s2 = extendIncreasingRunRight(s1, r);
    }
    else
    {
        s2 = extendStrictlyDecreasingRunRight(s1, r);
        reverseRange(s1, s2);
    }
    if (s2 - s1 < 24)
    {
        s2 = std::min(r, s1 + 24);
        insertionsort(s1, s2);
    }
    while (s2 < r)
    {
        if (*s2 <= *(s2 + 1))
        {
            s3 = extendIncreasingRunRight(s2, r);
        }
        else
        {
            s3 = extendStrictlyDecreasingRunRight(s2, s3);
            reverseRange(s2, s3);
        }

        if (s3 - s2 < 24)
        {
            s3 = std::min(r, s2 + 24);
            insertionsort(s2, s3);
        }

        int p = node_power_div(l - l, r - l, s1 - l, s2 - l, s3 - l);
        //int p = nodePower(s1, s2, s3, l, r);

        while (!powers.empty())
        {
            if (powers.top() > p)
            {
                x = leftRunStart.top();
                merge_run2(x, s1, s2, B);
                cost = cost + (s2 - x);
                s1 = x;
                leftRunStart.pop();
                powers.pop();
            }
            else
            {
                break;
            }
        }
        leftRunStart.push(s1);
        powers.push(p);
        s1 = s2;
        s2 = s3;
    }

    while (!leftRunStart.empty())
    {
        merge_run2(leftRunStart.top(), s1, s2, B);
        s1 = leftRunStart.top();
        cost += (s2 - s1);
        leftRunStart.pop();
    }
    mergeCost += cost;
}

void powersortBufferInserion2(Iter l, Iter r, Iter B)
{
    int cost = 0;
    int n = r - l;
    std::vector<Iter> leftRunStart(ceil(log2(n)) + 2);
    Iter powStart = (l + n + 4), pow = powStart, s1, s2, s3, x;
    Iter2 lrsStart = leftRunStart.begin(), lrs = lrsStart;
    int p;
    s1 = l;

    if (*s1 <= *(s1 + 1))
    {
        s2 = extendIncreasingRunRight(s1, r);
    }
    else
    {
        s2 = extendStrictlyDecreasingRunRight(s1, r);
        reverseRange(s1, s2);
    }

    if (s2 - s1 < 24)
    {
        s2 = std::min(r, s1 + 24);
        insertionsort(s1, s2);
    }

    while (s2 < r)
    {

        if (*s2 <= *(s2 + 1))
        {
            s3 = extendIncreasingRunRight(s2, r);
        }
        else
        {
            s3 = extendStrictlyDecreasingRunRight(s2, r);
            reverseRange(s2, s3);
        }

        if (s3 - s2 < 24)
        {
            s3 = std::min(r, s2 + 24);
            insertionsort(s2, s3);
        }

        p = node_power_div(l - l, r - l, s1 - l, s2 - l, s3 - l);

        while (pow > powStart)
        {
            if (*pow > p)
            {
                merge_run2(*lrs, s1, s2, B);
                cost = cost + (s2 - *lrs);
                s1 = *lrs;
                lrs--;
                pow--;
            }
            else
            {
                break;
            }
        }

        lrs++;
        pow++;
        *lrs = s1;
        *pow = p;
        s1 = s2;
        s2 = s3;
    }

    while (lrs > lrsStart)
    {
        merge_run2(*lrs, s1, s2, B);
        s1 = *lrs;
        cost += (s2 - s1);
        lrs--;
    }
    mergeCost += cost;
}

void powersort4BufferInsertion(Iter l, Iter r, Iter B)
{
    long long int cost = 0;
    int n = r - l;
    std::stack<Iter> leftRunStart;
    std::stack<int> powers;
    Iter s1, s2, s3, x, x1, x2, x3;
    s1 = l;

    if (*s1 <= *(s1 + 1))
    {
        s2 = extendIncreasingRunRight(s1, r);
    }
    else
    {
        s2 = extendStrictlyDecreasingRunRight(s1, r);
        reverseRange(s1, s2);
    }

    if (s2 - s1 < 24 && s1 + 24 < r)
    {
        s2 = s1 + 24;
        insertionsort(s1, s2);
    }

    while (s2 < r)
    {

        if (*s2 <= *(s2 + 1))
        {
            s3 = extendIncreasingRunRight(s2, r);
        }
        else
        {
            s3 = extendStrictlyDecreasingRunRight(s2, r);
            reverseRange(s2, s3);
        }

        if (s3 - s2 < 24 && s1 + 24 < r)
        {
            s3 = s2 + 24;
            insertionsort(s2, s3);
        }

        int p = nodePower4(s1, s2, s3, l, r);
        int numPowers;

        while (!powers.empty())
        {
            if (powers.top() > p)
            {
                numPowers = powercheck(powers);
                x1 = leftRunStart.top();
                leftRunStart.pop();
                if (numPowers == 1)
                {
                    merge_run2(x1, s1, s2, B);
                    cost = cost + (s2 - x1);
                    s1 = x1;
                }
                else if (numPowers == 2)
                {
                    x2 = leftRunStart.top();
                    leftRunStart.pop();
                    merge4way3(x2, x2, x1, s1, s2, B);
                    cost = cost + (s2 - x2);
                    s1 = x2;
                    powers.pop();
                }
                else if (numPowers == 3)
                {
                    x2 = leftRunStart.top();
                    leftRunStart.pop();
                    x3 = leftRunStart.top();
                    leftRunStart.pop();
                    merge4way3(x3, x2, x1, s1, s2, B);
                    cost = cost + (s2 - x3);
                    s1 = x3;
                    powers.pop();
                    powers.pop();
                }
                powers.pop();
            }
            else
            {
                break;
            }
        }
        leftRunStart.push(s1);
        powers.push(p);
        s1 = s2;
        s2 = s3;
    }

    while (!leftRunStart.empty())
    {
        x1 = leftRunStart.top();
        if (leftRunStart.size() >= 3)
        {
            leftRunStart.pop();
            x2 = leftRunStart.top();
            leftRunStart.pop();
            x3 = leftRunStart.top();
            merge4way3(x3, x2, x1, s1, s2, B);
            s1 = x3;
        }
        else if (leftRunStart.size() == 2)
        {
            leftRunStart.pop();
            x2 = leftRunStart.top();
            merge4way3(x2, x1, s1, s2, s2, B);
            s1 = x2;
        }
        else
        {
            merge_run2(x1, s1, s2, B);
            s1 = x1;
        }
        cost = cost + (s2 - s1);
        leftRunStart.pop();
    }
    mergeCost += cost;
}


void powersort4BufferInsertion2(Iter l, Iter r, Iter B)
{
    int cost = 0;
    int n = r - l;
    std::vector<Iter> leftRunStart(ceil(log2(n)) + 2);
    Iter powStart = (l + n + 4), pow = powStart, s1 = l, s2, s3, x, x1, x2, x3;
    Iter2 lrsStart = leftRunStart.begin(), lrs = lrsStart;
    if (*s1 <= *(s1 + 1))
    {
        s2 = extendIncreasingRunRight(s1, r);
    }
    else
    {
        s2 = extendStrictlyDecreasingRunRight(s1, r);
        reverseRange(s1, s2);
    }

    if (s2 - s1 < 24)
    {
        s2 = std::min(r, s1 + 24);
        insertionsort(s1, s2);
    }
    while (s2 < r)
    {

        if (*s2 <= *(s2 + 1))
        {
            s3 = extendIncreasingRunRight(s2, r);
        }
        else
        {
            s3 = extendStrictlyDecreasingRunRight(s2, r);
            reverseRange(s2, s3);
        }

        if (s3 - s2 < 24)
        {
            s3 = std::min(r, s2 + 24);
            insertionsort(s2, s3);
        }

        int p = nodePower4(s1, s2, s3, l, r);
        int numPowers;

        while (pow > powStart)
        {
            if (*pow > p)
            {
                
                numPowers = powercheck2(pow, powStart);
                x1 = *lrs;
                lrs--;
                if (numPowers == 1)
                {
                    merge_run2(x1, s1, s2, B);
                    cost = cost + (s2 - x1);
                    s1 = x1;
                }
                else if (numPowers == 2)
                {
                    x2 = *lrs;
                    lrs--;
                    merge4way3(x2, x2, x1, s1, s2, B);
                    cost = cost + (s2 - x2);
                    s1 = x2;
                    pow--;
                }
                else if (numPowers == 3)
                {
                    x2 = *lrs;
                    lrs--;
                    x3 = *lrs;
                    lrs--;
                    merge4way3(x3, x2, x1, s1, s2, B);
                    cost = cost + (s2 - x3);
                    s1 = x3;
                    pow--;
                    pow--;
                }
                pow--;
            }
            else
            {
                break;
            }
        }
        lrs++;
        pow++;
        *lrs = s1;
        *pow = p;
        s1 = s2;
        s2 = s3;
    }
    
    while (lrs  > lrsStart)
    {
        x1 = *lrs;
        if (lrs - lrsStart >= 3)
        {
            lrs--;
            x2 = *lrs;
            lrs--;
            x3 = *lrs;
            merge4way3(x3, x2, x1, s1, s2, B);
            s1 = x3;
        }
        else if (lrs - lrsStart == 2)
        {
            lrs--;
            x2 = *lrs;
            merge4way3(x2, x1, s1, s2, s2, B);
            s1 = x2;
        }
        else
        {
            merge_run2(x1, s1, s2, B);
            s1 = x1;
        }
        cost = cost + (s2 - s1);
        lrs--;
    }
    mergeCost += cost;
}

void experimentPowersortBufferInsertion(int x, int y, int size, int num, bool runs)
{
    std::cout << "experiment Powersort Buffer Insertion\n";
    std::cout << "size of vectors = " << size << "\nnumber of vectors =" << num << "\nrange of ints = " << x << " to " << y << "\nRuns = " << runs;

    std::vector<int> a, B(size + 4 + ceil(log2(size)) + 2);
    mergeCost = 0;
    a = inputs::random_vector(x, y, size * num);
    if (runs == true)
    {
        inputs::run_sort(a.begin(), a.end(), sqrt(size));
    }
    Iter l = a.begin(), r = l + size, b = B.begin();
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < num; i++)
    {
        powersortBufferInserion2(l, r, b);
        if (!std::is_sorted(l, r))
        {
            std::cout << "it is not sorted broke on " << i << "\n";
            break;
        }
        l = r;
        r = r + size;
    }
    auto finish = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = finish - start;
    std::cout << "\nElapsed time: " << elapsed.count() << " s\n";
    std::cout << "Average elapsed time:" << elapsed.count() / num << " s\n";
    std::cout << "Merge cost = " << mergeCost << "\nAverage merge cost = " << mergeCost / num;
}

void experimentPowersort4BufferInsertion(int x, int y, int size, int num, bool runs)
{
    std::cout << "experiment Powersort4 Buffer Insertion\n";
    std::cout << "size of vectors = " << size << "\nnumber of vectors =" << num << "\nrange of ints = " << x << " to " << y << "\nRuns = " << runs;
    std::vector<int> a, B(size + 4 + ceil(log2(size)) + 2);
    a = inputs::random_vector(x, y, size * num);
    mergeCost = 0;
    if (runs == true)
    {
        inputs::run_sort(a.begin(), a.end(), sqrt(size));
    }
    Iter l = a.begin(), r = l + size, b = B.begin();

    //static int mergeCost;
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < num; i++)
    {
        powersort4BufferInsertion(l, r, b);
        if (!std::is_sorted(l, r))
        {
            std::cout << "it is not sorted broke on " << i << "\n";
            break;
        }
        l = r;
        r = r + size;
    }
    auto finish = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = finish - start;
    std::cout << "\nElapsed time: " << elapsed.count() << " s\n";
    std::cout << "Average elapsed time:" << elapsed.count() / num << " s\n";
    std::cout << "Merge cost = " << mergeCost << "\nAverage merge cost = " << mergeCost / num;
}

void experimentPowersort4BufferInsertion2(int x, int y, int size, int num, bool runs)
{
    std::cout << "experiment Powersort4 Buffer Insertion 2\n";
    std::cout << "size of vectors = " << size << "\nnumber of vectors =" << num << "\nrange of ints = " << x << " to " << y << "\nRuns = " << runs;
    std::vector<int> a, B(size + 4 + ceil(log2(size)) + 2);
    a = inputs::random_vector(x, y, size * num);
    mergeCost = 0;
    if (runs == true)
    {
        inputs::run_sort(a.begin(), a.end(), sqrt(size));
    }
    Iter l = a.begin(), r = l + size, b = B.begin();

    //static int mergeCost;
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < num; i++)
    {
        powersort4BufferInsertion2(l, r, b);
        if (!std::is_sorted(l, r))
        {
            std::cout << "it is not sorted broke on " << i << "\n";
            break;
        }
        l = r;
        r = r + size;
    }
    auto finish = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = finish - start;
    std::cout << "\nElapsed time: " << elapsed.count() << " s\n";
    std::cout << "Average elapsed time:" << elapsed.count() / num << " s\n";
    std::cout << "Merge cost = " << mergeCost << "\nAverage merge cost = " << mergeCost / num;
}

void experimentStableSort(int x, int y, int size, int num, bool runs)
{
    std::cout << "Experiment std::Stable_sort \n";
    std::cout << "size of vectors = " << size << "\nnumber of vectors =" << num << "\nrange of ints = " << x << " to " << y << "\nRuns = " << runs;

    std::vector<int> a, B(size + 4);
    mergeCost = 0;
    a = inputs::random_vector(x, y, size * num);
    if (runs == true)
    {
        inputs::run_sort(a.begin(), a.end(), sqrt(size));
    }
    Iter l = a.begin(), r = l + size, b = B.begin();
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < num; i++)
    {
        std::stable_sort(l, r);
        if (!std::is_sorted(l, r))
        {
            std::cout << "it is not sorted broke on " << i << "\n";
            break;
        }
        l = r;
        r = r + size;
    }
    auto finish = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = finish - start;
    std::cout << "\nElapsed time: " << elapsed.count() << " s\n";
    std::cout << "Average elapsed time:" << elapsed.count() / num << " s\n";
    std::cout << "Merge cost = " << mergeCost << "\nAverage merge cost = " << mergeCost / num;
}

void experimentStdSort(int x, int y, int size, int num, bool runs)
{
    std::cout << "Experiment std::sort \n";
    std::cout << "size of vectors = " << size << "\nnumber of vectors =" << num << "\nrange of ints = " << x << " to " << y << "\nRuns = " << runs;

    std::vector<int> a, B(size + 4);
    mergeCost = 0;
    a = inputs::random_vector(x, y, size * num);
    if (runs == true)
    {
        inputs::run_sort(a.begin(), a.end(), sqrt(size));
    }
    Iter l = a.begin(), r = l + size, b = B.begin();
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < num; i++)
    {
        std::sort(l, r);
        if (!std::is_sorted(l, r))
        {
            std::cout << "it is not sorted broke on " << i << "\n";
            break;
        }
        l = r;
        r = r + size;
    }
    auto finish = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = finish - start;
    std::cout << "\nElapsed time: " << elapsed.count() << " s\n";
    std::cout << "Average elapsed time:" << elapsed.count() / num << " s\n";
    std::cout << "Merge cost = " << mergeCost << "\nAverage merge cost = " << mergeCost / num;
}

void experimentPeeksortInsertion(int x, int y, int size, int num, bool runs)
{
    std::cout << "Experiment Peeksort Insertion \n";
    std::cout << "size of vectors = " << size << "\nnumber of vectors =" << num << "\nrange of ints = " << x << " to " << y << "\nRuns = " << runs;

    std::vector<int> a, B(size + 4);
    mergeCost = 0;
    a = inputs::random_vector(x, y, size * num);
    if (runs == true)
    {
        inputs::run_sort(a.begin(), a.end(), sqrt(size));
    }
    Iter l = a.begin(), r = l + size, b = B.begin(), e, s;
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < num; i++)
    {
        e = findEandFlip(l, r), s = findSandFlip(l, r);
        peeksortInsertion(l, r, e, s, b);
        if (!std::is_sorted(l, r))
        {
            std::cout << "it is not sorted broke on " << i << "\n";
            break;
        }
        l = r;
        r = r + size;
    }
    auto finish = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = finish - start;
    std::cout << "\nElapsed time: " << elapsed.count() << " s\n";
    std::cout << "Average elapsed time:" << elapsed.count() / num << " s\n";
    std::cout << "Merge cost = " << mergeCost << "\nAverage merge cost = " << mergeCost / num;
}

void experimentPeeksort4Insertion(int x, int y, int size, int num, bool runs)
{
    std::cout << "Experiment Peeksort4way Insertion \n";
    std::cout << "size of vectors = " << size << "\nnumber of vectors =" << num << "\nrange of ints = " << x << " to " << y << "\nRuns = " << runs;

    std::vector<int> a, B(size + 5);
    mergeCost = 0;
    a = inputs::random_vector(x, y, size * num);
    if (runs == true)
    {
        inputs::run_sort(a.begin(), a.end(), sqrt(size));
    }
    Iter l = a.begin(), r = l + size, b = B.begin(), e = findEandFlip(l, r), s = findSandFlip(l, r);
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < num; i++)
    {
        peeksort4Insertion(l, r, e, s, b);
        if (!std::is_sorted(l, r))
        {
            std::cout << "it is not sorted broke on " << i << "\n";
            break;
        }
        l = r;
        r = r + size;
    }
    auto finish = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = finish - start;
    std::cout << "\nElapsed time: " << elapsed.count() << " s\n";
    std::cout << "Average elapsed time:" << elapsed.count() / num << " s\n";
    std::cout << "Merge cost = " << mergeCost << "\nAverage merge cost = " << mergeCost / num;
}

long int nodePower2(Iter s1, Iter s2, Iter s3, Iter l, Iter r)
{
    double n = r - l;
    int n1 = s2 - s1;
    int n2 = s3 - s2;
    long double a = ((s1 - l + n1 / 2.0) / n);
    long double b = ((s2 - l + n2 / 2.0) / n);
    long i = 0;
    while (floor(a * (pow(2, i))) == floor(b * (pow(2, i))))
    {
        i++;
    }
    std::cout << "\nn1 = " << n1 << ", n2 = " << n2 << ", a = " << a << ", b = " << b << " power = " << i << "\n";
    return i;
}



int main(int argc, char** argv)
{
	int minNum = INT_MIN, maxNum = INT_MAX-1;
	int n = 10000000, nInputs=10;
	bool withSortedRuns = true;
	
	inputs::RNG.seed( 32785623 );
	
	switch (argv[1][0]) {
	case 's':
		experimentStdSort(minNum, maxNum, n, nInputs, withSortedRuns);
		break;
	case 'S':
		experimentStableSort(minNum, maxNum, n, nInputs, withSortedRuns);
		break;
	case 'p':
		experimentPowersortBufferInsertion(minNum, maxNum, n, nInputs, withSortedRuns);
		break;
	case 'P':
		experimentPowersort4BufferInsertion2(minNum, maxNum, n, nInputs, withSortedRuns);
		break;
	case 'Q':
		experimentPowersort4BufferInsertion(minNum, maxNum, n, nInputs, withSortedRuns);
		break;
	case 'e':
		experimentPeeksortInsertion(minNum, maxNum, n, nInputs, withSortedRuns);
		break;
	case 'E':
		experimentPeeksort4Insertion(minNum, maxNum, n, nInputs, withSortedRuns);
		break;
	default:
		std::cout << "Select algorithm 'sSpPQeE'" << std::endl;
	}
	
	

    //experimentPowersortBufferInsertion(INT_MIN, INT_MAX - 1, 10000000, 1, true);

    //experimentPowersort4BufferInsertion(INT_MIN, INT_MAX - 1, 10000000, 1, false);
    //experimentPowersort4BufferInsertion2(INT_MIN, INT_MAX - 1, 10000000, 1, false);

    //experimentStableSort(INT_MIN, INT_MAX-1, 10000000, 10, false);

    //experimentStdSort(minNum, maxNum, n, nInputs, withSortedRuns);

    //experimentPeeksortInsertion(INT_MIN, INT_MAX - 1, 10000000, 10, true);

    //experimentPeeksort4Insertion(INT_MIN, INT_MAX - 1, 10000000, 10, true);

    //experimentPowersortBufferInsertion(INT_MIN, INT_MAX - 1, 10000000, 10, true);

    //experimentPowersort4BufferInsertion(INT_MIN, INT_MAX - 1, 10000000, 10, false);

    //experimentStableSort(INT_MIN, INT_MAX-1, 10000000, 10, true);

    //experimentPeeksortInsertion(INT_MIN, INT_MAX - 1, 10000000, 10, false);

    //experimentPeeksort4Insertion(INT_MIN, INT_MAX-1, 10000000, 10, true);

    return 0;
}
