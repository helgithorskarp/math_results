"""Exact cumulative incidence; imported theorems are not rerun here."""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATES = tuple(itertools.combinations(range(11),2))


def digest(x):
    return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()


def pinned(repository,path,sha):
    data = (repository/path).read_bytes()
    assert hashlib.sha256(data).hexdigest() == sha, ('import changed',path)
    return json.loads(data) if path.endswith('.json') else data


def main():
    assert __debug__, 'Run with assertions enabled'
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository',type=Path,default=HERE.parents[1])
    parser.add_argument('--out',type=Path,default=HERE/'out')
    parser.add_argument('--first3-certificate',type=Path)
    args = parser.parse_args()
    table = pinned(args.repository,'sorting_networks/thirteen_extreme_multiset_quotient/certificate.json',
                   'd670b600ed1c2e31990d6e2458b748d160a257b5dacf4bf15d3e270414202047')['class_table']
    previous = pinned(args.repository,'sorting_networks/thirteen_repeated_i4_exclusion/certificate.json',
                      'c0cfe9682597f18f6b099cb5c217a64d15c54df9a228371575185a15d77aaa52')
    pinned(args.repository,'sorting_networks/thirteen_repeated_i4_exclusion/PROOF.md',
           'a30277d544f7bd2020181389789af79a54e7ac432466a6ef4b0e6590b6e65f8c')
    first2 = pinned(args.repository,'sorting13_B11_first2_exclusion/certificate.json',
                    'c24c532fdf5ea6a2b24702e5af02a30b436046c31888848d5882bc415be2eea2')
    first3_path = args.first3_certificate or args.repository/'sorting13_B11_first3_exclusion/certificate.json'
    first3_raw = first3_path.read_bytes()
    assert hashlib.sha256(first3_raw).hexdigest() == 'c607be71aab34f1abb17f7dd7e3d66e19dc927a45dcd2f7bd1b8a46625c1212d'
    first3 = json.loads(first3_raw)
    assert len(table) == 480 and digest(table) == '5ac42c7b2ec5cc5485ea107338ddd20eaf9f8e5a56a6cbb8aa3e87e803799042'
    assert previous['newly_excluded_classes'] == [[i,table[i][0]] for i in [80,84,87,195,199,202,283,287,290]]
    assert first2['proof_status'] == 'ALL_PUBLIC_FINITE_REDUCTIONS_DATA_CLAUSES_NATIVE_DRAT_AND_PYTHON_RUP_ACTUALLY_CHECKED'
    assert len(first2['new_classes']) == 35 and all([c,e,n] == table[i] for i,c,e,n in first2['new_classes'])
    assert first3['agent'] == 'six-sorting-2' and first3['role'] == 'researcher'
    assert first3['proof_status'] == 'ALL_PUBLIC_FINITE_REDUCTIONS_DATA_CLAUSES_NATIVE_DRAT_COMPACT_NATIVE_AND_PYTHON_RUP_ACTUALLY_CHECKED'
    assert len(first3['new_classes']) == 36 and all([c,e,n] == table[i] for i,c,e,n in first3['new_classes'])
    assert sum(r[3] for r in first3['new_classes']) == 279810
    peer_codes = {r[1] for r in first2['new_classes']}
    first3_codes = {r[1] for r in first3['new_classes']}
    assert first3_codes.isdisjoint(peer_codes)
    fixture = json.loads((HERE/'fixture.json').read_text())
    current = json.loads((HERE/'certificate.json').read_text())
    own_codes = {r[1] for r in fixture['classes']}
    assert own_codes.isdisjoint(peer_codes)
    assert own_codes.isdisjoint(first3_codes)
    assert current['newly_excluded_classes'] == [[i,c] for i,c,e,n in fixture['classes']]
    assert current['newly_excluded_effective_orders'] == 440190
    baseline,before_current,remaining,excluded = [],[],[],Counter()
    for i,(c,e,n) in enumerate(table):
        counts = [int(c) >> (2*k) & 3 for k in range(55)]
        assert sum(counts) == e and e in (10,11) and max(counts) <= 2
        if e == 10:
            excluded['ten'] += 1
            continue
        if max(counts) == 2:
            excluded['eleven_repeated'] += 1
            continue
        if c in peer_codes:
            excluded['first2_distinct'] += 1
            continue
        baseline.append([c,e,n])
        if c in first3_codes:
            excluded['first3_distinct'] += 1
            continue
        before_current.append([c,e,n])
        if c in own_codes:
            excluded['first4_distinct'] += 1
        else:
            remaining.append([c,e,n])
    assert len(baseline) == 270 and sum(r[2] for r in baseline) == 1914030
    assert digest(baseline) == 'bc85c709702d769edb1f9550ab34e4e3d36bcb4322f63baeda241f646def5ac9'
    assert excluded == dict(ten=135,eleven_repeated=48,first2_distinct=27,first3_distinct=36,first4_distinct=45)
    assert len(before_current) == 234 and sum(r[2] for r in before_current) == 1634220
    assert len(remaining) == 189 and sum(r[2] for r in remaining) == 1194030
    assert sum(r[2] for r in before_current)-sum(r[2] for r in remaining) == 440190
    assert all(not (int(c) >> (2*GATES.index((i,10))) & 3) for c,e,n in remaining for i in (2,3,4))
    pair_groups = {}
    for c,e,n in remaining:
        partners = tuple(i for i in (1,5,6,8) if (int(c) >> (2*GATES.index((i,10))) & 3))
        assert partners in ((5,6),(5,8),(6,8))
        pair_groups.setdefault(partners,[]).append([c,e,n])
    assert [(k,len(pair_groups[k]),sum(r[2] for r in pair_groups[k])) for k in sorted(pair_groups)] == [
        ((5,6),18,210960),((5,8),135,561150),((6,8),36,421920)]
    result = dict(agent='six-sorting-1',role='researcher',status='EXACT_FIRST4_CONDITIONAL_FRONTIER_INCIDENCE_VERIFIED',
                  baseline_classes=270,baseline_effective_orders=1914030,previous_classes=234,
                  previous_effective_orders=1634220,remaining_classes=189,
                  remaining_effective_orders=1194030,counts=dict(eleven_distinct=189),excluded=dict(excluded),
                  class_table_sha256=digest(remaining),class_table=remaining,
                  remaining_first10_partners=[5,6,8],
                  port10_pair_groups=[dict(partners=list(k),classes=len(v),orders=sum(r[2] for r in v))
                                      for k,v in sorted(pair_groups.items())],
                  frontier_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  trust='Imported graph8395 distinct-event theorem, graph8382 first2 exclusion, and newly committed peer8420 first3 exclusion; exact incidence checked, imported proof suites not rerun.')
    args.out.mkdir(exist_ok=True)
    (args.out/'frontier.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='class_table'}))


if __name__ == '__main__':
    main()
