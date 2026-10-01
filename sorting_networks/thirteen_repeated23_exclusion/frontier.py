"""Exact cumulative incidence, importing the published whole-ten-branch theorem.

This checks class identities/counts, not the peer's large UNSAT certificates.
"""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAIRS = tuple(itertools.combinations(range(11), 2))


def main():
    if not __debug__:
        raise RuntimeError('Run with assertions enabled')
    parser = argparse.ArgumentParser()
    parser.add_argument('--quotient', type=Path, default=HERE.parent / 'thirteen_extreme_multiset_quotient/certificate.json')
    parser.add_argument('--peer-certificate', type=Path, default=HERE.parent.parent / 'sorting13_B11_ten_event_branch_exclusion/certificate.json')
    parser.add_argument('--ten-parent', type=Path, default=HERE.parent.parent / 'sorting13_B11_ten_event_loop_postponement/certificate.json')
    args = parser.parse_args()
    assert hashlib.sha256(args.quotient.read_bytes()).hexdigest() == 'd670b600ed1c2e31990d6e2458b748d160a257b5dacf4bf15d3e270414202047'
    assert hashlib.sha256(args.peer_certificate.read_bytes()).hexdigest() == '47ec194a3decff3508ffb5d0279aea2352de1921b790287a5c2212c62ef74bee'
    table = json.loads(args.quotient.read_text())['class_table']
    peer = json.loads(args.peer_certificate.read_text())
    assert peer['complete_branch_enrolled'] is True
    assert peer['proof_status'] == 'ALL_RECORDS_ACTUALLY_SCALAR_CLAUSE_NATIVE_AND_PYTHON_CHECKED'
    assert len(table) == 480
    ten = {code: orders for code, length, orders in table if length == 10}
    assert len(ten) == 135 and sum(ten.values()) == 751950
    assert len(peer['coverage']) == 77 and len({r['code'] for r in peer['coverage']}) == 77
    assert all(ten[r['code']] == r['effective_orders'] for r in peer['coverage'])
    assert sum(r['effective_orders'] for r in peer['coverage']) == 432186
    target = json.loads((HERE / 'fixture.json').read_text())['tails'][1]
    assert peer['tail_transfer']['class_code'] == target['class_code']
    assert peer['tail_transfer']['rows9_sha256'] == target['rows9_sha256']
    assert peer['tail_transfer']['local_image'] == 0 and peer['tail_transfer']['budget'] == 11
    assert hashlib.sha256(args.ten_parent.read_bytes()).hexdigest() == '5360120fc75814699b79879b4fc3a7c43f00a37af0876bf58e0fb8144cc2cdf9'
    assert json.loads(args.ten_parent.read_text())['images9'][2] == target['rows9']
    categories, remaining, exclusions = Counter(), [], Counter()
    repeat23 = []
    for index, (code, length, orders) in enumerate(table):
        counts = tuple((int(code) >> (2 * k)) & 3 for k in range(55))
        assert sum(counts) == length and max(counts) <= 2
        doubled = [gate for gate, count in zip(PAIRS, counts) if count == 2]
        assert len(doubled) <= 1
        if length == 10:
            assert not doubled
            exclusions['ten'] += 1
            continue  # Entire branch imported from graph8321, including its prior exclusions.
        assert length == 11
        if doubled == [(0, 1)]:
            exclusions['repeated01'] += 1
            continue  # Complete eighteen-class theorem8070.
        if code == '349871875148001158693749134458897':
            assert doubled == [(1, 2)]
            exclusions['class13'] += 1
            continue  # Complete class theorem8198.
        if doubled == [(2, 3)]:
            repeat23.append(index)
            exclusions['repeated23'] += 1
            continue  # Prior8281 plus present complete three-class exclusion.
        categories['eleven_repeated' if doubled else 'eleven_distinct'] += 1
        remaining.append([code, length, orders])
    assert repeat23 == [34, 40, 149, 155, 237, 243]
    assert exclusions == dict(ten=135, repeated01=18, class13=1, repeated23=6)
    assert categories == dict(eleven_distinct=297, eleven_repeated=23)
    assert len(remaining) == 320 and sum(r[2] for r in remaining) == 2186295
    digest = hashlib.sha256(json.dumps(remaining, separators=(',', ':')).encode()).hexdigest()
    assert digest == 'c63e46bc345c6a8973be7e62ecaae1bda06e687119a027e00c1195a4daca74f5'
    print(json.dumps(dict(agent='six-sorting-1', role='researcher',
                          status='EXACT_CONDITIONAL_FRONTIER_INCIDENCE_VERIFIED',
                          remaining_classes=320, counts=dict(categories), effective_orders=2186295,
                          class_table_sha256=digest,
                          trust='Peer8321 full branch proofs imported, read and not replayed by this script')))


if __name__ == '__main__':
    main()
