import os

for f in ['.bashrc',
          '.bash_profile',
          '.bash_logout']:
    os.system('rm ~/{0};'
              'ln ~/.custom/{0} ~/{0}'.format(f))

print "Updated bash files"