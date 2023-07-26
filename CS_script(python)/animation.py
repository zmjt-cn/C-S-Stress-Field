#!/usr/bin/python-----v2.7.5-----
# animation.py--------v1.0-------
# -----for CONTCAR animation-----
# ------and all OUTCAR data------
# It can be embedded in 'CS.py' or run alone.

import os
step0 = 0
step1 = 1000
aniname0 = 'allCONTCAR'
aniname1 = 'allOUTCAR'

def ani(name, step0, step1):
    try:
        os.mkdir(name +'/'+ aniname0+str(name[0:name.find('p')]))
        os.mkdir(name +'/'+ aniname1+str(name[0:name.find('p')]))
    except:
        pass
    for i in range(step0, step1 + 1):
        copy0 = 'cp '+ name +'/%s/CONTCAR ' %i + name +'/'+aniname0+str(name[0:name.find('p')])+'/CONTCAR%s' %i
        copy2 = 'cp '+ name +'/%s/OUTCAR ' %i + name +'/'+aniname1+str(name[0:name.find('p')])+'/OUTCAR%s' %i
        # copy2 = 'cp '+ name +'/last/CONTCAR '+ name +'/ani/%s' %i
        if os.path.exists(name + '/%s/CONTCAR' %i) == True:
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
thetar = fin_tmp[5][0]
star0 = fin_tmp[5][1]
stop0 = fin_tmp[5][2]

for i in range(int(star0), int(stop0)+1):
    Name = str(i*int(thetar[0:thetar.find('/')])) + 'pi' +str(thetar[thetar.find('/') + 1:])
    ani(Name, step0, step1)
# return