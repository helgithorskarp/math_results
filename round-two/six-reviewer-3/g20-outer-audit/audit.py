"""Independent binding of untrusted factor literals to actual G20 geometry."""
import argparse
import hashlib
import json
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from digit import T, Z, coefficients, monomials, prove_zero
from geometry import LABELS, CONTACTS, model, dot
from signs import complete_sign


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def packet(data):
    require(set(data)=={'schema_version','variable_order','coefficient_domain','rows'},'factor schema')
    require(type(data['schema_version']) is int and data['schema_version']==1,'factor version')
    require(data['variable_order']==['t','z','w'] and data['coefficient_domain']=='Z','factor variables/domain')
    require(set(data['rows'])=={'L5','M6','H10','H12'},'factor names')
    result={}
    for name,rows in data['rows'].items():
        require(type(rows) is list and 0<len(rows)<=200,'factor row count')
        decoded=[]
        for row in rows:
            require(type(row) is list and len(row)==4,'factor row arity')
            i,j,k,v=row
            require(type(i) is int and type(j) is int and type(k) is int and k==0,'factor exponents')
            require(type(v) is str and len(v)<=30,'factor integer text')
            n=int(v)
            require(str(n)==v and n!=0,'factor integer canonicality')
            decoded.append((i,j,n))
        result[name]=monomials(decoded)
    return result


def univariate_quotient(p,d):
    require(all(j==0 for i,j in d),'nonunivariate divisor')
    divisor={i:v for (i,j),v in d.items()}
    top=max(divisor);lead=divisor[top]
    answer={}
    for j in range(max((j for i,j in p),default=0)+1):
        rem={i:v for (i,k),v in p.items() if k==j}
        while rem and max(rem)>=top:
            degree=max(rem);q,r=divmod(rem[degree],lead)
            require(r==0,'nonintegral division step')
            k=degree-top;answer[k,j]=q
            for i,v in divisor.items():
                value=rem.get(i+k,0)-q*v
                if value:rem[i+k]=value
                else:rem.pop(i+k,None)
        require(not rem,'nonzero complete integer polynomial remainder')
    return {k:v for k,v in answer.items() if v}


def compile_identities(factors):
    m=model();t,z=T,Z
    a,b,c,D,C,K,J,h,S,E,G,R,O=(m[k] for k in ['a','b','c','D','C','K','J','h','S','E','G','R','Omega'])
    q5=dot(m['Y'][5],m['N'][12])-t*a*a*O
    q6=dot(m['Y'][6],m['N'][8])-t*a*a*O
    f5=t*a**10*b*c*(3*t-1)
    f6=a**5*b*c*(3*t-1)*(3*t+1)
    zz=t*(3*t+1)*z-(1+2*t)
    m5=1+2*t-t*t-2*t*b*c*z
    q=(1+t)*D*z*z-2*D*z+2*t*t-t+1
    a5=2*D*(b*z+1)*C*factors['L5']
    b5=-2*(b*z+1)*C*m5
    b6=2*(b*z+1)*factors['M6']
    r5=a*b**5*c**3*J*C*C*32*(b*z+1)**2*(1-b*z)*(b*c*z+t)*zz*q
    r6=a*a*b**4*c**3*J*4*(b*z+1)**2*q*factors['H10']*factors['H12']
    residuals={'q5_constant':q5.p-f5*a5,'q5_linear':q5.q-f5*b5,
               'q6_linear':q6.q-f6*b6,'q5_squared_uncancelled':q5.p**2-q5.q**2*R-f5**2*r5,
               'q6_squared_uncancelled':q6.p**2-q6.q**2*R-f6**2*r6,
               'Q_positive_square':a*q-D*(a*z-1)**2-4*t*t,
               'closed_bz1_boundary':b*(1+2*t-t*t)-2*t*b*c-b*(1-5*t*t),
               'G_positive_clearing':G-a**4*(1-t*t)*E+(K*C-S*t*a*a)**2}
    records={name:prove_zero(p) for name,p in residuals.items()}
    quotients={}
    for name,raw,divisor in [('A5',q5.p,f5),('B5',q5.q,f5),('A6',q6.p,f6),('B6',q6.q,f6)]:
        quotients[name]=univariate_quotient(coefficients(raw),coefficients(divisor))
    for name,value in [('A5',a5),('B5',b5),('B6',b6)]:
        require(quotients[name]==coefficients(value),'whole quotient coefficient mismatch')
    a6=monomials([(i,j,v) for (i,j),v in quotients['A6'].items()])
    records['q6_complete_division']=prove_zero(q6.p-f6*a6)
    records['q6_squared_after_division']=prove_zero(a6*a6-b6*b6*R-r6)
    record_rows={name:[[i,j,v] for (i,j),v in sorted(rows.items())] for name,rows in quotients.items()}
    return m,records,{'all_four_integer_quotients':record_rows,'whole_quotients_digest':digest(record_rows)}


def cover(cut):
    ta,tc,tb,zc,zb=F(14,25),F(113,200),F(593,1000),F(71,50),F(5,2)
    return [(ta,tc,cut,zc),(tc,tb,cut,zb),(ta,tb,zc,zb)]


def complete_cover(boxes,cut):
    tvalues=[F(14,25),F(113,200),F(593,1000)]
    zvalues=[cut,F(71,50),F(5,2)]
    def atoms(points):
        return [(points[0],points[0]),(points[0],points[1]),
                (points[1],points[1]),(points[1],points[2]),(points[2],points[2])]
    rows=[]
    for ta,tb in atoms(tvalues):
        for za,zb in atoms(zvalues):
            matches=[k for k,(a,b,c,d) in enumerate(boxes) if a<=ta<=tb<=b and c<=za<=zb<=d]
            require(matches,'uncovered whole elementary cell')
            rows.append([[str(x) for x in (ta,tb,za,zb)],matches])
    return rows


def signs(factors,cut):
    boxes=cover(cut);coverage=complete_cover(boxes,cut)
    whole=(F(14,25),F(593,1000),cut,F(5,2))
    zz=T*(3*T+1)*Z-(1+2*T)
    tasks=[('L5',factors['L5'],whole,1),('Z_upper_t',zz,boxes[1],1),
           ('Z_upper_z',zz,boxes[2],1),('M6',factors['M6'],boxes[0],1),
           ('H10',factors['H10'],boxes[0],-1),('H12',factors['H12'],boxes[0],1)]
    result={};full={}
    for name,p,box,sign in tasks:
        record=complete_sign(coefficients(p),box,sign)
        rows=record.pop('all_rows');full[name]=rows
        result[name]={**record,'expected_sign':sign,'box':[str(v) for v in box],
                      'whole_rows_sha256':digest(rows)}
    return {'cut':str(cut),'closed_rectangles':[[str(x) for x in box] for box in boxes],
            'elementary_cover':coverage,'signs':result,'all_sign_rows_sha256':digest(full)}


def physical_control(m):
    t,z,w=F(29,50),F(5400,3973),F(454484658996081,225033203125000)
    @lru_cache(None)
    def ev(node):
        if node.op=='c':return F(node.args[0])
        if node.op=='t':return t
        if node.op=='z':return z
        if node.op=='+':return ev(node.args[0])+ev(node.args[1])
        if node.op=='-':return -ev(node.args[0])
        if node.op=='*':return ev(node.args[0])*ev(node.args[1])
        raise ValueError('unknown rational control operation')
    require(w*w==ev(m['R']) and w>0,'positive actual radical control')
    omega=ev(m['Omega']);require(omega>0,'actual positive denominator control')
    points={i:[(ev(x.p)+w*ev(x.q))/omega for x in m['Y'][i]] for i in LABELS}
    def product(u,v):return (1-t)*sum(x*y for x,y in zip(u,v))+t*sum(u)*sum(v)
    require(all(product(points[i],points[i])==1 for i in LABELS),'original units control')
    gaps={}
    for k,i in enumerate(LABELS):
        for j in LABELS[k+1:]:
            gap=t-product(points[i],points[j]);require(gap>=0,'original physical packing control')
            gaps[str(i)+'-'+str(j)]=str(gap)
    require(all(gaps[str(i)+'-'+str(j)]=='0' for i,j in CONTACTS),'original20 contacts control')
    require(gaps['5-12']=='0' and z<F(1399,1000),'credited equality control below both cuts')
    require(2*ev(m['G'])>ev(m['a'])**4*ev(m['C'])**2,'actual imported regularity control')
    return {'credited_not_new':True,'parameters':[str(t),str(z),str(w)],'units':12,
            'pair_tests':66,'required_contacts':20,'all66_gaps_sha256':digest(gaps),
            'positive_denominator':True,'positive_radical':True,'additional5_12_equality':True}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--cut',default='7/5');ap.add_argument('--factors',default='FACTORS.json')
    args=ap.parse_args();cut=F(args.cut)
    require(cut in (F(7,5),F(1399,1000)),'unproved requested cut')
    data=Path(args.factors).read_bytes();factors=packet(json.loads(data))
    m,identities,quotients=compile_identities(factors)
    record={'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer',
            'factor_packet_sha256':hashlib.sha256(data).hexdigest(),'input_status':'untrusted published literals; not independently rediscovered',
            'complete_identity_records':identities,'complete_divisions':quotients,
            'closed_sign_cover':signs(factors,cut),'actual_original_control':physical_control(m)}
    print(json.dumps(record,sort_keys=True,separators=(',',':')))


if __name__=='__main__':
    main()
