import subprocess, os

pydir = os.path.abspath(os.path.dirname(__file__))
fontforge='fontforge'
python='python'
python3='python3'
pyfilef=os.path.join(pydir, 'convertf.py')
pyfileo=os.path.join(pydir, 'converto.py')

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
	args=list()
	infile=str()
	outfile=str()
	while not os.path.isfile(infile):
		infile=ckfile(input('请输入要处理的字体路径（或拖入文件）：\n'))
		if not os.path.isfile(infile):
			print('文件不存在，请重新选择！\n')
	while not outfile.strip():
		outfile=input('请输入输出文件：\n')
		outfile=outfile.strip('"').strip("'")
	appused=str()
	while appused not in ('otfcc', 'FontForge'):
		selapp=input('请选择字体处理内核：\n\t1.otfcc\n\t2.FontForge\n')
		if selapp=='1': appused='otfcc'
		if selapp=='2': appused='FontForge'
	args+=['-i', infile]
	args+=['-o', outfile]
	awks={'1':'00', '2':'01', '3':'10', '4':'11', '5':'12'}
	awk=str()
	while awk not in awks.keys():
		awk=input('请选择处理方式：\n\t1.生成简转繁字体\n\t2.生成繁转简字体\n\t3.从其他字体补入\n\t4.使用字体本身简繁异体补充字库\n\t5.合并简体与简入繁出字体\n')
	wk=awks[awk]

	if wk=='00':
		muls={'1':'0', '2':'1', '3':'2', '4':'3'}
		selmulti=str()
		while selmulti not in muls.keys():
			selmulti=input('请选择一简多繁处理方式：\n\t1.不处理一简多繁\n\t2.使用单一常用字\n\t3.使用词汇动态匹配\n\t4.使用台湾词汇动态匹配\n')
		wk+=muls[selmulti]
		if selmulti=='4':
			wk+='1'
		else:
			stvs={'1':'0', '2':'1', '3':'2', '4':'3'}
			stvar=str()
			while stvar not in stvs.keys():
				stvar=input('请选择繁体异体字：\n\t1.预设\n\t2.台湾\n\t3.香港\n\t4.旧字形\n')
			wk+=stvs[stvar]
	if wk=='01': wk='0100'
	args+=['-wk', wk]
	
	if wk.startswith('0'):
		vari=str()
		while vari not in {'y', 'n'}:
			vari=input('是否同时完成同义字补全字库(输入Y/N)：\n').lower()
		if vari=='y':
			args.append('-v')
	
	if wk=='10':
		ft2list=list()
		i=1
		while True:
			fl=str()
			ipt=f'请输入要补入的第{str(i)}个字体的路径（或拖入文件）'
			if i>1:ipt+='，若不想继续添加，可直接输入 Enter。\n'
			else:ipt+='：\n'
			fl=input(ipt)
			if not fl and len(ft2list)>0: break
			fl=ckfile(fl)
			if not os.path.isfile(fl):
				print('文件不存在，请重新选择！\n')
			else:
				ft2list.append(fl)
				i+=1
		for ftin2 in ft2list:
			args+=['-i2', ftin2]
	
	if wk=='12':
		infile2=str()
		while not os.path.isfile(infile2):
			infile2=ckfile(input('要补入的简入繁出字体：\n'))
			if not os.path.isfile(infile2):
				print('文件不存在，请重新选择！\n')
		args+=['-i2', infile2]

	if wk.startswith('1'):
		vari=str()
		while vari not in {'y', 'n'}:
			vari=input('是否移除 hingting (输入Y/N)：\n').lower()
		if vari=='y':
			args.append('-ih')

	enname=input('请输入新字体名称(英文), 如果不想设置可直接输入 Enter：\n').strip()
	if enname:
		args+=['-n', enname]
		tcname=input('请输入新字体繁体中文名称(可忽略)：\n').strip()
		scname=input('请输入新字体简体中文名称(可忽略)：\n').strip()
		version=input('请输入新字版本号：\n').strip()
		if tcname: args+=['-n1', tcname]
		if scname: args+=['-n2', scname]
		if version: args+=['-n3', version]

	print('正在处理，请稍后...\n')
	if appused=='FontForge':
		subprocess.run(tuple([fontforge, '-script', pyfilef]+args))
	else:
		try:
			subprocess.run(tuple([python, pyfileo]+args))
		except FileNotFoundError:
			subprocess.run(tuple([python3, pyfileo]+args))
	print('\n处理完毕。\n')
	otherfont=str()
	while otherfont not in {'y', 'n'}:
		otherfont=input('是否继续处理其他字体？(输入Y/N)：\n').lower()
	if otherfont=='n':
		break
