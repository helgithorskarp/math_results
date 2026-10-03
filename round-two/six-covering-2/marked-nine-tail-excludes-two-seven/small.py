"""Fresh physical parent2 single-H and dominating BASE-shadow certificate."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
from struct import pack

PREFIX = ((8,0),(9,0),(10,1),(14,0),(12,10),(16,2),(28,4),(32,6))
P = ((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))
D = tuple(d for d in range(3,316) if 315 % d == 0)


def generate():
    R = tuple(x for x in range(2520) if all(x % m != a for m,a in P))
    index = {x:i for i,x in enumerate(R)}
    all_bits = (1 << len(R)) - 1
    R2 = tuple(x for x in R if x % 8 == 2)
    R6 = tuple(x for x in R if x % 8 == 6)
    BASE = tuple(m for m in range(8,2521) if 2520 % m == 0 and m not in dict(P))
    phases = {m:tuple(sum(1 << index[x] for x in range(a,2520,m) if x in index)
                      for a in range(m)) for m in BASE}
    populations = [[d, [sum(x % d == a for x in R2) for a in range(d)]] for d in D]
    single = []
    for d in D:
        rows = []
        for a in range(10,16*d,16):
            rows.append([a, a % d, sum(all(n % 16 == 2 or n % (16*d) == a
                         for n in (x+2520*k for k in range(4))) for x in R2)])
        single.append([d, rows, max(row[2] for row in rows)])
    candidates = [d for d,_,c in single if c >= 27]
    raw = bytearray()
    small = []
    parent6 = sum(1 << index[x] for x in R6)
    for d in (5,9):
        for a in range(d):
            shadow = parent6 | sum(1 << index[x] for x in R2 if x % d == a)
            size = shadow.bit_count()
            if size < 177:
                small.append({'d':d,'odd_phase':a,'shadow_size':size,'status':'capacity<177'})
                continue
            outside = all_bits ^ shadow
            rows = []
            for m in BASE:
                values = [[(v & shadow).bit_count(), (v & outside).bit_count()] for v in phases[m]]
                for protected, unprotected in values:
                    raw.extend(pack('>HH',protected,unprotected))
                bound = max([0]+[out for inside,out in values if inside <= size-177])
                rows.append([m, values, bound])
            total = sum(row[2] for row in rows)
            small.append({'d':d,'odd_phase':a,'shadow_size':size,'protected_budget':size-177,
                          'outside_required':len(R)-size,'all_BASE_phase_rows':rows,
                          'sum_original_outside_maxima':total,'deficit':len(R)-size-total,
                          'excluded':total < len(R)-size})
    record = {'agent':'six-covering-2','role':'researcher','schema':1,'stage':'two-seven-small',
        'domain':{'minimum_exactly':8,'original_moduli_divide':10080,'literal_prefix':list(map(list,PREFIX)),
                  'essential_originals':[16,32],'productive_TAILs_exactly':9,'counts_in_actual_hole_parents2_6':[2,7],
                  'BASE_lower_bound_imported':177,'productivity':'meets actual BASE-hole lift x+2520k, k=0..3',
                  'all_other_original_labels_phases_omissions_free':True,'unproductive_selected_tails_allowed':True,
                  'actual_LCM_may_be_proper_divisor':True,'original_labels_preserved':True,
                  'numeric_input_from_six_three':False,'global_bound_changed':False,
                  'entire_two_seven_exclusion_claimed':False,'ordinary_proof_formalized':False,
                  'independent_person_reviewed':False},
        'BASE_prefix':list(map(list,P)), 'initial_R':list(R),'initial_R2':list(R2),'initial_R6':list(R6),
        'all_unused_BASE_originals':list(BASE),'all_BASE_phase_count':sum(BASE),
        'all_odd_phase_populations':populations,'all_single_H16d_physical_phases':single,
        'necessary_parent2_capacity':27,'cofactor_candidates':candidates,'mirrored_small_shadows':small,
        'raw_stream_bytes':len(raw),'raw_stream_sha256':sha256(raw).hexdigest(),
        'small_cofactors_excluded':[d for d in (5,9) if all(row.get('excluded',row['shadow_size']<177)
                                 for row in small if row['d']==d)],
        'remaining_parent2_H_phases_ge27':[[16*d,a,c] for d,rows,_ in single for a,_,c in rows
                                        if d in candidates and d not in (5,9) and c>=27]}
    return record, bytes(raw)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--raw',type=Path,required=True)
    args = parser.parse_args()
    record, raw = generate()
    args.out.write_text(json.dumps(record,sort_keys=True,separators=(',',':'))+'\n')
    args.raw.write_bytes(raw)
    print(json.dumps({'stage':record['stage'],'candidates':record['cofactor_candidates'],
                      'small_excluded':record['small_cofactors_excluded'],
                      'remaining_phases':record['remaining_parent2_H_phases_ge27'],
                      'shadows':[[r['d'],r['odd_phase'],r['shadow_size'],r.get('sum_original_outside_maxima'),r.get('deficit')] for r in record['mirrored_small_shadows']],
                      'raw_bytes':len(raw),'record_sha256':sha256(args.out.read_bytes()).hexdigest()}))
