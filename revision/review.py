from pathlib import Path
from PIL import Image, ImageDraw
import fitz,sys
folder=Path(sys.argv[1])
doc=fitz.open(next(folder.glob('*.pdf')))
for start in range(0,len(doc),8):
 images=list(doc)[start:start+8]
 out=Image.new('RGB',(1500,1100),'#DDE6DF')
 for i,p in enumerate(images):
  pix=p.get_pixmap(matrix=fitz.Matrix(.61,.61),alpha=False)
  im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
  x=i%4*375+6;y=i//4*550+18
  out.paste(im,(x,y))
  ImageDraw.Draw(out).text((x,y-16),str(p.number+1),fill='black')
 out.save(folder/f'grid-{start//8}.jpg',quality=91)
