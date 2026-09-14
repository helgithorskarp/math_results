"""Independent integer geometry and path-elimination verifier; stdlib only.

Imports neither the producer nor its search. Negative claims are decided by
enumerating the three internal colours of each cell, with a shared unit edge.
"""
from pathlib import Path
from itertools import product,combinations
from functools import lru_cache
import argparse,hashlib,json

HERE=Path(__file__).resolve().parent
R=(1,3,5,7,15,21,35,105)
# Masks of square-free products of the independent primes 3,5,7.
MASK=(0,1,2,4,3,5,6,7)
T=(5,6,7,8,12,13,14,15)
CELL_EDGES=((0,1),(0,4),(1,2),(2,3),(3,4),(2,5),(3,5),(2,6),(3,6),(0,7),(4,7),(0,8),(4,8))
SECOND=(1,0,9,10,11,12,13,14,15)
def need(ok,msg):
    if not ok:raise ValueError(msg)
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def rmul(a,b):
    out=[0]*8
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:
                    mask=MASK[i]&MASK[j];factor=1
                    for k,p in enumerate((3,5,7)):
                        if mask&(1<<k):factor*=p
                    out[MASK.index(MASK[i]^MASK[j])]+=x*y*factor
    return tuple(out)
def norm(row):return add(rmul(row[:8],row[:8]),rmul(row[8:],row[8:]))
def basis(rad,n):return tuple(n if r==rad else 0 for r in R)
ZERO=basis(1,0)
def coordinates():
    # Every row has common denominator 8, x followed by y.
    a=basis(1,-4)+ZERO;b=basis(1,4)+ZERO
    d=basis(1,6)+basis(15,2)
    c=ZERO+add(basis(15,2),basis(7,2))
    e=basis(1,-6)+basis(15,2)
    p=[a,b,d,c,e]
    # Closed formulas for the four external equilateral apices.
    p.extend([
        add(basis(1,3),basis(21,-1))+add(add(basis(15,2),basis(7,1)),basis(3,-3)),
        add(basis(1,3),basis(21,1))+add(add(basis(15,2),basis(7,1)),basis(3,3)),
        add(basis(1,-5),basis(5,3))+add(basis(15,1),basis(3,1)),
        add(basis(1,-5),basis(5,-3))+add(basis(15,1),basis(3,-1))])
    return p+[neg(x) for x in p[2:]]
def graph(p):
    return [(i,j) for i,j in combinations(range(len(p)),2)
            if norm(tuple(x-y for x,y in zip(p[i],p[j])))==(64,)+(0,)*7]
def normal(w):
    seen={};return ''.join(str(seen.setdefault(c,len(seen))) for c in w)
def patterns(n):
    # Independent brute enumeration of all named assignments and canonicalization.
    return sorted({normal(w) for w in product(range(4),repeat=n)})
def check_word(word,n,edges,pins=(),colours=4):
    need(isinstance(word,str) and len(word)==n,'word length/type')
    need(all(c in '0123'[:colours] for c in word),'word alphabet')
    need(all(word[a]!=word[b] for a,b in edges),'improper word')
    need(all(word[v]==str(c) for v,c in pins),'incorrect terminal pin')
@lru_cache(None)
def relation(w):
    """All allowed ordered colours at A,B for the 9-point cell's four ports."""
    x=set(w[:2]);y=set(w[2:]);allowed=set()
    for a,b in product('0123',repeat=2):
        if a==b or a in y:continue
        for d,c,e in product('0123',repeat=3):
            if (d not in x and c not in x and e not in y
                and d!=c and c!=e and e!=a and d!=b):
                allowed.add((a,b));break
    return frozenset(allowed)
def feasible(w):
    return bool(relation(w[:4]) & {(b,a) for a,b in relation(w[4:])})
def verify(cert):
    need(set(cert)=={'schema','denominator','radicals','points','single_cell_words','three_colour_word','positive','negative','irreducible_example','delete_one_pin_words'},'certificate fields')
    need(type(cert['schema']) is int and cert['schema']==1,'schema')
    need(cert['denominator']==8 and cert['radicals']==list(R),'coordinate convention')
    rows=cert['points'];need(isinstance(rows,list) and len(rows)==16,'point count')
    need(all(isinstance(row,list) and len(row)==16 and all(type(c)is int for c in row) for row in rows),'integer coordinate format')
    p=coordinates();need(rows==list(map(list,p)),'construction coordinates')
    need(len(set(p))==16,'physical collisions')
    edges=graph(p);expected=set(CELL_EDGES)|{tuple(sorted((SECOND[a],SECOND[b]))) for a,b in CELL_EDGES}
    need(set(edges)==expected and len(edges)==25,'all strict unit edges / cell decomposition')
    need(not any(a in T and b in T for a,b in edges),'terminals independent')
    for a,b in zip(T[::2],T[1::2]):
        need(norm(tuple(x-y for x,y in zip(p[a],p[b])))==(192,)+(0,)*7,'sqrt3 terminal pair')
    check_word(cert['three_colour_word'],16,edges,colours=3)
    # Both triangles and a positive 3-word give chromatic number exactly 3.
    need({(2,3),(2,5),(3,5)}<=set(edges),'unit triangle')
    singles=cert['single_cell_words'];need([w for w,_ in singles]==patterns(4),'single-cell complete domain')
    for w,word in singles:check_word(word,9,CELL_EDGES,zip(range(5,9),w))
    domain=patterns(8);positive=cert['positive'];negative=cert['negative']
    need(all(isinstance(row,list) and len(row)==2 for row in positive),'positive row format')
    yes=[w for w,_ in positive]
    need(yes==sorted(set(yes)) and negative==sorted(set(negative)),'duplicate/order')
    need(not(set(yes)&set(negative)) and sorted(yes+negative)==domain,'complete partition')
    # Word witnesses certify every positive case; independent elimination certifies
    # both signs and checks the geometric decomposition used for the negatives.
    for w,word in positive:check_word(word,16,edges,zip(T,w));need(feasible(w),'positive transfer agreement')
    for w in negative:need(not feasible(w),'false negative')
    projections={};seven_bad=[]
    for k in range(1,8):
        full=set(patterns(k));restricted=[]
        for subset in combinations(range(8),k):
            seen={normal(w[i] for i in subset) for w in yes};missing=full-seen
            if missing:restricted.append((subset,missing))
        projections[str(k)]={'subsets':len(list(combinations(range(8),k))),'nonneutral':len(restricted)}
        if k==7:seven_bad=restricted
    irreducible=[w for w in negative if not any(normal(w[i] for i in sub) in missing for sub,missing in seven_bad)]
    example=cert['irreducible_example'];need(example=='01020102' and example in irreducible,'irreducible example')
    deletion=cert['delete_one_pin_words'];need(len(deletion)==8,'eight pin relaxations')
    for k,word in enumerate(deletion):check_word(word,16,edges,[(v,c) for j,(v,c) in enumerate(zip(T,example)) if j!=k])
    # All labelled pairs of two-element palettes; no missing monochromatic cases
    # in the full theorem above. This separate corollary explicitly assumes size2.
    palettes=list(combinations('0123',2))
    for x,y in product(palettes,repeat=2):
        w=''.join(x+y+x+y)
        need(feasible(w)==(not(set(x)&set(y))),'complementary-palette corollary')
    return {'status':'VERIFIED_EXACT_JOINT_RELATION','points':16,'unit_edges':25,'chromatic_number':3,
            'terminals':list(T),'bare_patterns':len(domain),'allowed':len(yes),'forbidden':len(negative),
            'irreducible_eight_terminal_forbidden':len(irreducible),'projections':projections,
            'single_cell_points':9,'single_cell_edges':13,'single_cell_patterns':len(singles),
            'complementary_palette_checks':36,'relaxed_pin_checks':8,'pair_checks':120,
            'checked_word_edge_inequalities':len(yes)*25+15*13+8*25+25,
            'point_sha256':digest(rows),'edge_sha256':digest(edges),
            'negative_sha256':digest(negative),'irreducible_sha256':digest(irreducible)}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json');parser.add_argument('--check-expected',action='store_true');a=parser.parse_args()
    result=verify(json.loads(a.certificate.read_text()))
    fixture=[]
    for line in (HERE/'points.tsv').read_text().splitlines():
        if not line or line.startswith('#'):continue
        row=list(map(int,line.split()))
        need(row[0]==len(fixture),'point fixture labels')
        fixture.append(row[1:])
    need(fixture==list(map(list,coordinates())),'point fixture coordinates')
    if a.check_expected:need(result==json.loads((HERE/'expected.json').read_text()),'expected result')
    print(json.dumps(result,indent=2,sort_keys=True))
