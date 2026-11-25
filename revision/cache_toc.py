from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import fitz,re,sys

base=Path('revision')
target=next((base/'output').glob('*.docx'))
pdf=fitz.open(next(Path(sys.argv[1]).glob('*.pdf')))
w='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
norm=lambda s:' '.join(s.split())
with ZipFile(target) as docx:
 xml=etree.fromstring(docx.read('word/document.xml'))
 field_nodes=xml.findall('.//'+w+'fldSimple')
 labels={}
 rendered={}
 entries=pdf[1].get_text().splitlines()
 for line in entries:
  m=re.match(r'(.+?)\s*\.{4,}\s*(\d+)\s*$',line)
  if m:rendered[norm(m.group(1))]=m.group(2)
 for f in field_nodes:
  stmt=f.get(w+'instr','')
  if not stmt.strip().startswith('PAGEREF'):continue
  p=f.getparent()
  h=p.find(w+'hyperlink')
  label=norm(''.join(n.text or '' for n in h.iter(w+'t')))
  dest=h.get(w+'anchor')
  if label not in rendered: raise ValueError(f'Missing page number in rendered TOC for {label}')
  if all(norm(line)!=label for line in pdf[int(rendered[label])].get_text().splitlines()):
   raise ValueError(f'Bad rendered page for {label}, got {rendered[label]}')
  node=f.find("./"+w+"r/"+w+"t")
  if node is None: node=etree.SubElement(f.find(w+"r"),w+"t")
  node.text=rendered[label]
  labels[dest]=int(rendered[label])
 path=target.with_suffix('.tmp')
 with ZipFile(path,'w') as out:
  for info in docx.infolist():
   data=etree.tostring(xml,encoding='UTF-8',xml_declaration=True,standalone=True) if info.filename=='word/document.xml' else docx.read(info.filename)
   out.writestr(info,data)
path.replace(target)
print(f'{len(labels)} table-of-contents page labels cached and cross-checked.')
print('Pages',len(pdf),'executive summary',labels['Summary'],'references',labels['References'],'counted pages up to references',labels['References']-labels['Summary']+1)
print('PDF links',sum(len(p.get_links()) for p in pdf))
