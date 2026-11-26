"""Fill native OOXML chart caches from local worksheet references."""
from collections import defaultdict
from pathlib import Path
import re
import sys
from zipfile import ZipFile

from lxml import etree
from openpyxl import load_workbook
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string

C='{http://schemas.openxmlformats.org/drawingml/2006/chart}'
W='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
BOOK='xl/workbook.xml'
PRINT_AREAS={'Ringkasan':'$A$1:$I$27','Laporan':'$A$1:$M$66','Pendanaan':'$A$1:$I$27','CAPM':'$A$1:$E$26',
             'Ukuran Pasar':'$A$1:$D$19','Sensitivity':'$A$1:$G$27','Monte Carlo':'$A$1:$L$50'}
RANGE=re.compile(r"(?P<sheet>'(?:[^']|'')+'|[^!]+)!(?P<start>[A-Z]+[0-9]+)(?::(?P<end>[A-Z]+[0-9]+))?$")
source,target=map(Path,sys.argv[1:3])
if source.resolve()==target.resolve(): raise ValueError('Write the refreshed caches to a separate file')

with ZipFile(source) as xls:
    chart_parts={entry:etree.fromstring(xls.read(entry)) for entry in xls.namelist() if re.search(r'/charts/chart\d+\.xml$',entry)}
    references=defaultdict(list)
    for entry,chart in chart_parts.items():
        for ref,cache in (('numRef','numCache'),('strRef','strCache')):
            for node in chart.iter(C+ref):
                formula=node.findtext(C+'f','').replace('$','')
                match=RANGE.fullmatch(formula)
                if not match: raise ValueError(f'Unrecognized reference in {entry}: {formula}')
                sheet=match.group('sheet').strip("'").replace("''", "'")
                a,b=(coordinate_from_string(v) for v in (match.group('start'),match.group('end') or match.group('start')))
                r1,r2=a[1],b[1]; c1,c2=column_index_from_string(a[0]),column_index_from_string(b[0]);
                references[sheet].append((node,cache,r1,c1,r2,c2))
    book=load_workbook(source,read_only=True,data_only=True)
    for sheet, specs in references.items():
        worksheet=book[sheet]; last=max(s[4] for s in specs); right=max(s[5] for s in specs)
        values=list(worksheet.iter_rows(min_row=1,max_row=last,min_col=1,max_col=right,values_only=True))
        for node,kind,r1,c1,r2,c2 in specs:
            flat=[value for row in values[r1-1:r2] for value in row[c1-1:c2]]
            cache=node.find(C+kind)
            if cache is None:
                cache=etree.SubElement(node,C+kind)
            else:
                for item in list(cache):
                    if item.tag != C+'formatCode': cache.remove(item)
            if kind=='numCache' and cache.find(C+'formatCode') is None:
                etree.SubElement(cache,C+'formatCode').text='General'
            etree.SubElement(cache,C+'ptCount',val=str(len(flat)))
            for i,value in enumerate(flat):
                if value is None: continue
                if kind=='numCache' and not isinstance(value,(int,float)):
                    raise ValueError(f'Expected numeric cache values at {sheet} row {r1}: {value!r}')
                assigned=str(value)
                etree.SubElement(etree.SubElement(cache,C+'pt',idx=str(i)),C+'v').text=assigned
    print_areas=dict(PRINT_AREAS)
    if book['Monte Carlo']['Q55'].value is not None:
        print_areas.update({'Monte Carlo':'$A$1:$Q$54','Sensitivity':'$A$1:$I$27'})
    metadata=etree.fromstring(xls.read(BOOK))
    sheets=metadata.find(W+'sheets')
    names=metadata.find(W+'definedNames')
    if names is None:
        names=etree.Element(W+'definedNames')
        next_order={'calcPr','oleSize','customWorkbookViews','pivotCaches','smartTagPr','smartTagTypes','webPublishing','fileRecoveryPr','webPublishObjects','extLst'}
        insert_at=next((i for i,el in enumerate(metadata) if etree.QName(el).localname in next_order),len(metadata))
        metadata.insert(insert_at,names)
    for idx,sheet in enumerate(sheets):
        name=sheet.get('name')
        if name not in print_areas: continue
        key=next((el for el in names if el.get('name')=='_xlnm.Print_Area' and el.get('localSheetId')==str(idx)),None)
        if key is None: key=etree.SubElement(names,W+'definedName',name='_xlnm.Print_Area',localSheetId=str(idx))
        key.text=f"'{name}'!{print_areas[name]}"
    chart_parts[BOOK]=metadata
    with ZipFile(target,'w') as updated:
        for entry in xls.infolist():
            data=etree.tostring(chart_parts[entry.filename]) if entry.filename in chart_parts else xls.read(entry)
            updated.writestr(entry,data)
    print(f'{len(chart_parts)-1} native charts and {len(print_areas)} print areas updated in {target}')
