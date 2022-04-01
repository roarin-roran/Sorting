## Mergesorts in Python

* `pypy-sorters` contains RPython implementations of Timsort and Powersort from pypy ported to Python 3, and the pyflate list as simply benchmark.
* `rpython-benchmarks` contains RPython targets (to be compiled using `bin/rpython` from a pypy source copy) for Timsort and Powersort using the pyflate list.
* Other folders contain Ben's cleanroom implementation of mergesorts.



Interfaces are defined for each substitutable class, currently MergerIPQ and Sorter

one MergerIPQ is currently used - a dummy method that makes no pretense to efficiency

Two sorters are currently used, with an intermediate class defining methods which they both share - PingPong memory
    management

Adaptive sorting takes account of run length, Bottom up does not.

the mothballed folder contains several old attempts at making the mergeSorter class, retained for reference.
