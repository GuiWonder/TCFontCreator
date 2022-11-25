import os, sys, json, subprocess, platform, tempfile, gc
from collections import defaultdict
from datetime import date
from itertools import chain

pydir = os.path.abspath(os.path.dirname(__file__))
otfccdump = os.path.join(pydir, 'otfcc/otfccdump')
otfccbuild = os.path.join(pydir, 'otfcc/otfccbuild')
if platform.system() in ('Mac', 'Darwin'):
	otfccdump += '1'
	otfccbuild += '1'
if platform.system() == 'Linux':
	otfccdump += '2'
	otfccbuild += '2'

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

def addvariants():
	with open(os.path.join(pydir, 'datas/Variants.txt'),'r',encoding = 'utf-8') as f:
		for line in f.readlines():
			line = line.strip()
			if line.startswith('#') or '\t' not in line:
				continue
			vari = line.strip().split('\t')
			codein = 0
			for ch1 in vari:
				if str(ord(ch1)) in font['cmap']:
					codein = ord(ch1)
					break
			if codein != 0:
				for ch1 in vari:
					if str(ord(ch1)) not in font['cmap']:
						font['cmap'][str(ord(ch1))] = font['cmap'][str(codein)]

def transforme():
	with open(os.path.join(pydir, f'datas/Chars_{tabch}.txt'),'r',encoding = 'utf-8') as f:
		for line in f.readlines():
			line = line.strip()
			if line.startswith('#') or '\t' not in line:
				continue
			lnst=line.strip().split('\t')
			s, t = lnst[0], lnst[1]
			s = s.strip()
			t = t.strip()
			if s and t and s != t and (usemulchar or not s in mulchar):
				if str(ord(t)) in font['cmap']:
					font['cmap'][str(ord(s))] = font['cmap'][str(ord(t))]

def build_glyph_codes(f):
	glyph_codes = defaultdict(list)
	for codepoint, glyph_name in f['cmap'].items():
		glyph_codes[glyph_name].append(codepoint)
	return glyph_codes

def removeglyhps():
	usedg=set()

	if tabch != 'ts' and sys.argv[5] == "multi":
		s = set(chain(
			range(0x0000, 0x007E + 1),
			range(0x02B0, 0x02FF + 1),
			range(0x2002, 0x203B + 1),
			range(0x2E00, 0x2E7F + 1),
			range(0x2E80, 0x2EFF + 1),
			range(0x3000, 0x301C + 1),
			range(0x3100, 0x312F + 1),
			range(0x3190, 0x31BF + 1),
			range(0xFE10, 0xFE1F + 1),
			range(0xFE30, 0xFE4F + 1),
			range(0xFF01, 0xFF5E + 1),
			range(0xFF5F, 0xFF65 + 1),
		))
		with open(os.path.join(pydir, 'datas/Hans.txt'),'r',encoding = 'utf-8') as f:
			for line in f.readlines():
				if line.strip() and not line.strip().startswith('#'):
					s.add(ord(line.strip()))
		cdsall=set(map(str, s))
		nmap=set(font['cmap'].keys()).intersection(cdsall)
		for mp in nmap:
			usedg.add(font['cmap'][mp])
	else:
		usedg.update(set(font['cmap'].values()))
		if 'cmap_uvs' in font:
			for k in font['cmap_uvs'].keys():
				c, v=k.split(' ')
				if c in font['cmap']:
					usedg.add(font['cmap_uvs'][k])
	if 'GSUB' in font:
		for lkn in font['GSUB']['lookupOrder']:
			if lkn in font['GSUB']['lookups']:
				lookup=font['GSUB']['lookups'][lkn]
				if lookup['type'] == 'gsub_single':
					for subtable in lookup['subtables']:
						for g1, g2 in list(subtable.items()):
							if g1 in usedg:
								usedg.add(g2)
				elif lookup['type'] == 'gsub_alternate':
					for subtable in lookup['subtables']:
						for item in set(subtable.keys()):
							if item in usedg:
								usedg.update(set(subtable[item]))
				elif lookup['type'] == 'gsub_ligature': 
					for subtable in lookup['subtables']:
						for item in subtable['substitutions']:
							if set(item['from']).issubset(usedg):
								usedg.add(item['to'])
				elif lookup['type'] == 'gsub_chaining':
					for subtable in lookup['subtables']:
						for ls in subtable['match']:
							for l1 in ls:
								usedg.update(set(l1))
	unusegl=set()
	unusegl.update(set(font['glyph_order']))
	notg={'.notdef', '.null', 'nonmarkingreturn', 'NULL', 'NUL'}
	unusegl.difference_update(notg)
	unusegl.difference_update(usedg)
	for ugl in unusegl:
		font['glyph_order'].remove(ugl)
		del font['glyf'][ugl]

	print('Checking cmap tables...')
	for cod in set(font['cmap'].keys()):
		if font['cmap'][cod] in unusegl:
			del font['cmap'][cod]
	if 'cmap_uvs' in font:
		for uvk in set(font['cmap_uvs'].keys()):
			if font['cmap_uvs'][uvk] in unusegl:
				del font['cmap_uvs'][uvk]
	print('Checking Lookup tables...')
	if 'GSUB' in font:
		for lookup in font['GSUB']['lookups'].values():
			if lookup['type'] == 'gsub_single':
				for subtable in lookup['subtables']:
					for g1, g2 in list(subtable.items()):
						if g1 in unusegl or g2 in unusegl:
							del subtable[g1]
			elif lookup['type'] == 'gsub_alternate':
				for subtable in lookup['subtables']:
					for item in set(subtable.keys()):
						if item in unusegl or len(set(subtable[item]).intersection(unusegl))>0:
							del subtable[item]
			elif lookup['type'] == 'gsub_ligature': 
				for subtable in lookup['subtables']:
					s1=list()
					for item in subtable['substitutions']:
						if item['to'] not in unusegl and len(set(item['from']).intersection(unusegl))<1:
							s1.append(item)
					subtable['substitutions']=s1
			elif lookup['type'] == 'gsub_chaining':
				for subtable in lookup['subtables']:
					for ls in subtable['match']:
						for l1 in ls:
							l1=list(set(l1).difference(unusegl))
	if 'GPOS' in font:
		for lookup in font['GPOS']['lookups'].values():
			if lookup['type'] == 'gpos_single':
				for subtable in lookup['subtables']:
					for item in list(subtable.keys()):
						if item in unusegl:
							del subtable[item]
			elif lookup['type'] == 'gpos_pair':
				for subtable in lookup['subtables']:
					for item in list(subtable['first'].keys()):
						if item in unusegl:
							del subtable['first'][item]
					for item in list(subtable['second'].keys()):
						if item in unusegl:
							del subtable['second'][item]
			elif lookup['type'] == 'gpos_mark_to_base':
				nsb=list()
				for subtable in lookup['subtables']:
					gs=set(subtable['marks'].keys()).union(set(subtable['bases'].keys()))
					if len(gs.intersection(unusegl))<1:
						nsb.append(subtable)
				lookup['subtables']=nsb

def lookuptable():
	print('Building lookups...')
	if not 'GSUB' in font:
		print('Creating empty GSUB!')
		font['GSUB'] = {
							'languages': 
							{
								'hani_DFLT': 
								{
									'features': []
								}
							}, 
							'features': {}, 
							'lookups': {}, 
							'lookupOrder': []
						}
	if not 'hani_DFLT' in font['GSUB']['languages']:
		font['GSUB']['languages']['hani_DFLT'] = {'features': []}
	for table in font['GSUB']['languages'].values():
		table['features'].insert(0, 'ccmp_st')
	font['GSUB']['features']['ccmp_st'] = ['wordsc', 'stchars', 'wordtc']
	font['GSUB']['lookupOrder'].append('wordsc')
	font['GSUB']['lookupOrder'].append('stchars')
	font['GSUB']['lookupOrder'].append('wordtc')
	if tabch=='ts':
		build_char_tableTS()
	else:
		build_char_table()
	build_word_table()

def build_char_table():
	kt = dict()
	with open(os.path.join(pydir, f'datas/Chars_{tabch}.txt'),'r',encoding = 'utf-8') as f:
		for line in f.readlines():
			line = line.strip()
			if line.startswith('#') or '\t' not in line:
				continue
			s, t = line.strip().split('\t')
			s = s.strip()
			t = t.strip()
			if s and t and s != t and s in mulchar:
				if str(ord(s)) in font['cmap'] and str(ord(t)) in font['cmap']:
					kt[font['cmap'][str(ord(s))]] = font['cmap'][str(ord(t))]
	with open(os.path.join(pydir, 'datas/Punctuation.txt'),'r',encoding = 'utf-8') as f:
		for line in f.readlines():
			line = line.strip()
			if line.startswith('#') or '\t' not in line:
				continue
			s, t = line.strip().split('\t')
			if s and t and s != t:
				codesc = ord(s)
				codetc = ord(t)
				if str(ord(s)) in font['cmap'] and str(ord(t)) in font['cmap']:
					kt[font['cmap'][str(ord(s))]] = font['cmap'][str(ord(t))]
	font['GSUB']['lookups']['stchars'] = {
											'type': 'gsub_single',
											'flags': {},
											'subtables': [kt]
										 }

def build_char_tableTS():
	kt = dict()
	with open(os.path.join(pydir, f'datas/Chars_tsm.txt'),'r',encoding = 'utf-8') as f:
		for line in f.readlines():
			line = line.strip()
			if line.startswith('#') or '\t' not in line:
				continue
			s, t = line.strip().split('\t')
			s = s.strip()
			t = t.strip()
			if s and t and s != t:
				if str(ord(s)) in font['cmap'] and str(ord(t)) in font['cmap']:
					kt[font['cmap'][str(ord(s))]] = font['cmap'][str(ord(t))]
	font['GSUB']['lookups']['stchars'] = {
											'type': 'gsub_single',
											'flags': {},
											'subtables': [kt]
										 }

def build_word_table():
	phrases='datas/STPhrases.txt'
	if tabch=='ts':
		phrases='datas/TSPhrases.txt'
	stword = list()
	with open(os.path.join(pydir, phrases),'r',encoding = 'utf-8') as f:
		ccods=set(font['cmap'].keys())
		for line in f.readlines():
			line = line.strip().split(' ')[0]
			if line.startswith('#') or '\t' not in line:
				continue
			s, t = line.split('\t')
			s = s.strip()
			t = t.strip()
			if not(s and t):
				continue
			
			codestc = set(str(ord(c)) for c in s+t)
			if codestc.issubset(ccods):
				stword.append((s, t))
	if len(stword) + len(font['glyph_order']) > 65535:
		nd=len(stword) + len(font['glyph_order']) - 65535
		raise RuntimeError('Not enough glyph space! You need ' + str(nd) + ' more glyph space!')
	if len(stword) > 0:
		addlookupword(stword)

def addlookupword(stword):
	stword.sort(key=lambda x:len(x[0]), reverse = True)
	subtablesl = list()
	subtablesm = list()
	i, j = 0, 0
	sbs = list()
	sbt = dict()
	wlen = len(stword[0][0])
	while True:
		wds = list()
		wdt = list()
		for s1 in stword[i][0]:
			wds.append(font['cmap'][str(ord(s1))])
		for t1 in stword[i][1]:
			wdt.append(font['cmap'][str(ord(t1))])
		newgname = 'ligast' + str(i)
		font['glyf'][newgname] = {
									'advanceWidth': 0, 
									'advanceHeight': 1000, 
									'verticalOrigin': 880
								 }
		font['glyph_order'].append(newgname)
		sbs.append({'from': wds, 'to': newgname})
		sbt[newgname] = wdt
		if i >= len(stword) - 1:
			subtablesl.append({'substitutions': sbs})
			subtablesm.append(sbt)
			break
		j += len(stword[i][0] + stword[i][1])
		wlen2 = len(stword[i + 1][0])
		if j >= 20000 or wlen2 < wlen:
			j = 0
			wlen = wlen2
			subtablesl.append({'substitutions': sbs})
			subtablesm.append(sbt)
			sbs = list()
			sbt = dict()
		i += 1
	font['GSUB']['lookups']['wordsc'] = {
											'type': 'gsub_ligature',
											'flags': {},
											'subtables': subtablesl
										}
	font['GSUB']['lookups']['wordtc'] = {
											'type': 'gsub_multiple',
											'flags': {},
											'subtables': subtablesm
										}

def setinfo():
	enname = sys.argv[6]
	chname = sys.argv[7]
	psname = sys.argv[8]
	version = sys.argv[9]
	dateinfo = date.today().strftime('%b %d, %Y')
	sbfamily = 'Regular'
	versionstr = f'Version 1.00;{dateinfo}'
	for nm in font['name']:
		if nm['languageID'] == 1033 and nm['nameID'] == 2:
			sbfamily = nm['nameString']
		if nm['languageID'] == 1033 and nm['nameID'] == 5:
			versionstr = nm['nameString']
	if version:
		try:
			font['head']['fontRevision'] = float(version)
		except ValueError:
			pass
		versionstr = f'Version {version};{dateinfo}'
	else:
		version = '{:.2f}'.format(font['head']['fontRevision'])
	if not psname.lower().endswith(sbfamily.lower()):
		psname += '-' + sbfamily
	font['name'] = [
		{'platformID': 0, 'encodingID': 0, 'languageID': 0, 'nameID': 1, 'nameString': enname},
		{'platformID': 0, 'encodingID': 0, 'languageID': 0, 'nameID': 2, 'nameString': sbfamily},
		{'platformID': 0, 'encodingID': 0, 'languageID': 0, 'nameID': 3, 'nameString': f'{enname}:Version {version}'},
		{'platformID': 0, 'encodingID': 0, 'languageID': 0, 'nameID': 4, 'nameString': enname + ' ' + sbfamily},
		{'platformID': 0, 'encodingID': 0, 'languageID': 0, 'nameID': 5, 'nameString': versionstr},
		{'platformID': 0, 'encodingID': 0, 'languageID': 0, 'nameID': 6, 'nameString': psname},
		{'platformID': 0, 'encodingID': 0, 'languageID': 0, 'nameID': 16, 'nameString': enname},
		{'platformID': 3, 'encodingID': 1, 'languageID': 1028, 'nameID': 1, 'nameString': chname},
		{'platformID': 3, 'encodingID': 1, 'languageID': 1028, 'nameID': 2, 'nameString': sbfamily},
		{'platformID': 3, 'encodingID': 1, 'languageID': 1028, 'nameID': 4, 'nameString': chname + ' ' + sbfamily},
		{'platformID': 3, 'encodingID': 1, 'languageID': 1028, 'nameID': 16, 'nameString': chname},
		{'platformID': 3, 'encodingID': 1, 'languageID': 1033, 'nameID': 1, 'nameString': enname},
		{'platformID': 3, 'encodingID': 1, 'languageID': 1033, 'nameID': 2, 'nameString': sbfamily},
		{'platformID': 3, 'encodingID': 1, 'languageID': 1033, 'nameID': 3, 'nameString': f'{enname}:Version {version}'},
		{'platformID': 3, 'encodingID': 1, 'languageID': 1033, 'nameID': 4, 'nameString': enname + ' ' + sbfamily},
		{'platformID': 3, 'encodingID': 1, 'languageID': 1033, 'nameID': 5, 'nameString': versionstr},
		{'platformID': 3, 'encodingID': 1, 'languageID': 1033, 'nameID': 6, 'nameString': psname},
		{'platformID': 3, 'encodingID': 1, 'languageID': 1033, 'nameID': 16, 'nameString': enname},
		{'platformID': 3, 'encodingID': 1, 'languageID': 2052, 'nameID': 1, 'nameString': chname},
		{'platformID': 3, 'encodingID': 1, 'languageID': 2052, 'nameID': 2, 'nameString': sbfamily},
		{'platformID': 3, 'encodingID': 1, 'languageID': 2052, 'nameID': 4, 'nameString': chname + ' ' + sbfamily},
		{'platformID': 3, 'encodingID': 1, 'languageID': 2052, 'nameID': 16, 'nameString': chname},
		{'platformID': 3, 'encodingID': 1, 'languageID': 3076, 'nameID': 1, 'nameString': chname},
		{'platformID': 3, 'encodingID': 1, 'languageID': 3076, 'nameID': 2, 'nameString': sbfamily},
		{'platformID': 3, 'encodingID': 1, 'languageID': 3076, 'nameID': 4, 'nameString': chname + ' ' + sbfamily},
		{'platformID': 3, 'encodingID': 1, 'languageID': 3076, 'nameID': 16, 'nameString': chname},
		{'platformID': 3, 'encodingID': 1, 'languageID': 5124, 'nameID': 1, 'nameString': chname},
		{'platformID': 3, 'encodingID': 1, 'languageID': 5124, 'nameID': 2, 'nameString': sbfamily},
		{'platformID': 3, 'encodingID': 1, 'languageID': 5124, 'nameID': 4, 'nameString': chname + ' ' + sbfamily},
		{'platformID': 3, 'encodingID': 1, 'languageID': 5124, 'nameID': 16, 'nameString': chname},
	]
	if 'CFF_' in font:
		font['CFF_']['fontName']=psname
		font['CFF_']['fullName']=enname + ' ' + sbfamily
		font['CFF_']['familyName']=enname
		if 'fdArray' in font['CFF_']:
			nfd=dict()
			pn=enname.replace(' ', '')
			for k in font['CFF_']['fdArray'].keys():
				k2=pn+'-'+'-'.join(k.split('-')[1:])
				nfd[k2]=font['CFF_']['fdArray'][k]
			font['CFF_']['fdArray']=nfd
			for gl in font['glyf'].values():
				if 'CFF_fdSelect' in gl:
					gl['CFF_fdSelect']=pn+'-'+'-'.join(gl['CFF_fdSelect'].split('-')[1:])

def fontaddfont():
	print('Loading font2...')
	font2 = json.loads(subprocess.check_output((otfccdump, '--no-bom', fin2)).decode("utf-8", "ignore"))
	if tabch == "sat":
		print('Adding font2 codes...')
		with open(os.path.join(pydir, 'datas/Variants.txt'),'r',encoding = 'utf-8') as f:
			for line in f.readlines():
				line = line.strip()
				if line.startswith('#') or '\t' not in line:
					continue
				vari = line.strip().split('\t')
				codein = 0
				for ch1 in vari:
					if str(ord(ch1)) in font2['cmap']:
						codein = ord(ch1)
						break
				if codein != 0:
					for ch1 in vari:
						if str(ord(ch1)) not in font2['cmap']:
							font2['cmap'][str(ord(ch1))] = font2['cmap'][str(codein)]
	print('Adding glyphs...')
	glyph_codes2 = build_glyph_codes(font2)
	allcodes1 = set(font['cmap'].keys())
	scl = 1.0
	if font["head"]["unitsPerEm"] != font2["head"]["unitsPerEm"]:
		scl = font["head"]["unitsPerEm"] / font2["head"]["unitsPerEm"]
	for glyph_name in font2['glyph_order']:
		if set(glyph_codes2[glyph_name]).issubset(allcodes1):
			continue
		glyph_name1 = glyph_name
		j = 1
		while glyph_name1 in font['glyph_order']:
			glyph_name1 = glyph_name+'.'+str(j)
			j += 1
		font['glyf'][glyph_name1] = font2['glyf'][glyph_name]
		if scl != 1.0:
			sclglyph(font['glyf'][glyph_name1], scl)
		font['glyph_order'].append(glyph_name1)
		for codepoint in glyph_codes2[glyph_name]:
			if codepoint not in allcodes1:
				font['cmap'][codepoint] = glyph_name1
	del font2
	del glyph_codes2

def sclglyph(glyph, scl):
	glyph['advanceWidth'] = round(glyph['advanceWidth'] * scl)
	if 'advanceHeight' in glyph:
		glyph['advanceHeight'] = round(glyph['advanceHeight'] * scl)
		glyph['verticalOrigin'] = round(glyph['verticalOrigin'] * scl)
	if 'contours' in glyph:
		for contour in glyph['contours']:
			for point in contour:
				point['x'] = round(point['x'] * scl);
				point['y'] = round(point['y'] * scl);
	if 'references' in glyph:
		for reference in glyph['references']:
			reference['x'] = round(scl * reference['x'])
			reference['y'] = round(scl * reference['y'])
def jptotr():
	dv = dict()
	if 'cmap_uvs' not in font:
		raise RuntimeError('This font is not applicable!')
	for k in font['cmap_uvs'].keys():
		c, v = k.split(' ')
		if c not in dv:
			dv[c] = dict()
		dv[c][v] = font['cmap_uvs'][k]

	tv = dict()
	with open(os.path.join(pydir, 'datas/uvs-get-jp1-MARK.txt'), 'r', encoding='utf-8') as f:
		for line in f.readlines():
			if not line or line.startswith('#'):
				continue
			line = line.strip()
			if line.endswith('X'):
				a = line.split(' ')
				tv[str(ord(a[0]))] = str(int(a[3].strip('X'), 16))

	for k in dv.keys():
		if k in tv:
			if tv[k] in dv[k]:
				tch = dv[k][tv[k]]
				font['cmap'][k] = tch

if len(sys.argv) > 5:
	print('Loading font...')
	tabch = sys.argv[3]
	fin = sys.argv[1]
	if tabch in {"sat", "faf"}:
		fin, fin2 = sys.argv[1].split('|')
	font = json.loads(subprocess.check_output((otfccdump, '--no-bom', fin)).decode("utf-8", "ignore"))
	if tabch in {"sat", "faf"}:
		fontaddfont()
	if tabch == 'jt':
		print('Moving glyph codes...')
		jptotr()
	if tabch == "var" or sys.argv[4].lower() == "true":
		print('Adding variants...')
		addvariants()
	if tabch in {"st", "sttw", "sthk", "stcl", "ts"}:
		print('Transforming codes...')
		usemulchar = tabch == 'ts' or sys.argv[5] == 'single'
		mulchar = getmulchar(sys.argv[5] == "multi")
		transforme()
		print('Removing glyghs...')
		removeglyhps()
		if tabch == 'ts' or sys.argv[5] == "multi":
			print('Checking GSUB...')
			if tabch != 'ts' and sys.argv[4].lower() == "true":
				print('Checking variants...')
				addvariants()
			print('Building lookup table...')
			lookuptable()
	if len(sys.argv) > 9 and sys.argv[6]:
		print('Setting font info...')
		setinfo()
	print('Generating font...')
	tmpfile = tempfile.mktemp('.json')
	with open(tmpfile, 'w', encoding='utf-8') as f:
		f.write(json.dumps(font))
	del font
	for x in set(locals().keys()):
		if x not in ('os', 'subprocess', 'otfccbuild', 'sys', 'tmpfile', 'gc'):
			del locals()[x]
	gc.collect()
	print('Creating TTF/OTF...')
	subprocess.run((otfccbuild, '--keep-modified-time', '--keep-average-char-width', '-O3', '-q', '-o', sys.argv[2], tmpfile))
	os.remove(tmpfile)
	print('Finished!')
