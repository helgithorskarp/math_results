#!/usr/bin/env python3
"""Exact two-private-cap coupling; independent tower arithmetic and enumeration."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations,product
import argparse,json,hashlib
BASE=Path(__file__).resolve().parent
GT=(0,1,3,4,5,7,8,9);BM=(6,2,10,11,0,1,12,13);BT=(2,3,4,5,6,7);TERM=GT+(10,11,12,13)
def need(b,s):
    if not b:raise ValueError(s)
def scalar(x):return (Q(x),)+(Q(0),)*7
ZERO=scalar(0);ONE=scalar(1);S=(Q(0),Q(1))+(Q(0),)*6;T=(Q(0),Q(0),Q(1))+(Q(0),)*5;Y=(Q(0),)*4+(Q(1),)+(Q(0),)*3
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(a,x):return tuple(v*x for v in a)
def r2(a,b):return (a[0]*b[0]+3*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def r4(a,b):
    ac=r2(a[:2],b[:2]);bd=r2(a[2:],b[2:]);ad=r2(a[:2],b[2:]);bc=r2(a[2:],b[:2])
    return add(ac,scale(bd,11))+add(ad,bc)
def mul(a,b):
    ac=r4(a[:4],b[:4]);bd=r4(a[4:],b[4:]);ad=r4(a[:4],b[4:]);bc=r4(a[4:],b[:4])
    return add(ac,r4(bd,(Q(2),Q(-1,2),Q(0),Q(0))))+add(ad,bc)
def cmul(a,b):return sub(mul(a[0],b[0]),mul(a[1],b[1])),add(mul(a[0],b[1]),mul(a[1],b[0]))
def norm(a,b):
    x,y=sub(a[0],b[0]),sub(a[1],b[1]);return add(mul(x,x),mul(y,y))
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def geometry():
    half=scalar(Q(1,2));shalf=scale(S,Q(1,2))
    G=[(ZERO,ZERO),(ONE,ZERO),(half,shalf),(scale(half,-1),shalf),(scale(ONE,-1),ZERO),(scale(half,-1),scale(shalf,-1)),(half,scale(shalf,-1))]
    q=(scalar(Q(1,6)),scale(T,Q(1,6)));rot=(scalar(Q(-1,2)),shalf)
    G += [q,cmul(rot,q),cmul(cmul(rot,rot),q)]
    # Direct closed coordinates, rather than the producer's transformed chain.
    a= sub(add(scalar(Q(3,4)),scale(S,Q(1,12))),scale(Y,Q(1,2)))
    b= sub(sub(scalar(Q(1,4)),scale(S,Q(1,12))),scale(Y,Q(1,2)))
    c= add(scale(sub(ONE,S),Q(1,4)),scale(mul(S,Y),Q(1,6)))
    d= sub(scale(sub(ONE,S),Q(1,4)),scale(mul(S,Y),Q(1,6)))
    points=G+[(a,c),(b,d),(a,scale(c,-1)),(b,scale(d,-1))]
    need(len(set(points))==14,'exact distinct points')
    E=[];stream=[]
    for i,j in combinations(range(14),2):
        n=norm(points[i],points[j]);need(n!=ZERO,'nonzero norm');stream.append([str(x) for x in n])
        if n==ONE:E.append((i,j))
    GE=[e for e in E if e[1]<10];BE=[(i,j) for i,j in combinations(range(8),2) if norm(points[BM[i]],points[BM[j]])==ONE]
    need(len(GE)==18 and len(BE)==11 and len(E)==24,'complete strict edge counts')
    need(set(E)==set(GE)|{tuple(sorted((BM[i],BM[j]))) for i,j in BE},'no omitted incidental contacts')
    need([e for e in E if e[0]<10<=e[1]]==[(2,12),(2,13),(6,10),(6,11)],'exact private old--new contacts')
    need(set(BM)&set(range(10))=={0,1,2,6},'shared diamond')
    for v,want in [(2,{0,1,3,12,13}),(6,{0,1,5,10,11})]:
        neigh={b if a==v else a for a,b in E if v in (a,b)};need(neigh==want,'private-cap neighbourhood')
    rows=[[[str(x) for x in c] for c in p] for p in points]
    return E,GE,BE,{'points':14,'unit_edges':24,'pairs':91,'point_hash':digest(rows),'edge_hash':digest(E),'distance_hash':digest(stream),'shared_vertices':[0,1,2,6],'shared_private_vertices':[2,6],'old_new_private_edges':[[2,12],[2,13],[6,10],[6,11]],'incidental_edges':0}
def proper(w,E,n,k):
    return len(w)==n and all(isinstance(x,int) and 0<=x<k for x in w) and all(w[a]!=w[b] for a,b in E)
def decode(w,n,k,E):
    need(isinstance(w,str) and len(w)==n and set(w)<=set('01234'[:k]),'word format');x=tuple(map(int,w));need(proper(x,E,n,k),'proper literal word');return x
def named_words(n,E,pins):
    free=[i for i in range(n) if i not in pins]
    for values in product(range(4),repeat=len(free)):
        w=[pins.get(i,-1) for i in range(n)]
        for i,c in zip(free,values):w[i]=c
        if proper(w,E,n,4):yield tuple(w)
def canon(w):
    ren={};return ''.join(str(ren.setdefault(c,len(ren))) for c in w)
def sethash(R):return hashlib.sha256(''.join(''.join(map(str,w))+'\n' for w in sorted(R)).encode()).hexdigest()
def verify(cert):
    E,GE,BE,result=geometry()
    gw=list(named_words(10,GE,{0:0,1:1}));bw=list(named_words(8,BE,{4:0,5:1}))
    GR={tuple(w[i] for i in GT) for w in gw};BR={tuple(w[i] for i in BT) for w in bw}
    need(len(gw)==190 and len(bw)==144 and len(GR)==114 and len(BR)==100,'isolated complete input relations')
    # This particular Golomb projection is neutral, despite chi(G)=4.
    bareGE=[(GT.index(a),GT.index(b)) for a,b in GE if a in GT and b in GT]
    need(GR==set(named_words(8,bareGE,{0:0,1:1})),'Golomb eight-terminal neutrality')
    product_relation={g+b[:2]+b[4:] for g in GR for b in BR}
    joined=set();bad2=set();bad6=set();full_words=0;fibres={w:0 for w in gw}
    for w in product_relation:
        fixed=dict(zip(TERM,w));domain2=set(range(4))-{fixed[i] for i in (0,1,3,12,13)};domain6=set(range(4))-{fixed[i] for i in (0,1,5,10,11)}
        if not domain2:bad2.add(w)
        if not domain6:bad6.add(w)
        matches=0
        for c2,c6 in product(range(4),repeat=2):
            full=[fixed.get(i,-1) for i in range(14)];full[2]=c2;full[6]=c6
            if proper(full,E,14,4):
                matches+=1;fibres[tuple(full[:10])]+=1
        need(matches==len(domain2)*len(domain6),'independent exact private-list factorization')
        full_words+=matches
        if matches:joined.add(w)
    lost=product_relation-joined
    need(set(fibres.values())=={36},'every full Golomb word has exactly36 extensions')
    need(lost==bad2|bad6,'all losses attributable to private sharing')
    need({w[:8] for w in joined}==GR,'Golomb marginal full')
    need({w[8:10]+w[:2]+w[10:12] for w in joined}==BR,'chain marginal full')
    Cbase={canon(w) for w in product_relation};Cjoin={canon(w) for w in joined};Clost={canon(w) for w in lost}
    need(all(len(set(w))>=3 for w in product_relation),'trivial global S4 stabilizers')
    need(len(product_relation)==2*len(Cbase) and len(joined)==2*len(Cjoin),'two residual colour permutations')
    four=decode(cert['four_word'],14,4,E);five=decode(cert['proper_five_same_terminals'],14,5,E)
    forbidden=tuple(map(int,cert['forbidden_terminal_word']));need(forbidden in lost,'forbidden full-interface pattern')
    need(tuple(five[i] for i in TERM)==forbidden,'same terminal colours in five-word')
    gf=decode(cert['G_word_for_forbidden_projection'],10,4,GE);bf=decode(cert['B_word_for_forbidden_projection'],8,4,BE)
    need(tuple(gf[i] for i in GT)==forbidden[:8] and tuple(bf[i] for i in BT)==forbidden[8:10]+forbidden[:2]+forbidden[10:12],'isolated product witness')
    need(not any(proper(w,GE,10,3) for w in product(range(3),repeat=10)),'Golomb excludes three colours')
    result.update({'interface':list(TERM),'golomb_full_words_edge_pinned':len(gw),'chain_full_words_edge_pinned':len(bw),'golomb_input_relation_edge_pinned':len(GR),'chain_input_relation_edge_pinned':len(BR),'golomb_eight_terminal_relation_neutral':True,'input_joint_edge_pinned':len(product_relation),'composite_joint_edge_pinned':len(joined),'lost_joint_edge_pinned':len(lost),'input_joint_canonical':len(Cbase),'composite_joint_canonical':len(Cjoin),'lost_joint_canonical':len(Clost),'input_joint_labelled':24*len(Cbase),'composite_joint_labelled':24*len(Cjoin),'lost_joint_labelled':24*len(Clost),'union_full_words_edge_pinned':full_words,'private2_rejects_edge_pinned':len(bad2),'private6_rejects_edge_pinned':len(bad6),'both_caps_reject_edge_pinned':len(bad2&bad6),'both_input_marginals_full':True,'product_relation_hash':sethash(product_relation),'composite_relation_hash':sethash(joined),'lost_relation_hash':sethash(lost),'chromatic_number':4,'proper_four_checked':True,'proper_five_same_forbidden_pins_checked':True,'receiver_tested':False,'record_candidate':False,'every_full_golomb_four_colouring_extends':True,'extensions_per_full_golomb_word':36,'pendant_triangles':[[2,12,13],[6,10,11]],'private_coupler_admission_met':False,'architecture_retired':True})
    return result
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=BASE/'certificate.json');ap.add_argument('--output',type=Path);ap.add_argument('--check-expected',action='store_true');a=ap.parse_args();r=verify(json.loads(a.certificate.read_text()))
    if a.check_expected:need(r==json.loads((BASE/'EXPECTED.json').read_text()),'expected complete relation')
    text=json.dumps(r,indent=2,sort_keys=True)+'\n'
    if a.output:a.output.write_text(text)
    print(text,end='')
if __name__=='__main__':main()
