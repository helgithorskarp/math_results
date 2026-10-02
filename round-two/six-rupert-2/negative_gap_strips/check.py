"""Solver-free exact finite premises of the J74 negative-gap strip proof.

Uses only the standard library and two byte-pinned published geometric
inputs. Actual corner support maxima use every original receiving vertex.
All six spatial wrench components, weighted gaps and mass bounds are
checked as complete tensor-Bernstein coefficient identities/inequalities.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from math import comb
import argparse
import copy
import json
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
manifest=json.loads((HERE/'DEPENDENCIES.json').read_text())
for filename,fingerprint in manifest['pinned_input_sha256'].items():
    if sha256((ROOT/filename).read_bytes()).hexdigest()!=fingerprint:
        raise ValueError('published dependency fingerprint mismatch: '+filename)
sys.path.insert(0,str(ROOT))
from q5 import Q,add,sub,scale,dot,cross
from model import VERTICES as V,cupola_construction

def require(condition,message):
    if not condition:raise ValueError(message)

def field(pair):
    require(isinstance(pair,list) and len(pair)==2 and all(isinstance(x,str) for x in pair),'field encoding')
    return Q(F(pair[0]),F(pair[1]))

def vector(values):
    require(len(values)==3,'spatial vector dimension')
    return tuple(map(field,values))

def encoded(x):return [str(x.a),str(x.b)]

def apply(columns,v):return tuple(sum((columns[j][i]*v[j] for j in range(3)),Q()) for i in range(3))

def corner_elevation(corners,I,J):
    z,w=Q(F(I,2)),Q(F(J,2))
    return sum(((Q(1)-z if a==0 else z)*(Q(1)-w if b==0 else w)*corners[a][b]
                for a in range(2) for b in range(2)),Q())

def product_coefficient(controls,corners,I,J):
    result=Q()
    for k in range(2):
        for l in range(2):
            a,b=I-k,J-l
            if 0<=a<=1 and 0<=b<=1:
                result+=controls[k][l]*corners[a][b]/Q(comb(2,I)*comb(2,J))
    return result

def corner_powers(c):
    return {(0,0):c[0][0],(1,0):c[1][0]-c[0][0],
            (0,1):c[0][1]-c[0][0],(1,1):c[1][1]-c[1][0]-c[0][1]+c[0][0]}

def add_polynomial(target,source):
    for degree,value in source.items():target[degree]=target.get(degree,Q())+value

def multiply_powers(a,b):
    result={}
    for (i,j),x in a.items():
        for (k,l),y in b.items():
            degree=(i+k,j+l);result[degree]=result.get(degree,Q())+x*y
    return result

def bernstein2_powers(coefficients):
    # Three degree-two bases: (1-x)^2, 2x(1-x), x^2.
    bases=([1,-2,1],[0,2,-2],[0,0,1]);result={}
    for I,row in enumerate(coefficients):
        for J,x in enumerate(row):
            for i,a in enumerate(bases[I]):
                for j,b in enumerate(bases[J]):
                    degree=(i,j);result[degree]=result.get(degree,Q())+a*b*x
    return result

def verify(data):
    s=Q(0,1);phi=(1+s)/2
    m=scale(Q(1)/(2*phi),(Q(1),-phi,-phi*phi))
    d=((Q(-5)+3*s)/8,(Q(11)-3*s)/8,Q(F(-1,4)))
    e=cross(m,d)
    Q0=(((1+s)/4,(-1+s)/4,Q(F(1,2))),
        ((1-s)/4,Q(F(-1,2)),(1+s)/4),
        (Q(F(1,2)),-(1+s)/4,(1-s)/4))
    require(vector(data['m'])==m and vector(data['d'])==d and vector(data['e'])==e,'literal receiving coordinates')
    columns=tuple(vector(v) for v in data['proper_source_columns'])
    require(all(dot(a,b)==int(i==j) for i,a in enumerate(columns) for j,b in enumerate(columns)),
            'source-center orthogonality')
    require(dot(columns[0],cross(columns[1],columns[2]))==1,'proper source-center determinant')
    require(columns==Q0,'literal reference pose')
    require(dot(m,m)==1 and dot(d,d)<=1 and 0<dot(e,e)<=1,'receiving convex norm bounds and transverse independence')
    require(len(V)==60 and len(set(V))==60,'every original J74 vertex')
    originals,caps,gyrated,constructed,axes=cupola_construction()
    require(constructed==set(V) and len(originals)==60 and [len(cap) for cap in caps]==[5,5],
            'published two-cupola construction agrees with all originals')
    radius2=(11+4*s)/4
    require(all(dot(v,v)==radius2 for v in V) and radius2<Q(F(81,16)),'every original norm strictly below9/4')
    pairs=((0,7),(1,6),(2,5))
    require(all(V[b]==tuple(-x for x in V[a]) for a,b in pairs),'literal original antipodal pairs')
    determinant=dot(V[0],cross(V[1],V[2]))
    require(determinant!=0,'original antipodal span puts zero in the interior')
    require(Q(F(2673,256))<11 and Q(F(297,64))<5,'uniform quadratic and physical support constants')
    images=[apply(columns,v) for v in V]
    require(len(data['patches'])==2,'two stated receiving patches')
    declared=[('A',4+2*s,11+5*s,Q(F(1,100)),3),
              ('B',3+7*s/5,11+5*s,Q(F(1,200)),6)]
    result={'agent':'six-rupert-2','role':'researcher','proof_status':'exact finite premises; written continuous proof unformalized',
        'solid':'original unit-edge J74 metabigyrate rhombicosidodecahedron',
        'original_count':len(V),'source_pose_determinant':encoded(Q(1)),
        'original_radius_squared':encoded(radius2),'receiving_e_squared':encoded(dot(e,e)),
        'origin_interior_antipodal_pairs':[list(p) for p in pairs],
        'origin_spanning_determinant':encoded(determinant),
        'quadratic_support_constant':11,'physical_support_normal_norm_strict_upper_bound':5,
        'patches':[]}
    for patch,definition in zip(data['patches'],declared):
        label,lo,hi,sigma,mass_bound=definition
        require(patch['label']==label and list(map(field,patch['closed_t_interval']))==[lo,hi],
                'literal complete closed receiving interval')
        require(field(patch['strip_half_width'])==sigma and 0<sigma<=Q(F(1,32)),'literal strip width')
        tau=[lo/(1+lo),hi/(1+hi)]
        require(0<tau[0]<tau[1]<1,'positive affine receiving interval')
        normals=[[add(add(scale(1-t,m),scale(t,d)),scale(sign*sigma,e)) for sign in (-1,1)] for t in tau]
        require(all(u[2]<0 for row in normals for u in row),'receiving normal nonzero throughout closed rectangle')
        witnesses=patch['original_support_witnesses'];n=len(witnesses)-1
        require(n>0 and len({tuple(v) for v in witnesses})==len(witnesses),'distinct actual-original witnesses')
        for witness in witnesses:
            require(len(witness)==3 and all(isinstance(i,int) and 0<=i<60 for i in witness)
                    and witness[0]!=witness[1],'original support index domains')
        controls=patch['Bernstein_control_weights']
        require(len(controls)==2 and all(len(block)==2 for block in controls)
                and all(len(row)==n for block in controls for row in block),'bilinear weight dimensions')
        controls=[[[field(x) for x in row] for row in block] for block in controls]
        require(all(x>=0 for block in controls for row in block for x in row),'nonnegative Bernstein weight controls')
        masses=[[1+sum(row,Q()) for row in block] for block in controls]
        require(all(x<=mass_bound for row in masses for x in row),'uniform Bernstein mass bound')
        records=[]
        for a,b,k in witnesses:
            source=images[k];wrenches=[];gaps=[];ties=[]
            for j in range(2):
                wrenches.append([]);gaps.append([]);ties.append([])
                for h in range(2):
                    normal=cross(sub(V[b],V[a]),normals[j][h])
                    heights=[dot(normal,v) for v in V];height=max(heights)
                    require(height>=0,'actual receiving support nonnegative')
                    wrenches[j].append(tuple(cross(source,normal))+tuple(normal))
                    gaps[j].append(height-dot(normal,source))
                    ties[j].append([i for i,x in enumerate(heights) if x==height])
            records.append({'witness':[a,b,k],'corner_gap':gaps,'corner_wrench':wrenches,'corner_support_ties':ties})
        gapcoeff=[];balance_checks=0
        for I in range(3):
            gapcoeff.append([])
            for J in range(3):
                for component in range(6):
                    balance=corner_elevation([[x[component] for x in row] for row in records[0]['corner_wrench']],I,J)
                    for i,r in enumerate(records[1:]):
                        balance+=product_coefficient([[controls[k][l][i] for l in range(2)] for k in range(2)],
                            [[x[component] for x in row] for row in r['corner_wrench']],I,J)
                    require(balance==0,'full spatial wrench tensor polynomial balance')
                    balance_checks+=1
                gap=corner_elevation(records[0]['corner_gap'],I,J)
                for i,r in enumerate(records[1:]):
                    gap+=product_coefficient([[controls[k][l][i] for l in range(2)] for k in range(2)],r['corner_gap'],I,J)
                gapcoeff[I].append(gap)
        # A second polynomial representation verifies the product/elevation
        # identities directly; neither receives coefficients from an LP.
        for component in range(6):
            balance=corner_powers([[x[component] for x in row] for row in records[0]['corner_wrench']])
            for i,r in enumerate(records[1:]):
                add_polynomial(balance,multiply_powers(
                    corner_powers([[controls[k][l][i] for l in range(2)] for k in range(2)]),
                    corner_powers([[x[component] for x in row] for row in r['corner_wrench']])))
            require(all(x==0 for x in balance.values()),'direct ordinary-power full wrench identity')
        gap_power=corner_powers(records[0]['corner_gap'])
        for i,r in enumerate(records[1:]):
            add_polynomial(gap_power,multiply_powers(
                corner_powers([[controls[k][l][i] for l in range(2)] for k in range(2)]),corner_powers(r['corner_gap'])))
        expansion=bernstein2_powers(gapcoeff)
        require(all(gap_power.get((i,j),Q())==expansion.get((i,j),Q()) for i in range(3) for j in range(3)),
            'complete ordinary-power and tensor-Bernstein weighted-gap identity')
        delta=field(patch['strict_weighted_gap_floor']);kappa=field(patch['relative_source_Cayley_Euclidean_gate'])
        require(delta>0 and all(x < -delta for row in gapcoeff for x in row),'strict uniform negative weighted actual-support gap')
        margin=delta-22*mass_bound*kappa*kappa
        require(margin>0,'quadratic absorption on entire closed source radius')
        require(delta==Q(F(1,50)) and kappa==Q(F(1,100)),'literal stated gap and relative Cayley radius')
        result['patches'].append({'label':label,'closed_t_interval':[encoded(lo),encoded(hi)],
            'closed_tau_interval':[encoded(t) for t in tau],'strip_half_width':encoded(sigma),
            'proper_source_Cayley_Euclidean_radius':encoded(kappa),
            'all_original_corner_support_evaluations':len(witnesses)*4*len(V),
            'full_spatial_wrench_coefficient_equalities':balance_checks,
            'nonnegative_Bernstein_control_count':4*n,'minimum_control_weight':encoded(min(x for block in controls for row in block for x in row)),
            'control_mass_sums':[[encoded(x) for x in row] for row in masses],
            'integer_mass_upper_bound':mass_bound,
            'weighted_gap_tensor_Bernstein_coefficients':[[encoded(x) for x in row] for row in gapcoeff],
            'weighted_gap_ordinary_power_coefficients':[[encoded(gap_power.get((i,j),Q())) for j in range(3)] for i in range(3)],
            'maximum_weighted_gap_coefficient':encoded(max(x for row in gapcoeff for x in row)),
            'strict_weighted_gap_floor':encoded(delta),'raw_support_violation_lower_bound':encoded(margin),
            'physical_support_distance_lower_bound':encoded(margin/(5*mass_bound)),
            'actual_original_corner_support_records':[{'witness':r['witness'],
                'corner_support_ties':r['corner_support_ties'],
                'corner_source_gaps':[[encoded(x) for x in row] for row in r['corner_gap']]} for r in records],
            'conclusion':'no closed fit at any actual physical translation or lambda>=1, conditional on the stated proper relative source neighborhood'})
    return result

def self_test(data):
    damaged=[]
    def case(label,mutation):
        d=copy.deepcopy(data);mutation(d)
        try:verify(d)
        except (ValueError,ZeroDivisionError) as exc:damaged.append({'label':label,'rejected':True,'reason':str(exc)})
        else:raise ValueError('damaged mathematical control unexpectedly accepted: '+label)
    case('unbalanced positive control',lambda d:d['patches'][0]['Bernstein_control_weights'][0][0].__setitem__(0,
        encoded(field(d['patches'][0]['Bernstein_control_weights'][0][0][0])+Q(F(1,10**6)))))
    case('negative control',lambda d:d['patches'][0]['Bernstein_control_weights'][0][0].__setitem__(0,['-1','0']))
    case('wrong original source',lambda d:d['patches'][0]['original_support_witnesses'][0].__setitem__(2,36))
    case('wider receiving strip',lambda d:d['patches'][0].__setitem__('strip_half_width',['1/50','0']))
    case('enlarged source radius',lambda d:d['patches'][0].__setitem__('relative_source_Cayley_Euclidean_gate',['1/10','0']))
    case('unsupported gap floor',lambda d:d['patches'][0].__setitem__('strict_weighted_gap_floor',['1','0']))
    case('changed receiving ray',lambda d:d['m'].__setitem__(0,['1','0']))
    case('improper source pose',lambda d:d['proper_source_columns'].__setitem__(0,
        [encoded(-field(x)) for x in d['proper_source_columns'][0]]))
    return damaged

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write-expected',action='store_true')
    parser.add_argument('--print-record',action='store_true');parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args();data=json.loads((HERE/'certificate.json').read_text());record=verify(data)
    if args.write_expected:(HERE/'expected.json').write_text(json.dumps(record,indent=2)+'\n')
    else:require(record==json.loads((HERE/'expected.json').read_text()),'every complete expected mathematical field')
    if args.self_test:print(json.dumps({'rejected_semantic_damages':self_test(data)},indent=2))
    if args.print_record:print(json.dumps(record,sort_keys=True,separators=(',',':')))
    else:print('exact J74 negative-gap strip hypotheses verified')

if __name__=='__main__':main()
