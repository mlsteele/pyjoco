#!/usr/bin/env python
# https://bitbucket.org/pypy/numpy/issues/60/crash-in-nprandomshuffle
# Python 2.7.13 (1aa2d8e03cdfab54b7121e93fda7e98ea88a30bf, Apr 04 2017, 12:21:42)
# [PyPy 5.7.1 with GCC 6.3.0] on linux2
# pypy -m pip install git+https://bitbucket.org/pypy/numpy.git
import numpy as np

colors = np.zeros((2,1))
np.random.shuffle(colors)
print colors
