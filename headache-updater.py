#!/usr/bin/python

from subprocess import Popen

cfg = {'config': 'headache.conf',
       'header': 'headache.header',
       'types': ['py',                  # python
                 'txt', 'cmake',        # cmake
                 'hxx', 'cxx', 'in',    # c++
                 ],
       'find': r"find . -regex '%(regex)s' -exec %(command)s \;",
       'headache': 'headache -c %(config)s -h %(header)s %(invert)s {}',
       'invert': '-r'
       }

if __name__ == '__main__':
    # first, remove the old headers
    cfg['regex'] = r'.*\.\(' + r'\|'.join(cfg['types']) + r'\)'
    cfg['command'] = (cfg['headache'] % cfg)
    Popen (cfg['find'] % cfg, shell=True)
    # now, apply the new ones
    cfg['invert'] = ''
    cfg['command'] = (cfg['headache'] % cfg)
    Popen (cfg['find'] % cfg, shell=True)
