"""Reconcile saved core formulas and risk snapshots to the reference evaluator."""
import importlib.util
import json
import math
import sys
from pathlib import Path

qa=importlib.util.spec_from_file_location('workbook_qa','/tmp/ldfin/verify-workbook.py'); m=importlib.util.module_from_spec(qa); qa.loader.exec_module(m)
required={
 'Ringkasan':{'C6','C7','C11','C12','C13','C17','C18'},
 'Ukuran Pasar':{'B13','B15','B16'},
 'QA Model':{f'C{i}' for i in range(7,18)},
 'Sensitivity':{'D9','B21','B22','B23'},
 'Monte Carlo':{'A55','Q55','A56','I56','Q56','A10055','I10055','Q10055','B56','F56','B10055','F10055',
              'B7','C7','D7','E7','J7','D15','D19','M17','M18','AE10055'},
 'Asumsi':{'A110','A111','A112','A117','B118'},
}
metrics=json.loads(Path('/mnt/data/lihat_finance_metrics.json').read_text())
risk=json.loads(Path('/tmp/ldfin/risk-monthly-gap.json').read_text())
sim=risk['simulation']; base=metrics['scenarios']['Base']; run=m.xlsx_qa(Path(sys.argv[1]),required)
get=lambda sheet,cell:run['selected_cells'].get(sheet+'!'+cell,{}).get('cached_value')
active,control=(get('Ringkasan',cell) for cell in ('C6','C7'))
result=metrics['scenarios'][active] if control!='Terbatas' else next(iter(metrics['stress'].values()))
if control=='Terbatas':
    if 'withoutFollowOn' in metrics['stress']: result=metrics['stress']['withoutFollowOn']
    else:
        for key,r in metrics['stress'].items():
            if 'tanpa' in key.lower() or 'no' in key.lower(): result=r; break
expected={
 'Ringkasan':{'C11':result['capm'],'C12':result['npv'],'C13':result['irr'] if result['irr'] is not None else 'Tidak terdefinisi','C17':result['cashMin'],'C18':result['fundingGap']},
 'Ukuran Pasar':{'B13':result['market']['tam'],'B15':result['market']['sam'],'B16':result['annual'][3]['marketplaceRevenue']},
 'QA Model':{f'C{i}':'LULUS' for i in range(7,18)},
}
if get('Sensitivity','D9') is not None: expected['Sensitivity']={'D9':base['npv']}
if get('Monte Carlo','A56') is not None:
    if get('Monte Carlo','Q55') is not None:
        expected['Monte Carlo']={'A56':1,'A10055':10000,'I56':sim['rows'][0]['npv'],'I10055':sim['rows'][-1]['npv'],
        'Q56':sim['rows'][0]['fundingGap'],'Q10055':sim['rows'][-1]['fundingGap'],'C7':sim['summary']['npv']['p50'],'E7':10000,'J7':0}
    else:
        expected['Monte Carlo']={'A56':1,'A10055':10000,'B56':sim['rows'][0]['npv'],'B10055':sim['rows'][-1]['npv'],
        'F56':sim['rows'][0]['fundingGap'],'F10055':sim['rows'][-1]['fundingGap'],'D7':sim['summary']['npv']['p50'],'B7':10000,'D15':0,'D19':1}
errors=[]; values={}
for sheet,cells in expected.items():
    values[sheet]={}
    for cell,want in cells.items():
        observed=get(sheet,cell); values[sheet][cell]=observed
        ok=(isinstance(observed,(int,float)) and math.isclose(observed,want,rel_tol=1e-7,abs_tol=1e-6)) if isinstance(want,(int,float)) else observed==want
        if not ok: errors.append([sheet,cell,observed,want])
selected=set(expected.get('QA Model',{}))
print(json.dumps({'file':str(sys.argv[1]),'case':active,'funding_mode':control,'sheet_count':len(run['sheets']),
  'native_charts':run['native_chart_count'],'formula_error_count':len(run['formula_errors']),
  'formulas':sum(x.get('formulas',0) for x in run['sheets'].values()),'expectations':sum(map(len,expected.values())),
  'values':values,'mismatches':errors,'formula_errors':run['formula_errors']},ensure_ascii=False,indent=2))
sys.exit(bool(errors or run['formula_errors']))
