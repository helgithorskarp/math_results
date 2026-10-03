"""Proposed P-fixing root quotient: exact generators, closure and raw transports."""
from pathlib import Path
from itertools import product
from collections import deque
from hashlib import sha256
import argparse,json,struct,time

def require(test,message):
    if not test:raise ValueError(message)

p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
a=p.parse_args();out=a.out;out.mkdir(parents=True,exist_ok=True)
start=time.monotonic()
N=10080;P=[(8,0),(9,0),(10,1),(14,1),(12,10)]
mods=[n for n in range(8,N+1) if N%n==0]
spec=[(9,3,6),(9,1,4),(9,4,7),(9,2,5),(9,5,8),(5,0,2),(5,2,3),(5,3,4)]
gens=[]
for prime,i,j in spec:
    nine=list(range(9));five=list(range(5))
    v=nine if prime==9 else five;v[i],v[j]=v[j],v[i]
    gens.append((tuple(nine),tuple(five)))
identity=(tuple(range(9)),tuple(range(5)))
closure={identity};q=deque([identity])
while q:
    x9,x5=q.popleft()
    for g9,g5 in gens:
        z=(tuple(g9[x] for x in x9),tuple(g5[x] for x in x5))
        if z not in closure:closure.add(z);q.append(z)
require(len(closure)==1728,'Wrong complete coordinate group')
(out/'coordinate-group.bin').write_bytes(b''.join(bytes((*u,*v)) for u,v in sorted(closure)))
maps=[];phase_maps=[]
point_checks=phase_checks=class_members=0
with (out/'physical-generators.bin').open('wb') as points,(out/'original-phase-maps.bin').open('wb') as phases:
    for (prime,i,j),(g9,g5) in zip(spec,gens):
        weight=(N//prime)*pow(N//prime,-1,prime)
        component=g9 if prime==9 else g5
        perm=[(x+(component[x%prime]-x%prime)*weight)%N for x in range(N)]
        require(sorted(perm)==list(range(N)),'Physical generator not bijective')
        require(all(perm[x]%32==x%32 and perm[x]%7==x%7 for x in range(N)),'Fixed coordinates differ')
        points.write(struct.pack('<10080H',*perm));maps.append(perm);point_checks+=N
        tables={}
        for n in mods:
            targets=[perm[b]%n for b in range(n)]
            require(sorted(targets)==list(range(n)),'Original phase map not permutation')
            for x in range(N):
                require(perm[x]%n==targets[x%n],'Original phase family split by generator')
            class_members+=N;phase_checks+=n
            require(all(targets[b]==b for m,b in P if m==n),'Literal P phase moved')
            phases.write(struct.pack('<'+str(n)+'H',*targets));tables[n]=targets
        phase_maps.append(tables)
reps15=[0,1,5,6,10,11];reps18=[0,1,2,3,9,10,11,12]
expected=set(product(reps15,reps18));raw=set(product(range(15),range(18)))
unseen=set(raw);orbits=[];transport={}
while unseen:
    seed=min(unseen);orbit={seed};todo=deque([seed])
    while todo:
        b,c=todo.popleft()
        for table in phase_maps:
            z=(table[15][b],table[18][c])
            if z not in orbit:orbit.add(z);todo.append(z)
    hit=orbit&expected;require(len(hit)==1,'Proposed representative missing/duplicated in orbit')
    rep=next(iter(hit));unseen-=orbit
    for z in orbit:transport[z]=rep
    orbits.append({'representative':list(rep),'size':len(orbit),'members':[list(z) for z in sorted(orbit)]})
orbits.sort(key=lambda r:r['representative'])
require(len(orbits)==48 and set(transport)==raw,'Incomplete raw-root orbit cover')
path=Path('scratch/four-tail-global-base-pilot.bin');data=path.read_bytes()
require(sha256(data).hexdigest()=='73b75edfcff0a70b93879088232935a96021a594897ca850cd5dbbc15f268ca0','Previously checked raw roots changed')
require(len(data)==270*76,'Raw root record count changed')
rows={tuple(v[:2]):v for v in struct.iter_unpack('<38H',data)}
require(set(rows)==raw,'Raw original phase domain differs')
for z,rep in transport.items():require(rows[z][2:]==rows[rep][2:],'Raw root marginal/union/K transport differs')
result={'agent':'six-covering-3','role':'researcher','status':'PRODUCER_ONLY_AP_AUDIT_REQUIRED',
        'literal_P':P,'period':N,'all_original_modulus_labels':mods,'generators':[list(x) for x in spec],
        'complete_group_order':len(closure),'physical_point_generator_entries':point_checks,
        'complete_original_phase_entries':phase_checks,'physical_original_class_member_checks':class_members,
        'raw_root_pairs':270,'complete_orbits':orbits,'representatives15':reps15,'representatives18':reps18,
        'all38H_raw_to_representative_fields_compared':270,'retained_representatives_cutoff1237':[list(z) for z in sorted(expected) if rows[z][-1]>=1237],
        'original18_3_12_preserved_separate':transport[(0,3)]!=transport[(0,12)],
        'source_root_sha256':sha256(data).hexdigest(),
        'stream_hashes':{f:sha256((out/f).read_bytes()).hexdigest() for f in ('coordinate-group.bin','physical-generators.bin','original-phase-maps.bin')},
        'generic_mechanism_credit':{'agent':'six-covering-2','height':7174,'source':'b9d39eb740a866e07237be1c78b834d1ab6ea718'},
        'universal_BASE162_claimed':False,'uniform_six_TAIL_claimed':False,'seconds':time.monotonic()-start}
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('complete_orbits','all_original_modulus_labels')},indent=2))
