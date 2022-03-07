Interfaces are defined for each substitutable class, currently MergerIPQ and Sorter

one MergerIPQ is currently used - a dummy method that makes no pretense to efficiency

Two sorters are currently used, with an intermediate class defining methods which they both share - PingPong memory
    management

Adaptive sorting takes account of run length, Bottom up does not.

the mothballed folder contains several old attempts at making the mergeSorter class, retained for reference.



planned major features:
1. merge sorter interface, formatting our merger as an instance
2. merge method interface, separating our merger as an instance
    only need the one merger to support both existing sorters, taking a list of list slices as input
3. virtual sentinels
4. real IPQ
    tournament tree should make its own empty runs
5. top down
6. galloping merge

planned minor features:
1. basic test suite - random inputs and timing, output to screen
2. local k value for the ends - no point in having more than 50% of runs empty in a merge

delivered major features:
1. run detection
2. ListSlice object - implement and use
3. naming conventions