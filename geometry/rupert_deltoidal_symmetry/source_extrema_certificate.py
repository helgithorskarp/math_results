"""Exact sharp deltoidal source bounds by complete spherical critical strata.

Python3.11+ standard library. See source_extrema_proof.md.
"""
from pathlib import Path
from fractions import Fraction as F
from dataclasses import dataclass
from math import isqrt
from collections import Counter
import argparse,json,hashlib
from contextlib import contextmanager
ROOT=Path(__file__).parent
if not __debug__:raise RuntimeError('verification requires assertions; do not use python -O')
from verify import Q5,S,ZERO,vec,dot,cross,sub,mul,add
from area_polar_certificate import parse, audit_signs, pins as parent_pins
from global_area_certificate import check as check_parent, mm,mv,reflection,I,WALLS,QMIN
from orientation_certificate import build_cells, CHAMBER, determinant
from collections import deque
AREA_POLAR_SOURCE_SHA256='4486a75fc1206920979e4cb364f3044d9374992f5be16f5e64691cf5b8964f1b'

def pins():
    result=parent_pins()
    assert hashlib.sha256((ROOT/'area_polar_certificate.py').read_bytes()).hexdigest()==AREA_POLAR_SOURCE_SHA256
    return {**result,'area_polar_certificate.py':AREA_POLAR_SOURCE_SHA256}

@dataclass(frozen=True)
class Rad:
    a: Q5
    b: Q5
    d: Q5
    def __post_init__(self):
        assert self.d.sign()>=0
    def coerce(self,x):
        if isinstance(x,Rad):
            assert self.d==x.d
            return x
        return Rad(Q5.coerce(x),ZERO,self.d)
    def __add__(self,x):
        x=self.coerce(x);return Rad(self.a+x.a,self.b+x.b,self.d)
    __radd__=__add__
    def __neg__(self):return Rad(-self.a,-self.b,self.d)
    def __sub__(self,x):return self+-self.coerce(x)
    def __rsub__(self,x):return self.coerce(x)+-self
    def __mul__(self,x):
        x=self.coerce(x)
        return Rad(self.a*x.a+self.b*x.b*self.d,self.a*x.b+self.b*x.a,self.d)
    __rmul__=__mul__
    def sign(self):
        sa,sb,sd=self.a.sign(),self.b.sign(),self.d.sign()
        if sb==0 or sd==0:return sa
        if sa==0:return sb
        if sa==sb:return sa
        return sa*(self.a*self.a-self.b*self.b*self.d).sign()
    def serial(self):return {'a':str(self.a),'b':str(self.b),'radicand':str(self.d)}

def rdot(a,n):return sum((n[i]*a[i] for i in range(3)),0)
def candidate(A,B,D):return tuple(Rad(a,b,D) for a,b in zip(A,B))
def normalized(B,sgn=1):return candidate(vec((0,0,0)),mul(sgn,B),1/dot(B,B))
def compare(x,y):
    # Compare across different radicands without assuming irreducibility.
    # x-y=(x.a-y.a)+x.b*sqrt(x.d)-y.b*sqrt(y.d).
    left=Rad(x.a-y.a,x.b,x.d)
    sl=left.sign();sr=-(y.b.sign()*y.d.sign())
    if sl==0:return sr
    if sr==0 or sl==sr:return sl
    return sl*(left*left-y.b*y.b*y.d).sign()

def sqrti(x,bits):
    assert x>=0
    scale=1<<bits
    lo=isqrt(x.numerator*scale*scale//x.denominator)
    return F(lo,scale),F(lo+1,scale)
def qinterval(x,bits):
    lo,hi=sqrti(F(5),bits)
    return (x.a+x.b*lo,x.a+x.b*hi) if x.b>=0 else (x.a+x.b*hi,x.a+x.b*lo)
def interval(x,bits=96):
    aa=qinterval(x.a,bits);bb=qinterval(x.b,bits)
    if x.d==ZERO:return aa
    dl,dh=qinterval(x.d,bits)
    assert dh>=0
    rl=sqrti(max(dl,F(0)),bits)[0];rh=sqrti(dh,bits)[1]
    products=[b*r for b in bb for r in (rl,rh)]
    return aa[0]+min(products),aa[1]+max(products)

@contextmanager
def audit_radicals():
    """Independent rational enclosures for nonzero radical and comparison signs.

    Zero signs are checked by the exact squared identity and opposite branches;
    a nonzero expression must separate by rational bounds. No search guard changes.
    """
    original=Rad.sign;cache={}
    record={'sign_calls':0,'distinct_values':0,'zero_identity_checks':0,'maximum_binary_bits':0}
    def checked(x):
        record['sign_calls']+=1;actual=original(x)
        if x not in cache:
            bits=0
            if actual==0:
                if x.d==ZERO or x.b==ZERO:assert x.a==ZERO
                else:
                    assert x.a.sign()==-x.b.sign()!=0
                    assert x.a*x.a==x.b*x.b*x.d
                verified=0;record['zero_identity_checks']+=1
            else:
                bits=32
                while True:
                    assert bits<=1024,'radical audit exceeded declared precision cap'
                    lo,hi=interval(x,bits)
                    if lo>0:verified=1;break
                    if hi<0:verified=-1;break
                    bits*=2
            assert actual==verified,'radical sign disagrees with independent enclosure'
            cache[x]=verified;record['distinct_values']+=1
            record['maximum_binary_bits']=max(record['maximum_binary_bits'],bits)
        assert cache[x]==actual
        return actual
    Rad.sign=checked
    try:yield record
    finally:Rad.sign=original

def structure(P):
    cells,_=build_cells();nodes=sorted(set(u for p in cells for u in p))
    assert len(cells)==12 and len(nodes)==14
    assert [r['cell'] for r in P['cell_certificates']]==list(range(12))
    assert [r['index'] for r in P['corner_areas']]==list(range(14))
    assert [vec(map(parse,r['ray'])) for r in P['corner_areas']]==nodes
    for actual,row in zip(cells,P['cell_certificates']):
        assert [nodes[i] for i in row['corner_indices']]==actual
        assert len(actual) in (3,4)
        for i,u in enumerate(actual):
            assert determinant(u,actual[(i+1)%len(actual)],actual[(i+2)%len(actual)]).sign()>0
    return cells,nodes

def nearest_axis():
    pins();P=json.loads((ROOT/'expected_global_area.json').read_text())
    cells,N=structure(P);M=N[9]
    walls=[reflection(w) for w in WALLS]
    group={I};pending=deque([I])
    generators=[mm(walls[0],walls[1]),mm(walls[1],walls[2])]
    while pending:
        g=pending.popleft()
        for h in generators:
            x=mm(h,g)
            if x not in group:
                group.add(x);pending.append(x);assert len(group)<=60
    assert len(group)==60 and mv(walls[2],M)==M
    orbit={mv(g,M) for g in group};assert len(orbit)==60 and mul(-1,M) in orbit
    full=set(group)|{mm(walls[2],g) for g in group}
    assert len(full)==120 and {mv(g,M) for g in full}==orbit
    assert all(mm(w,g) in full for w in walls for g in full)
    values=[dot(sub(M,v),u) for v in sorted(orbit) for u in CHAMBER]
    assert len(values)==180 and all(x.sign()>=0 for x in values)
    return {'proper_group_count':60,'full_reflection_group_count':120,'directed_minimum_axes':60,
        'chamber_nearest_axis_corner_comparisons':180,'wall_reflection_fixes_M':True,
        'comparison_sha256':hashlib.sha256(json.dumps(list(map(str,values)),separators=(',',':')).encode()).hexdigest()}

def certify(T,a):
    P=json.loads((ROOT/'expected_global_area.json').read_text())
    structure(P)
    N=[vec(map(parse,row['ray'])) for row in P['corner_areas']]
    M=N[9];M2=dot(M,M);assert M==vec(((3*S-5)/6,(S-1)/6,1))
    threshold=(1-a*a/2)**2*M2
    rows=[];allcandidates=[];counts=Counter();minimum=None
    for row in P['cell_certificates']:
        ci=row['cell'];corners=[N[j] for j in row['corner_indices']]
        C=vec(map(parse,row['area_vector']));C2=dot(C,C)
        E=[cross(u,corners[(i+1)%len(corners)]) for i,u in enumerate(corners)]
        assert all(dot(e,e).sign()>0 for e in E)
        assert all(dot(e,u).sign()>=0 for e in E for u in corners)
        assert all(dot(M,u).sign()>0 and u[2].sign()>0 for u in corners)
        candidates=[]
        def put(kind,edge,n,active_area=False,active_edge=False):
            nonlocal minimum
            assert sum((x*x for x in n),0).sign()==1
            assert (sum((x*x for x in n),0)-1).sign()==0
            if active_area:assert (rdot(C,n)-T).sign()==0
            if active_edge:assert rdot(E[edge],n).sign()==0
            cone=[rdot(e,n).sign() for e in E]
            feasible=n[2].sign()>0 and all(s>=0 for s in cone) and (rdot(C,n)-T).sign()<=0
            counts['generated']+=1;counts[kind]+=1
            rec={'kind':kind,'edge':edge,'direction':[x.serial() for x in n],'feasible':feasible,'cone_signs':cone}
            if feasible:
                counts['feasible']+=1
                f=rdot(M,n);assert f.sign()>0
                margin=f*f-threshold
                rec.update(cap_margin=margin.serial(),cap_margin_sign=margin.sign(),objective=f.serial())
                if margin.sign()<=0:counts['failed_cap']+=1
                lo,hi=interval(f)
                if minimum is None or compare(f,minimum[4])<0:minimum=(hi,ci,kind,edge,f,n)
                allcandidates.append((ci,kind,edge,n,f,margin))
            candidates.append(rec)
        for i,u in enumerate(corners):put('corner',i,normalized(u))
        for sign in (-1,1):put('sphere_stationary',None,normalized(M,sign))
        proj=sub(M,mul(dot(M,C)/C2,C));proj2=dot(proj,proj)
        assert proj2.sign()>0,'actual cell must have nonconstant area-circle objective'
        radius2=1-T*T/C2
        if radius2.sign()>=0:
            A=mul(T/C2,C);D=radius2/proj2
            for sign in (-1,1):put('area_stationary',None,candidate(A,mul(sign,proj),D),True)
        for i,e in enumerate(E):
            e2=dot(e,e);me=sub(M,mul(dot(M,e)/e2,e));me2=dot(me,me)
            assert me2.sign()>0,'actual edge must have nonconstant objective'
            for sign in (-1,1):put('edge_stationary',i,normalized(me,sign),False,True)
            cp=sub(C,mul(dot(C,e)/e2,e));cp2=dot(cp,cp)
            assert cp2.sign()>0,'positive-area edge cannot have zero projected area vector'
            r2=1-T*T/cp2
            if r2.sign()>=0:
                B=cross(e,cp);assert dot(B,B).sign()>0
                A=mul(T/cp2,cp);D=r2/dot(B,B)
                for sign in (-1,1):put('area_edge_intersection',i,candidate(A,mul(sign,B),D),True,True)
        rows.append({'cell':ci,'corners':row['corner_indices'],'area_vector':list(map(str,C)),
            'area_sphere_radius_squared':str(radius2),'area_objective_projected_norm_squared':str(proj2),'candidates':candidates})
    assert minimum
    assert not counts['failed_cap'],'false proposed strict source cap'
    upper,ci,kind,edge,f,n=minimum
    comparisons=[compare(item[4],f) for item in allcandidates]
    assert all(s>=0 for s in comparisons)
    tied=[item for item,s in zip(allcandidates,comparisons) if s==0]
    for item in tied:
        assert all(compare(x,y)==0 for x,y in zip(n,item[3])), 'possible distinct maximizing directions'
    qlo,qhi=qinterval(M2,128);ml,mh=sqrti(qlo,128)[0],sqrti(qhi,128)[1]
    fl,fh=interval(f,128);coslo,coshi=fl/mh,fh/ml
    chordlo,chordhi=sqrti(2-2*coshi,96)[0],sqrti(2-2*coslo,96)[1]
    out={'agent':'six-rupert-1','role':'researcher','global_Rupert_property':'OPEN','area_budget':str(T),'source_chord':str(a),
        'counts':dict(counts),'minimum_comparisons':{str(k):v for k,v in Counter(comparisons).items()},
        'minimum_occurrences':[[i,j,k] for i,j,k,*_ in tied],
        'candidate_record_sha256':hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest(),
        'cell_candidate_counts':[{'cell':row['cell'],'generated':len(row['candidates']),'feasible':sum(c['feasible'] for c in row['candidates'])} for row in rows],
        'sharp_minimum_witness':{'cell':ci,'kind':kind,'edge':edge,'objective':f.serial(),
        'direction':[x.serial() for x in n],'chord_rational_enclosure':[str(chordlo),str(chordhi)]},
        'unit_norm_and_active_constraints_checked':counts['generated']}
    return out

def receiver_budget(scale,T):
    P=json.loads((ROOT/'expected_global_area.json').read_text())
    N=[vec(map(parse,r['ray'])) for r in P['corner_areas']]
    M=N[9];W=vec(((75-17*S)/114,(7+5*S)/114,1))
    C=vec(map(parse,P['cell_certificates'][9]['area_vector']))
    tri=[M,add(M,mul(scale,sub(W,M))),add(M,mul(scale,sub(N[10],M)))]
    cell=[N[i] for i in P['cell_certificates'][9]['corner_indices']]
    sides=[cross(u,cell[(i+1)%len(cell)]) for i,u in enumerate(cell)]
    assert all(dot(e,u).sign()>=0 for e in sides for u in tri)
    assert determinant(*tri).sign()!=0
    values=[dot(C,u)**2/dot(u,u) for u in tri];labels=['corner0','corner1','corner2']
    edges=[]
    for i,(a,b) in enumerate(zip(tri,tri[1:]+tri[:1])):
        aa,bb,ab=dot(a,a),dot(b,b),dot(a,b);ca,cb=dot(C,a),dot(C,b)
        det=aa*bb-ab*ab;assert det.sign()>0
        alpha=(ca*bb-cb*ab)/det;beta=(cb*aa-ca*ab)/det
        included=alpha.sign()>0 and beta.sign()>0
        edges.append({'edge':i,'included':included,'alpha':str(alpha),'beta':str(beta)})
        if included:
            p=add(mul(alpha,a),mul(beta,b));values.append(dot(p,p));labels.append('edge'+str(i))
    sign=determinant(*tri).sign()
    inside=all((dot(cross(a,b),C)*sign).sign()>0 for a,b in zip(tri,tri[1:]+tri[:1]))
    if inside:values.append(dot(C,C));labels.append('interior')
    q=max(values);assert Q5(T*T)>q
    assert Q5((T-F(1,10**6))**2)<=q
    assert F(1007,1000)**2*QMIN>Q5(T*T)
    return {'receiver_scale':str(scale),'rays':[list(map(str,u)) for u in tri],
        'area_squared_maximum':str(q),'active_strata':[label for label,v in zip(labels,values) if v==q],
        'edge_stationary_parameters':edges,'interior_stationary_included':inside,
        'strict_area_upper':str(T),'scale_squared_strict_upper':'1007/1000',
        'no_receiving_exclusion_claimed':True}

def sharp_window(out,lower,upper):
    record=out['sharp_minimum_witness']['objective']
    f=Rad(parse(record['a']),parse(record['b']),parse(record['radicand']))
    M=vec(((3*S-5)/6,(S-1)/6,1));M2=dot(M,M)
    assert f.sign()>0 and 0<lower<upper<1
    lower_margin=-(f*f-(1-lower*lower/2)**2*M2)
    upper_margin=f*f-(1-upper*upper/2)**2*M2
    assert lower_margin.sign()>0 and upper_margin.sign()>0
    out['sharp_chord_strict_window']=[str(lower),str(upper)]
    out['sharp_chord_window_squared_margins']=[lower_margin.serial(),upper_margin.serial()]
    out['unique_farthest_direction_in_closed_chamber']=True

def reject(name,job,records):
    try:job()
    except (AssertionError,ZeroDivisionError):records.append(name)
    else:raise AssertionError('malformed control accepted: '+name)

def controls():
    records=[];M=vec(((3*S-5)/6,(S-1)/6,1))
    reject('negative radical',lambda:Rad(ZERO,Q5(1),Q5(-1)),records)
    reject('zero direction normalization',lambda:normalized(vec((0,0,0))),records)
    reject('incompatible single-radical arithmetic',lambda:Rad(ZERO,Q5(1),Q5(2))+Rad(ZERO,Q5(1),Q5(3)),records)
    def wrong_norm():assert (rdot(M,normalized(M))-Q5(1)).sign()==0
    reject('raw direction confused with unit objective',wrong_norm,records)
    P=json.loads((ROOT/'expected_global_area.json').read_text())
    def missing_cell():
        bad=dict(P);bad['cell_certificates']=P['cell_certificates'][:-1];structure(bad)
    reject('missing closed cell',missing_cell,records)
    def reversed_cell():
        bad=dict(P);bad['cell_certificates']=[dict(r) for r in P['cell_certificates']]
        bad['cell_certificates'][0]['corner_indices']=list(reversed(bad['cell_certificates'][0]['corner_indices']))
        structure(bad)
    reject('reversed cell orientation',reversed_cell,records)
    reject('false strict source radius96537/1000000',lambda:certify(F(14803427,10**6),F(96537,10**6)),records)
    reject('false strict source radius105135/1000000',lambda:certify(F(7409521,500000),F(105135,10**6)),records)
    return records

def arithmetic_degeneracies():
    cases=[(Rad(Q5(1),Q5(-1),Q5(1)),0),(Rad(S,Q5(-1),Q5(5)),0),
        (Rad(Q5(-1),Q5(1),Q5(1)),0),(Rad(Q5(3),Q5(7),ZERO),1),
        (Rad(ZERO,Q5(-1),Q5(2)),-1),(Rad(Q5(2),Q5(-1),Q5(2)),1),
        (Rad(Q5(1),Q5(-1),Q5(2)),-1)]
    assert all(x.sign()==sign for x,sign in cases)
    assert compare(Rad(ZERO,Q5(1),Q5(5)),Rad(S,ZERO,ZERO))==0
    assert compare(Rad(Q5(1),Q5(1),Q5(2)),Rad(Q5(2),Q5(1),Q5(3)))<0
    assert compare(Rad(Q5(2),Q5(1),Q5(3)),Rad(Q5(1),Q5(1),Q5(2)))>0
    return {'sign_cases':len(cases),'cross_radical_comparison_cases':3,'reducible_and_zero_radicands_checked':True}

def check():
    out={'agent':'six-rupert-1','role':'researcher','proof_status':'exact finite hypotheses plus written continuous proof; unformalized and independently unreviewed',
        'global_Rupert_property':'OPEN','nearest_axis':nearest_axis(),'arithmetic_degeneracies':arithmetic_degeneracies()}
    budgets=[]
    for scale,T,lower,upper in ((F(2,3),F(14803427,10**6),F(96537,10**6),F(96538,10**6)),
        (F(1),F(7409521,500000),F(105135,10**6),F(105136,10**6))):
        b=certify(T,upper);sharp_window(b,lower,upper);b['receiver']=receiver_budget(scale,T);budgets.append(b)
    out['budgets']=budgets;out['malformed_controls_rejected']=controls()
    return out

def prerequisites():
    checked=pins();expected=json.loads((ROOT/'expected_global_area.json').read_text())
    expected.pop('malformed_controls_rejected',None)
    actual=check_parent();assert actual==expected
    return {'agent':'six-rupert-1','role':'researcher','all_parent_fields_matched':True,
        'parent_support_comparisons':actual['whole_cell_support_comparisons'],
        'parent_physical_area_checks':actual['shoelace_Jacobian_area_comparisons'],'pins':checked}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--prerequisites',action='store_true')
    args=parser.parse_args()
    if args.prerequisites:result=prerequisites()
    else:
        with audit_signs() as q5_audit,audit_radicals() as radical_audit:result=check()
        result['independent_Q5_sign_audits']=q5_audit
        result['independent_radical_sign_audits']=radical_audit
        expected=json.loads((ROOT/'expected_source_extrema.json').read_text())
        assert result==expected,'complete expected output mismatch'
    print(json.dumps(result,indent=2))
