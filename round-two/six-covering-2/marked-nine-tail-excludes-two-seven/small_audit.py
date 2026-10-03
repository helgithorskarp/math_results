"""Independent same-author literal set/histogram checker; no producer import."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
from struct import pack


def reconstruct():
    literal = ((8,0),(9,0),(10,1),(14,0),(12,10),(16,2),(28,4),(32,6))
    placed_BASE = ((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))
    covered = set()
    for m,a in placed_BASE:
        covered.update(range(a,2520,m))
    initial = sorted(set(range(2520)) - covered)
    parents = {p:sorted(set(range(p,2520,8)) - covered) for p in (2,6)}
    divisors = sorted({2**i * 3**j * 5**k * 7**ell
                       for i in range(4) for j in range(3) for k in range(2) for ell in range(2)})
    labels = [m for m in divisors if m>=8 and m not in {m for m,a in placed_BASE}]
    odds = sorted({3**j * 5**k * 7**ell for j in range(3) for k in range(2) for ell in range(2)}-{1})
    population = []
    single = []
    for d in odds:
        histogram = [0]*d
        for x in parents[2]:
            histogram[x%d] += 1
        population.append([d,histogram])
        phase_counts = [0]*(16*d)
        for x in parents[2]:
            missing = {x+2520*k for k in range(4) if (x+2520*k)%16!=2}
            residue_set = {n%(16*d) for n in missing}
            if len(residue_set)==1:
                phase_counts[next(iter(residue_set))] += 1
        rows = [[a,a%d,phase_counts[a]] for a in range(10,16*d,16)]
        single.append([d,rows,max(r[2] for r in rows)])
    candidate = [d for d,_,n in single if n>=27]
    small = []
    stream = bytearray()
    for d in (5,9):
        for a in range(d):
            S = set(parents[6]) | {x for x in parents[2] if x%d==a}
            s = len(S)
            if s<177:
                small.append({'d':d,'odd_phase':a,'shadow_size':s,'status':'capacity<177'})
                continue
            families = []
            for m in labels:
                counters = [[0,0] for _ in range(m)]
                for x in initial:
                    counters[x%m][0 if x in S else 1] += 1
                bound = 0
                for inside,outside in counters:
                    stream.extend(pack('>HH',inside,outside))
                    if inside<=s-177:
                        bound = max(bound,outside)
                families.append([m,counters,bound])
            total = sum(f[2] for f in families)
            small.append({'d':d,'odd_phase':a,'shadow_size':s,'protected_budget':s-177,
                          'outside_required':len(initial)-s,'all_BASE_phase_rows':families,
                          'sum_original_outside_maxima':total,'deficit':len(initial)-s-total,
                          'excluded':total<len(initial)-s})
    result = {'agent':'six-covering-2','role':'researcher','schema':1,'stage':'two-seven-small',
        'domain':{'minimum_exactly':8,'original_moduli_divide':10080,'literal_prefix':list(map(list,literal)),
                  'essential_originals':[16,32],'productive_TAILs_exactly':9,'counts_in_actual_hole_parents2_6':[2,7],
                  'BASE_lower_bound_imported':177,'productivity':'meets actual BASE-hole lift x+2520k, k=0..3',
                  'all_other_original_labels_phases_omissions_free':True,'unproductive_selected_tails_allowed':True,
                  'actual_LCM_may_be_proper_divisor':True,'original_labels_preserved':True,
                  'numeric_input_from_six_three':False,'global_bound_changed':False,
                  'entire_two_seven_exclusion_claimed':False,'ordinary_proof_formalized':False,
                  'independent_person_reviewed':False},
        'BASE_prefix':list(map(list,placed_BASE)),'initial_R':initial,'initial_R2':parents[2],'initial_R6':parents[6],
        'all_unused_BASE_originals':labels,'all_BASE_phase_count':sum(labels),
        'all_odd_phase_populations':population,'all_single_H16d_physical_phases':single,
        'necessary_parent2_capacity':27,'cofactor_candidates':candidate,'mirrored_small_shadows':small,
        'raw_stream_bytes':len(stream),'raw_stream_sha256':sha256(stream).hexdigest(),
        'small_cofactors_excluded':[d for d in (5,9) if all(row.get('excluded',row['shadow_size']<177)
                                  for row in small if row['d']==d)],
        'remaining_parent2_H_phases_ge27':[[16*d,a,c] for d,rows,_ in single for a,_,c in rows
                                         if d in candidate and d not in (5,9) and c>=27]}
    return result, bytes(stream)


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for label in ('reference','reference-raw','out','raw'):
        p.add_argument('--'+label,type=Path,required=True)
    args=p.parse_args()
    record,raw=reconstruct()
    canonical=(json.dumps(record,sort_keys=True,separators=(',',':'))+'\n').encode()
    if canonical!=args.reference.read_bytes():
        raise ValueError('Entire freshly reconstructed record differs')
    if raw!=args.reference_raw.read_bytes():
        raise ValueError('Entire freshly reconstructed raw phase stream differs')
    args.out.write_bytes(canonical)
    args.raw.write_bytes(raw)
    print(json.dumps({'all_record_bytes_agree':True,'all_raw_bytes_agree':True,
                      'raw_bytes':len(raw),'record_sha256':sha256(canonical).hexdigest(),
                      'remaining_phases':record['remaining_parent2_H_phases_ge27']}))
