#!usr/local/bin/python3

import ipaddress
import random


class IPv4RandomNetwork(ipaddress.IPv4Network):
    def __init__(self, start=0, end=32):
        ipaddress.IPv4Network.__init__(self,
                                       (random.randint(0x0b000000, 0xdf000000),
                                        random.randint(start, end)),
                                       strict=False
                                       )

    # The check can be written in one line, but we will not do this
    def regular(self):
        if self.is_multicast:
            return False
        if self.is_private:
            return False
        if self.is_unspecified:
            return False
        if self.is_reserved:
            return False
        if self.is_loopback:
            return False
        if self.is_link_local:
            return False
        return True

    # To sort by mask first, the mask will be first.
    # The length of the IP address fits in 4 bytes.
    # So that the mask and ip do not intersect - shift the mask by 32 bits.
    def key_value(self):
        return int(self.network_address) + (int(self.netmask) << 32)


def sortfunc(x):
    return x.key_value()


netlist = []

# We create a random subnet, put it in the list.
# The subnet must be regular and unique.
while len(netlist) != 50:
    rndNet = IPv4RandomNetwork(8, 24)
    if rndNet.regular() and rndNet is not netlist:
        netlist.append(rndNet)

for i in sorted(netlist, key=sortfunc):
    print(i)
