from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import shutil

def createNetwork():
    net = Mininet(controller=RemoteController)

    info("*** Adding controller\n")
    ryu_controller = net.addController('c0', controller=RemoteController, ip="172.31.26.197", port=6653)

    info("*** Adding hosts\n")
    h1 = net.addHost('h1', ip='10.0.0.1')
    h2 = net.addHost('h2', ip='10.0.0.2')
    h3 = net.addHost('h3', ip='10.0.0.3')

    info("*** Adding switch\n")
    s1 = net.addSwitch('s1')

    info("*** Creating links\n")
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)

    info("*** Starting network\n")
    net.start()

    # Add this line after net.start()
    copy_executables(net)

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network")
    net.stop()

def copy_executables(net):
    info("*** Copying executables\n")
    h1, h2, h3 = net.get('h1', 'h2', 'h3')
    for h in (h1, h2, h3):
        shutil.copy('/usr/bin/iperf3', h.cmd('mktemp -d'))

if __name__ == '__main__':
    setLogLevel('info')
    createNetwork()