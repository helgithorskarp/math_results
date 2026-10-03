"""Complete bitmap BASE phase bounds for small and canonical repair shadows."""
import argparse
from hashlib import sha256
import json
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

P=((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))
R=tuple(x for x in range(2520) if all(x%m!=a for m,a in P))
I={x:i for i,x in enumerate(R)};F=(1<<len(R))-1
R2=tuple(x for x in R if x%8==2)
BASE=tuple(m for m in range(8,2521) if 2520%m==0 and m not in dict(P))
PH={m:tuple(sum(1<<I[x] for x in range(a,2520,m) if x in I) for a in range(m)) for m in BASE}

def families(shadow,raw):
    budget=shadow.bit_count()-177;outside=F^shadow;rows=[]
    for m in BASE:
        counts=[[(v&shadow).bit_count(),(v&outside).bit_count()] for v in PH[m]]
        for i,o in counts:raw.extend(pack('>HH',i,o))
        bound=max([0]+[o for i,o in counts if i<=budget])
        rows.append([m,counts,bound])
    return rows,sum(r[-1] for r in rows)

def small():
    parent2=sum(1<<I[x] for x in R2);rows=[];raw=bytearray()
    for d in (5,9):
        for a in range(d):
            shadow=parent2|sum(1<<I[x] for x in R if x%8==6 and x%d==a)
            s=shadow.bit_count()
            if s<177:
                rows.append({'d':d,'odd_phase':a,'shadow_size':s,'status':'capacity<177',
                             'all_BASE_originals_omission_free':True})
                continue
            values,total=families(shadow,raw)
            rows.append({'d':d,'odd_phase':a,'shadow_size':s,'per_phase_protected_budget':s-177,
                         'outside_required':len(R)-s,'sum_per_original_outside_maxima':total,
                         'all_BASE_originals_omission_free':True,'all_BASE_phase_families':values,
                         'excluded_by_union_bound':total<len(R)-s})
    record=document('small', {'minimum_exactly':8,'original_moduli_divide':10080,
      'prefix':list(map(list,P))+[[16,2],[32,6]],'counts':[6,3],
      'all_H_and_Q_global_original_distinct':True,'shadow_cofactors':[5,9],
      'BASE_lower177_imported':True,'all_unused_BASE_originals':list(BASE),'BASE_phase_count':sum(BASE),
      'all_odd_phases':rows,'raw_phase_stream_bytes':len(raw),'raw_phase_sha256':sha256(raw).hexdigest(),
      'whole_63_count_exclusion_claimed':False,'global_bound_changed':False})
    return record,bytes(raw)

def gluing(phases):
    p6=sum(1<<I[x] for x in R if x%8==6 and x%3==2);rows=[];raw=bytearray()
    # Only the fresh complete compact phase record is read. No pilot input.
    for s2 in phases['canonical_repair_masks']:
        shadow=p6|sum(1<<I[x] for i,x in enumerate(R2) if s2&(1<<i))
        s=shadow.bit_count();values,total=families(shadow,raw)
        rows.append({'p2_mask':s2,'size':s,'protected_budget':s-177,
                     'outside_required':len(R)-s,'sum_per_original_outside_maxima':total,
                     'deficit':len(R)-s-total,'all_unused_BASE_families':values,
                     'excluded':total<len(R)-s})
    record=document('gluing', {'all_canonical_shapes':rows,'canonical_shapes':len(rows),
      'all_BASE_phase_entries':len(rows)*sum(BASE),'raw_bytes':len(raw),'raw_sha256':sha256(raw).hexdigest(),
      'minimum_deficit':min(r['deficit'] for r in rows),'unexcluded_shapes':sum(not r['excluded'] for r in rows),
      'all_original_BASE_phases_and_omissions_free':True,'full_count_63_exclusion_claimed':True,
      'global_bound_changed':False})
    return record,bytes(raw)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=('small','gluing'))
    p.add_argument('--out',type=Path,required=True);p.add_argument('--raw-stream',type=Path,required=True)
    p.add_argument('--phases',type=Path);args=p.parse_args()
    r,raw=small() if args.stage=='small' else gluing(json.loads(args.phases.read_text()))
    args.out.write_text(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n');args.raw_stream.write_bytes(raw)
    print(json.dumps({'stage':args.stage,'whole_sha256':sha256(args.out.read_bytes()).hexdigest(),
                      'raw_stream_bytes':len(raw),'minimum_deficit':r.get('minimum_deficit')}))
