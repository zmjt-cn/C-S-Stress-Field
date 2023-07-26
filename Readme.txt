

Authors: Ren Yabin (任亚斌), Yang Bo (杨波)
Address: School of Mechanical Engineering, Hebei University of Technology, Tianjin 300401, People's Republic of China
Emails: <s1345358@126.com>, <boyang@hebut.edu.cn>
Licence: Apache License 2.0

================================
=============CS.py==============
================================
=========Version V2.1.4=========
============20230327============

en-us
{
To apply a compressive-shear biaxial stress field to the unit cell and calculate the compressive-shear stress, this program has been developed.

>>The program features the following:
    1. Calculation of the anisotropy of the cell under compressive-shear biaxial stress field and automatic steering calculation.
    2. 'CONTCAR' file saved every 30 seconds in dual-thread mode, allowing visualization of structural deformation and analysis of phase transition mechanism.
    3. More detailed information is provided in the 'input' file.

>>Files required for the program to run include:
    Input files such as 'INCAR', 'POSCAR', 'POTCAR', and 'KPOINTS' used by the VASP software.
    Python scripts such as 'CS.py', 'animation.py', and 'Thread.py' are also required.
    'input.dat' is another important filed which contains parameter inputs.
    If you are using remote supercomputer server, you will also need to submit a PBS file for the task. In this example, a 'cs.pbs' file has been provided.

>>Files that the program generates include:
    Upon completion of the calculation, folders such as '0pi12' and '1pi12' will be generated, containing the original data results of the compressive-shear biaxial stress field calculated for your crystal direction. Additionally, the 'allCONTCAR' folder will contain all CONTCAR file results (if 'ifanimation' is set to '1').
    The 'POSCAR0' file is a backup of the original 'POSCAR' file submitted, with all parameters and input files automatically overwritten upon resubmission. 'POSorder' is a coordinate-transformed file of the original POSCAR file (if 'iforder' is set to '1').
    Generated files such as 'POSCAR0', 'POSCAR1', correspond to the step 0 structure of the crystal direction you calculated (i.e., the file following the initial rotation).
    Data files such as '0cs.dat' and '1cs.dat' are the calculation result data of one crystal direction, given in GPa.
    The 'cs.dat' file is the final generated data file, which collects data from all crystal data such as '0cs.dat' and '1cs.dat'.
}

zh-cn
{
为了对晶胞施加压缩-剪切双轴应力场，计算压缩-剪切应力，开发了本程序。

>>程序已经实现的功能：
    1.计算压缩-剪切双轴应力场作用下晶体的各向异性，实现自动转向计算。
    2.双线程模式计算时每30秒保存一次“CONTCAR”文件，可用于查看关键结构的变形过程，分析结构相变机理。
    3.input文件中提供了更多详细信息。

>>程序运行必要的文件：
    “INCAR”、“POSCAR”、“POTCAR”和“KPOINTS”，VASP软件的输入文件。
    “CS.py”、“animation.py”和“Thread.py”，程序运行的python脚本。
    “input.dat”，重要的参数输入文件。
    如果您使用的是远程超算服务器，还需要用于提交任务的pbs文件，算例中已经提供了一个“cs.pbs”文件。

>>程序生成文件介绍：
    在程序完成计算后，会生成“0pi12”、“1pi12”等文件夹，该类文件夹内有你所计算的晶向的压缩-剪切双轴应力场的原始数据结果，以及将本晶向所有CONTCAR文件结果集合到一起的“allCONTCAR”文件夹（如果你将是否开启动画的参数设置为“1”）。
    生成的“POSCAR0”文件为提交的原始“POSCAR”文件的备份（如果想重复提交运算，所有参数与输入文件均不需要改动，程序会自动覆盖），“POSorder”为原始文件“POSCAR”坐标轮换后的文件（如果你将是否坐标转换参数设置为“1”）。
    生成的“POSCAR_0”、“POSCAR_1”等文件对应的是你所计算的晶向的第0步结构（即原始文件转向后的文件）。
    “0cs.dat”、“1cs.dat”等数据文件是单条晶向的运算结果数据，单位为GPa。
    “cs.dat”文件是最终生成的数据文件，实际为“0cs.dat”、“1cs.dat”等所有晶向数据的集合。
}

================================
============GSFE.py=============
================================
=========Version V1.1.5=========
============20221125============

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

Thank you for using! Feedback is always welcome!
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

感谢您的使用，欢迎您的指正!
}

>>CS.py Changelog:

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