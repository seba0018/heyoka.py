#!/usr/bin/env bash

# Echo each command
#set -x

# Exit on error.
#set -e

# Core deps.
sudo apt-get install build-essential wget clang

# Install conda+deps.
wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-ppc64le.sh -O miniconda.sh
export deps_dir=$HOME/local
export PATH="$HOME/miniconda/bin:$PATH"
bash miniconda.sh -b -p $HOME/miniconda
mamba create -y -q -p $deps_dir cxx-compiler c-compiler cmake llvmdev boost-cpp sleef xtensor xtensor-blas blas blas-devel fmt spdlog python=3.8 pybind11 numpy mpmath sympy cloudpickle
source activate $deps_dir

# Checkout, build and install heyoka's HEAD.
git clone https://github.com/bluescarni/heyoka.git heyoka_cpp
cd heyoka_cpp
mkdir build
cd build

export LDFLAGS="-shared-libasan ${LDFLAGS}"

# GCC build.
CC=clang CXX=clang++ cmake ../ -DCMAKE_INSTALL_PREFIX=$deps_dir -DCMAKE_PREFIX_PATH=$deps_dir -DCMAKE_BUILD_TYPE=Debug -DHEYOKA_WITH_SLEEF=yes -DBoost_NO_BOOST_CMAKE=ON -DCMAKE_CXX_FLAGS="-fsanitize=address -fno-common -U_FORTIFY_SOURCE"
make -j2 VERBOSE=1 install

cd ../../

# Create the build dir and cd into it.
mkdir build
cd build

CC=clang CXX=clang++ cmake ../ -DCMAKE_INSTALL_PREFIX=$deps_dir -DCMAKE_PREFIX_PATH=$deps_dir -DCMAKE_BUILD_TYPE=Debug -DHEYOKA_PY_ENABLE_IPO=yes -DBoost_NO_BOOST_CMAKE=ON -DCMAKE_CXX_FLAGS="-fsanitize=address -fno-common -U_FORTIFY_SOURCE"
make -j2 VERBOSE=1 install

cd

while true
do
	LD_PRELOAD=$(clang -print-file-name=libclang_rt.asan-powerpc64le.so) python -c "from heyoka import test; test.run_test_suite()" 2>&1 > out.txt
    export BLAF=`grep -i invalid out.txt`
	if [[ "${BLAF}" != "" ]]; then
        echo "INVALID, printing:"
        cat out.txt
        exit 1
    else
        echo "Nothing found"
    fi
    rm out.txt
done

#LD_PRELOAD=$(clang -print-file-name=libclang_rt.asan-powerpc64le.so) python -c "from heyoka import test; test.run_test_suite()"

#set +e
#set +x