"""No producer imports: exact classification, Gram obstruction, and all-list audit."""
import argparse,json,hashlib,time
from pathlib import Path
from itertools import product,combinations
from collections import Counter
from fractions import Fraction as Q
HERE=Path(__file__).resolve().parent

def need(test,message):
    if not test:raise ValueError(message)

def graphs():
    return {'K33':[(i,j) for i in range(3) for j in range(3,6)],
            'prism':[(0,1),(0,2),(1,2),(3,4),(3,5),(4,5),(0,3),(1,4),(2,5)]}

def audit_lists(cert):
    need(set(cert)==set(graphs()),'wrong graph names');all_profiles=edges_checked=vertices_checked=0
    used={name:set() for name in graphs()}
    for name,edges in graphs().items():
        for f in product(range(4),repeat=6):
            # Derive the first-appearance permutation afresh, then complete its
            # inverse to all four palette colours, including unused colours.
            order=[]
            for c in f:
                if c not in order:order.append(c)
            key=''.join(str(order.index(c)) for c in f)
            order.extend(c for c in range(4) if c not in order)
            need(key in cert[name],'missing list witness');row=cert[name][key]
            need(len(row)==6 and all(c in '0123' for c in row),'malformed witness')
            cs=[order[int(c)] for c in row]
            need(all(cs[i]!=f[i] for i in range(6)),'forbidden colour used')
            need(all(cs[i]!=cs[j] for i,j in edges),'monochromatic edge')
            used[name].add(key);all_profiles+=1;vertices_checked+=6;edges_checked+=len(edges)
        need(set(cert[name])==used[name],'unused or duplicate canonical domain')
    return {'all_labelled_profiles':all_profiles,'canonical_rows':sum(map(len,used.values())),
            'witness_vertex_checks':vertices_checked,'witness_edge_checks':edges_checked}

def classify():
    counts=Counter();masks_checked=0
    for n in (4,6):
        pairs=list(combinations(range(n),2))
        for mask in range(1<<len(pairs)):
            masks_checked+=1;a=[set() for _ in range(n)]
            for k,(i,j) in enumerate(pairs):
                if mask>>k&1:a[i].add(j);a[j].add(i)
            if any(len(x)!=3 for x in a):continue
            seen={0};todo=[0]
            for u in todo:
                for v in a[u]-seen:seen.add(v);todo.append(v)
            need(len(seen)==n,'unexpected disconnected cubic graph')
            if n==4:counts['K4']+=1;continue
            # Complement of a cubic graph on six vertices is 2-regular.
            comp=[set(range(n))-{i}-a[i] for i in range(n)]
            parts=[];left=set(range(n))
            while left:
                seen={min(left)};todo=list(seen)
                for u in todo:
                    for v in comp[u]-seen:seen.add(v);todo.append(v)
                parts.append(len(seen));left-=seen
            if sorted(parts)==[3,3]:
                need(not any(all(j in a[i] for i,j in combinations(t,2)) for t in combinations(range(n),3)),'K33 has triangle')
                counts['K33']+=1
            elif parts==[6]:
                triangles=[set(t) for t in combinations(range(n),3) if all(j in a[i] for i,j in combinations(t,2))]
                need(len(triangles)==2 and triangles[0].isdisjoint(triangles[1]),'not prism')
                need(all(len(a[i]-t)==1 for t in triangles for i in t),'not prism matching')
                counts['prism']+=1
            else:raise ValueError('unexpected complement cycle type')
    need(dict(counts)=={'K4':1,'prism':60,'K33':10},'classification count mismatch')
    return {'simple_graph_masks':masks_checked,'labelled_cubic_graphs':dict(sorted(counts.items()))}

def gram_obstruction():
    hist=Counter();pairs=list(combinations(range(4),2))
    for k in range(4):
        for chosen in combinations(pairs,k):
            def d(i,j):return 0 if i==j else 7 if tuple(sorted((i,j))) in chosen else 1
            g=[[Q(d(0,i)+d(0,j)-d(i,j),2) for j in (1,2,3)] for i in (1,2,3)]
            det=g[0][0]*(g[1][1]*g[2][2]-g[1][2]*g[2][1])-g[0][1]*(g[1][0]*g[2][2]-g[1][2]*g[2][0])+g[0][2]*(g[1][0]*g[2][1]-g[1][1]*g[2][0])
            need(det!=0,'planar K4 distance pattern not excluded');hist[str(det)]+=1
    return {'K4_distance_patterns':sum(hist.values()),'Gram_determinants':dict(sorted(hist.items()))}

def controls(cert):
    changed=json.loads(json.dumps(cert));changed['K33']['000000']='000000'
    try:audit_lists(changed)
    except ValueError:pass
    else:raise ValueError('accepted invalid colouring')
    changed=json.loads(json.dumps(cert));del changed['prism']['012301']
    try:audit_lists(changed)
    except ValueError:pass
    else:raise ValueError('accepted missing profile')
    return 2

def main():
    p=argparse.ArgumentParser();p.add_argument('--work',required=True);a=p.parse_args();start=time.monotonic()
    raw=(HERE/'certificate.json').read_bytes();cert=json.loads(raw)
    result={**audit_lists(cert),**classify(),**gram_obstruction(),'rejection_controls':controls(cert),
        'certificate_sha256':hashlib.sha256(raw).hexdigest(),'native_solver_calls':0,'status':'PASS'}
    expected=json.loads((HERE/'expected.json').read_text()) if (HERE/'expected.json').exists() else None
    if expected is not None:need(result==expected,'expected result mismatch')
    work=Path(a.work);work.mkdir(parents=True,exist_ok=True)
    (work/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({**result,'seconds':time.monotonic()-start},sort_keys=True))
if __name__=='__main__':main()
