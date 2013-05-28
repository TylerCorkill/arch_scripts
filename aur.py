from urllib import urlopen
from contextlib import closing
import sys
import os
import re
from subprocess import Popen, PIPE


def scan(pac, regex=None):
    """
    Checks if package url exists

    """
    with closing(urlopen('https://aur.archlinux.org/packages/%s/' % pac)) as url:
        if regex is None:
            if len(url.readlines()) < 92:
                yield None
        else:
            for line in url:
                value = regex.search(line)
                if value is not None:
                    yield value.group(0)


def sync(package):
    """
    Installer function

    """
    for value in scan(package, re.compile(r'(?<=/packages)'
                                          r'[a-z/\-\d]+\.tar\.gz')):
        os.system('wget -P ~/.custom/aur '
                  'https://aur.archlinux.org/packages%s' % value)
        os.system(' tar -zkxf ~/.custom/aur/{0}.tar.gz'
                  ' -C ~/.custom/aur/;'
                  ' cd ~/.custom/aur/{0};'
                  ' makepkg -is;'
                  ' cd -;'
                  ' rm -fr ~/.custom/aur/*;'.format(package))


def update():
    """
    Updates all packages from aur

    """
    forLine = re.compile("(?<=<h2>Package Details: )[\w\s\.\-:]+")
    forPackage = re.compile("[a-zA-Z\-\d]+")
    process = Popen('pacman -Qm', shell=True, stdout=PIPE)
    while True:
        line = process.stdout.readline().strip()
        if not line:
            break
        pac = forPackage.search(line).group(0)
        for value in scan(pac, forLine):
            if value != line:
                print pac
                sync(pac)


def listPkgs():
    """
    Lists local packages from aur

    """
    os.system('pacman -Qm')


def search():
    """
    Searches for packages

    """
    for entry in sys.argv[2:]:
        if scan(entry) is not None:
            print "'%s' exists" % entry
        else:
            print "'%s' doesn't exist" % entry
    else:
        print 'Error: no argument'


def remove():
    """
    Removes packages

    """
    if len(sys.argv) > 2:
        cmd = ['sudo pacman -R']
        for entry in sys.argv[2:]:
            cmd.append(entry)
        os.system(' '.join(cmd))
    else:
        print 'Error: no argument'


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1][0] == '-':
            if len(sys.argv[1]) > 1:
                functions = {'u': update,
                             'l': listPkgs,
                             's': search,
                             'r': remove}
                if sys.argv[1][1] in functions:
                    functions[sys.argv[1][1]]()
                else:
                    print 'Error: unknown flag: %s' % sys.argv[1]
            else:
                print 'Error: empty flag'
        else:
            for entry in sys.argv[1:]:
                sync(entry)
    else:
        print 'Error: no argument'

