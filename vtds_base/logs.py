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
"""Logfile related tools

"""
from os.path import join as path_join
from os import (
    makedirs,
    devnull
)
from io import IOBase
from contextlib import contextmanager
from .errors import ContextualError


@contextmanager
def logfile(lfile, mode='w', encoding='UTF-8',  **kwargs):
    """Open a logfile and yield the resulting stream if 'lfile' is not
       None and is a string. If 'lfile' is None, yield a writable NULL
       stream (devnull). If 'lfile' is a stream (IOBase derived),
       yield 'lfile' itself and make sure not to close it on context
       exit.

    """
    stream = None
    try:
        if lfile is None:
            lfile = devnull
        if isinstance(lfile, str):
            stream = open(
                lfile, mode, encoding=encoding, **kwargs
            ) if lfile is not None else None
        elif isinstance(lfile, IOBase):
            stream = lfile
        else:
            raise ContextualError(
                "error opening a log file, expected the specified "
                "file to be a string, a stream or None, "
                "not '%s'" % str(type(lfile))
            )
    except OSError as err:
        raise ContextualError(
            "error opening log file '%s' - %s" % (lfile, str(err))
        ) from err
    try:
        yield stream
    finally:
        if isinstance(lfile, str) and stream is not None:
            stream.close()


def log_paths(build_dir, logname):
    """Compose an 'out' path and an 'error' path based on the base
    name 'logname' and return both to the caller.

    """
    logs = path_join(build_dir, "logs")
    try:
        makedirs(logs, mode=0o755, exist_ok=True)
    except OSError as err:
        raise ContextualError(
            "failed to create log directory '%s' - %s" % (
                logs, str(err)
            )
        ) from err
    out_path = path_join(
        logs,
        "%s-out.txt" % (logname)
    )
    err_path = path_join(
        logs,
        "%s-err.txt" % (logname)
    )
    return (out_path, err_path)
