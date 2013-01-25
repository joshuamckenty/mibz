import os
import sys
import glob
from pycopia.SMI import SMI

SMI.set_error_level(9)
MIBS_DIRS = ['/usr/share/mibs/*/*', '/usr/share/mibs/*.txt']

mods = []
for DIR in MIBS_DIRS:
	mods.extend( [x for x in glob.glob(DIR)] )

SMI.load_modules(mods)

for mod in SMI.get_modules():
	print mod

tree = {}

node = SMI.get_node('iscsiObjects')
if node is None:
	sys.exit(1)

first_mod = node.get_module()
tree[first_mod.name] = first_mod.path

def fetch_deps(mod, tree):
	imports = mod.get_imports()
	for imp in imports:
		if not tree.get(imp.module):
			real_mod = SMI.get_module(imp.module)
			tree[imp.module] = real_mod.path
			fetch_deps(SMI.get_module(imp.module), tree)

fetch_deps(first_mod, tree)
print tree