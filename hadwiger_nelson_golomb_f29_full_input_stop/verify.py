#!/usr/bin/env python3
"""Exact physical reconstruction and exhaustive source-witness verification.

No SAT solver, floating-point arithmetic, or graph library is used.
"""
from pathlib import Path
from itertools import combinations, product
import argparse, hashlib, json
BASE = Path(__file__).resolve().parent
DEN = 144
G12 = [(0,0,0,0),(12,0,0,0),(6,0,6,0),(-6,0,6,0),
       (-12,0,0,0),(-6,0,-6,0),(6,0,-6,0),(2,0,0,2),
       (-1,-1,1,-1),(-1,1,-1,-1)]
PARENT_MAP = [0,153,150,169,166,161,158,53,65,59]
FMAP = [7,10,11,12,13,14,15,16,17,18,19,20,21,22,23,1,
        24,25,26,27,2,28,29,30,0,9,31,3,8]

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(x):
    return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()

def norm(p):
    a,b,c,d = p
    return a*a+33*b*b+3*c*c+11*d*d, 2*a*b+2*c*d

def difference(p,q):
    return tuple(x-y for x,y in zip(p,q))

def physical_edges(points,den):
    require(len(set(points)) == len(points), 'unmerged coordinates')
    edges=[]; distances=[]
    for i,j in combinations(range(len(points)),2):
        n=norm(difference(points[i],points[j]));distances.append(n)
        if n == (den*den,0):
            edges.append((i,j))
    return edges,distances

def transform(row):
    # 144*(G7 + (G8-G7)*f), f=row/12.
    # Multiplication by (-3-sqrt33+i(sqrt3-3sqrt11))/12.
    a,b,c,d=row
    return (24-3*a-33*b-3*c+33*d,
            -a-3*b+3*c-d,
            a-33*b-3*c-11*d,
            24-3*a+3*b-3*c-3*d)

def reconstruct():
    rows=[]
    for line in (BASE/'f29.tsv').read_text().splitlines():
        if not line or line.startswith('#'):continue
        row=list(map(int,line.split()))
        require(len(row)==5 and row[0]==len(rows),'F29 row labels')
        rows.append(tuple(row[1:]))
    require(len(rows)==29,'F29 source size')
    g=[tuple(12*x for x in row) for row in G12]
    f=[transform(row) for row in rows]
    points=list(g);fm=[]
    for p in f:
        if p not in points:points.append(p)
        fm.append(points.index(p))
    require(fm==FMAP,'collision/source map')
    require((f[0],f[28],f[25])==(g[7],g[8],g[9]),'declared triangle frame')
    # The map is a unit isometry because its multiplier has norm one.
    require(norm((-3,-1,1,-3))==(144,0),'isometry multiplier')
    e,d=physical_edges(points,DEN)
    ge,gd=physical_edges(G12,12)
    fe,fd=physical_edges(rows,12)
    mapped={tuple(sorted((fm[a],fm[b]))) for a,b in fe}
    require(len(e)==86 and len(points)==32 and len(ge)==18 and len(fe)==75,
            'complete physical cardinalities')
    require(set(ge)<=set(e) and mapped<=set(e),'input edges preserved')
    require([x for x in e if x[1]<10]==ge,'induced Golomb input')
    extra=sorted(set(e)-set(ge)-mapped)
    require(extra==[(4,17),(6,20),(6,21)],'complete private cross contacts')
    shared=sorted(set(fm)&set(range(10)))
    require(shared==[0,1,2,3,7,8,9],'shared physical input')
    require(all(a not in fm and b>=10 for a,b in extra),'private/private contact claim')
    # A compact literal extraction, byte-checked against the pinned parent source
    # during publication. It establishes a role map, not receiver compatibility.
    extract=[]
    for line in (BASE/'parent_roles.tsv').read_text().splitlines():
        if not line or line.startswith('#'):continue
        extract.append(list(map(int,line.split())))
    require([row[0] for row in extract]==PARENT_MAP,'parent role labels')
    for grow,row in zip(G12,extract):
        want=[0]*16
        for i,j in enumerate([0,5,9,12]):want[j]=8*grow[i]
        require(row[1:]==want,'native parent role coordinates')
    return points,e,ge,fm,extra,d,rows

def proper(word,edges,k):
    return all(0<=c<k for c in word) and all(word[a]!=word[b] for a,b in edges)

def full_input_words(edges,k):
    # Fixed literal order: exactly k^7 assignments. Every colouring can be
    # normalized on the unit triangle 0,1,2, and no colour symmetry remains
    # for k=4 because a three-colour Golomb word does not exist.
    return [tuple((0,1,2)+w) for w in product(range(k),repeat=7)
            if proper((0,1,2)+w,edges,k)]

def components(n,edges,removed_vertex=None,removed_edge=None):
    adj=[set() for _ in range(n)]
    left=set(range(n))
    if removed_vertex is not None:left.remove(removed_vertex)
    for a,b in edges:
        if removed_vertex in (a,b) or (a,b)==removed_edge:continue
        adj[a].add(b);adj[b].add(a)
    count=0
    while left:
        count+=1;stack=[left.pop()]
        while stack:
            v=stack.pop()
            for u in adj[v]&left:
                left.remove(u);stack.append(u)
    return count

def verify(cert):
    p,e,ge,fm,extra,ds,frows=reconstruct()
    require(cert['points144']==[list(x) for x in p],'point certificate')
    require(cert['edges']==[list(x) for x in e],'complete edge certificate')
    source=full_input_words(ge,4)
    require(len(source)==95,'complete normalized input count')
    require(not full_input_words(ge,3),'Golomb chromatic lower bound')
    words=cert['extensions']
    require(len(words)==95 and len(set(words))==95,'extension certificate size')
    require(all(isinstance(w,str) and len(w)==32 and set(w)<=set('0123') for w in words),
            'malformed extension')
    decoded=[tuple(map(int,w)) for w in words]
    require([w[:10] for w in decoded]==source,'complete source projection coverage')
    require(all(proper(w,e,4) for w in decoded),'improper extension')
    four=tuple(map(int,cert['proper_four']));five=tuple(map(int,cert['proper_five']))
    require(len(four)==len(five)==32 and proper(four,e,4) and set(four)==set(range(4)),
            'proper four-word')
    require(proper(five,e,5) and set(five)==set(range(5)),'proper five-word')
    require(components(32,e)==1,'connectedness')
    articulations=[v for v in range(32) if components(32,e,removed_vertex=v)>1]
    bridges=[edge for edge in e if components(32,e,removed_edge=edge)>1]
    require(not articulations and not bridges,'nonseparability gate')
    return {'status':'VERIFIED_FIXED_GOLOMB_F29_UNIVERSAL_INPUT_EXTENSION',
            'points':32,'complete_unit_edges':86,'all_pairs':496,
            'golomb_edges':18,'f29_edges':75,'shared_vertices':7,'shared_edges':10,
            'private_cross_edges':[list(x) for x in extra],
            'articulation_vertices':articulations,'bridges':bridges,
            'normalized_complete_input_words':95,'labelled_complete_input_words':2280,
            'input_words_rejected':0,'input_words_extended':95,
            'chromatic_number':4,'proper_four':cert['proper_four'],
            'proper_five':cert['proper_five'],'native_parent_role_map':PARENT_MAP,
            'receiver_tested':False,'receiver_ready':False,'record_candidate':False,
            'point_hash':digest(p),'edge_hash':digest(e),'distance_hash':digest(ds),
            'input_word_hash':digest(source),'extension_hash':digest(words),
            'f29_fixture_sha256':hashlib.sha256((BASE/'f29.tsv').read_bytes()).hexdigest()}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=BASE/'certificate.json')
    ap.add_argument('--check-expected',action='store_true');args=ap.parse_args()
    r=verify(json.loads(args.certificate.read_text()))
    if args.check_expected:
        require(r==json.loads((BASE/'expected.json').read_text()),'expected result mismatch')
    print(json.dumps(r,indent=2,sort_keys=True))

if __name__=='__main__':main()
