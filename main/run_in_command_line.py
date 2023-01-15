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
	awks={'1':'st', '2':'var', '3':'sat', '4':'faf', '5':'jt', '6':'ts'}
	stmode=str()
	while stmode not in awks.keys():
		stmode=input('请选择类型：\n\t1.生成简转繁字体\n\t2.使用同义字补全字库\n\t3.合并简体 GB2312、繁体 GB2312\n\t4.合并字体 1、字体 2\n\t5.日本新字形转为传承正字\n\t6.生成繁转简字体\n')
	wk=awks[stmode]
	infile=str()
	while not os.path.isfile(infile):
		infile=ckfile(input('请输入字体文件：\n'))
		if not os.path.isfile(infile):
			print('文件不存在，请重新选择！\n')
	args+=['-i', infile]
	if wk in ("sat", "faf"):
		infile2=str()
		while not os.path.isfile(infile2):
			infile2=ckfile(input('请输入字体文件2：\n'))
			if not os.path.isfile(infile2):
				print('文件不存在，请重新选择！\n')
		args+=['-i2', infile2]
	outfile=str()
	while not outfile.strip():
		outfile=input('请输入输出文件：\n')
	args+=['-o', outfile]
	if wk!='var':
		vari=str()
		while vari not in {'y', 'n'}:
			vari=input('是否同时完成同义字补全字库(输入Y/N)：\n').lower()
		if vari=='y':
			args.append('-v')
	if wk=='st':
		stvs={'1':'', '2':'tw', '3':'hk', '4':'cl'}
		stvar=str()
		while stvar not in stvs.keys():
			stvar=input('请选择繁体异体字：\n\t1.默认\n\t2.台湾\n\t3.香港\n\t4.旧字形\n')
		wk+=stvs[stvar]
		selmulti=str()
		while selmulti not in {'1', '2', '3'}:
			selmulti=input('请选择简繁一对多的处理方式：\n\t1.不处理一对多\n\t2.使用单一常用字\n\t3.使用词汇正确一简对多繁\n')
		if selmulti=='2':
			wk+='.s'
		elif selmulti=='3':
			wk+='.m'
	args+=['-wk', wk]
	appused=str()
	while appused not in ('otfcc', 'FontForge'):
		selapp=input('请选择字体处理内核：\n\t1.otfcc\n\t2.FontForge\n')
		if selapp=='1': appused='otfcc'
		if selapp=='2': appused='FontForge'
	enname=input('请输入新字体名称(英文), 如果不想设置可直接输入回车：\n').strip()
	if enname:
		args+=['-n', enname]
		tcname=input('请输入新字体繁体中文名称(可忽略)：\n').strip()
		scname=input('请输入新字体简体中文名称(可忽略)：\n').strip()
		version=input('请输入新字版本号：\n').strip()
		if tcname: args+=['-ntc', tcname]
		if scname: args+=['-nsc', scname]
		if version: args+=['-vn', version]
	print('正在处理，请耐心等待....\n')
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
