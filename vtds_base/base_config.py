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
"""Operations on configuration structures.

"""

from os.path import join as path_join
from .errors import ContextualError
from .config_operations import read_config


# pylint: disable=too-few-public-methods
class BaseConfiguration:
    """BaseConfig class presents operations on the base configuration
    of the provider layer to callers.

    """
    def __init__(
            self,
            description,
            config_dir,
            config_file="config.yaml",
            test_overlay="test_overlay.yaml"
    ):
        """Constructor

        """
        self.config_dir = config_dir
        self.config_file = config_file
        self.test_overlay = test_overlay
        self.description = description

    def get_base_config(self):
        """Retrieve the base configuration for the provider in the
        form of a python data structure for use in composing and
        overall vTDS configuration.

        """
        config = path_join(self.config_dir, self.config_file)
        description = self.description + " base configuration"
        return read_config(config, description)

    def get_test_overlay(self):
        """Retrieve a pre-defined test overlay configuration in the
        form of a python data structure for use in composing vTDS
        configurations for testing with this provider layer.

        """
        config = path_join(self.config_dir, self.test_overlay)
        description = self.description + " test configuration overlay"
        return read_config(config, description)

    def get_base_config_text(self):
        """Retrieve the text of the base configuration file as a text
        string (UTF-8 encoded) for use in displaying the configuration
        to users.

        """
        config = path_join(self.config_dir, self.config_file)
        try:
            with open(config, 'r', encoding='UTF-8') as config_stream:
                return config_stream.read()
        except OSError as err:
            raise ContextualError(
                "cannot open %s base config file '%s' - %s" % (
                    self.description,
                    config, str(err)
                )
            ) from err
