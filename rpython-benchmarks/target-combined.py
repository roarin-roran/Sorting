"""
A simple target to run both Powersort and Timsort (as part of PyPy/RPython rlib itself, but replaceable).

The target below specifies None as the argument types list.
This is a case treated specially in driver.py . If the list
of input types is empty, it is meant to be a list of strings,
actually implementing argv of the executable.
"""




from rpython.rlib.rarithmetic import ovfcheck
from rpython.rlib.objectmodel import specialize


def nocheck_getitem(l, i):
    return l[i]

def nocheck_setitem(l, i, v):
    l[i] = v

## ------------------------------------------------------------------------
## really weird rpython plugin stuff, don't look at this

from rpython.rtyper import extregistry
from rpython.annotator import model as annmodel
from rpython.tool.pairtype import pairtype
from rpython.annotator.bookkeeper import getbookkeeper

class Entry(extregistry.ExtRegistryEntry):
    _about_ = nocheck_getitem

    def compute_result_annotation(self, s_lst, s_int):
        position = getbookkeeper().position_key
        return s_lst.listdef.read_item(position)

    def specialize_call(self, hop):
        from rpython.rtyper.lltypesystem import lltype
        hop.exception_cannot_occur()
        r_list = hop.args_r[0]
        T = r_list.lowleveltype
        v_items, v_index = hop.inputargs(*hop.args_r)
        if hasattr(T.TO, "items"):
            cname = hop.inputconst(lltype.Void, "items")
            v_items = hop.genop(
                    'getfield', [v_items, cname], resulttype=T.TO.items)
            T = T.TO.items
        return r_list.recast(hop.llops, hop.genop('getarrayitem',
                [v_items, v_index], resulttype=T.TO.OF))


class Entry(extregistry.ExtRegistryEntry):
    _about_ = nocheck_setitem

    def compute_result_annotation(self, s_lst, s_int, s_value):
        s_lst.listdef.mutate()
        s_lst.listdef.generalize(s_value)

    def specialize_call(self, hop):
        from rpython.rtyper.lltypesystem import lltype
        hop.exception_cannot_occur()
        r_list = hop.args_r[0]
        T = r_list.lowleveltype
        v_items, v_index, v_value = hop.inputargs(r_list, lltype.Signed, r_list.item_repr)
        if hasattr(T.TO, "items"):
            cname = hop.inputconst(lltype.Void, "items")
            v_items = hop.genop(
                    'getfield', [v_items, cname], resulttype=T.TO.items)
        return hop.genop('setarrayitem', [v_items, v_index, v_value])





## ------------------------------------------------------------------------
## Lots of code for an adaptive, stable, natural mergesort.  There are many
## pieces to this algorithm; read listsort.txt for overviews and details.
## ------------------------------------------------------------------------
##         Adapted from CPython, original code and algorithms by Tim Peters


def merge_compute_minrun(n):
    # Compute a good value for the minimum run length; natural runs shorter
    # than this are boosted artificially via binary insertion.
    #
    # If n < 64, return n (it's too small to bother with fancy stuff).
    # Else if n is an exact power of 2, return 32.
    # Else return an int k, 32 <= k <= 64, such that n/k is close to, but
    # strictly less than, an exact power of 2.
    #
    # See listsort.txt for more info.
    r = 0    # becomes 1 if any 1 bits are shifted off
    while n >= 64:
        r |= n & 1
        n >>= 1
    return n + r

def powerloop(s1, n1, n2, n):
    # Two adjacent runs begin at index s1. The first run has length n1, and
    # the second run (starting at index s1+n1) has length n2. The list has total
    # length n.
    # Compute the "power" of the first run. See listsort.txt for details.
    assert s1 >= 0
    assert n1 >= 1 and n2 >= 1
    assert s1 + n1 + n2 <= n
    # a' = s1 + n1/2
    # b' = s1 + n1 + n2/2 = a' + (n1 + n2)/2
    a = 2 * s1 + n1       # 2 * a'
    b = a + n1 + n2       # 2 * b'
    result = 0
    while True:
        result += 1
        if a >= n:
            assert b >= a
            a -= n
            b -= n
        elif b >= n:
            break
        assert a < b < n
        a <<= 1
        b <<= 1
    return result

def make_timsort_class(getitem=None, setitem=None, length=None,
                       getitem_slice=None, lt=None, powersort=False):

    if getitem is None:
        getitem = nocheck_getitem

    if setitem is None:
        setitem = nocheck_setitem

    if length is None:
        def length(list):
            return len(list)

    if getitem_slice is None:
        def getitem_slice(list, start, stop):
            return list[start:stop]

    if lt is None:
        def lt(a, b):
            return a < b

    class TimSort(object):
        """TimSort(list).sort()

        Sorts the list in-place, using the overridable method lt() for comparison.
        """

        def __init__(self, list, listlength=None):
            self.list = list
            if listlength is None:
                listlength = length(list)
            self.listlength = listlength
            if not listlength:
                self.scratch_list = None
            else:
                scratchsize = min((len(list) + 1) // 2, 256)
                self.scratch_list = [getitem(list, 0)] * scratchsize

        def setitem(self, item, val):
            setitem(self.list, item, val)

        def lt(self, a, b):
            return lt(a, b)

        def le(self, a, b):
            return not self.lt(b, a)   # always use self.lt() as the primitive

        # binarysort is the best method for sorting small arrays: it does
        # few compares, but can do data movement quadratic in the number of
        # elements.
        # "a" is a contiguous slice of a list, and is sorted via binary insertion.
        # This sort is stable.
        # On entry, the first "sorted" elements are already sorted.
        # Even in case of error, the output slice will be some permutation of
        # the input (nothing is lost or duplicated).

        def binarysort(self, a, sorted=1):
            abase = a.base
            alist = a.list
            for start in range(a.base + sorted, a.base + a.len):
                # set l to where list[start] belongs
                l = abase
                r = start
                pivot = getitem(alist, r)
                # Invariants:
                # pivot >= all in [base, l).
                # pivot  < all in [r, start).
                # The second is vacuously true at the start.
                while l < r:
                    p = l + ((r - l) >> 1)
                    if self.lt(pivot, getitem(alist, p)):
                        r = p
                    else:
                        l = p+1
                assert l == r
                # The invariants still hold, so pivot >= all in [base, l) and
                # pivot < all in [l, start), so pivot belongs at l.  Note
                # that if there are elements equal to pivot, l points to the
                # first slot after them -- that's why this sort is stable.
                # Slide over to make room.
                for p in xrange(start, l, -1):
                    setitem(alist, p, getitem(alist, p-1))
                setitem(alist, l, pivot)

        # Compute the length of the run in the slice "a".
        # "A run" is the longest ascending sequence, with
        #
        #     a[0] <= a[1] <= a[2] <= ...
        #
        # or the longest descending sequence, with
        #
        #     a[0] > a[1] > a[2] > ...
        #
        # Return (run, descending) where descending is False in the former case,
        # or True in the latter.
        # For its intended use in a stable mergesort, the strictness of the defn of
        # "descending" is needed so that the caller can safely reverse a descending
        # sequence without violating stability (strict > ensures there are no equal
        # elements to get out of order).

        def count_run(self, a, resultrun):
            if a.len <= 1:
                n = a.len
                descending = False
            else:
                n = 2
                if self.lt(a.getitem(a.base + 1), a.getitem(a.base)):
                    descending = True
                    for p in xrange(a.base + 2, a.base + a.len):
                        if self.lt(a.getitem(p), a.getitem(p-1)):
                            n += 1
                        else:
                            break
                else:
                    descending = False
                    for p in xrange(a.base + 2, a.base + a.len):
                        if self.lt(a.getitem(p), a.getitem(p-1)):
                            break
                        else:
                            n += 1
            resultrun.len = n
            return descending

        # Locate the proper position of key in a sorted vector; if the vector
        # contains an element equal to key, return the position immediately to the
        # left of the leftmost equal element -- or to the right of the rightmost
        # equal element if the flag "rightmost" is set.
        #
        # "hint" is an index at which to begin the search, 0 <= hint < a.len.
        # The closer hint is to the final result, the faster this runs.
        #
        # The return value is the index 0 <= k <= a.len such that
        #
        #     a[k-1] < key <= a[k]      (if rightmost is False)
        #     a[k-1] <= key < a[k]      (if rightmost is True)
        #
        # as long as the indices are in bound.  IOW, key belongs at index k;
        # or, IOW, the first k elements of a should precede key, and the last
        # n-k should follow key.

        # hint for the annotator: the argument 'rightmost' is always passed in as
        # a constant (either True or False), so we can specialize the function for
        # the two cases.  (This is actually needed for technical reasons: the
        # variable 'lower' must contain a known method, which is the case in each
        # specialized version but not in the unspecialized one.)
        @specialize.arg(4)
        def gallop(self, key, a, hint, rightmost):
            assert 0 <= hint < a.len
            if rightmost:
                lower = self.le   # search for the largest k for which a[k] <= key
            else:
                lower = self.lt   # search for the largest k for which a[k] < key

            p = a.base + hint
            lastofs = 0
            ofs = 1
            if lower(a.getitem(p), key):
                # a[hint] < key -- gallop right, until
                #     a[hint + lastofs] < key <= a[hint + ofs]

                maxofs = a.len - hint     # a[a.len-1] is highest
                while ofs < maxofs:
                    if lower(a.getitem(p + ofs), key):
                        lastofs = ofs
                        try:
                            ofs = ovfcheck(ofs << 1)
                        except OverflowError:
                            ofs = maxofs
                        else:
                            ofs = ofs + 1
                    else:  # key <= a[hint + ofs]
                        break

                if ofs > maxofs:
                    ofs = maxofs
                # Translate back to offsets relative to a.
                lastofs += hint
                ofs += hint

            else:
                # key <= a[hint] -- gallop left, until
                #     a[hint - ofs] < key <= a[hint - lastofs]
                maxofs = hint + 1   # a[0] is lowest
                while ofs < maxofs:
                    if lower(a.getitem(p - ofs), key):
                        break
                    else:
                        # key <= a[hint - ofs]
                        lastofs = ofs
                        try:
                            ofs = ovfcheck(ofs << 1)
                        except OverflowError:
                            ofs = maxofs
                        else:
                            ofs = ofs + 1
                if ofs > maxofs:
                    ofs = maxofs
                # Translate back to positive offsets relative to a.
                lastofs, ofs = hint-ofs, hint-lastofs

            assert -1 <= lastofs < ofs <= a.len

            # Now a[lastofs] < key <= a[ofs], so key belongs somewhere to the
            # right of lastofs but no farther right than ofs.  Do a binary
            # search, with invariant a[lastofs-1] < key <= a[ofs].

            lastofs += 1
            while lastofs < ofs:
                m = lastofs + ((ofs - lastofs) >> 1)
                if lower(a.getitem(a.base + m), key):
                    lastofs = m+1   # a[m] < key
                else:
                    ofs = m         # key <= a[m]

            assert lastofs == ofs         # so a[ofs-1] < key <= a[ofs]
            return ofs


        # ____________________________________________________________

        # When we get into galloping mode, we stay there until both runs win less
        # often than MIN_GALLOP consecutive times.  See listsort.txt for more info.
        MIN_GALLOP = 7

        def merge_init(self):
            # This controls when we get *into* galloping mode.  It's initialized
            # to MIN_GALLOP.  merge_lo and merge_hi tend to nudge it higher for
            # random data, and lower for highly structured data.
            self.min_gallop = self.MIN_GALLOP

            # A stack of n pending runs yet to be merged.  Run #i starts at
            # address pending[i].base and extends for pending[i].len elements.
            # It's always true (so long as the indices are in bounds) that
            #
            #     pending[i].base + pending[i].len == pending[i+1].base
            #
            # so we could cut the storage for this, but it's a minor amount,
            # and keeping all the info explicit simplifies the code.
            self.pending = [] 
            #    XXX should try [ListSlice(None,0,0)] * 85 # allocate with fixed size as in CPython

        # Merge the slice "a" with the slice "b" in a stable way, in-place.
        # a.len and b.len must be > 0, and a.base + a.len == b.base.
        # Must also have that b.list[b.base] < a.list[a.base], that
        # a.list[a.base+a.len-1] belongs at the end of the merge, and should have
        # a.len <= b.len.  See listsort.txt for more info.

        def merge_lo(self, a, b):
            assert a.len > 0 and b.len > 0 and a.base + a.len == b.base
            min_gallop = self.min_gallop
            dest = a.base
            a.copyitems(self)

            # Invariant: elements in "a" are waiting to be reinserted into the list
            # at "dest".  They should be merged with the elements of "b".
            # b.base == dest + a.len.
            # We use a finally block to ensure that the elements remaining in
            # the copy "a" are reinserted back into self.list in all cases.
            try:
                self.setitem(dest, b.popleft())
                dest += 1
                if a.len == 1 or b.len == 0:
                    return

                while True:
                    acount = 0   # number of times A won in a row
                    bcount = 0   # number of times B won in a row

                    # Do the straightforward thing until (if ever) one run
                    # appears to win consistently.
                    while True:
                        if self.lt(b.getitem(b.base), a.getitem(a.base)):
                            self.setitem(dest, b.popleft())
                            dest += 1
                            if b.len == 0:
                                return
                            bcount += 1
                            acount = 0
                            if bcount >= min_gallop:
                                break
                        else:
                            self.setitem(dest, a.popleft())
                            dest += 1
                            if a.len == 1:
                                return
                            acount += 1
                            bcount = 0
                            if acount >= min_gallop:
                                break

                    # One run is winning so consistently that galloping may
                    # be a huge win.  So try that, and continue galloping until
                    # (if ever) neither run appears to be winning consistently
                    # anymore.
                    min_gallop += 1

                    while True:
                        min_gallop -= min_gallop > 1
                        self.min_gallop = min_gallop

                        acount = self.gallop(b.getitem(b.base), a, hint=0,
                                             rightmost=True)
                        for p in xrange(a.base, a.base + acount):
                            self.setitem(dest, a.getitem(p))
                            dest += 1
                        a.advance(acount)
                        # a.len==0 is impossible now if the comparison
                        # function is consistent, but we can't assume
                        # that it is.
                        if a.len <= 1:
                            return

                        self.setitem(dest, b.popleft())
                        dest += 1
                        if b.len == 0:
                            return

                        bcount = self.gallop(a.getitem(a.base), b, hint=0,
                                             rightmost=False)
                        for p in xrange(b.base, b.base + bcount):
                            self.setitem(dest, b.getitem(p))
                            dest += 1
                        b.advance(bcount)
                        if b.len == 0:
                            return

                        self.setitem(dest, a.popleft())
                        dest += 1
                        if a.len == 1:
                            return

                        if acount < self.MIN_GALLOP and bcount < self.MIN_GALLOP:
                            break

                    min_gallop += 1  # penalize it for leaving galloping mode
                    self.min_gallop = min_gallop

            finally:
                # The last element of a belongs at the end of the merge, so we copy
                # the remaining elements of b before the remaining elements of a.
                assert a.len >= 0 and b.len >= 0
                for p in xrange(b.base, b.base + b.len):
                    self.setitem(dest, b.getitem(p))
                    dest += 1
                for p in xrange(a.base, a.base + a.len):
                    self.setitem(dest, a.getitem(p))
                    dest += 1

        # Same as merge_lo(), but should have a.len >= b.len.

        def merge_hi(self, a, b):
            assert a.len > 0 and b.len > 0 and a.base + a.len == b.base
            min_gallop = self.min_gallop
            dest = b.base + b.len
            b.copyitems(self)

            # Invariant: elements in "b" are waiting to be reinserted into the list
            # before "dest".  They should be merged with the elements of "a".
            # a.base + a.len == dest - b.len.
            # We use a finally block to ensure that the elements remaining in
            # the copy "b" are reinserted back into self.list in all cases.
            try:
                dest -= 1
                self.setitem(dest, a.popright())
                if a.len == 0 or b.len == 1:
                    return

                while True:
                    acount = 0   # number of times A won in a row
                    bcount = 0   # number of times B won in a row

                    # Do the straightforward thing until (if ever) one run
                    # appears to win consistently.
                    while True:
                        nexta = a.getitem(a.base + a.len - 1)
                        nextb = b.getitem(b.base + b.len - 1)
                        if self.lt(nextb, nexta):
                            dest -= 1
                            self.setitem(dest, nexta)
                            a.len -= 1
                            if a.len == 0:
                                return
                            acount += 1
                            bcount = 0
                            if acount >= min_gallop:
                                break
                        else:
                            dest -= 1
                            self.setitem(dest, nextb)
                            b.len -= 1
                            if b.len == 1:
                                return
                            bcount += 1
                            acount = 0
                            if bcount >= min_gallop:
                                break

                    # One run is winning so consistently that galloping may
                    # be a huge win.  So try that, and continue galloping until
                    # (if ever) neither run appears to be winning consistently
                    # anymore.
                    min_gallop += 1

                    while True:
                        min_gallop -= min_gallop > 1
                        self.min_gallop = min_gallop

                        nextb = b.getitem(b.base + b.len - 1)
                        k = self.gallop(nextb, a, hint=a.len-1, rightmost=True)
                        acount = a.len - k
                        for p in xrange(a.base + a.len - 1, a.base + k - 1, -1):
                            dest -= 1
                            self.setitem(dest, a.getitem(p))
                        a.len -= acount
                        if a.len == 0:
                            return

                        dest -= 1
                        self.setitem(dest, b.popright())
                        if b.len == 1:
                            return

                        nexta = a.getitem(a.base + a.len - 1)
                        k = self.gallop(nexta, b, hint=b.len-1, rightmost=False)
                        bcount = b.len - k
                        for p in xrange(b.base + b.len - 1, b.base + k - 1, -1):
                            dest -= 1
                            self.setitem(dest, b.getitem(p))
                        b.len -= bcount
                        # b.len==0 is impossible now if the comparison
                        # function is consistent, but we can't assume
                        # that it is.
                        if b.len <= 1:
                            return

                        dest -= 1
                        self.setitem(dest, a.popright())
                        if a.len == 0:
                            return

                        if acount < self.MIN_GALLOP and bcount < self.MIN_GALLOP:
                            break

                    min_gallop += 1  # penalize it for leaving galloping mode
                    self.min_gallop = min_gallop

            finally:
                # The last element of a belongs at the end of the merge, so we copy
                # the remaining elements of a and then the remaining elements of b.
                assert a.len >= 0 and b.len >= 0
                for p in xrange(a.base + a.len - 1, a.base - 1, -1):
                    dest -= 1
                    self.setitem(dest, a.getitem(p))
                for p in xrange(b.base + b.len - 1, b.base - 1, -1):
                    dest -= 1
                    self.setitem(dest, b.getitem(p))

        # Merge the two runs at stack indices i and i+1.

        def merge_at(self, i):
            a = self.pending[i]
            b = self.pending[i+1]
            assert a.len > 0 and b.len > 0
            assert a.base + a.len == b.base

            # Record the length of the combined runs and remove the run b
            self.pending[i] = ListSlice(self.list, a.base, a.len + b.len)
            del self.pending[i+1]

            # Where does b start in a?  Elements in a before that can be
            # ignored (already in place).
            k = self.gallop(b.getitem(b.base), a, hint=0, rightmost=True)
            a.advance(k)
            if a.len == 0:
                return

            # Where does a end in b?  Elements in b after that can be
            # ignored (already in place).
            b.len = self.gallop(a.getitem(a.base+a.len-1), b, hint=b.len-1,
                                rightmost=False)
            if b.len == 0:
                return

            # Merge what remains of the runs.  The direction is chosen to
            # minimize the temporary storage needed.
            if a.len <= b.len:
                self.merge_lo(a, b)
            else:
                self.merge_hi(a, b)

        def found_new_run(self, run):
            """
            The next run has been identified.
            If there's already a run on the stack, apply the "powersort" merge strategy:
            compute the topmost run's "power" (depth in a conceptual binary merge tree)
            and merge adjacent runs on the stack with greater power. See listsort.txt
            for more info.

            It's the caller's responsibilty to push the new run on the stack when this
            returns.

            See listsort.txt for more info.
            """

            p = self.pending
            if p:
                s1 = p[-1].base
                n1 = p[-1].len
                power = powerloop(s1, n1, run.len, self.listlength)
                while len(p) > 1 and p[-2].power > power:
                    self.merge_at(-2)
                assert len(p) < 2 or p[-2].power < power
                p[-1].power = power;

        def merge_collapse(self):
            p = self.pending
            while len(p) > 1:
                if len(p) >= 3 and p[-3].len <= p[-2].len + p[-1].len:
                    if p[-3].len < p[-1].len:
                        self.merge_at(-3)
                    else:
                        self.merge_at(-2)
                elif p[-2].len <= p[-1].len:
                    self.merge_at(-2)
                else:
                    break

        def merge_force_collapse(self):
            p = self.pending
            while len(p) > 1:
                n = -2
                if len(p) >= 3 and p[-3].len < p[-1].len:
                    n = -3
                self.merge_at(n)

        merge_compute_minrun = staticmethod(merge_compute_minrun)

        # ____________________________________________________________
        # Entry point.

        def sort(self):
            if self.listlength < 2:
                return
            remaining = ListSlice(self.list, 0, self.listlength)

            # March over the array once, left to right, finding natural runs,
            # and extending short natural runs to minrun elements.
            self.merge_init()
            minrun = self.merge_compute_minrun(remaining.len)

            while remaining.len > 0:
                # Identify next run.
                run = ListSlice(remaining.list, remaining.base, remaining.len)
                descending = self.count_run(remaining, run)
                if descending:
                    run.reverse()
                # If short, extend to min(minrun, nremaining).
                if run.len < minrun:
                    sorted = run.len
                    run.len = min(minrun, remaining.len)
                    self.binarysort(run, sorted)
                if powersort:
                    # maybe merge (but never the newest)
                    self.found_new_run(run)
                    # Push run onto pending-runs stack
                    self.pending.append(run)
                    # Advance remaining past this run.
                    remaining.advance(run.len)
                else:
                    # timsort

                    # Advance remaining past this run.
                    remaining.advance(run.len)
                    # Push run onto pending-runs stack, and maybe merge.
                    self.pending.append(run)
                    self.merge_collapse()

            assert remaining.base == self.listlength

            self.merge_force_collapse()
            assert len(self.pending) == 1
            assert self.pending[0].base == 0
            assert self.pending[0].len == self.listlength

    class ListSlice:
        "A sublist of a list."

        def __init__(self, list, base, len):
            self.list = list
            self.base = base
            self.len  = len
            if powersort:
                self.power = 0 # invalid value that is overwritten later; allocate it here so all objects have the field

        def __repr__(self):
            return "<ListSlice base=%s len=%s %s>" % (
                    self.base, self.len, self.list[self.base: self.base+self.len])

        def copyitems(self, sorter):
            "Make a copy of the slice of the original list."
            if sorter.scratch_list is None or self.len > len(sorter.scratch_list):
                start = self.base
                stop  = self.base + self.len
                assert 0 <= start <= stop     # annotator hint
                scratch_list = sorter.scratch_list = getitem_slice(self.list, start, stop)
            else:
                scratch_list = sorter.scratch_list
                base = self.base
                # XXX we want arraycopy but it's lltype only so far
                for i in range(self.len):
                    scratch_list[i] = self.list[base + i]
            self.list = scratch_list
            self.base = 0

        def advance(self, n):
            self.base += n
            self.len -= n

        def getitem(self, item):
            return getitem(self.list, item)

        def setitem(self, item, value):
            setitem(self.list, item, value)

        def popleft(self):
            result = getitem(self.list, self.base)
            self.base += 1
            self.len -= 1
            return result

        def popright(self):
            self.len -= 1
            return getitem(self.list, self.base + self.len)

        def reverse(self):
            "Reverse the slice in-place."
            list = self.list
            lo = self.base
            hi = lo + self.len - 1
            while lo < hi:
                list_hi = getitem(list, hi)
                list_lo = getitem(list, lo)
                setitem(list, lo, list_hi)
                setitem(list, hi, list_lo)
                lo += 1
                hi -= 1
    return TimSort

from pyflate_list import *

TimSort = make_timsort_class()

TimSortWrapped = make_timsort_class(lt=wrapper_lt)

PowerSort = make_timsort_class(powersort=True)

PowerSortWrapped = make_timsort_class(lt=wrapper_lt, powersort=True)







# __________  Entry point  __________


def entry_point(argv):
    variant = "powersort"
    if len(argv) >= 2:
        variant = argv[1]

    runs = 1000
    if len(argv) >= 3:
        runs = int(argv[2])
    
    #l = argv[1].split(",")
    #print(l)
    #TimSort(l).sort()
    #print(l)
    s = 0
    pyflate_list = [Wrapper(i) for i in pyflate_list_raw]
    if variant == "timsort":
        print("Running TimSort on raw pyflate list")
        for rep in range(runs):
            l = pyflate_list_raw[:]
            TimSort(l).sort()
            s += l[-42]
    elif variant == "timsort-wrapped":
        print("Running TimSort on wrapped pyflate list")
        for rep in range(runs):
            l = pyflate_list[:]
            TimSortWrapped(l).sort()
            s += l[-42]._key
    elif variant == "powersort":
        print("Running Powersort on raw pyflate list")
        for rep in range(runs):
            l = pyflate_list_raw[:]
            PowerSort(l).sort()
            s += l[-42]
    elif variant == "powersort-wrapped":
        print("Running Powersort on wrapped pyflate list")
        for rep in range(runs):
            l = pyflate_list[:]
            PowerSortWrapped(l).sort()
            s += l[-42]._key
#    elif variant == "list-sort":
#        print("Running Powersort on raw pyflate list")
#        for rep in range(runs):
#            l = pyflate_list_raw[:]
#            l.sort()
#            s += l[-42]
    else:
        print "invalid variant", variant
        return 1
    print(s)
    return 0

# _____ Define and setup target ___

def target(*args):
    return entry_point



