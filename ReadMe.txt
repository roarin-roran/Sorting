sorterManager creates inputs with various levels of presortedness, and will be expanded to add analysis functions

mergeSorter sorts an input using two-way ping-pong merge sort, as well as a k-way merge sort
it will be expanded to add run detection.

tournamentTree constructs an (unfinished) explicit tournament tree for k way merging, and will be expaned to include a more efficient binary heap version

the mothballed folder contains several old attempts at making the mergeSorter class, retained for reference.



planned major features:
1. merge sorter interface, formatting our merger as an instance
2. naming conventions
3. merge method interface, separating our merger as an instance
    only need the one merger to support both existing sorters, taking a list of list slices as input
4. virtual sentinels
5. real IPQ
    tournament tree should make its own empty runs
6. top down
7. galloping merge

planned minor features:
1. basic test suite - random inputs and timing, output to screen
2. local k value for the ends - no point in having more than 50% of runs empty in a merge

delivered major features:
1. run detection
2. ListSlice object - implement and use