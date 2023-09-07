#!/usr/bin/python==========v2.7.5==========
# GSFE.py==============v1.1.5==============
# ==========='To calculate GSFE'===========
# (Contains cases where compressive stress is present)
# Authors: Ren Yabin, Yang Bo
# Emails: <s1345358@126.com>, <boyang@hebut.edu.cn>
# Licence: Apache License 2.0

import math
import os
import sys

# Atomic sorting and rotation coordinates.
def order():
    global posatom
    global numatom
    sigma_ = str(sigma)
    fo = open(fname1, 'r')
    line = fo.readlines()
    fo.close()
    line.insert(7, 'Selective dynamics\n')
    L0 = []
    L1 = []
    for ii in range(2, 5):
        L0.append(line[ii].split())
    for i in range(9, numatom + 9):
        L1.append(line[i].split()[0:3])
    L0[0][0], L0[1][0], L0[1][1], L0[2][1], L0[2][2] = L0[2][2], L0[2][1], L0[0][0], L0[1][0], L0[1][1]
    for ij in range(0, len(L1)):
        L1[ij][0], L1[ij][1], L1[ij][2] = L1[ij][2], L1[ij][0], L1[ij][1]
    for i0 in range(0, 3):
        L0[i0] = '   ' + '   '.join(L0[i0][:]) + '\n'
    mina = L1[posatom[0]][0]
    maxa = L1[posatom[len(posatom)-1]][0]
    for i in range(0, len(L1)):
        if sigma_ == '0':
            L1[i] = '   ' + '   '.join(L1[i][:]) + '   T   F   F' + '\n'
        else:
            if L1[i][0] == mina or L1[i][0] == maxa:
                L1[i] = '   ' + '   '.join(L1[i][:]) + '   F   F   F' + '\n'
            else:
                L1[i] = '   ' + '   '.join(L1[i][:]) + '   T   F   F' + '\n'
    line[2:5] = L0
    line[9:] = L1
    fo = open(fname2, 'w')
    fo.writelines(line)
    fo.close()
    fo1 = open('POSorder', 'w')
    fo1.writelines(line)
    fo1.close()
    os.system(cp_pos)

# Calculate the list of atomic coordinate positions
def posatom_calculate(fname, n):
    global posatom
    global numatom
    fo = open(fname, 'r')
    line = fo.readlines()
    fo.close()
    L = []
    posatom = []
    numatom = 0
    for k in range(0, len(line[6].split())):
        numatom += int(line[6].split()[k])
    for ik in range(0, len(line)):
        if 'Direct' in line[ik]:
            S = ik
            break
    for i in range(S+1, numatom+S+1):
        L.append(line[i].split()[0:3])
    for ij in range(0, len(L)):
        L[ij].append(ij)
    def takeSecond(elem):
        if n == 0:
            return elem[0]
        else:
            return elem[2]
    L.sort(key=takeSecond)
    for kk in range(0, len(L)):
        posatom.append(L[kk][3])

# yn == 0, movey; yn == 1, movez
def move_yz(dyz, yn):
    global posatom
    global numatom
    dyz = float(dyz)
    layer = int(layer0)
    yn = int(yn)
    fo = open(fname1, 'r')
    line = fo.readlines()
    fo.close()
    L1 = []
    for i in range(9, numatom + 9):
        L1.append(line[i].split())
    for i in posatom[layer-1:len(posatom)]: # Move atoms starting from layer=layer0.
        if yn == 0:
            L1[i][1] = str(format(float(L1[i][1])+dyz, '.16f'))
        elif yn == 1:
            L1[i][2] = str(format(float(L1[i][2])+dyz, '.16f'))
    for i in range(0, len(L1)):
        L1[i] = '   ' + '   '.join(L1[i][:]) + '\n'
    line[9:] = L1
    fo = open(fname2, 'w')
    fo.writelines(line)
    fo.close()
    os.system(cp_pos)

# Calculate GSFE of single crystal orientation.
def move_agl(angle0):
    dagl0 = float(dagl)
    layer = int(layer1)
    fo = open(fname1, 'r')
    line = fo.readlines()
    fo.close()
    L1 = []
    for i in range(9, numatom + 9):
        L1.append(line[i].split())
    Angle, modb, modc = Angle_calculate('POSCAR')
    dagl1 = ((dagl0*dis_agl)*math.sin(Angle-angle0)/math.sin(math.pi-Angle))/modb
    dagl2 = ((dagl1*modb)*math.sin(angle0)/math.sin(Angle-angle0))/modc
    for i in posatom[layer-1:len(posatom)]: # Move atoms starting from layer=layer1.
        L1[i][1] = str(format(float(L1[i][1])+dagl1, '.16f'))
        L1[i][2] = str(format(float(L1[i][2])+dagl2, '.16f'))
    for i in range(0, len(L1)):
        L1[i] = '   ' + '   '.join(L1[i][:]) + '\n'
    line[9:] = L1
    fo = open(fname2, 'w')
    fo.writelines(line)
    fo.close()
    os.system(cp_pos)

# Apply normal stress.
def strain(dds):
    dds = float(dds)
    fo = open(fname1, 'r')
    line = fo.readlines()
    fo.close()
    A = line[2].split()
    Aa = (1-float(dds))*float(A[0]) # The default is compress.
    L = '   '+str(format(Aa, '.16f'))+'   '+A[1]+'   '+A[2]+'\n'
    line[2] = L
    fo = open(fname2, 'w')
    fo.writelines(line)
    fo.close()
    os.system(cp_pos)

# Calculate the true stress ratio except for the vacuum layer.
def ratio_calculate(fielname):
    global ratio
    global posatom
    fo1 = open(fielname, 'r')
    line = fo1.readlines()
    fo1.close()
    xx0 = line[posatom[0]+9].split()[0]
    xx1 = line[posatom[len(posatom)-1] + 9].split()[0]
    ratio = abs(float(xx1) - float(xx0))

# Calculate the angle between b and c and the length of b and c.
def Angle_calculate(fielname):
    fo1 = open(fielname, 'r')
    line = fo1.readlines()
    fo1.close()
    def mod(a):
        A = math.sqrt(a[0]**2+a[1]**2)
        return A
    def Dot(a1, a2):
        a12 = a1[0]*a2[0]+a1[1]*a2[1]
        return a12
    b = [float(line[3].split()[1]),float(line[3].split()[2])]
    c = [float(line[4].split()[1]),float(line[4].split()[2])]
    Angle = math.acos(Dot(b,c)/(mod(b)*mod(c)))
    modb = mod(b)
    modc = mod(c)
    return Angle, modb, modc

# Control compressive stress.
def sigma_ctrl(sigma0):
    sigma_ = str(sigma0)
    dds = ds # Variable initialization
    if sigma_ != '0':
        os.system('cp CONTCAR POSCAR')
        sigma1 = float(sigma0)
        # ============ Pressure control program ============ Dichotomy converges compressive stress.
        for i1 in range(0, 10000):
            for i2 in range(1, 10):
                fon = open('OUTCAR')
                for line in fon:
                    if 'in kB' in line:
                        ttt = line.split()
                fon.close()
                t0 = float(ttt[2])/10/ratio
                # --------------------
                if abs(dds) >= 0.04:
                    dds = 0.04 # Set the strain maximum
                if t0 < float(sigma1):
                    dds = abs(dds) # Compress
                else:
                    dds = -abs(dds) # Tensile
                strain(dds)
                os.system(cmd[8]) # stress-xx
                # --------------------
                fon1 = open('OUTCAR')
                for line in fon1:
                    if 'in kB' in line:
                        ttt1 = line.split()
                fon1.close()
                t1 = float(ttt1[2])/10/ratio
                # -------------------- If the result of the two calculations crosses the sigma setting value, the loop jumps out.
                if t0 >= sigma1 and t1 <= sigma1:
                    break
                elif t0 <= sigma1 and t1 >= sigma1:
                    break
                os.system('cp CONTCAR POSCAR')
                if i2 == 2:
                    dds = abs(dds)*4 # If the standard is not met after 2 calculations, 
                    break            # the strain is multiplied by 2 and cycled again.
                # --------------------
            if abs(t1 - sigma1) <= e:
                break
            else:
                os.system('cp CONTCAR POSCAR')
                dds = abs(dds)/2
        # ==================================================
    else:
        pass

# Introduction to the 'input.dat' file.
try:
    fin = open("input.dat")
except:
    fin = open("input.dat", 'w')
    fin.write("<< cellname\t\tsigma_0\tiforder\tifanimation >>\n")
    fin.write("POSCAR\tPOSCAR_new\t0\t1\t1\n")
    fin.write("<< ds/epsilon_xx	e=absolute_error_range/GPa >>\n")
    fin.write("0.01\t0.2\n")
    fin.write("<< stepy\tstepz\tlayer0\tangle >>\n")
    fin.write("12\t12\t21\tnon\n")
    fin.write("<< step\tlayer1\tdistance_agl >>\n")
    fin.write("24\t21\t2.52\n")
    fin.write("mpirun  -np 24  /opt/software/vasp.5.4.4.xx/bin/vasp_std >out.log\n")
    fin.write("mpirun  -np 24  vasp_ncl >out.log\n")
    fin.write("#==================== Parameter Description: ====================\n")
    fin.write("    # This file is a necessary input file. Lines starting with '#' are comment lines, while the rest of the lines are parameters.\n")
    fin.write("    # ATTENTION: The generalized stacking fault energy (GSFE) under the compressive stress field used by this program is based on calculations in VASP software. If you want to use this program successfully, you need to install VASP software locally, including the 'vasp_5.4.4.xx' software indicated in line 9 for the unrelaxed strain tensor epsilon_xx and the uncompiled basic version 'vasp_ncl' software indicated in line 10.\n")
    fin.write("    # Parameter setting in line 2: Please do not modify the first two parameters. The third parameter is the set compressive stress parameter 'sigma_0' in units of GPa. If input is '0', the calculation is the classical GSFE without compressive stress. The fourth parameter is whether to transform the coordinate system of the crystal cell. Set to '1' to transform the crystal plane from z-axis to the x-axis for calculation and fix the atoms of 'POSCAR', and set to '0' if not required. The fifth parameter is whether to open the animation archive of CONTCAR. It is the same as the setting of 'iforder'. Set to '1' to open and set to '0' to close.\n")
    fin.write("    # Parameter setting in line 4: The first parameter is the increment of the strain epsilon_xx in the direction perpendicular to the stacking fault plane, with a default value of 0.01. The second parameter is the absolute error of the set compressive stress 'sigma_0', defaults to 0.2GPa.\n")
    fin.write("    # Parameter setting in line 6: This line contains parameters for the calculation of GSFE-surface. The first and second parameters are the number of sampling points in the b and c directions, with higher density leading to higher accuracy. The third parameter is the layer (atom) of the crystal at which the calculation begins. If set to 21, all atoms beyond this layer (atom) will be moved. The fourth parameter is the angle between the specific crystal direction and the b lattice vector. Select 'non' to calculate GSFE-surface, while select '1/2' or other fraction to enable the calculation of the GSFE for a specific crystal direction. In this case, the parameters in line 8 will be used and the program will not perform GSFE-surface calculation.\n")
    fin.write("    # Parameter setting in line 8: This line contains parameters for the calculation of GSFE for a specific crystal direction. The first parameter is the number of sampling points, with higher density leading to higher accuracy. The second parameter is the layer (atom) of the crystal at which the move begins, consistent with the setting of the GSFE-surface parameters (line 6). The third parameter is the distance of the stacking fault, i.e., the distance of the stacking fault in the pi/2 direction. It is generally set to one period, but the exact value should be measured to determine the stacking fault distance. This parameter can be set to a decimal.\n")
    fin.write("    # Lines 9 and 10 are command lines for calling VASP software. Line 9 calls the unrelaxed strain tensor epsilon_xx in VASP software 'vasp.5.4.4.xx' (used for calculating the GSFE under compressive stress), while line 10 calls the uncompiled basic version 'vasp_ncl' (for classical GSFE calculation when the compressive stress is set to 0). Modify the statements after '24' based on your software installation location.\n")
    fin.write("    # If you are using a remote supercomputing server, the number of 'cores' in lines 9 and 10 should match those in the PBS file; otherwise, the program may fail to calculate.\n")
    fin.write("# Thank you for using! Feedback is always welcome!")
    fin.close()
    print("'input.dat' file is missing, please resubmit!")
    sys.exit()

filename = ['POSCAR','POSCAR0','INCAR','POTCAR','KPOINTS','animation.py']
ifexit = 0
if os.path.exists(filename[0]) == False and os.path.exists(filename[1]) == False:
    print("'"+filename[0]+"' file is missing, please resubmit!")
    ifexit = 1
for n in range(2,len(filename)):
    if os.path.exists(filename[n]) == False:
        ifexit = 1
        print("'"+filename[n]+"' file is missing, please resubmit!")
if ifexit == 1:
    sys.exit()

# ================== Main program ==================
fin_tmp = []
cmd = []
for line in fin:
    fin_tmp.append(line.split())
    cmd.append(line)
fin.close()
fname1 = fin_tmp[1][0]
fname2 = fin_tmp[1][1]
sigma = fin_tmp[1][2]
iforder = int(fin_tmp[1][3])
ifanimation = int(fin_tmp[1][4])
ds = float(fin_tmp[3][0])
e = float(fin_tmp[3][1])
stepy = int(fin_tmp[5][0])
stepz = int(fin_tmp[5][1])
layer0 = fin_tmp[5][2]
angle = fin_tmp[5][3]
step_agl = int(fin_tmp[7][0])
layer1 = int(fin_tmp[7][1])
dis_agl = float(fin_tmp[7][2])
dagl = 1/float(step_agl)
dy = 1/float(stepy)
dz = 1/float(stepz)
if os.path.exists('POSCAR0') == True:
    os.system('cp POSCAR0 POSCAR')
else:
    os.system('cp POSCAR POSCAR0')
cp_pos = 'cp ' + fname2 + ' ' + fname1
name_gsf = 'gsf.dat'
posatom_calculate(fname1, iforder)

if iforder == 1:
    order() # Atomic sorting and rotation coordinates.
if angle == 'non': # Calculate the Crystal planes GSFE.
    for j in range(0, stepz+1):
        try:
            os.mkdir(str(j))
        except:
            pass
        if j != 0:
            cp_pos1 = 'cp POSCAR_' + str(j-1) + ' ' + fname1
            os.system(cp_pos1)
            move_yz(dz, 1)
            if str(sigma) == '0':
                os.system(cmd[9]) # stress-free
            else:
                os.system(cmd[8]) # stress-xx
            ratio_calculate('POSCAR_0') # Calculate the true stress ratio except for the vacuum layer
            sigma_ctrl(sigma) # Control compressive stress
            try:
                os.mkdir(str(j)+'/0')
            except:
                pass
            cp_pos2 = 'cp CONTCAR POSCAR_' + str(j)
            os.system(cp_pos2)
            cp_command = 'cp CONTCAR POSCAR OUTCAR OSZICAR POSCAR_'+str(j)+' '+str(j)+'/0'
            os.system(cp_command)
            os.system('cp CONTCAR POSCAR')
        for i in range(0, stepy+1):
            if j == 0 and i == 0:
                os.system(cmd[9]) # 1st calculate, stress-free
                ratio_calculate('CONTCAR') # Calculate the true stress ratio except for the vacuum layer
                sigma_ctrl(sigma) # Control compressive stress
                try:
                    os.mkdir(str(j)+'/0')
                except:
                    pass
                os.system('cp CONTCAR POSCAR_0')
                cp_command = 'cp CONTCAR POSCAR OUTCAR OSZICAR POSCAR_'+str(j)+' '+str(j)+'/0'
                os.system(cp_command)
                os.system('cp CONTCAR POSCAR')
            if i != 0:
                move_yz(dy, 0)
                if str(sigma) == '0':
                    os.system(cmd[9]) # stress-free
                else:
                    os.system(cmd[8]) # stress-xx
                sigma_ctrl(sigma) # Control compressive stress
                try:
                    os.mkdir(str(j)+'/'+str(i))
                except:
                    pass
                cp_command1 = 'cp CONTCAR POSCAR OUTCAR OSZICAR POSCAR_'+str(j)+' '+str(j)+'/'+str(i)
                os.system(cp_command1)
                os.system('cp CONTCAR POSCAR')
        # -------------------- Extract the data from step j
        datna = str(j)+'/'+name_gsf
        fstr2 = open(datna, 'w')
        fstr2.write('move\tenergy\n')
        for k in range(0, stepy+1):
            open2 = str(j)+'/%s/OUTCAR' %k
            fon = open(open2)
            for line in fon:
                if 'without entropy' in line:
                    t = line.split()
            fon.close()
            tt=float(t[6])
            li = str(k)+'\t'+str(format(tt, '.8f'))+'\n'
            fstr2.write(li)
        fstr2.close()
        cp_gsfdat = 'cp '+ datna +' '+ str(j) +name_gsf
        os.system(cp_gsfdat)
else: # calculations for a single crystal orientation GSFE.
    if '/' in angle:
        angle0 = float(angle[0:angle.find('/')])/float(angle[angle.find('/')+1:])*math.pi
    else:
        angle0 = float(angle)*math.pi
    try:
        os.mkdir('0')
    except:
        pass
    for i in range(0, step_agl+1):
        try:
            os.mkdir('0/'+str(i))
        except:
            pass
        if i == 0:
            os.system(cmd[5]) # stress-free
            ratio_calculate('CONTCAR') # Calculate the true stress ratio except for the vacuum layer
            sigma_ctrl(sigma) # Control compressive stress
            os.system('cp CONTCAR POSCAR_0')
        else:
            move_agl(angle0)
            if str(sigma) == '0':
                os.system(cmd[9]) # stress-free
            else:
                os.system(cmd[8]) # stress-xx
            sigma_ctrl(sigma) # Control compressive stress
        cp_command = 'cp CONTCAR POSCAR OUTCAR OSZICAR POSCAR_0'+' 0/'+str(i)
        os.system(cp_command)
        os.system('cp CONTCAR POSCAR')
    datna = '0/'+name_gsf
    fstr2 = open(datna, 'w')
    fstr2.write('move\tenergy\n')
    for k in range(0, step_agl+1):
        open2 = '0/%s/OUTCAR' %k
        fon = open(open2)
        for line in fon:
            if 'without entropy' in line:
                t = line.split()
        fon.close()
        tt=float(t[6])
        li = str(k)+'\t'+str(format(tt, '.8f'))+'\n'
        fstr2.write(li)
    fstr2.close()
    cp_gsfdat = 'cp '+ datna +' 0'+name_gsf
    os.system(cp_gsfdat)
# ==================================================

# Save 'CONTCAR' animation.
if ifanimation == 1:
    os.system('python animation.py')

# Summarize all results
L1 = []
L2 = []
if angle != 'non':
    stepz = 0
for j in range(0, stepz+1):
    datna = str(j)+name_gsf
    L = []
    fin = open(datna)
    for line in fin:
        L.append(line.split())
        if j == 0:
            L1.append(line.split())
            L2.append(line.split())
    if j != 0:
        for i in range(0, len(L)):
            L1[i].append(L[i][1])
            L2[i].append(L[i][1])
    L1[0][j+1] = str(j)
    L2[0][j+1] = str(j)

eV = 16.021766208
fo_0 = []
fo = open('POSCAR_0', 'r')
for line in fo:
    fo_0.append(line.split())
fo.close()
a = float(fo_0[3][1])
b = float(fo_0[4][2])
L2[0][0] = 'sigma='+str(sigma)
for ii in range(1, len(L2)):
    for jj in range(1, len(L2[0])):
        L2[ii][jj] = str(format((float(L2[ii][jj]) - float(L1[1][1]))*eV/(a*b), '.8f'))
fon = open(name_gsf, 'w')
for k in range(0, len(L2)):
    LL = '\t'.join(L2[k][:])+'\n'
    fon.write(LL)
fon.close()

# Changelog #
# ------------- v1.0 -------------
# v1.0.0, 1st written Sep 15, 2022. Calculate the GSFE of the crystal plane.(stress-free)
# v1.0.1, 2nd written Oct 14, 2022. Program optimization.
# v1.0.2, 3rd written Oct 26, 2022. Program optimization.
# ------------- v1.1 -------------
# v1.1.0, 1st Overhaul Nov 23, 2022. Program optimization. Add cases where compressive stress is present.
# v1.1.1, 2nd written Nov 24, 2022. Add calculate GSFE of specific crystal direction.
# v1.1.2, 3rd written Nov 25, 2022. Program optimization.
# v1.1.3, 4th written Dec 10, 2022. Bug fixes.
# v1.1.4, 5th written Dec 12, 2022. Bug fixes.
# v1.1.5, 6th written Mar 28, 2023. Program optimization. Add broad applicability.
# ...