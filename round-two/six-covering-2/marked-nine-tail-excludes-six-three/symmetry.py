"""All physical CRT-generator images of every original congruence family."""
import argparse
import json
from hashlib import sha256
from pathlib import Path
from struct import pack


PREFIX=((8,0),(9,0),(10,1),(14,0),(12,10),(16,2),(28,4),(32,6))
def document(stage,values):
    return {'agent':'six-covering-2','role':'researcher','schema':1,'stage':stage,
      'status':'exact arithmetic record; ordinary conditional proof in proof.md',
      'domain':{'minimum_exactly':8,'original_moduli_divide':10080,
        'literal_prefix':list(map(list,PREFIX)),'essential_originals_explicit':[16,32],
        'productive_TAILs_exactly':9,'hole_parent_counts':[6,3],
        'BASE_lower_bound_imported':177,'productive_lower_bound_imported':9,
        'productivity':'meets an actual BASE-hole lift x+2520k, k=0,1,2,3',
        'all_other_original_phases_and_omissions_free':True,
        'unproductive_selected_TAILs_allowed':True,'proper_divisor_actual_LCM_allowed':True,
        'original_labels_preserved':True,'prior_private_pilot_as_input':False,
        'three_H_126_numerical_input_used':False,'ordinary_proof_formalized':False,
        'independent_person_reviewed':False,'new_tenth_tail_bound_claimed':False,
        'global_bound_changed':False},**values}

p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--raw-stream',type=Path,required=True);args=p.parse_args()

L=10080;MODS=tuple(m for m in range(8,L+1) if L%m==0)
FIXED=PREFIX+((48,14),(96,86))
GENERATORS=((5,0,2),(5,2,3),(5,3,4),(7,1,2),(7,2,3),(7,3,5),(7,5,6),
            (9,3,6),(9,1,4),(9,4,7),(9,2,5),(9,5,8))
rows=[];raw=bytearray()
for p,a,b in GENERATORS:
    e=(L//p)*pow(L//p,-1,p)
    permutation=tuple((x+e*(b-a))%L if x%p==a else (x+e*(a-b))%L if x%p==b else x for x in range(L))
    if sorted(permutation)!=list(range(L)):raise ValueError('Physical map is not bijective')
    phase_maps=[]
    for m in MODS:
        image=[-1]*m
        for x,y in enumerate(permutation):
            i=x%m;j=y%m
            if image[i] not in (-1,j):raise ValueError('Original congruence family split')
            image[i]=j
        if sorted(image)!=list(range(m)):raise ValueError('Original phases not bijective')
        for j in image:raw.extend(pack('>H',j))
        phase_maps.append([m,image])
    by=dict(phase_maps)
    if any(by[m][a]!=a for m,a in FIXED):raise ValueError('Literal marked prefix changed')
    rows.append({'axis':p,'transposition':[a,b],'all_original_phase_images':phase_maps,
                 'whole_literal_prefix_and48_96_fixed':True,'all_original_families_preserved':True})
r=document('symmetry', {
   'modulus':L,'all_original_moduli':list(MODS),'all_generators':rows,'generator_count':len(rows),
   'physical_n_m_checks':len(rows)*len(MODS)*L,'raw_phase_images_bytes':len(raw),'raw_sha256':sha256(raw).hexdigest(),
   'prefix_fixed':list(map(list,FIXED)),'families_not_quotiented':True,'global_bound_changed':False})
args.out.write_text(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
args.raw_stream.write_bytes(raw)
print(json.dumps({k:v for k,v in r.items() if k!='all_generators'}))
