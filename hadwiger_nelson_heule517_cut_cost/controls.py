#!/usr/bin/env python3
"""Reject failures of each mathematical certificate layer."""
from copy import deepcopy
import json
from verify import check, HERE, INPUT

original = json.loads((HERE / 'certificate.json').read_text())
raw = INPUT.read_bytes()
bad = []
x = deepcopy(original); x['input_sha256'] = '0' * 64; bad.append(x)
x = deepcopy(original); x['packing_extra_rows'][0] = x['packing_extra_rows'][1]; bad.append(x)
x = deepcopy(original); x['hub_forcing_steps'][0]['pair_rows'] = x['hub_forcing_steps'][0]['pair_rows'][:10]; bad.append(x)
x = deepcopy(original); x['residual_rows'].pop(); bad.append(x)
x = deepcopy(original); x['optimal_extras'].pop(); bad.append(x)
x = deepcopy(original); x['optimal_extras'][0][0] = 0; bad.append(x)
for x in bad:
    try:
        check(x, raw)
    except ValueError:
        continue
    raise RuntimeError('invalid certificate accepted')
print(json.dumps({'invalid_certificates_rejected': len(bad),
                  'production_graph_queries': 0, 'native_solver_used': False}))
