#
# MIT License
#
# (C) Copyright [2024] Hewlett Packard Enterprise Development LP
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
"""Public API module for the ubuntu platform layer, this gives callers
access to the Platform API and prevents them from seeing the private
implementation of the API.

"""
from abc import (
    ABCMeta,
    abstractmethod
)
from ..layerapi import LayerAPI


class PlatformAPI(LayerAPI, metaclass=ABCMeta):
    """ Presents the Platform API to callers.

    """
    @abstractmethod
    def get_blade_venv_path(self):
        """Return the file system path to the root of the shared blade
        virtual environment created and managed by the Platform layer.

        """

    @abstractmethod
    def get_blade_python_executable(self):
        """Return the file system path to the executable python
        interpreter within the shared blade virtual environment
        created and managed by the Platform layer.

        """
