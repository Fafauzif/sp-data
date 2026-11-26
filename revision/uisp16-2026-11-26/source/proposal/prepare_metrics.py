from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import json

w=Path(__file__).resolve().parent
root=w.parent/'finance'/'results'
main=json.loads((root/'lihat_finance_metrics.json').read_text())
sc=main['scenarios']
risk=json.loads((root/'lihat_finance_risk_summary.json').read_text())
if 'summary' in risk:risk=risk['summary']
base=sc['Base']
a=base['annual']
stages={s['round'].lower():s for s in main['stages']}
months=['Desember','Januari','Februari','Maret','April','Mei','Juni','Juli','Agustus','September','Oktober','November']
ym=lambda m:f'{months[m%12]} {2026+(m+11)//12}'
def num(v,places=0):
    s=f'{abs(v):,.{places}f}'.replace(',','X').replace('.',',').replace('X','.')
    return ('−' if v<0 else '')+s
def rp(v,as_mn=False):
    if as_mn:
        return ('−' if v<0 else '')+'Rp'+num(abs(v)/1000,2)+' miliar' if abs(v)>=1000 else ('−' if v<0 else '')+'Rp'+num(abs(v),2)+' juta'
    return ('−' if v<0 else '')+'Rp'+num(abs(v))
def pc(v,p=2):return num(v*100,p)+'%'
aov=int(Decimal(str(a[1]['aov']*1e6)).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
buyer=18000
seller_rate=Decimal('0.065')
seller=int((Decimal(aov)*seller_rate).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
deliv=100000
s3=a[3]['marketplaceRevenue']
mc=risk['npv']
r={
'BASE_MARKETPLACE_Y3_REVENUE':rp(s3,True),'BASE_Y3_COMPLETED_ORDERS':num(a[3]['orders']),
'BASE_NPV':rp(base['npv'],True),'BASE_IRR':'tidak terdefinisi','BASE_INITIAL_FUNDING':rp(stages['pendiri']['amount'],True),
'TAM':rp(base['market']['tam'],True),'SAM':rp(base['market']['sam'],True),'SOM':rp(s3,True),
'BUYER_FEE':rp(buyer),'SELLER_FEE':pc(float(seller_rate),1),'AOV':rp(aov),'DELIVERY_EXAMPLE':rp(deliv),
'BUYER_TOTAL':rp(aov+buyer+deliv),'SELLER_COMMISSION':rp(seller),'SELLER_NET':rp(aov-seller),'PLATFORM_FEE':rp(buyer+seller),
'OPERATING_BEP':'belum tercapai hingga 2036','FUND_FOUNDER':rp(stages['pendiri']['amount'],True),
'FUND_PRESEED':rp(stages['pre-seed']['amount'],True),'FUND_SEED':rp(stages['seed']['amount'],True),
'FUND_TOTAL':rp(sum(x['amount'] for x in main['stages']),True)+' bruto',
'WACC':pc(base['capm']),'NPV':rp(base['npv'],True),'IRR':'Tidak terdefinisi','PAYBACK':'Belum tercapai hingga 2036',
'CROSSING':'Tidak tercapai hingga 2036','NPV_DOWNSIDE':rp(sc['Downside']['npv'],True),'NPV_UPSIDE':rp(sc['Upside']['npv'],True),
'MC_PROB':f"{num(risk['positiveNpv']['numerator'])} dari {num(risk['trials'])}",
'MC_RANGE':' / '.join(rp(mc[k],True) for k in ('p05','p50','p95')),
'SBN':pc(.07696,3),'DEFAULT_SPREAD':pc(.0152),'ERP':pc(.042),'CRP':pc(.0236),
'BETA':num(1.39/(1+(1-.2537)*.1001),3),
'CONTRIB_PRE_CAC':rp(a[3]['unitContribution']*1e6),'CONTRIB_POST_CAC':rp(a[3]['unitAfter']*1e6),
'FUND_GAP':rp(base['fundingGap'],True),'CASH_NEGATIVE':ym(main['firstNegativeBase']),
'FINANCE_SOURCES':[
 {'title':'Damodaran, A. (2026). Country risk premiums dan industry beta (vintage model).','url':'https://pages.stern.nyu.edu/~adamodar/New_Home_Page/data.html'},
 {'title':'Investing.com. (2026, 25 November). Indonesia 10-year bond yield historical data.','url':'https://www.investing.com/rates-bonds/indonesia-10-year-bond-yield-historical-data'},
 {'title':'Bank Indonesia. (2025). Peraturan Bank Indonesia Nomor 10 Tahun 2025 tentang Pengaturan Industri Sistem Pembayaran.','url':'https://jdih.bi.go.id/Web/Beranda/DetailPeraturan/1295'},
 {'title':'iPaymu. (t.t.). Tarif layanan dan ketentuan escrow.','url':'https://ipaymu.com/id/secure-transaction-escrow/'},
]
}
for yr in (1,3,10):
    for k,field in {'ORDERS':'orders','GMV':'gmv','REV':'marketplaceRevenue','B2B':'b2bRevenue','NET':'earnings','FCF':'fcff'}.items():
        v=a[yr][field]
        r[f'{k}_Y{yr}']=num(v) if k=='ORDERS' else rp(v,True)
(w/'proposal_metrics.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
simple={}
for k,scn in sc.items():
    simple[k.lower()]={f:[v[f] for v in scn['annual']] for f in ('orders','fcff','cash','gmv','marketplaceRevenue')}
(w/'model_metrics_raw.json').write_text(json.dumps(simple))
print('Bound',len(r),'metrics')
