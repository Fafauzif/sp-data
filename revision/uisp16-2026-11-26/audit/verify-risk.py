"""Reconcile Finance simulation results to each trial's FCFF using NumPy roots independently."""
import argparse
from collections import Counter
import json
from pathlib import Path
import math

import numpy as np


def irr_outcome(flows):
    values = np.trim_zeros(flows, 'fb')
    if len(values) == 0:
        return 'tidak_terdefinisi', None
    if all(values >= 0) or all(values <= 0):
        return 'tidak_tersedia', None
    roots = np.roots(values[::-1] / np.max(np.abs(values)))
    solutions = sorted(1 / float(root.real) - 1 for root in roots
                       if root.real > 0 and abs(root.imag) <= 1e-7 * abs(root.real))
    unique = [v for i, v in enumerate(solutions) if i == 0 or abs(v - solutions[i-1]) > 1e-7]
    if len(unique) == 1:
        return 'valid', unique[0]
    return ('lebih_dari_satu' if unique else 'tidak_tersedia'), None


def check(indicators):
    risks, sens = indicators['simulation'], indicators['sensitivity']
    rows = risks['rows']
    counts = Counter()
    crossings = Counter()
    errors = []
    for trial in rows:
        ident = trial['id']
        for key, value in trial['multipliers'].items():
            bounds = risks['drivers'][key]['bounds']
            if not bounds[0] <= value <= bounds[2]:
                errors.append([ident, 'driver outside bound', key, value])
        flows = np.array(trial['cashflows'], dtype=float)
        capm = trial['capm']
        discounted = flows / ((1 + capm) ** np.arange(len(flows)))
        npv = float(np.sum(discounted))
        if not math.isclose(npv, trial['npv'], rel_tol=1e-9, abs_tol=1e-8):
            errors.append([ident, 'NPV mismatch', npv, trial['npv']])
        status, irr = irr_outcome(flows)
        counts[status] += 1
        if status != trial['irrStatus'] or irr is not None and not math.isclose(irr, trial['irr'], rel_tol=1e-6, abs_tol=1e-7):
            errors.append([ident, 'IRR mismatch', status, irr, trial['irrStatus'], trial['irr']])
        crossing = None
        for i in range(1, len(flows)):
            part = np.trim_zeros(flows[:i+1], 'fb')
            if len(part) < 2 or all(part >= 0) or all(part <= 0):
                continue
            sign_changes = sum(np.sign(part[1:]) * np.sign(part[:-1]) < 0)
            if sign_changes == 1 and part[0] < 0:
                if float(np.sum(discounted[:i+1])) > 1e-8:
                    crossing = risks['years'][i]
                    break
            else:
                _, partial_irr = irr_outcome(flows[:i+1])
                if partial_irr is not None and partial_irr > capm + 1e-10:
                    crossing = risks['years'][i]
                    break
        crossings[str(crossing)] += 1
        if crossing != trial['crossing']:
            errors.append([ident, 'crossing mismatch', crossing, trial['crossing']])
    ok_horizon = risks['assessmentYear'] == sens['assessmentYear']
    half = len(sens['levels']) // 2
    mid = sens['cells'][half][half]
    center_equal = math.isclose(mid['npv'], sens['center']['npv'], rel_tol=1e-9, abs_tol=1e-8)
    if risks['selector'] == 'Base':
        center_equal = center_equal and math.isclose(mid['npv'], risks['baseline']['npv'], rel_tol=1e-9, abs_tol=1e-8)
    hist_ok = sum(bin['count'] for bin in risks['npvHistogram']) == len(rows)
    return {
        'n':len(rows), 'start':risks['years'][0], 'end':risks['assessmentYear'],
        'verified_irr_classifications':dict(counts), 'verified_crossings':dict(crossings),
        'sensitivity_and_monte_carlo_same_end':ok_horizon,
        'sensitivity_center_matches_base_npv':center_equal,
        'npv_histogram_count_matches_trials':hist_ok,
        'errors':errors[:30], 'error_count':len(errors),
        'passed':len(errors)==0 and ok_horizon and center_equal and hist_ok,
    }


if __name__ == '__main__':
    arguments=argparse.ArgumentParser(description=__doc__)
    arguments.add_argument('risk_file', type=Path)
    options=arguments.parse_args()
    outcome=check(json.loads(options.risk_file.read_text(encoding='utf-8')))
    print(json.dumps(outcome, indent=2, ensure_ascii=False))
    raise SystemExit(0 if outcome['passed'] else 1)
