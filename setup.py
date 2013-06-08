import os

for f in ['.bashrc',
          '.bash_profile',
          '.bash_logout']:
    os.system('rm ~/{0};'
              'ln ~/.custom/{0} ~/{0}'.format(f))

os.system("sudo sh -c 'cat bash.bashrc > /etc/bash.bashrc'")

print "Updated bash files"