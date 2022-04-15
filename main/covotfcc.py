import os, sys, json, subprocess
from collections import defaultdict
from datetime import date
from itertools import chain

pydir = os.path.abspath(os.path.dirname(__file__))
otfccdump = os.path.join(pydir, 'otfcc/otfccdump')
otfccbuild = os.path.join(pydir, 'otfcc/otfccbuild')

def getmulchar():
    s = str()
    with open(os.path.join(pydir, 'datas/Multi.txt'), 'r', encoding = 'utf-8') as f:
        for l1 in f.readlines():
            if l1.strip():
                s += l1.strip()
    return s

def addvariants():
    with open(os.path.join(pydir, 'datas/Variants.txt'),'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            vari = line.strip().split('\t')
            if len(vari) < 2:
                continue
            codein = 0
            for ch1 in vari:
                if ord(ch1) in fontcodes:
                    codein = ord(ch1)
                    break
            if codein != 0:
                for ch1 in vari:
                    if ord(ch1) not in fontcodes:
                        font['cmap'][str(ord(ch1))] = font['cmap'][str(codein)]
                        fontcodes.add(ord(ch1))
                        adduni.add(ord(ch1))

def transforme():
    with open(os.path.join(pydir, f'datas/Chars_{tabch}.txt'),'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            s, t = line.strip().split('\t')
            s = s.strip()
            t = t.strip()
            if s and t and s != t and (usemulchar or not s in mulchar):
                addunicodest(ord(t), ord(s))

def addunicodest(tcunic, scunic):
    if tcunic not in fontcodes:
        return
    tcname = font['cmap'][str(tcunic)]
    font['cmap'][str(scunic)] = tcname
    fontcodes.add(scunic)
    adduni.add(scunic)

def build_glyph_codes():
    glyph_codes = defaultdict(list)
    for codepoint, glyph_name in font['cmap'].items():
        glyph_codes[glyph_name].append(codepoint)
    return glyph_codes

def removeglyhps():
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
    codes_final = s.union(adduni) & fontcodes
    to_del = fontcodes - codes_final
    for codepoint in to_del:
        if str(codepoint) in font['cmap']:
            glyph_name = font['cmap'].get(str(codepoint))
            if glyph_name and set(map(int, glyph_codes[glyph_name])).issubset(to_del):
                removecodes(glyph_name)
    for glyph_name in set(font['glyph_order']) - get_use_glyphs():
        if not glyph_name.startswith('.'):
            remove_glyph(glyph_name)

def removecodes(glyph_name):
    for codepoint in glyph_codes[glyph_name]:
        del font['cmap'][codepoint]
    del glyph_codes[glyph_name]

def get_use_glyphs():
    use_glyphs = set()
    for glyph_name in font['cmap'].values():
        use_glyphs.add(glyph_name)
        if 'GSUB' in font:
            for lookup in font['GSUB']['lookups'].values():
                if lookup['type'] == 'gsub_single':
                    for subtable in lookup['subtables']:
                        for a, b in subtable.items():
                            if glyph_name == a:
                                use_glyphs.add(b)
                elif lookup['type'] == 'gsub_alternate':
                    for subtable in lookup['subtables']:
                        for a, b1 in subtable.items():
                            if glyph_name == a:
                                use_glyphs.update(b1)
                elif lookup['type'] == 'gsub_ligature':
                    for subtable in lookup['subtables']:
                        for item in subtable['substitutions']:
                            if glyph_name in item['from']:
                                use_glyphs.add(item['to'])
                elif lookup['type'] == 'gsub_chaining':
                    for subtable in lookup['subtables']:
                        if glyph_name in subtable['match']:
                            use_glyphs.add(subtable['match'])
    return use_glyphs

def remove_glyph(glyph_name):
    for codepoint in glyph_codes[glyph_name]:
        del font['cmap'][codepoint]
    del glyph_codes[glyph_name]
    try:
        font['glyph_order'].remove(glyph_name)
    except ValueError:
        pass
    del font['glyf'][glyph_name]
    if 'GSUB' in font:
        for lookup in font['GSUB']['lookups'].values():
            if lookup['type'] == 'gsub_single':
                for subtable in lookup['subtables']:
                    for a, b in list(subtable.items()):
                        if glyph_name == a or glyph_name == b:
                            del subtable[a]
            elif lookup['type'] == 'gsub_alternate':
                for subtable in lookup['subtables']:
                    for a, b in list(subtable.items()):
                        if glyph_name == a or glyph_name in b:
                            del subtable[a]
            elif lookup['type'] == 'gsub_ligature':
                for subtable in lookup['subtables']:
                    def predicate(
                        item): return glyph_name not in item['from'] and glyph_name != item['to']
                    subtable['substitutions'][:] = filter(
                        predicate, subtable['substitutions'])
    if 'GPOS' in font:
        for lookup in font['GPOS']['lookups'].values():
            if lookup['type'] == 'gpos_single':
                for subtable in lookup['subtables']:
                    subtable.pop(glyph_name, None)
            elif lookup['type'] == 'gpos_pair':
                for subtable in lookup['subtables']:
                    subtable['first'].pop(glyph_name, None)
                    subtable['second'].pop(glyph_name, None)

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
    for table in font['GSUB']['languages'].values():
        table['features'].append('liga_st')
    font['GSUB']['features']['liga_st'] = ['wordsc', 'stchars', 'wordtc']
    font['GSUB']['lookupOrder'].append('wordsc')
    font['GSUB']['lookupOrder'].append('stchars')
    font['GSUB']['lookupOrder'].append('wordtc')
    build_char_table()
    build_word_table()

def build_char_table():
    chartab = []
    with open(os.path.join(pydir, f'datas/Chars_{tabch}.txt'),'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            s, t = line.strip().split('\t')
            s = s.strip()
            t = t.strip()
            if s and t and s != t and s in mulchar:
                codesc = ord(s)
                codetc = ord(t)
                if codesc in fontcodes and codetc in fontcodes:
                    chartab.append((s, t))
    with open(os.path.join(pydir, 'datas/Punctuation.txt'),'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            s, t = line.strip().split('\t')
            if s and t and s != t:
                codesc = ord(s)
                codetc = ord(t)
                if codesc in fontcodes and codetc in fontcodes:
                    chartab.append((s, t))
    addlookupschar(chartab)

def addlookupschar(chtab):
    kt = dict()
    for s, t in chtab:
        kt[font['cmap'][str(ord(s))]] = font['cmap'][str(ord(t))]
    font['GSUB']['lookups']['stchars'] = {
                                            'type': 'gsub_single',
                                            'flags': {},
                                            'subtables': [kt]
                                         }

def build_word_table():
    stword = list()
    with open(os.path.join(pydir, 'datas/STPhrases.txt'),'r',encoding = 'utf-8') as f:
        ls = list()
        for line in f.readlines():
            ls.append(line.strip().split(' ')[0])
        for line in ls:
            s, t = line.strip().split('\t')
            s = s.strip()
            t = t.strip()
            if not(s and t):
                continue
            codesc = tuple(ord(c) for c in s)
            codetc = tuple(ord(c) for c in t)
            if all(codepoint in fontcodes for codepoint in codesc) \
                    and all(codepoint in fontcodes for codepoint in codetc):
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
    ]

if len(sys.argv) > 5:
    print('Loading font...')
    font = json.loads(subprocess.check_output((otfccdump, sys.argv[1])))
    fontcodes = set(map(int, font['cmap']))
    adduni = set()
    tabch = sys.argv[3]
    if tabch == "var" or sys.argv[4].lower() == "true":
        print('Adding variants...')
        addvariants()
    if tabch != "var":
        print('Transforming codes...')
        usemulchar = sys.argv[5] == 'single'
        mulchar = getmulchar()
        transforme()
        if sys.argv[5] == "multi":
            print('Manage GSUB...')
            glyph_codes = build_glyph_codes()
            print('Removing glyghs...')
            removeglyhps()
            if sys.argv[4].lower() == "true":
                print('Recycling variants...')
                fontcodes = set(map(int, font['cmap']))
                addvariants()
            print('Building lookup table...')
            fontcodes = set(map(int, font['cmap']))
            lookuptable()
    if len(sys.argv) > 9 and sys.argv[6]:
        print('Setting font info...')
        setinfo()
    print('Generating font...')
    subprocess.run((otfccbuild, '-o', sys.argv[2], '--keep-modified-time'),
                input = json.dumps(font), encoding = 'utf-8')
    print('Finished!')
