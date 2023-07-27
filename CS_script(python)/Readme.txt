================================
=============CS.py==============
================================
=========Version V2.1.4=========
============20230327============

en-us
{
    Authors: Ren Yabin(zmjt-cn), Yang Bo
    Address: School of Mechanical Engineering, Hebei University of Technology, Tianjin 300401, People's Republic of China
    Emails:  <s1345358@126.com>, <boyang@hebut.edu.cn>
    Webside: https://github.com/zmjt-cn/C-S-Stress-Field

    User Agreement:
    {
        There are a few things you need to know and agree on before you start using this Software (code). Continuing to install this Software(code) means that you have approved the following:
        1. This Software(code) follows the Apache License 2.0 policy.
        2. This Software(code) is free of charge, any organization or individual shall NOT use any content of this Software(code) for commercial activities.
        3. The author owns the copyright of this software(code), please reference the source when using it.
        4. This User Agreement is subject to the latest released version.
    }

    Introduction:
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

        >>Introduction to the parameters of the 'input.dat' file:
            << cellname		sigma_0	iforder	ifthread	ifanimation >>
            POSCAR	POSCAR_new	20	1	0	1
            << ds/epsilon_xz	dds/epsilon_xx	e=absolute_error_range/GPa >>
            0.01	0.002	0.2
            << theta	start	end	rad/*math.pi/means:0pi/12->8pi/12_interval=1pi/12 >>
            1/12	0	8
            0	100	#start&end_step
            mpirun  -np 24  /opt/software/vasp.5.4.4.xxxz/bin/vasp_std >out.log
            mpirun  -np 24  /opt/software/vasp.5.4.4.xz/bin/vasp_std >out.log
            #==================== Parameter Description: ====================
            # This is a necessary input file. Lines starting with '#' are comments, while the other lines denote parameters.
            # ATTENTION: This program applies a compressive-shear biaxial stress field based on VASP software calculation. To use this program successfully, you need to install VASP software locally. This includes the software 'vasp.5.4.4.xxxz' for the unrelaxed strain tensor epsilon_xx and epsilon_xz denoted in line 8, and the software 'vasp.5.4.4.xz' for the unrelaxed strain tensor epsilon_xz denoted in line 9.
            # Line 2 parameter settings: Please do not modify the first two parameters. The third parameter sets the set compressive stress parameter 'sigma_0', with units in GPa. If set to '0', it computes simple shear without compressive stress. The fourth parameter determines whether to perform coordinate transformation on the crystal cell, with '1' denoting convert the crystal plane from z-axis to x-axis. If not needed, set to '0'. Parameters 5 and 6 determine whether to enable double-thread mode and animation archives of CONTCAR, respectively. Set to '1' to enable, or '0' to disable, consistent with the iforder setting.
            # Line 4 parameter settings: The first parameter specifies the increment in 'epsilon_xz' for shear direction and defaults to 0.01. The second parameter denotes the increment in 'epsilon_xx' for compressive direction and defaults to 0.002. The third parameter sets the absolute error limit of the set compressive stress 'sigma_0' at 0.2 GPa.
            # Line 6 parameter settings: The sixth line defines the rotation angle and rotation range of the crystal direction. The 1st parameter, 'theta' (in radians), is set as a fraction. E.g., '1/12' denotes pi/12 (i.e., 15 degrees). The second and third parameters specify the start and end ranges of rotation, e.g., 0 and 8 represents rotates 8 times in total, calculating 9 crystal directions with an interval size of pi/12, starting from 0pi/12 and ending at 8pi/12. Attention: Do not set angles or any parameters in this line to negative values, or the program will report an 'error' while creating folders, which prevents the program from running!!!
            # Line 7 parameter settings: This line denotes the number of steps for initial and final shear strain. It defaults to 0 and 100, respectively. You can set 'start_step' to a non-zero number to continue the previous calculations. For instance, if the first calculation stopped at step 30, you can perform subsequent calculations by extracting the results of Step 30 in the second calculation, instead of starting from 0 again, by setting the 'start_step' to 30. If start and end steps are equal, the program skips shear calculations and proceeds to data extraction.
            # Lines 8 and 9 contain command lines for calling VASP software. The 8th line calls the strain tensor epsilon_xx and epsilon_xz non-relaxation 'vasp.5.4.4.xxxz', whereas the 9th line calls the strain tensor epsilon_xz non-relaxation 'vasp.5.4.4.xz' for calculations involving simple shear stress field and when the compressive stress is set to 0. Modify the statements after '24' based on your software installation location.
            # If you are using a remote supercomputing server, the number of 'cores' in lines 8 and 9 should match those in the PBS file; otherwise, the program may fail to calculate.
    }
    Thank you for using! Feedback is always welcome!
}

zh-cn
{
    作者：任亚斌(zmjt-cn)，杨波
    地址：河北工业大学机械工程学院，天津 300401，中国
    邮箱：<s1345358@126.com>，<boyang@hebut.edu.cn>
    网址：https://github.com/zmjt-cn/C-S-Stress-Field

    用户协议：
    {
        在开始使用本软件(代码)之前，您需要了解并认可一些内容。继续使用本软件(代码)意味着您已认可以下内容：
        1.本软件(代码)遵循Apache License 2.0协议。
        2.本软件(代码)为免费软件(代码)，任何组织或个人不得将软件(代码)的任何内容用于商业行为。
        3.作者享有本软件(代码)著作权，使用请注明来源。
        4.用户协议以最新发布版为准。
    }

    简介：
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

        >>“input.dat”文件的参数介绍：
            << 晶胞名称		sigma_0/单位GPa	是否坐标转换	是否开启双线程	是否开启动画 >>
            POSCAR	POSCAR_new	20	1	0	1
            << ds/epsilon_xz增量=0.01	dds/epsilon_xx增量=0.002	e=绝对误差范围/GPa >>
            0.01	0.002	0.2
            << 旋转角	起始角	终止角	弧度制/*math.pi/表示:0pi/12->8pi/12 间隔1pi/12 >>
            1/12	0	8
            0	100	#起始步与终止步
            mpirun  -np 24  /opt/software/vasp.5.4.4.xxxz/bin/vasp_std >out.log
            mpirun  -np 24  /opt/software/vasp.5.4.4.xz/bin/vasp_std >out.log
            #==================== 参数说明: ====================
            #这个文件是一个必要的输入文件，以#开头的行是注释行，其余的行是参数行。
            #警告：本程序应用的压缩-剪切双轴应力场是基于VASP软件计算的。如果想成功使用这个程序，你需要在本地安装VASP软件，包括第8行表示的应变张量epsilon_xx和epsilon_xz不弛豫的“vasp.5.4.4.xxxz”软件，第9行表示的应变张量epsilon_xz不弛豫的“vasp.5.4.4.xz”软件。
            #   第2行参数设置:请不要修改前两个参数，第3个参数为设定的压缩应力参数“sigma_0”，单位为GPa，如果输入为0，计算为无压缩应力的简单剪切。第4个参数是是否对晶胞进行坐标转换，设置为“1”表示将需要计算的晶面从z轴转换为x轴，如果不需要，设置为“0”。第5和第6个参数是是否开启双线程模式，以及是否开启CONTCAR的动画存档，与是否坐标转换的设置相同，1打开，0关闭。
            #   第4行参数设置:第1个参数为在剪切方向上的应变epsilon_xz的增量，默认为0.01。第2个参数是压缩方向上的应变epsilon_xx的增量，默认为0.002。第3个参数是设定压缩应力sigma_0的绝对误差，设为0.2GPa。
            #   第6行参数设置:第6行是晶向的旋转角度和旋转范围。第1个参数是旋转角度theta，它被设置为一个分数，单位是弧度制。如1/12表示旋转角度是pi/12(即15度)。第2和第3个参数是旋转的开始和结束范围。如设为0和8，表示为从0pi/12开始，以pi/12为间隔旋转，到8pi/12结束，共旋转8次，计算9条晶向。注意：请不要将角度设置为负值，这一行的所有参数都不要设置为负值，否则程序在创建文件夹时会报错，程序将无法运行!!！
            #   第7行参数设置:第7行参数是剪切应变起始和终止的步数。默认起始为0，终止为100。您可以将起始步设置为非0，这意味着该程序将继续上一次的计算。例如，如果第一次计算在30步时停止，您可以在第二次计算中通过提取第30步的结果来执行后续计算，而不是再次从0开始，只需将起始步设置为30。如果起始步和终止步相等，程序将直接跳过剪切计算部分，进行后续的数据提取。
            #   第8行和第9行是调用VASP软件命令行。第8行命令调用应变张量epsilon_xx和epsilon_xz不弛豫的“vasp.5.4.4.xxxz”(用于计算压缩-剪切双轴应力场)，第9行命令调用应变张量epsilon_xz不弛豫的“vasp.5.4.4.xz”(为压应力设为0时的简单剪切应力场计算)。“24”后的语句为调用软件的路径，可根据实际情况进行更改。
            #   如果您使用的是远程超算服务器，第8行和第9行的核数值应该与pbs文件中的核数值相同，否则可能无法计算。
    }
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