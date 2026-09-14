"""Replay the entire modular metric inventory, independently solving each frame.

NumPy uses signed 64-bit exact integers. All factors are <p; dot products have
three terms, bounded by 3(p-1)^2 < 2^63. No floating arithmetic is used.
"""
import argparse, base64, hashlib, json, time
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import numpy as np
import model as m

def cofactor_metric(a,b,p):
    # Independently solve q(a)=q(b)=q(a-b)=1, by Cramer's rule.
    rows=[(x*x%p,x*y%p,y*y%p) for x,y in (a,b,((a[0]-b[0])%p,(a[1]-b[1])%p))]
    def det(r):
        a,b,c=r
        return (a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0]))%p
    d=det(rows)
    if not d:return None
    inv=pow(d,-1,p)
    return tuple(det([tuple(1 if j==i else row[j] for j in range(3)) for row in rows])*inv%p for i in range(3))

def peel(n,edges):
    adj=[[] for _ in range(n)]
    for i,j in edges:adj[i].append(j);adj[j].append(i)
    deg=[len(a) for a in adj];stack=[i for i,d in enumerate(deg) if d<=3];order=[]
    while stack:
        v=stack.pop();order.append(v);deg[v]=-1
        for u in adj[v]:
            if deg[u]>=0:
                deg[u]-=1
                if deg[u]==3:stack.append(u)
    if len(order)!=n:return None
    word=[-1]*n
    for v in reversed(order):
        used={word[u] for u in adj[v]};word[v]=next(c for c in range(4) if c not in used)
    m.require(all(word[i]!=word[j] for i,j in edges),'invalid reverse-peel word')
    return word

def check_word(word,edges):
    m.require(isinstance(word,str) and len(word)==509 and set(word)<=set('0123'),'malformed positive word')
    m.require(all(word[i]!=word[j] for i,j in edges),'invalid positive word')

def check_original_deletions(edges):
    path=m.HERE.parent/'hadwiger_nelson_parts509_criticality/certificate.json'
    m.require(hashlib.sha256(path.read_bytes()).hexdigest()=='d354f9629c41639168b80fc1aa6feb6e4187dd37dee7efcb83b4ef6ebe68d16c','changed deletion certificate')
    packed=base64.b64decode(json.loads(path.read_text())['deletion_colorings_base64'],validate=True)
    m.require(len(packed)==509*127,'deletion certificate length')
    for v in range(509):
        block=packed[127*v:127*(v+1)]
        def colour(i):
            k=i-(i>v);return (block[k//4]>>(2*(k%4)))&3
        m.require(all(colour(i)!=colour(j) for i,j in edges if i!=v and j!=v),'invalid original deletion word')
    return 509

def run(work,certificate=None):
    start=time.time();info=json.loads((work/'input_summary.json').read_text());p=info['p'];r5=info['sqrt5'];r33=info['sqrt33']
    proj=m.projection(p,r5,r33);P,den=m.points()
    # Read source independently, directly evaluating x and y/sqrt3 in F_p.
    raw=json.loads(m.SOURCE.read_text())['coordinates']
    def frac(s):
        f=F(s);return f.numerator*pow(f.denominator,-1,p)%p
    rawP=[]
    for i in range(509):
        x,y=raw[str(i)]
        X=(frac(x[0])+frac(x[2])*r5+frac(x[5])*r33+frac(x[7])*r5*r33)*den%p
        Y=(frac(y[1])+frac(y[3])*r5+(frac(y[4])+frac(y[6])*r5)*r33*pow(3,-1,p))*den%p
        rawP.append((X,Y))
    m.require(rawP==[(proj(x),proj(y)) for x,y in P],'source projections disagree')
    # Recover complete membership of each exact difference group from labels.
    exact={}
    for i,j in combinations(range(509),2):
        d=m.diff(P[j],P[i]);d=min(d,(m.neg(d[0]),m.neg(d[1])))
        exact.setdefault(d,[]).append((i,j))
    groups=sorted(exact.items());edges_by_group=[];rows=[]
    for d,edges in groups:
        i,j=edges[0];x,y=((rawP[j][k]-rawP[i][k])%p for k in range(2))
        rows.append((x*x%p,x*y%p,y*y%p));edges_by_group.append(edges)
        for a,b in edges:
            u,v=((rawP[b][k]-rawP[a][k])%p for k in range(2))
            m.require((u*u%p,u*v%p,v*v%p)==rows[-1],'wrong group membership')
    R=np.array(rows,dtype=np.int64)
    m.require(3*(p-1)**2<2**63,'int64 bound')
    metrics={};singular=[]
    for i,j in combinations(range(1,509),2):
        q=cofactor_metric(rawP[i],rawP[j],p)
        if q is None:
            m.require(m.det(P[i],P[j])==m.Z,'modular singular but physically valid frame')
            singular.append((i,j))
        else:metrics.setdefault(q,[]).append((i,j))
    native_singular=[tuple(map(int,l.split())) for l in (work/'scan_singular.txt').read_text().splitlines()]
    m.require(singular==native_singular,'singular census mismatch')
    cert=json.loads((certificate or m.HERE/'certificate.json').read_text())
    histogram=Counter();residual=[];checked=0;original_frames=0;max_nonoriginal=0;used=set();deletion_rows=0
    digest=hashlib.sha256()
    lines=(work/'scan_metrics.txt').read_text().splitlines()
    m.require(len(lines)==len(metrics),'incomplete metric output')
    for mid,((q,frames),line) in enumerate(zip(sorted(metrics.items()),lines)):
        v=list(map(int,line.split()));m.require(v[:4]==[mid,*q],'metric order mismatch')
        count,was_peel,nf=v[4:7];m.require(nf==len(frames),'frame multiplicity mismatch')
        m.require(v[7:7+2*nf]==[t for f in frames for t in f],'frame assignment mismatch')
        off=7+2*nf;ng=v[off];native_ids=v[off+1:];m.require(len(native_ids)==ng,'bad edge group output')
        ids=np.flatnonzero((R@np.array(q,dtype=np.int64))%p==1).tolist()
        m.require(ids==native_ids,'full entrywise contact comparison failed')
        edges=[e for k in ids for e in edges_by_group[k]];m.require(len(edges)==count,'edge count mismatch')
        word=peel(509,edges);m.require((word is not None)==bool(was_peel),'peeling mismatch')
        digest.update((' '.join(map(str,[mid,*ids]))+'\n').encode())
        histogram[count]+=1
        if word is None:
            if str(mid) in cert:
                check_word(cert[str(mid)],edges);used.add(str(mid));max_nonoriginal=max(max_nonoriginal,count)
                residual.append({'mod_metric':mid,'edges':count,'frames':len(frames),'positive_word':True})
            else:
                for a,b in frames:
                    qq=m.metric(P[a],P[b]);m.require(m.is_original(qq,den),'uncovered nonoriginal metric')
                    original_frames+=1
                m.require(all(m.add(m.mul(m.diff(P[i],P[j])[0],m.diff(P[i],P[j])[0]),m.scale(m.mul(m.diff(P[i],P[j])[1],m.diff(P[i],P[j])[1]),3))==(den*den,0,0,0) for i,j in edges),'original projected graph is not exact')
                deletion_rows+=check_original_deletions(edges)
                residual.append({'mod_metric':mid,'edges':count,'frames':frames,'exact_original_metric':True})
        else:max_nonoriginal=max(max_nonoriginal,count)
        checked+=1
    m.require(used==set(cert),'unused or missing certificate entries')
    out={'frames_total':508*507//2,'noncollinear_frames':sum(map(len,metrics.values())),'collinear_frames':len(singular),'mod_metrics':len(metrics),'three_degenerate_metrics':len(metrics)-len(residual),'positive_exception_words':len(used),'original_deletion_rows_checked':deletion_rows,'residual':residual,'original_frames':original_frames,'max_nonoriginal_supergraph_edges':max_nonoriginal,'edge_histogram':dict(sorted(histogram.items())),'contact_stream_sha256':digest.hexdigest(),'checked':checked,'seconds':time.time()-start,'record_improvement':False}
    (work/'verified.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
    return out
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('work',type=Path);ap.add_argument('--certificate',type=Path);args=ap.parse_args();run(args.work,args.certificate)
