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
"""Public API module for the GCP provider layer, this gives callers
access to the Provider API and prevents them from seeing the private
GCP specific implementation of the API.

"""
from abc import (
    ABCMeta,
    abstractmethod
)
from ..layerapi import LayerAPI


class ProviderAPI(LayerAPI, metaclass=ABCMeta):
    """ Provider class presents the Provider API to callers.

    """
    @abstractmethod
    def get_virtual_blades(self):
        """Return a the VirtualBlades object containing all of the
        available non-pure-base-class Virtual Blades.

        """

    @abstractmethod
    def get_blade_interconnects(self):
        """Return a BladeInterconnects object containing all the
        available non-pure-base-class Blade Interconnects.

        """

    @abstractmethod
    def get_secrets(self):
        """Return a Secrets API object that provides access to all
        available secrets.

        """

    @abstractmethod
    def get_site_config(self):
        """Retrieve the SiteConfig API object from the Provider.

        """
