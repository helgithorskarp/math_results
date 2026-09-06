"""Entrywise verifier comparison and malformed-graph controls."""
import argparse
import copy
import itertools as it
import json
from pathlib import Path

import verify
import bitcheck


def need(ok, text):
    if not ok:
        raise ValueError(text)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--directory',type=Path,default=Path(__file__).resolve().parent)
    p.add_argument('--report',type=Path,required=True)
    a=p.parse_args(); results={}
    for d in (92,93):
        g=json.loads((a.directory/f'H{d}.json').read_text())
        literal,details=verify.audit(g,d)
        packed,packed_details=bitcheck.audit(g,d)
        need(literal==packed and details==packed_details,'entrywise comparison')
        bad=[]
        def mutate(label, change):
            h=copy.deepcopy(g);change(h);bad.append((label,h))
        mutate('extra_field',lambda h:h.update(extra=True))
        mutate('wrong_n',lambda h:h.update(n=21))
        mutate('boolean_n',lambda h:h.update(n=True))
        mutate('duplicate_edge',lambda h:h['red_edges'].append(h['red_edges'][0]))
        mutate('missing_edge',lambda h:h['red_edges'].pop())
        mutate('reversed_pair',lambda h:h['red_edges'][0].reverse())
        mutate('out_of_range',lambda h:h['red_edges'].__setitem__(0,[0,20]))
        mutate('float_endpoint',lambda h:h['red_edges'].__setitem__(0,[0,10.0]))
        mutate('unsorted_edges',lambda h:h['red_edges'].reverse())
        mutate('nonlist_edges',lambda h:h.update(red_edges=tuple(h['red_edges'])))
        red={tuple(e) for e in g['red_edges']}
        free=[e for e in it.combinations(range(2,20),2) if e[1]>=10]
        w_removed=next(e for e in sorted(red) if 2<=e[0]<e[1]<10)
        w_added=next(e for e in free if e not in red)
        h=dict(n=20,red_edges=[list(e) for e in sorted((red-{w_removed})|{w_added})])
        bad.append(('balanced_W_change',h))
        # A balanced free-pair corruption preserves the density and every
        # fixed interface pair. Find one that fails actual Ramsey conditions.
        corruption=None
        for removed in [e for e in free if e in red]:
            for added in [e for e in free if e not in red]:
                h=dict(n=20,red_edges=[list(e) for e in sorted((red-{removed})|{added})])
                try:
                    bitcheck.audit(h,d)
                except ValueError as err:
                    if str(err) in ('red K4','blue K5'):
                        corruption=dict(removed=list(removed),added=list(added),failure=str(err))
                        bad.append(('balanced_free_clique_change',h))
                        break
            if corruption is not None:
                break
        need(corruption is not None,'missing genuine Ramsey corruption')
        for label,h in bad:
            for checker in (verify.audit,bitcheck.audit):
                try:
                    checker(h,d)
                except ValueError:
                    pass
                else:
                    raise ValueError('accepted negative control: '+label)
        results[d]=dict(status='EXACT_REPORTS_AND_CLIQUE_LISTS_AGREE',
                        red_triangle_masks_compared=len(details['red_triangle_masks']),
                        blue_K4_masks_compared=len(details['blue_K4_masks']),
                        rejected_controls=[label for label,_ in bad],
                        balanced_free_corruption=corruption,
                        clique_detail_sha256=literal['clique_detail_sha256'])
    with a.report.open('x') as f:
        json.dump(results,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps(results),flush=True)


if __name__=='__main__':
    main()
