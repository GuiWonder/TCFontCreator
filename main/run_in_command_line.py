import subprocess, os

pydir = os.path.abspath(os.path.dirname(__file__))
fontforge='fontforge'
pyfile=os.path.join(pydir, 'covff.py')

while True:
    infile=str()
    outfile=str()
    stmode=str()
    vari=str()
    multi=str()
    enname=str()
    chname=str()
    psname=str()
    version=str()
    while not os.path.isfile(infile):
        infile=input('请输入字体文件：\n')
        if not os.path.isfile(infile):
            print('文件不存在，请重新选择！\n')
    while not outfile.strip():
        outfile=input('请输入输出文件：\n')
    while stmode not in {'1', '2', '3', '4', '5'}:
        stmode=input('请选择类型：\n1.生成繁体\t2.生成繁体TW\t3.生成繁体HK\t4.生成繁体旧字形\t5.补全同义字\n')
    if stmode=='5':
        vari='no'
        multi='no'
    else:
        while vari.lower() not in {'y', 'n'}:
            vari=input('是否同时补全同义字(输入Y/N)：\n')
        while multi not in {'1', '2', '3'}:
            multi=input('请选择简繁一对多的处理方式：\n1.不处理一对多\t2.使用单一常用字\t3.使用词汇正确一简对多繁\n')
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
    else:
        stmode='var'
    if vari.lower()=='y':
        vari='True'
    else:
        vari='no'
    if multi=='2':
        multi='single'
    elif multi=='3':
        multi='multi'
    else:
        multi='no'
    print('正在处理，请耐心等待....\n')
    #print(infile, outfile, stmode, vari, multi, enname, chname, psname, version)
    subprocess.run((fontforge, '-script', pyfile, infile, outfile, stmode, vari, multi, enname, chname, psname, version))
    print('\n处理完毕。\n')
    otherfont=str()
    while otherfont.lower() not in {'y', 'n'}:
        otherfont=input('是否继续处理其他字体？输入“Y”(是)或“N”(否)：\n')
    if otherfont.lower()=='n':
        break
