"""Separately rebuild both anchors/all high placements and replay quota trees."""
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def require(condition,message):
    if not condition:raise ValueError(message)


def digest(value):
    return sha256((json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()


def model(name):
    if name == 'cycle10':
        cells = tuple(sorted((r,(r+d)%5) for r in range(5) for d in (2,3,4)))
    else:
        require(name == 'cycle6_cycle4','unknown literal model')
        cells = tuple((r,c) for r in range(5) for c in range(5)
                      if (r<2<=c) or (c<2<=r) or (r>=2 and c==2+r%3))
    anchors = tuple(tuple(x for x,c in enumerate(cells) if c[0]==r)+(15,) for r in range(5))
    anchors += tuple(tuple(x for x,c in enumerate(cells) if c[1]==r)+(16,) for r in range(5))
    covered = Counter(e for q in anchors for e in combinations(q,2))
    require(len(covered)==60 and set(covered.values())=={1},'literal anchor pair error')
    eligible = tuple(e for e in combinations(range(15),2) if e not in covered)
    candidates = tuple(q for q in combinations(range(15),4)
                       if set(combinations(q,2)) <= set(eligible))
    return cells,anchors,eligible,candidates


def group(cells,anchors):
    """Derive column maps from row-neighborhood images; do not scan column5!."""
    position = {c:x for x,c in enumerate(cells)}
    target = tuple(frozenset(r for r,c in cells if c==j) for j in range(5))
    maps = set()
    for swap in (False,True):
        source = tuple(frozenset(c if swap else r for r,c in cells
                                 if (r if swap else c)==j) for j in range(5))
        for row_map in permutations(range(5)):
            wanted = tuple(frozenset(row_map[x] for x in n) for n in source)
            options = tuple(tuple(j for j,n in enumerate(target) if n==w) for w in wanted)
            for col_map in product(*options):
                if len(set(col_map))!=5:continue
                image = tuple(position[(row_map[c],col_map[r])] if swap
                              else position[(row_map[r],col_map[c])] for r,c in cells)
                p = image+((16,15) if swap else (15,16))
                require(len(set(p))==17 and {tuple(sorted(p[x] for x in q)) for q in anchors}
                        == set(anchors),'literal derived map changes anchors')
                maps.add(p)
    return tuple(sorted(maps))


def input_for(high,anchors,eligible,candidates):
    high = frozenset(high)
    r = sum(set(e)<=high for q in anchors for e in combinations(q,2))
    if r>5:return None
    quota = tuple(2 if x in high else 3 for x in range(15))
    mandatory = tuple(e for e in eligible if not set(e)&high)
    columns = tuple(q for q in candidates
                    if sum(set(e)<=high for e in combinations(q,2)) <= 5-r)
    return quota,mandatory,columns,r


def replay(tree,eligible,columns,quota,mandatory):
    edges = tuple(frozenset(combinations(q,2)) for q in columns)
    nodes = 0
    def visit(node,available,left,need):
        nonlocal nodes
        nodes += 1
        require(any(left) or need,'negative tree reached positive completion')
        require(type(node) is list and len(node)==3,'malformed quota proof node')
        tag,pivot,children = node
        require(tag in ('P','V','C') and type(pivot) is int and type(children) is list,
                'malformed quota pivot')
        if tag=='P':
            require(0<=pivot<len(eligible) and eligible[pivot] in need,'pair pivot not mandatory')
        else:
            require(0<=pivot<15 and left[pivot]>0,'point pivot has no remaining quota')
        compatible = [i for i,q in enumerate(columns) if edges[i]<=available
                      and all(left[x]>0 for x in q)
                      and ((eligible[pivot] in edges[i]) if tag=='P' else pivot in q)]
        if tag=='C':
            require(not children and len(compatible)<left[pivot],'false point-capacity leaf')
            return
        require(all(type(c) is list and len(c)==2 and type(c[0]) is int for c in children)
                and [c[0] for c in children]==compatible,'missing/extra/reordered quota branch')
        for i,child in children:
            after = list(left)
            for x in columns[i]:after[x]-=1
            require(min(after)>=0,'literal quota underflow')
            visit(child,available-edges[i],tuple(after),need-edges[i])
    visit(tree,frozenset(eligible),tuple(quota),frozenset(mandatory))
    return nodes


def controls(first,tree):
    eligible,columns,quota,mandatory = first
    require(tree[2],'control tree has no branches')
    mutations = []
    bad = deepcopy(tree);bad[2].pop();mutations.append(bad)
    bad = deepcopy(tree);bad[1]=100;mutations.append(bad)
    bad = deepcopy(tree);bad[2][0][0]=len(columns);mutations.append(bad)
    rejected = 0
    for bad in mutations:
        try:replay(bad,eligible,columns,quota,mandatory)
        except ValueError:rejected+=1
        else:raise ValueError('damaged quota proof accepted')
    q = columns[0]
    small_quota = tuple(int(x in q) for x in range(15))
    small_need = tuple(combinations(q,2))
    for fake in (['C',q[0],[]],['P',eligible.index(small_need[0]),[]],
                 ['V',q[0],[[0,['C',q[0],[]]]]]):
        try:replay(fake,eligible,(q,),small_quota,small_need)
        except ValueError:rejected+=1
        else:raise ValueError('positive cover accepted as quota rejection')
    from check_unit_five import solve,Incomplete
    witness,_,_=solve(eligible,(q,),small_quota,small_need)
    require(witness==(0,),'positive solver control failed')
    missing = next(e for e in eligible if e not in small_need)
    witness,valid,_=solve(eligible,(q,),small_quota,small_need+(missing,))
    require(witness is None and replay(valid,eligible,(q,),small_quota,small_need+(missing,))>=1,
            'separate negative control failed')
    try:solve(eligible,(q,),small_quota,small_need,node_limit=0)
    except Incomplete:pass
    else:raise ValueError('zero-cap search did not return incomplete')
    return {'corrupt_and_false_negative_proofs_rejected':rejected,
            'positive_solver_and_literal_negative_checked':True,'zero_cap_incomplete':True}


def main():
    summary = json.loads((HERE/'unit_five_expected.json').read_text())['primary']
    require(summary['status']=='COMPLETE_PRIMARY_ALL_FIBERS_UNREPLAYED',
            'primary carrier is incomplete')
    proofs = json.loads((HERE/'unit_five_certificate.json').read_text())
    case_index,node_counts,models,stream = 0,[],[],sha256()
    first = None
    import unit_five_carrier as primary
    for name in ('cycle10','cycle6_cycle4'):
        cells,anchors,eligible,candidates = model(name)
        maps = group(cells,anchors)
        require((cells,anchors,eligible,candidates)==primary.matrix(name)
                and maps==primary.group(name,cells,anchors),'literal model/candidate/map mismatch')
        buckets = {}
        for high in combinations(range(15),5):
            root = min(tuple(sorted(p[x] for x in high)) for p in maps)
            buckets.setdefault(root,set()).add(high)
            independent = input_for(high,anchors,eligible,candidates)
            other = primary.instance(high,eligible,candidates)
            require(independent==(None if other is None else other[:4]),
                    'entry-level raw high-placement input mismatch')
        require(sum(len(b) for b in buckets.values())==3003,'literal high carrier incomplete')
        begin,excluded,raw_excluded = case_index,0,0
        for high,members in sorted(buckets.items()):
            orbit = {tuple(sorted(p[x] for x in high)) for p in maps}
            stabilizer = [p for p in maps if tuple(sorted(p[x] for x in high))==high]
            require(orbit==members and len(members)*len(stabilizer)==len(maps),'literal orbit error')
            instance = input_for(high,anchors,eligible,candidates)
            if instance is None:
                excluded+=1;raw_excluded+=len(members);continue
            quota,mandatory,columns,r = instance
            record = summary['cases'][case_index]
            encoded = [high,eligible,columns,quota,mandatory]
            require(record['model']==name and tuple(record['high'])==high
                    and record['orbit_size']==len(members) and record['R']==r
                    and record['status']=='EXACT_NO_WITNESS_UNREPLAYED'
                    and record['input_sha256']==digest(encoded),'actual quota case mismatch')
            tree = proofs[str(case_index)]
            nodes = replay(tree,eligible,columns,quota,mandatory)
            require(nodes==record['nodes'],'rejection node count mismatch')
            node_counts.append(nodes)
            stream.update((json.dumps(encoded,separators=(',',':'))+'\n').encode())
            if first is None:first=(eligible,columns,quota,mandatory),tree
            case_index+=1
        models.append({'model':name,'group_order':len(maps),'high_orbits':len(buckets),
                       'residual_cases':case_index-begin,'immediate_high_pair_orbits':excluded,
                       'raw_immediate_high_pair_placements':raw_excluded,
                       'raw_high_placements':3003,'candidate_quadruples':len(candidates)})
    require(case_index==len(summary['cases'])==len(proofs)==267
            and set(proofs)=={str(i) for i in range(case_index)},'missing/extra quota proof case')
    report = {'agent':'six-code-1','role':'researcher','status':'COMPLETE_SEPARATE_LITERAL_REPLAY',
              'models':models,'cases':case_index,'raw_high_placements':6006,
              'nodes':sum(node_counts),'maximum_nodes':max(node_counts),
              'input_stream_sha256':stream.hexdigest(),'nodes_sha256':digest(node_counts),
              'certificate_bytes':(HERE/'unit_five_certificate.json').stat().st_size,
              'certificate_sha256':sha256((HERE/'unit_five_certificate.json').read_bytes()).hexdigest(),
              'five_edge_unit_star_exclusion':True,'independent_peer_review':False,
              'ordinary_bridges_formalized':False,'entry_level_6006_input_comparison':True,
              'controls':controls(*first)}
    require(report==json.loads((HERE/'unit_five_expected.json').read_text())['verification'],'separate expected report mismatch')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
