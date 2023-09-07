#!/usr/bin/python==========v2.7.5==========
# CS.py===============v2.1.4===============
# ========'To apply a compressive-shear biaxial stress field========
# == to the unit cell and calculate the compressive-shear stress.'==
# (Contains cases where compressive stress is present.)
# Authors: Ren Yabin, Yang Bo
# Emails: <s1345358@126.com>, <boyang@hebut.edu.cn>
# Licence: Apache License 2.0

import math
import os
import sys

# Rotation coordinates.
def order():
    fo = open(fname1, 'r')
    line = fo.readlines()
    fo.close()
    # line.insert(7, 'Selective dynamics\n')
    numatom = 0
    for k in range(0, len(line[6].split())):
        numatom += int(line[6].split()[k])
    L0 = []
    L = []
    for ii in range(2, 5):
        L0.append(line[ii].split())
    for i in range(8, numatom + 8):
        L.append(line[i].split()[0:3])
    # if L0[2][2] >= 6:
    L0[0][0], L0[1][0], L0[1][1], L0[2][1], L0[2][2] = L0[2][2], L0[2][1], L0[0][0], L0[1][0], L0[1][1]
    for ij in range(0, len(L)):
        L[ij][0], L[ij][1], L[ij][2] = L[ij][2], L[ij][0], L[ij][1]
    # def takeSecond(elem):
    #     return elem[0]
    # L.sort(key=takeSecond)
    for ij in range(0, 3):
        L0[ij] = '   ' + '   '.join(L0[ij][:]) + '\n'
    for i in range(0, numatom):
        L[i] = '   ' + '   '.join(L[i][:]) + '\n'
    line[2:5] = L0
    line[8:] = L
    fo = open('POSorder', 'w')
    fo.writelines(line)
    fo.close()

# Applying compression-shear biaxial strain.
def cs(dds, step):
    fo = open(fname1, 'r')
    line = fo.readlines()
    fo.close()
    A = line[2].split()
    Aa = (1+float(dds))*float(A[0])
    Ac = float(ds)*float(step)*Aa
    # print(line)
    L =  '    '+str(format(Aa, '.16f'))+'    '+A[1]+'    '+str(format(Ac, '.16f'))+'\n'
    line[2] = L
    fo = open(fname2, 'w')
    fo.writelines(line)
    fo.close()
    os.system(cp_pos)
    # return

# Initial unit cell base vector rotation.
def revolve(name1, name2, theta0):
    fo = open(name1, 'r')
    line = fo.readlines()
    fo.close()
    B = line[3].split()
    C = line[4].split()
    modB = math.sqrt(float(B[1])**2+float(B[2])**2)
    modC = math.sqrt(float(C[1])**2+float(C[2])**2)
    if float(B[1]) >= 0:
        thetab = math.acos(float(B[2])/modB)
    else:
        thetab = -math.acos(float(B[2])/modB)
    if float(C[1]) >= 0:
        thetac = math.acos(float(C[2])/modC)
    else:
        thetac = -math.acos(float(C[2])/modC)
    Bb = modB*math.sin(thetab-theta0)
    Bc = modB*math.cos(thetab-theta0)
    Cb = modC*math.sin(thetac-theta0)
    Cc = modC*math.cos(thetac-theta0)
    # print(line)
    LB =  '    '+B[0]+'    '+str(format(Bb, '.16f'))+'    '+str(format(Bc, '.16f'))+'\n'
    LC =  '    '+C[0]+'    '+str(format(Cb, '.16f'))+'    '+str(format(Cc, '.16f'))+'\n'
    line[3] = LB
    line[4] = LC
    fo = open(name2, 'w')
    fo.writelines(line)
    fo.close()
    # return

# Control compressive stress.
def sigma_ctrl(sigma0):
    sigma_ = str(sigma0)
    dds1 = dds0 # Variable initialization
    if sigma_ != '0':
        os.system(cp_cont)
        sigma = float(sigma0)
        k=0
        # ============ Pressure control program ============ Dichotomy converges compressive stress.
        for i1 in range(0, 10000):
            k+=1
            for i2 in range(1, 10):
                fon = open('OUTCAR')
                for line in fon:
                    if 'in kB' in line:
                        ttt = line.split()
                fon.close()
                t0 = float(ttt[2])/10
                # --------------------
                if abs(dds1) >= 0.02:
                    dds1 = 0.02 # Set the strain maximum
                if t0 > sigma:
                    dds1 = abs(dds1) # Compress
                else:
                    dds1 = -abs(dds1) # Tensile
                cs(dds1, i)
                if ifthread == 1: # dual-thread mode
                    os.system(cmd[7].rstrip('\n')+' & python Thread.py')
                else:
                    os.system(cmd[7]) # stress-xxxz
                check(dds, i)
                # --------------------
                fon1 = open('OUTCAR')
                for line in fon1:
                    if 'in kB' in line:
                        ttt1 = line.split()
                fon1.close()
                t1 = float(ttt1[2])/10
                cun = 'cp CONTCAR OUTCAR OSZICAR '+Name+'/'+str(i)+'/'+str(k)
                cun_ = 'cp -r Temp '+Name+'/'+str(i)+'/'+str(k)
                try:
                    os.mkdir(Name+'/'+str(i)+'/'+str(k))
                except:
                    pass
                os.system(cun)
                if ifthread == 1:
                    os.system(cun_)
                # -------------------- If the result of the two calculations crosses the sigma setting value, the loop jumps out.
                if t0 >= sigma and t1 <= sigma:
                    break
                elif t0 <= sigma and t1 >= sigma:
                    break
                os.system(cp_cont)
                if i2 == 2:
                    dds1 = abs(dds1)*4 # If the standard is not met after 2 calculations, 
                    break            # the strain is multiplied by 2 and cycled again.
                # --------------------
            if abs(t1 - sigma) <= e:
                break
            else:
                os.system(cp_cont)
                dds1 = abs(dds1)/2
        # ==================================================
    else:
        pass

# Check patch program.
def check(dds, step):
    for i in range(100):
        fo1 = open('OUTCAR', 'r')
        t1t = []
        for line in fo1:
            if 'in kB' in line:
                t1t.append(float(line.split()[2])/10)
        fo1.close()
        t01 = float(max(t1t))
        if t01 > float(sigma)+15: # Eliminate potentially erroneous data.
            if dds >= 0.014:
                dds = 0.014
            cs(dds, step)
            if ifthread == 1:
                os.system(cmd[7].rstrip('\n')+' & python Thread.py')
            else:
                os.system(cmd[7])
            dds = dds*2
        else:
            os.system(cp_cont)
            break
    # return
# In the calculation of the mechanical behavior of diamond, there may be a situation that 
# compressive stress inhibits the graphitization of the structure. 
# This subroutine is designed to check and correct this situation (the correction threshold is 15GPa). 
# It may not be used by other materials you calculate.

# Introduction to the 'input.dat' file.
try:
    fin = open("input.dat")
except:
    fin = open("input.dat", 'w')
    fin.write("<< cellname\t\tsigma_0\tiforder\tifthread\tifanimation >>\n")
    fin.write("POSCAR\tPOSCAR_new\t20\t1\t0\t1\n")
    fin.write("<< ds/epsilon_xz\tdds/epsilon_xx\te=absolute_error_range/GPa >>\n")
    fin.write("0.01\t0.002\t0.2\n")
    fin.write("<< theta\tstart\tend\trad/*math.pi/means:0pi/12->8pi/12_interval=1pi/12 >>\n")
    fin.write("1/12\t0\t8\n")
    fin.write("0\t100\t#start&end_step\n")
    fin.write("mpirun  -np 24  /opt/software/vasp.5.4.4.xxxz/bin/vasp_std >out.log\n")
    fin.write("mpirun  -np 24  /opt/software/vasp.5.4.4.xz/bin/vasp_std >out.log\n")
    fin.write("#==================== Parameter Description: ====================\n")
    fin.write("    # This is a necessary input file. Lines starting with '#' are comments, while the other lines denote parameters.\n")
    fin.write("    # ATTENTION: This program applies a compressive-shear biaxial stress field based on VASP software calculation. To use this program successfully, you need to install VASP software locally. This includes the software 'vasp.5.4.4.xxxz' for the unrelaxed strain tensor epsilon_xx and epsilon_xz denoted in line 8, and the software 'vasp.5.4.4.xz' for the unrelaxed strain tensor epsilon_xz denoted in line 9.\n")
    fin.write("    # Line 2 parameter settings: Please do not modify the first two parameters. The third parameter sets the set compressive stress parameter 'sigma_0', with units in GPa. If set to '0', it computes simple shear without compressive stress. The fourth parameter determines whether to perform coordinate transformation on the crystal cell, with '1' denoting convert the crystal plane from z-axis to x-axis. If not needed, set to '0'. Parameters 5 and 6 determine whether to enable double-thread mode and animation archives of CONTCAR, respectively. Set to '1' to enable, or '0' to disable, consistent with the iforder setting.\n")
    fin.write("    # Line 4 parameter settings: The first parameter specifies the increment in 'epsilon_xz' for shear direction and defaults to 0.01. The second parameter denotes the increment in 'epsilon_xx' for compressive direction and defaults to 0.002. The third parameter sets the absolute error limit of the set compressive stress 'sigma_0' at 0.2 GPa.\n")
    fin.write("    # Line 6 parameter settings: The sixth line defines the rotation angle and rotation range of the crystal direction. The 1st parameter, 'theta' (in radians), is set as a fraction. E.g., '1/12' denotes pi/12 (i.e., 15 degrees). The second and third parameters specify the start and end ranges of rotation, e.g., 0 and 8 represents rotates 8 times in total, calculating 9 crystal directions with an interval size of pi/12, starting from 0pi/12 and ending at 8pi/12. Attention: Do not set angles or any parameters in this line to negative values, or the program will report an 'error' while creating folders, which prevents the program from running!!!\n")
    fin.write("    # Line 7 parameter settings: This line denotes the number of steps for initial and final shear strain. It defaults to 0 and 100, respectively. You can set 'start_step' to a non-zero number to continue the previous calculations. For instance, if the first calculation stopped at step 30, you can perform subsequent calculations by extracting the results of Step 30 in the second calculation, instead of starting from 0 again, by setting the 'start_step' to 30. If start and end steps are equal, the program skips shear calculations and proceeds to data extraction.\n")
    fin.write("    # Lines 8 and 9 contain command lines for calling VASP software. The 8th line calls the strain tensor epsilon_xx and epsilon_xz non-relaxation 'vasp.5.4.4.xxxz', whereas the 9th line calls the strain tensor epsilon_xz non-relaxation 'vasp.5.4.4.xz' for calculations involving simple shear stress field and when the compressive stress is set to 0. Modify the statements after '24' based on your software installation location.\n")
    fin.write("    # If you are using a remote supercomputing server, the number of 'cores' in lines 8 and 9 should match those in the PBS file; otherwise, the program may fail to calculate.\n")
    fin.write("# Thank you for using! Feedback is always welcome!")
    fin.close()
    print("'input.dat' file is missing, please resubmit!")
    sys.exit()

filename = ['POSCAR','POSCAR0','INCAR','POTCAR','KPOINTS','animation.py','Thread.py']
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
# print(cmd[4])
fname1 = fin_tmp[1][0]
fname2 = fin_tmp[1][1]
sigma = fin_tmp[1][2]
iforder = int(fin_tmp[1][3])
ifthread = int(fin_tmp[1][4])
ifanimation = int(fin_tmp[1][5])
ds = float(fin_tmp[3][0])
dds0 = float(fin_tmp[3][1])
e = float(fin_tmp[3][2])
thetar = fin_tmp[5][0]
start0 = int(fin_tmp[5][1])
end0 = int(fin_tmp[5][2])
start_step0 = int(fin_tmp[6][0])
end_step = int(fin_tmp[6][1])
if '/' in thetar:
    theta1 = float(thetar[0:thetar.find('/')]) / float(thetar[thetar.find('/') + 1:])
if os.path.exists('POSCAR0') == True:
    os.system('cp POSCAR0 POSCAR')
else:
    os.system('cp POSCAR POSCAR0')
cp_pos = 'cp ' + fname2 + ' ' + fname1
cp_cont = 'cp CONTCAR POSCAR'
name_cs = 'cs.dat' # Data file name

if iforder == 1:
    order() # Rotation coordinates.

for j in range(int(start0), int(end0)+1): # Crystal steering range.
    Name = str(j*int(thetar[0:thetar.find('/')])) + 'pi' +str(thetar[thetar.find('/') + 1:])
    try:
        os.mkdir(Name)
    except:
        pass
    name_revolve = 'POSCAR_'+str(Name[0:Name.find('p')])
    if int(start_step0) == 0:
        theta0 = j * theta1 * math.pi
        if iforder == 1:
            os.system('cp POSorder POSCAR')
        else:
            os.system('cp POSCAR0 POSCAR')
        revolve(fname1, name_revolve, theta0)
        cp_revolve = 'cp '+name_revolve+' '+fname1
        os.system(cp_revolve)
        start_step = start_step0
    else: # If the starting point is not 0, you can continue the previous calculation.
        cp_next = 'cp '+Name+'/'+str(start_step0)+'/'+'CONTCAR '+fname1
        os.system(cp_next)
        start_step = int(start_step0)+1 # The starting point of continuous calculation is step0 + 1.
    # ========================================
    for i in range(int(start_step), int(end_step)+1): # One crystal orientation calculation.
        dds = float(dds0)
        cs(dds, i)
        if str(sigma) == '0':
            os.system(cmd[8]) # stress-xz
        else:
            if ifthread == 1: # dual-thread mode
                os.system(cmd[7].rstrip('\n')+' & python Thread.py')
            else:
                os.system(cmd[7]) # stress-xxxz
            check(dds, i)
        cun0 = 'cp CONTCAR OUTCAR OSZICAR '+Name+'/'+str(i)+'/0'
        cun0_ = 'cp -r Temp '+Name+'/'+str(i)+'/0'
        try:
            os.mkdir(Name+'/'+str(i))
        except:
            pass
        try:
            os.mkdir(Name+'/'+str(i)+'/0')
        except:
            pass
        os.system(cun0)
        if ifthread == 1:
            os.system(cun0_)
        sigma_ctrl(sigma)
        cp_command = 'cp CONTCAR POSCAR OUTCAR OSZICAR '+name_revolve+' '+Name+'/'+str(i)
        os.system(cp_command)
        os.system(cp_cont)
    # ========================================
    datna = Name+'/'+name_cs
    fstr2 = open(datna, 'w')
    fstr2.write('strain\txx\txz\n')
    for k in range(0, int(end_step)+1):
        open2 = Name+'/'+'%s/OUTCAR' %k
        fon = open(open2)
        for line in fon:
            if 'in kB' in line:
                t = line.split()
        fon.close()
        tt=[float(t[2]), float(t[7])]
        li = str(format(float(ds)*k, '.3f'))+'\t'+str(format(tt[0]/10, '.5f'))+'\t'+str(format(tt[1]/10, '.5f'))+'\n'
        fstr2.write(li)
    fstr2.close()
    cp_csdat = 'cp '+ datna +' '+ str(Name[0:Name.find('p')]) +name_cs
    os.system(cp_csdat)
# ==================================================

# Save 'CONTCAR' animation.
if ifanimation == 1:
    os.system('python animation.py')

# Summarize all results
LL = []
for i in range(0, 50):
    name = str(i) +name_cs
    if os.path.exists(name) == True:
        fin = open(name)
        line1 = fin.readlines()
        fin.close()
        L = [[str(i), str(i), str(i)]]
        for j in range(0, len(line1)):
            L.append(line1[j].split())
        bol = LL == []
        if bol == False:
            for jj in range(0, len(L)):
                del L[jj][0]
        for ij in range(0, len(L)):
            if bol == True:
                LL.append(L[ij])
            else:
                for ji in range(0, len(L[0])):
                    LL[ij].append(L[ij][ji])
        print('Calculating...')
    else:
        pass
print('Calculation Complete')

line=[]
for i in range(0, len(LL)):
    for j in range(0, len(LL[i])):
        if j == 0:
            ss = str(LL[i][j])
        else:
            ss = ss+'\t'+str(LL[i][j])
    ss = ss + '\n'
    line.append(ss)
fon = open(name_cs, 'w')
fon.writelines(line)
fon.close()

# Changelog #
# -------- (move.py) v0.0 --------
# v0.0.0, 1st Written Mar 14, 2022. Original version. Modified for the first time.
# v0.1.0, 1st Overhaul Mar 15, 2022. For moving atoms.
# -------- (move.py) v1.0 --------
# v1.0.0, 2nd Overhaul May 28, 2022. In order to apply the compressive-shear biaxial stress field to the model and calculate the stress.
# v1.0.1, 2nd written Jul 1, 2022. Program optimization.
# v1.0.2, 3rd written Jul 4, 2022. Program optimization.
# v1.0.3, 4th written Aug 2, 2022. Bug fixes.
# v1.0.4, 5th written Aug 16, 2022. Program optimization.
# --------- (cs.py) v2.0 ---------
# v2.0.0, 3rd Overhaul Aug 23, 2022. Program renaming & optimization.
# v2.0.1, 2nd written Sep 6, 2022. Bug fixes.
# v2.0.2, 3rd written Sep 7, 2022. Bug fixes.
# --------- (CS.py) v2.1 ---------
# v2.1.0, 4th written Feb 22, 2023. Program structure adjustment and optimization.
# v2.1.1, 5th written Feb 28, 2023. Bug fixes & program optimization.
# v2.1.2, 6th written Mar 2, 2023. Program optimization. Add a dual-thread mode to view the specific situation of structural changes.
# v2.1.3, 7th written Mar 5, 2023. Bug fixes & program optimization. Eliminate potentially erroneous data.
# v2.1.4, 8th written Mar 27, 2023. Program optimization.
# ...