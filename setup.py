import os

for f in ['.bashrc',
          '.bash_profile',
          '.bash_logout']:
    os.system('rm ~/{0};'
              'ln ~/.custom/{0} ~/{0}'.format(f))

print "Updated bash files"

if not os.path.isdir('/home/tsx525/.custom/aur'):
    os.system('mkdir /home/tsx525/.custom/aur')