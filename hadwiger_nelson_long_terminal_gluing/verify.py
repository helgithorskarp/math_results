"""Solver-free verification in a separately implemented quadratic tower.

No producer or inherited field-arithmetic module is imported. The universal
placement theorem is the analytic argument in README.md; fixtures are controls.
"""
from pathlib import Path
from itertools import combinations,product
from hashlib import sha256
import argparse,json,time

HERE=Path(__file__).resolve().parent
INPUT=HERE.parent/'hadwiger_nelson_nonmono159_214_lowden2'
ZERO=(0,0,0,0)


def qmul(x,y):return (x[0]*y[0]+3*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def plus(x,y):return tuple(a+b for a,b in zip(x,y,strict=True))
def minus(x,y):return tuple(a-b for a,b in zip(x,y,strict=True))
def times(x,y):
    # (a+b*sqrt11)(c+d*sqrt11), where a,b,c,d are in Q(sqrt3).
    ac,bd,ad,bc=qmul(x[:2],y[:2]),qmul(x[2:],y[2:]),qmul(x[:2],y[2:]),qmul(x[2:],y[:2])
    return (ac[0]+11*bd[0],ac[1]+11*bd[1],ad[0]+bc[0],ad[1]+bc[1])
def norm(point):return plus(times(point[0],point[0]),times(point[1],point[1]))
def distance(a,b):return norm((minus(a[0],b[0]),minus(a[1],b[1])))


def decode(rows):
    out=[]
    for row in rows:
        assert len(row)==16 and all(type(x) is int for x in row)
        for off in (0,8):assert all(row[off+i]==0 for i in (2,3,6,7))
        out.append(tuple(tuple(row[off+i] for i in (0,1,4,5)) for off in (0,8)))
    return out


def proper(row,n,edges):
    assert len(row)==n and set(row)<=set('0123')
    assert all(row[a]!=row[b] for a,b in edges)


def all_extensions(record,n,edges):
    terminals=record['terminals'];rows=record['extensions']
    required=['001','010','011','012'] if len(terminals)==3 else ['01']
    assert [r['pattern'] for r in rows]==required
    for r in rows:
        proper(r['colours'],n,edges)
        assert ''.join(r['colours'][v] for v in terminals)==r['pattern']
    checked=0
    for target in product('0123',repeat=len(terminals)):
        if len(set(target))==1:continue
        order=list(dict.fromkeys(target));pattern=''.join(str(order.index(c)) for c in target)
        source=next(r['colours'] for r in rows if r['pattern']==pattern)
        palette=order+sorted(set('0123')-set(order))
        image=''.join(palette[int(c)] for c in source)
        assert tuple(image[v] for v in terminals)==target
        proper(image,n,edges);checked+=1
    return checked


def colour_interface(sets,unit_edges,selected):
    assert 1<=len(sets)<=3 and len(selected)==len(sets)
    vertices=sorted(set().union(*sets));u={tuple(sorted(e)) for e in unit_edges}
    assert all(len(s)>=2 for s in sets)
    neighbours={v:set() for v in vertices}
    for a,b in u:
        assert a!=b and a in neighbours and b in neighbours
        neighbours[a].add(b);neighbours[b].add(a)
    # The separation lemma implies these incidence bounds, including overlaps.
    for v in vertices:
        for s in sets:
            assert len(neighbours[v]&s)<=int(v not in s)
    auxiliary=u.copy()
    for s,pair in zip(sets,selected,strict=True):
        assert len(set(pair))==2 and set(pair)<=s
        auxiliary.add(tuple(sorted(pair)))
    adj={v:set() for v in vertices}
    for a,b in auxiliary:adj[a].add(b);adj[b].add(a)
    assert all(len(adj[v])<=len(sets) for v in vertices)
    colours={}
    for v in vertices:
        forbidden={colours[x] for x in adj[v] if x in colours}
        colours[v]=next(c for c in range(4) if c not in forbidden)
    assert all(colours[a]!=colours[b] for a,b in auxiliary)
    assert all(len({colours[v] for v in s})>=2 for s in sets)
    return max(map(len,adj.values()),default=0)


def geometric_controls():
    def p(x,y=0,ys=0):return ((x,0,0,0),(y,ys,0,0))
    # Coordinates are divided by12. Within-set distances are greater than2.
    fixtures=[
      ('shared_terminal',[[p(0),p(36),p(0,36)],[p(0),p(-36),p(0,-36)],[p(12),p(48),p(12,36)]]),
      ('triangular_prism',[[p(0),p(36)],[p(12),p(48)],[p(6,ys=6),p(42,ys=6)]]),
      ('three_identical_sets',[[p(0),p(36),p(0,36)]]*3),
      ('two_identical_pairs',[[p(0),p(36)]]*2),
      ('one_pair',[[p(0),p(36)]])]
    reports=[]
    for name,blocks in fixtures:
        points=sorted(set().union(*map(set,blocks)));index={v:i for i,v in enumerate(points)}
        for block in blocks:
            for a,b in combinations(block,2):
                q=distance(a,b);assert q[1:]==(0,0,0) and q[0]>4*144
        sets=[{index[p] for p in block} for block in blocks]
        edges=[(i,j) for i,j in combinations(range(len(points)),2) if distance(points[i],points[j])==(144,0,0,0)]
        choices=[list(combinations(sorted(s),2)) for s in sets];degrees=[]
        for pairs in product(*choices):degrees.append(colour_interface(sets,edges,pairs))
        reports.append({'fixture':name,'distinct_terminals':len(points),'unit_edges':len(edges),
                        'selected_pair_cases':len(degrees),'maximum_auxiliary_degree':max(degrees)})
    # At separation exactly2 the key one-neighbour fact fails.
    midpoint=p(0);ends=[p(-12),p(12)]
    assert distance(*ends)==(576,0,0,0)
    assert all(distance(midpoint,e)==(144,0,0,0) for e in ends)
    return reports


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);args=ap.parse_args();start=time.perf_counter()
    expected=json.loads((HERE/'expected.json').read_text());assert expected==json.loads((args.work/'result.json').read_text())
    raw=(HERE/'certificate.json').read_bytes();assert raw==(args.work/'certificate.json').read_bytes()
    assert sha256(raw).hexdigest()==expected['certificate_sha256'] and len(raw)==1100
    cert=json.loads(raw);assert set(cert)=={'159','214'};counts=[];edge_lists={}
    for r in expected['gadgets']:
        n=r['vertices'];key=str(n);path=INPUT/f'points{key}.tsv';text=path.read_text().splitlines()
        assert text[0]=='# scale 12' and sha256(path.read_bytes()).hexdigest()==r['coordinate_sha256']
        rows=[list(map(int,line.split())) for line in text[1:] if line.strip() and not line.startswith('#')]
        points=decode(rows);assert len(points)==len(set(points))==n
        graph_raw=(args.work/f'graph{key}.json').read_bytes();assert sha256(graph_raw).hexdigest()==r['graph_sha256']
        g=json.loads(graph_raw);assert g['denominator']==12
        assert [(list(a),list(b)) for a,b in points]==[(list(a),list(b)) for a,b in decode([x+y for x,y in g['points']])]
        distances={(i,j):distance(points[i],points[j]) for i,j in combinations(range(n),2)}
        edges=[list(e) for e,q in distances.items() if q==(144,0,0,0)]
        assert edges==g['edges'] and len(edges)==r['edges'];edge_lists[key]=edges
        ports=[141,142,144] if n==159 else [186,187]
        assert ports==g['terminals']==r['terminals']==cert[key]['terminals']
        sq=7 if n==159 else 9
        assert all(distances[i,j]==(144*sq,0,0,0) for i,j in combinations(ports,2))
        if n==159:
            assert [points[i] for i in ports]==[((6,0,0,0),(0,10,0,0)),((12,0,0,0),(0,-8,0,0)),((-18,0,0,0),(0,-2,0,0))]
            radial=[i for i,p in enumerate(points) if norm(p)==(336,0,0,0)]
            assert [list(t) for t in combinations(radial,3) if all(distances[i,j]==(1008,0,0,0) for i,j in combinations(t,2))]==[ports]
        else:
            assert [points[i] for i in ports]==[((18,0,0,0),ZERO),((-18,0,0,0),ZERO)]
        count=all_extensions(cert[key],n,edges);assert count==(60 if n==159 else 12)
        counts.append({'vertices':n,'edges':len(edges),'pair_norm_checks':len(distances),
          'terminal_assignments_extended':count,'expanded_colour_edge_checks':count*len(edges)})
    controls=geometric_controls();rejected=0
    bad=cert['159']['extensions'][0]['colours'];a,b=edge_lists['159'][0];bad=bad[:a]+bad[b]+bad[a+1:]
    try:proper(bad,159,edge_lists['159'])
    except AssertionError:rejected+=1
    altered=json.loads(json.dumps(cert['159']));altered['extensions']=altered['extensions'][:-1]
    try:all_extensions(altered,159,edge_lists['159'])
    except AssertionError:rejected+=1
    # A near-miss incidence violating the geometric separation premise is rejected.
    try:colour_interface([{0,1},{2,3}],[(0,2),(0,3)],[(0,1),(2,3)])
    except AssertionError:rejected+=1
    assert rejected==3
    result={'status':expected['status'],'arithmetic':'Independent Q(sqrt3)(sqrt11) tower; no producer imports',
      'graphs_compared_entrywise':2,'full_pair_norm_checks':sum(c['pair_norm_checks'] for c in counts),
      'canonical_positive_patterns_checked':5,'canonical_witness_edge_checks':3561,
      'all_nonmonochromatic_terminal_assignments_checked':sum(c['terminal_assignments_extended'] for c in counts),
      'expanded_colour_edge_checks':sum(c['expanded_colour_edge_checks'] for c in counts),'gadgets':counts,
      'geometric_auxiliary_controls':controls,'auxiliary_selected_pair_cases_checked':sum(c['selected_pair_cases'] for c in controls),
      'strict_distance_greater_than2_boundary_checked':True,'invalid_witnesses_or_premises_rejected':rejected,
      'universal_placement_argument':'Analytic separation and degree proof in README; finite fixtures are controls only',
      'negative_solver_proof_required':False,'native_solver_calls':0,'target_found':False,'seconds':time.perf_counter()-start}
    (args.work/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
