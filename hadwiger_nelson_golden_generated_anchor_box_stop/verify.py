#!/usr/bin/env python3
"""Solver-free checker using real quadratic pairs, not cyclotomic products.
Reconstructs the one full graph and the already-closed host containment gate.
"""
import copy
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations,product
from collections import Counter
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
Z=(F(0),F(0));O=(F(1),F(0));H=(F(10),F(2))
ONE=(O,Z);CZ=(Z,Z)
ROOT=((F(-1,4),F(1,4)),(F(1,4),F(0)))
BITS=((0,0,0,0),(1,0,0,0),(0,0,0,1),(1,0,0,1),
      (0,1,0,0),(0,0,1,0),(1,0,1,0),(0,1,0,1),
      (1,1,0,0),(0,0,1,1),(1,1,0,1),(1,0,1,1),
      (0,1,1,0),(1,1,1,0),(0,1,1,1),(1,1,1,1))
UNIT=(F(5,2),F(-1,2));GOLD=(F(5,2),F(1,2))
SCALES={'up':(F(3,2),F(1,2)),'down':(F(3,2),F(-1,2))}
UNIT_LABELS=((1,2),(1,3),(2,4),(2,5),(3,4),(3,6),(4,7),(4,8),(5,6),(5,8),(5,9),(6,7),(6,10),(7,9),(7,12),(7,13),(8,10),(8,11),(8,13),(9,11),(10,12),(11,12),(11,14),(12,15),(13,14),(13,15),(14,16),(15,16))
GOLD_LABELS=((1,5),(1,6),(2,3),(2,6),(2,7),(2,9),(3,5),(3,8),(3,10),(4,9),(4,10),(4,11),(4,12),(5,13),(6,13),(7,10),(7,14),(8,9),(8,15),(9,13),(9,14),(10,13),(10,15),(11,15),(11,16),(12,14),(12,16),(14,15))

def need(ok,msg):
    if not ok:raise ValueError(msg)
def qa(a,b):return a[0]+b[0],a[1]+b[1]
def qn(a):return -a[0],-a[1]
def qm(a,b):return a[0]*b[0]+5*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def qi(a):
    n=a[0]*a[0]-5*a[1]*a[1];need(n!=0,'zero inverse');return a[0]/n,-a[1]/n
def ca(a,b):return qa(a[0],b[0]),qa(a[1],b[1])
def cn(a):return qn(a[0]),qn(a[1])
def cs(a,b):return ca(a,cn(b))
def cc(a):return a[0],qn(a[1])
def cm(a,b):return qa(qm(a[0],b[0]),qn(qm(H,qm(a[1],b[1])))),qa(qm(a[0],b[1]),qm(a[1],b[0]))
def norm(a):return qa(qm(a[0],a[0]),qm(H,qm(a[1],a[1])))
def ci(a):
    r=qi(norm(a));return qm(r,a[0]),qn(qm(r,a[1]))
def scale(n,a):return (n*a[0][0],n*a[0][1]),(n*a[1][0],n*a[1][1])
def total(xs):
    r=CZ
    for x in xs:r=ca(r,x)
    return r

def power_row(a):
    (A,B),(C,D)=a
    v=(A-B+2*C+2*D,4*C+4*D,-2*B+2*C+6*D,-2*B+2*C-2*D)
    need(all(x.denominator==1 for x in v),'nonintegral point');return tuple(int(x) for x in v)
def radical_key(a):
    v=tuple(8*x for pair in a for x in pair)
    need(all(x.denominator==1 for x in v),'radical grid');return tuple(int(x) for x in v)
def norm8(v):
    a,b,c,d=v
    return a*a+5*b*b+10*c*c+50*d*d+20*c*d,2*a*b+2*c*c+10*d*d+20*c*d

def serial(rows):return ''.join(','.join(map(str,r))+'\n' for r in rows).encode('ascii')

def closed_base_overlay(B):
    pairs=list(combinations(range(16),2));dif={p:cs(B[p[1]],B[p[0]]) for p in pairs};ns={p:norm(dif[p]) for p in pairs}
    inv={(p,reflect):ci(cc(dif[p]) if reflect else dif[p]) for p in pairs for reflect in [False,True]}
    source_orient={reflect:[cc(x) if reflect else x for x in B] for reflect in [False,True]}
    closed=set(B);stats={}
    for name,s2 in SCALES.items():
        copies=set();raw=0
        for a,b in pairs:
            required=qm(s2,ns[a,b])
            for i,j in pairs:
                if ns[i,j]!=required:continue
                for left,right in [(i,j),(j,i)]:
                    for reflect in [False,True]:
                        raw+=1;m=cm(cs(B[right],B[left]),inv[((a,b),reflect)]);orient=source_orient[reflect]
                        offset=cs(B[left],cm(m,orient[a]));C=frozenset(ca(offset,cm(m,z)) for z in orient);copies.add(C)
        for C in copies:closed.update(C)
        stats[name]={'specifications':raw,'copies':len(copies)}
    return closed,stats

def geometry():
    powers=[ONE]
    for _ in range(4):powers.append(cm(powers[-1],ROOT))
    need(cm(powers[-1],ROOT)==ONE and total(powers)==CZ,'fifth roots')
    d=[cs(powers[i],powers[4]) for i in range(4)];b=scale(5,powers[4])
    B=[ca(b,total(scale(e,x) for e,x in zip(eps,d))) for eps in BITS]
    need(len(set(B))==16 and set(BITS)==set(product(range(2),repeat=4)),'source cube')
    lam=cm(d[0],ci(d[1]));need(norm(lam)==SCALES['down'],'wrong scale');need(power_row(lam)==(0,-1,0,-1),'multiplier identity')
    P={n:ca(b,cm(lam,total(scale(a,x) for a,x in zip(n,d)))) for n in product(range(4),range(4),range(4),range(7))}
    need(len(set(P.values()))==448,'grid collisions')
    C={k:tuple(ca(P[k],cm(lam,cs(z,b))) for z in B) for k in product(range(3),range(3),range(3),range(6))}
    need(len(C)==162 and set().union(*map(set,C.values()))==set(P.values()),'not whole copy union')
    need(C[0,0,0,0][0]==B[0] and C[0,0,0,0][4]==B[1],'root two anchors')
    seen=set(B);count=0;hist=Counter();parents=[]
    for k,vals in C.items():
        hist[len(set(vals)&set(B))]+=1
        if any(k):
            j=next(i for i in range(4) if k[i]);parent=tuple(k[i]-(i==j) for i in range(4));face=set(vals)&set(C[parent])
            need(len(face)==8 and face<=seen,'unavailable parent face')
            need(len(face-set(B))>=2,'anchors not generated');count+=1
            parents.append((k,parent))
        seen.update(vals)
    end=(2,2,2,5);corner=P[3,3,3,6]
    need(not set(C[end])&set(B),'terminal base anchored');need(corner not in B,'corner old')
    need(sum(corner in vals for vals in C.values())==1 and corner in C[end],'terminal copy unnecessary')
    merged=set(B)|set(P.values());need(len(set(B)&set(P.values()))==2,'overlap count');need(len(merged)==462 and len(merged)<=508,'cap')
    points=sorted(merged,key=power_row);rows=[power_row(x) for x in points];ix={x:i for i,x in enumerate(points)};rkeys=list(map(radical_key,points))
    edges=[]
    for i,j in combinations(range(len(points)),2):
        if norm8(tuple(a-b for a,b in zip(rkeys[j],rkeys[i])))==(160,-32):edges.append((i,j))
    src_unit=[(i+1,j+1) for i,j in combinations(range(16),2) if norm(cs(B[j],B[i]))==UNIT]
    src_gold=[(i+1,j+1) for i,j in combinations(range(16),2) if norm(cs(B[j],B[i]))==GOLD]
    need(tuple(src_unit)==UNIT_LABELS and tuple(src_gold)==GOLD_LABELS,'wrong source edge lists')
    closed,stats=closed_base_overlay(B);outside=[i for i,x in enumerate(points) if x not in closed]
    need(len(closed)==1386 and outside,'registered containment')
    need(corner not in closed,'terminal corner in closed overlay')
    return {'rows':rows,'edges':edges,'base_indices':[ix[x] for x in B],'outside':outside,'stats':stats,'hist':dict(sorted(hist.items())),'generated':count,'corner_index':ix[corner],'closed_points':len(closed)}

def validate(c,g,pblob,eblob):
    need(pblob==serial(g['rows']),'point bytes');need(eblob==serial(g['edges']),'incomplete edge bytes')
    need(c['point_sha256']==sha256(pblob).hexdigest(),'point hash');need(c['edge_sha256']==sha256(eblob).hexdigest(),'edge hash')
    need(c['vertices']==len(g['rows'])==462 and c['edges']==len(g['edges'])==1532,'counts')
    need(c['whole_copies']==162 and c['grid_points']==448 and c['intersection']==2,'copy budget')
    need(c['generated_anchored_copies']==g['generated']==161,'generated anchors')
    need(c['base_intersection_histogram']=={str(k):v for k,v in g['hist'].items()},'base anchoring histogram')
    need(c['terminal_unique_corner_index']==g['corner_index'] and c['terminal_copy_base_intersection']==0,'essential generated copy')
    need(c['outside_closed_overlay_points']==len(g['outside'])==406 and c['outside_overlay_witness_index']==g['outside'][0],'outside overlay witness')
    need(c['registered_overlay_counts']==g['stats'] and c['registered_overlay_points']==g['closed_points'],'registered overlay')
    need(c['base_indices']==g['base_indices'],'wrong role map')
    need(c['architecture_sha256']==sha256((HERE/'ARCHITECTURE.json').read_bytes()).hexdigest(),'changed architecture')
    word=c['four_word'];need(isinstance(word,str) and len(word)==462 and set(word)<=set('0123'),'four-word domain')
    need(all(word[i]!=word[j] for i,j in g['edges']),'monochromatic unit edge')
    sourceword=''.join(word[i] for i in g['base_indices']);need(sourceword==c['source_restriction_word'],'source word')
    failed=[[i,j] for i,j in GOLD_LABELS if sourceword[i-1]==sourceword[j-1]]
    need(failed==c['golden_source_constraints_violated'] and len(failed)==12,'concealed source failure')
    five=c['source_five_word'];need(len(five)==16 and set(five)<=set(range(5)),'source five word')
    need(all(five[i-1]!=five[j-1] for i,j in UNIT_LABELS+GOLD_LABELS),'improper source five word')
    K=c['source_K5_labels_one_based'];need(K==[1,2,3,5,6] and all(tuple(e) in UNIT_LABELS+GOLD_LABELS for e in combinations(K,2)),'source K5')
    need(c['source_two_distance_chromatic_number']==5 and c['ordinary_four_colourable'] is True and c['record_candidate'] is False and c['non_four_signal'] is False,'claim status')
    need(c['cap_proved_before_colouring'] is True,'pre-query cap')
    return True

def controls(c,g,pb,eb):
    trials=[]
    def altered(name,key,val):
        d=copy.deepcopy(c);d[key]=val;trials.append((name,d,pb,eb))
    i,j=g['edges'][0];bad=list(c['four_word']);bad[j]=bad[i]
    altered('monochromatic unit pair','four_word',''.join(bad))
    altered('truncated word','four_word',c['four_word'][:-1])
    altered('wrong physical cap','vertices',461)
    altered('missing generated-copy role','generated_anchored_copies',160)
    altered('false source lift','golden_source_constraints_violated',[])
    altered('false base-closure claim','outside_closed_overlay_points',0)
    altered('wrong terminal corner','terminal_unique_corner_index',0)
    altered('wrong source map','base_indices',list(reversed(c['base_indices'])))
    trials.append(('omitted unit edge',copy.deepcopy(c),pb,eb.split(b'\n',1)[1]))
    trials.append(('wrong coordinates',copy.deepcopy(c),pb.replace(b'-5',b'-6',1),eb))
    rejected=[]
    for name,d,p,e in trials:
        try:validate(d,g,p,e)
        except (ValueError,KeyError,IndexError,TypeError):rejected.append(name)
        else:raise ValueError('accepted corruption '+name)
    need(cm(ROOT,ci(ROOT))==ONE and norm(ROOT)==O and cc(cc(ROOT))==ROOT,'field controls')
    return rejected

def main():
    c=json.loads((HERE/'certificate.json').read_text());g=geometry();pb=(HERE/'points.csv').read_bytes();eb=(HERE/'edges.csv').read_bytes();validate(c,g,pb,eb);rejected=controls(c,g,pb,eb)
    print(json.dumps({'verified':True,'vertices':462,'unit_edges':1532,'complete_pairs':462*461//2,'ordinary_four_word_checked':True,'exact_chromatic_number_claimed':False,'grid_points':448,'base_overlap':2,'whole_copies':162,'generated_anchor_copies':161,'outside_base_overlay_points':406,'terminal_copy_necessary':True,'golden_constraints_violated':12,'point_sha256':sha256(pb).hexdigest(),'edge_sha256':sha256(eb).hexdigest(),'rejected_corruptions':rejected,'scope':'one frozen generated-anchor address box, no record improvement'},indent=2,sort_keys=True))
if __name__=='__main__':main()
