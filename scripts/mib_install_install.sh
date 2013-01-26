#!/bin/bash

curl http://mibz.org/scripts/mib_install -o /usr/local/bin/mib_install
# TODO: Consider patching shebang if required
chmod a+x /usr/local/bin/mib_install