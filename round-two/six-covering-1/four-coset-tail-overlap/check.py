"""Complete integer bitset certificate; CPython standard library only."""
from argparse import ArgumentParser
from itertools import combinations_with_replacement,product
import json
from math import gcd
from pathlib import Path
HERE=Path(__file__).resolve().parent

def need(ok,message):
    if not ok:raise RuntimeError(message)

def allocations(prefix=(0,),high=0):
    if len(prefix)==7:
        yield prefix;return
    for s in range(min(high+1,4)+1):
        yield from allocations(prefix+(s,),max(high,s))

def top(hist,h):
    score=0
    for k in range(len(hist)-1,-1,-1):
        take=min(h,hist[k]);score+=k*take;h-=take
    need(h==0,'target size exceeds domain');return score

def bins(Q,F):
    one=two=four=0
    for m in Q:
        c1=one&m;one^=m;c2=two&c1;two^=c1;four^=c2
    return [(one if k&1 else F^one)&(two if k&2 else F^two)&
            (four if k&4 else F^four) for k in range(6)]

def validate(c):
    need(c.get('schema')==1,'schema')
    need((c.get('candidate_period'),c.get('target_remainder4'),c.get('omitted_remainder9'),c.get('copy_prime'))==(720,0,6,7),'target domain')
    need(c.get('original_cofactors')==[d for d in range(2,721) if 720%d==0],'original resource inventory')
    need(c.get('whole_copy_cofactors')==[2,4],'whole-copy resources')
    need(c.get('selected_cofactors')==[8,3,6,12,5,10,20],'selected original resources')
    need(c.get('nine_cofactors')==[9,18,36] and c.get('four_cofactor')==16,'additional original resources')
    need((c.get('tested_holes'),c.get('conditional_upper'))==(111,110),'subset reduction boundary')
    need((c.get('other_resource_mass'),c.get('joint_threshold'))==(144,411),'capacity or threshold')
    need(c.get('equality_histogram')==[40,20,20,30,15,15,10,5,5,0],'equality histogram')
    need((c.get('equality_union_extra_ceiling'),c.get('equality_overlap_loss'))==(85,15),'equality overlap claim')
    need(c.get('global_L_min_8_improved') is False and c.get('tail_completion_asserted') is False,'scope')

def equality(Q,A,C,b,s9,r9,s4,r4,hist,copies,c):
    need(len(set(A))==len(set(C))==1 and A[0] in (1,2),'equality phase family')
    need(copies[:4]==(0,1,2,3) and sorted(copies[4:])==[1,2,3],'equality allocation')
    need(s9==s4==4 and r9%3==A[0] and r4%2==b,'equality selector')
    need(hist==c['equality_histogram'],'equality histogram differs')
    S={t for t in range(180) if t%9!=6}
    aa={t for t in S if t%3==A[0]};bb={t for t in S if t%2==b};cc={t for t in S if t%5==C[0]}
    QQ=[bb]+[aa|cc]*3+[set()];U=aa|bb|cc
    need([{t for t in S if m>>t&1} for m in Q]==QQ,'literal selected copy unions differ')
    need(len(U)==120 and sum(len(z) for z in QQ)==320,'equality physical support or mass')
    V={t for t in S if t%9==r9};W={t for t in S if t%4==r4}
    values={t:sum(t in q for q in QQ)+3*(t in V)+(t in W) for t in S}
    mandatory={t for t in S if values[t]>=2}
    need(len(mandatory)==100 and aa|W<=mandatory and {t for t in S if values[t]>0}==U,'mandatory equality points')
    need(sum(sorted(values.values(),reverse=True)[:111])==411,'literal equality top sum')
    # Every111-set attaining411 contains mandatory, lies in U, and
    # therefore contains all A and W. A full20-gain9-class can only
    # occur at the empty copy with phase inside A.
    phase_controls=0;full9=[];full4=[]
    for s in range(5):
        for r in range(9):
            R={t for t in S if t%9==r}
            cap=len((U-QQ[s])&R);phase_controls+=1
            if cap==20:full9.append((s,r))
            need(cap<=20,'nine capacity')
        for r in range(4):
            R={t for t in S if t%4==r}
            cap=len((U-QQ[s])&R);phase_controls+=1
            if cap==40:full4.append((s,r))
            need(cap<=40,'four capacity')
    need(full9==[(4,r) for r in range(9) if r%3==A[0]],'full nine selectors not forced')
    need(full4==[(4,r) for r in range(4) if r%2==b],'full four selectors not forced')
    count=0;max_union=0;min_loss=100
    for rr in product([r for _,r in full9],repeat=3):
        R=[{t for t in S if t%9==r} for r in rr]
        for _,v in full4:
            X={t for t in S if t%4==v}
            union=set().union(*R,X);count+=1;max_union=max(max_union,len(union));min_loss=min(min_loss,100-len(union))
    need(max_union==85 and min_loss==15,'equality actual resources do not have claimed unavoidable loss')
    return phase_controls,count,max_union,min_loss

def compute(c):
    validate(c);S=[t for t in range(180) if t%9!=6];F=sum(1<<t for t in S)
    selected=c['selected_cofactors'];additional=c['nine_cofactors']+[c['four_cofactor']]
    free=[d for d in c['original_cofactors'] if d not in c['whole_copy_cofactors']]
    caps={d:max(sum(t%(d//gcd(d,4))==r for t in S) for r in range(d//gcd(d,4))) for d in free}
    need(len(set(selected+additional))==11 and sum(caps.values())==600,'original labels or free mass')
    other=sum(v for d,v in caps.items() if d not in selected+additional)
    need(other==144 and len(free)-11==16,'remaining resource capacity')
    threshold=5*111-other;M={(e,r):sum(1<<t for t in S if t%e==r) for e in (2,3,5,9,4) for r in range(e)}
    parts=tuple(allocations());need(len(parts)==855 and len(set(parts))==855,'copy partitions')
    cases=active=joint=active9=critical=phases=controls=orders=0
    max7=prune7=prune9=expanded=max_union=0;min_loss=100
    critical_Q=set();critical_phases=set()
    for b in range(2):
      for A in combinations_with_replacement(range(3),3):
       for C in combinations_with_replacement(range(5),3):
        phases+=1;chosen=[M[2,b]]+[M[3,r] for r in A]+[M[5,r] for r in C]
        for copies in parts:
          cases+=1;Q=[0]*5
          for s,m in zip(copies,chosen):Q[s]|=m
          Z=bins(Q,F);H0=[z.bit_count() for z in Z]
          need(sum(H0)==160,'multiplicity histogram domain')
          score7=top(H0,111);max7=max(max7,score7)
          if score7+100<threshold:
            prune7=max(prune7,score7+100);continue
          active+=1
          for s9 in range(5):
           for r9 in range(9):
            V=M[9,r9]&(F^Q[s9]);H9=[0]*9;Z9=[0]*9
            for k,z in enumerate(Z):
              a=z&V;d=z&(F^V);H9[k]+=d.bit_count();H9[k+3]+=a.bit_count();Z9[k]|=d;Z9[k+3]|=a
            score9=top(H9,111)
            if score9+40<threshold:
              prune9=max(prune9,score9+40);continue
            active9+=1
            for s4 in range(5):
             for r4 in range(4):
              W=M[4,r4]&(F^Q[s4]);H=[0]*10
              for k,z in enumerate(Z9):
                a=(z&W).bit_count();H[k]+=H9[k]-a;H[k+1]+=a
              score=top(H,111);joint+=1;expanded=max(expanded,score)
              need(score<=threshold,'joint upper threshold exceeded')
              if score==threshold:
                critical+=1;critical_Q.add((b,A,C,copies));critical_phases.add((b,A,C))
                n,o,u,l=equality(Q,A,C,b,s9,r9,s4,r4,H,copies,c)
                controls+=n;orders+=o;max_union=max(max_union,u);min_loss=min(min_loss,l)
    need(max(prune7,prune9,expanded)==411 and critical>0,'wrong threshold boundary')
    result=dict(canonical_phase_multisets=phases,canonical_copy_partitions=len(parts),canonical_cases=cases,
                active_seven_profiles=active,pruned_seven_profiles=cases-active,nine_selectors_examined=45*active,
                active_nine_selectors=active9,pruned_nine_selectors=45*active-active9,joint_profiles=joint,
                maximum_seven_score=max7,maximum_pruned_seven_ceiling=prune7,maximum_pruned_nine_ceiling=prune9,
                maximum_expanded_joint_score=expanded,critical_joint_profiles=critical,critical_seven_profiles=len(critical_Q),
                critical_phase_multisets=len(critical_phases),literal_equality_copy_phase_controls=controls,
                ordered_nine_and_four_equality_controls=orders,maximum_equality_union_extra_hits=max_union,
                minimum_equality_overlap_loss=min_loss,other_resource_mass=other,necessary_hole_upper_bound=110)
    return result

def main():
    p=ArgumentParser();p.add_argument('--certificate',type=Path,default=HERE/'certificate.json');p.add_argument('--output',type=Path);a=p.parse_args()
    result=compute(json.loads(a.certificate.read_text()));expected=json.loads((HERE/'expected.json').read_text())
    if result!=expected:
        Path(str(a.output or HERE/'failed-replay')+'.mismatch.json').write_text(json.dumps({'actual':result,'expected':expected},indent=2)+'\n')
    need(result==expected,'frozen exact replay values differ')
    if a.output:a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main()
