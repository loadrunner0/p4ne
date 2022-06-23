#!usr/local/bin/python3

from pysnmp.hlapi import *

comname = 'public'
ip = '10.31.70.107'
port = 161
snmpObject1 = ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)
snmpObject2 = ObjectIdentity('1.3.6.1.2.1.2.2.1.2')

result = getCmd(SnmpEngine(),
                CommunityData(comname, mpModel=0),
                UdpTransportTarget((ip, port)),
                ContextData(), ObjectType(ObjectIdentity(snmpObject1)))

result2 = nextCmd(SnmpEngine(),
                  CommunityData(comname, mpModel=0),
                  UdpTransportTarget((ip, port)),
                  ContextData(), ObjectType(ObjectIdentity(snmpObject2)),
                  lexicographicMode=False)

for i in result:
    for j in i[3]:
        print(j)

for i in result2:
    for j in i[3]:
        print(j)
