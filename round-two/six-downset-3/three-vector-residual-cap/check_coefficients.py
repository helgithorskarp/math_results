"""standard-library coefficient verifier, no CAS imported.

Reconstructs original counted actions directly from a cleared literal
table; checks every symbolic second moment through its physical frame;
then checks all slack expansions and norm quotient/sandwich identities.
Same author as CAS derivation; algorithm independence is not peer review.
"""
from pathlib import Path
from math import comb
import json
import time
import resource
import residual
from algebra import add,mul,scale,constant,Q,K,ONE,twice_e
F,require=residual.F,residual.require


def load(name,expected):
    data=json.loads(Path(__file__).with_name(name).read_text())
    got=data.pop('record_sha256')
    require(residual.digest(data)==got==expected,'entire certificate record: '+name)
    return data


def decode(entries):
    return {tuple(p):F(c) for p,c in entries if F(c)}


def product(*terms):
    result=ONE
    for p in terms:result=mul(result,p)
    return result


def power(p,n):
    result=ONE
    for _ in range(n):result=mul(result,p)
    return result


def substitute(p,a,b):
    aa=[power(a,i) for i in range(max((i for i,j in p),default=0)+1)]
    bb=[power(b,j) for j in range(max((j for i,j in p),default=0)+1)]
    return add(*(scale(mul(aa[i],bb[j]),c) for (i,j),c in p.items()))


def choose(n,r):
    return (ONE,n,scale(mul(n,add(n,constant(-1))),F(1,2)))[r]


def physical_residual(rn,d0):
    qm1,qm2,qm3=(add(Q,constant(-i)) for i in (1,2,3))
    dt=product(Q,qm1,qm2,qm3);dt_q=product(qm1,qm2,qm3)
    s=add(scale(Q,3),constant(4))
    N=add(scale(add(mul(Q,Q),scale(Q,13),constant(16)),F(1,2)),scale(K,-1))
    gap=add(N,scale(s,-1));ell=add(scale(Q,5),constant(4),scale(K,-1))
    tab={}
    o,p,a,b,c,d,e=(0,1),(0,2),(1,0),(1,1),(2,0),(2,1),(3,0)
    put=lambda x,y,v:tab.__setitem__(tuple(sorted((x,y))),v)
    put(o,o,product(add(constant(6),scale(mul(Q,Q),-1),scale(Q,-4)),qm2,qm3))
    put(o,p,product(Q,Q,qm3,qm3))
    put(p,p,add(scale(qm1,12),scale(mul(Q,Q),4),scale(product(s,Q,qm1),-2),product(Q,Q,qm1,qm1)))
    for leaf,alpha,beta,gamma in ((o,add(dt,scale(dt_q,-1)),add(dt,dt_q),add(dt,scale(dt_q,6))),
                                  (p,dt,add(dt,scale(product(qm1,qm1,qm3),2)),add(dt,scale(dt_q,6)))):
        for core,value in ((a,alpha),(c,alpha),(b,beta),(d,beta),(e,gamma)):put(leaf,core,value)
    rr=add(scale(dt,3),scale(dt_q,2))
    ww=product(add(scale(mul(Q,Q),3),Q,constant(-2)),qm2,qm3)
    for x,y,v in ((a,a,{}),(a,b,{}),(b,b,{}),(a,c,scale(dt,2)),(a,d,rr),(b,c,rr),(b,d,ww)):put(x,y,v)
    keys=residual.orbits.forms(6,2)['keys']
    weights=[mul(choose(K,z),choose(add(Q,scale(K,-1)),w)) for cc,z,w in keys]
    fs=[[1,int(cc==1 and z+w==1),int(bool(cc&6) and not(cc in (3,5) and z+w==0))] for cc,z,w in keys]
    acts=[]
    for i,(cc,z,w) in enumerate(keys):
        rows=[scale(mul(gap,dt),f) for f in fs[i]]
        for j,(ccc,zz,ww) in enumerate(keys):
            if cc&ccc:continue
            count=mul(choose(add(K,constant(-z)),zz),choose(add(Q,scale(K,-1),constant(-w)),ww))
            base=tab[tuple(sorted(((cc.bit_count(),z+w),(ccc.bit_count(),zz+ww))))]
            term=mul(count,base)
            for v in range(3):
                if fs[j][v]:rows[v]=add(rows[v],scale(term,-1))
        acts.append(rows)
    first=[[add(*(scale(mul(weights[i],acts[i][b]),fs[i][a]) for i in range(23))) for b in range(3)] for a in range(3)]
    second=[[add(*(product(weights[i],acts[i][a],acts[i][b]) for i in range(23))) for b in range(3)] for a in range(3)]
    gap2=scale(gap,2)
    aq=add(mul(add(scale(K,2),ONE),mul(Q,Q)),mul(K,Q),scale(K,-2))
    cc=mul(ell,add(ONE,scale(K,-1)))
    bq=add(mul(Q,add(mul(add(Q,scale(K,-1)),s),scale(K,3))),scale(K,2))
    t2=mul(Q,gap2);v2=add(mul(ell,gap2),scale(mul(Q,s),-8))
    expected=[[scale(mul(twice_e(),dt),F(1,2)),mul(aq,dt_q),mul(cc,dt)],
              [mul(aq,dt_q),scale(mul(t2,dt),F(1,2)),scale(mul(bq,dt_q),-1)],
              [mul(cc,dt),scale(mul(bq,dt_q),-1),scale(mul(v2,dt),F(1,2))]]
    require(first==expected,'every entire first moment from original cleared table')
    r2=add(mul(Q,Q),Q,constant(6));df=product(Q,ell,r2)
    t=scale(mul(Q,ell),2)
    inv=[[t,scale(t,-1),scale(t,-1)],
         [scale(t,-1),add(mul(ell,r2),t),t],
         [scale(t,-1),t,add(mul(Q,r2),t)]]
    dr=product(dt,dt,df)
    checks=0
    for a,b in ((0,0),(0,1),(0,2),(1,1),(1,2),(2,2)):
        projected=add(*(product(first[a][i],inv[i][j],first[j][b]) for i in range(3) for j in range(3)))
        numerator=add(mul(second[a][b],df),scale(projected,-1))
        require(mul(numerator,d0)==mul(rn[str(a)+str(b)],dr),'entire symbolic physical second moment '+str(a)+str(b))
        checks+=1
    return checks


def cleared_slack(forms,rn):
    ell=add(scale(Q,5),constant(4),scale(K,-1));s=add(scale(Q,3),constant(4))
    gap2=add(mul(Q,Q),scale(Q,7),constant(8),scale(K,-2))
    gc2=add(mul(Q,Q),Q,scale(K,-2))
    t2=mul(Q,gap2);v2=add(mul(ell,gap2),scale(mul(Q,s),-8))
    aq=add(mul(add(scale(K,2),ONE),mul(Q,Q)),mul(K,Q),scale(K,-2))
    c=mul(ell,add(ONE,scale(K,-1)))
    bq=add(mul(Q,add(mul(add(Q,scale(K,-1)),s),scale(K,3))),scale(K,2))
    dn=add(product(Q,Q,t2,v2),scale(mul(bq,bq),-4))
    an=scale(mul(Q,add(mul(v2,aq),scale(mul(bq,c),2))),2)
    bn=scale(add(product(Q,Q,t2,c),scale(mul(bq,aq),2)),2)
    d0=product(power(Q,3),add(Q,constant(-2)),power(add(Q,constant(-1)),2),ell,add(mul(Q,Q),Q,constant(6)))
    ww=add(product(rn['00'],dn,dn),scale(product(an,dn,rn['01']),-2),scale(product(bn,dn,rn['02']),-2),
           product(an,an,rn['11']),scale(product(an,bn,rn['12']),2),product(bn,bn,rn['22']))
    eta=add(scale(product(Q,Q,add(mul(v2,rn['11']),mul(t2,rn['22']))),2),scale(product(Q,bq,rn['12']),8))
    numerator=add(product(gc2,d0,dn,dn),scale(add(mul(eta,dn),ww),-2))
    denominator=scale(product(d0,dn,dn),2)
    qnum=add(product(Q,twice_e(),dn),scale(mul(an,aq),-2),scale(product(Q,bn,c),-2))
    qden=scale(mul(Q,dn),2)
    expected={'d0':d0,'Dn':dn,'Rww_numerator':ww,'eta_numerator':eta,
              'numerator':numerator,'denominator':denominator,'Q_numerator':qnum,'Q_denominator':qden}
    require(expected==forms,'all entire cleared residual, trace, slack and scalar identities')


def old_mean(pell):
    qm1,qm2=add(Q,constant(-1)),add(Q,constant(-2))
    d=product(Q,qm1,qm2);dq=mul(qm1,qm2)
    ww=mul(add(scale(mul(Q,Q),2),scale(Q,2),constant(-2)),qm2)
    rows=[(add(scale(Q,5),constant(6),scale(K,-1)),mul(add(ONE,scale(K,-1)),d)),
          (ONE,add(mul(add(ONE,scale(K,2)),d),scale(mul(K,dq),2))),
          (K,mul(add(K,constant(-1)),ww)),
          (add(Q,scale(K,-1)),add(d,mul(K,ww))),
          (K,mul(add(K,constant(-1)),dq)),
          (add(Q,scale(K,-1)),add(d,mul(K,dq)))]
    for z in range(3):
        count=mul(choose(K,z),choose(add(Q,scale(K,-1)),2-z))
        value=add(scale(d,1-z),scale(mul(add(K,constant(-z)),mul(qm1,qm1)),2))
        rows.append((count,value))
    v=add(*(product(count,value,value) for count,value in rows))
    e=twice_e();n2=add(mul(Q,Q),scale(Q,13),constant(14),scale(K,-2));g2=add(mul(Q,Q),Q,scale(K,-2))
    numerator=add(product(e,n2,g2,d,d),scale(mul(n2,v),-4),scale(product(e,e,d,d),2))
    denominator=scale(product(n2,g2,d,d),2)
    require(numerator==decode(pell['mean_numerator']) and denominator==decode(pell['mean_denominator']),
            'entire old mean margin from independently cleared nine rows')


def shift_global(p,at):
    # Independently expands q=5k+u,k=at+x by the binomial theorem.
    result={}
    for (i,j),c in p.items():
        for b in range(i+1):
            degree=i-b+j
            t=c*comb(i,b)*5**(i-b)
            for a in range(degree+1):
                exponent=(a,b)
                result[exponent]=result.get(exponent,F(0))+t*comb(degree,a)*at**(degree-a)
    return {p:c for p,c in result.items() if c}


def norm_check(original,certificate):
    # Variables now represent P,k. Verify the complete quotient identity.
    replace=add(scale(K,3),scale(Q,F(1,2)),constant(F(-25,2)))
    norm=add(mul(Q,Q),scale(mul(K,K),-28),scale(K,-36),constant(-81))
    quotient=decode(certificate['quotient_coefficients']);remainder=decode(certificate['remainder_coefficients'])
    require(substitute(original,replace,K)==add(mul(quotient,norm),remainder),'entire norm quotient identity')
    f={p:c for p,c in remainder.items() if p[0]==0}
    g={(0,j):c for (i,j),c in remainder.items() if i==1}
    require(all(i<=1 for i,j in remainder),'norm remainder degree')
    at=certificate['minimum_k'];shift=add(K,constant(at))
    f1=substitute(f,Q,shift);g1=substitute(g,Q,shift)
    # Stored univariate x exponent is position zero; transpose it here.
    stored=lambda entries:{(0,p[0]):F(c) for p,c in entries if F(c)}
    require(f1==stored(certificate['shifted_f']) and g1==stored(certificate['shifted_g']),'every shifted norm coefficient')
    pos={p:c for p,c in g1.items() if c>0};neg={p:c for p,c in g1.items() if c<0}
    low=add(scale(shift,5),constant(9));high=add(scale(shift,F(16,3)),constant(3))
    lower=add(f1,mul(pos,low),mul(neg,high))
    require(lower==stored(certificate['coefficient_sandwich']) and lower.get((0,0),F(0))>0 and all(c>=0 for c in lower.values()),'every norm coefficient sandwich')
    return len(lower)


def run():
    start=time.perf_counter()
    slack=load('POLYNOMIAL-SLACK.json','9accb1e7993765314f92a27597b05a44e6701f03d0fd42aee9aec4be068e2ac6')
    pell=load('PELL-NORM.json','8fa1f8c909bb468232c113375ccdfa10e3d82ccfe5058d3476bb6af103db0f91')
    rr=load('RESIDUAL-NUMERATORS.json','cedbf5cb6116f42219249efce91128829ebbab0ce32affef14e070e58b6967b5')
    forms={name:decode(x) for name,x in slack['forms'].items()};rn={name:decode(x) for name,x in rr.items()}
    checks=physical_residual(rn,forms['d0'])
    cleared_slack(forms,rn)
    old_mean(pell)
    print('All six entire original physical second-moment identities pass',time.perf_counter()-start,flush=True)
    shifted=shift_global(forms['numerator'],25)
    require(shifted==decode(slack['global_slack']['coefficients']) and shifted.get((0,0),F(0))>0 and all(c>=0 for c in shifted.values()),'every independent uniform slack coefficient')
    normcounts=[norm_check(add(forms['Q_numerator'],scale(forms['Q_denominator'],-1)),pell['Q_minus_one']),
                norm_check(scale(decode(pell['mean_numerator']),-1),pell['negative_old_mean'])]
    # Recurrence is a full polynomial identity; endpoint comparisons are in the ordinary proof.
    nextk=add(scale(K,8),scale(Q,F(3,2)),constant(F(9,2)))
    nextp=add(scale(Q,8),scale(K,42),constant(27))
    norm=add(mul(Q,Q),scale(mul(K,K),-28),scale(K,-36),constant(-81))
    require(substitute(norm,nextp,nextk)==norm,'entire Pell recurrence norm invariant')
    # Actual parameter formula works without the earlier 40-step floor guard.
    parameters=[residual.encode(residual.rational_point(q,k)) for q,k in ((91,18),(1666,297),(26767,4743))]
    result={'agent':'six-downset-3','role':'researcher','status':'exact portable certificate checks; ordinary bridges unformalized',
            'entire_original_first_moment_entries':9,
            'entire_physical_second_moment_identities':checks,
            'entire_cleared_residual_trace_slack_scalar_identities':8,
            'entire_independently_rebuilt_old_mean_polynomials':2,
            'uniform_coefficients':len(shifted),
            'norm_sandwich_coefficient_counts':normcounts,'entire_norm_recurrence':True,
            'new_explicit_rational_parameters':parameters}
    result['record_sha256']=residual.digest(result)
    Path(__file__).with_name('PORTABLE-CHECK.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'digest':result['record_sha256'],'seconds':time.perf_counter()-start,
                      'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      'uniform_coefficients':len(shifted),'norm_counts':normcounts}))


if __name__=='__main__':run()
