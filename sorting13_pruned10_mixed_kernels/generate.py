"""Witnessed mixed pruning and structural kernel templates for X/10."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def apply(values, network):
    values = list(values)
    for a,b in network:
        values[a],values[b] = min(values[a],values[b]),max(values[a],values[b])
    return values


def cut(prefix,order,high,low):
    kinds = [1 if i in high else -1 if i in low else 0 for i in range(11)]
    ports,number = [],0
    for kind in kinds:
        ports.append(None if kind else number)
        number += not kind
    retained,deleted = [],[]
    for step,(a,b) in enumerate(prefix):
        if kinds[a]==kinds[b]==0:
            retained.append([ports[a],ports[b]])
        else:
            deleted.append(step)
            if kinds[a]>kinds[b]:
                kinds[a],kinds[b] = kinds[b],kinds[a]
                ports[a],ports[b] = ports[b],ports[a]
    return {'fixed_maxima':list(high),'fixed_minima':list(low),'deleted_steps':deleted,
            'maximum_holes':[i for i,p in enumerate(order) if kinds[p]==1],
            'minimum_holes':[i for i,p in enumerate(order) if kinds[p]==-1],
            'retained_network':retained,'output_order':[ports[p] for p in order if ports[p] is not None]}


def minimum_templates():
    """Cheap leaf1; child0 has <=1 unary passage, child5 has <=2."""
    words=set()

    def before(pos,word,tokens,parent_unaries):
        if tokens:
            child=tokens[0]
            for empty in range(11):
                if empty in pos:
                    continue
                a,b=sorted((pos[child],empty))
                after=pos.copy();after[child]=a
                before(after,word+[(a,b)],tokens[1:],parent_unaries)
            return
        a,b=sorted(pos[:2]);parent=a;cheap=pos[2]
        merged=word+[(a,b)]
        if parent_unaries:
            for empty in range(11):
                if empty not in (parent,cheap):
                    lo,hi=sorted((parent,empty))
                    words.add(tuple(merged+[(lo,hi),tuple(sorted((lo,cheap)))]))
        else:
            words.add(tuple(merged+[tuple(sorted((parent,cheap)))]))

    for parent_unaries in (0,1):
        for a in range(2-parent_unaries):
            for b in range(3-parent_unaries):
                for tokens in itertools.product((0,1),repeat=a+b):
                    if tokens.count(0)==a and tokens.count(1)==b:
                        before([0,5,1],[],tokens,parent_unaries)
    assert len(words)==1826
    # The opposite maximum trajectory10 is permanently on wire10. Initial
    # min0 <= max10 forbids a shared (0,10) gate in a minimum completion.
    words={word for word in words if (0,10) not in word}
    assert len(words)==1608
    return sorted(words)


def maximum_templates():
    """All three route caps2; the only unary can touch the cheap tree leaf."""
    words=set()
    for cheap in (6,9,10):
        children=[p for p in (6,9,10) if p!=cheap]
        a,b=children;parent=b
        words.add(((a,b),tuple(sorted((parent,cheap)))))
        for empty in range(11):
            if empty not in (6,9,10):
                lo,hi=sorted((cheap,empty))
                words.add(((lo,hi),(a,b),tuple(sorted((parent,hi)))))
        for empty in range(11):
            if empty not in (parent,cheap):
                lo,hi=sorted((cheap,empty))
                words.add(((a,b),(lo,hi),tuple(sorted((parent,hi)))))
    assert len(words)==54
    # In these templates (0,6) can only be the unary on singleton leaf6.
    # Both leaf6 and leaf10 start above the fixed minimum trajectory0.
    words={word for word in words if not set(word)&{(0,6),(0,10)}}
    assert len(words)==50
    return sorted(words)


def word_summary(identifier,side,positions,caps,words):
    data=(json.dumps(words,separators=(',',':'))+'\n').encode()
    return {'id':identifier,'polarity':side,'initial_candidates':positions,
            'candidate_touch_caps':caps,'words':len(words),
            'counts_by_length':{str(k):sum(len(w)==k for w in words) for k in range(2,6)},
            'canonical_word_sha256':hashlib.sha256(data).hexdigest()}


def build(fixture):
    prefix,order=fixture['prefix'],fixture['prefix_output_order']
    states=sorted({sum(apply([x>>i&1 for i in range(11)],prefix)[p]<<j for j,p in enumerate(order))
                   for x in range(2048)})
    best={}
    for side in ('maximum','minimum'):
        for fixed in range(11):
            row=cut(prefix,order,[fixed] if side=='maximum' else [],[fixed] if side=='minimum' else [])
            wire=(row['maximum_holes'] if side=='maximum' else row['minimum_holes'])[0]
            key=(side,wire)
            if key not in best or len(row['deleted_steps'])>len(best[key]['deleted_steps']):
                row.update({'polarity':side,'wire':wire,'suffix_touch_cap':35-29-len(row['deleted_steps'])})
                best[key]=row
    mixed={}
    for high,low in itertools.permutations(range(11),2):
        row=cut(prefix,order,[high],[low])
        i,j=row['maximum_holes'][0],row['minimum_holes'][0]
        key=(i,j)
        if key not in mixed or len(row['deleted_steps'])>len(mixed[key]['deleted_steps']):
            row.update({'maximum_wire':i,'minimum_wire':j,'suffix_union_cap':35-25-len(row['deleted_steps'])})
            mixed[key]=row
    ordered=[[i,j] for i,j in sorted(mixed) if all((x>>j&1)<=(x>>i&1) for x in states)]
    minima=minimum_templates();maxima=maximum_templates()
    covers=[word_summary('minimum_1608','minimum',[0,5,1],[3,4,1],minima),
            word_summary('maximum_50','maximum',[6,9,10],[2,2,2],maxima)]
    covers[0]['opposite_fixed_trajectory']={'polarity':'maximum','wire':10,'ordered_candidates':[0,1]}
    covers[1]['opposite_fixed_trajectory']={'polarity':'minimum','wire':0,'ordered_candidates':[6,10]}
    return {'schema':1,'agent':'six-sorting-2','role':'researcher','target':'X/10',
            'prefix_size':14,'completion_budget':21,'full_budget':35,
            'known_lower_sizes':{'9':25,'10':29,'11':35},'states':states,
            'single_extremum_bounds':[best[k] for k in sorted(best)],
            'mixed_bounds':[mixed[k] for k in sorted(mixed)],
            'initially_ordered_max_min_pairs':ordered,'derived_minimum_caps':{'0':3,'1':2,'5':4},
            'kernel_cover':covers,'tagged_cover_count':1658}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--export-kernels',type=Path)
    args=parser.parse_args()
    certificate=build(json.loads((ROOT/'fixture.json').read_text()))
    if args.check:
        assert certificate==json.loads((ROOT/'certificate.json').read_text())
    else:
        (ROOT/'certificate.json').write_text(json.dumps(certificate,indent=2,sort_keys=True)+'\n')
    if args.export_kernels:
        args.export_kernels.write_text(json.dumps({'minimum_1608':minimum_templates(),'maximum_50':maximum_templates()},separators=(',',':'))+'\n')
    print(json.dumps({'states':len(certificate['states']),
                      'mixed_matrix':[r['suffix_union_cap'] for r in certificate['mixed_bounds']],
                      'derived_minimum_caps':certificate['derived_minimum_caps'],
                      'kernel_words':[c['words'] for c in certificate['kernel_cover']],
                      'tagged_cover_count':certificate['tagged_cover_count']}))
