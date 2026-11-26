from pathlib import Path
import json
from PIL import Image, ImageDraw
import fitz

root=Path(__file__).resolve().parent
figures=json.loads((root/'layout.json').read_text())
pdf=fitz.open(root/'LihatDulu_Figur_UISP16.pdf')
for start in range(0,len(figures),4):
 ids=figures[start:start+4]
 sheet=Image.new('RGB',(1410,900),'#E3E8E2')
 d=ImageDraw.Draw(sheet)
 for j,f in enumerate(ids):
  im=Image.open(root/(f['id']+'.png')).convert('RGB')
  im.thumbnail((680,425))
  x,y=5+j%2*705,8+j//2*450
  d.text((x,y),f['id'],fill='black')
  sheet.paste(im,(x,y+17))
 sheet.save(root/f'qa-{start//4+1}.jpg',quality=89)
for page,desc in zip(pdf,figures):
 clip=fitz.Rect([v*.75 for v in desc['clip']])
 texts=[s for b in page.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans']]
 tiny=[(s['text'],s['size']) for s in texts if s['size']<8.45]
 out=[(s['text'],[round(v,1) for v in s['bbox']]) for s in texts if not clip.contains(fitz.Rect(s['bbox']))]
 print(desc['id'],'spans',len(texts),'tiny',tiny,'outside',out)
