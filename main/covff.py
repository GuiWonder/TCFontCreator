
import sys, os, datetime
dateinfo = datetime.date.today().strftime('%b %d, %Y')

import fontforge
from itertools import chain

pydir = os.path.abspath(os.path.dirname(__file__))

def addunicodest(tcunic, scunic):
    if tcunic not in amb and tcunic not in alladdcds:
        return
    glytc = amb[amb.findEncodingSlot(tcunic)]
    if scunic in amb or scunic in alladdcds:
        glysc = amb[amb.findEncodingSlot(scunic)]
        if glytc == glysc:
            return
        if scunic == glysc.unicode:
            if glysc.altuni != None:
                l1 = list()
                l2 = list()
                for sccds in glysc.altuni:
                    l1.append(sccds[0])
                glysc.unicode = l1[0]
                for u2 in l1:
                    if u2 != glysc.unicode:
                        l2.append((u2, ))
                if len(l2) > 0:
                    glysc.altuni = l2
                else:
                    glysc.altuni = None
            else:
                amb.removeGlyph(scunic)
        else:
            al1 = list()
            for alt in glysc.altuni:
                if alt[0] != scunic:
                    al1.append((alt[0], ))
            if len(al1) > 0:
                glysc.altuni = al1
            else:
                glysc.altuni = None
    ss = {scunic}
    ll = list()
    if glytc.altuni != None:
        for uni in glytc.altuni:
            ss.add(uni[0])
    for s1 in ss:
        ll.append((s1, ))
    glytc.altuni = ll
    alladdcds.add(scunic)

def ismulchar(char):
    with open(os.path.join(pydir, 'datas/Multi.txt'), 'r', encoding = 'utf-8') as f:
        mul = f.read()
        if char in mul:
            return True
    return False

def addvariants():
    with open(os.path.join(pydir, 'datas/Variants.txt'), 'r', encoding = 'utf-8') as f:
        for line in f.readlines():
            vari = line.strip().split('\t')
            if len(vari) < 2:
                continue
            codein = 0
            for ch1 in vari:
                chcode = ord(ch1)
                if chcode in amb or chcode in alladdcds:
                    codein = chcode
                    break
            if codein != 0:
                for ch1 in vari:
                    chcode = ord(ch1)
                    if chcode not in amb and chcode not in alladdcds:
                        addunicodest(codein, chcode)

def transforme():
    with open(os.path.join(pydir, f'datas/Chars_{tabch}.txt'), 'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            s, t = line.strip().split('\t')
            s = s.strip()
            t = t.strip()
            if sgmulchar or not ismulchar(s):
                if s and t and s != t:
                    addunicodest(ord(t), ord(s))

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
    with open(os.path.join(pydir, 'datas/Hans.txt'), 'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            if line.strip() and not line.strip().startswith('#'):
                alcodes.add(int(ord(line.strip())))
    alcodes.update(alladdcds)
    for gls in amb.glyphs():
        rmit = True
        if gls.glyphname.startswith('.') or gls.unicode in alcodes:
            rmit = False
        elif gls.altuni != None:
            for uni in gls.altuni:
                if uni[0] in alcodes:
                    rmit = False
                    break
        if rmit:
            amb.removeGlyph(gls)

def addlookupschar(tcunic, scunic):
    if (tcunic in amb or tcunic in alladdcds) and (scunic in amb or scunic in alladdcds):
        gtc = amb[amb.findEncodingSlot(tcunic)]
        gsc = amb[amb.findEncodingSlot(scunic)]
        if gtc.glyphname != gsc.glyphname:
            gsc.addPosSub('stchar1', gtc.glyphname)

def addlookupsword(tcword, scword, j, num):
    newgname = 'ligastch_' + num
    wdin = list()
    wdout = list()
    for s1 in scword:
        try:
            glys = amb[amb.findEncodingSlot(ord(s1))]
        except TypeError:
            print('Skip ' + s1)
            return
        wdin.append(glys.glyphname)
    for t1 in tcword:
        try:
            glyt = amb[amb.findEncodingSlot(ord(t1))]
        except TypeError:
            print('Skip ' + t1)
            return
        wdout.append(glyt.glyphname)
    newg = amb.createChar(-1, str(newgname))
    newg.width = 1000
    newg.vwidth = 800
    newg.addPosSub('stliga' + j, tuple(wdin))
    newg.addPosSub('stmult' + j, tuple(wdout))

def ForCharslookups():
    amb.addLookup('stchar', 'gsub_single', None, (("liga",(("hani",("dflt")),)),))
    amb.addLookupSubtable('stchar', 'stchar1')
    with open(os.path.join(pydir, f'datas/Chars_{tabch}.txt'), 'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            s, t = line.strip().split('\t')
            s = s.strip()
            t = t.strip()
            if s and t and ismulchar(s) and s != t:
                addlookupschar(ord(t), ord(s))
    with open(os.path.join(pydir, 'datas/Punctuation.txt'), 'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            s, t = line.strip().split('\t')
            s = s.strip()
            t = t.strip()
            if s and t and s != t:
                addlookupschar(ord(t), ord(s))

def ForWordslookups():
    amb.addLookup('stmult', 'gsub_multiple', None, (("liga",(("hani",("dflt")),)),), 'stchar')
    amb.addLookup('stliga', 'gsub_ligature', None, (("liga",(("hani",("dflt")),)),))
    with open(os.path.join(pydir, 'datas/STPhrases.txt'),'r',encoding = 'utf-8') as f:
        i, j, num = 1, 1, 0
        amb.addLookupSubtable('stmult', 'stmult' + str(j))
        amb.addLookupSubtable('stliga', 'stliga' + str(j))
        ls = list()
        for line in f.readlines():
            isavail = True
            for ch1 in line.strip().replace('\t', ''):
                if ord(ch1) not in amb and ord(ch1) not in alladdcds:
                    isavail = False
                    break
            if isavail:
                ls.append(line.strip().split(' ')[0])
        ls.sort(key = len, reverse = True)
        for line in ls:
            s, t = line.strip().split('\t')
            s = s.strip()
            t = t.strip()
            if not(s and t):
                continue
            i += 1
            if i >= 500:
                i = 1
                j += 1
                amb.addLookupSubtable('stmult', 'stmult' + str(j), 'stmult' + str(j - 1))
                amb.addLookupSubtable('stliga', 'stliga' + str(j), 'stliga' + str(j - 1))
            num += 1
            addlookupsword(t, s, str(j), str(num))

def setinfo():
    enname = sys.argv[6]
    chname = sys.argv[7]
    psname = sys.argv[8]
    version = sys.argv[9]
    sbfamily = 'Regular'
    versionstr = f'Version 1.00;{dateinfo}'
    for n1 in amb.sfnt_names:
        if n1[0] == 'English (US)' and n1[1] == 'SubFamily':
            sbfamily = n1[2]
        if n1[0] == 'English (US)' and n1[1] == 'Version':
            versionstr = n1[2]
    if version:
        try:
            amb.sfntRevision = float(version)
        except ValueError:
            amb.sfntRevision = None
        versionstr = f'Version {version};{dateinfo}'
    else:
        version = '{:.2f}'.format(amb.sfntRevision)
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
        ('Chinese (Hong Kong)', 'Preferred Family', chname)
    )
    amb.sfnt_names = sfntnames

if len(sys.argv) > 8:
    print('Loading font...')
    amb = fontforge.open(sys.argv[1])
    amb.reencode("unicodefull")
    alladdcds = set()
    tabch = sys.argv[3]
    if tabch == "var" or sys.argv[4].lower() == "true":
        print('Adding variants...')
        addvariants()
    if tabch != "var":
        print('Transforming codes...')
        sgmulchar = sys.argv[5] == 'single'
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
    if sys.argv[6]:
        print('Setting font info...')
        setinfo()
    print('Generating font...')
    amb.generate(sys.argv[2])
    print('Finished!')
