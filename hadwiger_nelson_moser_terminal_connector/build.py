"""Complete labelled placement enumeration and a conservative constraint graph."""
import argparse, hashlib, json, time
from itertools import combinations
from pathlib import Path
from intervals import I,S,BITS,Q,add,sub,scale,turn,norm,mul,boxdata
HERE=Path(__file__).resolve().parent

def digest(x):
    return hashlib.sha256(json.dumps(x,separators=(',',':'),sort_keys=True).encode()).hexdigest()

def enumerate_boxes():
    one=(Q(1),Q(0)); v=(Q(1,2),Q(3).sqrt()/Q(2)); rho=(Q(5,6),Q(11).sqrt()/Q(6))
    m=[(Q(0),Q(0)),one,v,add(one,v),mul(rho,one),mul(rho,v),mul(rho,add(one,v))]
    omega=(Q(1,2),Q(3).sqrt()/Q(2))
    points=list(m); labels=[['M',i] for i in range(7)]; triangles=[]; branch=[]
    for i,j in combinations(range(7),2):
        d=sub(m[j],m[i]); d2=norm(d)
        assert d2.lo>0 and d2.hi<4*S
        off=scale(turn(d),(Q(4)/d2-Q(1)).sqrt()/Q(2))
        mid=scale(add(m[i],m[j]),Q(1,2))
        for sign in (-1,1):
            a=add(mid,scale(off,Q(sign)))
            for k in range(7):
                delta=sub(m[k],a); r=norm(delta)
                disc=Q(16)*r-r.square()-Q(36)
                label=[i,j,sign,k]
                if disc.hi<0:
                    branch.append([label,'absent']);continue
                assert disc.lo>0 and r.lo>0, ('unresolved circle branch',label,disc.data())
                branch.append([label,'two'])
                foot=add(a,scale(delta,(r+Q(6))/(Q(2)*r)))
                off2=scale(turn(delta),disc.sqrt()/(Q(2)*r))
                for side in (-1,1):
                    b=add(foot,scale(off2,Q(side)))
                    for orientation in (-1,1):
                        rotation=(omega[0],omega[1]*Q(orientation))
                        c=add(a,mul(sub(b,a),rotation))
                        ids=list(range(len(points),len(points)+3));triangles.append(ids)
                        points.extend((a,b,c))
                        labels.extend([label+[side,orientation,t] for t in range(3)])
    return points,labels,triangles,branch

def constraints(points,triangles):
    # An exact equality must give intersecting certified boxes. Merge every such
    # pair and its transitive closure; no claim of exact equality is needed.
    parent=list(range(len(points)))
    def root(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]];i=parent[i]
        return i
    for i,j in combinations(range(len(points)),2):
        if all(points[i][c].meets(points[j][c]) for c in (0,1)):
            a,b=root(i),root(j)
            if a!=b:parent[max(a,b)]=min(a,b)
    roots=sorted({root(i) for i in range(len(points))});ren={r:i for i,r in enumerate(roots)}
    groups=[ren[root(i)] for i in range(len(points))]
    hulls=[]
    for g in range(len(roots)):
        members=[p for p,h in zip(points,groups) if h==g]
        hulls.append(tuple(I(min(p[c].lo for p in members),max(p[c].hi for p in members)) for c in (0,1)))
    for p in hulls:
        assert sum((p[c].hi-p[c].lo)**2 for c in (0,1))<S*S
    edges=[]
    for i,j in combinations(range(len(hulls)),2):
        d=norm(sub(hulls[i],hulls[j]))
        if d.lo<=S<=d.hi:edges.append([i,j])
    triples=sorted({tuple(sorted(groups[i] for i in t)) for t in triangles})
    assert all(len(set(t))==3 for t in triples)
    return groups,hulls,edges,[list(t) for t in triples]

def check_colours(data,colours):
    n=len(data['hulls'])
    assert len(colours)==n and all(type(c) is int and 0<=c<4 for c in colours)
    assert all(colours[i]!=colours[j] for i,j in data['edges'])
    assert all(len({colours[i] for i in t})>1 for t in data['triples'])

def build():
    points,labels,triangles,branches=enumerate_boxes()
    groups,hulls,edges,triples=constraints(points,triangles)
    data={'bits':BITS,'points':[boxdata(p) for p in points],'labels':labels,'labelled_triangles':triangles,
          'circle_branches':branches,'groups':groups,'hulls':[boxdata(p) for p in hulls],
          'edges':edges,'triples':triples}
    stats={'bits':BITS,'spindle_pairs':21,'labelled_double_contact_points':42,
           'second_anchor_cases':len(branches),'absent_cases':sum(b[1]=='absent' for b in branches),
           'two_intersection_cases':sum(b[1]=='two' for b in branches),
           'labelled_triangles':len(triangles),'labelled_points':len(points),'enclosure_clusters':len(hulls),
           'conservative_edges':len(edges),'distinct_cluster_triples':len(triples),'data_sha256':digest(data)}
    return data,stats

def main():
    assert __debug__,'run without -O'
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    data,stats=build(); cert=json.loads((HERE/'certificate.json').read_text())
    check_colours(data,cert['colours']);assert digest(cert['colours'])==cert['colours_sha256']
    assert cert['labelled_colours']==''.join(str(cert['colours'][g]) for g in data['groups'])
    assert stats==json.loads((HERE/'expected.json').read_text())
    (out/'build.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
    (out/'summary.json').write_text(json.dumps(stats,indent=2)+'\n')
    print(json.dumps({'status':'PASS','seconds':time.monotonic()-start,**stats},sort_keys=True))
if __name__=='__main__':main()
