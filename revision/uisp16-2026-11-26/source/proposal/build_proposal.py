from __future__ import annotations
import json
from pathlib import Path
import os
import re
import sys

from lxml import etree
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE
from docx.shared import Cm, Pt, RGBColor
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sections import pages as later

work = Path(__file__).resolve().parent
figdir = work.parent / 'figures'
gen = work.parent / 'campaign'
assets = work / 'proposal_assets'
assets.mkdir(exist_ok=True)
output = Path(sys.argv[1]) if len(sys.argv)>1 else work.parent.parent / 'build' / 'LihatDulu_UISP16_Proposal_v2.docx'
mode = os.environ.get('LIHAT_DRAFT','0')=='1'

with (work/'narrative.json').open() as f:
    narrative = json.load(f)
metrics_file = work/'proposal_metrics.json'
metrics = json.loads(metrics_file.read_text()) if metrics_file.exists() else {}
cache_file=work/'folio_cache.json'
folio_cache = json.loads(cache_file.read_text()) if cache_file.exists() else {}

forest='185544'; dark='15382C'; ink='263D34'; light='EDF4EE'; rules='CFDBD1'; warm='F2ECE2'; muted='52665B';
font='Times New Roman'
d=Document()
style=d.styles

def colour(s): return RGBColor.from_string(s)
def style_add(name, size, color=ink, bold=False, after=0, before=0, lines=1.5, align=None):
    st=style[name] if name in style else style.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
    st.font.name=font; st.font.size=Pt(size); st.font.bold=bold; st.font.color.rgb=colour(color)
    family=st._element.get_or_add_rPr().rFonts
    for attribute in ('asciiTheme','hAnsiTheme','eastAsiaTheme','cstheme','csTheme'):
        family.attrib.pop(qn('w:'+attribute),None)
    for attribute in ('ascii','hAnsi','eastAsia','cs'):
        family.set(qn('w:'+attribute),font)
    fmt=st.paragraph_format
    fmt.line_spacing=lines; fmt.space_after=Pt(after); fmt.space_before=Pt(before)
    if align is not None: fmt.alignment=align
    return st
style_add('Normal',12,'202620',False,2,0,1.5,WD_ALIGN_PARAGRAPH.JUSTIFY)
for name,sz,before,after in [('Heading 1',16,0,6),('Heading 2',14,5,4),('Heading 3',12,3,3)]:
    st=style_add(name,sz,'111711',True,after,before,1.12,WD_ALIGN_PARAGRAPH.LEFT)
    st.paragraph_format.keep_with_next=True
    st.paragraph_format.keep_together=True
style_add('LD lead',12,dark,True,5,1,1.25,WD_ALIGN_PARAGRAPH.LEFT)
style_add('LD caption',10,forest,True,2,5,1.03,WD_ALIGN_PARAGRAPH.LEFT)
style_add('LD image note',9,muted,False,6,1,1.02,WD_ALIGN_PARAGRAPH.LEFT)
style_add('LD label',9,forest,True,4,0,1.04,WD_ALIGN_PARAGRAPH.LEFT)
style_add('LD cell',10,'20382D',False,0,0,1.06,WD_ALIGN_PARAGRAPH.LEFT)
style_add('LD ref',10.5,'202620',False,4,0,1.16,WD_ALIGN_PARAGRAPH.LEFT)
style['LD ref'].paragraph_format.left_indent=Cm(0.65)
style['LD ref'].paragraph_format.first_line_indent=Cm(-0.65)
for nm in [f'TOC {i}' for i in range(1,4)] + ['Table of Figures']:
    st=style_add(nm,11,'202620',False,0,0,1.065,WD_ALIGN_PARAGRAPH.LEFT)
    st.paragraph_format.tab_stops.add_tab_stop(Cm(15.7), WD_ALIGN_PARAGRAPH.RIGHT, 1)

sec=d.sections[0]; sec.page_width=Cm(21); sec.page_height=Cm(29.7)
sec.top_margin=sec.bottom_margin=sec.left_margin=sec.right_margin=Cm(2.54)
sec.header_distance=Cm(1.15); sec.footer_distance=Cm(1.05)
sec.different_first_page_header_footer=True
hp=sec.header.paragraphs[0]
hp.style='LD label'
hp.paragraph_format.space_after=Pt(0)
hp.paragraph_format.tab_stops.add_tab_stop(Cm(15.92),WD_ALIGN_PARAGRAPH.RIGHT)
hp.add_run('LIHATDULU').font.size=Pt(9.5)
hp.add_run('\tUISP16  /  PROPOSAL BISNIS').font.size=Pt(8.5)
ppr=hp._p.get_or_add_pPr()
bd=OxmlElement('w:pBdr'); rule=OxmlElement('w:bottom')
for k,v in {'val':'single','sz':'11','space':'7','color':'8EA99A'}.items(): rule.set(qn('w:'+k),v)
bd.append(rule); ppr.append(bd)
fp=sec.footer.paragraphs[0]; fp.style='LD label'
fp.paragraph_format.tab_stops.add_tab_stop(Cm(15.92),WD_ALIGN_PARAGRAPH.RIGHT)
fp.add_run('LihatDulu\t')
def field_native(p, code, result=''):
    for typ,txt in [('begin',''),('instr',code),('separate',''),('result',result),('end','')]:
        rr=p.add_run()
        if typ=='instr':
            a=OxmlElement('w:instrText'); a.set(qn('xml:space'),'preserve'); a.text=txt; rr._r.append(a)
        elif typ=='result': rr.text=txt
        else:
            a=OxmlElement('w:fldChar'); a.set(qn('w:fldCharType'),typ); rr._r.append(a)
field_native(fp,' PAGE ','1')
settings=d.settings.element
u=OxmlElement('w:updateFields');u.set(qn('w:val'),'false');settings.append(u)

def fmt(v):
    if isinstance(v,str): return v
    if isinstance(v,(int,float)): return f'{v:,.0f}'.replace(',','.')
    return str(v)

missing=set()
def bind(s):
    def sub(m):
        key=m.group(1)
        if key in metrics and metrics[key] not in ('',None): return fmt(metrics[key])
        missing.add(key)
        return 'data model dalam proses' if mode else f'{{{{{key}}}}}'
    return re.sub(r'\{\{([A-Z0-9_]+)\}\}',sub,str(s))

toc=[]
figlist=[]
tblist=[]
ids=0
cursor=1

def bookmark(p,name):
    global ids
    ids+=1
    a=OxmlElement('w:bookmarkStart'); a.set(qn('w:id'),str(ids)); a.set(qn('w:name'),name)
    b=OxmlElement('w:bookmarkEnd'); b.set(qn('w:id'),str(ids))
    pos=1 if p._p.pPr is not None else 0
    p._p.insert(pos,a);p._p.append(b)

def emit(text='', sty=None):
    return d.add_paragraph(bind(text),style=sty)

def link(p, label, url=None, anchor=None):
    h=OxmlElement('w:hyperlink')
    if url: h.set(qn('r:id'),p.part.relate_to(url,RELATIONSHIP_TYPE.HYPERLINK,is_external=True))
    else: h.set(qn('w:anchor'),anchor)
    r=OxmlElement('w:r')
    rp=OxmlElement('w:rPr'); c=OxmlElement('w:color');c.set(qn('w:val'),forest);rp.append(c);r.append(rp)
    t=OxmlElement('w:t');t.text=label;t.set(qn('xml:space'),'preserve');r.append(t);h.append(r);p._p.append(h)

def h(text,level=2, name=None):
    pp=emit(text,f'Heading {level}')
    name=name or f'bagian{len(toc)+1}'
    bookmark(pp,name)
    toc.append((name,text,level,cursor))
    return pp

def fresh(title=None,level=2,name=None):
    global cursor
    d.add_page_break();cursor+=1
    if title: h(title,level,name)

def para(text):
    return emit(text,'Normal')

def note(text):
    return emit(text,'LD image note')

def lead(text): return emit(text,'LD lead')

def chart(out, labels, vals, maximum, serieslabel=None):
    with plt.rc_context({'font.family':'DejaVu Sans','font.size':10.4,'axes.facecolor':'#F0F5EF','figure.facecolor':'#F0F5EF','axes.edgecolor':'#ADBFB1','text.color':'#203A2D','xtick.color':'#37574A'}):
        shallow=out.name=='survey-barriers.png'
        fig,ax=plt.subplots(figsize=(6.20,1.48 if shallow else 2.58))
        fig.subplots_adjust(left=.38 if shallow else .42,right=.945,top=.95,bottom=.30 if shallow else .20)
        y=list(range(len(labels)))
        bars=ax.barh(y,vals,color=['#185544']+['#739984']*(len(labels)-1),height=.55)
        ax.set_yticks(y,labels=labels);ax.tick_params(axis='y',length=0,labelsize=9)
        ax.set_xlim(0,maximum);ax.invert_yaxis()
        ax.set_axisbelow(True);ax.grid(axis='x',color='#D9E4DB',linewidth=.6)
        for i,(b,v) in enumerate(zip(bars,vals)):
            ax.text(v+maximum*.022,b.get_y()+b.get_height()/2,str(v),va='center',fontweight='bold',fontsize=11,color='#185544')
        for k in ['top','right','left']:ax.spines[k].set_visible(False)
        if serieslabel: ax.set_xlabel(serieslabel,fontsize=8,labelpad=4)
        fig.savefig(out,dpi=300,facecolor=fig.get_facecolor());plt.close(fig)

survey=assets/'survey-barriers.png'
chart(survey,['Kondisi barang','Kecocokan ruang','Biaya atau cara angkut','Dimensi barang','Keandalan penjual'],[14,10,10,8,4],17,'Responden dengan pengalaman iklan spesifik (n = 17)')
actions=assets/'survey-actions.png'
chart(actions,['Meminta informasi','Melihat barang langsung','Menghubungi untuk membeli','Mencari pilihan lain','Menyimpan penawaran'],[12,8,6,6,6],17,'Responden dengan pengalaman iklan spesifik (n = 17)')
confidence=assets/'survey-confidence.png'
chart(confidence,['Lebih yakin','Tetap','Kurang yakin'],[34,16,10],45,'Jawaban berpasangan pada contoh iklan (n = 60)')

def cap(kind,title):
    ix=figlist if kind=='Gambar' else tblist
    n=len(ix)+1
    name=('gambar' if kind=='Gambar' else 'tabel')+str(n)
    p=emit('', 'LD caption')
    p.paragraph_format.keep_with_next=True
    p.add_run(kind+' ')
    field_native(p, ' SEQ '+kind+' \\* ARABIC ',str(n))
    p.add_run('. '+bind(title))
    bookmark(p,name)
    ix.append((name,f'{kind} {n}. '+bind(title),1,cursor))
    return p

def path_for(id):
    product=work/'product'
    named={
        'survey':survey,'survey-actions':actions,'survey-confidence':confidence,
        'product':product/'produk-alur-penjual-pembeli.png',
        'spz':product/'bukti-pemrosesan-lokal.png',
        'mock-creator':gen/'kreator-muat-nggak.png',
        'mock-bursa':gen/'bursa-pindahan.png',
        'mock-material':gen/'kartu-kondisi-dan-meja-bantuan.png',
        'risk-chart':work/'npv_histogram.png','orders-chart':work/'orders.png','cash-chart':work/'cash.png',
    }
    return named.get(id,figdir/(id+'.png'))

def figure(id,title,credit=None,maxheight=8.2):
    path=path_for(id)
    if not path.is_file():
        if not mode: raise FileNotFoundError(path)
        note(f'[Figur dalam pengerjaan: {id}]')
        return
    cap('Gambar',title)
    p=emit()
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    pf=p.paragraph_format;pf.space_before=Pt(0);pf.space_after=Pt(1);pf.line_spacing=1.0
    pf.keep_with_next=bool(credit)
    with Image.open(path) as image:
        x,y=image.size
    wi=min(15.9,maxheight*x/y)
    shape=p.add_run().add_picture(str(path),width=Cm(wi))
    shape._inline.docPr.set('descr',bind(title))
    if credit: note(credit)

def fill(cell, value, head=False):
    pp=cell.paragraphs[0];pp.style='LD cell'
    r=pp.add_run(bind(value));r.bold=head
    if head: r.font.color.rgb=colour('FFFFFF')

def table(title,cols, rows, widths=None):
    cap('Tabel',title)
    tb=d.add_table(rows=1,cols=len(cols))
    tb.autofit=False
    if widths is None:
        widths={2:[4.25,11.65],3:[3.2,6.6,6.1],4:[2.1,5.6,3.4,4.8],5:[5.05,2.7,2.7,2.7,2.75],6:[3.05,2.57,2.57,2.57,2.57,2.57]}.get(len(cols),[15.9/len(cols)]*len(cols))
    for c,w in zip(tb.columns,widths):c.width=Cm(w)
    allrows=[cols]+list(rows)
    for j, cells in enumerate(allrows):
        row=tb.rows[0] if j==0 else tb.add_row()
        trpr=row._tr.get_or_add_trPr()
        trpr.append(OxmlElement('w:cantSplit'))
        if j==0:trpr.append(OxmlElement('w:tblHeader'))
        for c,val,w in zip(row.cells,cells,widths):
            c.width=Cm(w)
            pr=c._tc.get_or_add_tcPr()
            sh=OxmlElement('w:shd');sh.set(qn('w:fill'),forest if j==0 else ('F0F5EF' if j%2 else 'F8FAF7'));pr.append(sh)
            margins=OxmlElement('w:tcMar')
            for edge,n in [('top','46'),('bottom','48'),('left','85'),('right','85')]:
                el=OxmlElement('w:'+edge);el.set(qn('w:w'),n);el.set(qn('w:type'),'dxa');margins.append(el)
            pr.append(margins)
            fill(c,val,j==0)
    return tb

def ref_note(title,url,loc=None):
    p=emit(title+' ', 'LD ref')
    if url: link(p,'Sumber',url=url);p.add_run('.')
    if loc:p.add_run(' '+loc)
    return p

def nav(anchor,label):
    p=emit('', 'LD image note');link(p,label,anchor=anchor); p.add_run('.')

# Cover intentionally reserved by the author.
fresh()
p=emit('Daftar isi','Heading 1');bookmark(p,'daftarisi')
toc_anchor=p._p
fresh()
p=emit('Daftar gambar','Heading 1');bookmark(p,'daftargambar')
fig_anchor=p._p
fresh()
p=emit('Daftar tabel','Heading 1');bookmark(p,'daftartabel')
tbl_anchor=p._p
fresh()
h('Statement of Authorship',1,'statement')

def product_assets(i):
    p=work/'product'
    return json.loads((p/'appendix.json').read_text()) if i else {}

append=product_assets(True)
narr= {p['page']:p for p in narrative['pages']}
for i in range(1,26):
    if i==1: fresh('Ringkasan eksekutif',1,'ringkasan')
    elif i==2: fresh('BAB 1 Pendahuluan',1,'bab1')
    elif i==4: fresh('BAB 2 Model bisnis',1,'bab2')
    elif i==8: fresh('BAB 3 Strategi operasi',1,'bab3')
    elif i==11: fresh('BAB 4 Strategi pemasaran',1,'bab4')
    elif i==19: fresh('BAB 5 Strategi keuangan',1,'bab5')
    else: fresh()
    if i<=10:
        for j,s in enumerate(narr[i]['sections']):
            if s['heading']:
                names={(3,1):'validasi',(4,0):'katalog',(6,0):'alurproduk',(7,0):'buktiteknis',(8,0):'alurkerja'}
                h(s['heading'],name=names.get((i,j)))
            paragraphs=s['paragraphs']
            if i==3 and j==0:
                paragraphs=[
                    'Pratama et al. (2021) menemukan kebutuhan jual beli perabot di kalangan penghuni kos di Yogyakarta. Di Depok, liputan detikFinance memperlihatkan furnitur bekas beredar kembali lewat Mall Rongsok (Faturahman, 2026). Namun, keberadaan kanal belum menjawab bagaimana penyewa menilai unit dan mengatur pengambilannya.',
                    'Iklan menyaring barang dari jenis, harga, dan lokasi. Namun, fungsi sering harus diperiksa melalui foto tambahan atau kunjungan. Sementara itu, dimensi dan akses masuk menentukan apakah barang bisa dibawa ke ruang yang tersedia.',
                    'Toko fisik membantu pembeli memeriksa barang. Sebaliknya, percakapan memungkinkan pembeli meminta rincian dari jauh. Pembeli tetap perlu menyatukan informasi kondisi, ukuran, dan angkutan sebelum membuat janji.'
                ]
            for text in paragraphs:para(text)
            if i==1:
                table('Hasil yang mengarahkan keputusan',['Bukti atau hasil','Implikasi'],[
                    ['14 dari 17 menyebut kondisi barang','Utamakan foto detail dan catatan per unit'],
                    ['{{SOM}} proyeksi pendapatan marketplace tahun ketiga','Nilai mengikuti stok, pesanan tuntas, dan kapasitas klaster'],
                    ['{{NPV}} NPV pada WACC {{WACC}}','Uji ekonomi pilot sebelum menyetujui perluasan'],
                ])
                nav('bab5','Lihat strategi keuangan dan keputusan ekspansi')
            if i==3 and j==1:
                figure('survey','Kendala ketika mempertimbangkan iklan tertentu','Sumber: survei final 26 November 2026; n = 17; pilihan ganda.',3.75)
            if i==4:
                figure('product','Dua sisi pengalaman katalog pada prototipe','Tangkapan asli prototipe. Panel penutupan pesanan menunjukkan rancangan operasi.',8.7)
                table('Pemeriksaan sebelum mengatur serah terima',['Informasi','Yang diperiksa'],[
                    ['Kondisi','Detail cacat dan fungsi yang diberitahukan penjual'],
                    ['Ukuran','Dimensi barang dan kesesuaian dengan ruang'],
                    ['Cara menerima','Lokasi, pilihan angkut, ketersediaan, dan jadwal'],
                ])
                lead('Bukti melekat pada unit hingga barang diterima')
                para('Tim menyimpan foto kondisi dan ukuran yang disepakati saat pesanan dikonfirmasi. Saat barang diterima, pembeli dan penjual bisa merujuk pada catatan unit yang sama. Tim meminta konfirmasi ulang jika foto, harga, atau pilihan terima berubah. Dengan begitu, laporan selisih dapat diperiksa terhadap informasi yang dipakai pembeli ketika membuat keputusan.')
            if i==5:
                figure('vpc','Proposisi nilai bagi pembeli dan penjual','Rancangan pilot. Profil pasokan berulang masih menunggu validasi penjual.',10.1)
                para('Pembeli dapat memutuskan perlu datang atau melanjutkan pencarian setelah membaca bukti yang tersedia. Sementara itu, penjual menyiapkan satu catatan yang hendak dipakai berulang sampai serah terima. Perbedaan kondisi saat barang diterima menjadi dasar untuk membuka kembali catatan pesanan.')
            if i==6:
                table('Urutan konfirmasi pesanan',['Tahap','Yang terjadi','Bukti untuk langkah berikut'],[
                    ['Dokumentasi','Penjual mengisi foto kondisi, dimensi, dan jadwal','Bukti asli per unit'],
                    ['Pemeriksaan','Pembeli menilai barang dan memilih cara menerima','Unit, lokasi dan opsi penerimaan'],
                    ['Konfirmasi','Tim dan penjual memeriksa stok, waktu dan rute bila perlu','Stok dan slot tercatat'],
                    ['Serah terima','Pembeli mengambil barang atau penyedia mengantar','Catatan terima, kondisi dan pengecualian'],
                    ['Penutupan','Dukungan memeriksa selisih dan mencatat penyelesaian','Status akhir dan penerimaan bersih'],
                ])
                lead('Pembeli melihat biaya sebelum berkomitmen')
                para('Pembeli memilih ambil sendiri ketika ukuran dan akses memungkinkan. Jika memilih kirim, ongkos mengikuti rute dan ukuran barang yang sudah dikonfirmasi. Karena itu, penawaran yang tampak menarik tetap harus memenuhi syarat serah terima sebelum pesanan ditutup.')
                nav('katalog','Lihat contoh layar katalog dan pemeriksaan pada Gambar 2')
                para('Tim menghubungkan status pembayaran dengan catatan serah terima dan menyimpan alasan perubahan. Catatan ini dipakai ketika pembeli menunda pengambilan atau melaporkan selisih kondisi.')
            if i==7 and j==0:
                figure('spz','Bingkai masukan dan keluaran SPZ dari uji lokal','Uji satu kursi, satu perangkat. Bagian bentuk masih kabur pada penampil.',5.65)
            if i==8 and j==0:
                table('Alur kerja dua lajur dan jalur pengecualian',['Lajur pelanggan','Lajur operasi','Jalur pengecualian'],[
                    ['Penjual memasukkan bukti unit','Katalog memeriksa kelengkapan','Listing dikembalikan dengan bagian yang perlu diperbaiki'],
                    ['Pembeli memilih cara terima','Pesanan memeriksa stok, jadwal, dan opsi angkut','Tawarkan slot atau rute lain bila tersedia'],
                    ['Pembeli mengonfirmasi kondisi','Dukungan menutup pengaduan dan mencatat status','Periksa versi foto dan kondisi sebelum penyelesaian dana'],
                ])
            if i==8 and j==1:
                lead('Tiga sumber daya yang menentukan pesanan')
                para('Pasokan harus bisa dikonfirmasi, tim layanan perlu menangani jadwal, dan calon pembeli membutuhkan informasi yang cukup. Pekerjaan media berjalan dalam antrean terpisah. Dengan begitu, banyaknya percobaan rekonstruksi tidak menentukan jumlah listing yang boleh terbit.')
            if i==9 and j==1:
                figure('roadmap','Peta jalan dan kesiapan tiap fase','Rencana operasi dan pembiayaan bersyarat, 2027 dan seterusnya.',8.1)
            if i==10 and j==0:
                figure('kpi','Indikator pilot dan dasar pengukuran','Penyebut ditetapkan sebelum mengumpulkan data transaksi pilot.',6)
            if i==10 and j==1:
                figure('risiko','Peta risiko dan pemilik respons','Klasifikasi kualitatif awal, ditinjau setelah pilot.',6.45)
        continue
    p=later[i]
    h(p['title'],name={12:'pasar',23:'kelayakan',24:'risikomodel'}.get(i))
    for txt in p['paragraphs']: para(txt)
    if p['figure']:
        fi=p['figure']
        credit='Sumber: workbook proyeksi LihatDulu. Nilai adalah hasil model.' if fi in {'market','keuangan','risk-chart'} else 'Visual konsep yang dibuat untuk proposal. Kegiatan belum berlangsung.' if fi.startswith('mock') else 'Sumber: rancangan LihatDulu. Templat BCC diadaptasi ke format A4.'
        maxh={12:7.1,13:6.7,14:6.7,15:8.5,16:8.5,17:8.5,18:6.8,23:5.0,24:5.2}.get(i,7.5)
        if fi=='risk-chart' and mode and not path_for(fi).exists(): pass
        else:figure(fi,p['label'],credit,maxh)
    if p['table']: table(*p['table'])
    for txt in p['after']:para(txt)
    if i==23:
        nav('lampirane','Lihat rekonsiliasi model dan komponen CAPM di Lampiran E')
    if i==19:
        figure('orders-chart','Pesanan selesai pada tiga skenario','Proyeksi yang merekonsiliasi volume, nilai transaksi, dan biaya pemenuhan.',4.25)
    if i==20:
        table('Ekonomi pesanan pada tahun ketiga',['Ukuran','Skenario dasar'],[
            ['Kontribusi sebelum akuisisi','{{CONTRIB_PRE_CAC}} per pesanan'],
            ['Kontribusi setelah akuisisi','{{CONTRIB_POST_CAC}} per pesanan'],
        ])
        para('Tambahan pesanan tidak menutup biaya bila pengeluaran akuisisi melebihi kontribusi. Karena itu, pilot menguji batas biaya akuisisi bersama harga dan kapasitas dukungan. Harga penawaran publik hanya dipakai sebagai tolok ukur awal.')
        para('Selisih sekitar Rp24.932 per pesanan selesai pada tahun ketiga adalah beban akuisisi yang dialokasikan oleh model. Untuk menilai kinerja kanal, tim memakai pembeli baru yang benar-benar menyelesaikan pesanan, sesuai penyebut pada Bab IV. Kedua ukuran menjawab keputusan anggaran yang berbeda.')
    if i==21:
        figure('cash-chart','Lintasan arus kas proyek menurut skenario','Arus kas proyek sebelum pembiayaan. Rp juta nominal.',4.55)
    if i==22:
        table('Batas yang menentukan kelanjutan operasi',['Ukuran dalam skenario dasar','Hasil'],[
          ['Kekurangan dana maksimum dengan cadangan','{{FUND_GAP}}'],
          ['Kas pertama negatif pada jadwal pendanaan model','{{CASH_NEGATIVE}}'],
        ])
        para('Selisih ini menentukan alasan untuk membatasi komitmen. Apabila biaya akuisisi belum turun dan kontribusi belum positif, tim mempertahankan uji dalam klaster awal. Implikasi ini berlaku meskipun pendanaan berikutnya tersedia.')
    if i==25:
        para('Dalam skenario dasar, pengeluaran untuk melayani dan memperoleh pesanan menekan kontribusi. Karena itu, ekspansi membutuhkan bukti bahwa biaya per pelanggan efektif dapat turun. Tim melaporkan hasil pilot terhadap target sebagai dasar membenahi penawaran, memperketat wilayah, atau menahan ekspansi.')

fresh('Daftar pustaka',1,'referensi')
for s in narrative['sources']:ref_note(s['apa'],s['url'])
for title,url in [
    ('Badan Pusat Statistik. (2026). Pengeluaran untuk konsumsi penduduk Indonesia, Maret 2026 (Tabel 3.4, hlm. 40).', 'https://www.bps.go.id/id/publication/2026/10/05/4e167126f0dc9e67c8e602b2/pengeluaran-untuk-konsumsi-penduduk-indonesia-maret-2026.html'),
    ('Badan Pusat Statistik. (2025). Jumlah penduduk berumur 5 tahun ke atas menurut wilayah metropolitan, status komuter, dan jenis kelamin.', 'https://www.bps.go.id/en/statistics-table/1/MjMwOCMx/jumlah-penduduk-berumur-5-tahun-ke-atas-menurut-wilayah-metropolitan-status-komuter-dan-jenis-kelamin.html'),
    ('OLX Indonesia. (2026, 26 November). Listing furnitur bekas Depok [Sampel penawaran per kategori].','https://www.olx.co.id/depok-kota_g4000024/q-bekas-furnitur'),
    ('LihatDulu. (2026). Bukti pemrosesan lokal dan prototipe katalog [Repositori kode dan artefak arsip].','https://github.com/Fafauzif/Lihatdulu/tree/cbf69f0'),
]:ref_note(title,url)

fresh('Lampiran A Model bisnis',1,'lampirana')
nav('bab2','Kembali ke model bisnis')
figure('bmc','Kanvas model bisnis LihatDulu','Dasar model bisnis, proses pilot, dan sumber pendapatan yang diajukan.',11.5)
table('Keterkaitan keputusan di dalam kanvas',['Keputusan','Hubungan dengan operasi'],[
    ['Hubungan pelanggan','Versi bukti yang sama dipakai dalam katalog dan dukungan'],
    ['Mitra utama','Reseller dan calon penyedia angkut harus memenuhi syarat kesiapan'],
    ['Pendapatan','Acara dan promosi diukur melalui pesanan yang selesai'],
])
para('Marketplace menempatkan barang pada penjual sampai serah terima. Tim menyediakan perangkat listing dan dukungan untuk menghubungkan penawaran dengan keputusan menerima barang. Karena biaya layanan mengikuti pesanan yang tuntas, kesiapan pasokan dan serah terima membatasi pertumbuhan.')

fresh('Lampiran B Survei dan persona',1,'lampiranb')
nav('validasi','Kembali ke validasi masalah')
para('Survei final berisi 60 respons dan 56 di antaranya berasal dari mahasiswa. Sebanyak 32 mencari furnitur bekas secara daring dalam 12 bulan sebelumnya. Tujuh belas mempertimbangkan sedikitnya satu iklan tertentu dan semuanya berstatus mahasiswa. Karena itu, penyebut modul pengalaman adalah 17, sedangkan penyebut evaluasi demo adalah 60 pasangan lengkap.')
figure('survey-actions','Tindakan setelah mempertimbangkan iklan','Pilihan ganda; n = 17. Aktivitas pada penawaran historis.',6.8)
table('Hasil akhir pada penawaran historis',['Hasil','Responden'],[
    ['Membeli barang pada iklan','6'],['Membeli barang bekas lain','2'],['Membeli barang baru','1'],['Masih mempertimbangkan','4'],['Batal membeli furnitur yang dicari','4'],
])
para('Keputusan tersebut terjadi pada kanal asal responden. Sementara itu, kesesuaian ruang dan biaya angkut dapat muncul bersamaan dalam satu pengalaman. Karena pilihan kendala dapat dijawab lebih dari sekali, persentase antarjawaban tidak dijumlahkan sebagai proporsi responden yang berbeda.')

fresh('B.1 Respons terhadap bukti kondisi')
figure('survey-confidence','Perubahan keyakinan dari awal ke tahap catatan kondisi','Responden melihat contoh yang sama dalam urutan tetap; n = 60.',6.7)
table('Rencana tindakan dalam contoh iklan',['Tindakan','Tahap awal','Setelah bukti kondisi'],[
    ['Meminta informasi','30','13'],['Mengatur kunjungan','9','24'],['Menghubungi untuk membeli atau mengambil','3','10'],['Menyimpan','14','8'],['Melewati','3','3'],['Belum tahu','1','2'],
])
para('Tahap kedua memperlihatkan catatan kondisi dan foto dekat secara bersamaan. Sepuluh orang menjadi kurang yakin dan 16 tidak berubah. Karena seseorang dapat semakin yakin untuk melewati barang, perubahan keyakinan dibaca bersama rencana tindakan. Rancangan ini belum mengisolasi efek foto, catatan, 3D, atau pratinjau ruang.')
para('Analisis ordinal minat beli memakai 52 pasangan setelah delapan respons tanpa penilaian pada salah satu tahap dikeluarkan. Dari pasangan itu, 27 naik, 18 tetap, dan tujuh turun. Perubahan ini adalah respons pada contoh iklan, sehingga tidak menjadi parameter konversi atau tarif.')

fresh('B.2 Persona kerja dan wawancara penjual')
figure('persona-pembeli','Persona kerja pembeli kos','Persona komposit kebutuhan. Rujukan: modul pengalaman iklan, n = 17.',6.6)
figure('persona-penjual','Hipotesis persona pemasok lokal','Profil usulan untuk diperdalam melalui satu wawancara penjual.',6.6)
lead('Ruang untuk wawancara penjual')
p=note('Placeholder tata letak. Isi berikut menunggu wawancara penjual dan persetujuan atas penggunaan kutipan.')
p.runs[0].italic=True
p=para('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer malesuada massa at nunc aliquet, sed placerat erat posuere. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae.')
p.runs[0].italic=True

fresh('Lampiran C Prototipe dan uji pemrosesan lokal',1,'lampiranc')
nav('buktiteknis','Kembali ke pembuktian konsep')
for p in append['technical_paragraphs'][:3]:para(p)
figure('spz','Masukan video dan penampil keluaran dari proses yang sama','Sumber: arsip Golden. Konfigurasi perangkat dan parameter terikat pada uji ini.',7.6)
fresh('C.1 Tujuh proses pada satu kursi')
for p in append['technical_paragraphs'][3:]:para(p)
rd=append['technical_run_table_data']
if isinstance(rd,dict): rows=[list(map(str,r)) for r in rd.get('rows',[])]
else: rows=[list(map(str,r)) for r in rd if isinstance(r,list)]
if not rows:
    data=json.loads((work/'product'/'bukti-pemrosesan-lokal.json').read_text())
    rows=[]
    for x in data['tables']:
        dec=lambda v:f'{v:.2f}'.replace('.',',')
        rows.append([x['id'],dec(x['seconds_clip'])+' detik',f"{x['frames_registered']}/{x['frames_extracted']}",dec(x['seconds_processing'])+' detik',dec(x['spz_mib'])+' MiB'])
if rows and len(rows[0])>=5:table('Rekaman dan hasil pemrosesan lokal',['Rekaman','Durasi','Bingkai','Proses','SPZ'],[r[:5] for r in rows])
else:
    table('Ruang lingkup bukti uji pemrosesan',['Ukuran','Hasil'],[
        ['Cakupan','7 keluaran dari rekaman satu kursi'],
        ['Proses','244,142–332,873 detik pada perangkat uji'],
        ['Ukuran','0,34–0,68 MiB'],
        ['Rekaman Golden','76 dari 76 bingkai, 291,281 detik, sekitar 0,52 MiB'],
        ['Batas','Sejumlah area kabur. Satu rekaman perlu ekstraksi ulang.'],
    ])
para('Satu pengambilan memerlukan ekstraksi ulang agar jumlah bingkai yang cukup tercapai. Reduksi atau perapian aset berjalan setelah proses registrasi. Karena model yang dapat dibuka belum tentu berguna untuk pembeli, uji lanjutan harus mengevaluasi bagian yang hilang dan konsistensi antarkategori.')
for l in append['technical_links']:
    if isinstance(l,dict):ref_note(l.get('label',l.get('title','Arsip teknis')),l.get('url',''))

fresh('Lampiran D Pasar dan pesaing',1,'lampirand')
nav('pasar','Kembali ke ukuran pasar')
figure('swot','Implikasi SWOT untuk eksperimen pasar','Temuan pembeli, rancangan produk, dan hipotesis pasokan ditandai sesuai jenis bukti.',7.2)
table('Input skenario ukuran pasar',['Input','Dasar atau batas interpretasi'],[
    ['Belanja kategori mebel','Belanja nasional, mencakup kategori lebih luas dari produk bekas'],
    ['Bagian barang bekas','Asumsi dengan rentang, tidak diperoleh dari survei'],
    ['Cakupan wilayah','Proksi geografi dan keterlayanan. Tidak diartikan sebagai pangsa pasar pasti'],
    ['Nilai per pesanan dan tarif','Harga penawaran sebagai titik awal. Harga transaksi serta kesediaan bayar diuji saat pilot'],
    ['Pesanan selesai tahun ketiga','Dibatasi permintaan, pasokan dan kapasitas per model'],
])
para('SOM tahun ketiga adalah {{SOM}} dan sama dengan pendapatan marketplace 2029 di workbook. Proyeksi tersebut dapat diperbarui ketika biaya, stok yang betul-betul tersedia, dan hasil transaksi sudah diketahui. Hindari menggabungkan belanja barang, pendapatan jasa, dan langganan karena ketiganya memiliki dasar hitung berbeda.')

fresh('Lampiran E Model dan rekonsiliasi',1,'lampirane')
nav('kelayakan','Kembali ke kelayakan proyek')
table('Peta bagian workbook yang mendasari proposal',['Bagian proposal','Area workbook','Ukuran yang diperiksa'],[
    ['Bab II dan IV','Ukuran Pasar B13, B15, B16','TAM, SAM, dan SOM'],
    ['Bab III','Operasi bulanan dan Laporan D/F/M','Pesanan (baris 7) dan GMV (baris 11)'],
    ['Bab V','Laporan D/F/M dan Ringkasan C11:C18','Pendapatan, laba, FCFF, kelayakan serta kebutuhan dana'],
    ['Bab V','CAPM B7:B22, Pendanaan A7:I9, Monte Carlo A6:E12','Biaya modal, penerimaan modal, dan sebaran risiko'],
])
table('Komponen CAPM dalam model',['Komponen','Nilai contoh skenario dasar','Interpretasi'],[
    ['Yield SBN IDR','{{SBN}}','Yield pemerintah pada tanggal acuan'],
    ['Spread gagal bayar','{{DEFAULT_SPREAD}}','Dikurangkan untuk proksi bebas risiko'],
    ['Beta tanpa utang','{{BETA}}','Pembanding model usaha asset-light'],
    ['ERP pasar matang','{{ERP}}','Premi pasar sebelum penyesuaian negara'],
    ['Premi risiko Indonesia','{{CRP}}','Eksposur Indonesia dalam rupiah'],
    ['Ke dan WACC','{{WACC}}','Utang pendanaan nol'],
])
para('Parameter dan sumber per komponen tercantum pada workbook. Pembanding beta merupakan proksi dan hasilnya sensitif terhadap pemilihan kelompok usaha. Karena itu, angka CAPM berfungsi sebagai ambang analisis proyek dalam model. Ia tidak mewakili target pengembalian investor tertentu.')

fresh('E.1 Risiko skenario, likuiditas dan pembiayaan')
table('Pemeriksaan yang harus dibaca sebelum menyimpulkan kelayakan',['Pemeriksaan','Kondisi keputusan'],[
    ['Sensitivitas dua arah','Pusat matriks sama dengan Base pada horizon dan definisi arus kas yang sama'],
    ['Pendanaan terbatas','Kas minimum dihitung sebelum mengasumsikan tambahan modal di luar rencana'],
    ['IRR','Percobaan tanpa solusi atau kemungkinan lebih dari satu solusi tidak dianggap bernilai nol'],
    ['Dana titipan','Dana barang dan angkut tidak dihitung sebagai kas bebas'],
    ['Pencairan modal','Dipisahkan dari arus kas proyek dan mengikuti milestone'],
])
para('Ringkasan simulasi memakai horizon yang sama hingga akhir 2036. Seed dan sebaran driver tercantum pada model. Uji sensitivitas menilai perubahan penggerak yang masuk akal secara operasional. Sementara itu, hasil yang dinyatakan sebagai peluang berlaku bersyarat pada asumsi model.')
para('Dari 10.000 lintasan, satu memiliki IRR yang terdefinisi, yaitu −74,16%. Tidak ada lintasan yang melampaui biaya modal. Seluruh lintasan mengalami kekurangan terhadap cadangan kas minimum pada jadwal pendanaan yang dimodelkan. Karena itu, tim perlu mengurutkan pengeluaran dan menguji keterlambatan pendanaan sebelum menambah staf atau wilayah.')
if metrics.get('FINANCE_SOURCES'):
    for sx in metrics['FINANCE_SOURCES']:
        ref_note(sx.get('title','Sumber model'),sx.get('url',''))

fresh('Lampiran F Kendali mutu dan pemenuhan',1,'lampiranf')
nav('alurkerja','Kembali ke alur kerja operasi')
para(append['operations_intro'])
orows=append['operations_table_rows']
orows[1][0]='Jadwal ambil'
orows[0][0]='Stok dan slot'
orows[0][1]='Penjual mengonfirmasi stok, lalu tim pesanan mencatat slot serta versi penawaran.'
orows[0][2]='Pesanan dengan stok dan slot pasti dibagi semua pesanan masuk.'
table(append['operations_table_caption'],['Tahap']+append['operations_table_columns'][1:],orows,[2.35,5.1,4.05,4.4])
para('Ukuran pada tabel merupakan rancangan pengukuran pilot. Ambang numerik Gambar 6 dipakai sebagai sasaran awal dan akan diuji dengan hasil operasi.')
para('Pembayaran dan pencairan akan diatur melalui penyedia berizin setelah persyaratan bisnis disepakati. Dalam pilot, tim memeriksa dukungan untuk penjual perorangan, pencairan per transaksi, rekonsiliasi, dan pembatalan sebelum mengaktifkan pembayaran dalam aplikasi.')
lead('Ukuran sebelum menambah wilayah')
para('Tim menguji target awal di Gambar 6 dengan log stok, slot, serah terima, dan keluhan. Biaya akuisisi per pembeli pertama dengan pesanan selesai juga harus berada di bawah kontribusi sebelum akuisisi. Selama bukti belum cukup, tim memperbaiki tahapan yang paling sering menghentikan pesanan dan menunda wilayah berikutnya.')

fresh('Lampiran G Kalender pemasaran dan instrumen atribusi',1,'lampirang')
nav('bab4','Kembali ke strategi pemasaran')
table('Peta kegiatan dan batas eksternal',['Waktu','Kegiatan','Data yang ditinjau'],[
    ['Bulan 0–6','Akuisisi reseller dan penghuni yang pindah di klaster UI Depok','Listing siap, stok aktif, pesanan selesai'],
    ['Bulan 7–12','Konten kreator dan tautan ke koleksi lokal','Pendatang, konfirmasi stok, biaya per pesanan selesai'],
    ['Tahun 2+','Bursa Pindahan setelah kesiapan pemenuhan','Listing terbit, penyelesaian 30 hari, biaya aktual acara'],
])
table('Rekam jejak kampanye ke transaksi',['Peristiwa','Bukti untuk atribusi'],[
    ['Pengunjung membuka katalog','ID kanal pada tautan kampanye dan wilayah katalog'],
    ['Penjual mengajukan penawaran','Tanggal, status listing, dan asal bantuan'],
    ['Pesanan berakhir','Status selesai, tanggal, dan kanal utama dalam jendela 30 hari'],
])
para('Reservasi hanya dicatat sebagai tanda minat sampai transaksi tuntas. Selanjutnya, tim mengaitkan satu pesanan ke satu sumber utama agar biaya promosi tidak dibagi dua kali. Apabila acara menunjukkan minat tetapi tidak menghasilkan pengambilan, evaluasi dimulai dari stok, jadwal dan biaya angkut.')

# Populate genuine Word fields with navigable cached result paragraphs.
def index_field(start,rows,code,default_style):
    if not rows: return
    preceding=start
    for i,(name,title,level,page) in enumerate(rows):
        pn=d.add_paragraph(style=f'TOC {min(level,3)}' if default_style=='TOC' else default_style)
        preceding.addnext(pn._p);preceding=pn._p
        if default_style=='TOC' and level>1:pn.paragraph_format.left_indent=Cm(.34*(level-1))
        if i==0:
            for tag,txt in [('begin',''),('instr',code),('separate','')]:
                rr=pn.add_run()
                el=OxmlElement('w:instrText' if tag=='instr' else 'w:fldChar')
                if tag=='instr':el.set(qn('xml:space'),'preserve');el.text=txt
                else:el.set(qn('w:fldCharType'),tag)
                rr._r.append(el)
        link(pn,title,anchor=name)
        pn.add_run('\t'+str(folio_cache.get(name,page)))
        if i==len(rows)-1:
            rr=pn.add_run();el=OxmlElement('w:fldChar');el.set(qn('w:fldCharType'),'end');rr._r.append(el)

# Top-level chapter divisions keep the front contents short; subheadings remain navigable in Word's outline.
index_field(toc_anchor,[r for r in toc if r[2]==1], ' TOC \\o "1-1" \\h \\z ', 'TOC')
index_field(fig_anchor,figlist,' TOC \\h \\z \\c "Gambar" ','Table of Figures')
index_field(tbl_anchor,tblist,' TOC \\h \\z \\c "Tabel" ','Table of Figures')
d.core_properties.title='LihatDulu Proposal Bisnis UISP16'
d.core_properties.subject='Marketplace furnitur rumah tangga bekas'
d.core_properties.keywords='furnitur bekas, UI Depok, UISP16, marketplace, proyeksi keuangan'
if missing and not mode: raise RuntimeError('Missing verified metrics: '+', '.join(sorted(missing)))
output.parent.mkdir(parents=True,exist_ok=True)
d.save(output)
print(f'{output} | {cursor} nominal pages | {len(figlist)} figures | {len(tblist)} tables')
(work/'proposal_index.json').write_text(json.dumps({'toc':toc,'figlist':figlist,'tblist':tblist,'missing_metrics':sorted(missing)},ensure_ascii=False,indent=2))
