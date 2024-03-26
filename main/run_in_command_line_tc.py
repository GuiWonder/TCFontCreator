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

print('====中文字型簡繁處理工具====\n')
while True:
	args=list()
	infile=str()
	outfile=str()
	while not os.path.isfile(infile):
		infile=ckfile(input('請輸入要處理的字型路徑（或拖入檔案）：\n'))
		if not os.path.isfile(infile):
			print('檔案不存在，請重新選擇！\n')
	while not outfile.strip():
		outfile=input('請輸入輸出檔案：\n')
		outfile=outfile.strip('"').strip("'")
	appused=str()
	while appused not in ('otfcc', 'FontForge'):
		selapp=input('請選擇字型處理核心：\n\t1.otfcc\n\t2.FontForge\n')
		if selapp=='1': appused='otfcc'
		if selapp=='2': appused='FontForge'
	args+=['-i', infile]
	args+=['-o', outfile]
	awks={'1':'00', '2':'01', '3':'10', '4':'11', '5':'12'}
	awk=str()
	while awk not in awks.keys():
		awk=input('請選擇處理方式：\n\t1.生成簡轉繁字型\n\t2.生成繁轉簡字型\n\t3.從其他字型補入\n\t4.使用字型本身簡繁異體補充字型檔\n\t5.合併簡體與簡入繁出字型\n')
	wk=awks[awk]

	if wk=='00':
		muls={'1':'0', '2':'1', '3':'2', '4':'3'}
		selmulti=str()
		while selmulti not in muls.keys():
			selmulti=input('請選擇一簡多繁處理方式：\n\t1.不處理一簡多繁\n\t2.使用單一常用字\n\t3.使用詞彙動態匹配\n\t4.使用臺灣詞彙動態匹配\n')
		wk+=muls[selmulti]
		if selmulti=='4':
			wk+='1'
		else:
			stvs={'1':'0', '2':'1', '3':'2', '4':'3'}
			stvar=str()
			while stvar not in stvs.keys():
				stvar=input('請選擇繁體異體字：\n\t1.預設\n\t2.臺灣\n\t3.香港\n\t4.舊字形\n')
			wk+=stvs[stvar]
	if wk=='01': wk='0100'
	args+=['-wk', wk]
	
	if wk.startswith('0'):
		vari=str()
		while vari not in {'y', 'n'}:
			vari=input('是否同時完成同義字補全字型檔(輸入Y/N)：\n').lower()
		if vari=='y':
			args.append('-v')
	
	if wk=='10':
		ft2list=list()
		i=1
		while True:
			fl=str()
			ipt=f'請輸入要補入的第{str(i)}個字型的路徑（或拖入檔案）'
			if i>1:ipt+='，若不想繼續新增，可直接輸入 Enter。\n'
			else:ipt+='：\n'
			fl=input(ipt)
			if not fl and len(ft2list)>0: break
			fl=ckfile(fl)
			if not os.path.isfile(fl):
				print('檔案不存在，請重新選擇！\n')
			else:
				ft2list.append(fl)
				i+=1
		for ftin2 in ft2list:
			args+=['-i2', ftin2]
	
	if wk=='12':
		infile2=str()
		while not os.path.isfile(infile2):
			infile2=ckfile(input('要補入的簡入繁出字型：\n'))
			if not os.path.isfile(infile2):
				print('檔案不存在，請重新選擇！\n')
		args+=['-i2', infile2]

	if wk.startswith('1'):
		vari=str()
		while vari not in {'y', 'n'}:
			vari=input('是否移除 hingting (輸入Y/N)：\n').lower()
		if vari=='y':
			args.append('-ih')

	enname=input('請輸入新字型名稱(英文), 如果不想設定可直接輸入 Enter：\n').strip()
	if enname:
		args+=['-n', enname]
		tcname=input('請輸入新字型繁體中文名稱(可忽略)：\n').strip()
		scname=input('請輸入新字型簡體中文名稱(可忽略)：\n').strip()
		version=input('請輸入新字版本號：\n').strip()
		if tcname: args+=['-n1', tcname]
		if scname: args+=['-n2', scname]
		if version: args+=['-n3', version]

	print('正在處理，請稍後...\n')
	if appused=='FontForge':
		subprocess.run(tuple([fontforge, '-script', pyfilef]+args))
	else:
		try:
			subprocess.run(tuple([python, pyfileo]+args))
		except FileNotFoundError:
			subprocess.run(tuple([python3, pyfileo]+args))
	print('\n處理完畢。\n')
	otherfont=str()
	while otherfont not in {'y', 'n'}:
		otherfont=input('是否繼續處理其他字型？(輸入Y/N)：\n').lower()
	if otherfont=='n':
		break
