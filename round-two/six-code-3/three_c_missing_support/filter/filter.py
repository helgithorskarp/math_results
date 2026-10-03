"""Compare all physical transports with independent six-order normalization."""
import argparse,hashlib,itertools,json,time
from collections import Counter
from pathlib import Path
START=time.monotonic();STATES=0
def require(ok,message):
    if not ok:raise ValueError(message)
def tick():
    global STATES
    STATES += 1
    if STATES > 500000 or time.monotonic() - START > 20:
        raise RuntimeError('INCOMPLETE: original500000/20 guard')


def canonical(d):return hashlib.sha256(json.dumps(d,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();root=Path(__file__).parent
    e=json.loads((root/'EXPECTED.json').read_text());inputs={}
    for name,sha in e['precursor_math_sha256'].items():
        d=json.loads((root/(name+'.json')).read_text());math=d['mathematics']
        require(d['common_math_sha256']==canonical(math)==sha,'whole completed precursor mathematics: '+name)
        inputs[name]=math
    records=inputs['ANCHORS']['records'];ordered=inputs['ORDERED'];full=inputs['FULL'];star=inputs['STAR']
    require(len(records)==56 and len(star['pair_cases'])==42 and len(star['coverage'])==2352,'complete precursor domains')
    raw_rooted={p['anchor_index'] for c in star['pair_cases'] for p in c['positive_anchors']}
    rooted={s for s in range(56) if any(ordered['equivalence'][s][t]=='1' for t in raw_rooted)}
    require(rooted==raw_rooted,'observed whole rooted set is already S4 closed; closure was not assumed')
    by_source={s:[] for s in range(56)}
    for t in full['all_transports']:by_source[t['source']].append(t)
    left=[];negative_certificates=[]
    for s in range(56):
        require(len(by_source[s])==144,'all raw physical class/member maps for each source')
        bad=[]
        for t in by_source[s]:
            tick()
            if t['target'] not in rooted:bad.append(t)
        left.append(not bad)
        if bad:
            t=bad[0];image=t['point_image'];target=t['target']
            require({frozenset(image[p] for p in w) for w in records[s]['anchor']}==
                    {frozenset(w) for w in records[target]['anchor']},'entire negative physical transport certificate')
            require(target not in rooted and all(star['coverage'][56*k+target]=='0' for k in range(42)),
                    'infeasible rooted target, not arbitrary label absence')
            negative_certificates.append(dict(source=s,excluded_rooted_target=target,whole_transport=t))
    # A second algorithm constructs each of six class orders directly from
    # literal block incidence; it consults neither full transport list nor full orbits.
    cells=[(r,c) for r in range(4) for c in range(4) if r!=c]
    index_at={cell:k for k,cell in enumerate(cells)}
    lookup={tuple(r['colors']):k for k,r in enumerate(records)};right=[];normalization_records=[]
    for s,rec in enumerate(records):
        targets=[]
        for order in itertools.permutations(range(3)):
            tick();classes=[list(map(set,rec['classes'][k])) for k in order]
            colors=[None]*12
            for row_label,row in enumerate(classes[0]):
                for p in row:
                    col=next(t for t in classes[1] if p in t)
                    symbol=next(t for t in classes[2] if p in t)
                    column_label=next(k for k,t in enumerate(classes[0]) if not(t&col))
                    symbol_label=next(k for k,t in enumerate(classes[0]) if not(t&symbol))
                    colors[index_at[row_label,column_label]]=symbol_label
            require(tuple(colors) in lookup,'actual direct normalized physical target')
            target=lookup[tuple(colors)];targets.append(target)
            normalization_records.append(dict(source=s,class_order=list(order),target=target,rooted_feasible=target in rooted))
        right.append(all(t in rooted for t in targets))
    require(left==right,'all56 necessary-type bits from two different mechanisms')
    survivors=[s for s in range(56) if left[s]];excluded=[s for s in range(56) if not left[s]]
    require([c['source'] for c in negative_certificates]==excluded,'a whole physical obstruction transport for every excluded source')
    # No full orbit may have a mixed verdict; these are isomorphism invariants
    # of an anchor with all three roots required to have a C star.
    summaries=[]
    for group in full['orbits']:
        require(len({left[s] for s in group})==1,'whole class-orbit verdict consistency')
        summaries.append(dict(representative_index=group[0],orbit_size=len(group),
                              required_all_roots_locally_possible=left[group[0]]))
    result=dict(agent='six-code-3',role='researcher',status='COMPLETE_AUTHOR_CHECKED_ALL_THREE_C_ROOT_NECESSARY_TYPES',
                cases=56,rooted_possible_indices=sorted(rooted),surviving_anchor_indices=survivors,
                excluded_anchor_indices=excluded,all56_method_bits_equal=True,
                full_class_summaries=summaries,whole_negative_transport_certificates=negative_certificates,
                all_six_order_normalizations=normalization_records,states=STATES,guard_states=500000,guard_seconds=20,
                inputs_bound_to_completed_corpora=True,simultaneous_three_star_gluing_completed=False,
                ordinary_bridges_formalized=False,independent_person_review=False,unrestricted_endpoint_improvement=False)
    result['whole_result_math_sha256']=canonical(result)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['whole_negative_transport_certificates','all_six_order_normalizations']},sort_keys=True))
if __name__=='__main__':main()
