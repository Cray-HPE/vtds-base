#
# MIT License
#
# (C) Copyright 2025 Hewlett Packard Enterprise Development LP
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
"""Operations on Jinja templated files and trees filled with Jinja
templated files.

"""

from glob import glob
from jinja2 import (
    Template,
    TemplateError
)

from .errors import ContextualError


def render_template_file(path, data, outpath=None):
    """Render the Jinja template found in 'path' using the parameters
        found in the dictionary supplied by 'data. The file supplied
        in 'path' is overwritten with the rendered template and not
        preserved anywhere.

    """
    outpath = path if outpath is None else outpath
    try:
        with open(path, 'r', encoding="UTF-8") as template_file:
            template_data = template_file.read()
            template = Template(template_data)
            rendered = template.render(data)
    except OSError as err:
        raise ContextualError(
            "cannot read Jinja template file %s: %s" % (
                path, str(err)
            )
        ) from err
    except TemplateError as err:
        raise ContextualError(
            "error rendering template file '%s' - %s" %
            (path, str(err))
        ) from err
    try:
        with open(outpath, 'w', encoding="UTF-8") as output_file:
            output_file.write(rendered)
    except OSError as err:
        raise ContextualError(
            "cannot write Jinja output file %s: %s" % (
                path, str(err)
            )
        ) from err


def render_templated_tree(patterns, data, build_dir):
    """Render the all of the files matching a pattern in 'patterns'
    found in the directory 'build_dir' in place as Jinja templates
    using the template data provided in 'data'.

    """
    # For each file name pattern specified, get the list of files
    # found in the build tree matching that pattern and render each
    # one.
    for pattern in patterns:
        paths = glob("%s/**/%s" % (build_dir, pattern), recursive=True)
        for path in paths:
            render_template_file(path, data)


def render_command_string(cmd, jinja_values):
    """Render a command string (not a command list) as a Jinja
    template with substitutions from the supplied jinja_values
    dictionary.

    """
    try:
        template = Template(cmd)
        return template.render(**jinja_values)
    except TemplateError as err:
        raise ContextualError(
            "error using Jinja to render command line '%s' - %s" % (
                cmd,
                str(err)
            )
        ) from err
