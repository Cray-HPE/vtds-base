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

from yaml import (
    YAMLError,
    safe_load
)
from .errors import ContextualError


def merge_configs(base, overlay):
    """Given a base configuration specified in 'base', merge an
    overlay configuration on top of that base configuration to form a
    new configuration that is the merged configuration. Data in the
    overlay override the contents of the base as follows:

    - Key / value pairs that exist in both and have scalar, list or
      class values are completely taken from the overlay (base
      content is discarded).

    - Key / value pairs that exist in both and have dictionaries are
      recursively merged using these rules.

    - Key / value pairs found only in the base are taken from the base

    - Key value pairs found only in the overlay are taken from the
      overlay.

    """
    # If either the base or the overlay is not a dictionary, then the
    # value going into the config at this layer (or the whole config
    # if we are in the zero-th recursion) is simply the overlay.
    if not isinstance(base, dict) or not isinstance(overlay, dict):
        return overlay

    # Both are dictionaries, so we are going to merge them. Make a new
    # dictionary to hold the merged configs at this level.
    new_config = {}

    # Populate the new config with all of the items that are in the
    # base appropriately overlaid.
    for key, value in base.items():
        if isinstance(value, dict):
            if key in overlay:
                # Base has a dictionary and overlay has something,
                # merge the two (if the overlay isn't a dictionary,
                # the check at the beginning kicks in and returns the
                # overlay value).
                new_config[key] = merge_configs(base[key], overlay[key])
                continue
            # Base has a dictionary, but the overlay has nothing, keep
            # the base.
            new_config[key] = value
            continue
        # Not a dictionary, overwrite from the overlay?
        if key in overlay:
            # Yep! Take the overlay value
            new_config[key] = overlay[key]
            continue
        # Nope. Keep the base value
        new_config[key] = value

    # Now, go through the overlay and catch any keys that aren't in
    # the base. If they were in both the base and overlay, we handled
    # then above, so we only care about what is only in the overlay,
    # and we just want to add it as is to the new config.
    for key, value in overlay.items():
        if key not in base:
            new_config[key] = value

    # new_config now contains the merged dictionary, return it.
    return new_config


def expand_inheritance(configs, config_name, ancestry=None, top_config=None):
    """Within a set of configurations contained in 'configs', perform an
    inheritace expansion of the configuration named 'config_name' that produces
    a fully populated configuation taking into account all of the
    ancestor configurations of 'config_name', and return the data structure
    containing the expanded configuration.

    The 'ancestry' and 'top_config' arguments are used internally during
    recursion and should not be set by the external caller.

    """
    # Set up an 'ancestry' array consisting of the config names we
    # have visited in the inheritance chain so we can tell if we hit
    # an inheritance loop.
    if ancestry is None:
        ancestry = []
    ancestry.append(config_name)
    if top_config is None:
        top_config = config_name
    try:
        config = configs[config_name]
    except KeyError as err:
        raise ContextualError(
            "cannot find config sub-tree named '%s' in config list %s" % (
                config_name, str(configs.keys())
            )
        ) from err
    if 'pure_base_class' not in config:
        # Make sure 'config' does not inherit the 'pure_base_class'
        # designation from any of its parent classes.
        config['pure_base_class'] = False
    parent = config.get('parent_class', None)
    if parent is None:
        # If this config does not inherit from anywhere, then we are
        # done, just return the content of the config.
        return config
    if parent in ancestry:
        # We have already seen 'parent' in the inheritiance chain,
        # this is a loop, so raise an exception.
        raise ContextualError(
            "the inheritance chain for '%s' has a circular dependency "
            "on '%s' - %s" % (
                top_config, parent, str(ancestry + [parent])
            )
        )
    parent_config = expand_inheritance(configs, parent, ancestry, top_config)
    # Merge the current config on top of the parent(s) that have
    # already been expanded, then set 'parent_class' to None because
    # this config is now fully expanded and does not need (or want)
    # further expansion due to inheritance.
    config = merge_configs(parent_config, config)
    config['parent_class'] = None
    return config


def read_config(path, description="configuration"):
    """Read in a YAML configuration from a file.

    """
    try:
        with open(path, 'r', encoding='UTF-8') as config_stream:
            return safe_load(config_stream)
    except OSError as err:
        raise ContextualError(
            "cannot open %s '%s' - %s" % (description, path, str(err))
        ) from err
    except YAMLError as err:
        raise ContextualError(
            "error parsing %s "
            "'%s' - %s" % (description, path, str(err))
        ) from err
