"""Complete physical redirect, composed with the preceding exchange normal form.

No queue, assumption stream, or verdict ledger is read or changed.
"""
from pathlib import Path
from itertools import combinations
import argparse
import json
import sys
PREVIOUS = Path(__file__).resolve().parent.parent/'ramsey_r55_core_exchange_normal_form'
sys.path.insert(0,str(PREVIOUS))
from exchange import decode, validate, descend, potential, clique, need
from catalog import Lookup
from destination import normalize


def blue_pair(a, vertices):
    fours = [list(S) for S in combinations(sorted(vertices),4)
             if all(a[u][v] == 0 for u,v in combinations(S,2))]
    for S,T in combinations(fours,2):
        if set(S).isdisjoint(T):
            return S,T
    return None


def augment_blue(a, red, blue, core):
    """One q=7 mixed-stratum redirect, or a literal blue five obstruction.

    Red blocks are retained exactly. Red maximality is unchanged because
    the union of the blue blocks and the core is unchanged.
    """
    red,blue,core = [B[:] for B in red],[B[:] for B in blue],core[:]
    validate(a,red,blue,core)
    need(len(a)==43 and len(red)+len(blue)==7 and len(red) in (5,6),'mixed q7 source')
    old = blue.pop(0); vertices = sorted(old+core)
    five = clique(a,vertices,5,0)
    if five is not None:
        return dict(status='MONOCHROMATIC_FIVE',color=0,vertices=five)
    pair = blue_pair(a,vertices)
    need(pair is not None,'sharp 19-vertex lemma failed; do not publish a redirect')
    blue.extend(pair); core = sorted(set(vertices)-set(sum(pair,[])))
    extra = []
    while True:
        K = clique(a,core,4,0)
        if K is None:
            break
        blue.append(K); extra.append(K); core = sorted(set(core)-set(K))
    validate(a,red,blue,core)
    need(8 <= len(red)+len(blue) <= 10,'larger q destination')
    return dict(status='BLUE_PACKING_AUGMENTATION',red=red,blue=blue,core=core,
                old_block=old,new_pair=list(pair),additional_blocks=extra)


def run(source, lookup):
    a = decode(source)
    red,blue,core = source['red'],source['blue'],source['core']
    validate(a,red,blue,core)
    need(len(a)==43 and len(red)>=5,'complete carrier source')
    stages = []; moves = 0
    while True:
        before = potential(a,red,blue,core)
        q,r = len(red)+len(blue),len(red)
        if q == 7 and r < 7:
            event = augment_blue(a,red,blue,core)
            if event['status'] == 'MONOCHROMATIC_FIVE':
                return dict(status='MONOCHROMATIC_FIVE',physical_five_in_input_labels=event,
                            stages=stages,new_original_task_verdict=False)
            red,blue,core = event['red'],event['blue'],event['core']
            need(potential(a,red,blue,core)>before,'blue augmentation potential')
            stages.append(event); moves += 1
        final = descend(a,red,blue,core)
        stages.append(dict(kind='PREVIOUS_NORMAL_FORM_DESCENT',steps=final['steps']))
        moves += len(final['steps'])
        red,blue,core = final['red'],final['blue'],final['core']
        need(moves <= 675,'combined finite potential')
        if len(red)+len(blue)!=7 or len(red)==7:
            break
    dest = normalize(a,final,lookup)
    return dict(status='GLOBAL_REDIRECT_NOT_ORIGINAL_TASK_UNSAT',packing=final,destination=dest,
                stages=stages,potential_moves=moves,new_original_task_verdict=False)


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('catalog_directory'); p.add_argument('source'); p.add_argument('output')
    args = p.parse_args()
    out = run(json.loads(Path(args.source).read_text()),Lookup(args.catalog_directory))
    Path(args.output).write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
