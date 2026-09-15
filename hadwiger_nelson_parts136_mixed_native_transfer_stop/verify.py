#!/usr/bin/env python3
"""Exact definition-level check of one fixed Parts136/A159/B214 union."""
from pathlib import Path
from itertools import combinations,product
from math import gcd
import argparse,hashlib,json
BASE=Path(__file__).resolve().parent
RAD=(1,3,5,15,11,33,55,165)
HASHES={'parts509.tsv':'f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50','points159.tsv':'4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02','points214.tsv':'97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f'}

def need(t,m):
    if not t:raise ValueError(m)
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def read(name,count,scale):
    data=(BASE/name).read_bytes();need(hashlib.sha256(data).hexdigest()==HASHES[name],'input hash '+name)
    rows=[tuple(scale*int(a) for a in l.split()) for l in data.decode().splitlines() if l and not l.startswith('#')]
    need(len(rows)==len(set(rows))==count and all(len(v)==16 for v in rows),'input dimensions')
    return rows

def norm(d):
    acc={}
    for axis in [d[:8],d[8:]]:
        terms=[(rad,a) for rad,a in zip(RAD,axis) if a]
        for i,(rad,a) in enumerate(terms):
            acc[1]=acc.get(1,0)+rad*a*a
            for s,b in terms[i+1:]:
                common=gcd(rad,s);r=rad*s//(common*common)
                acc[r]=acc.get(r,0)+2*common*a*b
    return tuple(acc.get(r,0) for r in RAD)

def graph():
    P=read('parts509.tsv',509,1);A=read('points159.tsv',159,8);B=read('points214.tsv',214,8)
    hp=[0]+list(range(374,509));H=[P[i] for i in hp]
    need(set(H)&set(A)=={P[0]} and not(set(H)&set(B)) and not(set(A)&set(B)),'exact input intersections')
    points=H+[v for v in A if v!=P[0]]+B
    need(len(points)==len(set(points))==508,'collision-merged cap')
    pos={v:i for i,v in enumerate(points)};am=[pos[v] for v in A];bm=[pos[v] for v in B];sa=set(am);sb=set(bm)
    edges=[];ds=hashlib.sha256()
    for i,j in combinations(range(508),2):
        n=norm(tuple(x-y for x,y in zip(points[i],points[j])))
        need(any(n),'no hidden collision');ds.update((','.join(map(str,n))+'\n').encode())
        if n==(96*96,0,0,0,0,0,0,0):edges.append([i,j])
    he=[e for e in edges if e[1]<136];ae=[e for e in edges if set(e)<=sa];be=[e for e in edges if set(e)<=sb]
    need([len(he),len(ae),len(be)]==[564,646,977],'complete constituent graphs')
    need({tuple(e) for e in edges}=={tuple(e) for e in he+ae+be},'no additional physical contacts')
    hn=[e for e in edges if e[0]<136<=e[1]];nn=[e for e in edges if e[0]>=136]
    actual=sorted({i for i,j in hn});need(actual==[0],'exact receiving interface')
    sigma=lambda v:tuple(-x if i%8&2 else x for i,x in enumerate(v));switch=set(P)|{sigma(v) for v in P}
    summary={'points':508,'edges':len(edges),'new_points':372,'host_edges':len(he),'A_edges':len(ae),'B_edges':len(be),'old_new_edges':len(hn),'new_new_edges':len(nn),'A_B_contacts':0,'actual_host_boundary_parent_labels':[hp[i] for i in actual],'boundary_outside_original_B':[],'outside_parent':len(set(points)-set(P)),'switching_host_points':len(switch),'outside_switching_host':len(set(points)-switch),'point_hash':digest(points),'edge_hash':digest(edges),'distance_hash':ds.hexdigest(),'all_pairs':508*507//2}
    return summary,edges,am,bm,hp

def proper(w,edges,n,k):
    need(isinstance(w,str) and len(w)==n and set(w)<=set('01234'[:k]),'colour word format')
    need(all(w[a]!=w[b] for a,b in edges),'proper complete colouring')

def verify(c):
    s,edges,am,bm,hp=graph();need(s==c['geometry'],'declared exact geometry')
    w=c['colour4'];proper(w,edges,508,4);proper(c['colour5'],edges,508,5)
    need(w[:136]==c['host_word'],'host word equality')
    pins=[0,430,432,434,476,478]+list(range(480,493));need(''.join(w[hp.index(v)] for v in pins)==c['boundary_word'],'host boundary projection')
    ae=[[am.index(a),am.index(b)] for a,b in edges if a in am and b in am];sw=''.join(w[i] for i in am);root=am.index(0)
    for col in '0123':
        old=sw[root];perm={str(i):str(i) for i in range(4)};perm[old]=col;perm[col]=old
        moved=''.join(perm[x] for x in sw);need(moved[root]==col,'universal root agreement');proper(moved,ae,159,4)
    ids=c['moser_vertices'];need(len(ids)==len(set(ids))==7 and all(0<=i<136 for i in ids),'retained Moser vertices')
    loc={v:i for i,v in enumerate(ids)};me=[[loc[a],loc[b]] for a,b in edges if a in loc and b in loc]
    need(len(me)==11,'Moser edge count');need(not any(all(c[a]!=c[b] for a,b in me) for c in product(range(3),repeat=7)),'no three-colouring')
    s.update({'chromatic_number':4,'proper_four_checked':True,'proper_five_checked':True,'every_host_four_colouring_extends':True,'every_host_projection_unchanged':True,'boundary_word':c['boundary_word'],'four_word_sha256':hashlib.sha256(w.encode()).hexdigest(),'record_candidate':False,'solver_required':False})
    return s,edges

def emit_cnf(path,edges,hw):
    clauses=[]
    for i in range(508):
        row=[4*i+c+1 for c in range(4)];clauses.append(row)
        clauses.extend([[-a,-b] for a,b in combinations(row,2)])
    for i,j in edges:
        clauses.extend([[-4*i-c-1,-4*j-c-1] for c in range(4)])
    clauses.extend([[4*i+int(c)+1] for i,c in enumerate(hw)])
    path.write_text('p cnf 2032 '+str(len(clauses))+'\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=BASE/'certificate.json');ap.add_argument('--output',type=Path);ap.add_argument('--emit-pinned-cnf',type=Path);ap.add_argument('--check-expected',action='store_true');args=ap.parse_args()
    c=json.loads(args.certificate.read_text());s,e=verify(c)
    if args.check_expected:need(s==json.loads((BASE/'EXPECTED.json').read_text()),'expected output')
    if args.emit_pinned_cnf:emit_cnf(args.emit_pinned_cnf,e,c['host_word'])
    data=json.dumps(s,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(data)
    print(data,end='')
if __name__=='__main__':main()
