"""Separate physical AP/Cartesian-coordinate audit of each original phase transport."""
from pathlib import Path
from itertools import product,permutations
from collections import deque
from hashlib import sha256
import argparse,json,struct,time

def require(test,message):
    if not test:raise ValueError(message)

p=argparse.ArgumentParser();p.add_argument('--data',type=Path,required=True)
a=p.parse_args();data=a.data;start=time.monotonic()
source=json.loads((data/'result.json').read_text())
N=32*9*5*7;P=[(8,0),(9,0),(10,1),(14,1),(12,10)]
D=sorted(2**i*3**j*5**k*7**l for i in range(6) for j in range(3) for k in range(2) for l in range(2) if 2**i*3**j*5**k*7**l>=8)
require(source['all_original_modulus_labels']==D and source['literal_P']==[list(x) for x in P] and source['period']==N,'Original physical domain differs')
spec=[(9,3,6),(9,1,4),(9,4,7),(9,2,5),(9,5,8),(5,0,2),(5,2,3),(5,3,4)]
require(source['generators']==[list(x) for x in spec],'Generator inventory differs')
coord9=[]
for x in permutations(range(9)):
    if x[0]==0 and all(x[t]%3==t%3 for t in range(9)):coord9.append(x)
coord5=[x for x in permutations(range(5)) if x[1]==1]
require(len(coord9)==72 and len(coord5)==24,'Full stabilizer component domain differs')
group=b''.join(bytes((*x,*y)) for x,y in product(sorted(coord9),sorted(coord5)))
require((data/'coordinate-group.bin').read_bytes()==group,'Generator closure not complete Cartesian stabilizer')
lookup={(x%32,x%9,x%5,x%7):x for x in range(N)}
require(len(lookup)==N,'Independent CRT physical lookup not bijective')
point_data=(data/'physical-generators.bin').read_bytes();phase_data=(data/'original-phase-maps.bin').read_bytes()
require(len(point_data)==2*N*8 and len(phase_data)==2*8*sum(D),'Truncated/extra physical or phase stream')
offset=0;tables=[];member_count=0;phase_count=0
for gi,(prime,i,j) in enumerate(spec):
    swap=lambda z:j if z==i else i if z==j else z
    perm=[]
    for x in range(N):
        coords=(x%32,swap(x%9) if prime==9 else x%9,swap(x%5) if prime==5 else x%5,x%7)
        perm.append(lookup[coords])
    require(tuple(perm)==struct.unpack_from('<10080H',point_data,2*N*gi),'Physical point map differs')
    require(len(set(perm))==N,'Physical map not permutation')
    inverse=[-1]*N
    for x,y in enumerate(perm):inverse[y]=x
    table={}
    for n in reversed(D):
        # Every ORIGINAL phase is a literal AP; verify its whole image and inverse.
        targets=[]
        for b in range(n):
            actual={perm[x] for x in range(b,N,n)}
            target=min(actual)%n
            expected=set(range(target,N,n))
            require(actual==expected and {inverse[x] for x in expected}==set(range(b,N,n)),
                    'Original AP image/inverse does not equal one phase family')
            targets.append(target);phase_count+=1;member_count+=N//n
        require(len(set(targets))==n,'Original phase map not permutation')
        table[n]=targets
    for n,b in P:
        require(table[n][b]==b and {perm[x] for x in range(b,N,n)}==set(range(b,N,n)),'Literal P cylinder moved')
    for n in D:
        raw=struct.unpack_from('<'+str(n)+'H',phase_data,offset)
        require(tuple(table[n])==raw,'Original phase-stream field differs');offset+=2*n
    tables.append(table)
require(offset==len(phase_data),'Extra phase entries')
raw=set(product(range(15),range(18)))
# Direct component enumeration supplies a second orbit derivation, not generator BFS.
components={(a,b):set() for a,b in raw}
for x9,x5 in product(coord9,coord5):
    for a15,a18 in raw:
        p15=next(t for t in range(a15%3,15,3) if t%5==x5[a15%5])
        p18=next(t for t in range(a18%2,18,2) if t%9==x9[a18%9])
        components[(a15,a18)].add((p15,p18))
expected=set(product((0,1,5,6,10,11),(0,1,2,3,9,10,11,12)))
entries=source['complete_orbits'];require(len(entries)==48,'Wrong original orbit inventory')
covered=set();transport={}
for row in entries:
    rep=tuple(row['representative']);orbit={tuple(z) for z in row['members']}
    require(rep in expected and orbit==components[rep] and len(orbit)==row['size'],'Full raw orbit fields differ')
    require(not covered&orbit and orbit&expected=={rep},'Orbit overlap/representative ambiguity')
    for z in orbit:require(components[z]==orbit,'Direct full-coordinate orbit differs from representative')
    covered|=orbit
    for z in orbit:transport[z]=rep
require(covered==raw and {tuple(x['representative']) for x in entries}==expected,'Missing raw orbit or representative')
root=Path('scratch/four-tail-global-base-pilot.bin').read_bytes()
require(len(root)==270*76 and sha256(root).hexdigest()==source['source_root_sha256']=='73b75edfcff0a70b93879088232935a96021a594897ca850cd5dbbc15f268ca0','Previously verified root input changed')
rows={tuple(x[:2]):x for x in struct.iter_unpack('<38H',root)}
require(set(rows)==raw,'Raw root inventory differs')
for z in sorted(raw):require(rows[z][2:]==rows[transport[z]][2:],'Every original marginal/union/K transport not preserved')
retained=[list(z) for z in sorted(expected) if rows[z][-1]>=1237]
require(retained==source['retained_representatives_cutoff1237'],'Normalized target frontier differs')
require(transport[(0,3)]!=transport[(0,12)] and source['original18_3_12_preserved_separate'],'Original18 parity improperly pooled')
hashes={f:sha256((data/f).read_bytes()).hexdigest() for f in ('coordinate-group.bin','physical-generators.bin','original-phase-maps.bin')}
require(hashes==source['stream_hashes'],'Complete transport stream hashes differ')
require(phase_count==source['complete_original_phase_entries']==314272 and member_count==source['physical_original_class_member_checks']==5241600,'Incomplete original phase/AP audit')
result={'agent':'six-covering-3','role':'researcher','status':'PRIVATE_COMPLETE_LITERAL_AP_ROOT_QUOTIENT',
 'period':N,'literal_P':[list(x) for x in P],'original_labels':len(D),'component_group_sizes':[72,24],
 'group_order':1728,'generator_count':8,'physical_point_entries':80640,
 'original_phase_entries':phase_count,'whole_original_AP_member_entries':member_count,
 'all270_raw_root_fields_equal':True,'raw_root_pairs':270,'canonical_root_pairs':48,
 'orbit_sizes':[r['size'] for r in entries],'retained_representatives_cutoff1237':retained,
 'stream_hashes':hashes,'original18_3_12_separate':True,'global_normalization_to_P_claimed':False,
 'universal_BASE162_claimed':False,'uniform_six_TAIL_claimed':False,'external_review':False,
 'ordinary_generator_composition_and_equivariance_unformalized':True,'seconds':time.monotonic()-start}
print(json.dumps(result,indent=2))
