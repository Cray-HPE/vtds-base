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
"""Functions for executing commands derived from the subprocess module.

"""
import subprocess

from .errors import ContextualError
from .logs import logfile


def run(cmd, log_files=None, **run_args):
    """Run a command. All of the standard subprocess.run() arguments
    are honored from the caller if they are provided. Returns the
    CompletedProcess object returned from the subprocess.run() call
    which contains, the return code from the command, and any stdout
    or stderr collected from the command.  By default, stdout and
    stderr are collected for logging purposes and the 'check' argument
    is set to 'True' which causes __run() to raise a ContextualError
    if the command fails. To capture 'stdout' and / or 'stderr' in the
    CompletedProcess instead, set either or both to
    'subprocess.PIPE'. To capture a non-zero exit value, set 'check'
    to False.

    The 'log_files' argument contains a tuple of either pathnames to
    files or open file streams for use in capturing output on stdout
    and stderr respectively. If either is None, output on that stream
    is discarded.  The behavior of 'log_files' can be explicitly
    overridden by setting the 'stdout' and 'stderr' keyword arguments
    to run() in the call.

    """
    log_files = (
        log_files
        if log_files is not None else
        ("/dev/null", "/dev/null")
    )
    out_file, err_file = log_files
    with logfile(out_file) as out, logfile(err_file) as err:
        try:
            # We want to set certain default arguments to run() if
            # they aren't overridden by the caller.
            run_actual = {
                'stdout': out,
                'stderr': err,
                'text': True,
                'encoding': 'UTF-8',
            }
            run_actual.update(run_args)
            check = run_actual.pop('check', True)
            completion = subprocess.run(cmd, check=check, **run_actual)
        except subprocess.CalledProcessError as err:
            raise ContextualError(
                "execution of '%s' command failed - %s" % (
                    " ".join(cmd),
                    str(err)
                ),
                out_file if isinstance(out_file, str) else None,
                err_file if isinstance(err_file, str) else None
            ) from err
    return completion
