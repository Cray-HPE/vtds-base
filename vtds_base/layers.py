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
import importlib
from .errors import ContextualError


class Layer:
    """The class representation of a vTDS layer, used for calling that
    layer's API and obtaining that layer's base and test configuration
    data.

    """
    def __init__(self, module_name):
        """Constructor. The 'module_name' is used to import the layer
        and install the layer's API and base configuration implementation.

        """
        try:
            module = importlib.import_module(module_name)
            self.layer_api_class = module.LayerAPI
            self.base_config = module.BaseConfig()
            self.layer_api = None
        except ImportError as err:
            raise ContextualError(
                "cannot import layer module '%s' - %s" % (
                    module_name, str(err)
                )
            ) from err
        except AttributeError as err:
            raise ContextualError(
                "layer module '%s' does not implement a vTDS layer - %s" % (
                    module_name, str(err)
                )
            ) from err

    def initialize(self, stack, config, build_dir):
        """Initialize a layer, setting up its actual implementation
        based on the stack of layers loaded, the overall fully resolved
        vTDS configuration and the path to the build directory for the
        specific layer.

        """
        self.layer_api = self.layer_api_class(stack, config, build_dir)

    def get_api(self):
        """Return the layer API implementation object for use by the
        caller.

        """
        return self.layer_api


class FullStack:
    """The class representation of the full stack of layers:
    application, cluster, platform and provider.

    """
    def __init__(
            self,
            application=None,
            cluster=None,
            platform=None,
            provider=None
    ):
        """Constructor. Stash the Layer objects for each of the layers
        in a vTDS system here for use by whoever needs access to
        another layer.

        """
        self.application = application
        self.cluster = cluster
        self.platform = platform
        self.provider = provider

    def __init_layer__(self, name, layer, config, build_dir):
        """Initialize a layer where 'name' identifies the name of the
        layer in the stack (used to sub-divide the build directory
        tree), 'layer' is the Layer object containing the layer
        information, 'config' is the full vTDS configuration to be
        supplied the layer and 'build_dir' is the root of the build
        directory tree. The build directory tree and sub-directories
        for each layer are created as needed.

        """
        if layer is None:
            # No such layer present, this is not an error, but we
            # don't want to go any further.
            return
        layer_build_dir = os.path.join(build_dir, name)
        try:
            os.makedirs(layer_build_dir, 0o700, True)
        except OSError as err:
            raise ContextualError(
                "failed to create build directory for layer "
                "'%s' ['%s'] - %s" % (name, layer_build_dir, str(err))
            ) from err
        layer.initialize(self, config, layer_build_dir)

    def initialize(self, config, build_dir):
        """Initialize all of the layers rooted at 'build_dir' and
        supplying the full vTDS configuration found in 'config'. Each
        layer will have a sub-directory created for it in the build
        directory tree.

        """
        self.__init_layer__("application", self.application, config, build_dir)
        self.__init_layer__("cluster", self.cluster, config, build_dir)
        self.__init_layer__("platform", self.platform, config, build_dir)
        self.__init_layer__("provider", self.provider, config, build_dir)

    def get_application(self):
        """Accessor for the applicaiton layer.

        """
        return self.application()

    def get_cluster(self):
        """Accessor for the cluster layer.

        """
        return self.cluster()

    def get_platform(self):
        """Accessor for the platform layer.

        """
        return self.platform()

    def get_provider(self):
        """Accessor for the provider layer.

        """
        return self.provider()
