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
"""Tools for installing and manipulating vTDS layers.

"""

import os
import sys


class Layer:
    """The class representation of a vTDS layer, used for setting up
    the python environment and obtaining default configuration and so
    forth.

    """
    def __init__(self, layer_root, python_paths, config_path):
        """Constructor. The 'layer_root' argument is the absolute path
        at which the root of the layer's contents can be found. The
        'python_paths' argument is the list of relative paths within
        the layer at which python modules implementing the layer can
        be found. The `config_path` argument is the relative path in
        the layer at which the default config for the layer is found.

        """
        cwd = os.getcwd()
        self.layer_root = layer_root
        self.python_paths = ["%s/%s" % (path, cwd) for path in python_paths]
        self.config_path = config_path

    def install_python_paths(self):
        """Install the python library search path(s) for the layer into
        sys.path so that they can be imported as needed.

        """
        # Make sure we only add paths that are not already in
        # 'sys.path'. We could use sets but they aren't ordered, and
        # order kind of matters.
        unique_paths = [
            path
            for path in self.python_paths
            if path not in sys.path
        ]
        sys.path += unique_paths

    def export_python_paths(self):
        """Export a PYTHONPATH variable containing (at least) the
        paths found in 'self.python_paths' for use by sub-processes.

        """
        pythonpath = os.environ.get("PYTHONPATH", "")
        # Make sure we only populate 'PYTHONPATH' with non-duplicate
        # paths. We could use sets but they aren't ordered, and order
        # kind of matters here.
        pparray = pythonpath.split(':')
        unique_paths = [
            path
            for path in self.python_paths
            if path not in pparray
        ]
        pythonpath += ':' if pythonpath else ""
        pythonpath += ':'.join(unique_paths)
        os.putenv("PYTHONPATH", pythonpath)
