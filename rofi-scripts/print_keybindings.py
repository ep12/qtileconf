from libqtile.ipc import find_sockfile, Client as IPCClient
from libqtile.command_client import InteractiveCommandClient
from libqtile.command_interface import IPCCommandInterface



if __name__ == '__main__':
    client = InteractiveCommandClient(IPCCommandInterface(IPCClient(find_sockfile())))
    # does not work:
    print(client.display_kb())
    # print(getattr(client, 'display_kb')())
