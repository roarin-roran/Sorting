"""Copy of Tim Peter's code to test mergecost of various merge policies.
see https://github.com/python/cpython/issues/78742"""


def merge_at(s, i):
    s[i] += s[i + 1]
    del s[i + 1]
    return s[i]


def merge_force_collapse(s):
    cost = 0
    while len(s) > 1:
        n = len(s) - 2
        if n > 0 and s[n - 1] < s[n + 1]:
            n -= 1
        cost += merge_at(s, n)
    return cost


def sort(runs, merge_collapse):
    stack = []
    maxstack = 0
    cost = 0
    for x in runs:
        stack.append(x)
        maxstack = max(maxstack, len(stack))
        cost += merge_collapse(stack)
    cost += merge_force_collapse(stack)
    return cost, maxstack


def timsort(s):
    cost = 0
    while len(s) > 1:
        n = len(s) - 2
        if ((n > 0 and s[n - 1] <= s[n] + s[n + 1]) or
                (n > 1 and s[n - 2] <= s[n - 1] + s[n])):
            if s[n - 1] < s[n + 1]:
                n -= 1
            cost += merge_at(s, n)
        elif s[n] <= s[n + 1]:
            cost += merge_at(s, n)
        else:
            break
    return cost


def twomerge(s):
    cost = 0
    while len(s) > 1:
        n = len(s) - 2
        if s[n] < 2 * s[n + 1]:
            if n > 0 and s[n - 1] < s[n + 1]:
                n -= 1
            cost += merge_at(s, n)
        else:
            break
    if len(s) > 1:
        assert s[-2] >= 2 * s[-1]
        if len(s) > 2:
            assert s[-3] >= 2 * s[-2]
    return cost


# The Shivers sort is taken from
# "Adaptive Shivers Sort:  An Alternative Sorting Algorithm"
# Vincent Jugé
# http://igm.univ-mlv.fr/~juge/papers/shivers_arxiv.pdf

# return floor(log2(i)) >= floor(log2(j))
def log2_ge(i, j):
    return i >= j or i > (i ^ j)


if 0:
    # floor(log2(j)) == j.bit_length() - 1
    def log2_ge_python(i, j):
        return i.bit_length() >= j.bit_length()


    from itertools import product

    for i, j in product(range(1200), repeat=2):
        assert log2_ge(i, j) == log2_ge_python(i, j)
    assert False, "done"


def shivers(s):
    cost = 0
    n = len(s)
    while n >= 3 and log2_ge(s[-1], s[-3]):
        cost += merge_at(s, n - 3)
        n -= 1
    while n >= 3 and log2_ge(s[-2], s[-3]):
        cost += merge_at(s, n - 3)
        n -= 1
    while n >= 2 and log2_ge(s[-1], s[-2]):
        cost += merge_at(s, n - 2)
        n -= 1
    assert len(s) == n
    return cost


# Adaptive Shivers from a later version of Vincent's paper. The code is
# shorter and more uniform, but appears to be functionally identical.
def shivers2(s):
    cost = 0
    while (n := len(s)) >= 3:
        x = s[n - 1] | s[n - 2]
        if x > (s[n - 3] & ~x):
            cost += merge_at(s, n - 3)
            n -= 1
        else:
            break
    assert len(s) == n
    return cost


from math import log2, floor


# Length-adaptive ShiversSort from Vincent's paper. Highly competitive
# with powersort!
# Alas, so far I haven't thought of a fast way to code the `if` test.
def shivers3(length, s):
    cost = 0
    n = len(s)
    while n >= 3:
        if (floor(log2(s[n - 3] / (length + 1))) <=
                floor(log2(max(s[n - 1], s[n - 2]) / (length + 1)))):
            cost += merge_at(s, n - 3)
            n -= 1
        else:
            break
    assert len(s) == n
    return cost


# shivers4 reworks shivers3 not to need division or math library calls;
# return floor(log2(i/(length + 1))) <= floor(log2(j/(length + 1))).
def float_log2_le(i, j, length):
    assert 0 < i <= length
    assert 0 < j <= length
    while True:
        i <<= 1
        j <<= 1
        if i > length:
            return j > length
        if j > length:
            return True


def shivers4(length, s):
    cost = 0
    n = len(s)
    while n >= 3:
        if float_log2_le(s[n - 3], max(s[n - 1], s[n - 2]), length):
            cost += merge_at(s, n - 3)
            n -= 1
        else:
            break
    assert len(s) == n
    return cost


if 0:
    for length in range(1, 1001):
        print("checking", length)
        for i in range(1, length + 1):
            for j in range(1, length + 1):
                result1 = (floor(log2(i / (length + 1))) <=
                           floor(log2(j / (length + 1))))
                result2 = float_log2_le(i, j, length)
                if result1 != result2:
                    print("OUCH!", i, j, length, result1, result2)
                    input("paused")


# Minimal cost across all possible ways of merging runs.
# Takes time cubic in len(runs).
def ideal(runs):
    runs = list(runs)
    n = len(runs)
    # c[i, w] is minimal cost of merging slice runs[i : i+w].
    c = {(i, 1): 0 for i in range(n)}
    prefixsum = runs[0]
    for width in range(2, n + 1):
        prefixsum += runs[width - 1]
        total = prefixsum
        for start in range(n - width + 1):
            c[start, width] = total + min(c[start, w] + c[start + w, width - w]
                                          for w in range(1, width))
            if start + width < n:
                total += runs[start + width] - runs[start]
    return c[0, n]


# Minimal cost across all possible ways of merging runs.
# Takes time quadratic in len(runs).
def ideal2(runs):
    runs = list(runs)
    n = len(runs)
    # c[i, w] is minimal cost of merging slice runs[i : i+w].
    c = {(i, 1): 0 for i in range(n)}
    c.update(((i, 2), runs[i] + runs[i + 1]) for i in range(n - 1))
    r = {(i, 2): i + 1 for i in range(n - 1)}
    prefixsum = runs[0] + runs[1]
    for width in range(3, n + 1):
        wm1 = width - 1
        prefixsum += runs[wm1]
        total = prefixsum
        for start in range(n - wm1):
            bestsum = None
            for start2 in range(r[start, wm1], r[start + 1, wm1] + 1):
                w = start2 - start
                x = c[start, w] + c[start2, width - w]
                if bestsum is None or x < bestsum:
                    bestsum = x
                    beststart2 = start2
            c[start, width] = total + bestsum
            r[start, width] = beststart2
            if start + width < n:
                total += runs[start + width] - runs[start]
    return c[0, n]


if 0:
    from random import randrange

    count = 0
    while True:
        count += 1
        rs = [randrange(1, 100) for i in range(randrange(10, 200))]
        print("x", end="")
        i1 = ideal(rs)
        print("y", end="")
        i2 = ideal2(rs)
        print("z", end="")
        assert i1 == i2
        if count % 20 == 0:
            print()
            if count % 20000 == 0:
                print(count)


def greedy(runs):
    s = list(runs)
    cost = 0
    while len(s) > 1:
        i = min(range(len(s) - 1), key=lambda i: s[i] + s[i + 1])
        cost += merge_at(s, i)
    return cost


# Bad sequence of run lengths for timsort, summing to `n`.
def rtim(n):
    if n <= 3:
        return [n]
    n2 = n >> 1
    return rtim(n2) + rtim(n2 - 1) + [(n & 1) + 1]


def power(s1, n1, n2, n):
    assert s1 >= 0
    assert n1 >= 1 and n2 >= 1
    assert s1 + n1 + n2 <= n
    # a = s1 + n1/2
    # b = s1 + n1 + n2/2 = a + (n1 + n2)/2
    a = 2 * s1 + n1  # 2*a
    b = a + n1 + n2  # 2*b
    # Array length has d bits.  Max power is d:
    #     b/n - a/n = (b-a)/n = (n1 + n2)/2/n >= 2/2/n = 1/n > 1/2**d
    # So at worst b/n and a/n differ in bit 1/2**d.
    # a and b have <= d+1 bits. Shift left by d-1 and divide by 2n =
    # shift left by d-2 and divide by n.  Result is d - bit length of
    # xor.  After the shift, the numerator has at most d+1 + d-2 = 2*d-1
    # bits. Any value of d >= n.bit_length() can be used.
    d = n.bit_length()  # or larger; smaller can fail
    a = (a << (d - 2)) // n
    b = (b << (d - 2)) // n
    return d - (a ^ b).bit_length()


# Like power but move n up to a power of 2.
def powercheat(s1, n1, n2, n):
    assert s1 >= 0
    assert n1 >= 1 and n2 >= 1
    assert s1 + n1 + n2 <= n
    a = 2 * s1 + n1  # 2*a
    b = a + n1 + n2  # 2*b
    d = n.bit_length()  # or larger; smaller can fail
    a >>= 2
    b >>= 2
    return d - (a ^ b).bit_length()


def powerloop(s1, n1, n2, n):
    assert s1 >= 0
    assert n1 >= 1 and n2 >= 1
    assert s1 + n1 + n2 <= n
    # a = s1 + n1/2
    # b = s1 + n1 + n2/2 = a + (n1 + n2)/2
    a = 2 * s1 + n1  # 2*a
    b = a + n1 + n2  # 2*b
    L = 0
    while True:
        L += 1
        if a >= n:
            assert b >= n
            a -= n
            b -= n
        elif b >= n:
            break
        assert a < b < n
        a <<= 1
        b <<= 1
    return L


from math import frexp

T53 = float(2 ** 53)


# Using frexp works fine for small n, but flakes out quickly as n grows.
# To get it to flake out even faster, instead of dividing by n, multiply
# by 1.0/n.
def power_frexp(s1, n1, n2, n):
    assert s1 >= 0
    assert n1 >= 1 and n2 >= 1
    assert s1 + n1 + n2 <= n
    # a = s1 + n1/2
    # b = s1 + n1 + n2/2 = a + (n1 + n2)/2
    a = s1 + n1 * 0.5
    b = a + (n1 + n2) * 0.5
    m1, e1 = frexp(a / n)
    m2, e2 = frexp(b / n)
    if e1 != e2:
        return 1 - max(e1, e2)
    m1 = int(m1 * T53)
    m2 = int(m2 * T53)
    x = m1 ^ m2
    assert x
    return 54 - x.bit_length() - e1


if 0:
    for N in range(2, 10001):
        print(N)
        for s1 in range(N - 1):
            # 2 <= sum of lengths <= N - s1
            for lensum in range(2, N - s1 + 1):
                for n1 in range(1, lensum):
                    n2 = lensum - n1
                    pold = powerloop(s1, n1, n2, N)
                    pnew = powercheat(s1, n1, n2, N)
                    if pold != pnew:
                        print("OUCH", N, pold, pnew, s1, n1, n2)
                        assert False

if 0:
    from random import randrange

    count = 0
    LO = 1 << 60
    HI = LO << 1
    while True:
        count += 1
        N = randrange(LO, HI)
        s1 = randrange(N - 1)
        for lensum in 2, N - s1, randrange(3, N - s1):
            for n1 in 1, lensum - 1, randrange(1, lensum):
                n2 = lensum - n1
                pold = powerloop(s1, n1, n2, N)
                pnew = powercheat(s1, n1, n2, N)
                if pold != pnew:
                    print("OUCH", N, pold, pnew, s1, n1, n2)
                    assert False
        if count % 100_000 == 0:
            print(count)


def powersort(runs):
    cost = 0
    maxstack = 0
    s = []
    runs = list(runs)
    n = sum(runs)
    s1, n1 = 0, runs[0]
    for i in range(1, len(runs)):
        s2, n2 = s1 + n1, runs[i]
        p = power(s1, n1, n2, n)
        # p = powercheat(s1, n1, n2, n)
        while s and s[-1][-1] > p:
            s0, n0, _ = s.pop()
            assert s0 + n0 == s1
            n1 += n0
            cost += n1
            s1 = s0
        assert s1 + n1 == s2
        if s:
            assert s[-1][-1] < p  # never equal!
        s.append((s1, n1, p))
        maxstack = max(maxstack, len(s))
        s1, n1 = s2, n2
    while s:
        s0, n0, _ = s.pop()
        assert s0 + n0 == s1
        n1 += n0
        cost += n1
        s1 = s0
    assert (s1, n1) == (0, n), (s1, n1, 0, n)
    return cost, maxstack


def new_powersort(runs):
    cost = 0
    maxstack = 0
    s = []
    runs = list(runs)
    n = sum(runs)
    nthird = int(n // 3)
    s1, n1 = 0, runs[0]
    for i in range(1, len(runs)):
        s2, n2 = s1 + n1, runs[i]
        p = power(s1, n1, n2, n)
        # p = powercheat(s1, n1, n2, n)
        while s and s[-1][-1] > p:
            # if s[-1][1] > n2:
            #    break
            if len(s) > 1 and s[-2][-1] > p and s[-2][1] < n1:
                s0, n0, p0 = s[-2]
                n0 += s[-1][1]
                cost += n0
                assert s0 + n0 == s1
                s[-2] = s0, n0, p0
                del s[-1]
                continue
            s0, n0, _ = s.pop()
            assert s0 + n0 == s1
            n1 += n0
            cost += n1
            s1 = s0
        assert s1 + n1 == s2
        if 0:  # s:
            assert s[-1][-1] < p  # never equal!
        s.append((s1, n1, 1 if n1 > nthird else p))
        # s.append((s1, n1, p))
        maxstack = max(maxstack, len(s))
        s1, n1 = s2, n2
    while s:
        if len(s) > 1 and s[-2][1] < n1:
            s0, n0, _ = s[-2]
            n0 += s[-1][1]
            cost += n0
            assert s0 + n0 == s1
            s[-2] = s0, n0, _
            del s[-1]
            continue
        s0, n0, _ = s.pop()
        assert s0 + n0 == s1
        n1 += n0
        cost += n1
        s1 = s0
    assert (s1, n1) == (0, n), (s1, n1, 0, n)
    return cost, maxstack


# powersort = new_powersort

def pmerge_at(s, i):
    s[i][1] += s[i + 1][1]
    del s[i + 1]
    return s[i][1]


def pmerge_force_collapse(s):
    cost = 0
    while len(s) > 1:
        n = len(s) - 2
        cost += pmerge_at(s, n)
    return cost


def pnewrun(stack, s2, n2, n):
    cost = 0
    if stack:
        s1, n1, p = stack[-1]
        assert s1 + n1 == s2
        assert p is None
        p = power(s1, n1, n2, n)
        while len(stack) > 1 and stack[-2][-1] > p:
            cost += pmerge_at(stack, len(stack) - 2)
        if len(stack) > 1:
            assert stack[-2][-1] < p
        stack[-1][-1] = p
    stack.append([s2, n2, None])
    return cost


def powersort_squash(runs):
    cost = 0
    maxstack = 0
    stack = []
    runs = list(runs)
    n = sum(runs)
    s2 = 0
    for n2 in runs:
        cost += pnewrun(stack, s2, n2, n)
        maxstack = max(maxstack, len(stack))
        s2 += n2
    cost += pmerge_force_collapse(stack)
    s1, n1, p = stack[-1]
    assert (s1, n1) == (0, n), (s1, n1, 0, n)
    return cost, maxstack


def show(runs):
    runs = list(runs)
    n = sum(runs)
    s1, n1 = 0, runs[0]
    for i in range(1, len(runs)):
        s2, n2 = s1 + n1, runs[i]
        p = power(s1, n1, n2, n)
        print(f"{n1} <{p}>")
        s1, n1 = s2, n2
    print(n1)


def midpoints(runs):
    runs = list(runs)
    n = sum(runs)
    s = 0
    for r in runs:
        print(r, (s + r / 2) / n)
        s += r


from functools import partial

if 0:
    def mids2(runs):
        ms = []
        sofar = 0
        for r in runs:
            ms.append(sofar + r)
            sofar += 2 * r
        return ms


    def temp():
        n = 1000000
        runs = [n - 1, 1, 1, n]
        print(runs, sum(runs))
        show(runs)
        print(ideal(runs))
        print(ideal2(runs))
        ms = mids2(runs)
        print(ms)
        d = n.bit_length()
        for i in range(0, len(ms) - 1):
            m1, m2 = ms[i: i + 2]
            a = (m1 << d - 2) // n
            b = (m2 << d - 2) // n
            print(a, b, a ^ b, bin(a ^ b))
        print()
        for i in range(0, len(ms) - 1):
            m1, m2 = ms[i: i + 2]
            a = (m1 << 63) // n
            b = (m2 << 63) // n
            print(a, b, a ^ b, bin(a ^ b))
        print()
        scale = 2 ** 63 // n
        print("scale", scale)
        for i in range(0, len(ms) - 1):
            m1, m2 = ms[i: i + 2]
            a = m1 * scale
            b = m2 * scale
            print(a, b, a ^ b, bin(a ^ b))


    temp()

if 1:
    def one(tag, r):
        print(tag)
        r = list(r)
        print("  timsort", sort(r, timsort))
        print(" twomerge", sort(r, twomerge))
        print(" shivers2", sort(r, shivers2))
        print(" shivers4", sort(r, partial(shivers4, sum(r))))
        print("powersort", powersort(r))
        print()


    from random import random, randrange

    one("all the same", [32] * 1000)  # identical stats
    one("ascending", range(1, 2000))  # timsort a little better
    one("descending", reversed(range(1, 2000)))  # twomerge significantly better
    one("bad timsort case", rtim(100000))
    n = 1000000
    one("bad powersort case", (n - 1, 1, 1, n))
    one("bad powersort case2?", (n, 1, 1, n-1))
    one("another bad timsort", (190000, 180000, 10000, 10000))
    one("bad twomerge case", (190000, 60000, 40000, 10000))
    one("bad shivers case", (30 << 12, 1 << 12, 16 << 12, 1 << 12))

    # "Random" run-length distributions are largely irrelevant, since on
    # randomly ordered input the actual sort is most likely to _force_
    # (via local binary insertion sorts) all runs to length `minrun`.
    # Nevertheless ... there's no clear overall winner in this
    # particular made-up distribution.  On some runs timsort "wins" in
    # the end, on others twomerge, but the total costs are typically
    # within 2% of each other.
    # Later:  powersort almost always dominates both.
    # Later:  and length-adaptive Shivers (shivers3/4) usually eeks out
    # powersort.
    # Later: although shivers4 eeking out powersort appears very
    # delicate, almost unique to the "0.80" below. Here's how it goes
    # for a number of cutoffs:
    #
    # timsort  766341817 14
    # twomerge 762098371 12
    # shivers2 741251511 14
    # shivers4 741806864 15
    # power    726306659 14
    # 0.00 % wrt powersort 6.49% 5.68% 2.50% 2.20% 0.00%
    # 0.05 % wrt powersort 6.30% 4.49% 2.83% 2.41% 0.00%
    # 0.10 % wrt powersort 5.91% 5.61% 3.78% 0.99% 0.00%
    # 0.15 % wrt powersort 6.13% 5.53% 5.05% 0.36% 0.00%
    # 0.20 % wrt powersort 5.39% 5.42% 2.94% 0.49% 0.00%
    # 0.30 % wrt powersort 5.46% 5.20% 0.44% 0.50% 0.00%
    # 0.40 % wrt powersort 5.64% 5.48% 1.50% 2.16% 0.00%
    # 0.50 % wrt powersort 5.66% 5.10% 2.39% 2.00% 0.00%
    # 0.60 % wrt powersort 5.44% 5.21% 4.71% 0.22% 0.00%
    # 0.70 % wrt powersort 4.61% 5.06% 1.83% 2.07% 0.00%
    # 0.75 % wrt powersort 5.00% 5.16% 2.09% 1.81% 0.00%
    # 0.80 % wrt powersort 3.94% 3.79% 5.75% -0.16% 0.00%
    # 0.85 % wrt powersort 4.52% 5.19% 0.88% 1.88% 0.00%
    # 0.90 % wrt powersort 3.57% 4.12% 4.09% 0.00% 0.00%
    # 1.00 % wrt powersort 7.12% 5.40% 0.67% 1.88% 0.00%

    print("randomized trials")
    totals = [0, 0, 0, 0, 0]
    for trial in range(20):
        runs = []
        for i in range(10000):
            switch = random()
            if switch < 0.80:
                x = randrange(1, 100)
            else:
                x = randrange(1000, 10000)
            runs.append(x)
        for i, which in enumerate([timsort, twomerge, shivers2,
                                   partial(shivers4, sum(runs))]):
            cost, depth = sort(runs, which)
            if hasattr(which, "__name__"):
                name = which.__name__
            else:
                name = which.func.__name__
            print(f"{name:8s}", cost, depth)
            totals[i] += cost
        # cost = ideal(runs)
        # print("   ideal", cost)
        # totals[2] += cost
        # cost = greedy(runs)
        # print("  greedy", cost)
        # totals[3] += cost
        cost, depth = powersort(runs)
        print("power   ", cost, depth)
        totals[-1] += cost
        ptotal = totals[-1]
        print("sofar totals", totals)
        print("% wrt powersort", " ".join(f"{(v - ptotal) / ptotal:.2%}"
                                          for v in totals))

if 0:
    def p(xs):
        def inner(i):
            if i == n:
                yield xs
                return
            orig = xs[i]
            for j in range(i, n):
                xs[i] = xs[j]
                xs[j] = orig
                yield from inner(i + 1)
                xs[j] = xs[i]
            xs[i] = orig

        n = len(xs)
        return inner(0)

if 0:
    from itertools import product

    worst = 0.0
    first = 1
    for t in product(list(range(1, 51)), repeat=3):
        if t[0] > first:
            print(t)
            first = t[0]
        g = ideal(t)

        # b, ignore = powersort(t)
        # b, ignore = new_powersort(t)
        # b, ignore = sort(t, timsort)
        # b, ignore = sort(t, twomerge)
        b, ignore = sort(t, shivers)
        # b = greedy(t)

        assert g <= b
        if g != b:
            ratio = b / g
            if ratio > worst:
                print(t, b, g,
                      sort(t, timsort),
                      sort(t, twomerge),
                      sort(t, shivers),
                      powersort(t),
                      ratio)
                worst = ratio
    print("done")
    # n-1, 1, 1, n  # sum = 2n + 1
    # best = 2 + n+1 + 2n+1 = 3n + 4
    # powersort = 4n + 2

    # a = (n-1)/2 / (2*n + 1) = (n-1)/(4n+2)
    # b = (n - 1 + 1/2) / (2*n + 1) = (2n-1)/(4n+2)
    # so (0, n-1, 1) has power 2

    # then (n-1, 1, 1)
    # a = n-1 + 1/2 = n - 1/2; (2n-1)/(4n+2)
    # b = n + 1/2l             (2n+1)/(4n+2)
    # so has power 1, and n-1 is merged with 1 first

if 0:
    def pch(old, new):
        return f"{(new - old) / old:.4%}"


    from itertools import product

    cost1 = cost2 = 0
    oldcostwon = newcostwon = costtied = 0
    stack1 = stack2 = 0
    oldstackwon = newstackwon = stacktied = 0


    def disp():
        print(cost1, cost2, pch(cost1, cost2))
        print(oldcostwon, newcostwon, costtied)
        print(stack1, stack2, pch(stack1, stack2))
        print(oldstackwon, newstackwon, stacktied)


    first = 1
    for t in product(range(1, 21), repeat=5):
        if t[0] > first:
            print(t)
            first = t[0]
            disp()
        c1, s1 = powersort(t)  # sort(t, partial(shivers3, sum(t)))
        # c2, s2 = sort(t, twomerge)
        # c2, s2 = powersort(t)
        # c1, s1 = powersort(t)
        c2, s2 = sort(t, partial(shivers4, sum(t)))
        cost1 += c1
        cost2 += c2
        stack1 += s1
        stack2 += s2
        if c1 < c2:
            oldcostwon += 1
            # print(t, c1, s2, c2, s2)
            # assert False
        elif c1 > c2:
            newcostwon += 1
            # print(t, c1, s2, c2, s2)
            # assert False
        else:
            costtied += 1
        if s1 < s2:
            oldstackwon += 1
        elif s1 > s2:
            newstackwon += 1
        else:
            stacktied += 1
    print("done")
    disp()
