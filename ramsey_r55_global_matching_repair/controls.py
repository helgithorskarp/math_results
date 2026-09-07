"""Exhaustive small matching families versus literal full graph enumeration."""
import copy
import json
from itertools import combinations

import produce
import verify


def ensure(ok, message):
    if not ok:
        raise RuntimeError(message)


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first, rest = vertices[0], vertices[1:]
    yield from matchings(rest)
    for i, second in enumerate(rest):
        for tail in matchings(rest[:i] + rest[i+1:]):
            yield ((first, second),) + tail


def run():
    stats = {"complete_small_graph_families": 0, "literal_matching_assignments": 0,
             "incremental_round_trips": 0, "verified_sat_families": 0,
             "verified_unsat_families": 0, "checked_proof_nodes": 0}
    for n in range(3, 6):
        pairs = list(combinations(range(n), 2))
        index = {e: i for i, e in enumerate(pairs)}
        mm = list(matchings(tuple(range(n))))
        ensure(len(mm) == {3:4, 4:10, 5:26}[n], "small matching count")
        for k in ([3] if n < 5 else [3,5]):
            for word in range(2**len(pairs)):
                state = produce.State(n, word, k)
                original_bad = set(state.bad)
                possible = False
                for matching in mm:
                    literal = verify.dense(n, word)
                    for u, v in matching:
                        literal[u][v] ^= 1
                        literal[v][u] ^= 1
                        state.flip(index[u,v])
                    bad = verify.bad_sets(literal, k)
                    physical_masks = {sum(2**v for v in q) for q, color in bad}
                    ensure(state.bad == physical_masks, "incremental physical bad-set mismatch")
                    possible |= not bad
                    for u, v in reversed(matching):
                        state.flip(index[u,v])
                    ensure(state.bad == original_bad, "incremental rollback mismatch")
                    stats["literal_matching_assignments"] += 1
                    stats["incremental_round_trips"] += 1
                proof = produce.decide(n, word, k, [10000])
                ensure((proof['status'] == 'SAT') == possible and proof['status'] != 'UNKNOWN', "complete small family decision")
                checked = verify.check(n, word, proof, k)
                stats["complete_small_graph_families"] += 1
                stats["verified_sat_families" if possible else "verified_unsat_families"] += 1
                stats["checked_proof_nodes"] += checked.get('nodes',0)
    n, k, word = 6, 3, 2**15-1
    proof = produce.decide(n, word, k)
    ensure(proof['status']=='UNSAT', 'nonvacuous unsat control')
    verify.check(n, word, proof, k)
    corrupt=[]
    for field,value in [('status','UNKNOWN'),('n',7),('k',4),('root',1)]:
        p=copy.deepcopy(proof);p[field]=value;corrupt.append(p)
    p=copy.deepcopy(proof);p['nodes'][0][0]=1;corrupt.append(p)
    p=copy.deepcopy(proof);p['nodes'][0][1].pop();corrupt.append(p)
    p=copy.deepcopy(proof);p['nodes'][0][1].append(0);corrupt.append(p)
    p=copy.deepcopy(proof);p['nodes'][0][1][0]=0;corrupt.append(p)
    p=copy.deepcopy(proof);p['nodes'][0][1][0]=len(p['nodes']);corrupt.append(p)
    p=copy.deepcopy(proof);p['nodes'].append(copy.deepcopy(p['nodes'][0]));corrupt.append(p)
    p=copy.deepcopy(proof);p['nodes'][0]=None;corrupt.append(p)
    for p in corrupt:
        try: verify.check(n,word,p,k)
        except (ValueError,TypeError): pass
        else: raise RuntimeError('bad DAG accepted')
    # A changed physical pair breaks the supplied root obstruction.
    try: verify.check(n,word ^ 1,proof,k)
    except ValueError: pass
    else: raise RuntimeError('wrong parent accepted')
    unknown=produce.decide(n,word,k,[0])
    ensure(unknown['status']=='UNKNOWN','zero budget status')
    try: verify.check(n,word,unknown,k)
    except ValueError: pass
    else: raise RuntimeError('unfinished proof accepted')
    pairs=list(combinations(range(5),2))
    cycle={tuple(sorted((i,(i+1)%5))) for i in range(5)}
    c5=sum(2**i for i,e in enumerate(pairs) if e in cycle)
    sat=produce.decide(5,c5,3)
    ensure(sat['status']=='SAT' and sat['matching']==[],'positive C5 control')
    sat_corrupt=[]
    for matching in ([0],[0,1],[10],[True]):
        p=copy.deepcopy(sat);p['matching']=matching;sat_corrupt.append(p)
    for p in sat_corrupt:
        try: verify.check(5,c5,p,3)
        except (ValueError,TypeError): pass
        else: raise RuntimeError('bad SAT certificate accepted')
    stats.update({"corrupt_DAG_rejections":len(corrupt),"wrong_parent_rejections":1,
                  "unfinished_proof_rejections":1,"corrupt_SAT_rejections":len(sat_corrupt),
                  "status":"VERIFIED_MATCHING_COVER_CONTROLS"})
    return stats


if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
