import sys, os
import fontforge
from itertools import chain
pydir = os.path.abspath(os.path.dirname(__file__))
def getmulchar(allch):
	s = str()
	with open(os.path.join(pydir, 'datas/STMulti1.txt'), 'r', encoding = 'utf-8') as f:
		for line in f.readlines():
			litm=line.split('#')[0].strip()
			if not litm: continue
			s += litm
	if not allch: return s
	with open(os.path.join(pydir, 'datas/STMulti2.txt'), 'r', encoding = 'utf-8') as f:
		for line in f.readlines():
			litm=line.split('#')[0].strip()
			if not litm: continue
			s += litm
	return s
def addvariants(font):
	print('Processing font variants...')
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
	print('Removing glyghs...')
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
def fontaddfont(font, fin2, gb=False):
	print('Loading font2...')
	code_glyph, glyph_codes=getallcodesname(font)
	font2 = fontforge.open(fin2)
	if font2.is_cid:
		print('Warning: This is a CID font, we need to FLATTEN it!')
		font2.cidFlatten()
	font2.reencode("unicodefull")
	font2.em = font.em
	print('Getting glyph2 codes')
	code_glyph2, glyph_codes2=getallcodesname(font2)
	if gb:
		print('Adding font2 codes...')
		with open(os.path.join(pydir, 'datas/Variants.txt'),'r',encoding = 'utf-8') as f:
			for line in f.readlines():
				litm=line.split('#')[0].strip()
				if '\t' not in litm: continue
				vari = litm.split('\t')
				codein = 0
				for ch1 in vari:
					if ord(ch1) in code_glyph2.keys():
						codein = ord(ch1)
						break
				if codein != 0:
					for ch1 in vari:
						if ord(ch1) not in code_glyph2.keys():
							gname=code_glyph2[codein]
							glyph_codes2[gname].append(ord(ch1))
							code_glyph2[ord(ch1)] = gname
		print('Adding glyphs...')
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
		print('Adding glyphs...')
		code_codes2 = {}
		for n2 in glyph_codes2.keys():
			lc = [ac1 for ac1 in glyph_codes2[n2] if ac1 not in code_glyph]
			if len(lc) > 0:
				code_codes2[lc[0]] = lc[1:]
		font2.selection.select(*code_codes2.keys())
		font2.copy()
		font.selection.select(*code_codes2.keys())
		font.paste()
		print('Adding extra codings...')
		for cd1 in code_codes2.keys():
			if len(code_codes2[cd1]) > 0:
				font[cd1].altuni = code_codes2[cd1]
		del code_codes2
	del glyph_codes2
	del code_glyph2
	font2.close()
def jptotr(font):
	print('Processing Japanese Kanji...')
	code_glyph, glyph_codes=getallcodesname(font)
	tv = dict()
	with open(os.path.join(pydir, 'datas/uvs-jp-MARK.txt'), 'r', encoding='utf-8') as f:
		for line in f.readlines():
			litm=line.split('#')[0].strip()
			if litm.endswith('X'):
				a = litm.split(' ')
				tv[ord(a[0])] = int(a[3].strip('X'), 16)
	ltb=list()
	for gls in font.glyphs():
		if gls.altuni != None:
			for alt in gls.altuni:
				if alt[1] > 0:
					if alt[0] in tv and tv[alt[0]] == alt[1]:
						ltb.append((gls.glyphname, alt[0]))
	if len(ltb)<1:
		raise RuntimeError('This font is not applicable!')
	for t1 in ltb:
		unimvtogly(font, code_glyph, glyph_codes, t1[1], t1[0])
def unimvtogly(font, code_glyph, glyph_codes, uni, gly):
	if code_glyph[uni]==gly:
		return
	rmcode(font, code_glyph, glyph_codes, code_glyph[uni], uni)
	adduni(font, code_glyph, glyph_codes, gly, uni)
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
def stts(font, wkon, vr=False):
	tabset=wkon.split('.')
	tabch=tabset[0]
	chardic, vardic, wddic=dict(), dict(), dict()
	mulp, locset, mulchar=str(), str(), str()
	if tabch=='st':
		locset, mulp=tabset[1], tabset[2]
		if mulp!='s':
			mulchar = getmulchar(mulp == "m")
		if mulp=='m' and locset in ['tw', 'twp'] and '么' not in mulchar:
			mulchar+='么'
	chardic=getdictxt('Chars_'+tabch)
	if locset in ['tw', 'hk', 'cl', 'twp']:
		if locset=='twp':vardic=getdictxt('Var_tw')
		else: vardic=getdictxt('Var_'+locset)
		for ch in vardic.keys():
			if ch not in chardic.values():
				chardic[ch]=vardic[ch]
		for ch in list(chardic.keys()):
			if chardic[ch] in vardic:
				chardic[ch]=vardic[chardic[ch]]
	if tabch == 'ts' or mulp == "m":
		phrases=f'datas/{tabch.upper()}Phrases.txt'
		with open(os.path.join(pydir, phrases),'r',encoding = 'utf-8') as f:
			for line in f.readlines():
				s, t=linesplit(line, '\t')
				if not(s and t): continue
				if locset in ['tw', 'hk', 'cl', 'twp']:
					t=varck(t, vardic)
				wddic[s]=t
		if locset=='twp':
			with open(os.path.join(pydir, 'datas/TWPhrases.txt'),'r',encoding = 'utf-8') as f:
				for line in f.readlines():
					s, t=linesplit(line, '\t')
					if not(s and t): continue
					if len(s)==1 and len(t)==1:
						chardic[s]=t
					else:
						wddic[s]=t
	mapts(font, chardic, mulchar)
	if mulp == "m":
		removeglyhps(font)
		if vr: addvariants(font)
	code_glyph, glyph_codes=getallcodesname(font)
	if tabch == 'ts' or mulp == "m":
		print('Check font lookups...')
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
	nwk['inFilePath'], nwk['outFilePath'], nwk['outFilePath2'], nwk['enN'], nwk['scN'], nwk['tcN'], nwk['vsN']=(str() for i in range(7))
	nwk['varit'], nwk['toST'], nwk['toTS'], nwk['jpCL'], nwk['rmUN']=(False for i in range(5))
	argn = len(args)
	i = 0
	while i < argn:
		arg  = args[i]
		i += 1
		if arg == "-o":
			nwk['outFilePath'] = args[i]
			i += 1
		elif arg == "-i":
			nwk['inFilePath'] = args[i]
			i += 1
		elif arg == "-i2":
			nwk['inFilePath2'] = args[i]
			i += 1
		elif arg == "-wk":
			nwk['work'] = args[i]
			i += 1
		elif arg == "-v":
			nwk['varit'] = True
		elif arg == "-n":
			nwk['enN'] = args[i]
			i += 1
		elif arg == "-nsc":
			nwk['scN'] = args[i]
			i += 1
		elif arg == "-ntc":
			nwk['tcN'] = args[i]
			i += 1
		elif arg == "-vn":
			nwk['vsN'] = args[i]
			i += 1
		else:
			raise RuntimeError("Unknown option '%s'." % (arg))
	if not nwk['inFilePath']:
		raise RuntimeError("You must specify one input font.")
	if not nwk['outFilePath']:
		raise RuntimeError("You must specify one output font.")
	if nwk['work'] in ("sat", "faf") and not nwk['inFilePath2']:
		raise RuntimeError("You must specify one input font2.")
	if not nwk['enN'] and (nwk['tcN'] or nwk['scN'] or nwk['vsN']):
		raise RuntimeError("You must specify English name first.")
	return nwk
def run(args):
	wkfl=parseArgs(args)
	print('Loading font...')
	infont=fontforge.open(wkfl['inFilePath'])
	if infont.is_cid:
		print('Warning: this is a CID font, we need to FLATTEN it!')
		infont.cidFlatten()
	infont.reencode("unicodefull")
	if wkfl['work'] in ("sat", "faf"):
		fontaddfont(infont, wkfl['inFilePath2'], wkfl['work']=="sat")
	if wkfl['work']=='jt':
		jptotr(infont)
	if wkfl['work']=="var" or wkfl['varit']:
		addvariants(infont)
	if wkfl['work'].split('.')[0] in ("st", "ts"):
		stts(infont, wkfl['work'], wkfl['varit'])
	if wkfl['enN']:
		setnm(infont, wkfl['enN'], wkfl['tcN'], wkfl['scN'], wkfl['vsN'])
	print('Saving font...')
	infont.generate(wkfl['outFilePath'])
	print('Finished!')
def main():
	run(sys.argv[1:])
if __name__ == "__main__":
	main()
