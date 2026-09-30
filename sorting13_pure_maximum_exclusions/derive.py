"""Exact ternary pruning witnesses for three binary-only maximum kernels."""
import itertools
import json
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEP = next(p/'sorting13_pruned10_mixed_kernels' for p in (HERE.parent,HERE.parents[2])
           if (p/'sorting13_pruned10_mixed_kernels').is_dir())
LOWER = [0,0,1,3,5,9,12,16,19,25,29,35]
AFTER = [(3,10),(6,9),(9,10)]
PURE = [[(5,8),(4,8),(6,8),(8,9)],
        [(4,8),(5,8),(6,8),(8,9)],
        [(4,5),(5,8),(6,8),(8,9)]]


def image(states, gates, n):
    result = set()
    for x in states:
        for a,b in gates:
            if x>>a&1 and not x>>b&1:
                x ^= (1<<a)|(1<<b)
        result.add(x&((1<<n)-1))
    return sorted(result)


def derive():
    start = time.monotonic()
    fixture = json.loads((DEP/'fixture.json').read_text())
    X = json.loads((DEP/'certificate.json').read_text())['states']
    K = image(X, AFTER, 10)
    frontiers = [dict(prefix=prefix,residual_states=image(K,prefix,9)) for prefix in PURE]
    best = [{} for _ in frontiers]
    kernel_best = {}
    # Shared first17 gates are evaluated only once per ternary assignment.
    for colors in itertools.product(range(3),repeat=11):
        v = list(colors); D = 0
        for a,b in fixture['prefix']:
            D += v[a]!=1 or v[b]!=1
            v[a],v[b] = min(v[a],v[b]),max(v[a],v[b])
        v = [v[i] for i in fixture['prefix_output_order']]
        for a,b in AFTER:
            D += v[a]!=1 or v[b]!=1
            v[a],v[b] = min(v[a],v[b]),max(v[a],v[b])
        kx=sum((value==2)<<i for i,value in enumerate(v[:10]))
        ky=sum((value!=0)<<i for i,value in enumerate(v[:10]))
        if ky==1023 and kx in (64,512):
            cap=35-LOWER[colors.count(1)]-D
            if kx not in kernel_best or cap<kernel_best[kx]['cap']:
                kernel_best[kx]=dict(x=kx,y=ky,cap=cap,deleted=D,
                    fixed_high=[i for i,value in enumerate(colors) if value==2],
                    fixed_low=[i for i,value in enumerate(colors) if value==0],
                    middle_count=colors.count(1))
        for c,frontier in enumerate(frontiers):
            z = list(v); d = D
            for a,b in frontier['prefix']:
                d += z[a]!=1 or z[b]!=1
                z[a],z[b] = min(z[a],z[b]),max(z[a],z[b])
            x = sum((value==2)<<i for i,value in enumerate(z[:9]))
            y = sum((value!=0)<<i for i,value in enumerate(z[:9]))
            cap = 35-LOWER[colors.count(1)]-d
            key = x,y
            if key not in best[c] or cap<best[c][key]['cap']:
                best[c][key] = dict(x=x,y=y,cap=cap,deleted=d,
                    fixed_high=[i for i,value in enumerate(colors) if value==2],
                    fixed_low=[i for i,value in enumerate(colors) if value==0],
                    middle_count=colors.count(1))
    result = dict(agent='six-sorting-2',role='researcher',reference_budget=14,
                  full_prefix_size=21,full_budget=35,lower_sizes=LOWER,
                  ternary_inputs=3**11,kernel_states=K,
                  kernel_bounds=[kernel_best[x] for x in (64,512)],cases=[])
    for c,frontier in enumerate(frontiers):
        J = image(K,frontier['prefix'],9)
        assert J==frontier['residual_states']
        assert all(x in J and y in J for x,y in best[c])
        maxima = {x:best[c][x,511] for x in J}
        minima = {y:best[c][0,y] for y in J}
        mc = sorted(x.bit_length()-1 for x in J if x.bit_count()==1)
        nc = sorted((511^x).bit_length()-1 for x in J if x.bit_count()==8)
        critical = [maxima[1<<i] for i in mc]+[minima[511^(1<<i)] for i in nc]
        mixed = [r for (x,y),r in best[c].items() if x and y!=511 and r['cap']<14
                 and r['cap']<maxima[x]['cap']+minima[y]['cap']]
        mixed.sort(key=lambda r:(r['cap'],r['cap']-maxima[r['x']]['cap']-minima[r['y']]['cap'],r['x'],r['y']))
        all_single = sorted([r for r in list(maxima.values())+list(minima.values())
                             if r['cap']<14],key=lambda r:(r['x'],r['y']))
        row = dict(case=c,prefix=frontier['prefix'],residual_wires=9,residual_states=J,
                   maximum_candidates=mc,minimum_candidates=nc,
                   maximum_caps=[maxima[1<<i]['cap'] for i in mc],
                   minimum_caps=[minima[511^(1<<i)]['cap'] for i in nc],
                   critical_single_bounds=critical,all_single_bounds=all_single,
                   selected_mixed_bounds=mixed[:32],nested_pairs=len(best[c]),
                   strict_mixed_pairs=len(mixed))
        result['cases'].append(row)
        print(json.dumps({k:row[k] for k in ('case','maximum_candidates','minimum_candidates','maximum_caps','minimum_caps','nested_pairs','strict_mixed_pairs')}),flush=True)
    (HERE/'pruning.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'seconds':time.monotonic()-start,'single_bounds':[len(c['all_single_bounds']) for c in result['cases']],
                      'mixed_caps':[[r['cap'] for r in c['selected_mixed_bounds'][:8]] for c in result['cases']]}))


if __name__=='__main__':derive()
