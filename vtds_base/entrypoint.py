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
"""Entrypoint handling.

"""
import sys
from .errors import (
    ContextualError,
    LoggedContextualError,
    UsageError,
    usage,
    error_msg
)


def entrypoint(usage_msg, main):
    """Generic entrypoint function. This sets up command line
    arguments for the invocation of a 'main' function and takes care
    of handling any vTDS exceptions that are raised to report
    errors. Other exceptions are allowed to pass to the caller for
    handling.

    """
    try:
        main(sys.argv[1:])
    except ContextualError as err:
        error_msg(str(err))
        sys.exit(1)
    except LoggedContextualError as err:
        error_msg(
            "%s\nStandard Output Log: '%s'\nStandard Error Log: '%s'" % (
                str(err),
                err.output,
                err.error
            )
        )
        sys.exit(1)
    except UsageError as err:
        usage(usage_msg, str(err))