"""Complete physical2520 AP replay of normalized tree, all raw-root numeric fields."""
from pathlib import Path
from itertools import product
from hashlib import sha256
import argparse,json,struct,time

def require(test,message):
    if not test:raise ValueError(message)

p=argparse.ArgumentParser();p.add_argument('--data',type=Path,required=True)
a=p.parse_args();data=a.data;started=time.monotonic()
source=json.loads((data/'result.json').read_text())
P=[(8,0),(9,0),(10,1),(14,1),(12,10)]
D=sorted(2**i*3**j*5**k*7**l for i in range(4) for j in range(3) for k in range(2) for l in range(2))
B=[n for n in D if n>=8 and n not in (8,9,10,12,14)]
R=sum(1<<x for x in range(2520) if all(x%n!=b for n,b in P))
require(source['BASE_original_labels']==B and source['literal_P']==[list(x) for x in P] and len(B)==36 and R.bit_count()==1398,'Original BASE/P domain differs')
require(source['required_points']==1398 and source['same_coverage_cutoff_ALL_stages']==1237 and source['maximum_allowed_holes']==161,'Global coverage cutoff or domain differs')
quot=json.loads(Path('scratch/root48-verified.json').read_text())
digest=sha256(json.dumps(quot['mathematical'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
require(digest==quot['full_math_sha256']==source['root_quotient_certificate_math_sha256'] and quot['complete_normal_optimized_AP_fields_equal'] and quot['all_semantic_controls_pass'],'Checked root quotient input differs/incomplete')
A={n:[sum(1<<x for x in range(b,2520,n)) for b in range(n)] for n in B}
marginals=phase_intersections=0

def expected_row(fixed,phases):
    global marginals,phase_intersections
    require(len(fixed)==len(phases) and len(set(fixed))==len(fixed) and all(n in B and 0<=b<n for n,b in zip(fixed,phases)),'Original fixed-phase domain differs')
    U=0
    for n,b in zip(fixed,phases):U|=A[n][b]&R
    leftover=R&~U;caps=[]
    for n in B:
        if n in fixed:continue
        # Descending original phases, independent from the compressed producer.
        cap=max((leftover&A[n][b]).bit_count() for b in range(n-1,-1,-1))
        caps.append(cap);marginals+=1;phase_intersections+=n
    return tuple([*phases,U.bit_count(),*caps,U.bit_count()+sum(caps)])

raw=Path('scratch/four-tail-global-base-pilot.bin').read_bytes()
require(len(raw)==270*76 and sha256(raw).hexdigest()==quot['root_input_sha256']=='73b75edfcff0a70b93879088232935a96021a594897ca850cd5dbbc15f268ca0','Prior complete raw roots changed')
oldrows=list(struct.iter_unpack('<38H',raw));roots={}
for b,c in product(range(15),range(18)):
    row=expected_row([15,18],[b,c]);index=18*b+c
    require(row==oldrows[index],'Previously audited raw root field differs under literalAP replay')
    roots[(b,c)]=row
reps=list(product((0,1,5,6,10,11),(0,1,2,3,9,10,11,12)))
rootstream=b''.join(struct.pack('<38H',*roots[z]) for z in reps)
require((data/'root.bin').read_bytes()==rootstream,'Complete normalized root domain/fields differ')
stages=source['stages'];require(len(stages)>=1,'Missing original root stage')
s=stages[0]
require(s['fixed_originals']==[15,18] and s['records']==48 and s['target']==1237,'Root original phase domain or cutoff differs')
retained=[list(z) for z in reps if roots[z][-1]>=1237]
require(s['retained_tuples']==retained and s['retained']==len(retained) and s['stream_sha256']==sha256(rootstream).hexdigest()
        and s['range']==[min(roots[z][-1] for z in reps),max(roots[z][-1] for z in reps)],'Complete normalized root summary differs')
out=[{'fixed_originals':[15,18],'records':48,'retained':len(retained),'target':1237,'range':s['range'],'stream_sha256':s['stream_sha256']}]
fixed=[15,18];retired_max=max(roots[z][-1] for z in reps if roots[z][-1]<1237)
for stage in stages[1:]:
    require(retained,'Extra stages after derived frontier closure')
    require(stage['target']==1237,'Every-stage coverage cutoff differs')
    new_fixed=stage['fixed_originals']
    require(new_fixed[:-1]==fixed and len(new_fixed)==len(fixed)+1 and new_fixed[-1] in B and new_fixed[-1] not in fixed,'Original extension-label domain differs')
    n=new_fixed[-1]
    require(stage['previous_tuples']==retained,'Preceding qualifying tuple domain omitted/duplicated/reordered')
    path=data/('stage'+str(n)+'.bin')
    expected_count=len(retained)*n
    require(path.stat().st_size==76*expected_count,'Incomplete/extra original phase stream')
    count=0;nextretained=[];lo,hi=65536,-1
    with path.open('rb') as f:
        for prefix in retained:
            for b in range(n):
                row=expected_row(new_fixed,prefix+[b]);actual=f.read(76)
                require(len(actual)==76 and struct.unpack('<38H',actual)==row,'Complete physical original row differs')
                K=row[-1];lo,hi=min(lo,K),max(hi,K);count+=1
                if K>=1237:nextretained.append(prefix+[b])
                else:retired_max=max(retired_max,K)
        require(f.read(1)==b'','Extra original phase record')
    tracehash=sha256(path.read_bytes()).hexdigest()
    require(stage['records']==count==expected_count and stage['retained_tuples']==nextretained
            and stage['retained']==len(nextretained) and stage['range']==[lo,hi]
            and stage['stream_sha256']==tracehash and stage['all_extension_phases_complete'],'Complete original frontier/range/hash/count summary differs')
    out.append({'fixed_originals':new_fixed,'records':count,'retained':len(nextretained),'target':1237,'range':[lo,hi],'stream_sha256':tracehash})
    fixed=new_fixed;retained=nextretained
require(not retained and source['complete_producer_frontier_closed'],'Unclosed original phase frontier proves no BASE bound')
require(retired_max<1237,'Retired original coverage bound not below target')
result={'agent':'six-covering-3','role':'researcher','status':'PRIVATE_AUTHOR_CHECKED_COMPLETE_LITERAL_AP_BASE162',
 'literal_P':[list(x) for x in P],'BASE_original_labels':B,'required_points':1398,'same_coverage_cutoff_ALL_stages':1237,
 'complete_raw_root_records_recomputed':270,'complete_normalized_tree_records':sum(x['records'] for x in out),
 'original_marginal_entries_recomputed':marginals,'physical_phase_intersections_recomputed':phase_intersections,
 'all_records_frontiers_fields_entrywise_equal':True,'stages':out,'largest_all_retired_coverage_bound':retired_max,
 'universal_BASE_holes_at_least':1398-retired_max,'required_BASE_holes_at_least':162,
 'root_quotient_certificate_math_sha256':digest,'fullP_exclusion_claimed':False,'global_Lmin8_bound_improved':False,
 'uniform_six_TAIL_ordinary_composition_needs_five_capacity161':True,'external_review':False,
 'ordinary_coverage_completion_symmetry_bridges_unformalized':True,'seconds':time.monotonic()-started}
print(json.dumps(result,indent=2))
