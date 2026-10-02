"""Separate raw-row census, conjugacy/diagonal bridges, and actual AP witnesses."""
import argparse
import copy
import csv
import json
from math import gcd
from pathlib import Path


def require(ok,message):
    if not ok:raise ValueError(message)


def bit(mask,s):return ((mask//2**(s%10))%2+s//10)%2


def power(u,t,i):return pow(u,i,20),sum(pow(u,j,20)*t for j in range(i))%20


def check(records,bridge_checks=True):
    require(type(bridge_checks) is bool,'explicit diagnostic bridge flag')
    representatives=[8,10,12,16,20,34,72];units=[u for u in range(20) if gcd(u,20)==1]
    expected=[(m,u,t) for m in representatives for u in units for t in range(20)]
    require(type(records) is list and len(records)==1120 and [(r[0],r[1],r[2]) for r in records]==expected,'complete seven-by160 ordered cover')
    require(all(type(r) is list and len(r)==8 and all(type(r[j]) is int for j in [0,1,2,3,5,6,7]) for r in records),'exact integer record domains')
    actualAPs=[]
    for a in range(20):
        for b in range(20):
            if a==b:continue
            actualAPs.append(sum(2**x for x in {(a+j*(b-a))%20 for j in range(7)}))
    admissible={m for m in range(1024) if all((m|((m^1023)<<10))&ap and (m|((m^1023)<<10))&ap!=ap for ap in actualAPs)}
    require(len(admissible)==580,'complete raw local census')
    partition={};normalizers={};sizes=[]
    for rep in representatives:
        orbit={}
        for v in units:
            for z in range(20):
                transformed=sum(bit(rep,(v*s+z)%20)*2**s for s in range(10))
                orbit[transformed]=(v,z)
        require(rep==min(orbit) and not(set(orbit)&set(partition)),'disjoint canonical local orbits')
        sizes.append(len(orbit))
        for m in orbit:
            matches=[(v,z) for v in units for z in range(20) if all(bit(m,(v*s+z)%20)==bit(rep,s) for s in range(20))]
            require(matches,'actual row normalization absent');normalizers[m]=min(matches);partition[m]=rep
    require(set(partition)==admissible and sizes==[160,40,80,160,40,80,20],'all580 local rows covered')
    conjugacies=0
    if bridge_checks:
        for row,(v,z) in normalizers.items():
            inverse=pow(v,-1,20)
            for u in units:
                for t in range(20):
                    conjugate=inverse*(t+(u-1)*z)%20
                    for s in range(20):
                        require((v*(u*s+conjugate)+z)%20==(u*(v*s+z)+t)%20,'whole affine-generator conjugacy')
                        conjugacies+=1
    logarithm={r:next(i for i in range(30) if pow(3,i,31)==r) for r in range(1,31)}
    require(set(logarithm.values())==set(range(30)) and pow(3,30,31)==1,'complete primitive3 field group')
    for a in range(1,31):
        for r in range(1,31):require(logarithm[a*r%31]==(logarithm[a]+logarithm[r])%30,'field logarithm multiplication')
    # Normalized nonzero field difference1 has exactly24 legal starts and400 phase pairs.
    legal=[a for a in range(31) if all((a+j)%31 for j in range(7))]
    require(len(legal)==24,'complete normalized nonzero-field AP domain')
    closed=bad=positive=identities=diagonal=H3=raw_eligible=nonclosed_H3=0;rows_count={m:0 for m in representatives}
    for row,u,t,closed_flag,status,a,d,color in records:
        pairs=[power(u,t,i) for i in range(31)]
        mul,shift=pairs[30]
        closure=all(bit(row,(mul*s+shift)%20)==bit(row,s) for s in range(20))
        require(closed_flag in [0,1] and closed_flag==int(closure),'actual closure flag; nonclosed profiles remain genuine canonical-log colorings')
        require(status in ['BAD_AP','CORE'],'canonical profile has no actual certificate/status')
        if closure:
            closed+=1;rows_count[row]+=1
            ten_u,ten_t=pairs[10]
            require(all(bit(row,(ten_u*s+ten_t)%20)==bit(row,s) for s in range(20)),'conditional multiplicative H3 bridge failed')
        word=[]
        for x in range(620):
            r,s=x%31,x%20
            if not r:word.append(None);continue
            ui,ti=pairs[logarithm[r]];word.append(bit(row,(ui*s+ti)%20));identities+=1
        if closure:
            require(all(word[x]==word[(521*x)%620] for x in range(620)),'closed profile actual CRT521 invariance')
            H3+=600
            if bridge_checks:
                for delta in range(1,31):
                    field_inverse=pow(delta,-1,31);ui,ti=pairs[logarithm[delta]]
                    A=next(a for a in range(620) if a%31==field_inverse and a%20==ui)
                    B=next(b for b in range(620) if b%31==0 and b%20==ti)
                    require(gcd(A,620)==1,'diagonal affine map not a unit')
                    for x in range(620):
                        y=(A*x+B)%620
                        require(y%31==(field_inverse*(x%31))%31 and y%20==(ui*(x%20)+ti)%20 and word[y]==word[x],'actual conditional diagonal CRT/color identity')
                        diagonal+=1
        else:
            require(any(word[x]!=word[(521*x)%620] for x in range(620)),'false global order3 premise for a nonclosed profile')
            nonclosed_H3+=1
        if status=='BAD_AP':
            require(0<=a<620 and 1<=d<=310 and color in [0,1],'integer witness domain')
            positions=[a+j*d for j in range(7)]
            require(max(positions)<=2479 and all(x%31 for x in positions) and all(word[x%620]==color for x in positions),'actual regular integer monochromatic AP')
            bad+=1
        else:
            require((a,d,color)==(-1,-1,-1),'core proposal sentinel')
            for first in range(620):
                for second in range(620):
                    if first==second:continue
                    positions=[(first+j*(second-first))%620 for j in range(7)]
                    if any(x%31==0 for x in positions):continue
                    require(len({word[x] for x in positions})>1,'untrusted regular proposal has a bad actual AP')
            positive+=1
    raw_eligible=sum(rows_count[r]*size for r,size in zip(representatives,sizes))
    return {'author':'six-vdw-1','role':'researcher','status':'COMPLETE_CANONICAL_AFFINE_PHASE_POWER_FAMILY_CHECK' if bridge_checks else 'DIAGNOSTIC_CERTIFICATE_CORE_CHECK_BRIDGES_OMITTED',
            'complete_conjugacy_and_diagonal_bridges_checked':bridge_checks,
            'all_raw_local_inputs':1024,'admissible_local_rows':580,'phase_generators':160,'normalized_base_generator_inputs':1120,
            'unquotiented_admissible_base_generator_inputs':92800,'closed_transport_normalized_pairs':closed,
            'closed_transport_unquotiented_pairs':raw_eligible,'actual_bad_APs':bad,'nonclosed_H3_counterexamples':nonclosed_H3,'checked_regular_cores':positive,
            'closed_by_representative':rows_count,'raw_original_point_identities':identities,'conjugacy_point_identities':conjugacies,
            'diagonal_CRT_color_identities':diagonal,'actual_H3_color_identities':H3,'complete_normalized_cross_APs_per_CLOSED_profile':9600,
            'scope':'All canonical-log affine phase-power parameters at primitive root3. Diagonal/H3 lemmas apply only to CLOSED profiles. No arbitrary regular620 or unrestricted W exclusion.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('catalogue',type=Path);a=p.parse_args()
    with a.catalogue.open(newline='') as f:
        reader=csv.reader(f);require(next(reader)==['row','u','t','closed','status','a','d','color'],'catalogue header')
        records=[[int(v) if j!=4 else v for j,v in enumerate(r)] for r in reader]
    print(json.dumps(check(records),sort_keys=True),flush=True)
