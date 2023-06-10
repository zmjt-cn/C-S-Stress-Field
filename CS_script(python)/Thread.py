#!/usr/bin/python-----v2.7.5-----
# Thread.py---------v1.0---------
# This is a dual-thread mode to view the specific situation of structural changes.
# Warning: Embedded in 'CS.py', can not run alone.

import os
import shutil
import time

try:
    shutil.rmtree('Temp') # Temporary archive initialization.
except:
    pass
os.mkdir('Temp')
for ik in range(240): # Maximum cycle execution time: 240 * 30 = 7200s (2h)
    time.sleep(30) # Copy the 'CONTCAR' file every half a minute.
    cun2 = 'cp CONTCAR Temp/CONTCAR'+str(ik)
    os.system(cun2)
    if ik >0:
        os.system('cp OUTCAR Temp/OUTCAR')
        fon01 = open('Temp/OUTCAR') # Check whether the 'OUTCAR' file completes the calculation, and if so stop execution.
        jobid = 0
        for line in fon01:
            if 'for this job' in line:
                jobid = 1
        fon01.close()
        if jobid == 1:
            break
# print('Temp is all')
# os.mkdir('1')
# os.system('cp -r Temp 1')