#!/usr/bin/env python3
"""Independent algebra or semantic damage controls; not independent review."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[key]='1'
from fractions import Fraction as F
from pathlib import Path
from itertools import permutations
from math import comb,factorial
import argparse,copy,hashlib,json,resource,time
import check as C
H,E=C.H,C.E

def require(ok,message):H.require(ok,message)

def exact_add(a,b):
    out=a.copy()
    for k,v in b.items():out[k]=out.get(k,F(0))+v
    return {k:v for k,v in out.items()if v}

def exact_mul(a,b):
    out={}
    for(i,j),v in a.items():
        for(k,l),w in b.items():out[i+k,j+l]=out.get((i+k,j+l),F(0))+v*w
    return {k:v for k,v in out.items()if v}

def oracle_determinant(A):
    n=len(A);out={}
    for p in permutations(range(n)):
        sign=(-1)**sum(p[i]>p[j]for i in range(n)for j in range(i+1,n))
        value={(0,0):F(sign)}
        for i,j in enumerate(p):value=exact_mul(value,A[i][j])
        out=exact_add(out,value)
    return out

def rejects(label,function):
    try:function()
    except (ValueError,KeyError):return label
    raise ValueError('semantic damage was accepted: '+label)

def algebra(certificate,expected,deadline):
    cases=[F(0),F(1,3),F(-1,7),F(23,19),F(-51,11),F(10**10+1,7)]
    rounded=0
    for a in cases:
        ia=E.B.rational(a)
        require(F(ia.lo,E.SCALE)<=a<=F(ia.hi,E.SCALE),'exact primitive rational rounding')
        for b in cases:
            ib=E.B.rational(b)
            for actual,box in ((a+b,ia+ib),(a-b,ia-ib),(a*b,ia*ib)):
                require(F(box.lo,E.SCALE)<=actual<=F(box.hi,E.SCALE),'outward operation contains exact rational')
                rounded+=1
    # Independently re-expand every triangular Bernstein basis identity.
    identities=0
    for degree in range(6):
        for i in range(degree+1):
            for j in range(degree+1-i):
                expanded={}
                for k in range(i,degree+1):
                    for l in range(j,degree+1-k):
                        coeff=F(comb(k,i)*comb(l,j),comb(degree,i+j)*comb(i+j,i))
                        basis={(k,l):F(comb(degree,k)*comb(degree-k,l))}
                        for _ in range(degree-k-l):basis=exact_mul(basis,{(0,0):F(1),(1,0):F(-1),(0,1):F(-1)})
                        expanded=exact_add(expanded,{key:coeff*value for key,value in basis.items()})
                require(expanded=={(i,j):F(1)},'complete exact triangle Bernstein power identity')
                identities+=1
    # Permutation formula is separate from the production subset DP.
    matrices=[[[{(0,0):F(((i+2)*(j+3))%7-3),(1,0):F((i+j)%3-1),(0,1):F((i+2*j)%3-1)}
                for j in range(n)]for i in range(n)]for n in(2,3,4,5)]
    checked=0
    for A in matrices:
        oracle=oracle_determinant(A)
        bounded=[[{k:E.B.rational(v)for k,v in z.items()}for z in row]for row in A]
        produced=E.determinant(bounded,deadline)
        require(set(produced)==set(oracle),'complete polynomial determinant coefficient inventory')
        for k,value in oracle.items():
            box=produced[k];require(F(box.lo,E.SCALE)==value==F(box.hi,E.SCALE),'independent integer polynomial determinant equality')
            checked+=1
    bound=F(expected['uniform_dual_weight_sum_upper']);damages=[]
    for label,key,value in [('unsupported dual mass26','dual_sum_bound',26),
                            ('motion radius at unclosed factor1','closed_cayley_infinity_radius','1/162'),
                            ('unsupported physical coefficient','physical_gap_coefficient','1/4000')]:
        damaged=copy.deepcopy(certificate);damaged[key]=value
        damages.append(rejects(label,lambda d=damaged:C.close_bounds(d,bound)))
    damages.append(rejects('reversed outward enclosure',lambda:E.B(2,1)))
    return dict(status='EXACT_ALGEBRA_AND_CLOSURE_CONTROLS_PASSED',outward_rational_operation_controls=rounded,
                exact_bernstein_power_reexpansions=identities,independent_determinant_coefficients_checked=checked,
                rejected_semantic_damages=damages)

def geometry(certificate,expected,deadline):
    data=H.build(deadline);rows,triangles,centroid,root,record=C.prepare(certificate,data,deadline)
    require(record==expected['closed_cell_geometry'],'entire fresh geometry record agrees')
    damages=[]
    for label,mutation in [('wrong facet phase',lambda c:c['facet_signs'].__setitem__(0,-c['facet_signs'][0])),
                           ('missing defining wall',lambda c:c['polygon'][-1].__setitem__(0,H.encode(H.K.coerce(F(1,1000))))),
                           ('star ordering of convex vertices',lambda c:c.__setitem__('polygon',[c['polygon'][i]for i in(0,2,4,1,3)])),
                           ('reversed support orientation',lambda c:c['duals'][0]['contacts'][0].__setitem__(slice(0,2),c['duals'][0]['contacts'][0][:2][::-1])),
                           ('nonendpoint source label',lambda c:c['duals'][0]['contacts'][0].__setitem__(2,91)),
                           ('unsupported quadratic constant',lambda c:c.__setitem__('remainder_constant',3))]:
        damaged=copy.deepcopy(certificate);mutation(damaged)
        damages.append(rejects(label,lambda d=damaged:C.prepare(d,data,deadline)))
    missing=copy.deepcopy(certificate['duals'][0]);missing['contacts'].pop()
    damages.append(rejects('missing dual row',lambda:C.certify_dual(missing,rows,triangles,centroid,root,deadline)))
    flipped=copy.deepcopy(certificate['duals'][0]);flipped['sign']=-flipped['sign']
    damages.append(rejects('wrong Cramer target sign',lambda:C.certify_dual(flipped,rows,triangles,centroid,root,deadline)))
    dropped=copy.deepcopy(rows)
    for row in dropped.values():row[3]=row[4]=(E.ZERO,E.ZERO,E.ZERO)
    damages.append(rejects('removed actual translation coordinates',lambda:C.certify_dual(certificate['duals'][0],dropped,triangles,centroid,root,deadline)))
    example=record['grazing_tie_example'];require(example is not None,'genuine offendpoint closed-boundary tie is retained')
    polygon=[tuple(C.decode(z)for z in p)for p in certificate['polygon']]
    a,b=example['edge'];s,t=polygon[example['polygon_vertex']]
    m=tuple(F(2)**example['exponent']*z for z in H.M.cross(H.M.sub(data['points'][b],data['points'][a]),(H.O,s,t)))
    gap=H.M.dot(m,H.M.sub(data['points'][a],data['points'][example['original']]))
    require(gap==H.Z,'actual offendpoint grazing equality')
    damages.append(rejects('discarded closed horizon tie',lambda:require(H.sign(gap,root)>0,'false strict support hypothesis')))
    return dict(status='EXACT_FRESH_GEOMETRY_BOUNDARY_AND_DAMAGE_CONTROLS_PASSED',
                full_named_geometry_rebuilt=True,closed_cell_geometry_record_matches=True,
                rejected_semantic_damages=damages,exact_offendpoint_grazing_tie_checked=True)

def physical(certificate,expected,deadline):
    data=H.build(deadline);rows,triangles,centroid,root,record=C.prepare(certificate,data,deadline)
    require(record==expected['closed_cell_geometry'],'entire fresh physical geometry record agrees')
    polygon=[tuple(C.decode(z)for z in p)for p in certificate['polygon']]
    # Definition-level rotation polynomial and physical gap checks at two
    # distinct genuine boundaries. Zero motion is an actual fit control.
    eta=F(certificate['closed_cayley_infinity_radius']);rho=F(certificate['physical_gap_coefficient'])
    qcases=[(F(0),F(0),F(0)),(eta,F(0),F(0)),(F(0),-eta,F(0)),(eta,-eta,eta)]
    unique=sorted({tuple(c)for d in certificate['duals']for c in d['contacts']})
    identities=0;physical=0;zero=0
    for vertex in(0,4):
        s,t=polygon[vertex];r=(H.O,s,t)
        for q in qcases:
            if time.monotonic()>=deadline:raise TimeoutError('boundary control deadline incomplete')
            c=tuple(H.K.coerce(z)for z in q);d=H.M.dot(c,c);u=max(abs(z)for z in q)
            alpha,beta=(F(0),F(0))if not u else(F(1,10000),F(-1,7000))
            maximum=None
            for a,b,v,k in unique:
                p=data['points'][v];m=tuple(F(2)**k*z for z in H.M.cross(H.M.sub(data['points'][b],data['points'][a]),r));h=H.M.dot(m,p)
                A=H.transformed(p,c)
                cleared=H.M.dot(m,A)+(1+d)*(m[1]*alpha+m[2]*beta)-(1+d)*h
                torque=H.M.dot(H.M.cross(p,m),c)
                rhs=2*torque+(1+d)*(m[1]*alpha+m[2]*beta)-2*d*h+2*H.M.dot(m,c)*H.M.dot(p,c)
                require(cleared==rhs,'exact actual Cayley support polynomial including translation')
                identities+=1
                excess=cleared/(1+d)
                if maximum is None or H.sign(excess-maximum,root)>0:maximum=excess
            if not u:require(maximum==H.Z,'zero motion identical actual fit');zero+=1
            else:
                require(H.sign(maximum-2*rho*u,root)>0,'actual support normal norm<2 converts this to the stated physical gap')
                physical+=1
    return dict(status='EXACT_FRESH_PHYSICAL_SUPPORT_AND_TRANSLATION_CONTROLS_PASSED',
                full_named_geometry_rebuilt=True,closed_cell_geometry_record_matches=True,
                actual_cayley_translation_identities=identities,
                nonzero_actual_physical_gap_controls=physical,identical_zero_motion_fit_controls=zero)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--kind',choices=('algebra','geometry','physical'),required=True)
    p.add_argument('--seconds',type=float,default=45.);p.add_argument('--output',type=Path)
    args=p.parse_args();start=time.monotonic();deadline=start+args.seconds
    certificate=json.loads((C.HERE/'certificate.json').read_text());expected=json.loads((C.HERE/'expected.json').read_text())
    record={'algebra':algebra,'geometry':geometry,'physical':physical}[args.kind](certificate,expected,deadline)
    raw=(json.dumps(record,sort_keys=True,indent=2)+'\n').encode()
    if args.output:args.output.write_bytes(raw)
    print(json.dumps(dict(actual_agent='six-rupert-1',role='researcher',status=record['status'],
                          bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),elapsed_seconds=time.monotonic()-start,
                          peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,threads=1)))

if __name__=='__main__':main()
