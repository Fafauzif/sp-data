"""Verify chapter, caption and printed folio labels from the actual rendered PDF."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import unicodedata

import fitz


def normalize(value):
    return ' '.join(unicodedata.normalize('NFKC', value).replace('\u00ad','').split())


def page_candidates(pdf):
    by_title = defaultdict(set)
    folios = {}
    for page in pdf:
        for block in page.get_text('blocks', flags=fitz.TEXTFLAGS_TEXT):
            x0,y0,x1,y1,text,*_ = block
            if y0 >= page.rect.height * .90:
                for value in (normalize(line) for line in text.splitlines()):
                    if re.fullmatch(r'[1-9][0-9]*', value):
                        if page.number in folios and folios[page.number] != int(value):
                            raise ValueError(f'Ambiguous footer on physical page {page.number+1}')
                        folios[page.number] = int(value)
            lines = [normalize(line) for line in text.splitlines() if line.strip()]
            for start in range(len(lines)):
                for stop in range(start+1,min(len(lines),start+3)+1):
                    line=' '.join(lines[start:stop])
                    if not re.search(r'\.{4,}',line):
                        by_title[line].add(page.number)
    outline=defaultdict(set)
    for _level,title,page in pdf.get_toc():
        if 0<page<=len(pdf):
            outline[normalize(title)].add(page-1)
    return by_title,folios,outline


def audit_front_lists(pdf, indexes, found):
    expected=(('toc',1),('figlist',2),('tblist',3))
    summary={}
    for key,page_index in expected:
        page=pdf[page_index]
        expected_items=Counter(
            (normalize(title),found[label]) for label,title,level,_ in indexes[key]
            if key!='toc' or level==1
        )
        actual_items=Counter()
        for text in page.get_text().splitlines():
            match=re.match(r'^(.*?)\s*\.{4,}\s*(\d+)\s*$',text)
            if match:
                actual_items[(normalize(match[1]),int(match[2]))]+=1
        destinations = Counter(l['page']+1 for l in page.get_links() if l['kind']==fitz.LINK_GOTO)
        expected_destinations=Counter()
        for (_title,value),count in expected_items.items():
            expected_destinations[value]+=count
        summary[key]={'expected':sum(expected_items.values()),'actual':sum(actual_items.values()),
                      'missing_rows':list((expected_items-actual_items).elements()),
                      'extra_rows':list((actual_items-expected_items).elements()),
                      'destination_counts_match':destinations==expected_destinations}
    return summary


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('pdf',type=Path)
    p.add_argument('index',type=Path)
    p.add_argument('--write-cache',type=Path)
    p.add_argument('--report',type=Path)
    args=p.parse_args()
    indexes=json.loads(args.index.read_text(encoding='utf-8'))
    with fitz.open(args.pdf) as pdf:
        titles,folios,outline=page_candidates(pdf)
        found={}
        physical={}
        for group in ('toc','figlist','tblist'):
            for ident,title,level,old in indexes[group]:
                label=normalize(title)
                candidates=(outline.get(label) if group=='toc' else None) or titles.get(label)
                if not candidates or len(candidates)!=1:
                    raise ValueError(f'{group}/{ident} {title!r} has ambiguous page candidates {candidates!r}')
                destination=next(iter(candidates))
                if destination not in folios:
                    raise ValueError(f'{ident} destination on page {destination+1} has no printed folio')
                found[ident]=folios[destination]
                physical[ident]=destination+1
        front=audit_front_lists(pdf,indexes,found)
        references=physical['referensi']
        summary_start=physical['ringkasan']
        invalid_links=[{'page':q.number+1,'xref':link['xref']} for q in pdf for link in q.get_links()
                       if link['kind']==fitz.LINK_GOTO and not 0<=link['page']<len(pdf)]
        report={'pages':len(pdf),'body_pages':references-summary_start,
                'body_range':[summary_start,references-1],'outline_count':len(pdf.get_toc()),
                'resolved_entries':len(found),'invalid_links':invalid_links,'front_lists':front}
    if args.write_cache:
        args.write_cache.write_text(json.dumps(found,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.report:
        args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return int(bool(invalid_links) or any(row['missing_rows'] or row['extra_rows'] or not row['destination_counts_match']
                                         for row in front.values()))


if __name__=='__main__':
    raise SystemExit(main())
