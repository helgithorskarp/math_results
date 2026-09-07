"""Solver-free proof checker using an independent finite-ring evaluation.

It checks all same-colour formal address pairs, without using a producer graph
or its field multiplication. See PROOF.md for why modular non-unit is decisive.
"""
import argparse
import base64
import hashlib
import itertools
import json
from pathlib import Path

import independent_field as exact

HERE = Path(__file__).resolve().parent
P = 1000001539
ROOTS = (512562457,103889680,157886017,2545130)  # a,b,c,e
FAMILY = 'Snail seed-centred seed-axis D9'
ORDER = 'k,reflection,seed; k=0..2; reflection=0,1; seed=0..28'


def require(condition,message):
    if not condition:
        raise ValueError(message)


def inv(x):
    return pow(x%P,-1,P)


def seed_values(rows,roots):
    """Evaluate the paper's formulas directly, with a=i*sqrt(3)."""
    a,b,c,e = (x%P for x in roots)
    w = (1+a)*inv(2)%P
    v = (5+b)*inv(6)%P
    p = (3+17*inv(8)*w-7*inv(8)*v+2*w*v
         +c*(-inv(4)+inv(8)*w-inv(8)*v+inv(4)*w*v))%P
    q = (11*inv(4)+13*inv(8)*w-inv(8)*v+2*w*v
         +e*inv(64)*(-w+v+w*v))%P
    return [p,q]+[(A+B*w+C*v+D*w*v)%P for A,B,C,D in rows]


def context(seed_bytes=None):
    if seed_bytes is None:
        seed_bytes = (HERE/'seed.json').read_bytes()
    data = json.loads(seed_bytes)
    rows = data['moser_rows']
    require(len(rows)==27 and all(isinstance(r,list) and len(r)==4
            and all(type(x) is int for x in r) for r in rows),'seed rows')
    a,b,c,e = ROOTS
    require((a*a+3)%P==0 and (b*b+11)%P==0 and (c*c-5)%P==0
            and (e*e+3320-632*a*b)%P==0,'residue equations')
    values = seed_values(rows,ROOTS)
    bars = seed_values(rows,(-a,-b,c,-e))
    require(len(set(zip(values,bars)))==29,'seed residue separation')
    return {'values':values,'bars':bars,'seed_sha256':hashlib.sha256(seed_bytes).hexdigest()}


def unpack(text,length):
    require(type(text) is str,'word type')
    data = base64.b64decode(text,validate=True)
    require(len(data)==(length+3)//4,'packed word length')
    require(base64.b64encode(data).decode()==text,'canonical base64')
    word = [(data[i//4]>>(2*(i%4)))&3 for i in range(length)]
    if length%4:
        require(data[-1]>>(2*(length%4))==0,'padding bits')
    return word


def addresses(ctx,centre,axis):
    s,bs = ctx['values'],ctx['bars']
    delta,bdelta = (s[axis]-s[centre])%P,(bs[axis]-bs[centre])%P
    require(delta!=0 and bdelta!=0,'axis denominator')
    u = delta*inv(bdelta)%P
    bu = bdelta*inv(delta)%P
    a = ROOTS[0]
    turn = (a-1)*inv(2)%P
    bturn = (-a-1)*inv(2)%P
    require(turn*bturn%P==1 and pow(turn,3,P)==1 and turn!=1,'rotation residue')
    out,bout = [],[]
    for k in range(3):
        t,bt = pow(turn,k,P),pow(bturn,k,P)
        for flip in range(2):
            for x,bx in zip(s,bs):
                v,bv = (x-s[centre])%P,(bx-bs[centre])%P
                if flip:
                    out.append(t*u*bv%P)
                    bout.append(bt*bu*v%P)
                else:
                    out.append(t*v%P)
                    bout.append(bt*bv%P)
    require(len(out)==174,'address count')
    return out,bout


def check_word(values,bars,word):
    require(len(values)==len(bars)==len(word),'word domain')
    comparisons = 0
    for colour in range(4):
        group = [i for i,c in enumerate(word) if c==colour]
        for i,j in itertools.combinations(group,2):
            require((values[i]-values[j])*(bars[i]-bars[j])%P!=1,
                    'same-colour pair has unit residue')
            comparisons += 1
    return comparisons


def three_colour(n,edges):
    """Definition-level exhaustive search with one triangle normalized."""
    neighbours = [set() for _ in range(n)]
    for i,j in edges:
        neighbours[i].add(j)
        neighbours[j].add(i)
    word = [-1]*n
    triangle = next(((i,j,k) for i,j in edges
                     for k in sorted(neighbours[i]&neighbours[j]) if j<k),None)
    if triangle:
        for colour,i in enumerate(triangle):
            word[i] = colour
    elif n:
        word[0] = 0
    nodes = 0

    def search():
        nonlocal nodes
        nodes += 1
        chosen = None
        best = None
        for i in range(n):
            if word[i]>=0:
                continue
            used = {word[j] for j in neighbours[i] if word[j]>=0}
            available = [c for c in range(3) if c not in used]
            if not available:
                return False
            key = (len(available),-len(neighbours[i]),i)
            if best is None or key<best:
                chosen,best = (i,available),key
        if chosen is None:
            return True
        i,available = chosen
        for colour in available:
            word[i] = colour
            if search():
                return True
        word[i] = -1
        return False

    found = search()
    return (word.copy() if found else None),nodes


def verify(certificate,ctx=None):
    if ctx is None:
        ctx = context()
    require(type(certificate.get('version')) is int and certificate['version']==2,'certificate version')
    require(certificate.get('family')==FAMILY,'certificate family')
    require(certificate.get('address_order')==ORDER,'address ordering')
    require(certificate.get('seed_sha256')==ctx['seed_sha256'],'seed hash')
    require(certificate.get('complete') is True,'incomplete certificate')
    cases = certificate['cases']
    expected = [(c,a) for c in range(29) for a in range(29) if c!=a]
    require(type(cases) is list and len(cases)==812,'complete case count')
    base = unpack(certificate['base_word'],29)
    require(all(c<3 for c in base),'seed three-colouring')
    comparisons = check_word(ctx['values'],ctx['bars'],base)
    seed = exact.exact_seed()
    triangle = certificate.get('seed_triangle')
    require(type(triangle) is list and len(triangle)==3
            and all(type(i) is int and 0<=i<29 for i in triangle)
            and len(set(triangle))==3,'seed triangle addresses')
    require(all(exact.norm(exact.minus(seed[i],seed[j]))==exact.times(exact.D**2,exact.ONE)
                for i,j in itertools.combinations(triangle,2)),'exact seed triangle')
    total = 0
    counts = {3:0,4:0}
    lower_nodes = 0
    max_nodes = 0
    max_core = 0
    for row,(c,a) in zip(cases,expected):
        require(type(row) is list and len(row)==5,'case row')
        require(type(row[0]) is int and type(row[1]) is int and row[:2]==[c,a],
                'complete ordered case coverage')
        word = unpack(row[2],174)
        chi,core = row[3:]
        require(type(chi) is int and chi in [3,4],'chromatic label')
        require(all(x<chi for x in word),'upper colour count')
        xs,bxs = addresses(ctx,c,a)
        total += check_word(xs,bxs,word)
        if chi==3:
            require(core==[],'unexpected three-colour core')
        else:
            require(type(core) is list and 4<=len(core)<=174
                    and all(type(i) is int and 0<=i<174 for i in core)
                    and len(set(core))==len(core),'lower core addresses')
            points,target = exact.exact_addresses(seed,c,a)
            selected = [points[i] for i in core]
            require(len(set(selected))==len(selected),'lower core coincidences')
            edges = [(i,j) for i,j in itertools.combinations(range(len(core)),2)
                     if exact.norm(exact.minus(selected[i],selected[j]))==target]
            model,nodes = three_colour(len(core),edges)
            require(model is None,'lower core is three-colourable')
            lower_nodes += nodes
            max_nodes = max(max_nodes,nodes)
            max_core = max(max_core,len(core))
        counts[chi] += 1
    return {'verified':True,'cases':812,'formal_D3_addresses_per_case':174,
            'family_D9_vertex_upper_bound':496,'seed_monochromatic_pairs':comparisons,
            'family_monochromatic_pairs':total,'all_graphs_four_colourable':True,
            'exactly_three_chromatic':counts[3],'exactly_four_chromatic':counts[4],
            'lower_core_search_nodes':lower_nodes,'max_lower_core_search_nodes':max_nodes,
            'max_lower_core_vertices':max_core,
            'record_improvement':False,'seed_sha256':ctx['seed_sha256'],
            'modulus':P,'proof_uses_solver_or_producer_geometry':False}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    args = p.parse_args()
    raw = args.certificate.read_bytes()
    result = verify(json.loads(raw))
    result['certificate_sha256'] = hashlib.sha256(raw).hexdigest()
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
