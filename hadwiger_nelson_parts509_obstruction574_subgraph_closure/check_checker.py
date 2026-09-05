#!/usr/bin/env python3
"""Small rejection controls for the direct positive-certificate checker."""
import json
from verify import check_colouring, require

labels = [0, 1, 2, 3]
edges = [(0, 1), (1, 2), (0, 2), (2, 3)]
require(check_colouring(labels, edges, 3, '012.') == 3, 'valid fixture')
bad = [(3, '002.'), (3, '012'), (3, '0124'), (3, '01..'), (2, '012.'), (9, '012.')]
for deleted, colours in bad:
    try:
        check_colouring(labels, edges, deleted, colours)
    except ValueError:
        pass
    else:
        raise AssertionError(('accepted malformed witness', deleted, colours))
print(json.dumps(dict(valid_fixture_accepted=True, malformed_witnesses_rejected=len(bad)), indent=2))
