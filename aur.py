from urllib import urlopen
import sys
import os
import re
from subprocess import Popen, PIPE


def scan(package):
    """
    Checks if package url exists

    """
    url = "%s/%s/" % (baseURL, package)
    urlLines = []
    for line in urlopen(url).readlines():
        urlLines.append(line.strip())
    if len(urlLines) < 92:
        print "'%s' doesn't exist" % package
        return
    return urlLines


def sync(url, package):
    """
    Installer function

    """
    forLine = re.compile(r">Download tarball</a>")
    forUrl = re.compile(r"(?<=/packages)[a-z/\-\d]+\.tar\.gz")
    for line in url:
        if forLine.search(line) is not None:
            os.system("wget -P ~/.custom/aur %s%s" % (
                baseURL, forUrl.search(line).group(0)))
            os.system("( tar -zkxf ~/.custom/aur/{0}"
                      ".tar.gz -C ~/.custom/aur/;"
                      " cd ~/.custom/aur/{0};"
                      " makepkg -is; cd -;"
                      " sudo rm -r ~/.custom/aur/{0};"
                      " rm ~/.custom/aur/{0}.tar.gz; )"
            .format(package))


def update():
    """
    Updates all packages from aur

    """
    forLine = re.compile("(?<=<h2>Package Details: )[\w\s\.\-:]+")
    forPackage = re.compile("[a-zA-Z\-\d]+")
    process = Popen("pacman -Qm", shell=True, stdout=PIPE)
    while True:
        line = process.stdout.readline()
        if line == "":
            break
        pac = forPackage.search(line).group(0)
        url = scan(pac)
        if url:
            for entry in url:
                detail = forLine.search(entry)
                if not detail:
                    continue
                if detail.group(0) != line[:-1]:
                    print pac
                    sync(url, pac)


def listPkgs():
    """
    Lists local packages from aur

    """
    os.system("pacman -Qm")


def search():
    """
    Searches for packages

    """
    if args > 2:
        for i in range(2, args):
            if scan(sys.argv[i]):
                print "'%s' exists" % sys.argv[i]
    else:
        print "Error: no argument"


def remove():
    """
    Removes packages

    """
    if args > 2:
        cmd = ""
        for i in range(2, args):
            cmd += " "
            cmd += sys.argv[i]
        os.system("sudo pacman -R" + cmd)
    else:
        print "Error: no argument"


if __name__ == "__main__":
    baseURL = "https://aur.archlinux.org/packages"
    args = len(sys.argv)
    if args > 1:
        if sys.argv[1][0] == "-":
            if len(sys.argv) > 1:
                functions = {'u': update,
                             'l': listPkgs,
                             's': search,
                             'r': remove}
                if sys.argv[1][1] in functions:
                    functions[sys.argv[1][1]]()
                else:
                    print "Error: unknown flag: %s" % sys.argv[1]
            else:
                print "Error: empty flag"
        else:
            for i in range(1, args):
                url = scan(sys.argv[i])
                if url:
                    sync(url, sys.argv[i])
    else:
        print "Error: no argument"