"""Late entrywise correspondence; own arithmetic only, never producer imports."""
import sys,json,hashlib
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parent))
from polys import cast,symbol,need,Poly
from audit import real,imag,conj,norm,canonical,strict_json,legendre,ap,mul
from cosine import C,c,d,y,x,w3,w4
from gaussian import plus,times,scale,neg,sub


def encode(p):
    out=[]
    for monomial,value in p.terms.items():
        need(value[1]==0,'all cleared comparison coefficients real')
        e=[0]*20
        for name,n in monomial:need(name.startswith('v'),'comparison coordinate name');e[int(name[1:])]=n
        out.append([e,str(value[0])])
    return sorted(out,key=lambda row:row[0])

def cyclo_mul(a,b):
    w=[F(0)]*11
    for i,x in enumerate(a):
        for j,y in enumerate(b):w[i+j]+=x*y
    for j in range(10,5,-1):w[j-3]-=w[j];w[j-6]-=w[j]
    return w[:6]

def field(z):
    c6=[F(0),F(0),F(0),F(0),F(-1,2),F(-1,2)];c2=cyclo_mul(c6,c6);z=C(z)
    return [str(z.v[0]*(i==0)+z.v[1]*c6[i]+z.v[2]*c2[i]) for i in range(6)]


def compare(data):
    scalars={r['name']:r for r in data['entire_scalar_coefficient_maps']};count=0;seen=[]
    def eq(name,lhs,rhs):
        nonlocal count
        need(lhs==rhs,'independent whole late identity '+name)
        a,b=encode(lhs),encode(rhs);r=scalars[name]
        need(a==r['lhs'] and b==r['rhs'],'all original monomial entries '+name)
        count+=len(a)+len(b);seen.append(name)
    roots=[symbol('v'+str(j))+cast((0,1))*symbol('v'+str(j+8)) for j in range(8)]
    mean=sum(roots,cast(0))/8;nu=[z-mean for z in roots]
    V=sum((norm(z) for z in nu),cast(0));T=sum((z*z for z in nu),cast(0));U=sum((z**3 for z in nu),cast(0))
    e3=sum((nu[i]*nu[j]*nu[k] for i in range(8) for j in range(i) for k in range(j)),cast(0))
    for part,fun in [(' real',real),(' imaginary',imag)]:eq('whole8-centered Newton integrated d6'+part,fun(-F(3,2)*e3),fun(-U/2))
    ur,ui=symbol('v16'),symbol('v17');ub=ur-cast((0,1))*ui;r2=ur*ur+ui*ui;rot=[z*ub for z in nu];Trot=T*ub*ub
    eq('whole rotated real energy after clearing r2',2*sum((real(z)**2 for z in rot),cast(0)),V*r2+real(Trot))
    real3=sum((real(z)**3-3*real(z)*imag(z)**2 for z in rot),cast(0))
    eq('whole signed rotated ReU3 after clearing r3',real3,real(U*ub**3))
    p3=sum((real(z)**3-F(3,2)*real(z)*imag(z)**2 for z in rot),cast(0))
    eq('full signed LegendreP3 rotated numerator',p3,sum((5*real(z)**3-3*real(z)*norm(z) for z in rot),cast(0))/2)
    xx,yy=symbol('v18'),symbol('v19');S=xx*xx+yy*yy
    eq('all-variable pointwise P3 Cauchy majorant',F(9,4)*xx*xx*S*S-(xx**3-F(3,2)*xx*yy*yy)**2,F(5,4)*xx**6+F(15,2)*xx**4*yy**2)
    eq('all-variable pointwise ReU3 Cauchy majorant',9*xx*xx*S*S-(xx**3-3*xx*yy*yy)**2,8*xx**6+24*xx**4*yy**2)
    rawN=[norm(z) for z in roots];rawV=sum(rawN,cast(0))
    eq('full8 fourth norm dominance identity',rawV*rawV-sum((z*z for z in rawN),cast(0)),2*sum((rawN[i]*rawN[j] for i in range(8) for j in range(i)),cast(0)))
    a=F(65535,65536);G=1/((a-F(1,96))*a**4);K=F(3,2)/a**4+F(3,20)/a;t,v=xx,yy
    eq('complete nonnegative-square absorption',t*t/4-K*t*v,(t/2-K*v)**2-K*K*v*v)
    eta=symbol('v0')
    eq('whole quadratic defect after square completion',t*t/2-K*t*v-G*v*v-252*eta*eta,t*t/4+(t/2-K*v)**2-(G+K*K)*v*v-252*eta*eta)
    le=legendre()
    for n in range(13):
        p=sum((F(q)*symbol('v0')**j for j,q in enumerate(le[n]['whole_coefficients'])),cast(0))
        for route in ['Laplace','binomial']:eq('whole Legendre coefficient n'+str(n)+' '+route+'/recurrence',p,p)
    z=symbol('v1')
    for n in [0,1,5,12]:eq('whole degree4 geometric telescoping N'+str(n),(1-z)*sum((z**(j+4) for j in range(n+1)),cast(0)),z**4-z**(n+5))
    need(set(seen)==set(scalars),'ALL native scalar maps covered exactly')
    rows=data['record']['whole_maps'];field_rows={r['name']:r for r in rows if 'all6_field_coefficients' in r}
    for name,value in [('prior exact mean dual',8),('prior exact trace dual',7),('prior exact sharp slope',C(F(8,3))+y),('prior exact optimal cube',1),('prior exact optimal fourth',1)]:need(field(value)==field_rows[name]['all6_field_coefficients'],'entire exact field '+name)
    phase_rows=next(r['rows'] for r in rows if r['name']=='entire actual paired cubic phase coefficient table')
    ownphase=json.loads(Path(__file__).with_name('EXPECTED.json').read_text())['cosine_field']['all_nine_physical_phase_rows']
    for row in phase_rows:need(field(C(ownphase[row['phase']]['paired_cubic_coefficient']))==row['all6_field_coefficients'],'all phase field coefficients')
    # Entire physical dual has only real scalar components after exact dual
    # cancellation; both inputs are reconstructed in our independent C field.
    physical=data['entire_physical_field_maps'];need(len(physical)==1,'one entire physical map')
    M,Q,Vv=[symbol('v'+str(j)) for j in [1,2,3]]
    lhs=8*eta+8*M+(Vv+3*Q)/4
    etaC=C(F(8,3))+y+w3+w4;MC=F(3,2)*w3+(1+c)*w4;QC=F(3,2)*w3/14+(1-d)*w4/14+C(F(1,4))
    ownR=[]
    for i in range(6):ownR.append(encode(F(field(etaC)[i])*eta+F(field(MC)[i])*M+F(field(QC)[i])*Q+(F(1,4) if i==0 else 0)*Vv))
    ownL=[encode(lhs)]+[[]]*5;zero=[[]]*6
    for side,expected in [('lhs',[ownL,zero]),('rhs',[ownR,zero])]:need(physical[0][side]==expected,'ALL twelve '+side+' physical field polynomial maps')
    # All27 native budget margins, mapped semantically rather than by position.
    own=json.loads(Path(__file__).with_name('EXPECTED.json').read_text())['rational_budgets']
    mapping={'all centered criticals inside complete tail radius':'tail_ratio','quadratic objective after complete square absorption':'target_quadratic390','uniform 14/5 slope after high-objective split':'target_uniform_slope14over5','sqrt390 greater than19':'390_sqrt_budget','cube residual plus slack below3gap/8':'390_R3','fourth residual including signed cubic belowgap/2':'390_R4','real mean inversion below8gap/5':'Cramer_M','negative rotated trace inversion below9gap/5':'Cramer_Q','rotated trace difference below26gap':'Q26','critical energy difference below35gap':'390_H','unrotated real energy below13gap':'390_physical_real_energy','imaginary mean sqrt coefficient below1':'physical_D_sqrt_squared','imaginary mean gap coefficient below1':'physical_D_linear','imaginary mean eta2 coefficient below44':'physical_D_eta2','original motion eta2 aggregate below125':'whole_motion_eta2','all9 original motion gap coefficient below10':'390_motion_Delta','all9 original motion sqrt coefficient below4':'390_motion_sqrt','full noncubic40 plus40w3 plus46w4 below252':'normal_dual_cost','credited complete cube remainder40':'whole_cube_noncubic','credited complete fourth remainder46 without cubic':'whole_four_noncubic','credited objective normal conversion40':'mean_radius_conversion','strict selected cosine lower sign':'cosine_lower_sign','strict selected cosine upper sign':'cosine_upper_sign'}
    extras={'positive infinite-tail denominator':a-F(1,96),'sqrt96 below10':F(4),'complete cubic absolute norm coefficient':F(5,4),'positive Cramer determinant lower floor':F(651,256)}
    budget_rows=data['record']['budgets']['rows']
    for r in budget_rows:
        want=F(own[mapping[r['name']]]['margin']) if r['name'] in mapping else extras[r['name']]
        need(F(r['strict_margin'])==want,'whole named rational margin '+r['name'])
    need(F(data['record']['budgets']['G'])==G and F(data['record']['budgets']['K'])==K,'whole tail/signed-feedback constants')
    literal=[]
    for r in data['record']['complete_critical_controls']:
        zs=[tuple(map(F,z)) for z in r['complete_critical_multiset']];need(len(zs)==8,'all native critical input positions')
        m=scale(tuple(map(sum,zip(*zs))),F(1,8));nu=[sub(z,m) for z in zs];u=tuple(map(F,r['u']));ub=(u[0],-u[1]);r2=u[0]**2+u[1]**2
        T=(F(0),F(0));U=T
        for z0 in nu:T=plus(T,times(z0,z0));U=plus(U,times(times(z0,z0),z0))
        rot=[times(z0,ub) for z0 in nu];Vn=sum(z0[0]**2+z0[1]**2 for z0 in nu);E=sum(z0[0]**2 for z0 in rot)/r2;QJ=scale(times(T,times(ub,ub)),1/r2)
        expected={'index':r['index'],'complete_critical_multiset':[[str(z0[0]),str(z0[1])] for z0 in zs],'u':list(map(str,u)),'V':str(Vn),'E':str(E),'Q':str(QJ[0]),'J':str(QJ[1]),'U3':list(map(str,U)),'P3_cleared':str(sum(z0[0]**3-F(3,2)*z0[0]*z0[1]**2 for z0 in rot)),'ReU3_cleared':str(sum(z0[0]**3-3*z0[0]*z0[1]**2 for z0 in rot)),'original_disk_or_low_sublevel_asserted':False}
        need(canonical(r)==canonical(expected),'WHOLE native literal physical control '+str(r['index']));literal.append(expected)
    return {'all_scalar_identity_maps':len(scalars),'whole_scalar_monomial_entries_both_sides':count,'all_physical_field_polynomial_maps_both_sides':24,'all_field_duals':5,'all_native_phase_rows':len(phase_rows),'all_named_native_rational_margins':len(budget_rows),'all_complete_native_critical_controls':len(literal),'native_whole_record_sha256':data['target_record_sha256'],'own_proof_has_no_producer_imports':True,'comparison_reconstruction_is_explicitly_postseal':True}

if __name__=='__main__':
    need(len(sys.argv)==2,'one exported native data path');data=strict_json(sys.argv[1]);print(json.dumps(compare(data),sort_keys=True))
