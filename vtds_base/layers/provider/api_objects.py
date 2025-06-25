#
# MIT License
#
# (C) Copyright 2024-2025 Hewlett Packard Enterprise Development LP
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
"""Objects presented on the Layer API containing public information
and operations in the provider layer.

"""
from abc import (
    ABCMeta,
    abstractmethod
)


class SiteConfigBase(metaclass=ABCMeta):
    """A class implementing public access to site configuration
    settings.

    """

    @abstractmethod
    def system_name(self):
        """Get the system name used to create the cluster on the
        provider. Returns a string representing the system name.

        """

    @abstractmethod
    def site_ntp_servers(self, address_family='AF_INET'):
        """Get the hostname / address of the NTP server offered by the
        provider or site in the specified address family. The
        'address_family' parameter is a string specifies the address
        family of the address to be returned, with a default value of
        'AF_INET'. Returns a list of dictionaries containing the
        following fields:

        - 'address_family' - the requested address family as passed in
        - 'hostname' - the host name of the NTP server if known, None if not
        - 'address' - the address within the address family of the NTP
          server if known, None if not

        Returns an empty list if the specified 'address_family' is not
        supported by the provider or not configured in the Provider
        configuration.

        """

    @abstractmethod
    def site_dns_servers(self, address_family='AF_INET'):
        """Get the address of the DNS server offered by the provider
        or site on the specified address family. The address_family'
        parameter is a string specifies the address family of the
        address to be returned, with a default value of
        'AF_INET'. Returns a list of dictionarie containing the
        following fields:

        - 'address_family' - the requested address family as passed in
        - 'address' - the address within the address family of the NTP
          server if known, None if not

        Returns an empty list if the specified 'address_family' is not
        supported by the provider or not configured in the Provider
        configuration.

        """


class VirtualBladesBase(metaclass=ABCMeta):
    """A class implementing public access to Virtual Blades and their
    operations.

    """
    @abstractmethod
    def blade_classes(self):
        """Get a list of virtual blade classes by name.

        """

    @abstractmethod
    def application_metadata(self, blade_class):
        """Get the application metadata for a named blade class from
        its config.

        """

    @abstractmethod
    def blade_count(self, blade_class):
        """Get the number of Virtual Blade instances of the specified
        class.

        """

    @abstractmethod
    def blade_interconnects(self, blade_class):
        """Return the list of Blade Interconnects by name connected to
        the specified class of Virtual Blade.

        """

    @abstractmethod
    def blade_hostname(self, blade_class, instance):
        """Get the hostname of a given instance of the specified class
        of Virtual Blade.

        """

    @abstractmethod
    def blade_ip(self, blade_class, instance, interconnect):
        """Return the IP address (string) on the named Blade
        Interconnect of a specified instance of the named Virtual
        Blade class.

        """

    @abstractmethod
    def blade_ssh_key_secret(self, blade_class):
        """Return the name of the secret containing the SSH key pair
        used to to authenticate with blades of the specified blade
        class.

        """

    @abstractmethod
    def blade_ssh_key_paths(self, blade_class):
        """Return a tuple of paths to files containing the public and
        private SSH keys used to to authenticate with blades of the
        specified blade class. The tuple is in the form '(public_path,
        private_path)' The value of 'private_path' is suitable for use
        with the '-i' option of 'ssh'. Before returning this call will
        verify that both files can be opened for reading and will fail
        with a ContextualError if either cannot.

        """

    @abstractmethod
    def connect_blade(self, blade_class, instance, remote_port):
        """Establish an external connection to the specified remote
        port on the specified instance of the named Virtual Blade
        class. Return a BladeConnection object for the connection.

        BladeConnections are context managed, so if this is used
        in a 'with' clause, upon leaving the 'with' context, the
        connection in the BladeConnection is automatically closed.

        To close the connection outside of a 'with' clause call
        the __exit__() method on the BladeConnection.

        """

    @abstractmethod
    def connect_blades(self, remote_port, blade_classes=None):
        """Establish external connections to the specified remote port
        on all the Virtual Blade instances on all the Virtual Blade
        classes listed by name in 'blade_classes'. If 'blade_classes' is not
        provided or None, all available blade classes are used. Return a
        BladeConnectionSet object representing the connections.

        BladeConnectionSets are context managed, so if this is used
        in a 'with' clause, upon leaving the 'with' context, the
        connections in the BladeConnectionSet are automatically closed.

        To close the connections outside of a 'with' clause call
        the __exit__() method on the BladeConnectionSet.

        """

    @abstractmethod
    def ssh_connect_blade(self, blade_class, instance, remote_port):
        """Establish an external connection to the SSH server
        port on the specified instance of the named Virtual Blade
        class. Return a BladeSSHConnection object for the
        connection.

        BladeSSHConnection are context managed, so if this is used
        in a 'with' clause, upon leaving the 'with' context, the
        connection in the BladeSSHConnection is automatically closed.

        To close the connection outside of a 'with' clause call
        the __exit__() method on the BladeSSHConnection.

        """

    @abstractmethod
    def ssh_connect_blades(self, blade_classes=None, remote_port=22):
        """Establish external connections to the specified remote port
        on all the Virtual Blade instances on all the Virtual Blade
        classes listed by name in 'blade_classes'. If 'blade_classes' is not
        provided or None, all available blade classes are used. Return a
        BladeSSHConnectionSet object representing the
        connections.

        BladeSSHConnectionSets are context managed, so if this is used
        in a 'with' clause, upon leaving the 'with' context, the
        connections in the BladeSSHConnectionSet are automatically closed.

        To close the connections outside of a 'with' clause call
        the __exit__() method on the BladeSSHConnectionSet.

        """


class BladeInterconnectsBase(metaclass=ABCMeta):
    """The external representation of the set of Blade Interconnects
    and public operations that can be performed on the interconnects.

    """
    @abstractmethod
    def interconnect_names(self):
        """Get a list of blade interconnects by name

        """

    @abstractmethod
    def application_metadata(self, interconnect_name):
        """Get the application metadata for a named interconnect from
        its config.

        """

    @abstractmethod
    def ipv4_cidr(self, interconnect_name):
        """Return the (string) IPv4 CIDR (<IP>/<length>) for the
        network on the named interconnect.

        """


class BladeConnectionBase(metaclass=ABCMeta):
    """A class containing the relevant information needed to use
    external connections to ports on a specific Virtual Blade.

    """
    @abstractmethod
    def blade_class(self):
        """Return the name of the Virtual Blade class of the connected
        Virtual Blade.

        """

    @abstractmethod
    def blade_hostname(self):
        """Return the hostname of the connected Virtual Blade.

        """

    @abstractmethod
    def local_ip(self):
        """Return the locally reachable IP address of the connection
        to the Virtual Blade.

        """

    @abstractmethod
    def local_port(self):
        """Return the TCP port number on the locally reachable IP
        address of the connection to the Virtual Blade.

        """

    @abstractmethod
    def remote_port(self):
        """Return the TCP port number on the on the Virtual blade to
        which the BladeConnection connects.

        """

    @abstractmethod
    def __enter__(self):
        """Context entry handler to make BladeConnection objects
        usable with the 'with ... as' construct. This returns the
        BladeConnection for use in a context.

        """

    @abstractmethod
    def __exit__(
            self,
            exception_type=None,
            exception_value=None,
            traceback=None
    ):
        """Context exit handler to make BladeConnection
        objects usable with the 'with ... as' construct. This cleans
        up all resources associated with the BladeConnection on
        exit from the 'with' block context. Not called if the object
        is used outside a 'with' context.

        """


class BladeConnectionSetBase(metaclass=ABCMeta):
    """A class that contains multiple active BladeConnections to
    facilitate operations on multiple simultaneous blades. This class
    is just a wrapper for a list of BladeContainers and should be
    obtained using the VirtualBlades.connect_blades() method not
    directly.

    """
    @abstractmethod
    def list_connections(self, blade_class=None):
        """List the connections in the BladeConnectionSet filtered by
        'blade_class' if that is present. Otherwise imply list all of
        the connections.

        """

    @abstractmethod
    def get_connection(self, hostname):
        """Return the connection corresponding to the specified
        VirtualBlade hostname ('hostname') or None if the hostname is
        not found.

        """

    @abstractmethod
    def __enter__(self):
        """Context entry handler to make BladeConnectionSet objects
        usable with the 'with ... as' construct. This returns the
        BladeConnectionSet for use in a context.

        """

    @abstractmethod
    def __exit__(
            self,
            exception_type=None,
            exception_value=None,
            traceback=None
    ):
        """Context exit handler to make BladeConnectionSet
        objects usable with the 'with ... as' construct. This cleans
        up all resources associated with the BladeConnectionSet on
        exit from the 'with' block context. Not called if the object
        is used outside a 'with' context.

        """


class BladeSSHConnectionBase(BladeConnectionBase, metaclass=ABCMeta):
    """Specifically a connection to the SSH server on a blade (remote
    port 22 unless otherwise specified) with methods to copy files to
    and from the blade using SCP and to run commands on the blade
    using SSH.

    """
    @abstractmethod
    def copy_to(
        self, source, destination,
        recurse=False, blocking=True, logname=None, **kwargs
    ):
        """Copy a file from a path on the local machine ('source') to
        a path on the virtual blade ('dest'). The SCP operation is run
        under a subprocess.Popen() object, which is returned at the
        end of the call. If additional keyword arguments are supplied,
        they may be used to override defaults set up by this function
        and passed to subprocess.Popen() or simply passed on to
        subprocess.Popen() as keyword arguments.

        If the 'recurse' argument is 'True' and the source is a
        directory, the directory and all of its descendents will be
        copied. Otherwise, the source should be a file and it alone
        will be copied.

        If the 'blocking' option is True (default), copy_to() will block
        waiting for the copy to complete (or fail) and raise a
        ContextualError exception if it fails. If the 'blocking' option
        is False, copy_to() will return immediately once the Popen()
        object is created and let the caller manage the sub-process.

        If the 'logname' argument is provided and not None, use the
        string found there to compose a pair of log files to capture
        standard output and standard error. Otherwise a generic log
        name is created.

        """

    @abstractmethod
    def copy_from(
        self, source, destination,
        recurse=False, blocking=True, logname=None, **kwargs
    ):
        """Copy a file from a path on the blade ('source') to a path
        on the local machine ('dest'). The SCP operation is run under
        a subprocess.Popen() object, which is returned at the end of
        the call. If additional keyword arguments are supplied, they
        may be used to override defaults set up by this function and
        passed to subprocess.Popen() or simply passed on to
        subprocess.Popen() as keyword arguments.

        If the 'recurse' argument is 'True' and the source is a
        directory, the directory and all of its descendents will be
        copied. Otherwise, the source should be a file and it alone
        will be copied.

        If the 'blocking' option is True (default), copy_from() will
        block waiting for the copy to complete (or fail) and raise a
        ContextualError exception if it fails. If the 'blocking' option
        is False, copy_from() will return immediately once the Popen()
        object is created and let the caller manage the sub-process.

        If the 'logname' argument is provided and not None, use the
        string found there to compose a pair of log files to capture
        standard output and standard error. Otherwise a generic log
        name is created.

        """

    @abstractmethod
    def run_command(self, cmd, blocking=True, logfiles=None, **kwargs):
        """Using SSH, run the command in the string 'cmd' on the
        blade. The string 'cmd' can be templated using Jinja
        templating to use any of the attributes of the underlying
        connection:

        - the blade class: 'blade_class'
        - the blade class instance: 'instance'
        - the blade hostname: 'blade_hostname'
        - the connection port on the blade: 'remote_port'
        - the local connection IP address: 'local_ip'
        - the local connection port: 'local_port'

        The resulting command will be executed by the shell on the
        blade under an SSH session by creating a subprocess.Popen()
        object. If additional keyword arguments are supplied, they may
        be used to override defaults set up by this function and
        passed to subprocess.Popen() or simply passed on to
        subprocess.Popen() as keyword arguments.

        If the 'logfiles' argument is provided, it contains a two
        element tuple telling run_command where to put standard output
        and standard error logging for the command respectively.
        Normally, these are specified as pathnames to log
        files. Either or both can also be a file object or None. If a
        file object is used, the output is written to the file. If
        None is used, the corresponding output is not redirected and
        the default Popen() behavior is used.

        If the 'blocking' option is False (default), run_command() will
        block waiting for the command to complete (or fail) and raise
        a ContextualError exception if it fails. If the 'blocking' option
        is False, run_command() will return immediately once the
        Popen() object is created and let the caller manage the
        sub-process.

        """

    @abstractmethod
    def __enter__(self):
        """Context entry handler to make BladeSSHConnection objects
        usable with the 'with ... as' construct. This returns the
        BladeSSHConnection for use in a context.

        """

    @abstractmethod
    def __exit__(
            self,
            exception_type=None,
            exception_value=None,
            traceback=None
    ):
        """Context exit handler to make BladeSSHConnection objects
        usable with the 'with ... as' construct. This cleans up all
        resources associated with the BladeSSHConnection on exit from
        the 'with' block context. Not called if the object is used
        outside a 'with' context.

        """


class BladeSSHConnectionSetBase(BladeConnectionSetBase, metaclass=ABCMeta):
    """A class to wrap multiple BladeSSHConnections and provide
    operations that run in parallel across multiple connections.

    """
    @abstractmethod
    def copy_to(
        self, source, destination,
        recurse=False, logname=None, blade_class=None
    ):
        """Copy the file at a path on the local machine ('source') to
        a path ('dest') on all of the selected blades (based on
        'blade_class'). If 'blade_class is not specified or None, copy
        the file to all connected blades. Wait until all copies
        complete or fail. If any of the copies fail, collect the
        errors they produce to raise a ContextualError exception
        describing the failures.

        If the 'recurse' option is True and the local file is a
        directory, the directory and all of its descendants will be
        copied.

        If the 'logname' argument is provided, use the string found
        there to compose paths to two files, one that will contain the
        standard output from the command and one that will contain the
        standard input. The paths to these files will be included in
        any error reporting from the operation.

        """

    @abstractmethod
    def run_command(self, cmd, logname=None, blade_class=None):
        """Using SSH, run the command in the string 'cmd'
        asynchronously on all connected blades filtered by
        'blade_class'. If 'blade_class' is unspecified or None, run on
        all connected blades. The string 'cmd' can be templated using
        Jinja templating to use any of the attributes of the
        underlying connection. In this case, the connection in which
        the command is being run will be used for the templating, so,
        for example, 'blade_hostname' will match the blade on which
        the command runs:

        - the blade class: 'blade_class'
        - the blade instance within its class: 'instance'
        - the blade hostname: 'blade_hostname'
        - the connection port on the blade: 'remote_port'
        - the local connection IP address: 'local_ip'
        - the local connection port: 'local_port'

        Wait until all commands complete or fail. If any of the
        commands fail, collect the errors they produce to raise a
        ContextualError exception describing the failures.

        If the 'logname' argument is provided, use the string found
        there to compose paths to two files, one that will contain the
        standard output from the command and one that will contain the
        standard input. The paths to these files will be included in
        any error reporting from the operation.

        """

    @abstractmethod
    def __enter__(self):
        """Context entry handler to make BladeSSHConnectionSet objects
        usable with the 'with ... as' construct. This returns the
        BladeSSHConnectionSet for use in a context.

        """

    @abstractmethod
    def __exit__(
            self,
            exception_type=None,
            exception_value=None,
            traceback=None
    ):
        """Context exit handler to make BladeSSHConnectionSet objects
        usable with the 'with ... as' construct. This cleans up all
        resources associated with the BladeSSHConnectionSet on exit
        from the 'with' block context. Not called if the object is
        used outside a 'with' context.

        """


class SecretsBase(metaclass=ABCMeta):
    """Provider Layers Secrets API object. Provides ways to populate
    and retrieve secrets through the Provider layer. Secrets are
    created by the provider layer by declaring them in the Provider
    configuration for your vTDS system, and should be known by their
    names as filled out in various places and verious layers in your
    vTDS system. For example the SSH key pair used to talk to a
    particular set of Virtual Blades through a blade connection is
    stored in a secret configured in the Provider layer and the name
    of that secret can be obtained from a VirtualBlades API object
    using the blade_ssh_key_secret() method.

    """
    @abstractmethod
    def store(self, name, value):
        """Store a value (string) in the named secret.

        """

    @abstractmethod
    def read(self, name):
        """Read the value (string) stored in a named secret. If no
        value is present, return None.

        """

    @abstractmethod
    def application_metadata(self, name):
        """Get the application metadata for a named secret from its
        config.

        """
