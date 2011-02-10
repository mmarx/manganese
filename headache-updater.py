#!/usr/bin/python

from sys import argv, exit
from subprocess import Popen

invert = False
error = True

if len(argv) > 1 and argv[1] == 'remove':
    invert = True
    error = False
elif len(argv) > 1 and argv[1] == 'update':
    error = False

if error:
    print 'usage: %s (update|remove)' % argv[0]
    exit(1)
    
cfg = {'config': 'headache.conf',
       'header': 'headache.header',
       'types': ['py',                  # python
                 'txt', 'cmake',        # cmake
                 'hxx', 'cxx', 'in',    # c++
                 ],
       'find': r"find . -regex '%(regex)s' -exec %(command)s \;",
       'headache': 'headache -c %(config)s -h %(header)s %(invert)s {}',
       'invert': '-r' if invert else ''
       }

cfg['regex'] = r'.*\.\(' + r'\|'.join(cfg['types']) + r'\)'
cfg['command'] = (cfg['headache'] % cfg)

if __name__ == '__main__':
    Popen (cfg['find'] % cfg, shell=True)
