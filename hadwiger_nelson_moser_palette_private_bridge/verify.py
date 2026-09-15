"""Independent quadratic-tower geometry and named-colour elimination checker.

Imports no producer or sibling module. The complete finite relation is
recomputed; the certificate's aggregate counts are never proof premises.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from hashlib import sha256
from pathlib import Path
import argparse
import json

HERE=Path(__file__).resolve().parent

def need(ok, message):
    if not ok: raise ValueError(message)

def plus(a,b): return tuple(x+y for x,y in zip(a,b))
def minus(a,b): return tuple(x-y for x,y in zip(a,b))
def times(a,q): return tuple(x*q for x in a)
def m2(a,b): return (a[0]*b[0]+3*a[1]*b[1], a[0]*b[1]+a[1]*b[0])
def m4(a,b):
    return plus(m2(a[:2],b[:2]),times(m2(a[2:],b[2:]),11))+plus(m2(a[:2],b[2:]),m2(a[2:],b[:2]))
H=(Q(2),Q(-1,2),Q(0),Q(0))
def m8(a,b):
    return plus(m4(a[:4],b[:4]),m4(H,m4(a[4:],b[4:])))+plus(m4(a[:4],b[4:]),m4(a[4:],b[:4]))
def number(x):return (Q(x),)+(Q(0),)*7
ZERO=number(0);ONE=number(1)
S=(Q(0),Q(1))+(Q(0),)*6
T=(Q(0),)*2+(Q(1),)+(Q(0),)*5
Y=(Q(0),)*4+(Q(1),)+(Q(0),)*3
def pplus(a,b):return plus(a[0],b[0]),plus(a[1],b[1])
def pminus(a,b):return minus(a[0],b[0]),minus(a[1],b[1])
def pmul(a,b):return minus(m8(a[0],b[0]),m8(a[1],b[1])),plus(m8(a[0],b[1]),m8(a[1],b[0]))
def norm(v):return plus(m8(v[0],v[0]),m8(v[1],v[1]))

def check_geometry(cert):
    need(len(cert['coordinates'])==19,'coordinate count')
    pts=[]
    for row in cert['coordinates']:
        need(len(row)==2 and all(len(v)==8 for v in row),'coordinate shape')
        pts.append(tuple(tuple(Q(x) for x in v) for v in row))
    need(len(set(pts))==19,'collision merging')
    # Verify the Moser frame from two unit diamonds and the stated cap rows.
    source=((0,0,0,0),(12,0,0,0),(6,0,6,0),(18,0,6,0),(10,0,0,2),(5,-1,5,1),(15,-1,5,3),(6,0,-6,0),(12,0,12,0),(20,0,0,4),(-5,-1,5,-1))
    for p,(a,b,c,d) in zip(pts,source):
        want=(times(plus(number(a),times(m8(S,T),b)),Q(1,12)),times(plus(times(S,c),times(T,d)),Q(1,12)))
        need(p==want,'Moser coordinate')
    # Invert the frozen isometry, then check the two retained caps and six
    # common neighbours directly. Deleted caps are construction centres only.
    inverse=(times(S,Q(-1,2)),number(Q(1,2)))
    caps=[(ZERO,ZERO),(times(plus(ONE,S),Q(1,2)),Y),(times(minus(ONE,S),Q(1,2)),Y),(ONE,ZERO)]
    back=[pplus(caps[1],pmul(inverse,pminus(p,(ZERO,ONE)))) for p in pts[11:]]
    need(back[:2]==caps[1:3],'retained palette caps')
    forward=(times(S,Q(-1,2)),number(Q(-1,2)))
    need(all(pplus((ZERO,ONE),pmul(forward,pminus(c,caps[1]))) not in pts for c in (caps[0],caps[3])),'deleted caps absent from union')
    for i in range(3):
        x,y=back[2+2*i:4+2*i];a,b=caps[i:i+2]
        need(pplus(x,y)==pplus(a,b),'diamond midpoint')
        delta=pminus(b,a)
        want=(times(m8(S,delta[1]),Q(-1,3)),times(m8(S,delta[0]),Q(1,3)))
        need(pminus(x,y)==want,'ordered common neighbours')
        need(norm(pminus(x,a))==norm(pminus(x,b))==norm(pminus(y,a))==norm(pminus(y,b))==ONE,'diamond incidence')
    distances=[];edges=[]
    for a,b in combinations(range(19),2):
        v=norm(pminus(pts[a],pts[b]));distances.append([a,b,[str(x) for x in v]])
        if v==ONE:edges.append((a,b))
    inherited=[e for e in edges if (e[0]<11)==(e[1]<11)]
    cross=[e for e in edges if e not in inherited]
    need(edges==[tuple(e) for e in cert['edges']],'complete unit edges')
    need(inherited==[tuple(e) for e in cert['inherited_edges']],'inherited edges')
    need(cross==[tuple(e) for e in cert['new_edges']]==[(0,11),(1,16),(2,15),(3,12)],'new contacts')
    need(len(edges)==34 and len(inherited)==30,'edge counts')
    need({e for e in edges if e[0]>=11}=={(11,13),(11,14),(11,15),(11,16),(12,15),(12,16),(12,17),(12,18),(13,14),(15,16),(17,18)},'palette elimination structure')
    return pts,edges,inherited,distances

def canonical(w):
    names={};return ''.join(str(names.setdefault(c,len(names))) for c in w)

def moser_fibres(edges):
    adj=[set() for _ in range(11)]
    for a,b in edges:
        if b<11:adj[a].add(b);adj[b].add(a)
    order=sorted(range(11),key=lambda a:(-len(adj[a]),a));word=[-1]*11
    fibres={};count=0
    def rec(pos):
        nonlocal count
        if pos==11:
            count+=1;fibres.setdefault(tuple(word[7:11]),set()).add(tuple(word[:4]));return
        v=order[pos]
        for c in range(4):
            if all(word[u]!=c for u in adj[v]):
                word[v]=c;rec(pos+1)
        word[v]=-1
    rec(0)
    return fibres,count

def complete_relation(edges):
    fibres,mwords=moser_fibres(edges)
    need(len(fibres)==240,'isolated Moser relation size')
    need(set(fibres)=={w for w in product(range(4),repeat=4) if not(w[0]==w[1] and w[2]==w[3])},'isolated Moser formula')
    palette=[]
    for w in product(range(4),repeat=6):
        e0,e1,e2=[set(w[i:i+2]) for i in (0,2,4)]
        if not all(len(e)==2 for e in (e0,e1,e2)):continue
        d1=set(range(4))-(e0|e1);d2=set(range(4))-(e1|e2)
        if d1 and d2:palette.append((w,d1,d2))
    need(len(palette)==1200,'isolated palette relation size')
    base=set();full=set();bn=fn=0;mp=set();pp=set();designed_only=0
    for mw,states in sorted(fibres.items()):
        for pw,d1,d2 in palette:
            w=mw+pw;cw=canonical(w);base.add(cw);bn+=1
            # Eliminate the two P8 private colours exactly. Each is an
            # independent choice from its available palette complement.
            good=any(a!=pw[3] and b!=pw[2] and (d1-{x}) and (d2-{y}) for x,a,b,y in states)
            two=any((d1-{x}) and (d2-{y}) for x,a,b,y in states)
            designed_only+=bool(two)
            if good:
                full.add(cw);fn+=1;mp.add(canonical(mw));pp.add(canonical(pw))
    # An independent named-colour audit covers every assignment. Obtain the
    # common canonical truth-stream order only after the classification.
    stream=sha256();nc=0
    for rest in product(range(4),repeat=9):
        w=(0,)+rest;cw=''.join(map(str,w))
        if canonical(w)!=cw:continue
        nc+=1;stream.update((cw+f':{int(cw in base)}{int(cw in full)}\n').encode())
    gains=sorted(base-full)
    result={'all_canonical_patterns':nc,'baseline_canonical':len(base),'full_canonical':len(full),'gain_canonical':len(gains),'baseline_named':bn,'full_named':fn,'gain_named':bn-fn,'canonical_truth_stream_sha256':stream.hexdigest(),'gain_words_sha256':digest(gains),'full_moser_projection_canonical':len(mp),'full_palette_projection_canonical':len(pp)}
    return result,{'named_moser_full_colourings':mwords,'named_relation_with_only_two_prescribed_contacts':designed_only,'named_baseline_words_checked':bn}

def digest(x):return sha256(json.dumps(x,separators=(',',':'),sort_keys=True).encode()).hexdigest()

def proper(word,k,edges):
    need(len(word)==19 and all(type(c) is int and 0<=c<k for c in word),'colour word')
    need(all(word[a]!=word[b] for a,b in edges),'colour inequality')

def verify(cert=None):
    if cert is None:cert=json.loads((HERE/'certificate.json').read_text())
    need(cert['schema']=='moser-palette-private-bridge-v1','schema')
    pts,edges,base,distances=check_geometry(cert)
    terms=(7,8,9,10,13,14,15,16,17,18)
    need(tuple(cert['terminals'])==terms,'terminal order')
    terminal_edges=[e for e in edges if all(v in terms for v in e)]
    need(terminal_edges==[(13,14),(15,16),(17,18)],'bare terminal graph')
    proper(cert['four_colouring'],4,edges);proper(cert['five_colouring'],5,edges)
    need(set(cert['five_colouring'])==set(range(5)),'five colours used')
    proper(cert['isolated_extension'],4,base)
    w=tuple(cert['newly_forbidden_terminal_word'])
    need(tuple(cert['isolated_extension'][t] for t in terms)==w==(0,0,1,2,2,3,0,2,0,1),'new gain witness pins')
    # Short nonextension proof. First diamond avoids colour 0, forcing its
    # caps M0=M3. Their available colours are {1,3}; private palette vertices
    # P1,P2 are forced 1,3 respectively and are joined to these equal caps.
    first={(0,1),(0,2),(1,2),(1,3),(2,3)}
    need(first<=set(edges) and {(0,7),(1,7),(2,8),(3,8),(0,10)}<=set(edges),'diamond witness structure')
    need(set(range(4))-{w[i] for i in (4,5,6,7)}=={1},'P1 unique colour')
    need(set(range(4))-{w[i] for i in (6,7,8,9)}=={3},'P2 unique colour')
    # Independently exhaust the elementary three-colour diamond used above.
    diamond=[q for q in product(range(3),repeat=4) if all(q[a]!=q[b] for a,b in first)]
    need(len(diamond)==6 and all(q[0]==q[3] for q in diamond),'diamond equality')
    # The inherited Moser spindle supplies the lower bound four.
    second={(0,4),(0,5),(4,5),(4,6),(5,6)}
    need(first|second|{(3,6)}=={e for e in edges if e[1]<7},'Moser lower bound')
    relation,detail=complete_relation(edges)
    need(relation==cert['relation'],'complete relation mismatch')
    need(relation['gain_canonical']>0,'strict gain')
    return {'status':'EXACT_HETEROGENEOUS_RELATION_GAIN','points':19,'strict_unit_edges':34,'all_pairs':171,'inherited_edges':30,'cross_edges':4,'chromatic_number':4,'proper_five_colouring_checked':True,'bare_terminal_edges':3,'relation':relation,'elimination_audit':detail,'coordinate_sha256':digest(cert['coordinates']),'distance_sha256':digest(distances),'edge_sha256':digest(cert['edges']),'record_candidate':False,'ordinary_nonfour_signal':False}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check-expected',action='store_true');args=parser.parse_args()
    result=verify()
    if args.check_expected:need(result==json.loads((HERE/'expected.json').read_text()),'expected result mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))
