import os

for f in ['.bashrc',
          '.bash_profile',
          '.bash_logout']:
    os.system('rm ~/{0};'
              'ln ~/.custom/{0} ~/{0}'.format(f))

os.system('cat ~/.custom/bash.bashrc | sudo tee /etc/bash.bashrc')

print "Updated bash files"