"""Exact mathematical output boundary; raw volatile provenance is checked first.

No vectors, failures, signatures, multiplicities, carrier, N support,
transition counts, physical witnesses or capacity certificates are removed.
The interval artifacts in the coverage summary are administrative copies
of the 56 complete outputs individually retained in this same stream.
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
    if name == 'pass21-T1-column-scope':
        y.pop('sealed_at')
    elif name.startswith('pass21-T1-N-') and name.endswith('-check'):
        y.pop('author_result_sha256')
    elif name == 'pass21-T1-column-coverage':
        for key in ['completed_at', 'live_cases_file', 'live_cases_sha256', 'interval_artifacts']:
            y.pop(key)
    elif name == 'pass21-T1-live-column-cases':
        y.pop('scope_sha256')
    elif name == 'pass21-T1-capacity-producer':
        y.pop('input_live_cases_sha256')
    elif name == 'pass21-T1-capacity-independent':
        y.pop('author_result_sha256')
    return y
