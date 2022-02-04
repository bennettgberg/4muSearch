

import os, glob

for d in glob.glob('*/'):
    os.system("cd {0:s}; mv {0:s}_001.out tmp; rm *.out; mv tmp {0:s}_001.out; cd ..".format(d.strip('/')))
