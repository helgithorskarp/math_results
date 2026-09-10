"""Independent center-incidence enumeration and complete case audit."""
from itertools import product
from two_p3_cases import PATTERNS,CASES,role_groups
from forest_profiles import profiles
from verify_forest_reduction import independent_rows

def enumerate_center_patterns():
    feasible=set();states=0
    # Center-neighbor incidences only, without importing the proposed
    # classification or the normalized SAT construction.
    for D,Q,T in product(range(4),repeat=3):
        if any((a&b)==3 for a,b in ((D,Q),(D,T),(Q,T))):continue
        for ordinary_shared in range(2):
            ordinary=[5-((D>>i)&1)-((Q>>i)&1) for i in range(2)]
            if min(ordinary)<ordinary_shared:continue
            if sum(ordinary)-ordinary_shared>15:continue
            for one_mask in range(4):
                two=[1-((T>>i)&1)-((one_mask>>i)&1) for i in range(2)]
                if min(two)<0:continue
                for two_shared in range(min(two)+1):
                    common=(D==3)+(Q==3)+(T==3)+ordinary_shared+two_shared
                    if common!=1:continue
                    if any(2*ordinary[i]+((D>>i)&1)+3*((Q>>i)&1)+two[i]+2*((T>>i)&1)!=10 for i in range(2)):continue
                    states+=1;feasible.add((D,Q,T,ordinary_shared,two_shared,one_mask))
    return feasible,states

def check():
    feasible,states=enumerate_center_patterns()
    expected=set()
    for D in range(4):
        for Q in (0,1,2):
            if Q&~D:continue
            expected.add((D,Q,0,int(D!=3),0,3^(D^Q)))
    if feasible!=expected:raise AssertionError((feasible-expected,expected-feasible))
    # Profile zero has five ordinary six-neighbors and one c=1 seven-
    # neighbor at each center. Pair uniqueness forces exactly one common
    # six-neighbor, giving sizes 1,4,4,8.
    c0=[(shared,5-shared,5-shared,17-10+shared) for shared in range(6) if shared==1]
    if c0!=[(1,4,4,8)]:raise AssertionError(c0)
    return {'profile3_center_patterns':len(feasible),'feasible_incidence_states':states,'profile0_six_role_sizes':list(c0[0])}

def complete_profiles():
    expected={(a,b) for q,a in independent_rows(6,17,51,2) for r,b in independent_rows(7,24,41,2) if q+r==2}
    actual={(tuple(a),tuple(b)) for a,b in profiles(6,2)}
    if expected!=actual or len(actual)!=6:raise AssertionError('histogram coverage')
    return len(actual)

def audit_roles():
    tested=0
    for profile,index in CASES:
        if profile not in (0,3):continue
        A,B,groups=role_groups(profile,index)
        six=[set(S) for S in A]
        if any(len(S)!=5 or not S<=set(range(13,30)) for S in six):raise AssertionError('center six counts')
        if len(six[0]&six[1])!=1 or len(set(B))!=2:raise AssertionError('unique common-six and distinct seven')
        a,b=profiles(6,2)[profile];cs={v:c for v,c in enumerate([c for c,n in enumerate(a) for _ in range(n)]+[c for c,n in enumerate(b) for _ in range(n)],13)}
        if any(sum(cs[v]-1 for v in six[i]) + cs[B[i]]-1!=10 for i in range(2)):raise AssertionError('high pair count')
        if profile==3:
            D,Q=PATTERNS[index]
            if tuple(int(13 in S) for S in six)!=D or tuple(int(29 in S) for S in six)!=Q:raise AssertionError('exceptional masks')
        members=[v for group in groups for v in group]
        if len(members)!=len(set(members)):raise AssertionError('overlapping row groups')
        # Every permitted row permutation fixes degree, high count, and
        # both center incidences. Distinguished singleton rows need no group.
        for group in groups:
            colors={(6 if v<30 else 7,cs[v],int(v in six[0]) if v<30 else int(v==B[0]),int(v in six[1]) if v<30 else int(v==B[1])) for v in group}
            if len(colors)>1:raise AssertionError('invalid row symmetry')
        tested+=1
    return tested

def main():
    import json
    result=check();result.update(complete_profiles=complete_profiles(),normalized_role_cases=audit_roles(),total_sat_cases=len(CASES))
    if len(PATTERNS)!=8 or len(CASES)!=13:raise AssertionError('case count')
    actual={(sum(d<<i for i,d in enumerate(D)),sum(q<<i for i,q in enumerate(Q))) for D,Q in PATTERNS}
    expected={(r[0],r[1]) for r in enumerate_center_patterns()[0]}
    if actual!=expected:raise AssertionError('SAT pattern cover')
    print(json.dumps(result,sort_keys=True));return result

if __name__=='__main__':main()
