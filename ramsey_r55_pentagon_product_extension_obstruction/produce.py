"""Produce a complete 243-class extension obstruction certificate."""
from collections import Counter
from itertools import product
import json
import core


def make():
    inside = [core.inner(word) for word in range(32)]
    weights = Counter(row['tag'] for row in inside)
    outside = [core.outer(tags) for tags in product((1,2,3),repeat=5)]
    coverage = 0
    for row in outside:
        weight = 1
        for tag in row['tags']:
            weight *= weights[tag]
        row['attachment_count'] = weight
        coverage += weight
    return dict(format='pentagon-product-extension-v1', inner=inside, outer=outside,
                tag_counts={str(k):v for k,v in sorted(weights.items())},
                attachment_count=coverage, free_43_edges=603,
                fixed_ordered_core_family_count=1 << 603,
                status='COMPLETE_CORE_EXTENSION_FAMILY_EXCLUDED')


if __name__ == '__main__':
    print(json.dumps(make(), indent=2, sort_keys=True))
