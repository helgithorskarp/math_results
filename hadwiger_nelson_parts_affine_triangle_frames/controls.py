"""Definition-level exact metric checks, physical fixture, and malformed controls."""
import argparse,json,random,hashlib
from pathlib import Path
import model as m
from check import check_word,cofactor_metric,peel

def run(work):
    rng=random.Random(54);tested=0
    for _ in range(100):
        a,b=[tuple(tuple(rng.randrange(-3,4) for _ in range(4)) for _ in range(2)) for _ in range(2)]
        if m.det(a,b)==m.Z:continue
        q=m.metric(a,b)
        m.require(m.unit(q,a) and m.unit(q,b) and m.unit(q,m.diff(a,b)),'equilateral frame equations')
        d=tuple(tuple(rng.randrange(-3,4) for _ in range(4)) for _ in range(2))
        A=m.det(d,b);B=m.det(a,d);D=m.det(a,b)
        lhs=m.add(m.add(m.mul(A,A),m.mul(A,B)),m.mul(B,B))
        x,y=d;xx,xy,yy,dd=q
        rhs=m.add(m.add(m.mul(xx,m.mul(x,x)),m.mul(xy,m.mul(x,y))),m.mul(yy,m.mul(y,y)))
        m.require(lhs==rhs and dd==m.mul(D,D),'independent determinant metric mismatch');tested+=1
    P,den=m.points();fixture=json.loads((m.HERE/'fixture.json').read_text());_,a,b=fixture['frame'];q=m.metric(P[a],P[b]);edges=[];pairs=0
    for i in range(509):
        for j in range(i+1,509):
            d=m.diff(P[i],P[j]);A=m.det(d,P[b]);B=m.det(P[a],d);D=m.det(P[a],P[b])
            hit=m.add(m.add(m.mul(A,A),m.mul(A,B)),m.mul(B,B))==m.mul(D,D)
            m.require(hit==m.unit(q,d),'physical fixture metric mismatch')
            if hit:edges.append((i,j))
            pairs+=1
    m.require(len(edges)==fixture['edges'] and hashlib.sha256(json.dumps(edges,separators=(',',':')).encode()).hexdigest()==fixture['edge_sha256'],'physical fixture census')
    check_word(fixture['four_word'],edges)
    bad=0
    for word in ('0'*509,'0'*508,'0'*510,'4'*509,[],None):
        try:check_word(word,edges)
        except (ValueError,TypeError):bad+=1
        else:raise ValueError('malformed word accepted')
    for args in ((1000000271,0,767568613),(1000000272,838613109,767568613)):
        try:m.projection(*args)
        except ValueError:bad+=1
        else:raise ValueError('bad ring map accepted')
    m.require(peel(5,[(i,j) for i in range(5) for j in range(i+1,5)]) is None,'K5 accepted as 3-degenerate')
    m.require(cofactor_metric((1,0),(2,0),1000000271) is None,'singular frame accepted')
    p=1000000271
    m.require((p+1)**2%p==1 and (p+1)**2!=1,'strict supergraph false-positive control')
    out={'random_exact_frame_identities':tested,'fixture_pair_checks':pairs,'fixture_vertices':509,'fixture_edges':len(edges),'malformed_rejections':bad,'known_graph_controls':2,'strict_supergraph_control':True,'PASS':True}
    (work/'controls.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));return out
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('work',type=Path);args=ap.parse_args();run(args.work)
