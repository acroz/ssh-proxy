from __future__ import print_function
from six.moves import input

import argparse
from contextlib import contextmanager
import threading
import subprocess
try:
    from subprocess import DEVNULL
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')

from . import networksetup


def signal_on_error(process, event):
    """Wait for a process to exit and signal if it fails.

    Parameters
    ----------
    process : subprocess.Popen
    event : threading.Event
        An event to set() on non-zero return from the process
    """
    retcode = process.wait()
    if retcode:
        event.set()
        raise subprocess.CalledProcessError(retcode, process.args)


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

    ssh_error = threading.Event()
    thread = threading.Thread(target=signal_on_error,
                              args=(process, ssh_error),
                              daemon=True)
    thread.start()

    try:
        yield ssh_error
    finally:
        process.terminate()


def threaded_quit_prompt():
    """Prompt the user to quit in a thread."""
    def prompt():
        while input('  Enter q to end: ').strip().lower() != 'q':
            continue
    thread = threading.Thread(target=prompt, daemon=True)
    thread.start()
    return thread


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

    with ssh_proxy(args.host, args.port) as ssh_error_event:
        with networksetup.socks_proxy(args.interface, 'localhost',
                                      args.port, args.sudo):
            print('Proxy running on port {}'.format(args.port))
            prompt_thread = threaded_quit_prompt()
            while prompt_thread.is_alive() and not ssh_error_event.is_set():
                prompt_thread.join(0.5)
