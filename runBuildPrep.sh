#!/bin/bash
#
# MIT License
# 
# (C) Copyright 2024 Hewlett Packard Enterprise Development LP
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

set -x
export PATH="${PATH}:${HOME}/.local/bin"
set +x
pip3 install --upgrade pip
pip3 install --upgrade --no-use-pep517 nox
pip3 install --upgrade wheel

hash -r   # invalidate hash tables since we may have moved things around
pip3 install --ignore-installed virtualenv
pip3 install --ignore-installed -r requirements-style.txt
pip3 install --ignore-installed -r requirements-lint.txt
pip3 install --ignore-installed -r requirements-test.txt
pip3 install --ignore-installed build
hash -r   # invalidate hash tables since we may have moved things around

find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf


set -e

# Remove before just to ensure a clean nox env.
rm -rf .nox

# Lint the code and fail early if that is going to fail.
nox -s lint

# Style check the code and fail early if that is going to fail
nox -s style

# Run unit tests and fail early if that is going to fail
#
# Temporarily Disabled until there are unit tests to run
# nox -s tests

# Remove these files again to speed up source tar for build step.
rm -rf .nox
