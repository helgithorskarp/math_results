#!/usr/bin/env python3
"""Complete exact geometry and an all-source-colouring extension proof.

Reads two small hash-pinned coordinate fixtures in this repository. Uses no
solver, source-relation census, numerical incidence or imported arithmetic.
"""
from pathlib import Path
from itertools import combinations,product
import argparse,hashlib,json
BASE=Path(__file__).resolve().parent
ROOT=BASE.parent
D=(1,3,5,15,11,33,55,165)
SCALE=288
BITS=(2,3,6,7,10,11,14,15)
SOURCE_HASH='8e44b5746cc16badb0ddc6db1bb33d5d64baa088f0715a175632977c5d371a13'

def need(ok,msg):
    if not ok:raise ValueError(msg)

def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()

def square_distance(a,b):
    out=[0]*8
    for k in (0,8):
        terms=[(i,a[k+i]-b[k+i]) for i in range(8) if a[k+i]!=b[k+i]]
        for ix,(i,x) in enumerate(terms):
            out[0]+=D[i]*x*x
            for j,y in terms[ix+1:]:out[i^j]+=2*D[i&j]*x*y
    return tuple(out)

def read_inputs():
    data={};manifest=json.loads((BASE/'inputs.json').read_text())
    for item in manifest['inputs']:
        raw=(ROOT/item['path']).read_bytes()
        need(hashlib.sha256(raw).hexdigest()==item['sha256'],'input identity: '+item['path'])
        data[item['role']]=raw
    b=[]
    for line in data['b214'].decode().splitlines():
        if not line or line.startswith('#'):continue
        p=tuple(map(int,line.split()))
        need(len(p)==16 and all(p[j]==0 for j in range(16) if j not in (0,5,9,12)),
             'native B214 coordinate field')
        b.append(tuple(24*x for x in p))
    need(len(b)==214 and len(set(b))==214,'B214 input order')
    old=[tuple(p) for p in json.loads(data['old507'])]
    need(len(old)==507 and all(len(p)==16 and all(type(x) is int for x in p) for p in old),
         'old coordinate extraction')
    h=[p for p in old if any(p[k] for k in BITS)]
    need(len(h)==133 and len(set(h))==133,'native Heule complement')
    return b,h,old

def construct():
    b,h,old=read_inputs()
    grows=[(0,0,0,0),(12,0,0,0),(6,0,6,0),(-6,0,6,0),
           (-12,0,0,0),(-6,0,-6,0),(6,0,-6,0),(2,0,0,2),
           (-1,-1,1,-1),(-1,1,-1,-1)]
    g=[]
    for row in grows:
        q=[0]*16
        for i,j in enumerate((0,5,9,12)):q[j]=24*row[i]
        g.append(tuple(q))
    raw=list(g)
    for reflect in (False,True):
        for p in b:
            z=list(p)
            if reflect:z[:8]=[-x for x in z[:8]]
            z[0]+=144 if reflect else -144
            raw.append(tuple(z))
    s=list(dict.fromkeys(raw));need(len(s)==343,'source collision merge')
    # Confirm exact identity/order with the reviewed source, without replaying
    # its negative relation proof or its neutral A159 completion.
    lines=[]
    for q in s:
        need(all(q[j]%8==0 for j in (0,1,4,5,8,9,12,13)),'source scale conversion')
        lines.append(' '.join(str(q[j]//8) for j in (0,1,4,5,8,9,12,13)))
    need(hashlib.sha256(('\n'.join(lines)+'\n').encode()).hexdigest()==SOURCE_HASH,
         'reviewed source coordinate identity')
    p=list(dict.fromkeys(s+h));need(len(p)==476 and p[:343]==s and p[343:]==h,'full collision merge')
    unit=(SCALE*SCALE,)+(0,)*7;edges=[];ds=hashlib.sha256()
    for i,j in combinations(range(476),2):
        n=square_distance(p[i],p[j]);ds.update((','.join(map(str,n))+'\n').encode())
        if n==unit:edges.append((i,j))
    se=[e for e in edges if e[1]<343]
    he=[e for e in edges if e[0]>=343]
    cross=[e for e in edges if e[0]<343<=e[1]]
    need((len(se),len(he),len(cross))==(1782,547,12),'complete edge partition')
    need({a for a,b in cross}=={0} and p[0]==(0,)*16,'one-origin attachment')
    outside=[i for i,x in enumerate(p) if x not in set(old)]
    need(len(outside)==146,'fixed previous-host containment screen')
    return p,edges,se,he,cross,ds.hexdigest(),outside

def proper(word,n,edges,k):
    return (isinstance(word,str) and len(word)==n and set(word)<=set(str(i) for i in range(k))
            and all(word[a]!=word[b] for a,b in edges))

def swap_zero(word,c):
    c=str(c)
    return ''.join(c if x=='0' else '0' if x==c else x for x in word)

def check_extension_rule(cert,edges):
    cword=cert['complement_with_origin_four_word']
    mapped=[]
    for a,b in edges:
        if b<343:continue
        # All these edges lie inside H133 plus source vertex0.
        need(a==0 or a>=343,'additional source contact breaks the rule')
        mapped.append((0 if a==0 else a-342,b-342))
    need(cword[0]=='0' and proper(cword,134,mapped,4),'proper complement with origin')
    # For every possible colour at the source origin, the literal transposition
    # 0<->c preserves every complement edge. No other source colour is used.
    for c in range(4):
        v=swap_zero(cword,c)
        need(v[0]==str(c) and proper(v,134,mapped,4),'colour-equivariant extension')
    return mapped

def verify(cert):
    p,edges,se,he,cross,dh,outside=construct()
    need(cert['schema']=='opposed343-native-heule133-fixed-stop-v1','certificate schema')
    need(proper(cert['source_four_word'],343,se,4),'source positive word')
    ce=check_extension_rule(cert,edges)
    word=cert['source_four_word']+swap_zero(cert['complement_with_origin_four_word'],cert['source_four_word'][0])[1:]
    need(word==cert['whole_four_word'] and proper(word,476,edges,4),'whole extension')
    need(proper(cert['whole_five_word'],476,edges,5) and set(cert['whole_five_word'])==set('01234'),'proper five word')
    ge=[e for e in edges if e[1]<10]
    need(len(ge)==18,'retained complete Golomb')
    need(all(any(w[a]==w[b] for a,b in ge) for tail in product(range(3),repeat=7)
             for w in [(0,1,2)+tail]),'ordinary chromatic lower bound')
    return {'status':'VERIFIED_FIXED_OPPOSED343_HEULE133_UNIVERSAL_EXTENSION',
            'points':476,'complete_unit_edges':len(edges),'all_pairs':113050,
            'source_points':343,'source_edges':len(se),'complement_new_points':133,
            'complement_internal_edges':len(he),'cross_edges':len(cross),
            'source_contact_vertices':[0],'complement_plus_origin_edges':len(ce),
            'complete_source_projection':'unchanged: every full source four-colouring extends',
            'chromatic_number':4,'receiver_tested':False,'record_candidate':False,
            'outside_old_closed507_host':len(outside),'point_hash':digest(p),
            'edge_hash':digest(edges),'distance_hash':dh,'reviewed_source_point_hash':SOURCE_HASH,
            'extension_rule_origin_colours_checked':4}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=BASE/'certificate.json');ap.add_argument('--check-expected',action='store_true');args=ap.parse_args()
    result=verify(json.loads(args.certificate.read_text()))
    if args.check_expected:need(result==json.loads((BASE/'expected.json').read_text()),'expected result mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
