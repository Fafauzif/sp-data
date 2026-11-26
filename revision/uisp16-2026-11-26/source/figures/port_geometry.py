"""Keep exact editable DrawingML freeform paths from the supplied BCC slides."""
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from lxml import etree

root = Path(__file__).resolve().parent
source = root.parents[3] / 'upload' / '02-FRAMEWORK-BCC.pptx'
draft = root / 'draft-native.pptx'
ppi = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
       'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
port_map = {}
with ZipFile(source) as original:
    for page in (3,6,9,20,87,89,90,91,96,97,98,99,100,101,103,110,111):
        dom = etree.fromstring(original.read(f'ppt/slides/slide{page}.xml'))
        for shape in dom.xpath('//p:sp[p:spPr/a:custGeom]',namespaces=ppi):
            name = shape.find('p:nvSpPr/p:cNvPr',ppi).get('name')
            port_map[(str(page),name)] = shape.find('p:spPr/a:custGeom',ppi)

ports=0
per_slide={}
source_pages=set()
with ZipFile(draft) as provider, ZipFile(root/'LihatDulu_Figur_UISP16.pptx', 'w', ZIP_DEFLATED) as final:
    for member in provider.namelist():
        xml = provider.read(member)
        if member.startswith('ppt/slides/slide') and member.endswith('.xml'):
            doc = etree.fromstring(xml)
            n = 0
            for shape in doc.xpath('//p:sp',namespaces=ppi):
                meta = shape.find('p:nvSpPr/p:cNvPr',ppi)
                name = meta.get('name','')
                if not name.startswith('BCC__'):
                    continue
                _,page,source_name=name.split('__',2)
                source_pages.add(page)
                geometry = port_map[(page,source_name)]
                prop = shape.find('p:spPr',ppi)
                current = prop.find('a:prstGeom',ppi)
                if current is None:
                    current = prop.find('a:custGeom',ppi)
                assert current is not None
                substitute = deepcopy(geometry)
                prop.replace(current,substitute)
                meta.set('name',f'BCC {page} · {source_name}')
                n += 1
            per_slide[member] = n
            ports += n
            xml=etree.tostring(doc,encoding='UTF-8',xml_declaration=True,standalone=True)
        final.writestr(member,xml)
assert len(per_slide)==14 and all(per_slide.values()), per_slide
print(ports, f'editable freeforms copied from {len(source_pages)} BCC source slides', per_slide)
