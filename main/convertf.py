import sys, os
import fontforge
from itertools import chain
pydir = os.path.abspath(os.path.dirname(__file__))
def getmulchar(allch):
	s = str()
	with open(os.path.join(pydir, 'datas/Multi.txt'), 'r', encoding = 'utf-8') as f:
		for line in f.readlines():
			line = line.strip()
			if not line or line.startswith('##'):
				continue
			if allch:
				s += line.strip('#').strip()
			elif not line.startswith('#'):
				s += line
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
def transforme(font, tabch, mulchar):
	print('Processing Chinese Chars...')
	code_glyph, glyph_codes=getallcodesname(font)
	with open(os.path.join(pydir, f'datas/Chars_{tabch}.txt'), 'r',encoding = 'utf-8') as f:
		for line in f.readlines():
			litm=line.split('#')[0].strip()
			if '\t' not in litm: continue
			lnst=litm.split('\t')
			s, t = lnst[0].strip(), lnst[1].strip()
			if s and t and s != t and (s not in mulchar):
				mvcodetocode(font, code_glyph, glyph_codes, ord(s), ord(t))
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
		range(0x2002, 0x203C),
		range(0x2E00, 0x2F00),
		range(0x3000, 0x301D),
		range(0x3100, 0x3130),
		range(0x3190, 0x31E0),
		range(0xFE10, 0xFE20),
		range(0xFE30, 0xFE50),
		range(0xFF01, 0xFF66)
	))
	with open(os.path.join(pydir, 'datas/Hans.txt'), 'r', encoding = 'utf-8') as f:
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
def ForCharslookups(font, tabch, mulchar):
	code_glyph, glyph_codes=getallcodesname(font)
	font.addLookup('stchar', 'gsub_single', None, (("ccmp",(("hani",("dflt")),)),))
	font.addLookupSubtable('stchar', 'stchar1')
	if tabch=='ts':
		txtfl=['Chars_tsm', ]
	else:
		txtfl=[f'Chars_{tabch}', 'Punctuation']
	for txf in txtfl:
		with open(os.path.join(pydir, f'datas/{txf}.txt'), 'r', encoding = 'utf-8') as f:
			for line in f.readlines():
				litm=line.split('#')[0].strip()
				if '\t' not in litm: continue
				s, t = litm.split('\t')
				s = s.strip()
				t = t.strip()
				if tabch!='ts' and s not in mulchar:continue
				if s and t and s != t and ord(t) in code_glyph and ord(s) in code_glyph:
					gntc = code_glyph[ord(t)]
					gnsc = code_glyph[ord(s)]
					if gntc != gnsc:
						font[gnsc].addPosSub('stchar1', gntc)
def ForWordslookups(font, tabch):
	code_glyph, glyph_codes=getallcodesname(font)
	phrases='datas/STPhrases.txt'
	if tabch=='ts':
		phrases='datas/TSPhrases.txt'
	stword = list()
	with open(os.path.join(pydir, phrases),'r',encoding = 'utf-8') as f:
		ccods=set(code_glyph.keys())
		for line in f.readlines():
			litm=line.split('#')[0].strip()
			litm=litm.split(' ')[0].strip()
			if '\t' not in litm: continue
			s, t = litm.split('\t')
			s = s.strip()
			t = t.strip()
			if not(s and t): continue
			codestc = set(ord(c) for c in s+t)
			if codestc.issubset(ccods):
				stword.append((s, t))
	if len(stword) < 1:
		return
	sumf = sum(1 for _ in font.glyphs())
	if len(stword) + sumf > 65535:
		raise RuntimeError('Not enough glyph space! You need ' + str(len(stword) + sumf - 65535) + ' more glyph space!')
	stword.sort(key=lambda x:len(x[0]), reverse = True)
	font.addLookup('stmult', 'gsub_multiple', None, (("ccmp",(("hani",("dflt")),)),), 'stchar')
	font.addLookup('stliga', 'gsub_ligature', None, (("ccmp",(("hani",("dflt")),)),))
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
	with open(os.path.join(pydir, 'datas/uvs-get-jp1-MARK.txt'), 'r', encoding='utf-8') as f:
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
		raise RuntimeError('This font is not applicable! 此功能不適用這個字體。')
	for t1 in ltb:
		unimvtogly(font, code_glyph, glyph_codes, t1[1], t1[0])
def unimvtogly(font, code_glyph, glyph_codes, uni, gly):
	if code_glyph[uni]==gly:
		return
	rmcode(font, code_glyph, glyph_codes, code_glyph[uni], uni)
	adduni(font, code_glyph, glyph_codes, gly, uni)
def stts(font, wkon, vr=False):
	mulp=str()
	tabch=wkon.split('.')[0]
	if '.' in wkon: mulp=wkon.split('.')[1]
	mulchar = getmulchar(mulp == "multi")
	if tabch == 'ts' or mulp == 's':
		transforme(font, tabch, "")
	else:
		transforme(font, tabch, mulchar)
	if tabch != 'ts' and mulp == "m":
		removeglyhps(font)
		if vr:
			addvariants(font)
	if tabch == 'ts' or mulp == "m":
		print('Adding lookups...')
		ForCharslookups(font, tabch, mulchar)
		ForWordslookups(font, tabch)
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
		versn='{:.2f}'.format(font.sfntRevision)
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
	if wkfl['work'].split('.')[0] in ("st", "sttw", "sthk", "stcl", "ts"):
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
