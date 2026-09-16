#!/usr/bin/env python3
"""Regenerate the literal extension witnesses after an independent inspection."""

import json

from model import canonical_colorings, construction, find_coloring, induced_edges


points, edges, _, source = construction()
source_edges = induced_edges(source, edges)
source_words = canonical_colorings(7, source_edges, 4)
records = []
for word in source_words:
    extension = find_coloring(
        len(points), edges, 4, {source[i]: word[i] for i in range(7)}
    )
    if extension is not None:
        records.append({
            "source_word": "".join(map(str, word)),
            "extension": "".join(map(str, extension)),
        })
print(json.dumps({
    "schema": "hendecagon-c11-spindle-round-v1",
    "source_extensions": records,
}, indent=2, sort_keys=True))

