import subprocess
from contextlib import contextmanager


def set_socks_proxy_state(interface, on, sudo=False):
    """Use networksetup to set the SOCKS proxy on or off.

    Parameters
    ----------
    interface : str
        An available networksetup interface
    on : bool
        True to set state 'on', False to set state 'off'
    sudo : bool, optional
        Execute the command with sudo (default: False)
    """
    state = 'on' if on else 'off'
    cmd = ['networksetup', '-setsocksfirewallproxystate', interface, state]
    if sudo:
        cmd = ['sudo'] + cmd
    subprocess.check_call(cmd)


def configure_socks_proxy(interface, host, port, sudo=False):
    """Use networksetup to configure the SOCKS proxy.

    Parameters
    ----------
    interface : str
        An available networksetup interface
    host : str
        The host running the SOCKS proxy
    port : int
        The port to use on the SOCKS host
    sudo : bool, optional
        Execute the command with sudo (default: False)
    """
    cmd = ['networksetup', '-setsocksfirewallproxy', interface, host,
           str(port)]
    if sudo:
        cmd = ['sudo'] + cmd
    subprocess.check_call(cmd)


@contextmanager
def socks_proxy(interface, host, port, sudo=False):
    """Use a SOCKS proxy configured with networksetup.

    Parameters
    ----------
    interface : str
        An available networksetup interface
    host : str
        The host running the SOCKS proxy
    port : int
        The port to use on the SOCKS host
    sudo : bool, optional
        Execute the command with sudo (default: False)
    """
    configure_socks_proxy(interface, host, port, sudo)
    try:
        yield
    finally:
        set_socks_proxy_state(interface, False, sudo)
