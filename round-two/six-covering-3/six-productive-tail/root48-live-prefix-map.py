"""Exact reusable original15 phase reduction for a fully specified live Q prefix."""
from pathlib import Path
from hashlib import sha256
import json,time

def require(test,message):
    if not test:raise ValueError(message)

start=time.monotonic();N=10080
Q=[(8,0),(9,0),(10,1),(14,0),(12,10),(16,2),(28,4),(32,6),(20,3),(18,6),(35,2)]
swap=(4,1,2,3,0)
cert=json.loads(Path('scratch/root48-verified.json').read_text())
rawgroup=Path('scratch/root48-normal/coordinate-group.bin').read_bytes()
require(sha256(rawgroup).hexdigest()==cert['mathematical']['stream_hashes']['coordinate-group.bin'],'Full audited coordinate group changed')
element=bytes((*range(9),*swap))
require(element in {rawgroup[i:i+14] for i in range(0,len(rawgroup),14)},'Proposed prefix stabilizer absent from audited group')
phi=[(x+2016*(swap[x%5]-x%5))%N for x in range(N)]
lookup={(x%32,x%9,x%5,x%7):x for x in range(N)}
independent=[lookup[(x%32,x%9,swap[x%5],x%7)] for x in range(N)]
require(phi==independent and len(set(phi))==N,'Independent physical CRT maps differ/nonbijective')
mods=[n for n in range(8,N+1) if N%n==0];tables={};checks=0
for n in mods:
    phases=[]
    for a in range(n):
        actual={phi[x] for x in range(a,N,n)};target=phi[a]%n
        require(actual==set(range(target,N,n)),'Original phase AP family split by permutation')
        phases.append(target);checks+=1
    require(len(set(phases))==n,'Original-label phase map not bijective');tables[n]=phases
for n,a in Q:
    require(tables[n][a]==a and {phi[x] for x in range(a,N,n)}==set(range(a,N,n)),'A literal Q anchor moved')
reps=[0,1,2,3,5,6,7,8,10,11,12,13];raw=set(range(15));seen=set();orbits=[]
for r in reps:
    orbit={r,tables[15][r]}
    require(not seen&orbit and orbit&set(reps)=={r},'Original15 representative domain overlaps')
    seen|=orbit;orbits.append({'representative':r,'members':sorted(orbit)})
require(seen==raw and checks==39284,'Incomplete original phase or original15 domain')
result={'agent':'six-covering-3','role':'researcher','status':'PRIVATE_COMPLETE_LITERAL_Q_ORIGINAL15_TRANSFORMATION',
 'literal_Q':[list(z) for z in Q],'period':N,'original_labels':len(mods),'original_phase_AP_checks':checks,
 'coordinate_stabilizer_order':2,'five_coordinate_permutation':list(swap),'physical_permutation_formula':'x+2016*(swap(x mod5)-(x mod5)) mod10080',
 'all10080_CRT_maps_agree':True,'all_literal_prefix_class_APs_fixed':True,
 'complete_original15_phase_map':tables[15],'present_original15_representatives':reps,'orbits':orbits,
 'original15_presence_forced':False,'original15_omission_remains_free':True,
 'root_quotient_math_sha256':cert['full_math_sha256'],'generic_mechanism_credit':'six-covering-2, published7174',
 'stronger_prefix_needs_actual_stabilizer_check':True,'negative_15_case_or_closed_tree_claimed':False,
 'BASE_hole_or_P_numeric_transfer_claimed':False,'external_review':False,'ordinary_group_composition_unformalized':True,
 'seconds':time.monotonic()-start}
print(json.dumps(result,indent=2))
