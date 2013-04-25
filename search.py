import sys
import os

search = "https://www.google.com/search?q="
for i in range(1, len(sys.argv)):
	search += "%s+" % str(sys.argv[i])
os.system("chromium %s" % search)