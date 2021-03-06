
import sys, os, datetime
dateinfo = datetime.date.today().strftime('%b %d, %Y')

import fontforge
from itertools import chain

pydir = os.path.abspath(os.path.dirname(__file__))

def getmulchar():
    s = str()
    with open(os.path.join(pydir, 'datas/Multi.txt'), 'r', encoding = 'utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if line and not line.startswith('#'):
                s += line
    return s

def addvariants():
    with open(os.path.join(pydir, 'datas/Variants.txt'), 'r', encoding = 'utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('#') or '\t' not in line:
                continue
            vari = line.strip().split('\t')
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
                        addunicodest(codein, chcode)

def transforme():
    with open(os.path.join(pydir, f'datas/Chars_{tabch}.txt'), 'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('#') or '\t' not in line:
                continue
            s, t = line.strip().split('\t')
            s = s.strip()
            t = t.strip()
            if s and t and s != t and (usemulchar or not s in mulchar):
                addunicodest(ord(t), ord(s))

def addunicodest(tcunic, scunic):
    if tcunic not in code_glyph:
        return
    glytc = font[code_glyph[tcunic]]
    if scunic in code_glyph:
        glysc = font[code_glyph[scunic]]
        if glytc.glyphname == glysc.glyphname:
            return
        glyph_codes[glysc.glyphname].remove(scunic)
        if glysc.unicode == scunic:
            glysc.unicode = -1
        elif glysc.altuni != None:
            l1 = list()
            for aa in glysc.altuni:
                if aa[0] != scunic or aa[1] > 0:
                    l1.append(aa)
            if len(l1) > 0:
                glysc.altuni = tuple(l1)
            else:
                glysc.altuni = None
    l2=list()
    if glytc.altuni != None:
        for a2 in glytc.altuni:
            l2.append(a2)
    l2.append((scunic, -1, 0))
    glytc.altuni = tuple(l2)
    glyph_codes[glytc.glyphname].append(scunic)
    code_glyph[scunic] = glytc.glyphname

def removeglyhps():
    alcodes = set(chain(
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
    with open(os.path.join(pydir, 'datas/Hans.txt'), 'r', encoding = 'utf-8') as f:
        for line in f.readlines():
            if line.strip() and not line.strip().startswith('#'):
                alcodes.add(ord(line.strip()))
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
            font.removeGlyph(gls)
    getallcodesname(font, code_glyph, glyph_codes)

def ForCharslookups():
    font.addLookup('stchar', 'gsub_single', None, (("liga",(("hani",("dflt")),)),))
    font.addLookupSubtable('stchar', 'stchar1')
    with open(os.path.join(pydir, f'datas/Chars_{tabch}.txt'), 'r', encoding = 'utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('#') or '\t' not in line:
                continue
            s, t = line.strip().split('\t')
            s = s.strip()
            t = t.strip()
            if s and t and s != t and s in mulchar:
                addlookupschar(ord(t), ord(s))
    with open(os.path.join(pydir, 'datas/Punctuation.txt'), 'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('#') or '\t' not in line:
                continue
            s, t = line.strip().split('\t')
            s = s.strip()
            t = t.strip()
            if s and t and s != t:
                addlookupschar(ord(t), ord(s))

def addlookupschar(tcunic, scunic):
    if tcunic in code_glyph and scunic in code_glyph:
        gntc = code_glyph[tcunic]
        gnsc = code_glyph[scunic]
        if gntc != gnsc:
            font[gnsc].addPosSub('stchar1', gntc)

def ForWordslookups():
    stword = list()
    with open(os.path.join(pydir, 'datas/STPhrases.txt'),'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('#') or '\t' not in line:
                continue
            isavail = True
            for ch1 in line.strip().replace('\t', '').replace(' ', ''):
                if ord(ch1) not in code_glyph:
                    isavail = False
                    break
            if isavail:
                s, t = line.strip().split(' ')[0].split('\t')
                if s.strip() and t.strip():
                    stword.append((s.strip(), t.strip()))
    if len(stword) < 1:
        return
    sumf = sum(1 for _ in font.glyphs())
    if len(stword) + sumf > 65535:
        raise RuntimeError('Not enough glyph space! You need ' + str(len(stword) + sumf - 65535) + ' more glyph space!')
    stword.sort(key=lambda x:len(x[0]), reverse = True)
    font.addLookup('stmult', 'gsub_multiple', None, (("liga",(("hani",("dflt")),)),), 'stchar')
    font.addLookup('stliga', 'gsub_ligature', None, (("liga",(("hani",("dflt")),)),))
    i, j, tlen, wlen = 0, 0, 0, len(stword[0][0])
    font.addLookupSubtable('stmult', 'stmult0')
    font.addLookupSubtable('stliga', 'stliga0')
    for wd in stword:
        tlen += len(wd[0] + wd[1])
        wlen2 = len(stword[i][0])
        if tlen >= 15000 or wlen2 < wlen:
            tlen = 0
            wlen = wlen2
            j += 1
            font.addLookupSubtable('stmult', 'stmult' + str(j), 'stmult' + str(j - 1))
            font.addLookupSubtable('stliga', 'stliga' + str(j), 'stliga' + str(j - 1))
        i += 1
        addlookupsword(wd[1], wd[0], str(j), str(i))

def addlookupsword(tcword, scword, j, i):
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

def setinfo():
    enname = sys.argv[6]
    chname = sys.argv[7]
    psname = sys.argv[8]
    version = sys.argv[9]
    sbfamily = 'Regular'
    versionstr = f'Version 1.00;{dateinfo}'
    for n1 in font.sfnt_names:
        if n1[0] == 'English (US)' and n1[1] == 'SubFamily':
            sbfamily = n1[2]
        if n1[0] == 'English (US)' and n1[1] == 'Version':
            versionstr = n1[2]
    if version:
        try:
            font.sfntRevision = float(version)
        except ValueError:
            font.sfntRevision = None
        versionstr = f'Version {version};{dateinfo}'
    else:
        version = '{:.2f}'.format(font.sfntRevision)
    if not psname.lower().endswith(sbfamily.lower()):
        psname += '-' + sbfamily
    sfntnames = (
        ('English (US)', 'Family', enname), 
        ('English (US)', 'SubFamily', sbfamily), 
        ('English (US)', 'UniqueID', f'{enname}:Version {version}'), 
        ('English (US)', 'Fullname', enname + ' ' + sbfamily), 
        ('English (US)', 'Version', versionstr), 
        ('English (US)', 'PostScriptName', psname), 
        ('English (US)', 'Preferred Family', enname), 
        ('Chinese (Taiwan)', 'Family', chname), 
        ('Chinese (Taiwan)', 'SubFamily', sbfamily), 
        ('Chinese (Taiwan)', 'Fullname', chname + ' ' + sbfamily), 
        ('Chinese (Taiwan)', 'Preferred Family', chname), 
        ('Chinese (PRC)', 'Family', chname), 
        ('Chinese (PRC)', 'SubFamily', sbfamily), 
        ('Chinese (PRC)', 'Fullname', chname + ' ' + sbfamily), 
        ('Chinese (PRC)', 'Preferred Family', chname), 
        ('Chinese (Hong Kong)', 'Family', chname), 
        ('Chinese (Hong Kong)', 'SubFamily', sbfamily), 
        ('Chinese (Hong Kong)', 'Fullname', chname + ' ' + sbfamily), 
        ('Chinese (Hong Kong)', 'Preferred Family', chname), 
        ('Chinese (Macau)', 'Family', chname), 
        ('Chinese (Macau)', 'SubFamily', sbfamily), 
        ('Chinese (Macau)', 'Fullname', chname + ' ' + sbfamily), 
        ('Chinese (Macau)', 'Preferred Family', chname)
    )
    font.sfnt_names = sfntnames

def getallcodesname(font, code_glyph, glyph_codes):
    code_glyph.clear()
    glyph_codes.clear()
    for gls in font.glyphs():
        glyph_codes[gls.glyphname]=list()
        if gls.unicode > -1:
            code_glyph[gls.unicode]=gls.glyphname
            glyph_codes[gls.glyphname].append(gls.unicode)
        if gls.altuni != None:
            for uni in gls.altuni:
                if uni[1] <= 0:
                    code_glyph[uni[0]] = gls.glyphname
                    glyph_codes[gls.glyphname].append(uni[0])

def fontaddfont():
    print('Loading font2...')
    font2 = fontforge.open(fin2)
    if font2.is_cid:
        font2.cidFlatten()
    font2.em = font.em
    print('Getting glyph2 codes')
    code_glyph2 = dict()
    glyph_codes2=dict()
    getallcodesname(font2, code_glyph2, glyph_codes2)
    if tabch == "sat":
        font2.reencode("unicodefull")
        print('Adding font2 codes...')
        allcodes2 = code_glyph2.keys()
        with open(os.path.join(pydir, 'datas/Variants.txt'),'r',encoding = 'utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if line.startswith('#') or '\t' not in line:
                    continue
                vari = line.strip().split('\t')
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
        allcodes = code_glyph.keys()
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
    else:
        print('Adding glyphs...')
        code_codes2 = {}
        for n2 in glyph_codes2.keys():
            lc = list()
            for ac1 in glyph_codes2[n2]:
                if ac1 not in code_glyph.keys():
                    lc.append(ac1)
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
    getallcodesname(font, code_glyph, glyph_codes)

def jptotr():
    tv = dict()
    with open(os.path.join(pydir, 'datas/uvs-get-jp1-MARK.txt'), 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.endswith('X'):
                a = line.split(' ')
                tv[ord(a[0])] = int(a[3].strip('X'), 16)
    ltb=list()
    for gls in font.glyphs():
        if gls.altuni != None:
            for alt in gls.altuni:
                if alt[1] > 0:
                    if alt[0] in tv and tv[alt[0]] == alt[1]:
                        ltb.append((gls.glyphname, alt[0]))
    for t1 in ltb:
        g = font[code_glyph[t1[1]]]
        if t1[0] == g.glyphname:
            continue
        if g.unicode == t1[1]:
            g.unicode = -1
        elif g.altuni != None:
            l1=list()
            for aa in g.altuni:
                if aa[0] == t1[1] and aa[1] <= 0:
                    continue
                l1.append(aa)
            if len(l1) > 0:
                g.altuni = tuple(l1)
            else:
                g.altuni = None
        if font[t1[0]].unicode == -1:
            font[t1[0]].unicode = t1[1]
        else:
            l2 = list()
            if font[t1[0]].altuni != None:
                for a2 in font[t1[0]].altuni:
                    l2.append(a2)
            l2.append((t1[1], -1, 0))
            font[t1[0]].altuni = tuple(l2)
        glyph_codes[g.glyphname].remove(t1[1])
        glyph_codes[t1[0]].append(t1[1])
        code_glyph[t1[1]]=t1[0]

if len(sys.argv) > 5:
    print('Loading font...')
    tabch = sys.argv[3]
    fin = sys.argv[1]
    if tabch in {"sat", "faf"}:
        fin, fin2 = sys.argv[1].split('|')
    font = fontforge.open(fin)
    if font.is_cid:
        font.cidFlatten()
    font.reencode("unicodefull")
    code_glyph = dict()
    glyph_codes=dict()
    getallcodesname(font, code_glyph, glyph_codes)
    if tabch in {"sat", "faf"}:
        fontaddfont()
    if tabch == 'jt':
        print('Moving glyph codes...')
        jptotr()
    if tabch == "var" or sys.argv[4].lower() == "true":
        print('Adding variants...')
        addvariants()
    if tabch in {"tc", "tctw", "tchk", "tct"}:
        print('Transforming codes...')
        usemulchar = sys.argv[5] == 'single'
        mulchar = getmulchar()
        transforme()
        if sys.argv[5] == "multi":
            print('Removing glyghs...')
            removeglyhps()
            if sys.argv[4].lower() == "true":
                print('Recycling variants...')
                addvariants()
            print('Manage GSUB...')
            print('Adding chars lookups...')
            ForCharslookups()
            print('Adding words lookups...')
            ForWordslookups()
    if len(sys.argv) > 9 and sys.argv[6]:
        print('Setting font info...')
        setinfo()
    del code_glyph
    del glyph_codes
    print('Generating font...')
    font.generate(sys.argv[2])
    print('Finished!')
