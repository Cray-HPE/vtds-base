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
"""The base layer API class which provides the methods (in pure
virtual form) used by vtds-core to manage vTDS systems. All layers
implement thes methods.

"""
from abc import (
    ABCMeta,
    abstractmethod
)


class LayerAPI(metaclass=ABCMeta):
    """A class defining the minimum Layer API for all vTDS layer
    implementations.

    """
    @abstractmethod
    def consolidate(self):
        """Consolidate layer configurations, carrying out any actions
        that might affect other layer configurations. At the end of
        this phase, the overall configuration is fully specified and
        ready for use by prepare and validate.

        """

    @abstractmethod
    def prepare(self):
        """Prepare data files and other state needed for
        deployment. At the end of this stage the layer is ready to be
        displayed, validated, deployed or removed.

        """

    @abstractmethod
    def validate(self):
        """Run any configuration validation that may be appropriate
        for the layer and fail if that validation
        fails. Prerequisites: consolidate() and prepare().

        """

    @abstractmethod
    def deploy(self):
        """Deploy the layer. Prerequisites: consolidate() and prepare().

        """

    @abstractmethod
    def remove(self):
        """Remove respources owned by the layer. Prerequisites:
        consolidate() and prepare().

        """
