from collections import Counter
import csv
import json
from pathlib import Path

source = Path(__file__).with_name('Respons_Survei_LihatDulu_Final_60_Timestamp_Redacted.csv')
with source.open(encoding='utf-8-sig', newline='') as stream:
    reader = csv.reader(stream)
    next(reader)
    answers = list(reader)

considered = [a for a in answers if 'setidaknya satu iklan' in a[2]]
confidence = ['Sangat tidak yakin', 'Tidak yakin', 'Cukup yakin', 'Yakin', 'Sangat yakin']
intent = ['Sangat kecil', 'Kecil', 'Sedang', 'Besar', 'Sangat besar']

def multiple_choice(col):
    return Counter(item.strip() for a in considered for item in a[col].split(',') if item.strip())

def shifts(col1, col2, order):
    counts = Counter()
    for a in answers:
        if a[col1] not in order or a[col2] not in order:
            counts['excluded'] += 1
            continue
        diff = order.index(a[col2]) - order.index(a[col1])
        counts['increased' if diff>0 else 'decreased' if diff<0 else 'unchanged'] += 1
    return dict(counts)

result = {
    'responses': len(answers),
    'students': sum(a[1]=='Ya' for a in answers),
    'searched_online': sum(a[2].startswith('Pernah mencari') for a in answers),
    'considered_specific_listing': len(considered),
    'students_considering_specific_listing': sum(a[1]=='Ya' for a in considered),
    'listing_obstacles_multiple_choice': dict(multiple_choice(3)),
    'listing_actions_multiple_choice': dict(multiple_choice(4)),
    'confidence_change_fixed_order': shifts(6, 9, confidence),
    'stated_purchase_intent_change_fixed_order': shifts(8, 11, intent),
}
print(json.dumps(result, ensure_ascii=False, indent=2))
