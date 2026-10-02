#!/usr/bin/env python3
"""Exact normalizer/linearization and complex s=0 rank exclusion.
Actual six-sendov-2, researcher. Same-author9550 arithmetic is credited;
this is not independent review or proof-assistant formalization.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse, hashlib, importlib.util, json

PARENT_COMMIT='cb4cf7d9d83f3d376d3763b65cbe2fddd50637f4'
PARENT_FILES={'verify.py':'793731739751b6aa21213932a371d3985a5b69f010604017d1a1695fce478deb',
              'expected.json':'37efc29f52d2ddb4efb91fcd3f5c9e69a2f4d96a4e12adf797e6bbb74a760f96'}
PARENT_RECORD='c808d09b1f60281d10a76384306b974d8bf94d3647fa037fcf01dd23a76c023c'

def require(condition,message):
    if not condition:raise ValueError(message)

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()

def same_typed(a,b):
    if type(a)is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys()and all(same_typed(a[k],b[k])for k in a)
    if isinstance(a,list):return len(a)==len(b)and all(same_typed(x,y)for x,y in zip(a,b))
    return a==b

class Capture:
    def write_text(self,text):self.data=json.loads(text)

def parent_input():
    directory=Path(__file__).resolve().parent.parent/'degree-five-triangular'
    for name,digest in PARENT_FILES.items():
        require(hashlib.sha256((directory/name).read_bytes()).hexdigest()==digest,'pinned9550 source '+name)
    spec=importlib.util.spec_from_file_location('sendov_9550_input',directory/'verify.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    capture=Capture();record=module.make_certificate(capture)
    require(same_typed(record,json.loads((directory/'expected.json').read_text())),'whole pinned9550 fixture')
    require(hashlib.sha256(canonical(record)).hexdigest()==PARENT_RECORD,'whole pinned9550 record')
    return module,capture.data

def trim(a):
    a=[F(x)for x in a]
    while len(a)>1 and a[-1]==0:a.pop()
    return a

def add(a,b):
    return trim([(a[i]if i<len(a)else 0)+(b[i]if i<len(b)else 0)for i in range(max(len(a),len(b)))])

def scale(c,a):return trim([c*x for x in a])

def mul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return trim(out)

def div(a,b):
    a,b=trim(a),trim(b);require(b!=[0],'nonzero univariate divisor')
    q=[F(0)]*max(1,len(a)-len(b)+1)
    while a!=[0]and len(a)>=len(b):
        k,c=len(a)-len(b),a[-1]/b[-1];q[k]+=c
        a=add(a,[F(0)]*k+scale(-c,b))
    return trim(q),a

def unit(a,b):
    a0,a1=trim(a),trim(b);u0,u1=[F(1)],[F(0)];v0,v1=[F(0)],[F(1)]
    while a1!=[0]:
        q,rest=div(a0,a1);a0,a1=a1,rest
        u0,u1=u1,add(u0,scale(-1,mul(q,u1)))
        v0,v1=v1,add(v0,scale(-1,mul(q,v1)))
    require(len(a0)==1 and a0[0]!=0,'exact relatively prime slice pair')
    u,v=scale(1/a0[0],u0),scale(1/a0[0],v0)
    require(add(mul(u,a),mul(v,b))==[1],'whole rational unit multiplication')
    return {'left':[str(x)for x in a],'right':[str(x)for x in b],
            'left_multiplier':[str(x)for x in u],'right_multiplier':[str(x)for x in v],'identity':['1']}

def finite_unit(cert,prime=13):
    vals=[F(x)for name in ['left','right','left_multiplier','right_multiplier']for x in cert[name]]
    require(all(v.denominator%prime for v in vals),'unit denominators nonzero modulo prime')
    convert=lambda a:[(F(v).numerator%prime)*pow(F(v).denominator%prime,-1,prime)%prime for v in a]
    a,b,u,v=[convert(cert[name])for name in ['left','right','left_multiplier','right_multiplier']]
    require(a[-1]!=0 and b[-1]!=0,'slice degrees preserved modulo prime')
    product=trim([int(x)%prime for x in add(mul(u,a),mul(v,b))])
    require(product==[1],'whole finite-field unit')
    return {'prime':prime,'left':a,'right':b,'left_multiplier':u,'right_multiplier':v,'identity':[1],
            'both_leading_coefficients_nonzero':True}

def gram_gate(a,b,alpha,beta,damage=None):
    a,b=[F(x)for x in a],[F(x)for x in b];alpha,beta=F(alpha),F(beta)
    S=sum(x*x for x in a);T=sum(x*y for x,y in zip(a,b));U=sum(y*y for y in b)
    if S==0:
        if U!=0:return {'positive_root':damage=='ignore_zero_slope','branch':'no_finite_root'}
        yes=alpha<0 or(alpha==0 and beta<0)or(alpha>0 and beta<0 and beta*beta>=4*alpha)
        return {'positive_root':yes,'branch':'rank1_scalar'}
    yes=(damage=='drop_gram'or S*U==T*T)and(damage=='drop_positive'or T<0)
    yes=yes and(damage=='drop_quadratic'or alpha*T*T-beta*T*S+S*S==0)
    out={'positive_root':yes,'branch':'rank2_or_no_root','S':str(S),'T':str(T),'U':str(U)}
    if yes:
        t=-T/S;out['root']=str(t)
        if damage is None:require(all(x*t+y==0 for x,y in zip(a,b))and alpha*t*t+beta*t+1==0,'entire linear/scalar root control')
    return out

def controls(damage=None):
    cases=[
      ('unique_positive',[1,2,0,0,0],[-2,-4,0,0,0],0,F(-1,2),True),
      ('negative_root',[1,2,0,0,0],[2,4,0,0,0],0,F(1,2),False),
      ('zero_root',[1,0,0,0,0],[0,0,0,0,0],0,0,False),
      ('nonproportional',[1,0,0,0,0],[-2,1,0,0,0],0,F(-1,2),False),
      ('wrong_scalar',[1,0,0,0,0],[-2,0,0,0,0],0,1,False),
      ('constant_linear_vector',[0]*5,[1,0,0,0,0],-1,0,False),
      ('scalar_negative_leading',[0]*5,[0]*5,-1,3,True),
      ('scalar_two_positive',[0]*5,[0]*5,2,-3,True),
      ('scalar_double_positive',[0]*5,[0]*5,1,-2,True),
      ('scalar_irrational_positive',[0]*5,[0]*5,1,-3,True),
      ('scalar_negative_only',[0]*5,[0]*5,1,3,False),
      ('scalar_nonreal',[0]*5,[0]*5,1,0,False),
      ('scalar_linear_positive',[0]*5,[0]*5,0,-1,True),
      ('scalar_linear_negative',[0]*5,[0]*5,0,1,False),
      ('scalar_nonzero_constant',[0]*5,[0]*5,0,0,False)]
    out=[]
    for name,a,b,alpha,beta,expected in cases:
        value=gram_gate(a,b,alpha,beta,damage)
        require(value['positive_root']==expected,'Gram/scalar control '+name)
        out.append({'name':name,'a':[str(x)for x in a],'b':[str(x)for x in b],
                    'alpha':str(alpha),'beta':str(beta),'result':value})
    return out

def certificate(export=None):
    k,data=parent_input();P=k.P
    B,E,r,s,t=[k.variable(i)for i in range(5)]
    def decode(a):
        require(all(len(key)==5 and all(type(e)is int and e>=0 for e in key)and key[4]==0 for key,c in a),'matrix ordinary coefficient domain')
        return P({tuple(key+[0]*5):F(c)for key,c in a})
    M=[[decode(a)for a in row]for row in data['matrix_rows_ABC']]
    A,L,C=[[row[j]for row in M]for j in range(3)]
    checks={}
    def eq(name,a,b=0):
        require(P(a)==P(b),'universal '+name);checks[name]=True
    cexpr=[F(-160,3)*(28*r-21*s*s+12),
       F(8,15)*(288*B+2800*r*s-2100*s**3+1245*s),
       F(8,45)*(-432*B*s+2800*r*r-6300*r*s*s+2250*r+3150*s**4-2655*s*s+450),
       -96*s,F(-8,3)*(40*r-39*s*s+12)]
    for i in range(5):eq('constant_column'+str(i),C[i],cexpr[i])
    w=[P(F(-1,192)),P(0),P(0),F(7,384)*s,P(F(7,96))]
    dot=lambda a,b:sum((x*y for x,y in zip(a,b)),P(0))
    eq('polynomial_constant_column_unit',dot(w,C),1)
    eq('strict_real_reference_constant',C[0]-14*C[4],-48*(7*s*s+4))
    alpha,beta=dot(w,A),dot(w,L)
    a=[A[i]-C[i]*alpha for i in range(5)];b=[L[i]-C[i]*beta for i in range(5)]
    eq('weighted_linear_slope',dot(w,a));eq('weighted_linear_constant',dot(w,b))
    Q=alpha*t*t+beta*t+1
    for i in range(5):eq('entire_linearization_row'+str(i),t*(a[i]*t+b[i])+C[i]*Q,A[i]*t*t+L[i]*t+C[i])
    # Rank1 alone implies a=b=0; b3 has a globally nonzero REAL E pivot.
    eq('rank1_E_pivot',k.diffvar(b[3],1),F(-44,7)*(49*s*s+2))
    R=924672*B*r*s-848736*B*s**3+302976*B*s+3849440*r*r*s*s+219520*r*r
    R+=-4602080*r*s**4+2603440*r*s*s+146880*r+1286250*s**6-1694385*s**4+403500*s*s+22860
    eq('entire_rank1_E_equation',-3360*b[3],21120*(49*s*s+2)*E+R)
    # Exact s0 complex-rank slice, with no original feasibility assumptions.
    e0=F(-1,2112)*(10976*r*r+7344*r+1143)
    az=[k.sub(k.sub(x,3,0),1,e0)for x in a]
    bz=[k.sub(k.sub(x,3,0),1,e0)for x in b]
    qexpr=24080*r*r+16296*r+2727;hexpr=5488*r*r+7280*r+1875
    eq('s0_rank1_E_equation',k.sub(b[3],3,0),F(-44,7)*(2*E+F(1,1056)*(10976*r*r+7344*r+1143)))
    eq('s0_b0_BQ',bz[0],F(-8,45)*B*qexpr)
    eq('s0_a3_BH',az[3],F(-3,34496)*B*hexpr)
    p=[157599,1459368,4606896,4934272]
    pexpr=sum((F(c)*r**i for i,c in enumerate(p)),P(0))
    eq('s0_B0_b1_cubic',k.sub(bz[1],0,0),F(-1,9504)*pexpr)
    a0=k.sub(az[0],0,0)
    a0_coeff=[k.scalar(x)for x in k.coefficients(a0,2)]
    primitive=k.primitive_integer(a0_coeff)
    normalized=[int(x)for x in primitive]
    require(all(F(x).denominator==1 for x in primitive),'primitive integer quintic')
    quintic=sum((F(c)*r**i for i,c in enumerate(normalized)),P(0))
    leading_ratio=a0_coeff[-1]/F(normalized[-1])
    eq('s0_B0_a0_quintic',a0,leading_ratio*quintic)
    units={'Bnonzero':unit([2727,16296,24080],[1875,7280,5488]),
           'Bzero':unit(p,normalized)}
    finite={name:finite_unit(cert)for name,cert in units.items()}
    # Independent-indeterminate Lagrange identity; NOT expanded at actual parameters.
    ga=[k.variable(i)for i in range(5)];gb=[k.variable(i)for i in range(5,10)]
    S,T,U=dot(ga,ga),dot(ga,gb),dot(gb,gb)
    minors=[ga[i]*gb[j]-ga[j]*gb[i]for i in range(5)for j in range(i+1,5)]
    eq('universal_Gram_sum_of_ten_squares',S*U-T*T,sum((x*x for x in minors),P(0)))
    # Outer variable is a separate formal scalar; check ALL three coefficients.
    require([S*U,2*S*T,S*S]==k.ua(k.um([T,S],[T,S]),[S*U-T*T]),
            'entire generic scalar least-squares identity')
    checks['entire_generic_scalar_least_squares_identity']=True
    damages=[]
    probes={
      'wrong_normalizer_sign':lambda:eq('damaged_unit',dot([w[0],w[1],w[2],-w[3],w[4]],C),1),
      'wrong_real_reference':lambda:eq('damaged_reference',C[0]-14*C[4],-48*(7*s*s-4)),
      'wrong_E_pivot':lambda:eq('damaged_E',k.diffvar(b[3],1),F(-44,7)*(49*s*s-2)),
      'wrong_slice_Q':lambda:eq('damaged_Q',bz[0],F(-8,45)*B*(qexpr+1)),
      'wrong_unit_multiplier':lambda:require(add(mul(add([F(x)for x in units['Bnonzero']['left_multiplier']],[1]),[2727,16296,24080]),mul([F(x)for x in units['Bnonzero']['right_multiplier']],[1875,7280,5488]))==[1],'damaged whole unit'),
      'ignore_zero_slope':lambda:controls('ignore_zero_slope'),
      'drop_gram':lambda:controls('drop_gram'),
      'drop_positive':lambda:controls('drop_positive'),
      'drop_quadratic':lambda:controls('drop_quadratic')}
    for name,probe in probes.items():
        try:probe()
        except ValueError:damages.append(name)
        else:raise ValueError('mathematical damage survived '+name)
    def encoded(a):
        require(all(key[4]==0 and all(e==0 for e in key[5:])for key in P(a).c),
                'four-parameter coefficient circuit')
        return [[list(key[:5]),str(c)]for key,c in sorted(P(a).c.items())]
    record={'actual_agent':'six-sendov-2','role':'researcher',
      'input9550':{'source_commit':PARENT_COMMIT,'file_sha256':PARENT_FILES,'whole_record_sha256':PARENT_RECORD,
                   'entire_parent_fixture_checked':True,'same_author_code_reuse_not_independent_review':True},
      'ring':'QQ[B,E,r,s], real Gram statements require real parameters; complex s0 rank exclusion',
      'universal_identities':sorted(checks),'w':[encoded(x)for x in w],
      'alpha':k.polydigest([alpha]),'beta':k.polydigest([beta]),
      'linear_a':[k.polydigest([x])for x in a],'linear_b':[k.polydigest([x])for x in b],
      'rank1_E_numerator':encoded(R),'s0_B0_quintic':normalized,
      's0_B0_a0_scale':str(leading_ratio),'rational_slice_units':units,'finite_slice_units':finite,
      'Gram_controls':controls(),'rejected_mathematical_damages':damages,
      'rank0_excluded_over_complex':True,'s0_rank_at_least2_over_complex':True,
      'rank1_snonzero_classified':False,'all_stationary_profiles_classified':False,'complex_first_power_proved':False,
      'feasibility_required':['t>0','ALL reduced equations','seven SIMPLE REAL criticals','STRICT p(lambda)>0'],
      'ordinary_bridges':'9550 feasible theorem, unit-column rowspace splitting, t-positive cancellation, real sum-of-squares equality, positive quadratic-root branches, exact univariate Bezout incompatibility; unformalized'}
    if export is not None:
        export.write_text(json.dumps({'actual_agent':'six-sendov-2','role':'researcher','variables':['B','E','r','s','t'],
          'monomial_format':'[five nonnegative integral exponents in B,E,r,s,t, exact rational coefficient]; t exponent zero in alpha,beta,a,b',
          'w':[encoded(x)for x in w],'alpha':encoded(alpha),'beta':encoded(beta),
          'linear_a':[encoded(x)for x in a],'linear_b':[encoded(x)for x in b],
          'S_circuit':'sum a_i²','T_circuit':'sum a_i*b_i','U_circuit':'sum b_i²',
          'rank2_conditions':['S>0','T<0','SU-T²=0','alpha*T²-beta*T*S+S²=0'],
          'rank2_reconstruction':'t=-T/S',
          'rank1_conditions':['a=b=0','alpha*t²+beta*t+1=0','t>0'],
          'parent_reconstruction':data,'feasibility_required':record['feasibility_required'],
          'rank1_snonzero_classified':False},indent=2,sort_keys=True)+'\n')
    return record

def main():
    p=argparse.ArgumentParser();p.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'))
    p.add_argument('--emit',action='store_true');p.add_argument('--export',type=Path);args=p.parse_args()
    record=certificate(args.export)
    if args.emit:args.expected.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    else:require(same_typed(record,json.loads(args.expected.read_text())),'whole typed expected record mismatch')
    print(json.dumps({'status':'PASS','record_sha256':hashlib.sha256(canonical(record)).hexdigest(),
      'universal_identities':len(record['universal_identities']),'Gram_controls':len(record['Gram_controls']),
      'mathematical_damages':len(record['rejected_mathematical_damages']),'rational_slice_units':len(record['rational_slice_units']),
      'pinned_parent_complete_record_checked':True}))

if __name__=='__main__':main()
