"""Standalone exact certificate for the first ten-point decagon core."""
from pathlib import Path
from fractions import Fraction as Q
from functools import reduce
from itertools import combinations
from math import gcd, lcm
import argparse, copy, hashlib, json
import kernel as P

HERE = Path(__file__).resolve().parent
TARGET = (Q(113,225), Q(583,1000))
LABELS = (0,1,2,3,4,5,6,7,11,12)
ORIGIN_LABELS = (0,1,4,5)
CORE_KEY = [2,1,1]

def digest(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def core_points():
    """Seven reflections as polynomials in r=2t/(1+t), then common denominator S^3."""
    points = {2:[P.ONE,P.ZERO,P.ZERO],6:[P.ZERO,P.ONE,P.ZERO],7:[P.ZERO,P.ZERO,P.ONE]}
    folds = ((1,2,7,6),(3,2,6,7),(0,1,7,2),(5,3,6,2),
             (4,3,5,6),(11,1,0,7),(12,7,0,1))
    for new,i,j,old in folds:
        points[new] = [P.sub(P.mul(P.T,P.add(x,y)),z)
                       for x,y,z in zip(points[i],points[j],points[old])]
    D = P.power(P.S,3)
    def substitute(p):
        P.need(len(p)<=4,'degree at most three in r')
        return reduce(P.add,(P.scale(P.mul(P.power((0,2),k),P.power(P.S,3-k)),c)
                             for k,c in enumerate(p)),P.ZERO)
    return {i:[substitute(p) for p in points[i]] for i in LABELS}, D

def normalize_row(row):
    """Remove positive constants and powers of S=1+t only."""
    denominator = lcm(*(Q(v).denominator for p in row for v in p))
    row = [tuple(int(Q(v)*denominator) for v in p) for p in row]
    while True:
        divisions = [P.integer_divrem(p,P.S) for p in row]
        if not all(q is not None and not r for q,r in divisions):
            break
        row = [q for q,r in divisions]
    content = reduce(gcd,(v for p in row for v in p),0)
    P.need(content>0,'nonzero inequality row')
    return [tuple(v//content for v in p) for p in row]

def cap_rows(certificate):
    axes = [[P.decode(z) for z in row] for row in certificate['axes']]
    P.need(len(axes)==4 and all(len(row)==3 and any(row) for row in axes),'four nonzero three-dimensional axes')
    h0,eps = P.decode(certificate['base_height']),P.decode(certificate['epsilon'])
    P.need(h0>0 and eps>0,'positive base height and epsilon')
    rows,heights,guards = [],[],[]
    for w in axes:
        axis = [(z,) if z else P.ZERO for z in w]
        norm = P.metric(axis,axis)
        g = P.scale(P.mul(P.S,norm),Q(1,2))
        h = P.add(P.scale(P.add((h0*h0,),g),1/(2*h0)),(eps,))
        a = P.sub((h0*h0,),g)
        identity = P.add(P.scale(P.mul(a,a),1/(4*h0*h0)),
                         P.add(P.scale(P.add((h0*h0,),g),eps/h0),(eps*eps,)))
        P.need(P.sub(P.sub(P.mul(h,h),g),identity)==P.ZERO,'strict AM-GM cap guard identity')
        rows.append(normalize_row(P.normal(axis)+[h]))
        heights.append(h);guards.append(P.scale(identity,2))
    return rows,heights,guards

def intervals(certificate):
    P.need(certificate['format']==1 and tuple(map(P.decode,certificate['interval']))==TARGET,'fixed theorem interval/format')
    pieces = [tuple(map(P.decode,z)) for z in certificate['pieces']]
    P.need(bool(pieces) and pieces[0][0]==TARGET[0] and pieces[-1][1]==TARGET[1],'interval endpoints')
    P.need(all(TARGET[0]<=a<b<=TARGET[1] for a,b in pieces),'nonempty subintervals')
    P.need(all(pieces[i][1]==pieces[i+1][0] for i in range(len(pieces)-1)),'closed cover without gaps')
    P.need(Q(1,2)<TARGET[0]<TARGET[1]<Q(3,5),'positive definite metric domain')
    return pieces

def core_audit(points,D,pieces):
    P.need(set(points)==set(LABELS) and len(points)==10,'ten labeled core points')
    P.need(all(P.metric(v,v)==P.mul(D,D) for v in points.values()),'ten unit norms')
    contacts = []
    for i,j in combinations(LABELS,2):
        gap = P.sub(P.mul(P.T,P.mul(D,D)),P.metric(points[i],points[j]))
        if not gap:
            contacts.append([i,j])
        else:
            P.need(all(P.closed_sign(gap,a,b)==1 for a,b in pieces),'all45 core packing inequalities')
    P.need(len(contacts)==17,'seventeen exact core contacts')
    # Normalized positive origin relation, weights A/W,B/W,A/W,B/W.
    A,B,W = (-1,-1,5,5),(1,5,-1,-13),(0,8,8,-16)
    weights = (A,B,A,B)
    P.need(reduce(P.add,weights,P.ZERO)==W,'origin weight normalization')
    P.need(all(reduce(P.add,(P.mul(w,points[i][k]) for w,i in zip(weights,ORIGIN_LABELS)),P.ZERO)==P.ZERO
               for k in range(3)),'origin identity')
    rank = P.determinant([points[i] for i in ORIGIN_LABELS[:3]])
    for a,b in pieces:
        P.need(P.closed_sign(D,a,b)==1,'positive common coordinate denominator')
        P.need(all(P.closed_sign(w,a,b)==1 for w in weights+(W,)),'strictly positive origin weights')
        P.need(P.closed_sign(rank,a,b) in (-1,1),'rank three origin tetrahedron')
    return {'labels':list(LABELS),'contacts':contacts,'origin_labels':list(ORIGIN_LABELS),
            'origin_weight_numerators':[list(x) for x in weights],'origin_weight_denominator':list(W),
            'common_coordinate_denominator':list(D),'coordinates_sha256':digest(points)}

def cramer_data(rows):
    normals,rhs = [row[:3] for row in rows],[row[3] for row in rows]
    pair_crosses = {(i,j):P.cross(normals[i],normals[j]) for i,j in combinations(range(14),2)}
    result = []
    for triple in combinations(range(14),3):
        i,j,k = triple
        crosses = [pair_crosses[j,k],[P.scale(x,-1) for x in pair_crosses[i,k]],pair_crosses[i,j]]
        d = P.dot(normals[i],crosses[0])
        Y = [reduce(P.add,(P.mul(rhs[label],v[q]) for label,v in zip(triple,crosses)),P.ZERO)
             for q in range(3)]
        P.need(all(P.dot(normals[label],Y)==P.mul(d,rhs[label]) for label in triple),'undivided Cramer identity')
        E = [P.sub(P.mul(b,d),P.dot(n,Y)) for n,b in zip(normals,rhs)]
        K = P.sub(P.metric(Y,Y),P.mul(d,d))
        result.append((triple,d,Y,E,K))
    P.need(len(result)==364,'all14 choose3 active triples')
    return result

def verify(certificate, trace=False):
    pieces = intervals(certificate)
    points,D = core_points()
    core_summary = core_audit(points,D,pieces)
    rows = [normalize_row(P.normal(points[i])+[P.mul(P.T,D)]) for i in LABELS]
    caps,heights,guards = cap_rows(certificate); rows += caps
    P.need(len(rows)==14,'fourteen inequality rows')
    for a,b in pieces:
        P.need(all(P.closed_sign(h,a,b)==1 for h in heights),'positive cap heights')
    data = cramer_data(rows)
    summaries,traces = [],[]
    for a,b in pieces:
        counts = {'identically_singular':0,'opposite_slacks':0,'strict_norm':0}
        witnesses = []
        for triple,d,Y,E,K in data:
            if not d:
                counts['identically_singular']+=1; witnesses.append([list(triple),'singular']);continue
            signs = [P.closed_sign(e,a,b) for e in E]
            if 1 in signs and -1 in signs:
                counts['opposite_slacks']+=1
                witnesses.append([list(triple),'opposite',signs.index(1),signs.index(-1)])
            else:
                P.need(P.closed_sign(K,a,b)==-1,f'unproved active triple {triple} on [{a},{b}]')
                counts['strict_norm']+=1; witnesses.append([list(triple),'norm'])
        P.need(sum(counts.values())==364,'complete interval partition')
        summaries.append({'interval':[P.encode(a),P.encode(b)],'partition':counts,'witnesses_sha256':digest(witnesses)})
        if trace:traces.append(witnesses)
    result = {'agent':'six-tammes-2','role':'researcher','claim_status':'EXACT_COMPUTER_ASSISTED_CONDITIONAL_EXCLUSION',
              'interval':[P.encode(x) for x in TARGET],'core_key':CORE_KEY,
              'core':core_summary,'rows_sha256':digest(rows),'pieces':summaries,
              'total_active_triple_checks':364*len(pieces),'cap_capacity':1,'cover_capacity':4,
              'fifteen_point_extension':'excluded on the entire stated closed interval',
              'global_tammes15_bounds':'unchanged','independent_review':'pending',
              'trust_boundary':'exact Python arithmetic and checker; written polytope/cap proof; no formalization'}
    if trace:result['traces']=traces
    return result

def selftest(certificate):
    count = 0
    P.need(P.closed_sign((1,-2,2),Q(0),Q(1))==1,'positive polynomial with zero middle Bernstein coefficient')
    P.need(P.closed_sign((0,1),Q(0),Q(1)) is None,'zero closed endpoint cannot imply strict sign')
    P.need(P.closed_sign((0,1,-1),Q(0),Q(1)) is None,'both zero endpoints cannot imply strict sign')
    P.need(P.closed_sign(P.ZERO,Q(0),Q(1))==0,'zero polynomial')
    P.need(P.closed_sign((-1,2,-2),Q(0),Q(1))==-1,'negative polynomial')
    count += 5
    mutations = []
    z=copy.deepcopy(certificate);z['axes']=z['axes'][:3];mutations.append(z)
    z=copy.deepcopy(certificate);z['axes'][0]=[[0,1]]*3;mutations.append(z)
    z=copy.deepcopy(certificate);z['epsilon']=[0,1];mutations.append(z)
    z=copy.deepcopy(certificate);z['base_height']=[-1,1];mutations.append(z)
    z=copy.deepcopy(certificate);z['pieces'][1][0]=[523,1000];mutations.append(z)
    z=copy.deepcopy(certificate);z['pieces'][0][0]=[503,1000];mutations.append(z)
    z=copy.deepcopy(certificate);z['axes'][0][0]=[1,0];mutations.append(z)
    # A diameter guard alone is insufficient: these four axes cannot cover the sphere slice.
    z=copy.deepcopy(certificate);z['axes']=[[[1,1],[0,1],[0,1]]]*4;mutations.append(z)
    for z in mutations:
        try:verify(z)
        except (ValueError,KeyError,TypeError,ZeroDivisionError):count+=1
        else:raise ValueError('false certificate accepted')
    return count

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    parser.add_argument('--selftest',action='store_true');parser.add_argument('--trace',type=Path)
    parser.add_argument('--write-expected',action='store_true');args=parser.parse_args()
    certificate=json.loads(args.certificate.read_text());result=verify(certificate,trace=bool(args.trace))
    if args.trace:args.trace.write_text(json.dumps(result['traces'],separators=(',',':'))+'\n');del result['traces']
    if args.selftest:selftest(certificate)
    expected=HERE/'EXPECTED.json'
    if args.write_expected:expected.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:P.need(result==json.loads(expected.read_text()),'expected exact result mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))
