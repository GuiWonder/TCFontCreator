import subprocess, os

pydir = os.path.abspath(os.path.dirname(__file__))
fontforge='fontforge'
python='python'
python3='python3'
pyfilef=os.path.join(pydir, 'covff.py')
pyfileo=os.path.join(pydir, 'covotfcc.py')

def ckfile(f):
    f=f.strip()
    if not os.path.isfile(f):
        if os.path.isfile(f.strip('"')):
            return f.strip('"')
        elif os.path.isfile(f.strip("'")):
            return f.strip("'")
    return f

print('====中文字体简繁处理工具====\n')
while True:
    infile=str()
    infile2=str()
    outfile=str()
    stmode=str()
    vari='no'
    multi='no'
    jtos=str()
    appused='otfcc'
    enname=str()
    chname=str()
    psname=str()
    version=str()
    while stmode not in {'1', '2', '3', '4', '5', '6', '7', '8'}:
        stmode=input('请选择类型：\n\t1.生成繁体字体\n\t2.生成繁体字体TW\n\t3.生成繁体字体HK\n\t4.生成繁体字体旧字形\n\t5.补全同义字\n\t6.合并简体 GB2312、繁体 GB2312\n\t7.合并字体 1、字体 2\n\t8.日本新字形转为传承正字\n')
    while not os.path.isfile(infile):
        infile=input('请输入字体文件：\n')
        infile=ckfile(infile)
        if not os.path.isfile(infile):
            print('文件不存在，请重新选择！\n')
    if stmode in {'6', '7'}:
        while not os.path.isfile(infile2):
            infile2=input('请输入字体文件2：\n')
            infile2=ckfile(infile2)
            if not os.path.isfile(infile2):
                print('文件不存在，请重新选择！\n')
        infile+='|'+infile2
    while not outfile.strip():
        outfile=input('请输入输出文件：\n')
    if stmode!='5':
        while vari not in {'y', 'n'}:
            vari=input('是否同时补全同义字(输入Y/N)：\n').lower()
        if vari.lower()=='y':
            vari='True'
    if stmode=='8':
        while jtos not in {'y', 'n'}:
            jtos=input('是否同转换日本汉字至繁体(输入Y/N)：\n').lower()
        if jtos=='y':
            multi='true'
    if stmode in {'1', '2', '3', '4'}:
        selmulti=str()
        while selmulti not in {'1', '2', '3'}:
            selmulti=input('请选择简繁一对多的处理方式：\n\t1.不处理一对多\n\t2.使用单一常用字\n\t3.使用词汇正确一简对多繁\n')
        if selmulti=='2':
            multi='single'
        elif selmulti=='3':
            multi='multi'
    if stmode in {'1', '2', '3', '4', '5', '6', '7'}:
        selapp=str()
        while selapp not in {'1', '2'}:
            selapp=input('请选择字体处理内核：\n\t1.otfcc\n\t2.FontForge\n')
        if selapp=='2':
            appused='FontForge'
    
    enname=input('请输入新字体名称(英文), 如果不想设置可直接输入回车：\n').strip()
    if enname:
        while not chname:
            chname=input('请输入新字体名称(中文)：\n').strip()
        psname=input('请输入新字体PostScript名称(可忽略)：\n').strip()
        if not psname:
            psname=enname.replace(' ', '')
        while not version:
            version=input('请输入新字体版本：\n').strip()
    if stmode=='1':
        stmode='tc'
    elif stmode=='2':
        stmode='tctw'
    elif stmode=='3':
        stmode='tchk'
    elif stmode=='4':
        stmode='tct'
    elif stmode=='5':
        stmode='var'
    elif stmode=='6':
        stmode='sat'
    elif stmode=='7':
        stmode='faf'
    elif stmode=='8':
        stmode='jt'
    print('正在处理，请耐心等待....\n')
    if appused=='FontForge':
            subprocess.run((fontforge, '-script', pyfilef, infile, outfile, stmode, vari, multi, enname, chname, psname, version))
    else:
        try:
            subprocess.run((python, pyfileo, infile, outfile, stmode, vari, multi, enname, chname, psname, version))
        except FileNotFoundError:
            subprocess.run((python3, pyfileo, infile, outfile, stmode, vari, multi, enname, chname, psname, version))
    print('\n处理完毕。\n')
    otherfont=str()
    while otherfont not in {'y', 'n'}:
        otherfont=input('是否继续处理其他字体？(输入Y/N)：\n').lower()
    if otherfont=='n':
        break
