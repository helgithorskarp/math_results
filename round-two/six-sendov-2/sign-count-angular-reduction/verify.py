#!/usr/bin/env python3
"""Exact finite algebra for the sign-count angular reduction; standard library."""
from fractions import Fraction as F
from pathlib import Path
import argparse, hashlib, json, sys, time

def need(ok, message):
    if not ok: raise ValueError(message)

def add(*ps):
    out={}
    for p in ps:
        for k,v in p.items(): out[k]=out.get(k,F(0))+v
    return {k:v for k,v in out.items() if v}

def mul(a,b):
    out={}
    for k,v in a.items():
        for l,w in b.items():
            t=tuple(x+y for x,y in zip(k,l));out[t]=out.get(t,F(0))+v*w
    return {k:v for k,v in out.items() if v}

def scale(a,c):return {k:v*c for k,v in a.items() if v*c}
def power(a,n):
    out={(0,)*len(next(iter(a))):F(1)}
    for _ in range(n):out=mul(out,a)
    return out

def canonical(p):return [[list(k),str(v)] for k,v in sorted(p.items())]
def invariant(u):
    need(sum(u)==0,'literal profile is unbalanced')
    N=sum(x*x for x in u);need(N>0,'zero profile')
    return {'u':list(u),'N':str(N),'S4':str(sum(x**4 for x in u)),'X':str(F(sum(x**4 for x in u),N*N))}

def calculate():
    records=[]
    def record(name,value):records.append({'name':name,'value':value})
    bound=F(13,84)
    for n in [7,8]:
        for k in range(1,4):
            m=n-k;X=F(m**3+k**3,m*k*n*n)
            need(X>=bound,'two-level moment below barrier')
            record(f'two-level-{n}-{k}',{'negative':m,'positive':k,'X':str(X),'gap':str(X-bound)})
    admissible=[]
    for n in [7,8]:
        for m in range(1,n-1):
            k=n-1-m
            item={'support':n,'multiplicities':[m,1,k]}
            if m==1 or k==1:item['excluded']='outer root would be zero'
            else:
                left=F(-1);right=F(m-1,k-1);middle=-left-right
                levels=[left,middle,right];item['levels']=[str(t) for t in levels]
                if not left<middle<right:item['excluded']='root order'
                elif middle==0:item['excluded']='zero is not in the active support'
                else:
                    positive=k+int(middle>0);negative=m+int(middle<0)
                    if min(positive,negative)>3:item['excluded']='outside sign sector'
                    else:
                        N=m*left**2+middle**2+k*right**2
                        X=(m*left**4+middle**4+k*right**4)/N**2
                        need(X>bound,'three-level minimum candidate below barrier')
                        hessian=4*(middle-left)*(middle-right)
                        need(hessian<0,'middle splitting sign')
                        item.update({'X':str(X),'gap':str(X-bound),'sign_counts':[negative,positive],'middle_hessian':str(hessian)})
                        admissible.append((n,m,k))
            record(f'three-level-{n}-{m}',item)
    need(admissible==[(8,3,4),(8,4,3)],'complete three-level case list')
    record('small-support',{'holder_lower':'1/6','gap':str(F(1,6)-bound)})
    eq=invariant([4]*3+[-3]*4+[0]);need(F(eq['X'])==bound,'sign equality profile')
    record('sign-equality',eq)
    eq5=invariant([3]*5+[-5]*3);need(F(eq5['X'])==F(19,120),'fivefold equality profile')
    record('fivefold-equality',eq5)
    a={(1,0,0):F(1)};x={(0,1,0):F(1)};y={(0,0,1):F(1)};t=[x,y,scale(add(x,y),F(-1))]
    tau=add(*(power(v,2) for v in t));T3=add(*(power(v,3) for v in t));T4=add(*(power(v,4) for v in t))
    need(T4==scale(power(tau,2),F(1,2)),'balanced triple fourth identity')
    record('balanced-triple-fourth',canonical(T4))
    discriminant=power(mul(mul(add(t[0],scale(t[1],F(-1))),add(t[1],scale(t[2],F(-1)))),add(t[2],scale(t[0],F(-1)))),2)
    need(add(power(tau,3),scale(power(T3,2),F(-6)))==scale(discriminant,F(2)),'balanced triple cubic identity')
    record('balanced-triple-cubic',canonical(scale(discriminant,F(2))))
    center=scale(a,F(-5,3));u=[a]*5+[add(center,v) for v in t]
    N=add(*(power(v,2) for v in u));S4=add(*(power(v,4) for v in u))
    need(N==add(scale(power(a,2),F(40,3)),tau),'fivefold norm identity')
    record('fivefold-norm',canonical(N))
    target=add(scale(power(a,4),F(760,27)),scale(mul(power(a,2),tau),F(50,3)),scale(mul(a,T3),F(-20,3)),scale(power(tau,2),F(1,2)))
    need(S4==target,'fivefold fourth moment expansion')
    record('fivefold-fourth',canonical(S4))
    constants={'base':F(760,27)*F(3,40)**2,'quadratic_variance':F(50,3)*F(3,40),'cubic_bound_square':F(20,3)**2*F(3,40)/6}
    need(constants=={'base':F(19,120),'quadratic_variance':F(5,4),'cubic_bound_square':F(5,9)},'normalized heavy coefficients')
    record('normalized-heavy-coefficients',{k:str(v) for k,v in constants.items()})
    q={(1,):F(1)};one={(0,):F(1)};A=add(scale(one,F(112)),scale(q,F(-71)))
    Q=add(power(A,2),scale(mul(q,add(one,scale(q,F(-1)))),F(-8000)))
    need(Q=={(0,):F(12544),(1,):F(-23904),(2,):F(13041)},'heavy squared comparison')
    completed=add(power(add(scale(q,F(26082)),scale(one,F(-23904))),2),scale(one,F(82944000)))
    need(scale(Q,F(4*13041))==completed,'positive quadratic completion')
    record('heavy-positive-quadratic',{'polynomial':canonical(Q),'completion_constant':82944000,'minimum':str(F(82944000,4*13041)),'positive_linear_min':41})
    gap=bound-F(1,8);need(gap==F(5,168),'sign denominator gap')
    bounds={str(r):str(F(r-2,r-1)/gap) for r in range(2,9)}
    need(bounds['4']=='112/5','four-level angular barrier')
    need(F(2,3)/(F(19,120)-F(1,8))==20,'heavy angular barrier')
    record('angular-bounds',{'sign_moment_gap':str(gap),'sign_by_levels':bounds,'heavy_four_level':20,'strictness':'moment equality has only two or three original levels'})
    record('threshold-order',{'sign_below_49_2':str(F(49,2)-F(112,5)),'heavy_below_49_2':str(F(49,2)-20)})
    # Necessary sign chart for a=1 in the4+2+1+1 family.
    record('four-two-chart',{'b_interval':['-2','0'],'V_interval':['0','(b+2)^2'],'identity':'both singletons negative iff b>-2 and V<(b+2)^2'})
    return records

def controls():
    rejected=0
    def reject(action):
        nonlocal rejected
        try:action()
        except ValueError:rejected+=1
        else:raise ValueError('damaged claim accepted')
    reject(lambda:invariant([3]*5+[-5,-5,-4]))
    reject(lambda:need(F(2,3)/F(13,84)==F(112,5),'omitted denominator shift'))
    uniform=[1]*4+[-1]*4
    reject(lambda:need(min(sum(x>0 for x in uniform),sum(x<0 for x in uniform))<=3,'uniform wrongly included in sign sector'))
    reject(lambda:need(4*(F(-1,2)+1)*(F(-1,2)-F(3,2))>0,'middle Hessian sign reversed'))
    return rejected

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write-expected',action='store_true');parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'));args=parser.parse_args()
    start=time.monotonic();records=calculate();damage=controls();text=json.dumps(records,indent=2)+'\n'
    if args.write_expected:args.expected.write_text(text)
    need(json.loads(args.expected.read_text())==records,'expected fixture differs')
    canonical_text=json.dumps(records,sort_keys=True,separators=(',',':'))
    print(json.dumps({'checks':len(records),'damage_controls':damage,'record_sha256':hashlib.sha256(canonical_text.encode()).hexdigest(),'elapsed_seconds':round(time.monotonic()-start,6)}))
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,json.JSONDecodeError) as error:print('verification failed: '+str(error),file=sys.stderr);raise SystemExit(1)
