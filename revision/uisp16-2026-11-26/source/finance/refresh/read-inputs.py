"""Read editable input cells, without modifying the workbook."""
import json
import sys
from openpyxl import load_workbook

doc = load_workbook(sys.argv[1], data_only=True, read_only=True)
sheet = doc["Asumsi"]
cases = ("Downside", "Base", "Upside")
result = {}
for code, label, down, base, up in sheet.iter_rows(min_row=7, max_row=116, max_col=5, values_only=True):
    if not code:
        continue
    if not all(isinstance(value, (int, float)) for value in (down, base, up)):
        raise ValueError(f"Input skenario tidak valid: {code} ({label})")
    result[code] = dict(zip(cases, (down, base, up)))
result["clusterPlan"] = [cell.value for cell in sheet[118][1:11]]
if len(result["clusterPlan"]) != 10 or not all(isinstance(x, (int,float)) and x>=1 for x in result["clusterPlan"]):
    raise ValueError("Batas klaster harus berupa sepuluh angka positif.")
result["activeCase"] = doc["Ringkasan"]["C6"].value
result["activeFunding"] = doc["Ringkasan"]["C7"].value
print(json.dumps(result, allow_nan=False))
