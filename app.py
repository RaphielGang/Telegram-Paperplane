from config import *
from set_variables import *
import glob
import subprocess
import os
os.chdir("modules")
files=[]
for file in glob.glob("*"):
    files.append(file)
for file in files:
     with open(f,'rb') as fd:
            subprocess.run(['python',fd],stdout=suprocess.PIPE)
