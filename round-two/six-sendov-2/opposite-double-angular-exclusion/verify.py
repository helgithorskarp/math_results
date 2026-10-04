"""Exact whole opposite-double identities and continuum sign certificates.

Actual author six-sendov-2/researcher. Ordinary bridges are in PROOF.md.
All arithmetic routes share the author; no independent review or formalization.
"""
from argparse import ArgumentParser
from copy import deepcopy
from pathlib import Path
import sys

BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE))
from algebra import *

SOURCE="39ccb1eef4b190986e60a79154cbd07cef0ed671"
SOURCE_HASH="080a36d30d22e43eccb52aa67fcaace9c71b569f617967d23db1d309aac004d5"
NEW_DOMAIN="QQ[s,lambda][z]; actual s>0,exacttwo opposite-sign doubles,four singles,4+4; equal-magnitude branch separate9416"
COVER=[["0","1/2"],["1/2","3/4"],["3/4","7/8"],["7/8","1"]]

def input_schema(data):
    keys={"actual_agent","role","source_commit","source_certificate_sha256",
          "whole_embedded_fields_canonical_sha256","inherited_defining_data",
          "new_domain","positive_v_upper","positive_closed_b_cover",
          "positive_bound","negative_bound"}
    require(type(data)is dict and set(data)==keys,"whole input schema")
    for k,v in [("actual_agent","six-sendov-2"),("role","researcher"),
                ("source_commit",SOURCE),("source_certificate_sha256",SOURCE_HASH),
                ("whole_embedded_fields_canonical_sha256",SOURCE_HASH),
                ("new_domain",NEW_DOMAIN),("positive_v_upper","5/9"),
                ("positive_bound","47/2"),("negative_bound","16")]:
        require(type(data[k])is str and data[k]==v,"exact input metadata")
    typed_equal(data["positive_closed_b_cover"],COVER)
    certificate_schema(data["inherited_defining_data"])

def rotate(poly,k=0,global_power=0):
    # p=-i*s, z_old=i*z; divide by i**global_power.
    out={}
    for (i,j),c in poly.items():
        require((k+i-global_power)%2==0,"real coefficient rotation parity")
        out[i,j]=c*(-1)**i*(-1)**((k+i-global_power)//2)
    return out

def zrotate(poly,global_power=0):
    return [rotate(c,k,global_power)for k,c in enumerate(poly)]

def traces(H):
    out=[scale(ONE,len(H)-1)]
    for k in range(1,len(H)-1):
        value=scale(H[len(H)-1-k],-k)
        for j in range(1,k):
            value=sub(value,mul(H[len(H)-1-j],out[k-j]))
        out.append(value)
    return out

def ztrace(poly,H):
    t=traces(H);value=ZERO
    for k,c in enumerate(poly):value=add(value,mul(c,t[k]))
    return value

def zrows(poly):return [terms(c)for c in poly]

def actual_identity(cert):
    # Defining data is inherited openly; both new f and its actual H are fresh.
    oldH=list(map(parse,cert["critical_quintic"]))
    oldI=list(map(parse,cert["inverse_numerators"]))
    oldDelta=parse(cert["inverse_common_denominator"])
    oldDisc=parse(cert["discriminant"])
    require(mul(oldDelta,parse(cert["discriminant_divided_by_inverse_denominator"]))==oldDisc,
            "whole specialization divisor")
    S={(1,0):Q(1)};L={(0,1):Q(1)}
    d=[scale(ONE,-1),S,ONE]
    B=[scale(ONE,-1),scale(S,-1),ONE]
    q=[sub(mul(S,S),ONE),scale(S,-2),ONE]
    quartic=zadd(zmul(B,B),[mul(L,c)for c in q])
    f=zmul(zmul(d,d),quartic)
    h=zscale(zderivative(f),Q(1,8))
    H,rem=zdivide(h,d)
    require(rem==[ZERO] and H==zrotate(oldH,1),"whole actual canceled quintic")
    require(f[7]==f[5]==f[3]==ZERO,"whole odd-moment coefficients")
    require(f[1]==scale(mul(power(S,3),L),-2),"entire surviving odd coefficient")
    oldd=[ONE,scale(S,-1),ONE]
    oldf=zmul(zmul(oldd,oldd),zadd(zmul([ONE,S,ONE],[ONE,S,ONE]),
        [scale(mul(L,c),-1)for c in [add(power(S,2),ONE),scale(S,2),ONE]]))
    require(zrotate(oldf)==f,"whole octic algebraic rotation")
    require(zrotate(zscale(zderivative(oldf),Q(1,8)),-1)==h,"whole derivative rotation")
    disc=resultant(H,zderivative(H))
    require(disc==rotate(oldDisc),"ENTIRE actual Sylvester discriminant")
    Delta=rotate(oldDelta);I=zrotate(oldI)
    require(Delta==scale(disc,16),"whole inverse/discriminant license")
    iq,rem=zdivide(zmul(zderivative(H),I),H)
    require(rem==[Delta],"whole actual derivative inverse identity")
    mass=zdivide(zmul(zscale(zmul(d,quartic),-8),I),H)[1]
    mass2=zdivide(zmul(mass,mass),H)[1]
    N=scale(f[6],-2)
    X=sub(scale(mul(N,N),Q(1,2)),scale(f[4],4))
    D=sub(X,scale(mul(N,N),Q(1,8)))
    require(N==add(add(scale(power(S,2),4),scale(ONE,8)),scale(L,-2)),"whole raw norm")
    expectedD=add(add(scale(power(L,2),Q(3,2)),scale(mul(L,power(S,2)),2)),
                  add(scale(power(S,4),2),scale(power(S,2),8)))
    require(D==expectedD,"whole raw fourth denominator")
    complete_square=add(scale(power(add(L,scale(power(S,2),Q(2,3))),2),Q(3,2)),
                        add(scale(power(S,4),Q(4,3)),scale(power(S,2),8)))
    require(D==complete_square,"entire positive completed square")
    mt=ztrace(mass,H);eta=ztrace(mass2,H)
    require(mt==mul(N,Delta),"whole five-positive-slot norm")
    num=parse(cert["angular_numerator_y_tau"]);den=parse(cert["angular_denominator_y_tau"])
    newnum={(2*i,j):c*(-1)**i for(i,j),c in num.items()}
    newden={(2*i,j):c*(-1)**i for(i,j),c in den.items()}
    require(newden==scale(mul(D,disc),8192),"whole actual denominator factor")
    lhs=mul(sub(mul(power(N,2),power(Delta,2)),eta),newden)
    rhs=mul(mul(D,power(Delta,2)),newnum)
    require(lhs==rhs,"ENTIRE500-monomial angular identity")
    require(len(lhs)==500,"whole cleared identity degree support")
    return {
        "whole_f":zrows(f),"whole_h":zrows(h),"whole_quartic":zrows(quartic),
        "whole_H5":zrows(H),"whole_discriminant":terms(disc),
        "whole_inverse_denominator":terms(Delta),"whole_inverse_numerators":zrows(I),
        "whole_inverse_quotient":zrows(iq),"whole_mass_remainder":zrows(mass),
        "whole_squared_mass_remainder":zrows(mass2),
        "whole_mass_trace":terms(mt),"whole_eta_numerator":terms(eta),
        "whole_raw_N":terms(N),"whole_raw_X":terms(X),"whole_raw_D":terms(D),
        "whole_transferred_num":terms(newnum),"whole_transferred_den":terms(newden),
        "whole_cleared_identity":terms(lhs),
    }

def compose(poly,Y,T):
    yp=[ONE];tp=[ONE]
    for _ in range(max(i for i,j in poly)):yp.append(mul(yp[-1],Y))
    for _ in range(max(j for i,j in poly)):tp.append(mul(tp[-1],T))
    out=ZERO
    for(i,j),c in poly.items():out=add(out,scale(mul(yp[i],tp[j]),c))
    return out

def leading(poly):
    degree=min(2*i+j for i,j in poly)
    return {"degree":degree,"coefficient":str(sum(c for(i,j),c in poly.items() if 2*i+j==degree))}

def negative_sector(cert,fault=None):
    num=parse(cert["angular_numerator_y_tau"]);den=parse(cert["angular_denominator_y_tau"])
    Y={(2,0):Q(-1),(3,0):Q(-1)}
    T={(1,0):Q(-4),(2,0):Q(-4),(3,0):Q(-1),(0,1):Q(-1)}
    de=compose(den,Y,T);gap=compose(sub(scale(den,16),num),Y,T)
    if fault=="negative sign":
        gap[max(gap)]=-1
    require(len(de)==210 and len(gap)==202,"complete negative-sector support")
    require(all(c>0 for p in [de,gap]for c in p.values()),"whole negative-sector coefficient positivity")
    require(leading(de)=={"degree":6,"coefficient":"62208"} and
            leading(gap)=={"degree":7,"coefficient":"497664"},"whole sharp-sequence leading terms")
    return {"Y":terms(Y),"T":terms(T),"whole_den":terms(de),"whole_gap16":terms(gap),
            "sharp_den_leading":leading(de),"sharp_gap_leading":leading(gap)}

def clear_positive(cert):
    num=parse(cert["angular_numerator_y_tau"]);den=parse(cert["angular_denominator_y_tau"])
    Y={(2,0):Q(-1),(3,0):Q(1)}
    M=add(ONE,Y);L={(1,0):Q(4),(2,0):Q(-4),(3,0):Q(1)}
    LM=mul(L,M);T=add(LM,mul({(0,1):Q(1)},sub(ONE,LM)))
    degree=max(j for p in [num,den]for i,j in p)
    require(degree==9,"entire lambda clearing degree")
    yp=[ONE];tp=[ONE];mp=[ONE]
    for _ in range(max(i for p in [num,den]for i,j in p)):yp.append(mul(yp[-1],Y))
    for _ in range(degree):
        tp.append(mul(tp[-1],T));mp.append(mul(mp[-1],M))
    def clear(p):
        out=ZERO
        for(i,j),c in p.items():out=add(out,scale(mul(mul(yp[i],tp[j]),mp[degree-j]),c))
        return out
    de=clear(den);gap=clear(sub(scale(den,Q(47,2)),num))
    # Entire threshold separator in u=1-v.
    U=sub(ONE,{(1,0):Q(1)})
    P=sub(add(add(scale(U,2),power(U,2)),scale(ONE,-1)),power(U,3))
    require(sub(ONE,LM)==mul(power(U,3),P),"whole threshold separator")
    require(-1+2*Q(4,9)+Q(4,9)**2-Q(4,9)**3==Q(-1,729),"exact strict containing bound")
    require(1-Q(5,9)**2==Q(56,81)>0,"clearing factor lower bound")
    return de,gap,{"Y":terms(Y),"M":terms(M),"L":terms(L),"T_numerator":terms(T)}

def affine_b(poly,left,right):
    out=ZERO
    for(i,j),c in poly.items():
        for k in range(j+1):
            key=(i,k)
            out=add(out,{key:c*comb(j,k)*left**(j-k)*(right-left)**k})
    return out

def tensor_record(poly,fault=None):
    unit={key:c*Q(5,9)**key[0]for key,c in poly.items()}
    matrix=tensor_bernstein(unit);m=len(matrix)-1;n=len(matrix[0])-1
    require([m,n]==[63,9],"entire tensor degrees")
    if fault=="tensor sign":matrix[-1][-1]=Q(-1)
    require(all(c>=0 for row in matrix for c in row),"whole nonnegative tensor")
    endpoints=[sum(matrix[i][j]>0 for i in range(m+1))for j in [0,n]]
    if fault=="endpoint":endpoints[0]=0
    require(all(endpoints),"closed endpoint strictness")
    return {"degrees":[m,n],"whole_polynomial":terms(poly),"whole_unit_polynomial":terms(unit),
            "whole_Bernstein":[[str(c)for c in row]for row in matrix],
            "positive":sum(c>0 for row in matrix for c in row),
            "zero":sum(c==0 for row in matrix for c in row),
            "endpoint_positive":endpoints}

def positive_sector(cert,cover,fault=None):
    typed_equal(cover,COVER)
    de,gap,maps=clear_positive(cert)
    dr=tensor_record(de)
    leaves=[]
    for index,(lo,hi) in enumerate(cover):
        leaf=affine_b(gap,Q(lo),Q(hi))
        leaf_fault=fault if index==3 else None
        leaves.append({"b_interval":[lo,hi],**tensor_record(leaf,leaf_fault)})
    require(dr["positive"]==619 and dr["zero"]==21,"whole denominator controls")
    require([(x["positive"],x["zero"])for x in leaves]==[(619,21),(640,0),(640,0),(640,0)],
            "whole closed-cover control counts")
    return {"substitution":maps,"whole_cleared_gap":terms(gap),"denominator":dr,
            "closed_gap_cover":leaves,"whole_Bernstein_slots":3200}

def actual_cases(cert,fault=None):
    num=parse(cert["angular_numerator_y_tau"]);den=parse(cert["angular_denominator_y_tau"])
    cases=[]
    for s,l in [(Q(36,125),Q(1)),(Q(171,1000),Q(4,5)),(Q(66,125),Q(-3)),(Q(0),None)]:
        d=[Q(-1),s,Q(1)]
        if l is None:quartic=[Q(6),Q(0),Q(-5),Q(0),Q(1)]
        else:
            B=[Q(-1),-s,Q(1)]
            quartic=u_add(u_mul(B,B),u_scale([s*s-1,-2*s,Q(1)],l))
        rc=root_count(quartic)
        require(rc["positive_distinct"]==rc["negative_distinct"]==2 and rc["zero_distinct"]==0 and rc["gcd_degree"]==0,
                "actual quartic reality/sign/multiplicity")
        f=u_mul(u_mul(d,d),quartic);h=u_scale(u_derivative(f),Q(1,8))
        hc=root_count(h);fc=root_count(f)
        if fault=="omit zero critical" and l is None:hc["zero_distinct"]=0
        require(hc["positive_distinct"]+hc["negative_distinct"]+hc["zero_distinct"]==7 and hc["gcd_degree"]==0,
                "all seven actual critical slots simple")
        require(fc["positive_distinct"]==fc["negative_distinct"]==3 and fc["zero_distinct"]==0 and fc["gcd_degree"]==2,
                "actual six original levels and two doubles")
        H=zero_matrix()
        for j in range(6):H[j+1][j]=Q(1)
        for j in range(7):H[j][6]=-h[j]
        hp=matrix_eval(u_derivative(h),H);inverse=matrix_inverse(hp)
        require(matrix_mul(hp,inverse)==identity(),"whole seven-companion inverse")
        mass=matrix_scale(matrix_mul(matrix_eval(f,H),inverse),-8)
        N=-2*f[6];X=N*N/2-4*f[4];D=X-N*N/8
        eta=matrix_trace(matrix_mul(mass,mass));C=(N*N-eta)/D
        moments=[Q(8)]
        for k in range(1,6):
            value=-k*f[8-k]
            for j in range(1,k):value-=f[8-j]*moments[k-j]
            moments.append(value)
        require(moments[1]==moments[3]==moments[5]==0 and moments[2]==N and moments[4]==X,
                "entire original first-five moments")
        require(matrix_trace(mass)==N and N>0 and D>0 and C<Q(47,2),"actual angular normalization")
        if l is not None:
            require(C==scalar(num,-s*s,l)/scalar(den,-s*s,l),"generic value matches all seven slots")
            if l<0:require(C<16,"actual negative-sector control")
        cases.append({"s":str(s),"lambda":None if l is None else str(l),
            "whole_quartic":[str(c)for c in quartic],"whole_f":[str(c)for c in f],"whole_h":[str(c)for c in h],
            "whole_Q_Sturm":rc,"whole_f_Sturm":fc,"whole_h_Sturm":hc,
            "whole_derivative_inverse":[[str(c)for c in row]for row in inverse],
            "whole_mass_matrix":[[str(c)for c in row]for row in mass],
            "moments":[str(c)for c in moments[1:]],"N":str(N),"X":str(X),"D":str(D),
            "eta_raw":str(eta),"C":str(C),"all_seven_slots_retained":True,
            "equal_magnitude_separate_even_branch":l is None})
    return cases

def build(data):
    input_schema(data);cert=data["inherited_defining_data"]
    require(sha256(canonical(cert)).hexdigest()==SOURCE_HASH,"whole inherited source fields hash")
    full={"actual_identity":actual_identity(cert),
          "negative_sector":negative_sector(cert),
          "positive_sector":positive_sector(cert,data["positive_closed_b_cover"]),
          "actual_cases":actual_cases(cert)}
    summary={"actual_agent":"six-sendov-2","role":"researcher",
        "claim_status":"complete ordinary opposite-double proof; unformalized and independently unreviewed",
        "input_source_commit":SOURCE,"input_certificate_sha256":SOURCE_HASH,
        "actual_identity_monomials":500,"negative_positive_entries":[210,202],
        "positive_full_Bernstein_entries":3200,"actual_cases":4,
        "closed_b_cover":COVER,"negative_sharp_limit":"16",
        "whole_field_sha256":{k:sha256(canonical(v)).hexdigest()for k,v in full.items()},
        "whole_record_bytes":len(canonical(full)),
        "whole_record_sha256":sha256(canonical(full)).hexdigest()}
    return summary,full

def self_test(data):
    cert=data["inherited_defining_data"]
    count=0
    for key,gate in [
        ("critical_quintic","whole actual canceled quintic"),
        ("inverse_numerators","whole actual derivative inverse identity"),
        ("discriminant","whole specialization divisor"),
        ("discriminant_divided_by_inverse_denominator","whole specialization divisor"),
        ("angular_numerator_y_tau","ENTIRE500-monomial angular identity"),
        ("angular_denominator_y_tau","whole actual denominator factor"),
    ]:
        damaged=deepcopy(cert);rows=damaged[key]
        if key in {"critical_quintic","inverse_numerators"}:rows=next(slot for slot in rows if slot)
        row=next(r for r in rows if Q(r["coefficient"])+1!=0)
        row["coefficient"]=str(Q(row["coefficient"])+1)
        try:actual_identity(damaged)
        except ValueError as e:require(str(e)==gate,"correct semantic rejection gate")
        else:raise ValueError("damaged actual identity accepted")
        count+=1
    for fault,gate in [("negative sign","whole negative-sector coefficient positivity"),
                       ("tensor sign","whole nonnegative tensor"),("endpoint","closed endpoint strictness"),
                       ("omit zero critical","all seven actual critical slots simple")]:
        try:
            if fault=="omit zero critical":actual_cases(cert,fault)
            elif fault=="negative sign":negative_sector(cert,fault)
            else:positive_sector(cert,COVER,fault)
        except ValueError as e:require(str(e)==gate,"correct sector rejection gate")
        else:raise ValueError("damaged sector proof accepted")
        count+=1
    return count

def main():
    p=ArgumentParser()
    p.add_argument("--input",type=Path,default=BASE/"INPUT.json")
    p.add_argument("--expected",type=Path,default=BASE/"EXPECTED.json")
    p.add_argument("--write-whole-record",type=Path)
    p.add_argument("--self-test",action="store_true")
    args=p.parse_args()
    data=load_json(args.input);summary,full=build(data)
    typed_equal(summary,load_json(args.expected))
    rejects=self_test(data)if args.self_test else 0
    if args.write_whole_record:args.write_whole_record.write_bytes(canonical(full))
    print(json.dumps({"complete":True,"whole_record_bytes":summary["whole_record_bytes"],
        "whole_record_sha256":summary["whole_record_sha256"],"all3200controls_paid":True,
        "actual_cases":4,"semantic_rejections":rejects,"whole_compact_fixture_matches":True}))

if __name__=="__main__":main()
