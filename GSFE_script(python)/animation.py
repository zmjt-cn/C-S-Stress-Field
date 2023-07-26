#!/usr/bin/python-----v2.7.5-----
# animation.py--------v1.0-------
# -----for CONTCAR animation-----
# ------and all OUTCAR data------
# It can be embedded in 'GSFE.py' or run alone.

import os
step0 = 0
step1 = 1000
aniname0 = 'CONTCAR'
aniname1 = 'POSCAR'

def ani(name, step0, step1):
    try:
        os.mkdir(name +'/all'+ aniname0+str(name))
        os.mkdir(name +'/all'+ aniname1+str(name))
    except:
        pass
    for i in range(step0, step1 + 1):
        copy0 = 'cp '+ name +'/%s/' %i +aniname0+' '+ name +'/all'+ aniname0+str(name)+'/'+aniname0+str(i)
        copy2 = 'cp '+ name +'/%s/' %i +aniname1+' '+ name +'/all'+ aniname1+str(name)+'/'+aniname1+str(i)
        # copy2 = 'cp '+ name +'/last/CONTCAR '+ name +'/ani/%s' %i
        if os.path.exists(name + '/%s/' %i + aniname0) == True:
            os.system(copy0+' & '+copy2)
            print('Calculating...')
            # elif os.path.exists(name + '/last/CONTCAR') == True:
            # os.system(copy2)
            # print('Calculation complete')
            # break
        else:
            print('Calculation complete')
            break
    return

fin = open("input.dat")
fin_tmp = []
for line in fin:
    fin_tmp.append(line.split())
fin.close()
ifanimation = int(fin_tmp[1][4])
if str(fin_tmp[5][3]) == 'non':
    stepz = int(fin_tmp[5][1])
else:
    stepz = 0

for i in range(0, stepz+1):
    Name = str(i)
    ani(Name, step0, step1)
# return