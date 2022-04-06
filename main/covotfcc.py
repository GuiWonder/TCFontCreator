import sys, json, subprocess
from collections import defaultdict
from datetime import date
from itertools import chain, groupby
from os import path

pydir = path.abspath(path.dirname(__file__))
otfccdump = path.join(pydir, 'otfcc/otfccdump')
otfccbuild = path.join(pydir, 'otfcc/otfccbuild')

def build_cmap_rev():
    cmap_rev = defaultdict(list)
    for codepoint, glyph_name in font['cmap'].items():
        cmap_rev[glyph_name].append(codepoint)
    return cmap_rev

def code_to_name(codepoint):
    return font['cmap'][str(codepoint)]

def ismulchar(char):
    with open(path.join(pydir, 'datas/Multi.txt'),'r',encoding = 'utf-8') as f:
        mul = f.read()
        if char in mul:
            return True
    return False

def addunicodest(tcunic, scunic):
    if tcunic not in codepoints_font:
        return
    tcname = code_to_name(tcunic)
    font['cmap'][str(scunic)] = tcname
    codepoints_font.add(scunic)
    adduni.add(scunic)

def remove_glyph(glyph_name):
    for codepoint in font['cmap_rev'][glyph_name]:
        del font['cmap'][codepoint]
    del font['cmap_rev'][glyph_name]
    try:
        font['glyph_order'].remove(glyph_name)
    except ValueError:
        pass
    del font['glyf'][glyph_name]
    if 'GSUB' in font:
        for lookup in font['GSUB']['lookups'].values():
            if lookup['type'] == 'gsub_single':
                for subtable in lookup['subtables']:
                    for k, v in list(subtable.items()):
                        if glyph_name == k or glyph_name == v:
                            del subtable[k]
            elif lookup['type'] == 'gsub_alternate':
                for subtable in lookup['subtables']:
                    for k, v in list(subtable.items()):
                        if glyph_name == k or glyph_name in v:
                            del subtable[k]
            elif lookup['type'] == 'gsub_ligature':
                for subtable in lookup['subtables']:
                    def predicate(
                        item): return glyph_name not in item['from'] and glyph_name != item['to']
                    subtable['substitutions'][:] = filter(
                        predicate, subtable['substitutions'])
            elif lookup['type'] == 'gsub_chaining':
                for subtable in lookup['subtables']:
                    for item in subtable['match']:
                        if glyph_name in item:
                            del subtable
            else:
                print('1.NotImplementedError.Unknown GSUB lookup type')
    if 'GPOS' in font:
        for lookup in font['GPOS']['lookups'].values():
            if lookup['type'] == 'gpos_single':
                for subtable in lookup['subtables']:
                    subtable.pop(glyph_name, None)
            elif lookup['type'] == 'gpos_pair':
                for subtable in lookup['subtables']:
                    subtable['first'].pop(glyph_name, None)
                    subtable['second'].pop(glyph_name, None)
            elif lookup['type'] == 'gpos_mark_to_base':
                for subtable in lookup['subtables']:
                    if glyph_name in subtable['marks'] or glyph_name in subtable['bases']:
                        del subtable
            else:
                print('2.NotImplementedError.Unknown GPOS lookup type')

def get_use_glyphs():
    reachable_glyphs = {'.notdef', '.null'}
    for glyph_name in font['cmap'].values():
        reachable_glyphs.add(glyph_name)
        if 'GSUB' in font:
            for lookup in font['GSUB']['lookups'].values():
                if lookup['type'] == 'gsub_single':
                    for subtable in lookup['subtables']:
                        for k, v in subtable.items():
                            if glyph_name == k:
                                reachable_glyphs.add(v)
                elif lookup['type'] == 'gsub_alternate':
                    for subtable in lookup['subtables']:
                        for k, vs in subtable.items():
                            if glyph_name == k:
                                reachable_glyphs.update(vs)
                elif lookup['type'] == 'gsub_ligature':
                    for subtable in lookup['subtables']:
                        for item in subtable['substitutions']:
                            if glyph_name in item['from']:
                                reachable_glyphs.add(item['to'])
                elif lookup['type'] == 'gsub_chaining':
                    for subtable in lookup['subtables']:
                        if glyph_name in subtable['match']:
                            reachable_glyphs.add(subtable['match'])
                else:
                    print('3.NotImplementedError.Unknown GSUB lookup type')
    return reachable_glyphs

def insert_empty_glyph(name):
    font['glyf'][name] = {'advanceWidth': 0,
                         'advanceHeight': 1000, 'verticalOrigin': 880}
    font['glyph_order'].append(name)

def grouper(iterable, n=4000):
    iterator = iter(iterable)
    while True:
        lst = []
        try:
            for _ in range(n):
                lst.append(next(iterator))
        except StopIteration:
            if lst:
                yield lst
            break
        yield lst

def grouper2(iterable, n=4000, key=None):
    for _, vx in groupby(iterable, key=key):
        for vs in grouper(vx, n):
            yield vs

def build_char_table():
    chartab = []
    with open(path.join(pydir, f'datas/Chars_{tabch}.txt'),'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            s, t = line.strip().split('\t')
            s = s.strip()
            t = t.strip()
            if s and t and ismulchar(s) and s != t:
                codes = ord(s)
                codet = ord(t)
                if codes in codepoints_font and codet in codepoints_font:
                    chartab.append((code_to_name(codes), code_to_name(codet)))
    with open(path.join(pydir, 'datas/Punctuation.txt'),'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            s, t = line.strip().split('\t')
            if s and t and s != t:
                codes = ord(s)
                codet = ord(t)
                if codes in codepoints_font and codet in codepoints_font:
                    chartab.append((code_to_name(codes), code_to_name(codet)))
    return chartab

def build_word_table():
    entries = []
    with open(path.join(pydir, 'datas/STPhrases.txt'),'r',encoding = 'utf-8') as f:
        ls = []
        for line in f.readlines():
            ls.append(line.strip().split(' ')[0])
        ls.sort(key=len, reverse=True)
        for line in ls:
            s, t = line.strip().split('\t')
            s = s.strip()
            t = t.strip()
            if not(s and t):
                continue
            codes = tuple(ord(c) for c in s)
            codet = tuple(ord(c) for c in t)
            if all(codepoint in codepoints_font for codepoint in codes) \
                    and all(codepoint in codepoints_font for codepoint in codet):
                entries.append((codes, codet))
    return entries

def insert_empty_feature(feature_name):
    for table in font['GSUB']['languages'].values():
        table['features'].append(feature_name)
    font['GSUB']['features'][feature_name] = []

def create_word2pseu_table(feature_name, conversions):
    def conversion_item_len(conversion_item): return len(conversion_item[0])
    subtables = [{'substitutions': [{'from': glyph_names_k, 'to': pseudo_glyph_name} for glyph_names_k, pseudo_glyph_name in subtable]}
                 for subtable in grouper2(conversions, key = conversion_item_len)]
    font['GSUB']['features'][feature_name].append('word2pseu')
    font['GSUB']['lookups']['word2pseu'] = {
        'type': 'gsub_ligature',
        'flags': {},
        'subtables': subtables
    }
    font['GSUB']['lookupOrder'].append('word2pseu')

def create_char2char_table(feature_name, conversions):
    subtables = [{k: v for k, v in subtable}
                 for subtable in grouper(conversions)]
    font['GSUB']['features'][feature_name].append('char2char')
    font['GSUB']['lookups']['char2char'] = {
        'type': 'gsub_single',
        'flags': {},
        'subtables': subtables
    }
    font['GSUB']['lookupOrder'].append('char2char')

def create_pseu2word_table(feature_name, conversions):
    def conversion_item_len(conversion_item): return len(conversion_item[1])
    subtables = [{k: v for k, v in subtable}
                 for subtable in grouper2(conversions, key = conversion_item_len)]
    font['GSUB']['features'][feature_name].append('pseu2word')
    font['GSUB']['lookups']['pseu2word'] = {
        'type': 'gsub_multiple',
        'flags': {},
        'subtables': subtables
    }
    font['GSUB']['lookupOrder'].append('pseu2word')

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

def addvariants():
    with open(path.join(pydir, 'datas/Variants.txt'),'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            vari = line.strip().split('\t')
            if len(vari) < 2:
                continue
            codein = 0
            for ch1 in vari:
                if ord(ch1) in codepoints_font:
                    codein = ord(ch1)
                    break
            if codein != 0:
                for ch1 in vari:
                    if ord(ch1) not in codepoints_font:
                        font['cmap'][str(ord(ch1))] = code_to_name(codein)
                        codepoints_font.add(ord(ch1))
                        adduni.add(ord(ch1))

def transforme():
    with open(path.join(pydir, f'datas/Chars_{tabch}.txt'),'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            s, t = line.strip().split('\t')
            s = s.strip()
            t = t.strip()
            if sgmulchar or not ismulchar(s):
                if s and t and s != t:
                    addunicodest(ord(t), ord(s))

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
    with open(path.join(pydir, 'datas/Hans.txt'),'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            if line.strip() and not line.strip().startswith('#'):
                s.add(int(ord(line.strip())))
    codepoints_final = s.union(adduni) & codepoints_font
    to_del = codepoints_font - codepoints_final
    for codepoint in to_del:
        if str(codepoint) in font['cmap']:
            glyph_name = font['cmap'].get(str(codepoint))
            if glyph_name and set(map(int, font['cmap_rev'][glyph_name])).issubset(to_del):
                remove_glyph(glyph_name)
    for glyph_name in set(font['glyph_order']) - get_use_glyphs():
        remove_glyph(glyph_name)

def lookuptable():
    entries_word = build_word_table()
    available_glyph_count = 65535 - len(font['glyph_order'])
    if len(entries_word) > available_glyph_count:
        print('You need ' + str(len(entries_word) - available_glyph_count) + ' more space!')
        return
    word2pseu_table = []
    char2char_table = build_char_table()
    pseu2word_table = []
    for i, (codes, codet) in enumerate(entries_word):
        empty_glyph_name = 'pseu%X' % i
        names = [code_to_name(codepoint) for codepoint in codes]
        namet = [code_to_name(codepoint) for codepoint in codet]
        insert_empty_glyph(empty_glyph_name)
        word2pseu_table.append((names, empty_glyph_name))
        pseu2word_table.append((empty_glyph_name, namet))
    print('Building lookups...')
    if not 'GSUB' in font:
        print('Creating empty GSUB!')
        font['GSUB'] = {'languages': {'hani_DFLT': {'features': []}}, 'features': {}, 'lookups': {}, 'lookupOrder': []}
    feature_name = 'liga_s2t'
    insert_empty_feature(feature_name)
    create_word2pseu_table(feature_name, word2pseu_table)
    create_char2char_table(feature_name, char2char_table)
    create_pseu2word_table(feature_name, pseu2word_table)

if len(sys.argv) > 8:
    print('Loading font...')
    font = json.loads(subprocess.check_output((otfccdump, sys.argv[1])))
    codepoints_font = set(map(int, font['cmap']))
    adduni = set()
    tabch = sys.argv[3]
    if tabch == "var" or sys.argv[4].lower() == "true":
        print('Adding variants...')
        addvariants()
    if tabch != "var":
        print('Transforming codes codes...')
        sgmulchar = sys.argv[5] == 'single'
        transforme()
    if sys.argv[5] == "multi":
        print('Manage GSUB...')
        font['cmap_rev'] = build_cmap_rev()
        print('Removing glyghs...')
        removeglyhps()
        if sys.argv[4].lower() == "true":
            print('Recycling variants...')
            codepoints_font = set(map(int, font['cmap']))
            addvariants()
        print('Building lookup table...')
        codepoints_font = set(map(int, font['cmap']))
        lookuptable()
        del font['cmap_rev']
    if sys.argv[6]:
        setinfo()
    print('Generating font...')
    subprocess.run((otfccbuild, '-o', sys.argv[2], '--keep-modified-time'),
                input = json.dumps(font), encoding = 'utf-8')
    print('Finished!')
