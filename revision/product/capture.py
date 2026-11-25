from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent
raw=root/'raw'; raw.mkdir(exist_ok=True)
class Handler(SimpleHTTPRequestHandler):
 def __init__(self, *args): super().__init__(*args, directory=str(root/'checkout/dist'))
 def do_GET(self):
  if not Path(self.translate_path(self.path)).exists() and '.' not in self.path.split('?')[0].split('/')[-1]:
   self.path='/index.html'
  super().do_GET()
 def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}'
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
 page=browser.new_page(viewport={'width':1320,'height':1000}, device_scale_factor=1.4)
 page.on('pageerror',lambda err: print('Page error:',str(err)[:200]))
 def goto(path):
  page.goto(base+path,wait_until='networkidle')
  page.evaluate("document.fonts.ready")
 def capture(name,sel=None):
  page.wait_for_timeout(350)
  opt={'path':str(raw/(name+'.png')),'animations':'disabled'}
  if sel: page.locator(sel).first.screenshot(**opt)
  else: page.screenshot(**opt)
  print(name)
 goto('/barang/sora?tab=photos')
 capture('listing')
 capture('conditions','#catatan-kondisi')
 page.get_by_role('button',name='Goresan pintu kiri',exact=False).last.click()
 capture('scratch','dialog')
 goto('/barang/sora?tab=room')
 page.locator('canvas').first.wait_for()
 page.wait_for_timeout(1300)
 capture('room','.product-media')
 goto('/jual/sora/rekam')
 capture('seller')
 goto('/jual/sora/tinjau')
 capture('seller_review')
 goto('/beli')
 capture('marketplace')
 browser.close()
server.shutdown()
