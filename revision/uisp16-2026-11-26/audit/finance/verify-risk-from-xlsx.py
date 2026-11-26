"""Compare all 10,000 cached XLSX draws with independently regenerated draw JSON."""
from pathlib import Path
import sys,json,math
from openpyxl import load_workbook
from zipfile import ZipFile
from lxml import etree
from collections import Counter
risk=json.loads(Path('/tmp/ldfin/risk-monthly-gap.json').read_text())['simulation']
file=sys.argv[1]; wb=load_workbook(file,read_only=True,data_only=True)
ws=wb['Monte Carlo']; width=len(list(ws.iter_rows(min_row=55,max_row=55,values_only=True))[0]); full=width>=31
keys=('seller','demand','fee','aov','cost','completion','capex')
errors=[]; number=0
for number,(row,r) in enumerate(zip(ws.iter_rows(min_row=56,max_row=10055,max_col=31 if full else 6,values_only=True),risk['rows'],strict=True),1):
    if full:
        exp=[r['id'],*(r['multipliers'][k] for k in keys),r['npv'],r['irr'],r['irrStatus'],r['crossing'],r['capm'],r['funding'],r['cashMin'],r['cashMinUnfunded'],r['fundingGap'],int(r['fundingAtRisk']),r['endingOrders'],*r['cashflows'],r['fundingNeeded']]
    else:
        exp=[r['id'],r['npv'],r['irr'],r['crossing'],r['cashMin'],r['fundingGap']]
    for col,(a,b) in enumerate(zip(row,exp,strict=True),1):
        ok=(isinstance(a,(int,float)) and math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-9)) if isinstance(b,(int,float)) else a==b
        if not ok: errors.append((number,col,a,b))
    if len(errors)>15:break
with ZipFile(file) as z:
    charts=[]
    for name in z.namelist():
        if not(name.endswith('.xml') and '/charts/chart' in name): continue
        tree=etree.fromstring(z.read(name)); C='{http://schemas.openxmlformats.org/drawingml/2006/chart}'
        axis=tree.find('.//'+C+'barDir'); orient=axis.get('val') if axis is not None else None
        vals=[int(float(x.text)) for x in tree.findall('.//'+C+'val//'+C+'v')]
        charts.append({'path':name,'orientation':orient,'points':len(vals),'count':sum(vals)})
print(json.dumps({'file':file,'full_draw_schema':full,'matched_trial_rows':number,'matched_values':number*(31 if full else 6),
  'record_count_expected':len(risk['rows']),'errors':errors[:15], 'native_chart_caches':charts},ensure_ascii=False,indent=2))
sys.exit(bool(errors or number!=10000 or len(charts)!=2 or any(x['count']!=10000 for x in charts)))
