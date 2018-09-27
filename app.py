from config import *
from set_variables import *
from shutil import copy
import subprocess
import glob
import subprocess
import os
path=os.getcwd()
os.chdir("modules")
files=[]
for file in glob.glob("*"):
    files.append(file)
for file in files:
     with open(file,'r') as fd:
            os.chdir(path)
            copy('template_start.py','test.py')
            with open('test.py','a') as w:
                string=fd.readlines()
                w.writelines(string)
                subprocess.run('python test.py',shell=True)
for i in files:
    print("INFO: Successfully Loaded: "+ i)
