#!/usr/bin/env python3
"""Reconstruct every fixed-core exclusion tree independently.

Literal Steiner triples and combination traversal reconstruct the full row
universe. Indexed sets reconstruct each emitted domain from all rows.
Full S6 permutation orbits audit the type partition and normalization.
Imports no generator code. Assertions must remain enabled.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
if not __debug__:
    raise RuntimeError('run this checker with Python assertions enabled')
Y = [1, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 20, 23, 24]


def core_from_triples():
    blocks = [frozenset((x+d) % 13 for d in base)
              for base in [(0, 1, 4), (0, 2, 7)] for x in range(13)]
    assert len(set(blocks)) == 26
    assert all(sum(set(p) <= b for b in blocks) == 1
               for p in combinations(range(13), 2))
    triples = [blocks[i] for i in Y]
    return [frozenset(j for j, b in enumerate(triples)
                      if i != j and not a & b)
            for i, a in enumerate(triples)]


def known_adjacency(core, masks, J):
    """Unknown cross edges belong to neither color; all J edges are known."""
    vertices = set(range(16))
    red = [set(s) for s in core]+[set() for _ in range(6)]
    blue = [vertices-{i}-set(s) for i, s in enumerate(core)]+[set() for _ in range(6)]
    for role in range(6):
        red[16+role] = {16+j for j in J[0][role]}
        blue[16+role] = {16+j for j in J[1][role]}
    for role, mask in masks.items():
        for y in range(16):
            adjacency = red if mask >> y & 1 else blue
            adjacency[16+role].add(y)
            adjacency[y].add(16+role)
    return red, blue


def first_book(core, masks, J):
    for color, adjacency in enumerate(known_adjacency(core, masks, J)):
        cap = [3, 6][color]
        for i in range(22):
            for j in range(i):
                if j in adjacency[i]:
                    pages = adjacency[i] & adjacency[j]
                    if len(pages) > cap:
                        return color, j, i, sorted(pages)[:cap+1]
    return None


def compute(trace_directory, progress_path, max_seconds):
    core = core_from_triples()
    fixture = (HERE/'core16.edges').read_text().splitlines()
    assert fixture[0] == '16'
    fixture_edges = [tuple(map(int, line.split())) for line in fixture[1:]]
    assert len(fixture_edges) == len(set(fixture_edges)) == 48
    assert set(fixture_edges) == {(i, j) for i in range(16) for j in core[i] if j < i}
    vertices = frozenset(range(16))
    blue_core = [vertices-{i}-ns for i, ns in enumerate(core)]
    assert all(len(s) == 6 for s in core)
    spines = [(i, j, color) for color, adjacency in enumerate([core, blue_core])
              for i in range(16) for j in range(i) if j in adjacency[i]]
    capacities = [[3, 6][c]-len([core, blue_core][c][i] & [core, blue_core][c][j])
                  for i, j, c in spines]
    assert Counter(capacities) == {0: 3, 1: 45, 2: 69, 3: 3}
    zero = [(i, j, c) for (i, j, c), cap in zip(spines, capacities) if cap == 0]
    # Combination traversal and literal neighborhoods, rather than mask scan.
    row_sets = {}
    for size in range(17):
        for subset in combinations(range(16), size):
            ns = frozenset(subset)
            if any(len(core[y] & ns) > 3 for y in ns):
                continue
            bs = vertices-ns
            if any(i in [ns, bs][c] and j in [ns, bs][c] for i, j, c in zero):
                continue
            if any(len(blue_core[y] & bs) > 6 for y in bs):
                continue
            row_sets[sum(1 << y for y in ns)] = (ns, bs)
    masks = sorted(row_sets)
    ns = [row_sets[m][0] for m in masks]
    bs = [row_sets[m][1] for m in masks]
    m = len(masks)
    all_rows = (1 << m)-1
    row_id = {mask: i for i, mask in enumerate(masks)}
    ten = [i for i, n in enumerate(ns) if len(n) == 10]
    assert len(ten) == 4
    assert all(len(n) >= 5 and len(b) >= 6 for n, b in zip(ns, bs))
    assert all(len(core[y] & ns[i]) == 3 for i in ten for y in ns[i])
    not_ten = all_rows ^ sum(1 << i for i in ten)
    # Bit sets index rows, not core vertex assignments. All tables below are
    # derived from literal page definitions in this independent reconstruction.
    points = [sum(1 << i for i in range(m) if y in ns[i]) for y in range(16)]
    new_red = [[sum(1 << i for i in range(m)
                    if y not in ns[i] or len(core[y] & ns[i])+k <= 3)
                for k in range(6)] for y in range(16)]
    new_blue = [[sum(1 << i for i in range(m)
                     if y not in bs[i] or len(blue_core[y] & bs[i])+k <= 6)
                 for k in range(6)] for y in range(16)]
    features = [frozenset(k for k, (a, b, c) in enumerate(spines)
                          if a in [ns[i], bs[i]][c] and b in [ns[i], bs[i]][c])
                for i in range(m)]
    spine_rows = [sum(1 << i for i in range(m) if k in features[i])
                  for k in range(len(spines))]
    keys = [(0, cap) for cap in range(4)] + [(1, cap) for cap in range(2,7)]
    compat = {key: [0]*m for key in keys}
    for i in range(m):
        for j in range(i,m):
            common_red = (masks[i] & masks[j]).bit_count()
            common_blue = ((65535^masks[i]) & (65535^masks[j])).bit_count()
            for cap in range(common_red,4):
                compat[0,cap][i] |= 1<<j
                compat[0,cap][j] |= 1<<i
            for cap in range(max(common_blue,2),7):
                compat[1,cap][i] |= 1<<j
                compat[1,cap][j] |= 1<<i

    def members(bits):
        while bits:
            low = bits & -bits
            yield low.bit_length()-1
            bits ^= low

    def domain(context, role, J, base=all_rows):
        allowed = base
        # First intersect whole indexed pair domains. No branch is dropped
        # by a heuristic; every intersection expresses a spine inequality.
        for old_role, old_id in context:
            color = 0 if old_role in J[0][role] else 1
            cap = [3, 6][color]-len(J[color][role] & J[color][old_role])
            allowed &= compat[color, cap][old_id]
            if not allowed:
                return 0
        used = Counter(k for _, old_id in context for k in features[old_id])
        for k, count in used.items():
            assert count <= capacities[k], 'invalid input context'
            if count == capacities[k]:
                allowed &= all_rows ^ spine_rows[k]
                if not allowed:
                    return 0
        for old_role, old_id in context:
            color = 0 if old_role in J[0][role] else 1
            neighbor_set = [ns, bs][color][old_id]
            for y in neighbor_set:
                pages = len([core, blue_core][color][y] & neighbor_set)
                pages += sum(other_role in J[color][old_role] and
                             y in [ns, bs][color][other_id]
                             for other_role, other_id in context)
                assert pages <= [3, 6][color]
                if pages == [3, 6][color]:
                    allowed &= (all_rows ^ points[y]) if color == 0 else points[y]
                    if not allowed:
                        return 0
        for y in range(16):
            r = sum(old_role in J[0][role] and y in ns[old_id]
                    for old_role, old_id in context)
            b = sum(old_role in J[1][role] and y in bs[old_id]
                    for old_role, old_id in context)
            allowed &= new_red[y][r] & new_blue[y][b]
            if not allowed:
                return 0
        return allowed

    # The generator partitions by five adjacent transpositions. Here each
    # representative is checked by all720 permutations, with disjoint full
    # orbits covering all32768 labeled internal graphs.
    from itertools import permutations
    import time
    pair_list=list(combinations(range(6),2))
    pair_id={p:i for i,p in enumerate(pair_list)}
    perms=list(permutations(range(6)))
    types=json.loads((HERE/'core_extension_types.json').read_text())['types']
    generation={r['mask']:r for r in json.loads((HERE/'core_extension_expected.json').read_text())['cases']}
    checker_hash=sha256(Path(__file__).read_bytes()).hexdigest()
    generator_hash=sha256((HERE/'search_core_extension.cpp').read_bytes()).hexdigest()
    signature={'checker_sha256':checker_hash,'generator_sha256':generator_hash,
               'types_sha256':sha256((HERE/'core_extension_types.json').read_bytes()).hexdigest(),
               'expected_sha256':sha256((HERE/'core_extension_expected.json').read_bytes()).hexdigest()}
    progress={'agent':'six-books-2','role':'researcher','signature':signature,
              'verified':{},'complete':False}
    progress_path=Path(progress_path)
    if progress_path.exists():
        previous=json.loads(progress_path.read_text())
        assert previous['signature']==signature,'progress belongs to different source'
        progress=previous
    assert set(progress['verified']) <= {str(t['mask']) for t in types}, 'unknown checkpoint type'
    seen=set();metadata={}
    for case in types:
        mask=case['mask']
        edges=frozenset(pair_list[k] for k in range(15) if mask>>k&1)
        orbit=set();aut=[]
        for p in perms:
            moved=frozenset(tuple(sorted((p[a],p[b]))) for a,b in edges)
            word=sum(1<<pair_id[e] for e in moved)
            orbit.add(word)
            if moved==edges:aut.append(p)
        assert min(orbit)==mask and len(orbit)==case['labeled_graphs']
        assert not seen&orbit;seen|=orbit
        assert len(orbit)*len(aut)==720
        red=[frozenset(b for a,b in edges if a==i)|frozenset(a for a,b in edges if b==i) for i in range(6)]
        blue=[frozenset(range(6))-{i}-red[i] for i in range(6)]
        order=sorted(range(6),key=lambda r:(len(red[r]),r))
        stabilizer=aut;inequalities=[]
        for role in order:
            orbit_roles={p[role] for p in stabilizer}
            inequalities.extend((role,other) for other in sorted(orbit_roles-{role}))
            stabilizer=[p for p in stabilizer if p[role]==role]
        assert len(stabilizer)==1
        # Values enter only through their strict order. Check every ranking
        # of six distinct row masks, and every automorphism image of it.
        valid_ranks={ranks for ranks in perms if all(ranks[a]<ranks[b] for a,b in inequalities)}
        assert len(valid_ranks)==720//len(aut)
        for ranks in perms:
            canonical={tuple(ranks[p[v]] for v in range(6)) for p in aut}&valid_ranks
            assert len(canonical)==1,'normalization does not cover each orbit exactly once'
        metadata[mask]=(red,blue,inequalities,len(aut))
    assert seen==set(range(32768)) and len(types)==156
    progress['all32768_internal_graphs_covered']=True
    progress['all156_normalizations_checked_on720_rankings_each']=True
    started=time.monotonic()
    for case in types:
        mask=case['mask'];trace=Path(trace_directory)/f'{mask}.trace'
        digest=sha256(trace.read_bytes()).hexdigest()
        expected=generation[mask]['counts']
        assert expected['internal_red_mask']==mask
        assert expected['complete'] and expected['full_valid']==0
        assert digest==generation[mask]['trace_sha256']
        if str(mask) in progress['verified']:
            assert progress['verified'][str(mask)]['trace_sha256']==digest
            continue
        if progress['verified'] and max_seconds is not None and time.monotonic()-started>=max_seconds:
            break
        red,blue,inequalities,aut_count=metadata[mask];J=red,blue
        with trace.open() as lines:
            first=next(lines).split()
            if first[0]=='I':
                a,b,*pages=map(int,first[1:])
                assert 0<=a<6 and 0<=b<6 and a!=b
                assert all(0<=p<6 for p in pages)
                assert len(pages)==len(set(pages))==4, 'internal pages not four distinct roles'
                assert b in red[a] and all(y in red[a]&red[b] for y in pages)
                assert next(lines,None) is None and expected['internal_book']
                result={'mask':mask,'internal_book':True,'trace_sha256':digest,'complete':True}
            else:
                observed=[]
                while first[0]=='R':
                    assert len(first)==2;observed.append(int(first[1]))
                    first=next(lines).split()
                assert observed==masks and expected['rows']==m, 'incomplete/wrong one-row list'
                assert expected['automorphism_count']==aut_count and not expected['internal_book']
                initial=[not_ten if len(red[role])>=2 else all_rows for role in range(6)]
                nodes=[0]*7;branches=[0]*7;empty=[0]*7
                pending=[first]
                def next_record():
                    if pending:return pending.pop()
                    line=next(lines,None)
                    assert line is not None,'truncated proof tree'
                    return line.split()
                def check_node(context):
                    depth=len(context);nodes[depth]+=1
                    tokens=next_record()
                    assert tokens[0]=='D','complete candidate or malformed tree needs further research'
                    values=list(map(int,tokens[1:]));assert values[0]==depth<6
                    emitted=tuple(zip(values[1:2*depth+1:2],values[2:2*depth+1:2]))
                    assert emitted==tuple((r,masks[i]) for r,i in context),'missing/reordered branch'
                    role=values[2*depth+1];count=values[2*depth+2];candidate=values[2*depth+3:]
                    assert 0<=role<6 and role not in {r for r,_ in context}
                    assert len(candidate)==count
                    allowed=domain(context,role,J,initial[role])
                    assigned=dict(context)
                    for _,i in context:allowed&=all_rows^(1<<i)
                    for a,b in inequalities:
                        if a==role and b in assigned:allowed&=(1<<assigned[b])-1
                        if b==role and a in assigned:allowed=allowed>>(assigned[a]+1)<<(assigned[a]+1)
                    ids=list(members(allowed))
                    assert candidate==[masks[i] for i in ids],'incomplete/wrong row domain'
                    if not ids:empty[depth]+=1
                    else:
                        branches[depth]+=len(ids)
                        for i in ids:check_node(context+((role,i),))
                check_node(())
                assert next(lines,None) is None,'extra proof tree records'
                assert nodes==expected['records_by_depth']
                assert branches==expected['branches_by_depth']
                assert empty==expected['empty_domains_by_depth']
                result={'mask':mask,'internal_book':False,'nodes':sum(nodes),
                        'records_by_depth':nodes,'branches_by_depth':branches,
                        'empty_domains_by_depth':empty,'trace_sha256':digest,'complete':True}
        progress['verified'][str(mask)]=result
        progress['complete']=len(progress['verified'])==156
        temporary = progress_path.with_name(progress_path.name+'.tmp')
        temporary.write_text(json.dumps(progress,indent=2)+'\n')
        temporary.replace(progress_path)
        print(json.dumps({'verified_mask':mask,'verified_types':len(progress['verified']),
                          'total_types':156,'nodes':result.get('nodes',0),
                          'chunk_seconds':time.monotonic()-started}),flush=True)
    progress['complete']=len(progress['verified'])==156
    temporary = progress_path.with_name(progress_path.name+'.tmp')
    temporary.write_text(json.dumps(progress,indent=2)+'\n')
    temporary.replace(progress_path)
    return {'complete':progress['complete'],'verified_types':len(progress['verified']),
            'total_types':156,'all_labeled_internal_graphs':32768,
            'chunk_seconds':time.monotonic()-started}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('trace_directory',help='scratch directory generated by check_core_extension.py')
    parser.add_argument('--progress',help='optional local progress path; defaults inside scratch')
    parser.add_argument('--max-seconds',type=float,help='optional budget checked between complete types')
    args=parser.parse_args()
    progress = args.progress or str(Path(args.trace_directory)/'independent-progress.json')
    print(json.dumps(compute(args.trace_directory,progress,args.max_seconds),indent=2,sort_keys=True))
