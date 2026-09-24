"""Regenerate the complete finite obstruction with standard-library Python."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from census import census
from local import solve
from complete import enumerate_covers
from symmetry import make_templates
from glue import joins
from finish import require, residual, check_weights

ROOT = Path(__file__).resolve().parent


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def compute(check_fixtures=True):
    records, high_census = census()
    completions = {}
    local_nodes = 0
    for index, record in enumerate(records):
        decision = solve(record['columns'])
        local_nodes += decision['states']
        if 'witness' in decision:
            complete = enumerate_covers(record['columns'])
            require(complete['covers'], 'feasible local decision has no bounded-degree completion')
            completions[index] = list(map(list, complete['covers']))
    local_fixture = [dict(type=index, a=records[index]['rows'], covers=covers)
                     for index, covers in sorted(completions.items())]
    templates, orbit_summary = make_templates(records, completions)
    if check_fixtures:
        require(local_fixture == json.loads((ROOT / 'LOCAL.json').read_text()),
                'complete local fixture mismatch')
        require(templates == json.loads((ROOT / 'LINKS.json').read_text()),
                'pointed-link orbit fixture mismatch')
    certificates = json.loads((ROOT / 'weights.json').read_text())
    weights = {(row['root'], row['index']): row for row in certificates}
    require(len(weights) == len(certificates), 'duplicate closure certificate')
    used = set()
    join_summary = []
    all_joins = []
    closed = []
    degree_exclusions = 0
    for index, template in enumerate(templates):
        joined = joins(template, templates)
        all_joins.append(joined)
        counts = Counter()
        for case, configuration in enumerate(joined['configurations']):
            if residual(joined, configuration) is None:
                degree_exclusions += 1
                counts['degree'] += 1
            else:
                key = index, case
                require(key in weights, 'missing weight certificate')
                checked = check_weights(joined, configuration, weights[key])
                closed.append(dict(root=index, index=case, **checked))
                counts['weights'] += 1
                used.add(key)
        join_summary.append(dict(root=index, type=template['type'], cover=template['cover'],
                                 alpha=joined['alpha'], beta=joined['beta'],
                                 embeddings=joined['raw_embeddings'],
                                 compatible_embeddings=joined['compatible_embeddings'],
                                 configurations=len(joined['configurations']),
                                 exclusions=dict(counts)))
    require(used == set(weights), 'unused or extraneous weight certificate')
    result = dict(
        status='VERIFIED_NO_EXCEPTIONAL_12_9_PROFILE',
        local_types=len(records), heavy_support_types=len(high_census),
        through_overlap_counts=dict(sorted(Counter(r['overlap'] for r in records).items())),
        completable_types=len(completions), labelled_completions=sum(map(len, completions.values())),
        pointed_link_classes=len(templates),
        local_decision_states=local_nodes,
        census_sha256=digest(records), local_fixture_sha256=digest(local_fixture),
        link_fixture_sha256=digest(templates), joined_configurations_sha256=digest(all_joins),
        joins=join_summary, orbit_summary=orbit_summary,
        degree_exclusions=degree_exclusions, weight_exclusions=len(closed),
        weight_capacity_checks=sum(row['capacity_checks'] for row in closed),
        minimum_weight_gap=min(row['gap'] for row in closed),
        maximum_weight=max(value for row in certificates for _, value in row['weights']),
        weights_file_sha256=sha256((ROOT / 'weights.json').read_bytes()).hexdigest(),
        closure=closed)
    return result, local_fixture, templates


if __name__ == '__main__':
    print(json.dumps(compute()[0], indent=2, sort_keys=True))
