"""PRIVATE actual four-hub markings, distinguished defect-two hub.

Pressure premise is an ordinary deduction from8323: if a is high at
s, every low saturated leave friend t of a forces a positive at deficit.
Hence delta_sa+L_s(a)<=5+4*(20-r_a). Code1's private chat1836 supplies
method credit for this precise screen. No P21 exclusion is claimed.
"""
import hashlib
import itertools
import json
from pathlib import Path
import sys
import time

ROOT=Path('round-two/six-code-3')
sys.path.insert(0,str(ROOT/'four_hub_p21_endpoint_cut'))
import produce

def main():
    data=json.loads((ROOT/'four_hub_p21_endpoint_cut/fixtures.json').read_text())
    rows=produce.rows_from_data(data)
    physical_row={(r['fixture'],tuple(r['hub_high'])):r for r in rows}
    expected=json.loads((ROOT/'four_hub_p21_endpoint_cut/expected.json').read_text())
    type_index={produce.type_key(r):i for i,r in enumerate(expected['types'])}
    records=[];all_marks=0;all_accepted=0;started=time.monotonic()
    for fi,words in enumerate(data['stars']):
        star=produce.compile_star(words,fi)
        delta=star['delta'];high_mask=sum(1<<p for p in star['high'])
        low_mask=((1<<17)-1)^high_mask
        covered={tuple(sorted(t)) for w in words for t in itertools.combinations(w,2)}
        low_friends={a:sum(1<<b for b in range(17) if b!=a and (low_mask>>b)&1
                           and tuple(sorted((a,b))) not in covered) for a in star['high']}
        accepted=0;marks=0;types={};row_counts={};first_failure=None;membership=0
        for hubs in itertools.combinations(range(17),4):
            hub_mask=sum(1<<p for p in hubs)
            J=tuple(p for p in hubs if (high_mask>>p)&1)
            row=physical_row[fi,J];type_id=type_index[produce.type_key(row)]
            for heavy in hubs:
                marks+=1;all_marks+=1
                if all_marks>218960 or time.monotonic()-started>30:
                    raise RuntimeError('INCOMPLETE fixed actual-marking guard; no mathematical absence')
                bad=None
                for a in star['high']:
                    L=(low_friends[a]&~hub_mask).bit_count()
                    defect=2 if a==heavy else 1 if a in hubs else 0
                    if delta[a]+L>5+4*defect:
                        bad=dict(point=a,delta=delta[a],low_saturated_friends=L,
                                 global_point_defect=defect,hubs=list(hubs),heavy=heavy,
                                 hub_high=list(J),type_id=type_id)
                        break
                if bad:
                    if first_failure is None:first_failure=bad
                    continue
                accepted+=1;all_accepted+=1;membership |= 1 << (marks-1)
                types[type_id]=types.get(type_id,0)+1
                row_counts[J]=row_counts.get(J,0)+1
        if marks!=9520:raise ValueError('full physical marking count')
        records.append(dict(fixture=fi,physical_marks=marks,accepted_marks=accepted,
                            accepted_type_multiplicities=sorted(types.items()),
                            accepted_high_mark_multiplicities=[[list(J),c] for J,c in sorted(row_counts.items())],
                            first_failure=first_failure,accepted_membership_hex=membership.to_bytes(1190,'little').hex()))
    if all_marks!=218960:raise ValueError('whole actual marking coverage')
    projection=sorted({i for record in records for i,c in record['accepted_type_multiplicities']})
    result=dict(agent='six-code-3',role='researcher',status='PRIVATE_FROZEN_FIRST_ENGINE_COMPLETE_MARKING_MEMBERSHIP',
                source_fixture_sha256=produce.PIN,physical_markings=all_marks,accepted_markings=all_accepted,
                surviving_type_projection=projection,records=records,
                exact_next_target='Actual four-hub P21 feasibility; this screen does not assume P21 or give a global packing',
                method_credit_chat=1836,independent_reconstruction_pending=True,
                ordinary_pressure_bridge_formalized=False,new_pair_total_claim=None)
    out=ROOT/'scratch/pass16-first-engine-low-friends.json'
    if out.exists():raise ValueError('fresh pilot output required')
    encoded=json.dumps(result,sort_keys=True,indent=2).encode()+b'\n';out.write_bytes(encoded)
    print(json.dumps(dict(status=result['status'],physical_marks=all_marks,accepted_marks=all_accepted,
                          projected_types=len(projection),elapsed_seconds=time.monotonic()-started,
                          artifact_sha256=hashlib.sha256(encoded).hexdigest())))

if __name__=='__main__':main()
