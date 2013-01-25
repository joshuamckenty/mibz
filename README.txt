FIRST IDEA:
-----------
Deploy GitLab, backed onto an object store, using CloudBirds and CloudEnvy.


http://dev.cloudbirds.org/

fixed: 		15.185.99.198
floating: 	15.185.109.96

https://github.com/gitlabhq/gitlabhq/blob/stable/doc/install/installation.md
https://github.com/gitlabhq/gitlabhq/blob/stable/doc/install/databases.md
https://github.com/gitlabhq/gitlabhq
http://www.fancybeans.com/blog/2012/08/24/how-to-use-s3-as-a-private-git-repository/


SECOND IDEA:
-------------
Set up a MIBS service (bought mibz.org) that works like PyPy, e.g.:

> mib_install ifName

ifName is provided by IF-MIB
IF-MIB depends on SNMP-MIB
Installing IF-MIB and dependencies...
...done.

Do this using pysnmp, pycopia, and libsnmp.
mymy.py will slurp in all the MIBS in the world (using pycopia) and build an index of dependencies and terms.
mib_install will be a bash script that calls:

http://mibz.org/get-by-term/<someterm>

Which returns json list of urls to fetch mibs from:

{'IF-MIB': 'http://mibz.org/mibs/IF-MIB',
 'SNMP-MIB' : 'http://mibz.org/mibs/SNMP-MIB'}

Then mib_install will wget each of those into /usr/share/mibs (or distro-specific target.)


THIRD IDEA:
-----------
Write a REST-to-SNMP bridge.

http://myserver-to-monitor:162/by-name/MIB/somename
http://myserver-to-monitor:162/by-oid/1.3.4.1.2.1

Register webhooks against the SNMP agent:

http://myserver-to-monitor:162/by-name/IF-MIB/ifHCInOctets/greater-than?57.2
x-callback header: http://monitoring-host.com

Use HTTP auth to pass credentials for SNMP v3 auth.
Use POST or PUT for SNMP Set.
Return SNMP tables in JSON format, matching (roughly) the output of pycopia MIB classes.

WHY IT'S COOL:
==============

The REST agent doesn't have to run on the host that the SNMP agent is running on, necessarily.
So you could run proxy agents to provide REST endpoints for the SNMP data coming off of network hardware.
And instead of polling that (which would require real-world access to your network switch's SNMP interface),
you've essentially proxied it - AND the webhooks model means you don't have to poll, you simply get notifications.


SCRATCH NOTES:

http://pysnmp.sourceforge.net/download.html

DOWNLOADED NET-SNMP from SOURCE and copied all the MIBS from it.
http://sourceforge.net/projects/net-snmp/files/net-snmp/5.7.2/

curl -O ftp://ftp.ibr.cs.tu-bs.de/pub/local/libsmi/libsmi-current.tar.gz
tar -zxvf libsmi-current.tar.gz


http://www.debianadmin.com/linux-snmp-oids-for-cpumemory-and-disk-statistics.html


ALSO SEE:

http://tools.cisco.com/Support/SNMP/do/BrowseMIB.do?local=en&step=2&submitClicked=true&mibName=TUNNEL-MIB#dependencies
http://www.simpleweb.org/ietf/mibs/modules/IETF/txt/SNMPv2-MIB
http://stackoverflow.com/questions/7731411/how-can-i-check-the-data-transfer-on-a-network-interface-in-python


server-1357278006-az-1-region-a-geo-1

sudo -u gitlab -H git config --global user.email "gitlab@cloudbirds.org"

/etc/hosts for the outside hostname


from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.CommunityData('public'),
    cmdgen.UdpTransportTarget(('localhost', 161)),
    # cmdgen.MibVariable('IF-MIB', 'ifTable').loadMibs(),
    ( ( 'IF-MIB', 'ifHCInOctets' ), ),
)

errorIndication, errorStatus, errorIndex, \
                 varBindTable = cmdGen.nextCmd( 
    cmdgen.CommunityData( 'public' ),
    cmdgen.UdpTransportTarget( ( 'localhost', 161 ) ),
    ( ( 'IF-MIB', 'ifHCInOctets' ), ),
    )

print varBindTable

for varBindTableRow in varBindTable:
    for name, val in varBindTableRow:
        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))