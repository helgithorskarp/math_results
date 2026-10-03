"""Reduced literalP BASE tree; proof status remains provisional until full AP replay."""
from pathlib import Path
from hashlib import sha256
import argparse,json,struct,time

def require(test,message):
    if not test:raise ValueError(message)

p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
a=p.parse_args();out=a.out;out.mkdir(parents=True,exist_ok=True);start=time.monotonic()
proof=json.loads(Path('scratch/root48-verified.json').read_text())
require(proof['complete_normal_optimized_AP_fields_equal'] and proof['all_semantic_controls_pass'],'Root quotient not fully checked')
P=[(8,0),(9,0),(10,1),(14,1),(12,10)]
B=[n for n in range(8,2521) if 2520%n==0 and n not in (8,9,10,12,14)]
points=[x for x in range(2520) if all(x%n!=b for n,b in P)]
require(len(B)==36 and len(points)==1398,'BASE/physicalP domain changed')
target=len(points)-161
actions={n:[0]*n for n in B}
for i,x in enumerate(points):
    for n in B:actions[n][x%n]|=1<<i
raw=Path('scratch/four-tail-global-base-pilot.bin').read_bytes()
require(sha256(raw).hexdigest()=='73b75edfcff0a70b93879088232935a96021a594897ca850cd5dbbc15f268ca0','Prior audited roots changed')
roots={tuple(row[:2]):row for row in struct.iter_unpack('<38H',raw)}
reps=[(b,c) for b in (0,1,5,6,10,11) for c in (0,1,2,3,9,10,11,12)]
retained=[list(z) for z in reps if roots[z][-1]>=target]
require(retained==proof['mathematical']['retained_representatives_cutoff1237'],'Canonical initial frontier differs')
rootstream=b''.join(struct.pack('<38H',*roots[z]) for z in reps)
(out/'root.bin').write_bytes(rootstream)
stages=[{'fixed_originals':[15,18],'records':48,'target':target,'retained':len(retained),
         'retained_tuples':retained,'stream_sha256':sha256(rootstream).hexdigest(),'range':[min(roots[z][-1] for z in reps),max(roots[z][-1] for z in reps)]}]
fixed=[15,18]
for n in (24,36,20,21,28):
    before_tuples=retained;new_fixed=fixed+[n];remaining=[m for m in B if m not in new_fixed]
    retained=[];count=0;low,high=65536,-1;digest=sha256()
    with (out/('stage'+str(n)+'.bin')).open('wb') as stream:
        for earlier in before_tuples:
            old=0
            for m,b in zip(fixed,earlier):old|=actions[m][b]
            for b in range(n):
                U=old|actions[n][b]
                marginal=[max((v&~U).bit_count() for v in actions[m]) for m in remaining]
                K=U.bit_count()+sum(marginal);phase=earlier+[b]
                record=struct.pack('<38H',*phase,U.bit_count(),*marginal,K)
                stream.write(record);digest.update(record);count+=1;low,high=min(low,K),max(high,K)
                if K>=target:
                    retained.append(phase)
                    if len(retained)>300:raise RuntimeError('Frontier300 cap: incomplete, no exclusion')
    stage={'fixed_originals':new_fixed,'previous_tuples':before_tuples,'records':count,'target':target,
           'range':[low,high],'retained':len(retained),'retained_tuples':retained,'stream_sha256':digest.hexdigest(),
           'all_extension_phases_complete':count==len(before_tuples)*n}
    require(stage['all_extension_phases_complete'],'Incomplete original phase extension')
    (out/('stage'+str(n)+'.json')).write_text(json.dumps(stage,indent=2)+'\n')
    stages.append(stage);fixed=new_fixed
    print(json.dumps({k:v for k,v in stage.items() if k not in ('previous_tuples','retained_tuples')}),flush=True)
    if not retained:break
result={'agent':'six-covering-3','role':'researcher','status':'PRODUCER_ONLY_FULL_AP_REPLAY_REQUIRED',
        'literal_P':P,'BASE_original_labels':B,'required_points':1398,'same_coverage_cutoff_ALL_stages':target,
        'maximum_allowed_holes':161,'stages':stages,'complete_producer_frontier_closed':not retained,
        'root_quotient_certificate_math_sha256':proof['full_math_sha256'],'fullP_exclusion_claimed':False,
        'universal_BASE162_claimed':False,'uniform_six_TAIL_claimed':False,'seconds':time.monotonic()-start}
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='stages'},indent=2))
