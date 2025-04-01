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

from os import makedirs
from os.path import join as path_join
import importlib
from .errors import ContextualError
from .config_operations import merge_configs


class Layer:
    """The class representation of a vTDS layer, used for calling that
    layer's API and obtaining that layer's base and test configuration
    data.

    """
    def __init__(self, module_name, is_core=False):
        """Constructor. The 'module_name' is used to import the layer
        and install the layer's API and base configuration implementation.

        """
        self.is_core = is_core
        try:
            module = importlib.import_module(module_name)
            self.layer_api_class = module.LayerAPI if not is_core else None
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
        if self.is_core:
            return
        self.layer_api = self.layer_api_class(stack, config, build_dir)

    def get_api(self):
        """Return the layer API implementation object for use by the
        caller.

        """
        return self.layer_api


def __construct_layer__(module_name, is_core=False):
    """Given a module name that could be None or empty, return a Layer
    based on that module name or None if the name was None or empty.

    """
    return Layer(module_name, is_core) if module_name else None


class VTDSStack:
    """The class representation of the full stack of layers:
    application, cluster, platform and provider.

    """
    def __init__(
            self,
            application_name=None,
            cluster_name=None,
            platform_name=None,
            provider_name=None,
            core_name=None
    ):
        """Constructor. Create a stack using the Python module names
        for the application, cluster, platform and provider layers
        specified in the 'application_name', 'cluster_name',
        'platform_name' and 'provider_name' arguments respectively.

        """
        core_name = "vtds_core" if not core_name else core_name
        self.application = __construct_layer__(application_name)
        self.cluster = __construct_layer__(cluster_name)
        self.platform = __construct_layer__(platform_name)
        self.provider = __construct_layer__(provider_name)
        self.core = __construct_layer__(core_name, is_core=True)
        self.config = None

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
        layer_build_dir = path_join(build_dir, name)
        try:
            makedirs(layer_build_dir, 0o700, True)
        except OSError as err:
            raise ContextualError(
                "failed to create build directory for layer "
                "'%s' ['%s'] - %s" % (name, layer_build_dir, str(err))
            ) from err
        layer.initialize(self, config, layer_build_dir)

    def __active_apis__(self, api_list=None):
        """Get the list of active APIs in the stack. If 'api_list' is
        provided, then get the APIs in the order specified. Otherwise,
        get them in the following order: 'provider', 'platform',
        'cluster', 'application'.

        """
        api_list = (
            [
                self.provider.get_api() if self.provider else None,
                self.platform.get_api() if self.platform else None,
                self.cluster.get_api() if self.cluster else None,
                self.application.get_api() if self.application else None,
            ] if api_list is None else api_list
        )
        return [api for api in api_list if api is not None]

    def __active_configs__(self, config_list=None):
        """Get the list of active base configs in the stack. If
        'config_list' is provided, then get the configs in the order
        specified. Otherwise, get them in the following order:
        'provider', 'platform', 'cluster', 'application'.

        """
        config_list = (
            [
                self.provider.base_config if self.provider else None,
                self.platform.base_config if self.platform else None,
                self.cluster.base_config if self.cluster else None,
                self.application.base_config if self.application else None,
                self.core.base_config if self.core else None,
            ] if config_list is None else config_list
        )
        return [config for config in config_list if config is not None]

    def initialize(self, config, build_dir):
        """Initialize all of the layers rooted at 'build_dir' and
        supplying the full vTDS configuration found in 'config'. Each
        layer will have a sub-directory created for it in the build
        directory tree.

        """
        self.__init_layer__("core", self.core, config, build_dir)
        self.__init_layer__("application", self.application, config, build_dir)
        self.__init_layer__("cluster", self.cluster, config, build_dir)
        self.__init_layer__("platform", self.platform, config, build_dir)
        self.__init_layer__("provider", self.provider, config, build_dir)
        self.config = config

    def consolidate(self):
        """Execute the stack 'consolidate' phase. This runs the
        'consolidate()' method in each of the layers from the bottom
        to the top to set up for any phases that rely on a fully
        resolved configuration.

        """
        for api in self.__active_apis__():
            api.consolidate()

    def prepare(self):
        """Execute the stack 'prepare' phase. This runs the
        'prepare()' method in each of the layers from the bottom to
        the top to set up for the 'validate' and 'deploy' phases.

        """
        for api in self.__active_apis__():
            api.prepare()

    def validate(self):
        """Execute the stack 'validate' phase. This runs the
        'validate()' method in each of the layers from the bottom to
        the top to ensure that the layers are ready for the 'deploy'
        phase.

        """
        for api in self.__active_apis__():
            api.validate()

    def deploy(self):
        """Execute the stack 'deploy' phase. This runs the
        'deploy()' method in each of the layers from the bottom to
        the top.

        """
        for api in self.__active_apis__():
            api.deploy()

    def remove(self):
        """Execute the stack 'remove' phase. This runs the
        'remove()' method in each of the layers from the top to
        the bottom to clean up all resources used by the vTDS.

        """
        # Work from top to bottom instead of bottom to top to avoid
        # pulling a dependency out from under an upper layer.
        api_list = [
                self.application.get_api() if self.application else None,
                self.cluster.get_api() if self.cluster else None,
                self.platform.get_api() if self.platform else None,
                self.provider.get_api() if self.provider else None,
        ]
        for api in self.__active_apis__(api_list):
            api.remove()

    def get_base_config_text(self):
        """Collate the annotated base configurations of all of the
        layers that are present into a single YAML string and return
        it to the caller.

        """
        ret = ""
        configs = self.__active_configs__()
        for config in configs:
            ret += config.get_base_config_text() + '\n'
        return ret

    def get_base_config(self):
        """Collate and merge the base configurations of all of the
        layers that are present into a single base configuration and
        return it to the caller as a configuration collection for use
        in constructing a config to deploy a vTDS.

        """
        ret = {}
        configs = self.__active_configs__()
        for config in configs:
            ret = merge_configs(ret, config.get_base_config())
        return ret

    def get_final_config(self):
        """Return the full configuration after all of the overlays
        have been applied that is given to the layers. This only works
        after initialize() and consolidate() have been run...

        """
        if self.config is None:
            raise ContextualError(
                "can't request stack configuration before calling initialize()"
            )
        return self.config

    def get_test_config(self):
        """Get a base configuration and then apply all of the layer
        test overlays to it to get a test configuration.

        """
        base_config = self.get_base_config()
        configs = self.__active_configs__()
        for config in configs:
            base_config = merge_configs(base_config, config.get_test_overlay())
        return base_config

    def get_application_api(self):
        """Accessor for the application layer API.

        """
        return (
            self.application.get_api() if self.application is not None
            else None
        )

    def get_application_base_config(self):
        """Accessor for the application layer base configuration..

        """
        return (
            self.application.base_config if self.application is not None
            else None
        )

    def get_cluster_api(self):
        """Accessor for the cluster layer API.

        """
        return (
            self.cluster.get_api() if self.cluster is not None
            else None
        )

    def get_cluster_base_config(self):
        """Accessor for the cluster layer base configuration..

        """
        return (
            self.cluster.base_config if self.cluster is not None
            else None
        )

    def get_platform_api(self):
        """Accessor for the platform layer API.

        """
        return (
            self.platform.get_api() if self.platform is not None
            else None
        )

    def get_platform_base_config(self):
        """Accessor for the platform layer base configuration..

        """
        return (
            self.platform.base_config if self.platform is not None
            else None
        )

    def get_provider_api(self):
        """Accessor for the provider layer API.

        """
        return (
            self.provider.get_api() if self.provider is not None
            else None
        )

    def get_provider_base_config(self):
        """Accessor for the provider layer base configuration..

        """
        return (
            self.provider.base_config if self.provider is not None
            else None
        )
