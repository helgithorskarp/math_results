#!/usr/bin/env python3
"""Exact fixed-outer local exclusion for Johnson solid J77; Python 3.11+.

Only the standard library is used. PROOF.md gives the geometric implication.
The input is the compact contact certificate, never floating hull/LP output.
"""
import argparse
from fractions import Fraction as F
from functools import reduce
import hashlib
import itertools
import json
from math import gcd, isqrt, lcm
from pathlib import Path

from chamber import partition
from model import VERTICES, cupola_construction
from q5 import Q, add, cross, dot, scale, sub

ROOT=Path(__file__).resolve().parent
R2=Q(11,4)/4
ZERO=(0,0)
CHILDREN=(((2,0,0),(1,1,0),(1,0,1)),((1,1,0),(0,2,0),(0,1,1)),
          ((1,0,1),(0,1,1),(0,0,2)),((1,1,0),(0,1,1),(1,0,1)))


def require(condition,message):
    if not condition:raise ValueError(message)


def decode(v):return tuple(Q(*x) for x in v)
def encode(v):return [[str(x.a),str(x.b)] for x in v]
def padd(x,y):return (x[0]+y[0],x[1]+y[1])
def pneg(x):return (-x[0],-x[1])
def pmul(x,y):return (x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0])


def psign(x):
    a,b=x
    if not a:return (b>0)-(b<0)
    if not b:return (a>0)-(a<0)
    if a>0 and b>0:return 1
    if a<0 and b<0:return -1
    c=a*a-5*b*b
    return ((c>0)-(c<0))*((a>0)-(a<0))


def monomials(n):
    return tuple(sorted({tuple(p.count(k) for k in range(3))
                         for p in itertools.product(range(3),repeat=n)},reverse=True))


def integer_column(vectors):
    denominator=lcm(*(x.a.denominator for v in vectors for x in v),
                    *(x.b.denominator for v in vectors for x in v))
    pairs=tuple(tuple((int(x.a*denominator),int(x.b*denominator)) for x in v) for v in vectors)
    divisor=reduce(gcd,(abs(z) for v in pairs for x in v for z in x))
    if divisor:pairs=tuple(tuple((a//divisor,b//divisor) for a,b in v) for v in pairs)
    return pairs


def determinant_polynomial(columns):
    """Exterior-algebra dynamic program, independently replayed below."""
    n=len(columns);states={(0,(0,0,0)):(1,0)}
    for col in columns:
        following={}
        for (mask,e),value in states.items():
            for row in range(n):
                if mask&(1<<row):continue
                negative=((mask>>(row+1)).bit_count()%2)==1
                for k in range(3):
                    x=col[k][row]
                    if x==ZERO:continue
                    term=pmul(value,x)
                    if negative:term=pneg(term)
                    f=tuple(e[j]+int(j==k) for j in range(3))
                    key=(mask|(1<<row),f)
                    following[key]=padd(following.get(key,ZERO),term)
        states=following
    return {e:states.get(((1<<n)-1,e),ZERO) for e in monomials(n)}


def reference_determinant(columns):
    """Direct Leibniz sum, independent of polynomial state propagation."""
    n=len(columns);total=ZERO
    for rows in itertools.permutations(range(n)):
        value=(1,0)
        for j,row in enumerate(rows):value=pmul(value,columns[j][row])
        if sum(rows[i]>rows[j] for i in range(n) for j in range(i+1,n))%2:value=pneg(value)
        total=padd(total,value)
    return total


def value_at(p,point):
    total=ZERO
    for e,x in p.items():
        coefficient=reduce(lambda a,b:a*b,(point[k]**e[k] for k in range(3)),1)
        total=padd(total,(coefficient*x[0],coefficient*x[1]))
    return total


def check_model():
    V=set(VERTICES);original,core,cap,gyrated,_=cupola_construction()
    require(len(V)==len(VERTICES)==55,'invalid J77 vertex count')
    require((len(original),len(core),len(cap),len(gyrated))==(60,50,5,5),'invalid independent cupola construction')
    require(V==core|gyrated and not core&gyrated,'fixture differs from independently constructed J77')
    require(all(tuple(-x for x in v) in core for v in core),'core is not centrally symmetric')
    require(sum(tuple(-x for x in v) in V for v in V)==50,'invalid antipodal structure')
    require(all(dot(v,v)==R2 for v in V),'invalid common circumradius')
    spanning=tuple(VERTICES[i] for i in (8,29,23))
    require(all(v in core for v in spanning) and dot(spanning[0],cross(spanning[1],spanning[2]))!=0,
            'three antipodal core pairs do not certify origin in the interior')


class Audit:
    def __init__(self):
        self.values=[];self.support_cache={};self.comparisons=0;self.coefficient_records=[]
        self.coefficients=0;self.positive_coefficients=0;self.simplex_counts={'paired':0,'full':0}
        self.reference_replays=0

    def contact(self,ids,triangle,kind):
        require(kind in ('paired','full'),'unknown contact kind')
        require(len(ids)==3 and all(type(k) is int and 0<=k<55 for k in ids),'invalid contact indices')
        a,b,j=ids;require(a!=b,'zero edge')
        v=VERTICES[j];edge=sub(VERTICES[b],VERTICES[a]);out=[]
        if kind=='paired':require(tuple(-x for x in v) in set(VERTICES),'missing selected antipodal vertex')
        for u in triangle:
            require(u[1]>0,'retained-coordinate chart fails')
            m=cross(edge,u);offset=dot(m,v)
            require(dot(m,u)==0,'normal outside target plane')
            require(dot(m,VERTICES[a])==offset==dot(m,VERTICES[b]),'contact misses its supporting edge')
            if all(x==0 for x in m):
                require(offset==0,'zero normal has nonzero offset')
            else:
                require(offset>0,'nonpositive supporting offset')
                self.values.append(offset)
                normalized=tuple(x/offset for x in m)
                key=(normalized,kind)
                if key not in self.support_cache:
                    for w in VERTICES:
                        value=dot(normalized,w)
                        gap=1-value
                        require(gap>=0,'vertex crosses a supporting line')
                        self.values.append(gap);self.comparisons+=1
                        if kind=='paired':
                            gap=1+value
                            require(gap>=0,'opposite support line fails')
                            self.values.append(gap);self.comparisons+=1
                    self.support_cache[key]=True
            out.append(cross(v,m) if kind=='paired' else cross(v,m)+(m[0],m[2]))
        return integer_column(out)

    def simplex(self,certificate,triangle,label):
        kind=certificate['kind'];ids=certificate['contacts'];n=3 if kind=='paired' else 5
        require(kind in ('paired','full') and len(ids)==n+1 and len({tuple(c) for c in ids})==n+1,
                'invalid contact simplex size or repeated contact')
        cols=[self.contact(c,triangle,kind) for c in ids];polys=[]
        test=(1,2,3)
        evaluated=[tuple(reduce(padd,((test[k]*c[k][r][0],test[k]*c[k][r][1]) for k in range(3)),ZERO)
                         for r in range(n)) for c in cols]
        for j in range(n+1):
            p=determinant_polynomial([c for k,c in enumerate(cols) if k!=j])
            require(value_at(p,test)==reference_determinant([c for k,c in enumerate(evaluated) if k!=j]),
                    'polynomial determinant disagrees with independent Leibniz replay')
            self.reference_replays+=1
            if j%2:p={e:pneg(x) for e,x in p.items()}
            polys.append(p)
        signs=[psign(value_at(p,(1,1,1))) for p in polys]
        if all(s==-1 for s in signs):polys=[{e:pneg(x) for e,x in p.items()} for p in polys]
        else:require(all(s==1 for s in signs),'cofactor kernel is not strictly positive at the centroid')
        require(all(psign(x)>=0 for p in polys for x in p.values()),'negative polynomial coefficient')
        self.values.extend(Q(*x) for p in polys for x in p.values())
        vals=[value_at(p,test) for p in polys]
        require(all(reduce(padd,(pmul(w,c[r]) for w,c in zip(vals,evaluated)),ZERO)==ZERO for r in range(n)),
                'signed cofactor kernel identity fails')
        corners=[all(psign(p[tuple(n if k==j else 0 for k in range(3))])>0 for p in polys) for j in range(3)]
        edges=[all(any(psign(x)>0 and e[missing]==0 for e,x in p.items()) for p in polys) for missing in range(3)]
        self.coefficients+=sum(len(p) for p in polys)
        self.positive_coefficients+=sum(psign(x)>0 for p in polys for x in p.values())
        self.simplex_counts[kind]+=1
        self.coefficient_records.append([label,kind,[[[list(e),list(p[e])] for e in sorted(p,reverse=True)] for p in polys]])
        return corners,edges


def solve_equilibrium(columns,target):
    n=len(columns)
    require(0<n<=5 and len(target)==6,'invalid equilibrium dimensions')
    matrix=[[columns[j][i] for j in range(n)]+[Q(target[i])] for i in range(6)];row=0
    for j in range(n):
        pivot=next((k for k in range(row,6) if matrix[k][j]!=0),None)
        require(pivot is not None,'dependent equilibrium columns')
        matrix[row],matrix[pivot]=matrix[pivot],matrix[row]
        divisor=matrix[row][j];matrix[row]=[x/divisor for x in matrix[row]]
        for k in range(6):
            if k!=row:
                multiplier=matrix[k][j]
                matrix[k]=[x-multiplier*y for x,y in zip(matrix[k],matrix[row])]
        row+=1
    require(all(matrix[k][-1]==0 for k in range(row,6)),'inconsistent normal equilibrium')
    weights=[matrix[k][-1] for k in range(n)]
    require(all(sum((w*c[k] for w,c in zip(weights,columns)),Q())==target[k] for k in range(6)),
            'reconstructed equilibrium fails')
    require(all(w>0 for w in weights),'nonpositive equilibrium coefficient')
    return weights


def check_vertex(record,audit):
    u=decode(record['direction']);C,M=record['C'],record['M'];bases=record['bases'];probes={};totals=[]
    require(type(C) is int and C>0 and type(M) is int and M>0,'invalid pointwise bounds')
    require(len(bases)==6 and {(b['axis'],b['sign']) for b in bases}=={(k,s) for k in range(3) for s in (1,-1)},
            'missing signed rotation target')
    for b in bases:
        columns=[]
        for ids in b['contacts']:
            key=tuple(ids)
            if key not in probes:
                audit.contact(ids,(u,u,u),'full')
                a,z,j=ids;m=cross(sub(VERTICES[z],VERTICES[a]),u);offset=dot(m,VERTICES[j])
                require(offset>0,'zero vertex probe');m=tuple(x/offset for x in m)
                bound=Q(M*M)-R2*dot(m,m)
                require(bound>0,'pointwise normal norm bound fails');audit.values.append(bound)
                probes[key]=cross(VERTICES[j],m)+m
            columns.append(probes[key])
        target=[0]*6;target[b['axis']]=b['sign']
        weights=solve_equilibrium(columns,target);total=sum(weights,Q())
        require(total<C,'pointwise coefficient bound fails')
        audit.values.extend(weights+[Q(C)-total]);totals.append(len(weights))
    return {'direction':record['direction'],'C':C,'M':M,'rotation_angle_bound_radians':str(F(1,2*C*M)),
            'positive_coefficient_count':sum(totals)}


def independent_sign_audit(values):
    denominator=10**200;root=isqrt(5*denominator*denominator)
    low,high=F(root,denominator),F(root+1,denominator)
    extra=[Q(),Q(1),Q(-1),Q(0,1),Q(0,-1),Q(9,-4),Q(9,4)]
    pell=Q(1)
    for _ in range(60):pell=pell*Q(9,-4)
    extra+=[pell,-pell]
    for x in values+extra:
        if x==0:expected=0
        else:
            endpoints=(x.a+x.b*low,x.a+x.b*high)
            require(min(endpoints)>0 or max(endpoints)<0,'independent rational sign enclosure is inconclusive')
            expected=1 if min(endpoints)>0 else -1
        require(x.sign()==expected,'ordered-field sign audit disagrees')
    return len(values)+len(extra)


def leaf_paths(data,parent_count):
    refinements={tuple(x) for x in data['second_refinements']}
    require(len(refinements)==len(data['second_refinements']) and
            all(len(x)==2 and 0<=x[0]<parent_count and 0<=x[1]<4 for x in refinements),
            'invalid adaptive refinement list')
    expected={(i,(j,k)) if (i,j) in refinements else (i,(j,))
              for i in range(parent_count) for j in range(4)
              for k in (range(4) if (i,j) in refinements else (0,))}
    actual=[(r['parent'],tuple(r['path'])) for r in data['leaves']]
    require(len(set(actual))==len(actual) and set(actual)==expected,'missing, duplicate, or extraneous leaf')
    return refinements


def child_triangle(parent,path):
    triangle=parent
    for j in path:
        require(type(j) is int and 0<=j<4,'invalid child index')
        triangle=tuple(tuple(sum((Q(w)*triangle[k][s]/2 for k,w in enumerate(t)),Q()) for s in range(3))
                       for t in CHILDREN[j])
    return triangle


def check(data):
    check_model();part=partition();parents=[tuple(decode(u) for u in t) for t in part['triangles']]
    require(data['parent_cells_sha256']==part['cells_sha256'],'partition digest differs from certificate model')
    refinements=leaf_paths(data,len(parents));audit=Audit();vertices=set();covered=set();open_edges=set()
    for leaf in data['leaves']:
        label=[leaf['parent'],leaf['path']];triangle=child_triangle(parents[leaf['parent']],leaf['path'])
        require(leaf['certificates'],'uncertified leaf interior')
        corner_covered=[False]*3;edge_covered=[False]*3
        for c in leaf['certificates']:
            corners,edges=audit.simplex(c,triangle,label)
            corner_covered=[x or y for x,y in zip(corner_covered,corners)]
            edge_covered=[x or y for x,y in zip(edge_covered,edges)]
        vertices.update(triangle)
        covered.update(u for u,yes in zip(triangle,corner_covered) if yes)
        for missing,yes in enumerate(edge_covered):
            if not yes:open_edges.add(tuple(sorted(u for k,u in enumerate(triangle) if k!=missing)))
    supplied_edges=[tuple(sorted(decode(u) for u in r['endpoints'])) for r in data['edges']]
    require(len(set(supplied_edges))==len(supplied_edges) and set(supplied_edges)==open_edges,
            'exceptional edge list is incomplete or extraneous')
    for i,(edge,record) in enumerate(zip(supplied_edges,data['edges'])):
        _,edges=audit.simplex(record['certificate'],(edge[0],edge[1],edge[1]),['edge',i])
        require(edges[2],'exceptional open edge is uncertified')
    remaining=vertices-covered;supplied=[decode(r['direction']) for r in data['vertices']]
    require(len(set(supplied))==len(supplied) and set(supplied)==remaining,
            'exceptional vertex list is incomplete or extraneous')
    point_bounds=[check_vertex(r,audit) for r in data['vertices']]
    audit_count=independent_sign_audit(audit.values)
    coefficient_digest=hashlib.sha256(json.dumps(audit.coefficient_records,separators=(',',':')).encode()).hexdigest()
    fixture_digest=hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {'agent':'six-rupert-2','role':'researcher',
            'claim_status':'every_fixed_outer_J77_projection_excludes_sufficiently_small_nonzero_relative_rotations',
            'arbitrary_planar_translations_covered':True,'scales_covered':'lambda >= 1',
            'uniform_rotation_bound_claimed':False,'global_rupert_status_resolved':False,
            'vertex_count':55,'antipodal_core_vertex_count':50,'origin_in_interior_pairs':[8,29,23],
            'supporting_faces_checked':part['face_count_checked'],'distinct_face_normal_planes':part['distinct_unoriented_face_planes'],
            'projective_polygons':part['polygon_count'],'parent_triangles':len(parents),
            'adaptive_second_refinements':len(refinements),'leaf_triangles':len(data['leaves']),
            'mesh_vertices':len(vertices),'vertices_covered_by_triangle_cofactors':len(covered),
            'exceptional_open_edges':len(open_edges),'exceptional_vertices':len(remaining),
            'contact_simplex_counts':audit.simplex_counts,'support_comparisons':audit.comparisons,
            'nonnegative_cofactor_coefficients':audit.coefficients,'strictly_positive_cofactor_coefficients':audit.positive_coefficients,
            'independent_Leibniz_determinant_replays':audit.reference_replays,
            'independent_rational_sign_audits':audit_count,'pointwise_vertex_bounds':point_bounds,
            'partition_sha256':part['cells_sha256'],'exact_coefficient_sha256':coefficient_digest,
            'canonical_certificate_sha256':fixture_digest}


def self_test(data):
    bad=json.loads(json.dumps(data));bad['leaves'].pop()
    failures=[lambda:leaf_paths(bad,44)]
    part=partition();first=data['leaves'][0];triangle=child_triangle(tuple(decode(u) for u in part['triangles'][first['parent']]),first['path'])
    c=json.loads(json.dumps(first['certificates'][0]));a,b,j=c['contacts'][0];c['contacts'][0]=[b,a,j]
    failures.append(lambda:Audit().simplex(c,triangle,['invalid reversed support']))
    repeated=json.loads(json.dumps(first['certificates'][0]));repeated['contacts'][1]=repeated['contacts'][0]
    failures.append(lambda:Audit().simplex(repeated,triangle,['invalid repeated contact']))
    point=json.loads(json.dumps(data['vertices'][0]));point['bases'].pop()
    failures.append(lambda:check_vertex(point,Audit()))
    for invalid in failures:
        try:invalid()
        except ValueError:pass
        else:raise ValueError('malformed certificate accepted')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args();data=json.loads((ROOT/'certificates.json').read_text())
    if args.self_test:self_test(data)
    print(json.dumps(check(data),indent=2,sort_keys=True))
