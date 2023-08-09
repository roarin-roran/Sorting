#! /bin/bash
repetitions=1
timestamp=`date +%Y-%m-%d_%H-%M-%S`
host=`hostname`
#echo `which python`
algo=`which python`
algo=${algo%/venv/bin/python}
algo=${algo#*cpython-3.11-}
outfile="PyConEnergy-${algo}-energy-$host-$timestamp"
echo "Running $algo for $repetitions repetitions, writing to $outfile."

perf stat -o $outfile.data -r $repetitions -e power/energy-cores/,power/energy-ram/,power/energy-gpu/,power/energy-pkg/ python PyConRunningTimes.py > $outfile
