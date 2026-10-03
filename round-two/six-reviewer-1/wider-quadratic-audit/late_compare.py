"""LATE data-only common comparison. Does not import producer source."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import argparse,json
from core import R,rv,K,P,variable,cosine,digest,require
from validate import equal,load

def decode(rows):
    d={}
    for powers,q in rows:
        require(len(powers)==20 and all(type(n)is int and n>=0 for n in powers),'complete producer monomial dimension')
        key=tuple(sorted('v'+str(j)for j,n in enumerate(powers)for _ in range(n)))
        require(key not in d,'duplicate producer monomial')
        d[key]=F(q)
    return R(d)

def add(*zs):return sum((z[0]for z in zs),R()),sum((z[1]for z in zs),R())
def sc(z,q):return z[0]*q,z[1]*q
def mul(z,w):return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]
def norm(z):return z[0]**2+z[1]**2
def pw(z,n):
    out=R(1),R()
    for _ in range(n):out=mul(out,z)
    return out

def complete_expected_maps(independent):
    """Definition-level full centered maps in a second monomial backend."""
    v=[rv('v'+str(j))for j in range(20)];expected={}
    def put(name,poly):require(name not in expected,'unique expected map');expected[name]=R(poly)
    roots=[(v[j],v[j+8])for j in range(8)]
    mean=sc(add(*roots),F(1,8));nu=[add(z,sc(mean,-1))for z in roots]
    V=sum((norm(z)for z in nu),R());T=add(*(pw(z,2)for z in nu));U=add(*(pw(z,3)for z in nu))
    # Integrated coefficient by full subset expansion, not producer e3 code.
    e3=add(*(mul(mul(nu[j],nu[k]),nu[l])for j in range(8)for k in range(j+1,8)for l in range(k+1,8)))
    for side,label in enumerate(['real','imaginary']):put('whole8-centered Newton integrated d6 '+label,-F(3,2)*e3[side])
    ub=v[16],-v[17];r2=v[16]**2+v[17]**2;rot=[mul(z,ub)for z in nu]
    put('whole rotated real energy after clearing r2',2*sum((z[0]**2 for z in rot),R()))
    put('whole signed rotated ReU3 after clearing r3',mul(U,pw(ub,3))[0])
    put('full signed LegendreP3 rotated numerator',sum((z[0]**3-F(3,2)*z[0]*z[1]**2 for z in rot),R()))
    X,Y=v[18],v[19];S=X*X+Y*Y
    put('all-variable pointwise P3 Cauchy majorant',F(5,4)*X**6+F(15,2)*X**4*Y**2)
    put('all-variable pointwise ReU3 Cauchy majorant',8*X**6+24*X**4*Y**2)
    ns=[norm(z)for z in roots]
    put('full8 fourth norm dominance identity',2*sum((ns[j]*ns[k]for j in range(8)for k in range(j+1,8)),R()))
    cn=[norm(z)for z in nu]
    for j in range(8):
        put('whole other-seven centered pair identity '+str(j),sum((norm(add(nu[k],sc(nu[l],-1)))for k in range(8)for l in range(k+1,8)if k!=j and l!=j),R()))
    put('whole centered quartic SOS credited9845',7*V*V-8*sum((z*z for z in cn),R()))
    G=F(independent['whole_arithmetic']['G']);Kc=F(independent['whole_arithmetic']['K'])
    t,w=X,Y;eta=v[0]
    put('complete nonnegative-square absorption',(t/2-Kc*w)**2-Kc*Kc*w*w)
    put('whole quadratic defect after square completion',t*t/2-Kc*t*w-G*w*w-190*eta*eta)
    put('whole unconditional square completion',(t-Kc*w)**2/2-(G+Kc*Kc/2)*w*w-190*eta*eta)
    t,w,z=v[0],v[1],v[2]
    put('whole retained broad mean square',4*(t-F(2,15)*w)**2-F(1216,225)*w*w)
    put('whole stronger paired mean square',4*(t-F(2,15)*w)**2-F(976,225)*w*w)
    e=F(independent['whole_arithmetic']['endpoint']);a=1-e;Kv=F(3,2)/a**4
    put('whole real-energy square in V5 bootstrap',F(5,14)*(z-F(7,5)*Kv*w)**2)
    q=v[3];eta=v[4]
    put('whole cube variance and real-energy decomposition',w/14+F(5,28)*(w+q))
    put('whole joint trace conic after12eta constraint',294*eta**2-24*(q+F(5,2)*eta)**2)
    av,eta,t2,V,q,ri,tail=v[:7]
    put('whole individual slack after objective substitution',eta-eta**2/2-F(15,16)*av**3*eta-F(3,4)*t2-F(3,64)*V-F(15,448)*q+F(3,64)*(1-av**3*ri)*(V+3*q)+F(3,16)*av**3*tail)
    # Restrict independent homogeneous Legendre maps to X=t,Y²=1-t².
    for row in independent['whole_Legendre_through_degree12']:
        n=row['degree'];p=R()
        for mon,q in row['whole_coefficients']:
            nx=mon.count('X');ny=mon.count('Y');require(ny%2==0 and nx+ny==n,'whole Legendre homogeneous shape')
            p+=F(q)*v[0]**nx*(1-v[0]**2)**(ny//2)
        for route in ['Laplace/recurrence','binomial/recurrence']:put('whole Legendre coefficient n'+str(n)+' '+route,p)
    for n in [0,1,5,12]:put('whole degree4 geometric telescoping N'+str(n),v[1]**4-v[1]**(n+5))
    return expected

def scalar_controls(rows):
    """All fields of every producer literal tuple, independently from definitions."""
    out=[]
    def addg(*zs):return sum((z[0]for z in zs),F()),sum((z[1]for z in zs),F())
    def sg(z,c):return z[0]*c,z[1]*c
    def mg(z,w):return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]
    def pg(z,n):
        s=F(1),F()
        for _ in range(n):s=mg(s,z)
        return s
    for row in rows:
        zs=[tuple(F(q)for q in z)for z in row['complete_critical_multiset']]
        require(len(zs)==8,'every producer critical multiplicity')
        mean=sg(addg(*zs),F(1,8));nu=[addg(z,sg(mean,-1))for z in zs]
        u=tuple(F(q)for q in row['u']);ub=u[0],-u[1];r2=sum(q*q for q in u)
        rot=[mg(z,ub)for z in nu];T=addg(*(pg(z,2)for z in nu));U=addg(*(pg(z,3)for z in nu))
        q,j=sg(mg(T,pg(ub,2)),1/r2);V=sum(x*x+y*y for x,y in nu);E=sum(x*x for x,y in rot)/r2
        p3=sum(x**3-F(3,2)*x*y*y for x,y in rot);real3=mg(U,pg(ub,3))[0]
        out.append({'index':row['index'],'complete_critical_multiset':[[str(x),str(y)]for x,y in zs],'u':[str(x)for x in u],'V':str(V),'E':str(E),'Q':str(q),'J':str(j),'U3':[str(x)for x in U],'P3_cleared':str(p3),'ReU3_cleared':str(real3),'original_disk_or_low_sublevel_asserted':False})
    return out

def compare(data,independent):
    maps=data['full_maps'];expected=complete_expected_maps(independent);seen=set();count=0;coefficients=0
    for row in maps:
        name=row['name'];require(name not in seen,'unique full producer map');seen.add(name)
        if row['kind']=='rational':
            require(name in expected,'covered complete producer rational map '+name)
            want=expected[name];left=decode(row['lhs']);right=decode(row['rhs'])
            require(left==want and right==want,'ENTIRE producer/independent coefficient map '+name)
            coefficients+=2*len(want.d);count+=1
        else:
            require(name=='complete physical defect before signed normal substitution','covered full field polynomial')
            eta,M,q,V=[rv('v'+str(j))for j in range(4)]
            want=8*eta+8*M+(V+3*q)/4
            zero=R()
            for side in ['lhs','rhs']:
                require(len(row[side])==2 and all(len(z)==6 for z in row[side]),'full twelve field maps')
                for j,z in enumerate(sum(row[side],[])):require(decode(z)==(want if j==0 else zero),'ENTIRE physical field map')
            coefficients+=2*len(want.d);count+=1
    require(set(expected)<=seen,'every independent expected common map covered')
    native=data['record'];whole=native['whole_maps'];special=0
    c=-cosine(4);d=2*c*c-1;y=1/(3*(1+c));x=K(F(2,3))-y;C=K(F(8,3))+y;w4=1/(c+d);w3=F(2,3)*(7-(1-d)*w4)
    dual={'prior exact mean dual':K(8),'prior exact trace dual':K(7),'prior exact sharp slope':C,'prior exact optimal cube':K(1),'prior exact optimal fourth':K(1)}
    for row in whole:
        if 'all6_field_coefficients'in row:
            equal(dual[row['name']].pack(),row['all6_field_coefficients']);special+=1
        if 'rows'in row:
            for item in row['rows']:
                k=item['phase'];equal(((cosine(3*k)-1)/18).pack(),item['all6_field_coefficients']);special+=1
    equal(scalar_controls(native['complete_critical_controls']),native['complete_critical_controls'])
    b=native['budgets'];r=independent['whole_arithmetic'];scalar_checks=[]
    correspond={'eta_endpoint':'endpoint','G':'G','K':'K','broad_pair_coefficient':'broad_pair','broad_individual_coefficient':'broad_individual','early_radius_floor':'early_radius','credited_kappa':'adopted_kappa','variance_error':'two_square_Bv'}
    for producer,own in correspond.items():equal(b[producer],r[own]);scalar_checks.append(producer)
    for producer,want in {'physical_error':'272','objective_error':'243','quartic_factor':'7/8','broad_energy':'1/375','broad_rho':'1/54','fine_rho':'1/160','fine_V_endpoint':'1/3200'}.items():equal(b[producer],want);scalar_checks.append(producer)
    a=1-F(r['endpoint']);tau=F(1,50)
    equal(b['variance_G'],str(1/((a-tau)*a**4)));equal(b['variance_K'],str(F(3,2)/a**4));scalar_checks+=['variance_G','variance_K']
    stages=[{'prior_V_cap':z['previous'],'tau':z['tau'],'new_V_cap':z['next'],'whole_divisor':z['divisor']}for z in r['whole_variance_bootstrap']]
    equal(stages,b['stages'])
    require(digest(native)==data['producer_whole_record_sha256'],'entire replay record digest AFTER independent common comparisons')
    # Native margin rows are replayed whole by capture_native, but differing
    # conservative constants are not represented as blanket common equality.
    return {'status':'PASS','agent':'six-reviewer-1','role':'independent mathematical reviewer','producer_whole_record_sha256':data['producer_whole_record_sha256'],'complete_common_maps':count,'whole_common_coefficient_entries':coefficients,'whole_special_field_rows':special,'every_literal_control_field':True,'literal_control_count':len(native['complete_critical_controls']),'complete_scalar_streams':len(scalar_checks),'whole_seven_bootstrap_rows':True,'independent_record_sha256':digest(independent),'trust':'LATE data-only check; no producer imports. Every captured whole map and special field row covered. Producer native107 margin rows/18 damages are replay validation; independent121 written-proof margins/13 math damages have their separate scope.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('export',type=Path);a=p.parse_args()
    data=load(a.export);independent=load(Path(__file__).with_name('EXPECTED.json'))
    print(json.dumps(compare(data,independent),sort_keys=True))

if __name__=='__main__':main()
