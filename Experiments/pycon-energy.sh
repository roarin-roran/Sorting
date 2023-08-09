#! /bin/bash
repetitions=100
#echo `which python`
algo=`which python`
algo=${algo%/venv/bin/python}
algo=${algo#/home/swild/Uni/projects/cpython-3.11-}
outfile="PyConEnergy-${algo}-energy"
echo "Running $algo for $repetitions repetitions, writing to $outfile."

perf stat -o $outfile.data -r $repetitions -e power/energy-cores/,power/energy-ram/,power/energy-gpu/,power/energy-pkg/,power/energy-psys/ python PyConRunningTimes.py > $outfile
