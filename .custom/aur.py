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
	if package[0] == "-" and length > 1:
		# U for Upgrade
		if package[1] == "U":
			if length < 3:
				print "Error: unimplimented"
			# a for all
			elif package[2] == "a":
				forLine = re.compile("(?<=<h2>Package Details: )[\w\s\.\-]+")
				forLocPac = re.compile("[a-zA-Z\-]+")
				# forRmPac = re.compile("(?<=<h2>Package Details: )[a-zA-Z \-]+")
				process = Popen("pacman -Qm", shell=True, stdout=PIPE)
				outOfDate = []
				while True:
					line = process.stdout.readline()
					if line == "":
						break
					pac = forLocPac.search(line).group(0)
					url = "%s/%s/" % (baseURL, pac)
					# print url
					urlLines = []
					for urlLine in urlopen(url).readlines():
						urlLines.append(urlLine.strip())
					for entry in urlLines:
						detail = forLine.search(entry)
						if detail != None:
							# print detail.group(0), line[:-1]
							if detail.group(0) != line[:-1]:
								print pac
								outOfDate.append(pac)
				for pac in outOfDate:
					sync(pac)
		else:
			print "Error: unknown command: %s" % package
	else:
		sync(package)
else:
	print "Error: no argument"