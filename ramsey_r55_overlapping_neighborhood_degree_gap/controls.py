"""Reject malformed/local-non-Ramsey pieces without a repair search."""
import argparse
import copy
import itertools as it
import json
from pathlib import Path
import check


def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True)
    a=p.parse_args();base=Path(__file__).resolve().parent;results={}
    for d in (92,93):
        H=json.loads((base/f'H{d}.json').read_text())
        Q=[json.loads((base/f'Q{d}_{j}.json').read_text()) for j in (0,1)]
        for j in (0,1):
            bad=[]
            def mutate(label,change):
                g=copy.deepcopy(Q[j]);change(g);bad.append((label,g))
            mutate('extra_field',lambda g:g.update(extra=True))
            mutate('wrong_order',lambda g:g.update(n=23))
            mutate('boolean_order',lambda g:g.update(n=True))
            mutate('duplicate',lambda g:g['red_edges'].append(g['red_edges'][0]))
            mutate('missing_edge',lambda g:g['red_edges'].pop())
            mutate('reverse_pair',lambda g:g['red_edges'][0].reverse())
            mutate('bad_endpoint',lambda g:g['red_edges'].__setitem__(0,[0,22]))
            mutate('float_endpoint',lambda g:g['red_edges'].__setitem__(0,[0,1.0]))
            mutate('unsorted',lambda g:g['red_edges'].reverse())
            mutate('not_list',lambda g:g.update(red_edges=tuple(g['red_edges'])))
            red={tuple(e) for e in Q[j]['red_edges']}
            free=[e for e in it.combinations(range(1,22),2) if e[1]>=13]
            fixed_edge=next(e for e in sorted(red) if e[1]<13)
            free_blue=next(e for e in free if e not in red)
            g=dict(n=22,red_edges=[list(e) for e in sorted((red-{fixed_edge})|{free_blue})])
            bad.append(('balanced_fixed_core_change',g))
            corruption=None
            for removed in [e for e in free if e in red]:
                for added in [e for e in free if e not in red]:
                    modified=(red-{removed})|{added}
                    blue=set(it.combinations(range(22),2))-modified
                    r=next(check.bit_cliques(check.rows_for(22,modified),(1<<22)-1,5),None)
                    b=next(check.bit_cliques(check.rows_for(22,blue),(1<<22)-1,4),None)
                    if r is not None or b is not None:
                        corruption=dict(removed=list(removed),added=list(added),red_K5_mask=r,blue_K4_mask=b)
                        bad.append(('balanced_free_clique_change',dict(n=22,red_edges=[list(e) for e in sorted(modified)])))
                        break
                if corruption is not None:break
            check.need(corruption is not None,'no genuine clique corruption')
            for label,g in bad:
                inputs=Q.copy();inputs[j]=g
                try:check.audit(H,*inputs,d)
                except ValueError:pass
                else:raise ValueError('accepted corruption: '+label)
            results[f'{d}-{j}']=dict(rejected=[label for label,_ in bad],balanced_free_corruption=corruption)
    with a.report.open('x') as f:json.dump(results,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps(results),flush=True)


if __name__=='__main__':main()
