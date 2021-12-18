from kazoo.client import KazooClient, KazooState

zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()

def my_listener(state):
    if state == KazooState.LOST:
        print("LOST")
    elif state == KazooState.SUSPENDED:
        print("Suspended")
    else:
        print("Connected")

zk.add_listener(my_listener)

# Create a node with data
#zk.create("/TEST", b"a value")
print(zk.get("TEST"))
print(zk.connected)