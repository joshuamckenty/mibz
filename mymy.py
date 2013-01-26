# LICENSE HERE
"""
Simple MIBZ daemon, returns lists of needed MIBS.
Also resolves those to URLS of statically served MIB files.
"""

import os
import logging
import sys
import glob
import json
from flask import Flask, request, render_template, g
from twisted.internet import task
from twisted.internet import reactor
from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site

from pycopia.SMI import SMI

PORT = 8000

app = Flask(__name__)

SMI.set_error_level(9)
MIB_DIR = "/usr/share/mibs"
WEBPATH = "http://mibz.org/mibs"
MIBS_DIRS = ['%s/*/*' % MIB_DIR, '%s/*.txt' % MIB_DIR]

mods = []
for DIR in MIBS_DIRS:
	mods.extend( [x for x in glob.glob(DIR)] )

SMI.load_modules(mods)

def pathify(path):
	return path.replace(MIB_DIR, WEBPATH)

def fetch_deps(mod, tree):
	imports = mod.get_imports()
	for imp in imports:
		if not tree.get(imp.module):
			real_mod = SMI.get_module(imp.module)
			tree[imp.module] = pathify(real_mod.path)
			fetch_deps(SMI.get_module(imp.module), tree)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/by-node/<nodename>')
def tree_for_node(nodename='iscsiObjects'):
	tree = {}
	node = SMI.get_node(nodename)
	if node is not None:
		first_mod = node.get_module()
		tree[first_mod.name] = pathify(first_mod.path)
		fetch_deps(first_mod, tree)
	return json.dumps(tree)


resource = WSGIResource(reactor, reactor.getThreadPool(), app)
site = Site(resource)
reactor.listenTCP(PORT, site)
reactor.run()

