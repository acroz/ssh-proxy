from __future__ import print_function
from six.moves import input

import argparse
from contextlib import contextmanager
import subprocess
try:
    from subprocess import DEVNULL
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')

from . import networksetup


@contextmanager
def ssh_proxy(host, proxy_port):
    """Start a dynamic forwarding connection over SSH.

    Parameters
    ----------
    host : str
        The host to connect through
    proxy_port : int
        The local port to set up dynamic forwarding on
    """
    cmd = ['ssh', host, '-q', '-N', '-D', str(proxy_port)]
    process = subprocess.Popen(cmd, stdin=DEVNULL)
    try:
        yield
    finally:
        process.terminate()


def main():
    """Run a SOCKS proxy over an SSH dynamic forwarding connection."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('host',
                        help='Host to proxy through')
    parser.add_argument('--port',
                        type=int, default=9999,
                        help='Local port to use for dynamic forwarding')
    parser.add_argument('--interface',
                        default='Wi-Fi',
                        help='Network interface to configure proxy on - run '
                             '"networksetup -listallnetworkservices" for a '
                             'list of valid values')
    parser.add_argument('--sudo',
                        action='store_true',
                        help='Run networksetup without sudo')
    args = parser.parse_args()

    with ssh_proxy(args.host, args.port):
        with networksetup.socks_proxy(args.interface, 'localhost',
                                      args.port, args.sudo):
            print('Proxy running on port {}'.format(args.port))
            while input('  Enter q to end: ').strip().lower() != 'q':
                continue


if __name__ == '__main__':
    main()
