#! /bin/sh
BUILDDIR=cmake-build-debug
mkdir $BUILDDIR
cd $BUILDDIR
cmake -DCMAKE_BUILD_TYPE=Debug ..
make runUnitTests
src/test/runUnitTests
cd ..
