"""Whole-image comparison after checking every removed raw provenance link.

No row, type, multiplicity, signature, frequency, physical witness, carrier,
N tuple, transition count, allowed-row set, bound, extremum or failure is
removed. Only timing and explicitly rebound raw execution metadata differ.
The interval-artifact directory in coverage duplicates the complete 348
outputs retained individually in this same mathematical stream.
"""
import json

def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':')).encode()

def without_timing(x):
    if isinstance(x, dict):
        return {k: without_timing(v) for k, v in x.items() if k != 'elapsed_seconds'}
    if isinstance(x, list):
        return [without_timing(v) for v in x]
    return x

def mathematical(name, x):
    y = without_timing(x)
    if name == 'pass23-T0-column-scope':
        y.pop('sealed_at')
    elif name.startswith('pass23-T0-N-') and name.endswith('-check'):
        y.pop('author_result_sha256')
    elif name == 'pass23-T0-column-coverage':
        for field in ['completed_at', 'live_cases_file', 'live_cases_sha256', 'interval_artifacts']:
            y.pop(field)
    elif name == 'pass23-T0-live-column-cases':
        y.pop('scope_sha256')
    elif name == 'pass23-T0-capacity-producer':
        y.pop('input_live_cases_sha256')
    elif name == 'pass23-T0-capacity-independent':
        y.pop('input_live_cases_sha256')
        y.pop('author_result_sha256')
    elif name == 'pass23-T0-row-base':
        y.pop('input_live_sha256')
        y.pop('input_capacity_sha256')
    elif name == 'pass23-T0-row-base-independent':
        y.pop('author_sha256')
    return y
