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
"""Operations on Jinja templated files and trees filled with Jinja
templated files.

"""

from glob import glob
from jinja2 import Template

from .errors import ContextualError


def render_template_file(path, data):
    """Render the Jinja template found in 'path' using the parameters
        found in the dictionary supplied by 'data. The file supplied
        in 'path' is overwritten with the rendered template and not
        preserved anywhere.

    """
    try:
        with open(path, 'r', encoding="UTF-8") as template_file:
            template_data = template_file.read()
    except OSError as err:
        raise ContextualError(
            "cannot read Jinja template file %s: %s" % (
                path, str(err)
            )
        ) from err
    template = Template(template_data)
    rendered = template.render(data)
    try:
        with open(path, 'w', encoding="UTF-8") as output_file:
            output_file.write(rendered)
    except OSError as err:
        raise ContextualError(
            "cannot write Jinja template file %s: %s" % (
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
        paths = glob("%s/**/%s" % (build_dir, pattern))
        for path in paths:
            render_template_file(path, data)
