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
"""Public API for the GCP provider layer base configuration data, this
gives callers access to the Provider's BaseConfig API and prevents
them from seeing the private GCP specific implementation of the API.

"""
from abc import (
    ABCMeta,
    abstractmethod
)


class BaseConfig(meta_class=ABCMeta):
    """BaseConfig class presents operations on the base configuration
    of the provider layer to callers.

    """
    @abstractmethod
    def get_base_config(self):
        """Retrieve the base configuration for the provider in the
        form of a python data structure for use in composing and
        overall vTDS configuration.

        """

    @abstractmethod
    def get_base_config_text(self):
        """Retrieve the text of the base configuration file as a text
        string (UTF-8 encoded) for use in displaying the configuration
        to users.

        """

    @abstractmethod
    def get_test_overlay(self):
        """Retrieve a pre-defined test overlay configuration in the
        form of a python data structure for use in composing vTDS
        configurations for testing with this provider layer.

        """
