import os, sys, json, subprocess, platform
from collections import defaultdict
from datetime import date
from itertools import chain

pydir = os.path.abspath(os.path.dirname(__file__))
otfccdump = os.path.join(pydir, 'otfcc/otfccdump')
otfccbuild = os.path.join(pydir, 'otfcc/otfccbuild')
if platform.system() == 'Mac':
    otfccdump += '1'
    otfccbuild += '1'
if platform.system() == 'Linux':
    otfccdump += '2'
    otfccbuild += '2'

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
    if not 'hani_DFLT' in font['GSUB']['languages']:
        font['GSUB']['languages']['hani_DFLT'] = {'features': []}
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
        {'platformID': 3, 'encodingID': 1, 'languageID': 5124, 'nameID': 1, 'nameString': chname},
        {'platformID': 3, 'encodingID': 1, 'languageID': 5124, 'nameID': 2, 'nameString': sbfamily},
        {'platformID': 3, 'encodingID': 1, 'languageID': 5124, 'nameID': 4, 'nameString': chname + ' ' + sbfamily},
        {'platformID': 3, 'encodingID': 1, 'languageID': 5124, 'nameID': 16, 'nameString': chname},
    ]

def jptotr():
    notr = True
    if 'GSUB' in font:
        trtab = list()
        jis78 = list()
        exptfm = list()
        aalt = list()
        torm = set()
        for lp in font['GSUB']['lookups'].keys():
            ftag = lp.split('_')[1].lower()
            ftype = font['GSUB']['lookups'][lp]['type']
            if ftype == 'gsub_single' or ftype=='gsub_alternate':
                if ftag == 'trad':
                    trtab.append(lp)
                elif ftag == 'jp78':
                    jis78.append(lp)
                elif ftag == 'expt':
                    exptfm.append(lp)
                elif ftag=='aalt':
                    aalt.append(lp)
                elif ftag in {'jp83', 'jp90'}:
                    torm.add(lp)
        if len(exptfm) > 0:
            print('Find ' + str(len(exptfm)) + ' Expert Form(s)!')
            notr = False
            gettab(exptfm)
        if len(jis78) > 0:
            print('Find ' + str(len(jis78)) + ' JIS78 Form(s)!')
            notr = False
            gettab(jis78)
        if len(aalt) > 0:
            print('Find '+str(len(aalt))+' Access All Alternate(s)!')
            notr=False
            gettabaa(aalt)
        if len(trtab) > 0:
            print('Find ' + str(len(trtab)) + ' Traditional Form(s)!')
            notr = False
            gettab(trtab, ckkanji=False)
        for subs in torm:
            del font['GSUB']['lookups'][subs]
            f1todel = set()
            for f1 in font['GSUB']['features'].keys():
                if subs in font['GSUB']['features'][f1]:
                    font['GSUB']['features'][f1].remove(subs)
                if len(font['GSUB']['features'][f1]) == 0:
                    f1todel.add(f1)
                    continue
            for  f1 in f1todel:
                del font['GSUB']['features'][f1]
    if notr:
            print('No form found!')

def gettrch(j, t):
    for cod in glyph_codes[j]:
        font['cmap'][str(cod)] = t
        glyph_codes[t].append(cod)
    glyph_codes[j].clear()

def gettab(chtat, ckkanji=True):
    for l1 in chtat:
        ftype = font['GSUB']['lookups'][l1]['type']
        for subtable in font['GSUB']['lookups'][l1]['subtables']:
            for j, t in list(subtable.items()):
                if ftype == 'gsub_single':
                    cht = t
                elif ftype == 'gsub_alternate' and len(t) == 1:
                    cht = t[0]
                if ckkanji and j in trex:
                    continue
                if not ckkanji or cht not in kanjigl:
                    gettrch(j, cht)

def gettabaa(aalt):
    for aa in aalt:
        ftype=font['GSUB']['lookups'][aa]['type']
        for subtable in font['GSUB']['lookups'][aa]['subtables']:
            for j, t in list(subtable.items()):
                if ftype=='gsub_single':
                    cht=t
                elif ftype=='gsub_alternate' and len(t)==1:
                    cht=t[0]
                if j in kanjiaa and cht not in kanjigl:
                    gettrch(j, cht)

def getkanji():
    s = set()
    with open(os.path.join(pydir, 'datas/Kanji.txt'),'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            chord=ord(line.strip())
            if chord in fontcodes:
                s.add(font['cmap'][str(chord)])
    return s

def getkanjiaa():
    s=set()
    with open(os.path.join(pydir, 'datas/Kanjiaa.txt'),'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            if not line.startswith('0') and not line.startswith('#'):
                chord=ord(line[0])
                if chord in fontcodes:
                    s.add(font['cmap'][str(chord)])
    return s

def gettrex():
    s = set()
    for ch in '邇珊跚麪麭猷叟鴉芽訝疼豹恢甑芒蜃埴据茨汲均鈷柔穿箭像揃噸頓篇巓扁拏擲斃氓膊膵茣裘褫襪贏躑輓閻霤霽騙魍親柧':
        chord = ord(ch)
        if chord in fontcodes:
            s.add(font['cmap'][str(chord)])
    return s

def fontaddfont():
    print('Loading font2...')
    font2 = json.loads(subprocess.check_output((otfccdump, '--no-bom', fin2)).decode("utf-8", "ignore"))
    if tabch == "sat":
        print('Adding font2 codes...')
        fontcodes2 = set(map(int, font2['cmap']))
        with open(os.path.join(pydir, 'datas/Variants.txt'),'r',encoding = 'utf-8') as f:
            for line in f.readlines():
                vari = line.strip().split('\t')
                if len(vari) < 2:
                    continue
                codein = 0
                for ch1 in vari:
                    if ord(ch1) in fontcodes2:
                        codein = ord(ch1)
                        break
                if codein != 0:
                    for ch1 in vari:
                        if ord(ch1) not in fontcodes2:
                            font2['cmap'][str(ord(ch1))] = font2['cmap'][str(codein)]
                            fontcodes2.add(ord(ch1))
    print('Adding glyphs...')
    glyph_codes2 = defaultdict(set)
    for codepoint, glyph_name in font2['cmap'].items():
        glyph_codes2[glyph_name].add(codepoint)
    allcodes1 = set(font['cmap'].keys())
    scl = 1.0
    if font["head"]["unitsPerEm"] != font2["head"]["unitsPerEm"]:
        scl = font["head"]["unitsPerEm"] / font2["head"]["unitsPerEm"]
    for glyph_name in font2['glyph_order']:
        if glyph_codes2[glyph_name].issubset(allcodes1):
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

if len(sys.argv) > 5:
    print('Loading font...')
    tabch = sys.argv[3]
    fin = sys.argv[1]
    if tabch in {"sat", "faf"}:
        fin, fin2 = sys.argv[1].split('|')
    font = json.loads(subprocess.check_output((otfccdump, '--no-bom', fin)).decode("utf-8", "ignore"))
    if tabch in {"sat", "faf"}:
        fontaddfont()
    adduni = set()
    fontcodes = set(map(int, font['cmap']))
    if tabch == 'jt':
        glyph_codes = build_glyph_codes()
        kanjigl = getkanji()
        kanjiaa = getkanjiaa()
        trex = gettrex()
        print('Moving glyph codes...')
        jptotr()
    if tabch == "var" or sys.argv[4].lower() == "true":
        print('Adding variants...')
        addvariants()
    if tabch in {"tc", "tctw", "tchk", "tct"} or (tabch == "jt" and sys.argv[5].lower() == "true"):
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
    subprocess.run((otfccbuild, '--keep-modified-time', '--keep-average-char-width', '-O3', '-q', '-o', sys.argv[2]),
                input = json.dumps(font), encoding = 'utf-8')
    print('Finished!')
