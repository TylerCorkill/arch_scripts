from urllib import urlopen
import sys
import os
import re
from subprocess import Popen, PIPE

package = str(sys.argv[1])
baseURL = "https://aur.archlinux.org/packages"

def sync(package):
	url = "%s/%s/" % (baseURL, package)
	print url
	urlLines = []
	for line in urlopen(url).readlines():
		urlLines.append(line.strip())
	if len(urlLines) < 92:
		print "Error: Package doesn't exist"
	else:
		forLine = re.compile(r">Download tarball</a>")
		forUrl = re.compile(r"(?<=/packages)[a-z/-]+.tar.gz")
		for line in urlLines:
			if forLine.search(line) != None:
				tarball = forUrl.search(line).group(0)
				wget = "wget -P ~/.custom/aur %s%s" % (baseURL, tarball)
				print wget
				os.system(wget)
				tar = "tar -zkxf ~/.custom/aur/%s.tar.gz -C ~/.custom/aur/" % package
				cdTo = "cd ~/.custom/aur/%s" % package
				make = "makepkg -is"
				cdBack = "cd -"
				rmDir = "rm -r ~/.custom/aur/%s" % package
				rmTar = "rm ~/.custom/aur/%s.tar.gz" % package
				os.system("( %s; %s; %s; %s; %s; %s; )" % (tar, cdTo, make, cdBack, rmDir, rmTar))

length = len(package)
if length > 0:
	if package[0] == "-":
		if length > 1:
			# u for upgrade
			if package[1] == "u":
				forLine = re.compile("(?<=<h2>Package Details: )[\w\s\.\-:]+")
				forPackage = re.compile("[a-zA-Z\-]+")
				process = Popen("pacman -Qm", shell=True, stdout=PIPE)
				outOfDate = []
				while True:
					line = process.stdout.readline()
					if line == "":
						break
					pac = forPackage.search(line).group(0)
					url = "%s/%s/" % (baseURL, pac)
					urlLines = []
					for urlLine in urlopen(url).readlines():
						urlLines.append(urlLine.strip())
					for entry in urlLines:
						detail = forLine.search(entry)
						if detail != None:
							if detail.group(0) != line[:-1]:
								print pac
								outOfDate.append(pac)
				for pac in outOfDate:
					sync(pac)
			# l for list
			elif package[1] == "l":
				os.system("pacman -Qm")
			else:
				print "Error: unknown flag: %s" % package
		else:
			print "Error: empty flag"
	else:
		sync(package)
else:
	print "Error: no argument"