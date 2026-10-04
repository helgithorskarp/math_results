"""Whole exact two-same-sign-double identities and tensor signs.

Standard library only. All large maps/vectors are regenerated internally.
The ordinary physical-domain/compression/limit proof is in PROOF.md.
Actual author six-sendov-2/researcher; unformalized, not independent review.
"""
from argparse import ArgumentParser
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
from math import comb
from pathlib import Path
import json

BASE=Path(__file__).resolve().parent
DOMAIN='QQ[p,tau][z]; actual p>2,0<tau<T,tau<1/(p^2+1),p=r+r^3,r>1'
ZERO={}
ONE={(0,0):Q(1)}

def require(ok,message):
    if not ok:raise ValueError(message)

def add(a,b):
    out=dict(a)
    for k,v in b.items():
        out[k]=out.get(k,Q(0))+v
        if not out[k]:out.pop(k)
    return out

def scale(a,c):
    return {k:v*c for k,v in a.items() if v*c}

def sub(a,b):return add(a,scale(b,-1))

def mul(a,b):
    out={}
    for (i,j),v in a.items():
        for (k,l),w in b.items():
            key=(i+k,j+l)
            out[key]=out.get(key,Q(0))+v*w
    return {k:v for k,v in out.items() if v}

def power(a,n):
    out=ONE
    for _ in range(n):out=mul(out,a)
    return out

def parse(rows):
    require(type(rows)is list,'coefficient rows type')
    require(len(rows)<=512,'bounded complete sparse coefficient list')
    out={}
    previous=None
    for row in rows:
        require(type(row)is dict and set(row)=={'powers','coefficient'},'coefficient schema')
        p=row['powers'];c=row['coefficient']
        require(type(p)is list and len(p)==2 and all(type(i)is int and 0<=i<=32 for i in p),'power vector')
        require(type(c)is str and 0<len(c)<=500,'rational string')
        v=Q(c);require(str(v)==c and v!=0,'canonical nonzero coefficient')
        k=tuple(p);require(previous is None or previous<k,'strict sparse monomial order');previous=k;require(k not in out,'duplicate monomial')
        out[k]=v
    return out

def terms(a):
    return [{'powers':list(k),'coefficient':str(v)} for k,v in sorted(a.items())]

def trim(a):
    a=list(a)
    while len(a)>1 and not a[-1]:a.pop()
    return a or [ZERO]

def zadd(a,b):
    return trim([add(a[i] if i<len(a) else ZERO,b[i] if i<len(b) else ZERO)
                 for i in range(max(len(a),len(b)))])

def zscale(a,c):return trim([scale(x,c) for x in a])

def zmul(a,b):
    out=[ZERO for _ in range(len(a)+len(b)-1)]
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]=add(out[i+j],mul(x,y))
    return trim(out)

def zderivative(a):
    return trim([scale(a[i],i) for i in range(1,len(a))])

def zdivide(a,b):
    require(b[-1]==ONE,'monic outer divisor')
    a=trim(a);out=[ZERO for _ in range(max(1,len(a)-len(b)+1))]
    while a!=[ZERO] and len(a)>=len(b):
        k=len(a)-len(b);c=a[-1]
        out[k]=add(out[k],c)
        a=zadd(a,[ZERO]*k+[scale(mul(c,v),-1) for v in b])
    return trim(out),trim(a)

def resultant(a,b):
    n,m=len(a)-1,len(b)-1;size=n+m
    rows=[]
    for i in range(m):
        rows.append([ZERO]*i+list(reversed(a))+[ZERO]*(m-i-1))
    for i in range(n):
        rows.append([ZERO]*i+list(reversed(b))+[ZERO]*(n-i-1))
    dp={0:ONE}
    for row in rows:
        new={}
        for mask,value in dp.items():
            for j,c in enumerate(row):
                if mask&(1<<j) or not c:continue
                term=mul(value,c)
                if (mask>>(j+1)).bit_count()%2:term=scale(term,-1)
                key=mask|(1<<j)
                new[key]=add(new.get(key,ZERO),term)
        dp=new
    return dp.get((1<<size)-1,ZERO)

def expand_y(a):
    return {(2*i,j):c for (i,j),c in a.items()}

def substitute_y_tau(a):
    # Now the inner variables are u,b. y=u(1+u)^2,
    # tau=(u-1)^2(u+1)b. Complete sparse composition.
    Y={(1,0):Q(1),(2,0):Q(2),(3,0):Q(1)}
    T={(0,1):Q(1),(1,1):Q(-1),(2,1):Q(-1),(3,1):Q(1)}
    ymax=max(i for i,j in a);tmax=max(j for i,j in a)
    yp=[ONE];tp=[ONE]
    for _ in range(ymax):yp.append(mul(yp[-1],Y))
    for _ in range(tmax):tp.append(mul(tp[-1],T))
    out=ZERO
    for (i,j),c in a.items():out=add(out,scale(mul(yp[i],tp[j]),c))
    return out

def divide_linear_u(a,root):
    # Division separately in each entire b coefficient, avoiding CAS gcd.
    out={}
    for j in sorted({j for i,j in a}):
        degree=max(i for i,k in a if k==j)
        coeff=[a.get((i,j),Q(0)) for i in range(degree+1)]
        quotient=[Q(0)]*max(1,degree)
        for i in range(degree,0,-1):
            quotient[i-1]=coeff[i]
            coeff[i-1]+=root*coeff[i]
        require(coeff[0]==0,'whole exact common-factor division')
        for i,c in enumerate(quotient):
            if c:out[i,j]=c
    return out

def strip_common(a):
    for _ in range(4):a=divide_linear_u(a,Q(1))
    for _ in range(6):a=divide_linear_u(a,Q(-1))
    return a

def shift_unit(a):
    out={}
    for (i,j),c in a.items():
        for k in range(i+1):
            key=k,j
            out[key]=out.get(key,Q(0))+c*comb(i,k)*Q(9,40)**k
    return {k:v for k,v in out.items() if v}

def tensor_bernstein(a):
    n=max(i for i,j in a);m=max(j for i,j in a)
    first={}
    for k in range(n+1):
        for j in range(m+1):
            first[k,j]=sum(a.get((i,j),Q(0))*Q(comb(k,i),comb(n,i))
                           for i in range(k+1))
    return [[sum(first[k,j]*Q(comb(l,j),comb(m,j)) for j in range(l+1))
             for l in range(m+1)] for k in range(n+1)]

def u_trim(a):
    a = list(a)
    while len(a) > 1 and (not a[-1]):
        a.pop()
    return a or [Q(0)]

def u_add(a, b):
    return u_trim([(a[i] if i < len(a) else Q(0)) + (b[i] if i < len(b) else Q(0)) for i in range(max(len(a), len(b)))])

def u_scale(a, t):
    return u_trim([x * t for x in a])

def u_sub(a, b):
    return u_add(a, u_scale(b, -1))

def u_mul(a, b):
    c = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    c[i + j] += x * y
    return u_trim(c)

def u_divide(a, b):
    a, b = (u_trim(a), u_trim(b))
    require(b != [0], 'zero polynomial divisor')
    q = [Q(0)] * max(1, len(a) - len(b) + 1)
    while a != [0] and len(a) >= len(b):
        j, v = (len(a) - len(b), a[-1] / b[-1])
        q[j] += v
        a = u_sub(a, [Q(0)] * j + u_scale(b, v))
    return (u_trim(q), u_trim(a))

def zero_matrix():
    return [[Q(0) for _ in range(7)] for _ in range(7)]

def identity(c=Q(1)):
    out = zero_matrix()
    for i in range(7):
        out[i][i] = c
    return out

def matrix_add(a, b):
    return [[a[i][j] + b[i][j] for j in range(7)] for i in range(7)]

def matrix_mul(a, b):
    out = zero_matrix()
    for i in range(7):
        for k in range(7):
            if a[i][k]:
                for j in range(7):
                    if b[k][j]:
                        out[i][j] += a[i][k] * b[k][j]
    return out

def matrix_scale(a, c):
    return [[v * c for v in row] for row in a]

def matrix_inverse(a):
    out = [row[:] + e for row, e in zip(a, identity())]
    for j in range(7):
        pivot = next((i for i in range(j, 7) if out[i][j]), None)
        require(pivot is not None, 'singular seven-slot derivative')
        out[j], out[pivot] = (out[pivot], out[j])
        t = out[j][j]
        out[j] = [v / t for v in out[j]]
        for i in range(7):
            if i != j and out[i][j]:
                t = out[i][j]
                out[i] = [v - t * w for v, w in zip(out[i], out[j])]
    return [row[7:] for row in out]

def matrix_eval(a, H):
    out = zero_matrix()
    for c in reversed(a):
        out = matrix_add(matrix_mul(out, H), identity(c))
    return out

def matrix_trace(a):
    return sum((a[i][i] for i in range(7)))

def canonical(value):
    return (json.dumps(value,sort_keys=True,indent=2)+'\n').encode('utf-8')

def unique_object(pairs):
    value={}
    for key,item in pairs:
        require(key not in value,'duplicate JSON key')
        value[key]=item
    return value

def load_json(path):
    raw=Path(path).read_bytes()
    require(len(raw)<=100000,'oversized defining certificate or compact fixture')
    return json.loads(raw,object_pairs_hook=unique_object)

def typed_equal(a,b):
    require(type(a)is type(b),'whole fixture exact type')
    if type(a)is dict:
        require(set(a)==set(b),'whole fixture key set')
        for key in a:typed_equal(a[key],b[key])
    elif type(a)is list:
        require(len(a)==len(b),'whole fixture list length')
        for left,right in zip(a,b):typed_equal(left,right)
    else:require(a==b,'whole fixture scalar')

def certificate_schema(cert):
    fields={'domain','critical_quintic','inverse_common_denominator',
            'inverse_numerators','discriminant',
            'discriminant_divided_by_inverse_denominator',
            'angular_numerator_y_tau','angular_denominator_y_tau'}
    require(type(cert)is dict and set(cert)==fields,'complete certificate schema')
    require(type(cert['domain'])is str and cert['domain']==DOMAIN,'exact coefficient/physical domain')
    for name,length in [('critical_quintic',6),('inverse_numerators',5)]:
        require(type(cert[name])is list and len(cert[name])==length,'complete quintic slots')
        for rows in cert[name]:parse(rows)
    for name in fields-{'domain','critical_quintic','inverse_numerators'}:parse(cert[name])

def bidegree(poly):
    return [max(i for i,j in poly),max(j for i,j in poly)]

def core(cert,fault=None):
    certificate_schema(cert)
    H5=list(map(parse,cert['critical_quintic']))
    invnum=list(map(parse,cert['inverse_numerators']))
    Delta=parse(cert['inverse_common_denominator'])
    require(H5[-1]==ONE,'monic quintic')
    P={(1,0):Q(1)};T={(0,1):Q(1)}
    d2=[ONE,scale(P,-1),ONE]
    q=[add(mul(P,P),ONE),scale(P,-2),ONE]
    gU=zmul(d2,d2)
    other=zadd(gU,[scale(mul(T,c),-1) for c in q])
    reflected=[scale(c,(-1)**i) for i,c in enumerate(other)]
    f=zmul(gU,reflected)
    require(f[7]==f[5]==f[3]==ZERO,'whole original odd-moment coefficients')
    h=zscale(zderivative(f),Q(1,8))
    quotient,rem=zdivide(h,d2)
    require(rem==[ZERO] and quotient==H5,'whole actual canceled quintic')
    Hp=zderivative(H5)
    disc=resultant(H5,Hp)
    require(disc==parse(cert['discriminant']),'ENTIRE quintic Sylvester discriminant')
    require(mul(Delta,parse(cert['discriminant_divided_by_inverse_denominator']))==disc,
            'whole nonzero specialization divisor')
    inverse_quotient,rem=zdivide(zmul(Hp,invnum),H5)
    require(rem==[Delta],'whole quintic derivative inverse identity')
    mass=zdivide(zmul(zscale(zmul(d2,reflected),-8),invnum),H5)[1]
    mass2=zdivide(zmul(mass,mass),H5)[1]
    powers=[scale(ONE,5)]
    for k in range(1,5):
        value=scale(H5[5-k],-k)
        for j in range(1,k):value=sub(value,mul(H5[5-j],powers[k-j]))
        powers.append(value)
    def trace(a):
        out=ZERO
        for i,c in enumerate(a):out=add(out,mul(c,powers[i]))
        return out
    N=scale(f[6],-2)
    X=sub(scale(mul(N,N),Q(1,2)),scale(f[4],4))
    D=sub(X,scale(mul(N,N),Q(1,8)))
    if fault=='normalization':N=add(N,ONE)
    require(N==add(sub(scale(mul(P,P),4),scale(ONE,8)),scale(T,2)),'whole raw norm')
    require(trace(mass)==mul(N,Delta),'whole actual five-slot mass normalization')
    eta_num=trace(mass2)
    raw_num=sub(mul(mul(N,N),mul(Delta,Delta)),eta_num)
    declared_num=parse(cert['angular_numerator_y_tau'])
    declared_den=parse(cert['angular_denominator_y_tau'])
    lhs=mul(raw_num,expand_y(declared_den))
    rhs=mul(mul(D,mul(Delta,Delta)),expand_y(declared_num))
    require(lhs==rhs,'ENTIRE bivariate actual angular identity')
    normalized_num=strip_common(substitute_y_tau(declared_num))
    normalized_den=strip_common(substitute_y_tau(declared_den))
    gap=divide_linear_u(sub(scale(normalized_den,16),normalized_num),Q(1))
    complete_fields={};compact_fields=[]
    for name,poly in [('denominator',normalized_den),('divided_gap16',gap)]:
        unit=shift_unit(poly)
        bern=tensor_bernstein(unit)
        if fault=='last tensor sign' and name=='divided_gap16':bern[-1][-1]=Q(-1)
        require(all(x>0 for row in bern for x in row),'strict ENTIRE tensor positivity')
        encoded=[[str(x)for x in row]for row in bern]
        field={'whole_original_terms':terms(poly),'whole_unit_terms':terms(unit),
               'complete_tensor_bernstein':encoded}
        complete_fields[name]=field
        compact_fields.append({'name':name,'degree':bidegree(poly),
                               'entries':sum(len(row)for row in bern),
                               'minimum':str(min(x for row in bern for x in row)),
                               'all_entries_strictly_positive':True,
                               'whole_field_sha256':sha256(canonical(field)).hexdigest()})
    require([r['degree']for r in compact_fields]==[[26,9],[25,9]],'complete tensor degrees')
    large=sub(scale(D,20),mul(N,N))
    expected_large={(4,0):Q(24),(2,0):Q(-96),(0,0):Q(-64),
                    (2,1):Q(-56),(0,1):Q(32),(0,2):Q(26)}
    require(large==expected_large,'whole large-region polynomial')
    upper=Q(49,40)
    require(upper*(1+upper)**2>6 and 1+2*upper-upper**2-upper**3>0,
            'exact containing physical rectangle')
    complete={'whole_f':[terms(a)for a in f],'whole_H5':[terms(a)for a in H5],
              'whole_discriminant':terms(disc),'whole_inverse_identity_quotient':[terms(a)for a in inverse_quotient],
              'whole_mass_remainders':[terms(a)for a in mass],
              'whole_squared_mass_remainders':[terms(a)for a in mass2],
              'whole_mass_trace':terms(trace(mass)),'whole_eta_numerator':terms(eta_num),
              'whole_cleared_angular_identity':terms(lhs),
              'whole_transformed_numerator':terms(normalized_num),'fields':complete_fields}
    compact={'whole_polynomial_checks_passed':True,'raw_N':terms(N),'raw_X':terms(X),
             'raw_D':terms(D),'large_region_20D_minus_N2':terms(large),
             'angular_bidegrees':[bidegree(declared_num),bidegree(declared_den)],
             'cleared_identity_monomials':len(lhs),'discriminant_bidegree':bidegree(disc),
             'complete_fields':compact_fields,
             'whole_internal_polynomial_record_sha256':sha256(canonical(complete)).hexdigest(),
             'physical_B_upper':str(1+2*upper-upper**2-upper**3),
             'physical_y_upper':str(upper*(1+upper)**2)}
    return compact,complete

def variations(values):
    signs=[(x>0)-(x<0)for x in values if x]
    return sum(a!=b for a,b in zip(signs,signs[1:]))

def u_derivative(a):
    return u_trim([(i+1)*a[i+1]for i in range(len(a)-1)])

def root_count(a):
    chain=[a,u_derivative(a)]
    while True:
        rem=u_divide(chain[-2],chain[-1])[1]
        if rem==[0]:break
        chain.append(u_scale(rem,-1))
    at0=variations([p[0]for p in chain]);plus=variations([p[-1]for p in chain])
    minus=variations([p[-1]*(-1)**(len(p)-1)for p in chain])
    return {'positive_distinct':at0-plus,'negative_distinct':minus-at0,
            'gcd_degree':len(chain[-1])-1,
            'entire_sturm_chain':[[str(c)for c in row]for row in chain]}

def scalar(poly,y,tau):
    return sum(c*y**i*tau**j for (i,j),c in poly.items())

def seven_slot_cases(cert):
    num=parse(cert['angular_numerator_y_tau']);den=parse(cert['angular_denominator_y_tau'])
    rows=[]
    for r in [Q(101,100),Q(21,20),Q(11,10),Q(10,9)]:
        p=r+r**3;B=1+2*r*r-r**4-r**6;T=(r*r-1)**2*(r*r+1)
        require(r>1 and B>0,'actual finite original parameter')
        d2=[Q(1),-p,Q(1)];gU=u_mul(d2,d2);q=[p*p+1,-2*p,Q(1)]
        for b in [Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)]:
            tau=b*T;other=u_sub(gU,u_scale(q,tau));roots=root_count(other)
            count=2 if b==0 else 3 if b==1 else 4
            require(roots['positive_distinct']==count and roots['negative_distinct']==0
                    and roots['gcd_degree']==4-count,'whole actual finite Sturm root count')
            f=u_mul(gU,[c*(-1)**i for i,c in enumerate(other)])
            h=u_scale(u_derivative(f),Q(1,8));H=zero_matrix()
            for j in range(6):H[j+1][j]=Q(1)
            for j in range(7):H[j][6]=-h[j]
            hp=matrix_eval(u_derivative(h),H);inverse=matrix_inverse(hp)
            require(matrix_mul(hp,inverse)==identity(),'ENTIRE seven-slot derivative inverse')
            mass=matrix_scale(matrix_mul(matrix_eval(f,H),inverse),-8)
            N=-2*f[6];X=N*N/2-4*f[4];D=X-N*N/8
            eta=matrix_trace(matrix_mul(mass,mass));C=(N*N-eta)/D
            moments=[Q(8)]
            for k in range(1,6):
                value=-k*f[8-k]
                for j in range(1,k):value-=f[8-j]*moments[k-j]
                moments.append(value)
            declared_den=scalar(den,p*p,tau)
            require(declared_den!=0 and C==scalar(num,p*p,tau)/declared_den,
                    'whole generic value agrees with all seven slots')
            require(matrix_trace(mass)==N and D>0 and C<16
                    and moments[1]==moments[3]==moments[5]==0
                    and moments[2]==N and moments[4]==X,'actual finite masses and moments')
            rows.append({'r':str(r),'p':str(p),'y':str(p*p),'B':str(B),'fraction_of_T':str(b),
                         'tau':str(tau),'actual_companion_root_record':roots,
                         'whole_f':[str(c)for c in f],'whole_h':[str(c)for c in h],
                         'original_first_five_powers':[str(c)for c in moments[1:]],
                         'N':str(N),'X':str(X),'D':str(D),'raw_eta':str(eta),
                         'angular_C':str(C),'all_seven_slots_accounted_for':True})
    lookup={row['fraction_of_T']:row for row in rows if row['r']=='21/20'}
    difference=Q(lookup['3/4']['angular_C'])-Q(lookup['1']['angular_C'])
    require(difference>0,'actual fixed-p endpoint comparison obstruction')
    obstruction={'r':'21/20','interior_fraction':'3/4','endpoint_fraction':'1',
                 'strict_positive_C_difference':str(difference),
                 'not_the_10200_fixed_norm_midpoint_path':True}
    return rows,obstruction

def build(cert):
    compact,complete=core(cert)
    rows,obstruction=seven_slot_cases(cert)
    record={'actual_agent':'six-sendov-2','role':'researcher',
            'status':'whole defining identities and all530positive tensor coefficients verified',
            'trust_boundary':'ordinary written physical-domain/compression/limit proof, unformalized and independently unreviewed',
            'domain':DOMAIN,'core':compact,'actual_seven_slot_cases':rows,
            'fixed_p_endpoint_comparison_obstruction':obstruction}
    return record,complete

def self_test(cert):
    damages=[('critical_quintic','whole actual canceled quintic'),
             ('inverse_numerators','whole quintic derivative inverse identity'),
             ('discriminant','ENTIRE quintic Sylvester discriminant'),
             ('discriminant_divided_by_inverse_denominator','whole nonzero specialization divisor'),
             ('angular_numerator_y_tau','ENTIRE bivariate actual angular identity'),
             ('angular_denominator_y_tau','ENTIRE bivariate actual angular identity')]
    count=0
    for key,gate in damages:
        damaged=deepcopy(cert);rows=damaged[key]
        if key in ['critical_quintic','inverse_numerators']:rows=next(slot for slot in rows if slot)
        row=next(row for row in rows if Q(row['coefficient'])+1!=0)
        row['coefficient']=str(Q(row['coefficient'])+1)
        try:core(damaged)
        except ValueError as exc:require(str(exc)==gate,'wrong semantic rejection gate')
        else:raise ValueError('damaged defining certificate accepted')
        count+=1
    for fault,gate in [('normalization','whole raw norm'),('last tensor sign','strict ENTIRE tensor positivity')]:
        try:core(cert,fault=fault)
        except ValueError as exc:require(str(exc)==gate,'wrong internal mathematical rejection gate')
        else:raise ValueError('damaged mathematical computation accepted')
        count+=1
    return count

def main():
    parser=ArgumentParser()
    parser.add_argument('--certificate',type=Path,default=BASE/'CERTIFICATE.json')
    parser.add_argument('--expected',type=Path,default=BASE/'EXPECTED.json')
    parser.add_argument('--self-test',action='store_true')
    parser.add_argument('--write-record',type=Path)
    args=parser.parse_args()
    cert=load_json(args.certificate);record,_=build(cert)
    typed_equal(record,load_json(args.expected))
    controls=self_test(cert)if args.self_test else 0
    data=canonical(record)
    if args.write_record:args.write_record.write_bytes(data)
    print(json.dumps({'status':record['status'],'record_bytes':len(data),'record_sha256':sha256(data).hexdigest(),
                      'whole_compact_fixture_matches':True,'semantic_rejections':controls,
                      'actual_finite_cases':len(record['actual_seven_slot_cases'])}))

if __name__=='__main__':main()
