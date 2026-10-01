"""Exact cumulative quota incidence; imported proof suites are not rerun."""
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
    raw = (repository/path).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == sha,('import bytes changed',path)
    return json.loads(raw)

def main():
    assert __debug__,'Run with assertions enabled'
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository',type=Path,default=HERE.parents[1])
    parser.add_argument('--out',type=Path,default=HERE/'out')
    args = parser.parse_args()
    table = pinned(args.repository,'sorting_networks/thirteen_extreme_multiset_quotient/certificate.json',
                   'd670b600ed1c2e31990d6e2458b748d160a257b5dacf4bf15d3e270414202047')['class_table']
    pinned(args.repository,'sorting_networks/thirteen_repeated_i4_exclusion/certificate.json',
           'c0cfe9682597f18f6b099cb5c217a64d15c54df9a228371575185a15d77aaa52')
    first2 = pinned(args.repository,'sorting13_B11_first2_exclusion/certificate.json',
                    'c24c532fdf5ea6a2b24702e5af02a30b436046c31888848d5882bc415be2eea2')
    first3 = pinned(args.repository,'sorting13_B11_first3_exclusion/certificate.json',
                    'c607be71aab34f1abb17f7dd7e3d66e19dc927a45dcd2f7bd1b8a46625c1212d')
    first4 = pinned(args.repository,'sorting_networks/thirteen_first4_branch_exclusion/certificate.json',
                    '5d329f690e4fac86cdeee44fca56cd684be52b55291334de39fc1c71b3fa6cb7')
    f4 = pinned(args.repository,'sorting_networks/thirteen_first4_branch_exclusion/fixture.json',
                '53844719a3d1ffe97e1e454652464126dd8f00aca2c1613283b67cd9f830d439')
    assert len(table) == 480 and digest(table) == '5ac42c7b2ec5cc5485ea107338ddd20eaf9f8e5a56a6cbb8aa3e87e803799042'
    for prior,size in ((first2,35),(first3,36)):
        assert len(prior['new_classes']) == size
        assert all([c,e,n] == table[i] for i,c,e,n in prior['new_classes'])
    assert first4['newly_excluded_classes'] == [[i,c] for i,c,e,n in f4['classes']]
    assert len(f4['classes']) == 45 and sum(r[3] for r in f4['classes']) == 440190
    codes2 = {r[1] for r in first2['new_classes']}
    codes3 = {r[1] for r in first3['new_classes']}
    codes4 = {r[1] for r in f4['classes']}
    fixture = json.loads((HERE/'fixture.json').read_text())
    certificate = json.loads((HERE/'certificate.json').read_text())
    own = {r[1] for r in fixture['classes']}
    assert certificate['newly_excluded_classes'] == [[i,c] for i,c,e,n in fixture['classes']]
    assert len(own) == 18 and certificate['newly_excluded_effective_orders'] == 210960
    sets = (codes2,codes3,codes4,own)
    assert all(a.isdisjoint(b) for a,b in itertools.combinations(sets,2))
    before,remaining = [],[]
    excluded = Counter()
    for code,events,orders in table:
        quota = [int(code)>>(2*k)&3 for k in range(55)]
        assert sum(quota) == events and events in (10,11) and max(quota)<=2
        if events == 10:
            excluded['ten'] += 1
        elif max(quota) == 2:
            excluded['eleven_repeated'] += 1
        elif code in codes2:
            excluded['first2_distinct'] += 1
        elif code in codes3:
            excluded['first3_distinct'] += 1
        elif code in codes4:
            excluded['first4_distinct'] += 1
        else:
            before.append([code,events,orders])
            if code in own:
                excluded['joint56_distinct'] += 1
            else:
                remaining.append([code,events,orders])
    assert excluded == dict(ten=135,eleven_repeated=48,first2_distinct=27,first3_distinct=36,
                            first4_distinct=45,joint56_distinct=18)
    assert len(before) == 189 and sum(r[2] for r in before) == 1194030
    assert digest(before) == 'c7c376e080fb6df7842af4d9a42f8802fc10125400607878852f33535b726034'
    assert len(remaining) == 171 and sum(r[2] for r in remaining) == 983070
    groups = {}
    for code,events,orders in remaining:
        # These allowed partners classify quota membership, not event order.
        # Later comparisons with partners7/9 are still allowed.
        partners = tuple(i for i in (1,5,6,8) if int(code)>>(2*GATES.index((i,10)))&3)
        assert partners in ((5,8),(6,8))
        groups.setdefault(partners,[]).append([code,events,orders])
    assert [(k,len(v),sum(r[2] for r in v)) for k,v in sorted(groups.items())] == [
        ((5,8),135,561150),((6,8),36,421920)]
    result = dict(agent='six-sorting-1',role='researcher',status='EXACT_JOINT56_CUMULATIVE_INCIDENCE_VERIFIED',
                  previous_classes=189,previous_effective_orders=1194030,
                  remaining_classes=171,remaining_effective_orders=983070,excluded=dict(excluded),
                  class_table=remaining,class_table_sha256=digest(remaining),
                  groups=[dict(allowed_partners=list(k),classes=len(v),orders=sum(r[2] for r in v))
                          for k,v in sorted(groups.items())],
                  frontier_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  trust='Imports distinct-event8395, first2/first3/first4 exclusions; proof suites not rerun. Concurrent peer8452 first4 variant counts zero additional classes. Other new peer closures are outside this pinned incidence calculation.')
    args.out.mkdir(exist_ok=True)
    (args.out/'frontier.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='class_table'}))

if __name__ == '__main__':
    main()
