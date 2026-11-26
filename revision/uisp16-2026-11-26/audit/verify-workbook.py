"""Workbook package QA. Run after saving and again after a real calculation-engine round."""
import argparse
from collections import Counter
import json
from pathlib import Path
from posixpath import join, normpath
import re
from zipfile import ZipFile

from lxml import etree


S = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
ERR_TOKENS = re.compile(r'#(?:REF!|DIV/0!|VALUE!|NAME\?|N/A|NUM!|NULL!|SPILL!|CALC!)')
ELEMENTS = {S + tag for tag in ('c', 'pane')}


def xlsx_qa(workbook, selection):
    with ZipFile(workbook) as package:
        entries = package.namelist()
        metadata = etree.fromstring(package.read('xl/workbook.xml'))
        relations = etree.fromstring(package.read('xl/_rels/workbook.xml.rels'))
        rels = {rel.get('Id'): rel.get('Target') for rel in relations}
        sheet_info = metadata.find(S + 'sheets')
        assert sheet_info is not None, 'Missing workbook sheets'
        result = {'workbook': str(workbook), 'sheets': {}, 'selected_cells': {}, 'formula_errors': [],
                  'external_workbook_parts': [part for part in entries if re.match(r'xl/externalLinks/externalLink\d+\.xml$', part)],
                  'native_chart_count': sum(bool(re.match(r'xl/(?:drawings/)?charts/chart\d+\.xml$', part)) for part in entries),
                  'calculation_properties': {}}
        calc = metadata.find(S + 'calcPr')
        if calc is not None:
            result['calculation_properties'] = dict(calc.attrib)
        strings = []
        if 'xl/sharedStrings.xml' in entries:
            with package.open('xl/sharedStrings.xml') as stream:
                for _, item in etree.iterparse(stream, events=('end',), tag=S+'si'):
                    strings.append(''.join(part.text or '' for part in item.iter(S+'t')))
                    item.clear()
        for sheet in sheet_info:
            name = sheet.get('name')
            target = rels[sheet.get(R + 'id')]
            path = target.lstrip('/') if target.startswith('/') else normpath(join('xl', target))
            metrics = Counter()
            first_errors = []
            selected = selection.get(name, set())
            with package.open(path) as stream:
                for _, cell in etree.iterparse(stream, events=('end',), tag=tuple(ELEMENTS)):
                    if cell.tag == S+'pane':
                        if cell.get('state', '').startswith('frozen'):
                            metrics['frozen_panes'] += 1
                        continue
                    formula = cell.find(S + 'f')
                    value = cell.find(S + 'v')
                    raw = value.text if value is not None else None
                    address = cell.get('r')
                    kind = cell.get('t')
                    metrics['cells'] += 1
                    if formula is not None:
                        metrics['formulas'] += 1
                        if raw is None or raw == '':
                            if kind == 'str':
                                metrics['string_or_empty_result'] += 1
                            else:
                                metrics['formula_cache_absent'] += 1
                        if formula.text and (match := ERR_TOKENS.search(formula.text)):
                            metrics['error_tokens_in_formula'] += 1
                            if len(first_errors) < 30:
                                first_errors.append([address, 'token in formula', match.group()])
                    if kind == 'e' and raw:
                        metrics['cached_errors'] += 1
                        if len(first_errors) < 30:
                            first_errors.append([address, 'cached error', raw])
                    if address in selected:
                        cached = raw
                        if kind == 's' and raw is not None:
                            cached = strings[int(raw)]
                        elif kind == 'inlineStr':
                            cached = ''.join(part.text or '' for part in cell.iter(S+'t'))
                        elif kind in (None, 'n') and raw is not None:
                            try:
                                cached = float(raw)
                            except ValueError:
                                pass
                        result['selected_cells'][name+'!'+address] = {
                            'formula': formula.text if formula is not None else None, 'cached_value': cached,
                            'type': kind,
                        }
                    cell.clear()
                    previous = cell.getprevious()
                    while previous is not None:
                        del cell.getparent()[0]
                        previous = cell.getprevious()
            result['sheets'][name] = {**dict(metrics), 'visibility': sheet.get('state', 'visible')}
            result['formula_errors'] += [[name, *error] for error in first_errors]
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('xlsx', type=Path)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--cell', action='append', default=[], help='Workbook sheet and cell, e.g. Cover!F9')
    parser.add_argument('--require', action='append', default=[], help='Required worksheet name')
    parser.add_argument('--max-uncached', type=int)
    args = parser.parse_args()
    selection = {}
    for full in args.cell:
        sheet, address = full.rsplit('!', 1)
        selection.setdefault(sheet, set()).add(address)
    result = xlsx_qa(args.xlsx, selection)
    result['missing_sheets'] = [name for name in args.require if name not in result['sheets']]
    result['missing_selected_cells'] = sorted(set(args.cell)-result['selected_cells'].keys())
    result['uncached_formula_count'] = sum(metric.get('formula_cache_absent', 0) for metric in result['sheets'].values())
    result['cached_formula_error_count'] = sum(metric.get('cached_errors', 0) for metric in result['sheets'].values())
    if args.report:
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    overview = {key: result[key] for key in ('formula_errors', 'native_chart_count', 'external_workbook_parts',
                                            'cached_formula_error_count', 'uncached_formula_count',
                                            'missing_sheets', 'missing_selected_cells')}
    overview['sheet_count'] = len(result['sheets'])
    overview['formula_count'] = sum(metric.get('formulas', 0) for metric in result['sheets'].values())
    print(json.dumps(overview, ensure_ascii=False, indent=2))
    return int(any((result['formula_errors'], result['missing_sheets'], result['missing_selected_cells'],
                    result['external_workbook_parts'],
                    args.max_uncached is not None and result['uncached_formula_count'] > args.max_uncached)))


if __name__ == '__main__':
    raise SystemExit(main())
