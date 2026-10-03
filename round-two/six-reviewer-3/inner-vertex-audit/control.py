"""Literal rational geometry versus every primary compiled branch predicate.

Read-only profiling captures primary expressions without changing sealed code.
The known rational12-core is credited; no arbitrary-three packing is asserted.
"""
import hashlib,json,sys
from fractions import Fraction as F
from functools import lru_cache
from geometry import model,LABELS,CONTACTS
from census import CAPS,classify,PLANES
from gram import det,adj
from systems import generate

def check():
    t,z,w=F(29,50),F(5400,3973),F(454484658996081,225033203125000)
    @lru_cache(None)
    def ev(p):
        if p.op=='c':return F(p.args[0])
        if p.op=='t':return t
        if p.op=='z':return z
        if p.op=='+':return ev(p.args[0])+ev(p.args[1])
        if p.op=='-':return -ev(p.args[0])
        if p.op=='*':return ev(p.args[0])*ev(p.args[1])
        raise ValueError('unknown exact DAG operation')
    m=model();O=ev(m['Omega'])
    if O<=0 or w<=0 or w*w!=ev(m['R']):raise ValueError('signed original rational root/control')
    P={i:[(ev(v.p)+w*ev(v.q))/O for v in m['Y'][i]] for i in LABELS}
    def dot(u,v):return (1-t)*sum(x*y for x,y in zip(u,v))+t*sum(u)*sum(v)
    for i in LABELS:
        if dot(P[i],P[i])!=1:raise ValueError('actual original unit')
    gaps={str(i)+'_'+str(j):t-dot(P[i],P[j]) for k,i in enumerate(LABELS) for j in LABELS[k+1:]}
    if any(g<0 for g in gaps.values()) or any(gaps[str(i)+'_'+str(j)]!=0 for i,j in CONTACTS):raise ValueError('entire original66 packing/20 contact control')
    expected_base={}
    for i in LABELS:expected_base['unit_'+str(i)]=O*O*(dot(P[i],P[i])-1)
    for i,j in CONTACTS:expected_base['contact_'+str(i)+'_'+str(j)]=O*O*(dot(P[i],P[j])-t)
    expected_base.update({'positive_w':w,'strict_original_regularity':2*ev(m['G'])-ev(m['a'])**4*ev(m['C'])**2,
        't_lower':25*t-14,'t_upper':593-1000*t,'z_lower':5*z-6,'z_upper':7-5*z,'original_chart':1-(1-t)**2*z*z})
    for k,i in enumerate(LABELS):
        for j in LABELS[k+1:]:expected_base['packing_'+str(i)+'_'+str(j)]=O*O*gaps[str(i)+'_'+str(j)]
    normals=dict(P);thresholds={i:t for i in LABELS}
    for i,(normal,u) in CAPS.items():normals[i]=list(map(F,normal));thresholds[i]=F(u)
    expect={};geometry={}
    for row in classify():
        if row['case']!='residual':continue
        tri=tuple(row['triple']);A=[[dot(normals[i],normals[j]) for j in tri] for i in tri];D=det(A);B=adj(A);rhs=[thresholds[i] for i in tri]
        lam=[sum(B[k][l]*rhs[l] for l in range(3)) for k in range(3)];X=[sum(lam[k]*normals[tri[k]][j] for k in range(3)) for j in range(3)]
        q=sum(rhs[k]*lam[k] for k in range(3))
        vals={'regular_basis':O**6*D,'long_vertex':O**6*(q-D)}
        for j in PLANES:vals['closed_feasible_'+str(j)]=O**7*(thresholds[j]*D-dot(normals[j],X))
        expect[tri]=vals;geometry[tri]={'determinant':str(D),'norm_numerator':str(q),'closed_products':{str(j):str(thresholds[j]*D-dot(normals[j],X)) for j in PLANES}}
    captured={};count=0
    def profile(frame,event,arg):
        nonlocal count
        if event!='return' or frame.f_code.co_name!='root_record' or frame.f_globals.get('__name__')!='systems':return
        f=frame.f_locals;p=f['p'];tri=frame.f_back.f_locals.get('tri');key=None if tri is None else tuple(tri);name=f['name'];value=ev(p.p)+w*ev(p.q)
        if key not in captured:captured[key]={}
        if name in captured[key]:raise ValueError('duplicate captured original predicate')
        captured[key][name]=value;count+=1
    sys.setprofile(profile)
    try:compiled=generate()
    finally:sys.setprofile(None)
    if captured.pop(None)!=expected_base or captured!=expect:raise ValueError('ENTIRE compiled/scalar physical predicate mapping differs')
    if len(compiled['whole260_branches'])!=len(expect):raise ValueError('whole branch domain changed')
    full={str(list(k)):{n:str(v) for n,v in sorted(vals.items())} for k,vals in sorted(expect.items())}
    out={'credited_not_new':True,'parameters':[str(t),str(z),str(w)],'actual_units':12,'actual_pair_tests':66,'required_contacts':20,
        'entire_primary_compiled_predicates_checked':count,'whole260_physical_records':{str(list(k)):v for k,v in sorted(geometry.items())},
        'whole_all_branch_predicate_values_sha256':hashlib.sha256(json.dumps(full,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        'all_branches_exact_mapping':True,'root_macro_checked_separately':True,'arbitrary_three_realization_asserted':False}
    ev.cache_clear();return out

if __name__=='__main__':print(json.dumps(check(),sort_keys=True,separators=(',',':')))
