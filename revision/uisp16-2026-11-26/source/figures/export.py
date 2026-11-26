from pathlib import Path
import json
import fitz

p=Path(__file__).resolve().parent
figures=json.loads((p/'layout.json').read_text())
doc=fitz.open(p/'LihatDulu_Figur_UISP16.pdf')
assert len(doc)==len(figures)==14
for page,f in zip(doc,figures):
    assert abs(page.rect.width-595.28)<0.5 and abs(page.rect.height-841.89)<0.5, page.rect
    x1,y1,x2,y2=[v*0.75 for v in f['clip']]
    clip=fitz.Rect(x1,y1,x2,y2)
    page.get_pixmap(dpi=300,clip=clip,alpha=False).save(str(p/(f['id']+'.png')))
    print(f['id'], page.number+1, clip, len(page.get_text()))
