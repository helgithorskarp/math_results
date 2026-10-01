"""Stable compact readouts and positive literal coverage checks.

Digests compare replays; completeness comes from the generators and proofs.
"""
from collections import Counter
from copy import deepcopy
from itertools import combinations
import hashlib
import json
from pathlib import Path
import carrier as C
from paths import HERE, INPUTS, WORK, verify_inputs
from quotient import compose, inverse, encoded


def load(path):
    return json.loads(path.read_text())


def digest(value):
    return hashlib.sha256(encoded(value)).hexdigest()


def stable(value):
    if isinstance(value, dict):
        return {k:stable(v) for k,v in value.items() if k not in
                ('seconds','peak_RSS_kib','child_peak_RSS_kib','source_record_sha256','record_sha256')}
    if isinstance(value, list):
        return [stable(v) for v in value]
    return value


def verify_coverage(data, carriers):
    C.require(data['status']=='COMPLETE_POSITIVE_ROOT_COVER_ONLY' and
              len(data['roots'])==619 and len(data['coverage'])==6334,
              'incomplete root coverage')
    expected={}
    for fi, source in enumerate(carriers):
        C.require(source['fixture']==fi and
                  source['status']=='COMPLETE_LABELLED_LAMBDA5_STAR_UNION_CARRIER',
                  'incomplete fixture carrier')
        for row in source['rows']:
            key=(fi,row['mate'],tuple(row['mapping']))
            C.require(key not in expected, 'duplicate labelled input')
            expected[key]=row
    covered=set()
    for entry in data['coverage']:
        key=(entry['fixture'],entry['mate'],tuple(entry['mapping']))
        C.require(key in expected and key not in covered, 'false or duplicate coverage key')
        covered.add(key)
        ri=entry['root']
        C.require(type(ri) is int and 0<=ri<len(data['roots']), 'root index domain')
        root=data['roots'][ri]; p=tuple(entry['from_root'])
        C.require(root['fixture']==entry['fixture'] and sorted(p)==list(range(18)),
                  'root transport domain')
        ip=inverse(p)
        C.require(p[root['mate']]==entry['mate'] and
                  tuple(p[root['mapping'][ip[v]]] for v in range(18))==key[2] and
                  tuple(sorted(C.image(w,p) for w in root['words']))==tuple(expected[key]['words']),
                  'false literal coverage transport')
    C.require(covered==set(expected), 'omitted labelled map')
    for root in data['roots']:
        key=(root['fixture'],root['mate'],tuple(root['mapping']))
        C.require(key in covered and root['words']==expected[key]['words'], 'false root')
        words,p=C.normalize(tuple(root['words']),tuple(root['mapping']),root['mate'])
        C.require(words==tuple(root['normalized']) and p==tuple(root['transport']),
                  'false normalization transport')


def verify_bound_records(color, native, count=619):
    C.require(len(color)==len(native)==count and
              [r['root'] for r in color]==[r['root'] for r in native]==list(range(count)),
              'missing or duplicate bound case')
    for a,b in zip(color,native):
        C.require(a['status']=='COMPLETE_MAXIMUM' and
                  b['status']=='COMPLETE_EXACT_UPPER_AND_LITERAL_LOWER' and
                  a['residual_weight']==b['upper']<=34 and b['larger_cliques']==0 and
                  a['vertices']==b['orbit_vertices'] and a['fixture']==b['fixture'],
                  'incomplete or inconsistent bound')


def verify_trade(witness):
    import steiner
    from check_witness import check
    check(witness)
    old=set(steiner.code()); cap=witness['construction']['cap']
    C.require(type(cap) is int and 0<=cap<1<<17 and cap.bit_count()==5 and
              max((cap&w).bit_count() for w in old)<=3,'five-cap domain')
    removed={w for w in old if (cap&w).bit_count()==3}
    raw=witness['construction']['omissions']; omit=dict(raw)
    C.require(len(raw)==len(omit)==10 and set(omit)==removed and all(
              type(v) is int and 0<=v<17 and (w&cap)&(1<<v) for w,v in omit.items()),
              'ten actual parent omissions')
    tails=tuple(w^(1<<omit[w]) for w in sorted(removed))
    C.require(all((a&b).bit_count()<=1 for a,b in combinations(tails,2)), 'tail packing')
    code=tuple(sorted((old-removed)|{cap}|{t|(1<<17) for t in tails}))
    C.require(code==tuple(witness['words']), 'trade certificate differs from literal code')
    return check(witness)


def controls(data, carriers, color, native, witness):
    from check_witness import check
    rejected=[]
    def reject(name, action):
        try: action()
        except (ValueError,KeyError,IndexError): rejected.append(name)
        else: raise ValueError('damage accepted: '+name)
    bad=deepcopy(data);bad['coverage'].pop()
    reject('omitted-coverage-map',lambda:verify_coverage(bad,carriers))
    bad=deepcopy(data);bad['roots'].pop()
    reject('omitted-root',lambda:verify_coverage(bad,carriers))
    bad=deepcopy(data);bad['coverage'][0]['from_root'][0]=bad['coverage'][0]['from_root'][1]
    reject('false-point-transport',lambda:verify_coverage(bad,carriers))
    reject('omitted-native-case',lambda:verify_bound_records(color,native[:-1]))
    damaged=deepcopy(color);damaged[0]['status']='INCOMPLETE'
    reject('incomplete-producer',lambda:verify_bound_records(damaged,native))
    bad=deepcopy(witness);bad['words'][0]=bad['words'][1]
    reject('duplicate-witness-word',lambda:check(bad))
    bad=deepcopy(witness);bad['words'][0]^=1<<17
    reject('wrong-weight',lambda:check(bad))
    bad=deepcopy(witness);bad['centers']=[16,17]
    reject('fixed-centers',lambda:check(bad))
    bad=deepcopy(witness);bad['replications'][0]-=1
    reject('false-replication',lambda:check(bad))
    bad=deepcopy(witness);bad['construction']['omissions'][0][1]=17
    reject('false-parent-omission',lambda:verify_trade(bad))
    # Each pinned input is separately corrupted and passed through the real checker.
    import tempfile
    with tempfile.TemporaryDirectory(dir=WORK) as td:
        target=Path(td)
        import shutil
        for item in load(HERE/'INPUTS.json'):
            for source in INPUTS.iterdir():
                if source.is_file():shutil.copyfile(source,target/source.name)
            f=target/item['path'];f.write_bytes(f.read_bytes()+b' ')
            reject('changed-input-'+item['path'],lambda:verify_inputs(target))
    return rejected


def collect(work, run_controls=True):
    carriers=[load(work/'swapped-m5-full'/f'fixture-{i:02d}.json') for i in range(23)]
    groups=load(work/'swapped-full-groups.json')
    roots=load(work/'swapped-m5-roots.json')
    color=load(work/'swapped-m5-full-completions'/'summary.json')
    native=load(work/'swapped-m5-native'/'summary.json')
    baseline=load(work/'swapped-classical68.json')
    trades=load(work/'swapped-steiner-one-cap-trades.json')
    field=load(work/'swapped-steiner-field-family.json')
    witness=load(work/'swapped-steiner-witness69.json')
    verify_coverage(roots,carriers)
    verify_bound_records(color['records'],native['records'])
    C.require(witness==load(HERE/'WITNESS69.json'), 'changed canonical witness')
    positive=verify_trade(witness)
    acl=tuple(frozenset(i for i,b in enumerate(line.strip()) if b=='1')
              for line in (INPUTS/'acl69.txt').read_text().splitlines())
    C.require(len(acl)==len(set(acl))==69 and all(len(w)==5 for w in acl) and
              all(len(a&b)<=2 for a,b in combinations(acl,2)), 'ACL69 primary baseline')
    acl_profile=sorted(Counter(sum(v in w for w in acl) for v in range(18)).items())
    C.require(acl_profile==[(12,1),(18,2),(19,3),(20,12)] and
              acl_profile!=positive['degree_profile'], 'degree profile comparison')
    damages=controls(roots,carriers,color['records'],native['records'],witness) if run_controls else None
    stats=[{'fixture':i,'mates':len(c['mates']),'raw_maps':sum(r['raw_maps'] for r in c['mates']),
            'valid_maps':len(c['rows']),'rooted_cases':sum(r['fixture']==i for r in roots['roots'])}
           for i,c in enumerate(carriers)]
    return {'agent':'six-code-2','role':'researcher','status':'COMPLETE_SCOPED_SHARP69',
            'fixtures':stats,'eligible_mates':sum(s['mates'] for s in stats),
            'raw_maps':sum(s['raw_maps'] for s in stats),'valid_maps':len(roots['coverage']),
            'rooted_cases':len(roots['roots']),
            'carrier_sha256':digest([stable(c) for c in carriers]),
            'actual_groups_sha256':digest(groups['groups']),'group_orders':groups['orders'],
            'positive_roots_and_coverage_sha256':digest({'roots':roots['roots'],'coverage':roots['coverage']}),
            'weighted_results_sha256':digest(stable(color['records'])),
            'native_results_sha256':digest(native['records']),
            'weighted_nodes':sum(r['nodes'] for r in color['records']),
            'native_nodes':sum(r['native_nodes'] for r in native['records']),
            'weighted_controls':color['small_weighted_controls'],'native_controls':native['native_small_cases'],
            'maximum_code_size_distribution':sorted(Counter(r['words'] for r in color['records']).items()),
            'roots_reaching69':[r['root'] for r in color['records'] if r['words']==69],
            'expanded_vertex_range':[min(r['expanded_vertices'] for r in native['records']),max(r['expanded_vertices'] for r in native['records'])],
            'classical68_sha256':digest(baseline),'trade_family_sha256':digest(stable(trades)),
            'field_family_sha256':digest(field),'canonical_witness':positive,
            'acl69_degree_profile':acl_profile,'controls':damages}
