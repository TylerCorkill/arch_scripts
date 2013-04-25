import os

files = [".bashrc",
		 ".bash_profile",
		 ".bash_logout"]
for f in files:
	os.system("ln %s ../%s" % f)
