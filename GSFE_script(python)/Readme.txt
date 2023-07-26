================================
============GSFE.py=============
================================
=========Version V1.1.5=========
============20221125============

Authors: Ren Yabin (任亚斌), Yang Bo (杨波)
Address: School of Mechanical Engineering, Hebei University of Technology, Tianjin 300401, People's Republic of China
Emails: <s1345358@126.com>, <boyang@hebut.edu.cn>
Licence: Apache License 2.0

en-us
{
To calculate generalized stacking fault energy (GSFE), (Contains cases where compressive stress is present)

>> Functions implemented in the program:
    1. Calculate the GSFE-surface for any material.
    2. Calculate the GSFE curve of a specific crystal direction for any material.
    3. More detailed information is provided in the 'input' file.

>> Required files for program execution:
    'INCAR', 'POSCAR', 'POTCAR', and 'KPOINTS', input files for VASP software.
    'GSFE.py' and 'animation.py', Python scripts for program execution.
    'input.dat', an important parameter input file.
    If you are using a remote supercomputing server, you will also need a PBS file for the task. An example of a 'gsf.pbs' file is provided in this example.

>> File generation by program:
    After the program has finished running, folders such as '0' and '1' will be generated, which contain the raw data results of the GSFE, as well as the 'allCONTCAR' folder that combines all CONTCAR files for this direction, if the parameter for animation is set to '1'. If calculating the GSFE for a specific crystal direction, only the '0' folder will be generated, which contains the data for the specific direction.
    The 'POSCAR0' file generated is a backup of the original 'POSCAR' file submitted. If you want to redo the calculation, there is no need to change any parameters or input files, the program will automatically overwrite. 'POSorder' is the file obtained after transforming the coordinates of the original 'POSCAR' file (if the parameter for 'ifanimation' is set to '1').
    The 'POSCAR_0', 'POSCAR_1', etc. files are generated when calculating the GSFE-surface. If calculating the GSFE for a specific crystal direction, only the 'POSCAR_0' file will be generated.
    The data files generated, such as '0gsf.dat', '1gsf.dat', etc., contain the calculated results of the program in units of GPa.
    The 'cs.dat' file is the final data file, actually a collection of all data such as '0cs.dat', '1cs.dat', etc.

>>Introduction to the parameters of the 'input.dat' file:
    << cellname			sigma_0	iforder	ifanimation >>
    POSCAR	POSCAR_new	20	1	1
    << ds/epsilon_xx	e=absolute_error_range/GPa >>
    0.01	0.2
    << stepy	stepz	layer0	angle >>
    12	12	21	non_or_1/2
    << step  layer1	distance_agl >>
    24	21	2.52
    mpirun  -np 24  /opt/software/vasp.5.4.4.xx/bin/vasp_std >out.log
    mpirun  -np 24  vasp_ncl >out.log
    #==================== Parameter Explanation: ====================
    # This file is a necessary input file. Lines starting with '#' are comment lines, while the rest of the lines are parameters.
    # ATTENTION: The generalized stacking fault energy (GSFE) under the compressive stress field used by this program is based on calculations in VASP software. If you want to use this program successfully, you need to install VASP software locally, including the 'vasp_5.4.4.xx' software indicated in line 9 for the unrelaxed strain tensor epsilon_xx and the uncompiled basic version 'vasp_ncl' software indicated in line 10.
    # Parameter setting in line 2: Please do not modify the first two parameters. The third parameter is the set compressive stress parameter 'sigma_0' in units of GPa. If input is '0', the calculation is the classical GSFE without compressive stress. The fourth parameter is whether to transform the coordinate system of the crystal cell. Set to '1' to transform the crystal plane from z-axis to the x-axis for calculation and fix the atoms of 'POSCAR', and set to '0' if not required. The fifth parameter is whether to open the animation archive of CONTCAR. It is the same as the setting of 'iforder'. Set to '1' to open and set to '0' to close.
    # Parameter setting in line 4: The first parameter is the increment of the strain epsilon_xx in the direction perpendicular to the stacking fault plane, with a default value of 0.01. The second parameter is the absolute error of the set compressive stress 'sigma_0', defaults to 0.2GPa.
    # Parameter setting in line 6: This line contains parameters for the calculation of GSFE-surface. The first and second parameters are the number of sampling points in the b and c directions, with higher density leading to higher accuracy. The third parameter is the layer (atom) of the crystal at which the calculation begins. If set to 21, all atoms beyond this layer (atom) will be moved. The fourth parameter is the angle between the specific crystal direction and the b lattice vector. Select 'non' to calculate GSFE-surface, while select '1/2' or other fraction to enable the calculation of the GSFE for a specific crystal direction. In this case, the parameters in line 8 will be used and the program will not perform GSFE-surface calculation.
    # Parameter setting in line 8: This line contains parameters for the calculation of GSFE for a specific crystal direction. The first parameter is the number of sampling points, with higher density leading to higher accuracy. The second parameter is the layer (atom) of the crystal at which the move begins, consistent with the setting of the GSFE-surface parameters (line 6). The third parameter is the distance of the stacking fault, i.e., the distance of the stacking fault in the pi/2 direction. It is generally set to one period, but the exact value should be measured to determine the stacking fault distance. This parameter can be set to a decimal.
    # Lines 9 and 10 are command lines for calling VASP software. Line 9 calls the unrelaxed strain tensor epsilon_xx in VASP software 'vasp.5.4.4.xx' (used for calculating the GSFE under compressive stress), while line 10 calls the uncompiled basic version 'vasp_ncl' (for classical GSFE calculation when the compressive stress is set to 0). Modify the statements after '24' based on your software installation location.
    # If you are using a remote supercomputing server, the number of 'cores' in lines 9 and 10 should match those in the PBS file; otherwise, the program may fail to calculate.
    # Thank you for using! Feedback is always welcome!
}

zh-cn
{
计算广义层错能（包含了有压应力的情况）。

>>程序已经实现的功能:
    1.计算任意材料整个晶面的面层错能。
    2.计算任意材料特定晶向的层错能。
    3.input文件中提供了更多详细信息。

>>程序运行必要的文件：
    “INCAR”、“POSCAR”、“POTCAR”和“KPOINTS”，VASP软件的输入文件。
    “GSFE.py”和“animation.py”，程序运行的python脚本。
    “input.dat”，重要的参数输入文件。
    如果您使用的是远程超算服务器，还需要用于提交任务的pbs文件，算例中已经提供了一个“gsf.pbs”文件。

>>程序生成文件介绍：
    在程序完成计算后，会生成“0”、“1”等文件夹，该类文件夹内有你所计算的晶向的广义层错能的原始数据结果，以及将本晶向所有CONTCAR文件结果集合到一起的“allCONTCAR”文件夹（如果你将是否开启动画的参数设置为“1”）。如果选择计算特定晶向层错能，只会生成“0”文件夹，该文件夹即为特定晶向的层错能数据。
    生成的“POSCAR0”文件为提交的原始“POSCAR”文件的备份（如果想重复提交运算，所有参数与输入文件均不需要改动，程序会自动覆盖），“POSorder”为原始文件“POSCAR”坐标轮换后的文件（如果你将是否坐标转换参数设置为“1”）。
    生成的“POSCAR_0”、“POSCAR_1”等文件是计算面层错能生成的，若选择计算特定晶向层错能，只会生成“POSCAR_0”文件。
    “0gsf.dat”、“1gsf.dat”等数据文件是生成的运算结果数据，单位为GPa。
    “cs.dat”文件是最终生成的数据文件，实际为“0cs.dat”、“1cs.dat”等所有数据的集合。

>>“input.dat”文件的参数介绍：
    << 晶胞名称		sigma_0/单位GPa	是否坐标转换	是否开启动画 >>
    POSCAR	POSCAR_new	20	1	1
    << ds/epsilon_xx增量=0.01	e=绝对误差范围/GPa >>
    0.01	0.2
    << b方向取点数	c方向取点数	层错开始层（原子）	晶向角 >>
    12	12	21	non
    << 取点数	层错开始层（原子）	层错总距离 >>
    24	21	2.52
    mpirun  -np 24  /opt/software/vasp.5.4.4.xx/bin/vasp_std >out.log
    mpirun  -np 24  vasp_ncl >out.log
    #==================== 参数说明: ====================
    #这个文件是一个必要的输入文件，以#开头的行是注释行，其余的行是参数行。
    #警告：本程序应用的压缩应力场下的广义层错能是基于VASP软件计算的。如果想成功使用这个程序，你需要在本地安装VASP软件，包括第9行表示的应变张量epsilon_xx不弛豫的“vasp.5.4.4.xx”软件，第10行表示的未编译的基础版“vasp_ncl”软件。
    #   第2行参数设置:请不要修改前两个参数，第3个参数为设定的压缩应力参数“sigma_0”，单位为GPa，如果输入为0，计算为无压缩应力的经典广义层错能。第4个参数是是否对晶胞进行坐标转换，设置为“1”表示将需要计算的晶面从z轴转换为x轴，如果不需要，设置为“0”。第5个参数是是否开启CONTCAR的动画存档，与是否坐标转换的设置相同，1打开，0关闭。
    #   第4行参数设置:第1个参数为垂直层错面方向上的应变epsilon_xx的增量，默认为0.01。第2个参数是设定压缩应力sigma_0的绝对误差，设为0.2GPa。
    #   第6行参数设置:第6行是面层错能计算相关参数。第1第2个参数是b和c方向的取点数，点数越密精度越高。第3个参数是层错开始的层数（原子数），如设定为21，则原子位置超过21的所有原子都将被移动。第4个参数是特定晶向与b晶胞矢量的夹角，选择为“non”表示不开始特定晶向计算，程序将计算面层错能。选择为“1/2”或其它分数表示开启特定晶向计算，层错方向为和b晶胞矢量逆时针夹角pi/2的晶向，此时第8行的参数将启用，程序将不进行面层错能计算。
    #   第8行参数设置:第8行是特定晶向层错能计算相关参数。第1个参数是取点数，点数越密精度越高。第2个参数是层错开始的层数（原子数），与面层错能参数的设置方法一致。第3个参数是层错总距离，即在pi/2方向上的层错距离，一般设定为一个周期，请使用者进行精确测量以确定层错距离，该参数可设定为小数。
    #   第9行和第10行是调用VASP软件命令行。第9行命令调用应变张量epsilon_xx不弛豫的“vasp.5.4.4.xx”(用于计算压缩应力场下的层错能)，第9行命令调用未编译的基础版“vasp_ncl”(为压应力设为0的经典层错能计算)。“24”后的语句为调用软件的路径，可根据实际情况进行更改。
    #   如果您使用的是远程超算服务器，第9行和第10行的核数值应该与pbs文件中的核数值相同，否则可能无法计算。
    #感谢您的使用，欢迎您的指正!
}

>>GSFE.py Changelog:

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