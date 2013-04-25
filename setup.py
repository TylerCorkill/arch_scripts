import os

files = [".bashrc",
		 ".bash_profile",
		 ".bash_logout"]
for f in files:
	os.system("rm ~/%s" % f)
	os.system("ln ~/.custom/%s ~/%s" % (f,f))
print "Updated bash files"
os.system("rm -r ~/.custom/aur")
os.system("mkdir ~/.custom/aur")
