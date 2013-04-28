from urllib import urlopen
import sys
import os
import re
from subprocess import Popen, PIPE

baseURL = "https://aur.archlinux.org/packages"
args = len(sys.argv)

def scan(package):
	url = "%s/%s/" % (baseURL, package)
	urlLines = []
	for line in urlopen(url).readlines():
		urlLines.append(line.strip())
	if len(urlLines) < 92:
		print "'%s' doesn't exist" % package
	else:
		return urlLines

def sync(url, package):
	forLine = re.compile(r">Download tarball</a>")
	forUrl = re.compile(r"(?<=/packages)[a-z/-]+.tar.gz")
	for line in url:
		if forLine.search(line) != None:
			tarball = forUrl.search(line).group(0)
			cmd = "wget -P ~/.custom/aur %s%s"
			os.system(cmd % (baseURL, tarball))
			cmd = "( tar -zkxf ~/.custom/aur/"
			cmd += package
			cmd += ".tar.gz -C ~/.custom/aur/;"
			cmd += " cd ~/.custom/aur/%s;" % package
			cmd += " makepkg -is; cd -;"
			cmd += " rm -r ~/.custom/aur/%s;" % package
			cmd += " rm ~/.custom/aur/%s.tar.gz; )" % package
			os.system(cmd)

if args > 1:
	if sys.argv[1][0] == "-":
		if len(sys.argv) > 1:
			# u for upgrade
			if sys.argv[1][1] == "u":
				forLine = re.compile("(?<=<h2>Package Details: )[\w\s\.\-:]+")
				forPackage = re.compile("[a-zA-Z\-]+")
				process = Popen("pacman -Qm", shell=True, stdout=PIPE)
				outOfDate = []
				while True:
					line = process.stdout.readline()
					if line == "":
						break
					pac = forPackage.search(line).group(0)
					url = scan(pac)
					if url:
						for entry in url:
							detail = forLine.search(entry)
							if detail != None:
								if detail.group(0) != line[:-1]:
									print pac
									sync(url, pac)
			# l for list
			elif sys.argv[1][1] == "l":
				os.system("pacman -Qm")
			# s for search
			elif sys.argv[1][1] == "s":
				if args > 2:
					for i in range(2,args):
						if scan(sys.argv[i]):
							print "'%s' exists" % sys.argv[i]
				else:
					print "Error: no argument"
			# r for remove
			elif sys.argv[1][1] == "r":
				if args > 2:
					cmd = ""
					for i in range(2,args):
						cmd += " "
						cmd += sys.argv[i]
					os.system("sudo pacman -R" + cmd)
				else:
					print "Error: no argument"
			else:
				print "Error: unknown flag: %s" % sys.argv[1]
		else:
			print "Error: empty flag"
	else:
		for i in range(1,args):
			url = scan(sys.argv[i])
			if url:
				sync(url,sys.argv[i])
else:
	print "Error: no argument"