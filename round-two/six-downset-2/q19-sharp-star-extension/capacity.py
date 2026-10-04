"""Exact four-type degree-capacity reduction and unavoidable NN mass penalties.

This concerns necessary entry/degree conditions; sufficiency for the entire
H matrix is not asserted by an interval or by a feasible KK flow.
"""
import argparse
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
from model import canonical, choose, coefficient_input, comparison, require, type_budgets


def interval(m,dYY,dB,dBC,cYY,cYB,cYBC,cBC,tau):
    require(type(m) is int and m>=4 and all(type(x) is F for x in
            (dYY,dB,dBC,cYY,cYB,cYBC,cBC,tau)), 'exact count/capacity domain')
    require(dYY>0 and dB>0 and dBC>0 and tau>=0, 'strict bad degrees and nonnegative floor')
    n=F(choose(m-1,2));a=F(choose(m-2,2));p=F(m-2)
    beta=(dBC+tau)/n
    A=dYY+tau-p*beta
    lower=max(F(0),(A-a*(cYY-tau))/(2*p),
              (dB+tau-(m-1)*(cBC-tau))/n)
    upper=min(cYB-tau,A/(2*p),(dB+tau)/n)
    feasible=0<=beta<=cYBC-tau and lower<=upper
    return dict(beta=beta,lower=lower,upper=upper,feasible=feasible)


def bad_sets(m):
    """Literal YY,bY,cY,bcY sets on named points, separate from count formulas."""
    ys=[('y',i) for i in range(m)]
    b=('core','b');c=('core','c')
    out=[('YY',frozenset(v)) for v in combinations(ys,2)]
    out += [('bY',frozenset((b,y))) for y in ys]
    out += [('cY',frozenset((c,y))) for y in ys]
    out += [('bcY',frozenset((b,c,y))) for y in ys]
    return out


def literal_flow(m,dYY,dB,dBC,cYY,cYB,cYBC,cBC,tau,zeta):
    result=interval(m,dYY,dB,dBC,cYY,cYB,cYBC,cBC,tau)
    require(result['feasible'] and result['lower']<=zeta<=result['upper'], 'complete interval membership')
    beta=result['beta']
    alpha=(dYY+tau-(m-2)*(beta+2*zeta))/choose(m-2,2)
    eta=(dB+tau-choose(m-1,2)*zeta)/(m-1)
    vertices=bad_sets(m);degrees=[F(0)]*len(vertices);count=0
    kinds={('YY','YY'):(alpha,cYY),('YY','bY'):(zeta,cYB),
           ('YY','cY'):(zeta,cYB),('YY','bcY'):(beta,cYBC),('bY','cY'):(eta,cBC)}
    for i,(tag,v) in enumerate(vertices):
        for j,(other,w) in enumerate(vertices[i+1:],i+1):
            if v.isdisjoint(w):
                amount,capacity=kinds[(tag,other)]
                require(0<=amount<=capacity-tau,'each individual original KK edge capacity')
                degrees[i]+=amount;degrees[j]+=amount;count+=1
    demand={'YY':dYY,'bY':dB,'cY':dB,'bcY':dBC}
    require(all(a==demand[tag]+tau for a,(tag,v) in zip(degrees,vertices)),
            'EVERY individual bad degree, no unexamined row')
    return dict(vertices=len(vertices),individual_degree_checks=len(vertices),individual_KK_edge_checks=count,
                alpha=str(alpha),beta=str(beta),zeta=str(zeta),eta=str(eta),
                decreasing_mass=str(sum(degrees)/2),necessary_flow_only=True)


def q19_data(raw_table):
    table=comparison(raw_table,9,10);b=type_budgets(table,9,10)
    yy,by,cy,bcy=(0,0,2),(2,0,1),(4,0,1),(6,0,1)
    require(b['bad_nn']==[yy,by,cy,bcy] and b['ell'][by]==b['ell'][cy], 'actual four bad types/equal light degrees')
    cap=lambda t,u:1+table[tuple(sorted((t,u)))]
    require(cap(yy,by)==cap(yy,cy),'symmetric light capacities')
    data=[-b['ell'][yy],-b['ell'][by],-b['ell'][bcy],
          cap(yy,yy),cap(yy,by),cap(yy,bcy),cap(by,cy)]
    return table,b,data


def affine_constraints(m,data):
    """Every interval inequality as an exact intercept+slope*tau >= 0."""
    dYY,dB,dBC,cYY,cYB,cYBC,cBC=data
    n=F(choose(m-1,2));a=F(choose(m-2,2));p=F(m-2)
    A=(dYY-p*dBC/n,1-p/n)
    lo=[('zero',(F(0),F(0))),
        ('alpha_capacity',((A[0]-a*cYY)/(2*p),(A[1]+a)/(2*p))),
        ('eta_capacity',((dB-(m-1)*cBC)/n,F(m)/n))]
    hi=[('zeta_capacity',(cYB,F(-1))),
        ('alpha_sign',(A[0]/(2*p),A[1]/(2*p))),
        ('eta_sign',(dB/n,1/n))]
    result=[dict(label=lname+' <= '+hname,intercept=hval[0]-lval[0],slope=hval[1]-lval[1])
            for lname,lval in lo for hname,hval in hi]
    result += [dict(label='beta_nonnegative',intercept=dBC,slope=F(1)),
               dict(label='beta_capacity',intercept=n*cYBC-dBC,slope=-n-1)]
    return result


def penalty_data(table,b):
    K=set(b['bad_nn']);k,m=b['k'],b['m'];out=[]
    for (t,u),val in sorted(table.items()):
        if t[0]&1 or u[0]&1 or not (t in K or u in K):continue
        require(not t[0]&u[0],'actual disjoint bad capacity type')
        d=choose(k-t[1],u[1])*choose(m-t[2],u[2])
        e=choose(k-u[1],t[1])*choose(m-u[2],t[2])
        require(b['weights'][t]*d==b['weights'][u]*e,'whole incidence multiplicity symmetry')
        number=F(b['weights'][t]*d,2 if t==u else 1)
        require(number.denominator==1 and number>0,'positive integer unordered multiplicity')
        kind='KK' if t in K and u in K else 'KG'
        out.append(dict(types=[t,u],kind=kind,unordered_count=number.numerator,
                        capacity=1+val,penalty_factor=F(1) if kind=='KK' else F(1,2)))
    return out


def envelope(tau,b,penalties):
    require(type(tau) is F and tau>=0,'exact nonnegative floor')
    nbad=sum(b['weights'][t] for t in b['bad_nn'])
    extra=sum(x['penalty_factor']*x['unordered_count']*max(tau-x['capacity'],F(0)) for x in penalties)
    return dict(tau=str(tau),base_mass=str(b['P0']+F(nbad+1,2)*tau),
                unavoidable_capacity_penalty=str(extra),
                necessary_total_NN_positive_mass=str(b['P0']+F(nbad+1,2)*tau+extra),
                necessary_for_ALL_individual_real_H_competitors=True,
                H_existence_or_full_primal_feasibility_NOT_claimed=True)


def run(path):
    raw=coefficient_input(path);table,b,data=q19_data(raw)
    conditions=affine_constraints(10,data)
    require(all(x['intercept']>=0 for x in conditions),'entire KK interval contains zero')
    bounds=[(-x['intercept']/x['slope'],x['label']) for x in conditions if x['slope']<0]
    maximum,label=min(bounds)
    require(maximum==F(25083,32768) and label=='eta_capacity <= eta_sign', 'exact KK-only threshold')
    require(all(x['intercept']+x['slope']*maximum>=0 for x in conditions), 'every affine bound at threshold')
    flows=[]
    for tau in [F(0),F(1,128),maximum]:
        iv=interval(10,*data,tau)
        require(iv['feasible'],'fresh KK floor-feasible point')
        flows.append(dict(tau=str(tau),zeta_interval=[str(iv['lower']),str(iv['upper'])],
                          literal_flow=literal_flow(10,*data,tau,iv['lower'])))
    beyond=interval(10,*data,maximum+F(1,32768))
    require(not beyond['feasible'],'KK capacity impossibility beyond exact threshold')
    penalties=penalty_data(table,b)
    require(sum(x['unordered_count'] for x in penalties if x['kind']=='KK')==1800 and
            sum(x['unordered_count'] for x in penalties if x['kind']=='KG')==10820,
            'all actual penalty-class multiplicities')
    first=min(x['capacity'] for x in penalties)
    active=[x for x in penalties if x['capacity']==first]
    require(first==F(3755,8192) and len(active)==1 and active[0]['kind']=='KG' and
            active[0]['unordered_count']==405,'first unavoidable positive capacity penalty')
    # Literal feasibility and two genuinely infeasible degree/capacity controls.
    controls=[]
    for name,m,args,expected in [
        ('small_feasible',4,[F(2),F(1),F(1)]+[F(10)]*4,True),
        ('bc_degree_cone',4,[F(1),F(1),F(10)]+[F(100)]*4,False),
        ('YY_degree_capacity',4,[F(100),F(1),F(1)]+[F(1)]*4,False)]:
        iv=interval(m,*args,F(0))
        require(iv['feasible']==expected,'exact degree/capacity hand control')
        rec=dict(name=name,feasible=iv['feasible'],beta=str(iv['beta']),
                 zeta_interval=[str(iv['lower']),str(iv['upper'])])
        if expected:rec['literal_flow']=literal_flow(m,*args,F(0),iv['lower'])
        controls.append(rec)
    return dict(agent='six-downset-2',role='researcher',k=9,m=10,
                bad_capacities_and_demands=[str(a) for a in data],
                exact_KK_only_feasible_tau_interval=['0',str(maximum)],
                KK_interval_original_PSD_star_GG_sufficiency_NOT_claimed=True,
                affine_inequalities=[dict(label=x['label'],intercept=str(x['intercept']),slope=str(x['slope'])) for x in conditions],
                complete_individual_KK_flows=flows,hand_controls=controls,
                all_penalty_types=[{**x,'capacity':str(x['capacity']),'penalty_factor':str(x['penalty_factor'])} for x in penalties],
                first_capacity_penalty_tau=str(first),first_penalty_count=405,
                minimum_mass_sharpness_impossible_above_first_capacity_threshold=True,
                representative_envelopes=[envelope(t,b,penalties) for t in
                    [F(0),F(1,128),first,first+F(1,8192),maximum]],
                ALL_real_interval_averaging_proof_ordinary_unformalized='STRUCTURAL.md')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--coefficients',required=True);p.add_argument('--out',required=True)
    args=p.parse_args();record=run(args.coefficients);raw=canonical(record)+b'\n';Path(args.out).write_bytes(raw)
    import hashlib
    print(json.dumps(dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),
                          KK_only_interval=record['exact_KK_only_feasible_tau_interval'],
                          first_unavoidable_penalty_tau=record['first_capacity_penalty_tau'])))
