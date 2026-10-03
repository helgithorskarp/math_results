"""Current10109 untrusted literal factors bound to actual original geometry."""
import json,hashlib
from pathlib import Path
from digit import T,Z,expr,monomials,coefficients,prove_zero
from geometry import model,Radical,dot,cross
from census import classify,LABELS,CONTACTS,PAIRS,CAPS

def require(ok,msg):
    if not ok:raise ValueError(msg)

def decode(data,R):
    require(set(data)=={'schema_version','variable_order','coefficient_domain','rows'},'factor schema')
    require(data['schema_version']==1 and data['variable_order']==['t','z','w'] and data['coefficient_domain']=='Z','factor variables')
    require(set(data['rows'])=={'bound0','bound1','bound2','delta','C0','C4','C6','margin','bound2_square_factor','critical_norm99','R'},'factor names')
    out={}
    for name,rows in data['rows'].items():
        require(type(rows) is list and 0<len(rows)<=200,'factor rows')
        parts=[[],[]];seen=set()
        for row in rows:
            require(type(row) is list and len(row)==4,'row arity')
            i,j,k,v=row
            require(all(type(x) is int for x in [i,j,k]) and k in [0,1],'radical exponent')
            require(type(v) is str and len(v)<=30,'coefficient text')
            n=int(v);require(str(n)==v and n!=0,'canonical nonzero coefficient')
            require((i,j,k) not in seen,'duplicate literal');seen.add((i,j,k));parts[k].append((i,j,n))
        out[name]=Radical(monomials(parts[0]),monomials(parts[1]),R)
    for name in ['R','critical_norm99','bound2_square_factor']:require(not out[name].q.norm,'scalar factor')
    return out

def divide(p,d):
    require(d,'zero divisor');lead=max(d);lc=d[lead];rem=dict(p);out={}
    while rem:
        top=max(rem)
        require(all(top[k]>=lead[k] for k in range(2)),'nonzero complete polynomial remainder')
        v,r=divmod(rem[top],lc);require(r==0,'nonintegral quotient')
        power=(top[0]-lead[0],top[1]-lead[1]);out[power]=out.get(power,0)+v
        for (i,j),coef in d.items():
            k=(i+power[0],j+power[1]);n=rem.get(k,0)-v*coef
            if n:rem[k]=n
            else:rem.pop(k,None)
        if len(out)>1000:raise RuntimeError('fixed quotient resource guard; incomplete')
    return {k:v for k,v in out.items() if v}

def scope(s):
    require(s['t_interval']==['14/25','593/1000'] and s['z_interval']==['6/5','7/5'] and s['intervals_closed'] is True,'closed scope')
    require(s['required_labels']==list(LABELS) and s['original_contacts']==[list(p) for p in CONTACTS],'entire original scope')
    require(s['other_points']=='three_arbitrary_unit_points_with_all_pair_products_at_most_t' and s['extra_contacts_allowed'] is True,'arbitrary additions')
    require(s['normalization_imports']==[9774,9912] and s['sheet']==[-1,1] and s['root']=='w>0; w*w=R' and s['regularity']=='2G-a^4 C^2>0','actual imports/root')
    require(s['additional_hypotheses']==[] and s['global_bound_claimed'] is False and s['conclusion']=='necessary_260_regular_vertex_systems_only','conclusion scope')
    require(s['cap_planes']==[{'label':k,'normal':list(n),'rhs':v} for k,(n,v) in CAPS.items()],'actual caps')
    rows=classify();require(s['incompatible_pairs']==[list(p) for p in PAIRS] and s['all_low_A_triple']==[6,7,9] and s['critical_short_triple']==[4,7,99],'case domains')
    require(s['equilateral_short_triples']==[r['triple'] for r in rows if r['case']=='original_equilateral'],'every original contact clique')
    require(s['residual_triples']==[r['triple'] for r in rows if r['case']=='residual'],'EVERY actual residual triple')
    return rows

def compile(m,factors,system):
    t,z=T,Z;a,b,c,R,O=(m[k] for k in ['a','b','c','R','Omega']);Y=m['Y'];rows={};quotients={}
    def rad(name,p):
        rows[name+'_constant']=prove_zero(p.p);rows[name+'_linear']=prove_zero(p.q)
    def quotient(name,p,d):
        drows=coefficients(d);qs=[]
        for tag,raw in [('constant',p.p),('linear',p.q)]:
            q=divide(coefficients(raw),drows);quotients[name+'_'+tag]=[[i,j,v] for (i,j),v in sorted(q.items())]
            qs.append(monomials([(i,j,v) for (i,j),v in q.items()]))
        result=Radical(*qs,R);rad('complete_division_'+name,p-result*d);return result
    rows['literal_R']=prove_zero(factors['R'].p-R)
    F=a**5*c*(3*t-1)*(b*z+1)
    for j in range(3):rad('bound_coordinate_'+str(j),-Y[0][j]-2*Y[11][j]-factors['bound'+str(j)]*F)
    F0=a**6*c*(3*t-1)*(b*z+1);F6=a**4*c*(3*t-1)*(3*t+1)*(b*z+1)
    u0=[quotient('u0_'+str(j),Y[0][j],F0) for j in range(3)]
    u6=[quotient('u6_'+str(j),Y[6][j],F6) for j in range(3)]
    L0=quotient('L0',Radical(O,0,R),F0);L6=quotient('L6',Radical(O,0,R),F6)
    delta=u0[1]*u6[0]-u0[0]*u6[1]
    alpha=-2*u6[0]+13*u6[1];beta=2*u0[0]-13*u0[1]
    C0=L0*alpha;C6=L6*beta;C4=15*delta-alpha*u0[2]-beta*u6[2]
    margin=24*delta-(C0+C4+C6)*t
    for j,target in enumerate([-13,-2,15]):rad('physical_Cramer_'+str(j),C0*Y[0][j]+C4*Y[4][j]+C6*Y[6][j]-delta*O*target)
    Q=a*m['D']*z*z-2*m['D']*z+2*t*t-t+1
    positive={'a':a,'b':b,'c':c,'J':m['J'],'C':m['C'],'Q':Q,'3t+1':3*t+1,'bz+1':b*z+1}
    for name,p in [('delta',delta),('C0',C0),('C4',C4),('C6',C6),('margin',margin)]:
        factor=expr(1)
        for key in system['Farkas_positive_factors'][name]:
            require(key in positive,'unproved clearing factor');factor=factor*positive[key]
        rad('Farkas_binding_'+name,p-factors[name]*factor)
    # Direct scalar physical Gram, with ALL cofactor terms, no radical-field expansion.
    N12=[q.p for q in m['N'][12]];e=[expr(1),expr(0),expr(0)]
    cr=cross(N12,e);Lv=[v*c-sum(cr)*t for v in cr]
    d=a*a*m['C'];W=[(m['D']*z*z-1)*a*a*e[j]+2*t*N12[j]+2*b*z*Lv[j] for j in range(3)]
    for j in range(3):rad('original_W_numerator_'+str(j),Y[7][j]*d-O*W[j])
    rows['original_W_unit']=prove_zero(dot(W,W)-d*d)
    x=dot([expr(0),expr(0),expr(1)],W)
    y=dot(W,CAPS[99][0]);s=20-19*t;q=621-620*t
    det=(q-s*s)*d*d-q*x*x+2*s*x*y-y*y
    norm=t*t*((q*d*d-y*y)+(q-s*s)*d*d+2*(s*y*d-q*x*d))+225*(d*d-x*x)+30*t*(x*y-s*d*d+s*x*d-y*d)
    rows['critical_physical_Gram']=prove_zero(99*det-100*norm-factors['critical_norm99'].p)
    return m,rows,quotients,{'determinant_cleared':det,'norm_cleared':norm}

def main():
    raw=Path('FACTORS.json').read_bytes();system=json.loads(Path('SYSTEM.json').read_text());domain=scope(system)
    m=model();f=decode(json.loads(raw),m['R']);m,rows,quotients,critical=compile(m,f,system)
    out={'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','whole_identity_records':rows,'whole_integer_quotients':quotients,'whole364_case_rows':domain,'factor_sha256':hashlib.sha256(raw).hexdigest(),'untrusted_shared_literals_not_independently_rediscovered':True}
    print(json.dumps(out,sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
