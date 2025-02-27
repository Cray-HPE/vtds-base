#
# MIT License
#
# (C) Copyright [2024] Hewlett Packard Enterprise Development LP
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
from contextlib import contextmanager
from abc import (
    ABCMeta,
    abstractmethod
)


class VirtualNodesBase(metaclass=ABCMeta):
    """A class implementing public access to Virtual Nodes and their
    operations.

    """
    @abstractmethod
    def node_classes(self):
        """Get a list of Virtual Node classes by name.

        """

    @abstractmethod
    def application_metadata(self, node_class):
        """Get the application metadata for a named node class from
        its config.

        """

    @abstractmethod
    def node_count(self, node_class):
        """Get the number of Virtual Node instances of the specified
        class.

        """

    @abstractmethod
    def set_node_node_name(self, node_class, instance, name):
        """When called during the 'prepare' phase by a higher layer,
        this sets the contextual node name (i.e. the node name used on
        the mechanism used to implement the Virtual Node, perhaps a
        Virtual Machine) to be used for a given node instance in a
        given node class to the specified name. This modifies the
        configuration data used during the deploy and remove phases.

        """

    @abstractmethod
    def node_node_name(self, node_class, instance):
        """Get the node name (used for contextually naming the
        implementation of a Virtual Node) of a given Virtual Node
        class instance (i.e. Virtual Node). This will also be the core
        hostname (minus the network name) of the node if there is no
        host naming specified in the configuration.

        """

    @abstractmethod
    def network_names(self, node_class):
        """Return the list of Network Names of the Networks connected
        to the specified class of Virtual Node.

        """

    @abstractmethod
    def set_node_hostname(self, node_class, instance, name):
        """When called during the 'prepare' phase by a higher layer,
        this sets the network hostname to be used for a given node
        instance in a given node class to the specified name. This
        modifies the configuration data used during the deploy and
        remove phases.

        """

    @abstractmethod
    def node_hostname(self, node_class, instance, network_name=None):
        """Get the hostname of a given Virtual Node class instance
        (i.e. Virtual Node). Optionally, look up the hostname by
        network name for local names on a given Virtual Network.

        """

    def node_host_blade_info(self, node_class):
        """Get the host Virtual Blade class information from a a given
        Virtual Node class instance (i.e. Virtual Node). This returns
        a dictionary with the following elements:

        - blade_class: the name of the Virtual Blade class to which
          the blade belongs.

        - instance_capacity: the maximum number of host instances that
          will be created per blade.

        """

    @abstractmethod
    def node_ipv4_addr(self, node_class, instance, network_name):
        """Get the configured IPv4 address (if any) for the specified
        instance of the specified node class on the specified
        network. If IP addresses are not configured for the specified
        node class (i.e. they are dynamic DHCP addresses) this will
        return None. If the specified node class is not present on the
        specified network this will raise a ContextualError exception.

        """

    @abstractmethod
    def node_class_addressing(self, node_class, network_name):
        """Obtain an Addressing object describing the addressing of
        the specified node class within the named network. If the node
        class has no addressing in (i.e. is not connected to) the
        specified network, return None.

        """

    @abstractmethod
    def node_ssh_key_secret(self, node_class):
        """Return the name of the secret containing the SSH key pair
        used to to authenticate with Virtual Node of the specified
        node class.

        """

    @abstractmethod
    def node_ssh_key_paths(self, node_class):
        """Return a tuple of paths to files containing the public and
        private SSH keys used to to authenticate with Virtual Nodes of
        the specified node class. The tuple is in the form
        '(public_path, private_path)' The value of 'private_path' is
        suitable for use with the '-i' option of 'ssh'. Before
        returning this call will verify that both files can be opened
        for reading and will fail with a ContextualError if either
        cannot.

        """

    @abstractmethod
    @contextmanager
    def connect_node(self, node_class, instance, remote_port):
        """Establish an external connection to the specified remote
        port on the specified instance of the named Virtual Node
        class. Return a context manager (suitable for use in a 'with'
        clause) yielding an NodeConnection object for the
        connection. Upon leaving the 'with' context, the connection in
        the NodeConnection is closed.

        """

    @contextmanager
    @abstractmethod
    def connect_nodes(self, remote_port, node_classes=None):
        """Establish external connections to the specified remote port
        on all the Virtual Node instances on all the Virtual Node
        classes listed by name in 'node_classes'. If 'node_classes' is not
        provided or None, all available node classes are used. Return a
        context manager (suitable for use in a 'with' clause) yielding
        a NodeConnectionSet object representing the connections. Upon
        leaving the 'with' context, all the connections in the
        NodeConnectionSet object are closed.

        """

    @abstractmethod
    @contextmanager
    def ssh_connect_node(self, node_class, instance, remote_port=22):
        """Establish an external connection to the SSH server
        port on the specified instance of the named Virtual Node
        class. Return a context manager (suitable for use in a 'with'
        clause) yielding a NodeSSHConnection object for the
        connection. Upon leaving the 'with' context, the connection in
        the NodeSSHConnection is closed.

        """

    @contextmanager
    @abstractmethod
    def ssh_connect_nodes(self, node_classes=None, remote_port=22):
        """Establish external connections to the specified remote port
        on all the Virtual Node instances on all the Virtual Node
        classes listed by name in 'node_classes'. If 'node_classes' is not
        provided or None, all available node classes are used. Return a
        context manager (suitable for use in a 'with' clause) yielding
        a NodeSSHConnectionSet object representing the connections. Upon
        leaving the 'with' context, all the connections in the
        NodeSSHConnectionSet are closed.

        """


class VirtualNetworksBase(metaclass=ABCMeta):
    """The external representation of the set of Virtual Networks
    and public operations that can be performed on the list..

    """
    @abstractmethod
    def network_names(self):
        """Get a list of network names

        """

    @abstractmethod
    def application_metadata(self, network_name):
        """Get the application metadata for a named virtual network
        from its config.

        """

    @abstractmethod
    def ipv4_cidr(self, network_name):
        """Return the (string) IPv4 CIDR (<IP>/<length>) for the
        named network.

        """

    @abstractmethod
    def non_cluster_network(self, network_name):
        """A network in the cluster configuration may be a network
        used by vTDS for constructing the cluster but not intended for
        use by applications running on the cluster. Such a network is
        a 'non-cluster network'.  Return True if the specified network
        name refers to a non-cluster network otherwise return False.

        """

    @abstractmethod
    def blade_class_addressing(self, blade_class, network_name):
        """Obtain an Addressing object describing the addressing of
        the specified connected blade class within the named
        network. If the blade class has no addressing in (i.e. is not
        connected to) the specified network, return None.

        """


class NodeConnectionBase(metaclass=ABCMeta):
    """A class containing the relevant information needed to use
    external connections to ports on a specific Virtual Node.

    """
    @abstractmethod
    def node_class(self):
        """Return the name of the Virtual Node class of the connected
        Virtual Node.

        """

    @abstractmethod
    def node_hostname(self, network_name=None):
        """Return the hostname of the connected Virtual Node. If
        network_name is specified and not none, return the local
        hostname on the specified Virtual Network.

        """

    @abstractmethod
    def local_ip(self):
        """Return the locally reachable IP address of the connection
        to the Virtual Node.

        """

    @abstractmethod
    def local_port(self):
        """Return the TCP port number on the locally reachable IP
        address of the connection to the Virtual Node.

        """

    @abstractmethod
    def remote_port(self):
        """Return the TCP port number on the on the Virtual Node to
        which the NodeConnection connects.

        """


class NodeConnectionSetBase(metaclass=ABCMeta):
    """A class that contains multiple active NodeConnections to
    facilitate operations on multiple simultaneous nodes. This class
    is just a wrapper for a list of NodeConnections and should be
    obtained using the VirtualNodes.connect_nodes() method not
    directly.

    """
    @abstractmethod
    def list_connections(self, node_class=None):
        """List the connections in the NodeConnectionSet filtered by
        'node_class' if that is present. Otherwise simply list all of
        the connections.

        """

    @abstractmethod
    def get_connection(self, hostname):
        """Return the connection corresponding to the specified
        VirtualNode hostname ('hostname') or None if the hostname is
        not found.

        """


class NodeSSHConnectionBase(NodeConnectionBase, metaclass=ABCMeta):
    """Specifically a connection to the SSH server on a node (remote
    port 22 unless otherwise specified) with methods to copy files to
    and from the node using SCP and to run commands on the node
    using SSH.

    """
    @abstractmethod
    def copy_to(
        self, source, destination,
        recurse=False, blocking=True, logname=None, **kwargs
    ):
        """Copy a file from a path on the local machine ('source') to
        a path on the Virtual Node ('dest'). The SCP operation is run
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
        """Copy a file from a path on the node ('source') to a path
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
        node. The string 'cmd' can be templated using Jinja
        templating to use any of the attributes of the underlying
        connection:

        - the node class: 'node_class'
        - the node hostname: 'node_hostname'
        - the connection port on the node: 'remote_port'
        - the local connection IP address: 'local_ip'
        - the local connection port: 'local_port'

        The resulting command will be executed by the shell on the
        node under an SSH session by creating a subprocess.Popen()
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


class NodeSSHConnectionSetBase(NodeConnectionSetBase, metaclass=ABCMeta):
    """A class to wrap multiple NodeSSHConnections and provide
    operations that run in parallel across multiple connections.

    """
    @abstractmethod
    def copy_to(
        self, source, destination, recurse=False, logname=None, node_class=None
    ):
        """Copy the file at a path on the local machine ('source') to
        a path ('dest') on all of the selected nodes (based on
        'node_class'). If 'node_class is not specified or None, copy
        the file to all connected nodes. Wait until all copies
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
    def run_command(self, cmd, logname=None, node_class=None):
        """Using SSH, run the command in the string 'cmd'
        asynchronously on all connected nodes filtered by
        'node_class'. If 'node_class' is unspecified or None, run on
        all connected nodes. The string 'cmd' can be templated using
        Jinja templating to use any of the attributes of the
        underlying connection. In this case, the connection in which
        the command is being run will be used for the templating, so,
        for example, 'node_hostname' will match the node on which
        the command runs:

        - the node class: 'node_class'
        - the node instance within its class: 'instance'
        - the node hostname: 'node_hostname'
        - the connection port on the node: 'remote_port'
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


class AddressingBase(metaclass=ABCMeta):
    """Addressing information for node and blade classes. This
    contains all addressing by address family for instances of node
    class or blade classes as assigned at the cluster level.

    """
    @abstractmethod
    def address(self, family, instance):
        """Retrieve the address within the address family specified by
        the string 'family' (AF_INET, AF_INET6, AF_PACKET, or
        whatever) of a specified instance number (integer) of the
        object class (node class or blade class) and network from
        which this Addressing object was obtained. The form of the
        address will be a string formatted in the canonical way for
        the specified address family.

        """

    @abstractmethod
    def addresses(self, family):
        """Retrieve a dictionary of instance number (integer) to
        address (string) mapping pairs within the address family
        specified by the string 'family' (AF_INET, AF_INET6,
        AF_PACKET, or whatever) of the object class (node class or
        blade class) and network from which this Addressing object was
        obtained.

        """

    @abstractmethod
    def address_families(self):
        """Retrieve a list of address family names ('AF_INET',
        'AF_INET6', 'AF_PACKET', or whatever) supported by the object
        class (node class or blade class) and network from which this
        Addressing object was obtained.

        """

    @abstractmethod
    def instances(self):
        """Retrieve a list of instance numbers within the object class
        (node class or blade class) and network from which this
        addressing object was created. Only instances that are
        connected to the network are reported.

        """
