MIBZ:
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

INSTALLATION:
=============

Pycopia is a PITA to install - see especially http://code.google.com/p/pycopia/issues/detail?id=6
I unpacked all the MIBS from libsmi into /usr/share/mibs/.
ftp://ftp.ibr.cs.tu-bs.de/pub/local/libsmi/


apt-get install vim subversion lighttpd libreadline-dev libsqlite3-dev libsmi2-dev openssl postgresql postgresql-client libpq-dev snmpd snmp libsmi
pip install pyrex pyro4 pyxml docutils psycopg2 sqlalchemy simplejson pytz pycrypto
svn checkout http://pycopia.googlecode.com/svn/trunk/ pycopia
cd pycopia/utils
pyrexc pycopia.itimer.pyx
cd ..
python setup.py install

pip install flask twisted

TODO: Download all the mibs from http://www.plixer.com/Support/mib-resources.html
TODO: Add all the mibs from http://www.snmp4tpc.com/MIBS.htm
TODO: Make it not segfault when MIBs are missing dependencies on the server.
