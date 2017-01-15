SSH Proxy
=========

A simple tool for temporarily configuring a SOCKS proxy over an SSH dynamic
forwarding connection.

Installation
------------

To install:

.. code-block:: bash

    $ pip install ssh-proxy

Usage
-----

Run the SSH proxy with:

.. code-block:: bash

    $ sshproxy hostname

where the hostname is a valid hostname provided to the SSH command line, e.g.
``user@domain.com``, ``100.10.100.10``. If you need to configure SSH keys etc.,
it is recommended to do so using your ``~/.ssh/config`` file, e.g.::

    Host myhost
        HostName myhost.com
        User myuser
        IdentityFile ~/.ssh/myhost

``networksetup`` requires enhanced permissions to run. To avoid entering your
password in a dialog several times, run with ``--sudo`` to run ``networksetup``
as root:

.. code-block:: bash

    $ sshproxy myhost --sudo

For other command line options, run:

.. code-block:: bash

    $ sshproxy --help

Contribute
----------

The source is hosted in GitHub at https://github.com/acroz/ssh-proxy.git. At
present the code assumes that no password needs to be entered and that the user
is on a Mac and therefore has ``networksetup`` available. Improvements,
including ridding the code of these assumptions, are welcome via pull request.
