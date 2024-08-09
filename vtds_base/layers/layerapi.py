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
    def prepare(self):
        """Prepare the provider for deployment.

        """

    @abstractmethod
    def validate(self):
        """Run any configuration validation that may be appropriate
        for the provider layer.

        """

    @abstractmethod
    def deploy(self):
        """Deploy the provider (must call prepare() prior to this
        call.

        """

    @abstractmethod
    def shutdown(self, virtual_blade_names=None):
        """Shutdown operation. This will shut down (power off) the
        specified virtual blades, or, if none are specified, all
        virtual blades, in the provider, leaving them provisioned.

        """

    @abstractmethod
    def startup(self, virtual_blade_names=None):
        """Startup operation. This will start up (power on) the
        specified virtual blades, or, if none are specified, all
        virtual blades, in the provider as long as they are
        provisioned.

        """

    @abstractmethod
    def dismantle(self):
        """Dismantle operation. This will de-provision all virtual
        blades in the provider.

        """

    @abstractmethod
    def restore(self):
        """Restore operation. This will re-provision deprovisioned
        virtual blades in the provider.

        """

    @abstractmethod
    def remove(self):
        """Remove operation. This will remove all resources
        provisioned for the provider layer.

        """
