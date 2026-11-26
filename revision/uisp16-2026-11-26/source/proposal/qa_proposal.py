import json
import re
import sys
from pathlib import Path
from zipfile import ZipFile
from collections import Counter

import fitz
from lxml import etree

wat=Path(sys.argv[1])
pdf=fitz.open(wat.with_suffix('.pdf'))
txt=[' '.join(p.get_text().split()) for p in pdf]
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with ZipFile(wat) as doc:
    co=etree.fromstring(doc.read('word/document.xml'))
    st=etree.fromstring(doc.read('word/styles.xml'))
    sp=co.find('.//w:sectPr',ns)
    mt=sp.find('w:pgMar',ns)
    assert all(mt.get('{'+ns['w']+'}'+x)=='1440' for x in ['top','bottom','left','right'])
    for sid,sz in [('Normal','24'),('Heading1','32'),('Heading2','28'),('Heading3','24')]:
        stl=st.xpath(f"//w:style[@w:styleId='{sid}']/w:rPr",namespaces=ns)[0]
        assert stl.find('w:rFonts',ns).get('{'+ns['w']+'}ascii')=='Times New Roman'
        assert stl.find('w:sz',ns).get('{'+ns['w']+'}val')==sz
    assert st.xpath("//w:style[@w:styleId='Normal']/w:pPr/w:spacing",namespaces=ns)[0].get('{'+ns['w']+'}line')=='360'
    fields=[n.text or '' for n in co.findall('.//w:instrText',ns)]
    assert Counter(f.split()[0] for f in fields)==dict(TOC=3,SEQ=58)
    anchors={n.get('{'+ns['w']+'}name') for n in co.findall('.//w:bookmarkStart',ns)}
    dangling={n.get('{'+ns['w']+'}anchor') for n in co.findall('.//w:hyperlink',ns)}-anchors-{None}
    assert not dangling, dangling
print('Word format, 3 TOC/list fields, 58 numbering fields, all anchors resolved')
assert len(pdf)==42
assert 'Ringkasan eksekutif' in txt[5] and 'Daftar pustaka' in txt[30]
assert not txt[0] and 'Statement of Authorship' in txt[4]
assert sum(t.count('Lorem ipsum') for t in txt)==1
assert all(not re.search(r'data model dalam proses|\{\{[A-Z_0-9]+|\b(sora|kiri|polycam)\b',t,re.I) for t in txt)
fonts=Counter()
gaps={}
for q in pdf:
    if 5<=q.number<30:
        for b in q.get_text('dict')['blocks']:
            if 'lines' not in b: continue
            for l in b['lines']:
                fonts.update(s['font'] for s in l['spans'])
        y=max(b[3] for b in q.get_text('blocks',flags=fitz.TEXTFLAGS_TEXT) if b[1]>72 and b[3]<q.rect.height-71 and b[4].strip())
        gaps[q.number+1]=round((q.rect.height-72-y)/(q.rect.height-144)*100,2)
for i,s in [(5,'Rp231,45 juta'),(16,'Rp89,928 juta'),(24,'Rp24.932'),(26,'Rp2,2924 miliar'),(27,'13,97%'),(28,'0 dari 10.000'),(29,'Rp328,28 juta'),(39,'74,16%')]:
    assert s in txt[i], (i+1,s)
out={'body_pages':25,'total_pages':len(pdf),'main_pdf_fonts':dict(fonts),'bottom_gap_percent':gaps,
     'body_pages_over_15pct':{p:f for p,f in gaps.items() if f>15}}
print(json.dumps(out,indent=2))
