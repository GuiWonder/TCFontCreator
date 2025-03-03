import sys, os
import fontforge
from itertools import chain

pydir = os.path.abspath(os.path.dirname(__file__))

def addvariants(font):
	print('Processing variant characters...')
	code_glyph, glyph_codes=getallcodesname(font)
	with open(os.path.join(pydir, 'datas/Variants.txt'), 'r', encoding = 'utf-8') as f:
		for line in f.readlines():
			litm=line.split('#')[0].strip()
			if '\t' not in litm: continue
			vari = litm.split('\t')
			codein = 0
			for ch1 in vari:
				chcode = ord(ch1)
				if chcode in code_glyph:
					codein = chcode
					break
			if codein != 0:
				for ch1 in vari:
					chcode = ord(ch1)
					if chcode not in code_glyph:
						mvcodetocode(font, code_glyph, glyph_codes, chcode, codein)

def mvcodetocode(font, code_glyph, glyph_codes, uni, unito):
	if unito not in code_glyph:
		return
	gto=code_glyph[unito]
	if uni in code_glyph:
		gf=code_glyph[uni]
		if gf==gto:
			return
		rmcode(font, code_glyph, glyph_codes, gf, uni)
	adduni(font, code_glyph, glyph_codes, gto, uni)

def rmcode(font, code_glyph, glyph_codes, gly, uni):
	glyph_codes[gly].remove(uni)
	del code_glyph[uni]
	gl=font[gly]
	lu=list()
	if len(glyph_codes[gly])<1:
		if gl.unicode==uni:
			gl.unicode=-1
			return
		gl.unicode=-1
		if gl.altuni!=None:
			for alt in gl.altuni:
				if alt[1] > 0:
					lu.append(alt)
	else:
		gl.unicode=glyph_codes[gly][0]
		if gl.altuni!=None:
			for alt in gl.altuni:
				if alt[1] > 0:
					lu.append(alt)
		for u1 in glyph_codes[gly][1:]:
			lu.append((u1, -1, 0))
	if len(lu) > 0:
		gl.altuni = tuple(lu)
	else:
		gl.altuni = None

def adduni(font, code_glyph, glyph_codes, gly, uni):
	glyph_codes[gly].append(uni)
	code_glyph[uni]=gly
	if font[gly].unicode<0:
		font[gly].unicode=uni
	else:
		lu=list()
		if font[gly].altuni != None:
			for alt in font[gly].altuni:
				lu.append(alt)
		lu.append((uni, -1, 0))
		font[gly].altuni = tuple(lu)

def removeglyhps(font):
	print('Cleaning up glyphs...')
	code_glyph, glyph_codes=getallcodesname(font)
	alcodes = set(chain(
		range(0x0000, 0x007F),
		range(0x02B0, 0x0300),
		range(0x2000, 0x2050),
		range(0x2100, 0x2150),
		range(0x3000, 0x301D),
		range(0x3100, 0x3130),
		range(0x31A0, 0x31E3),
		range(0xFE10, 0xFE20),
		range(0xFE30, 0xFE50),
		range(0xFF01, 0xFF66)
	))
	with open(os.path.join(pydir, 'datas/UsedChar.txt'), 'r', encoding = 'utf-8') as f:
		for line in f.readlines():
			litm=line.split('#')[0].strip()
			if litm: alcodes.add(ord(litm))
	useg=set()
	for gls in font.glyphs():
		if gls.glyphname in ('.notdef', '.null', 'nonmarkingreturn', 'NULL', 'NUL'):
			useg.add(gls.glyphname)
		elif len(set(glyph_codes[gls.glyphname]).intersection(alcodes)) > 0:
			useg.add(gls.glyphname)
	reget = set()
	for gly in useg:
		tg = font[gly].getPosSub('*')
		if len(tg) > 0:
			for t1 in tg:
				if t1[1] == 'Substitution' and t1[2] not in useg:
					reget.add(t1[2])
	useg.update(reget)
	for gls in font.glyphs():
		if gls.glyphname not in useg:
			gls.removePosSub('*')
			font.removeGlyph(gls)

def getlklan(font):
	lans=list()
	for lk in font.gsub_lookups:
		lkif=font.getLookupInfo(lk)
		if len(lkif)>2 and len(lkif[2])>0:
			for lan in lkif[2][0][1]:
				if lan not in lans: lans.append(lan)
	return lans

def addlookupsword(font, code_glyph, tcword, scword, j, i):
	newgname = 'ligast' + i
	wdin = list()
	wdout = list()
	for s1 in scword:
		try:
			glys = font[code_glyph[ord(s1)]]
		except TypeError:
			print('Skip ' + s1)
			return
		wdin.append(glys.glyphname)
	for t1 in tcword:
		try:
			glyt = font[code_glyph[ord(t1)]]
		except TypeError:
			print('Skip ' + t1)
			return
		wdout.append(glyt.glyphname)
	newg = font.createChar(-1, newgname)
	newg.width = 1000
	newg.vwidth = 800
	newg.addPosSub('stliga' + j, tuple(wdin))
	newg.addPosSub('stmult' + j, tuple(wdout))

def getallcodesname(thfont):
	c_g = dict()
	g_c=dict()
	for gls in thfont.glyphs():
		g_c[gls.glyphname]=list()
		if gls.unicode > -1:
			c_g[gls.unicode]=gls.glyphname
			g_c[gls.glyphname].append(gls.unicode)
		if gls.altuni != None:
			for uni in gls.altuni:
				if uni[1] <= 0:
					c_g[uni[0]] = gls.glyphname
					g_c[gls.glyphname].append(uni[0])
	return c_g, g_c

def mgsg1(font, fin2, gb=False):
	code_glyph, glyph_codes=getallcodesname(font)
	font2 = fontforge.open(fin2)
	if font2.is_cid:
		print('Warning: This is a CID font, we need to FLATTEN it!')
		font2.cidFlatten()
	font2.reencode("unicodefull")
	font2.em = font.em
	code_glyph2, glyph_codes2=getallcodesname(font2)
	if gb:
		addvariants(font2)
		print('Merging glyphs...')
		print('This will take some time...')
		allcodes = set(code_glyph.keys())
		for n2 in glyph_codes2.keys():
			scds=set(glyph_codes2[n2])
			if not scds.issubset(allcodes):
				sdcs = scds.difference(allcodes)
				gcs = list(sdcs)
				font2.selection.select(n2)
				font2.copy()
				font.selection.select(gcs[0])
				font.paste()
				font[gcs[0]].unicode = gcs[0]
				if len(gcs)>1:
					font[gcs[0]].altuni = gcs[1:]
				allcodes.update(sdcs)
	else:
		print('Merging glyphs...')
		code_codes2 = {}
		for n2 in glyph_codes2.keys():
			lc = [ac1 for ac1 in glyph_codes2[n2] if ac1 not in code_glyph]
			if len(lc) > 0:
				code_codes2[lc[0]] = lc[1:]
		font2.selection.select(*code_codes2.keys())
		font2.copy()
		font.selection.select(*code_codes2.keys())
		font.paste()
		for cd1 in code_codes2.keys():
			if len(code_codes2[cd1]) > 0:
				font[cd1].altuni = code_codes2[cd1]
		del code_codes2
	del glyph_codes2
	del code_glyph2
	font2.close()

def mgft(font, ftfls, gb=False):
	for ftfl in ftfls:
		print('Merge font', ftfl)
		mgsg1(font, ftfl, gb)

def mapts(font, maindic, ignch):
	code_glyph, glyph_codes=getallcodesname(font)
	for ch in maindic.keys():
		if ch in ignch: continue
		cdto=ord(maindic[ch])
		if cdto in code_glyph:
			mvcodetocode(font, code_glyph, glyph_codes, ord(ch), cdto)

def checklk(font):
	lantgs=getlklan(font)
	for lantg in ('DFLT', 'hani', 'latn'):
		if (lantg, ('dflt',)) not in lantgs:
			lantgs.append((lantg, ('dflt',)))
	font.addLookup('stchar', 'gsub_single', None, (("ccmp", tuple(lantgs)), ))
	font.addLookup('stmult', 'gsub_multiple', None, (("ccmp", tuple(lantgs)), ), 'stchar')
	font.addLookup('stliga', 'gsub_ligature', None, (("ccmp", tuple(lantgs)), ))
	font.addLookupSubtable('stchar', 'stchar1')

def linesplit(l, ch):
	litm=l.split('#')[0].strip().split(' ')[0]
	if ch not in litm: return '', ''
	lnst=litm.split(ch)
	return lnst[0].strip(), lnst[1].strip()

def getdictxt(tabnm):
	txtdic=dict()
	with open(os.path.join(pydir, f'datas/{tabnm}.txt'),'r',encoding = 'utf-8') as f:
		for line in f.readlines():
			s, t=linesplit(line, '\t')
			if s and t and s != t:
				txtdic[s]=t
	return txtdic

def varck(text, vardic):
	for ch in vardic.keys():
		text=text.replace(ch, vardic[ch])
	return text

def getstmul(wkon):
	str1=str()
	if wkon[1]!='0' or wkon[2]=='1':return ''
	stfls=list()
	stfls.append('STMulti1.txt')
	if wkon[2]!='0':stfls.append('STMulti2.txt')
	for stfl in stfls:
		with open(os.path.join(pydir, 'datas/'+stfl), 'r', encoding = 'utf-8') as f:
			for line in f.readlines():
				litm=line.split('#')[0].strip()
				if litm: str1+=litm
	if (wkon[2]=='3' or wkon[3]=='1') and '么' not in str1:
		str1+='么'
	return str1

def stts(font, wkon, vr=False):
	tabch=['st', 'ts'][int(wkon[1])]
	locset, mulset=str(), str()
	if tabch=='st':
		mulset=wkon[2]
		if mulset=='3':
			locset='tw'
		else:
			locset=['', 'tw', 'hk', 'cl'][int(wkon[3])]
	mulchar= getstmul(wkon)
	chardic=getdictxt('Chars_'+tabch)
	vardic=dict()
	if locset:
		vardic=getdictxt('Var_'+locset)
		for ch in vardic.keys():
			if ch not in chardic.values():
				chardic[ch]=vardic[ch]
		for ch in list(chardic.keys()):
			if chardic[ch] in vardic:
				chardic[ch]=vardic[chardic[ch]]

	wddic=dict()
	if tabch == 'ts' or mulset in ['2', '3']:
		phrases=f'datas/{tabch.upper()}Phrases.txt'
		with open(os.path.join(pydir, phrases),'r',encoding = 'utf-8') as f:
			for line in f.readlines():
				s, t=linesplit(line, '\t')
				if not(s and t): continue
				if locset in ['tw', 'hk', 'cl']:
					t=varck(t, vardic)
				wddic[s]=t
		if mulset=='3':
			with open(os.path.join(pydir, 'datas/TWPhrases.txt'),'r',encoding = 'utf-8') as f:
				for line in f.readlines():
					s, t=linesplit(line, '\t')
					if not(s and t): continue
					if len(s)==1 and len(t)==1:
						chardic[s]=t
					else:
						wddic[s]=t


	mapts(font, chardic, mulchar)
	if mulset in ['2', '3']:
		removeglyhps(font)
		if vr: addvariants(font)
	code_glyph, glyph_codes=getallcodesname(font)

	if tabch == 'ts' or mulset in ['2', '3']:
		print('Checking lookup tables...')
		checklk(font)
		if tabch=='ts':
			ftdic=getdictxt('Chars_tsm')
		else:
			ftdic=dict()
			for ch in chardic.keys():
				if ch in mulchar:
					ftdic[ch]=chardic[ch]
			if locset in ['tw', 'twp']:
				ftdic['么']='麼'
				ftdic['幺']='么'
		for ch in ftdic.keys():
			cd1, cd2=str(ord(ch)), str(ord(ftdic[ch]))
			if cd1 in code_glyph and cd2 in code_glyph:
				gntc = code_glyph[cd2]
				gnsc = code_glyph[cd1]
				if gntc != gnsc:
					font[gnsc].addPosSub('stchar1', gntc)
		stword = list()
		ccods=set(code_glyph.keys())
		for wd in wddic.keys():
			s, t=wd, wddic[wd]
			codestc = set(ord(c) for c in s+t)
			if codestc.issubset(ccods):
				stword.append((s, t))
		if len(stword) > 0:
			sumf = sum(1 for _ in font.glyphs())
			if len(stword) + sumf > 65535:
				raise RuntimeError('Not enough glyph space! You need ' + str(len(stword) + sumf - 65535) + ' more glyph space!')
			stword.sort(key=lambda x:len(x[0]), reverse = True)
			i, j, tlen, wlen = 0, 0, 0, len(stword[0][0])
			font.addLookupSubtable('stmult', 'stmult0')
			font.addLookupSubtable('stliga', 'stliga0')
			for wd in stword:
				tlen += len(wd[0] + wd[1])
				wlen2 = len(stword[i][0])
				if tlen >= 20000 or wlen2 < wlen:
					tlen = 0
					wlen = wlen2
					j += 1
					font.addLookupSubtable('stmult', 'stmult' + str(j), 'stmult' + str(j - 1))
					font.addLookupSubtable('stliga', 'stliga' + str(j), 'stliga' + str(j - 1))
				i += 1
				addlookupsword(font, code_glyph, wd[1], wd[0], str(j), str(i))

def setnm(font, ennm, tcnm='', scnm='', versn=''):
	print('Processing font name...')
	wt=str()
	for n1 in font.sfnt_names:
		if n1[0] == 'English (US)' and n1[1] == 'SubFamily':
			wt = n1[2]
		elif n1[0] == 'English (US)' and n1[1] == 'Preferred Styles':
			wt = n1[2]
			break
	if wt.lower() in ('regular', 'bold', 'italic', 'bold italic'):
		wt=wt.title()
	isit='Italic' in wt
	wt=wt.replace('Italic', '').strip()
	if not wt: wt='Regular'
	itml, itm=str(), str()
	if isit: itml, itm=' Italic', 'It'
	if not versn:
		if font.sfntRevision:
			versn='{:.2f}'.format(font.sfntRevision)
		else:
			print('No sfntRevision.')
			versn='1.00'
	else:
		font.sfntRevision = float(versn)
	fmlName=ennm
	ftName=ennm
	ftNamesc=scnm
	ftNametc=tcnm
	if wt not in ('Regular', 'Bold'):
		ftName+=' '+wt
		ftNamesc+=' '+wt
		ftNametc+=' '+wt
	subfamily='Regular'
	if isit:
		if wt=='Bold':
			subfamily='Bold Italic'
		else:
			subfamily='Italic'
	elif wt=='Bold':
		subfamily='Bold'
	psName=fmlName.replace(' ', '')+'-'+wt+itm
	uniqID=versn+';'+psName
	if wt=='Bold':
	#if wt in ('Regular', 'Bold') and not (isit and wt=='Regular'):
		fullName=ftName+' '+wt+itml
		fullNamesc=ftNamesc+' '+wt+itml
		fullNametc=ftNametc+' '+wt+itml
	else:
		fullName=ftName+itml
		fullNamesc=ftNamesc+itml
		fullNametc=ftNametc+itml
	newname=list()
	newname+=[
		('English (US)', 'Family', ftName), 
		('English (US)', 'SubFamily', subfamily), 
		('English (US)', 'UniqueID', uniqID), 
		('English (US)', 'Fullname', fullName), 
		('English (US)', 'Version', 'Version '+versn), 
		('English (US)', 'PostScriptName', psName), 
	]
	if wt not in ('Regular', 'Bold'):
		newname+=[
			('English (US)', 'Preferred Family', fmlName), 
			('English (US)', 'Preferred Styles', wt+itml), 
		]
	if tcnm:
		for lang in ('Chinese (Taiwan)', 'Chinese (Hong Kong)', 'Chinese (Macau)'):
			newname+=[
			(lang, 'Family', ftNametc), 
			(lang, 'SubFamily', subfamily), 
			(lang, 'Fullname', fullNametc), 
			]
			if wt not in ('Regular', 'Bold'):
				newname+=[
					(lang, 'Preferred Family', tcnm), 
					(lang, 'Preferred Styles', wt+itml), 
				]
	if scnm:
		for lang in ('Chinese (PRC)', 'Chinese (Singapore)'):
			newname+=[
			(lang, 'Family', ftNamesc), 
			(lang, 'SubFamily', subfamily), 
			(lang, 'Fullname', fullNamesc), 
			]
			if wt not in ('Regular', 'Bold'):
				newname+=[
					(lang, 'Preferred Family', scnm), 
					(lang, 'Preferred Styles', wt+itml), 
				]
	font.sfnt_names=tuple(newname)

def parseArgs(args):
	nwk=dict()
	cfars=['-i', '-o', '-wk', '-n', '-n1', '-n2', '-n3']
	for arg in cfars:
		nwk[arg]=str()
	nwk['-i2']=list()
	nwk['-v']=False
	nwk['-ih']=False
	argn = len(args)
	i = 0
	while i<argn:
		arg=args[i]
		i+=1
		if arg in cfars:
			nwk[arg]=args[i]
			i+=1
		elif arg=='-i2':
			nwk['-i2'].append(args[i])
			i += 1
		elif arg in ['-v', '-ih']:
			nwk[arg]=True
		else:
			raise RuntimeError("Unknown option '%s'." % (arg))
	if not nwk['-i']:
		raise RuntimeError("You must specify one input font.")
	if not nwk['-o']:
		raise RuntimeError("You must specify one output font.")
	if nwk['-wk'] in ('10', '12') and len(nwk['-i2'])<1:
		raise RuntimeError("You must specify one input font2.")
	return nwk

def run(args):
	wkfl=parseArgs(args)
	print(f'Loading font', wkfl['-i'])
	infont=fontforge.open(wkfl['-i'])
	if infont.is_cid:
		print('Warning: this is a CID font, we need to FLATTEN it!')
		infont.cidFlatten()
	infont.reencode("unicodefull")
	if wkfl['-wk'] in ("10", "12"):
		mgft(infont, wkfl['-i2'], wkfl['-wk']=="12")
	if wkfl['-wk']=="11" or wkfl['-v']:
		addvariants(infont)
	if wkfl['-wk'].startswith('0'):
		stts(infont, wkfl['-wk'], wkfl['-v'])
	if wkfl['-n']:
		setnm(infont, wkfl['-n'], wkfl['-n1'], wkfl['-n2'], wkfl['-n3'])
	print('Saving font', wkfl['-o'])
	if wkfl['-ih']:
		gflags=('opentype', 'omit-instructions',)
		infont.generate(wkfl['-o'], flags=gflags)
	else:
		infont.generate(wkfl['-o'])
	print('Finished!')

def main():
	run(sys.argv[1:])

if __name__ == "__main__":
	main()
