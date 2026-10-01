"""Compare the complete regenerated compact record to a reviewer baseline."""
from pathlib import Path
from hashlib import sha256
import argparse
import json
import carrier as c
from counting import validate

HERE = Path(__file__).resolve().parent
TARGET_SHA256 = '01910b2cc840f9bef0e8221df0edf3464d39090d5cff2b4a6f3cf739690228ec'
NATIVE_SHA256 = 'c10c9bfd02323d890ccaef72803566c5fee764e360f4fe32af477b57265c1afc'

def compact(work, target):
    c.require(sha256(target.read_bytes()).hexdigest() == TARGET_SHA256, 'target runtime source pin differs')
    c.require(sha256((HERE/'partition.cpp').read_bytes()).hexdigest() == NATIVE_SHA256, 'reused reviewer native source pin differs')
    census = json.loads((work/'census.json').read_text())
    classification = json.loads((work/'classification.json').read_text())
    controls = json.loads((work/'controls.json').read_text())
    c.require(census['status'] == 'COMPLETE independent carrier and native cover census' and classification['status'] == 'COMPLETE eight packing classes and corrected full automorphism orders' and controls['status'] == 'COMPLETE independent controls', 'complete cold phase records required')
    c.require(len(census['fibers']) == 75 and census['total_covers'] == 45504, 'complete fiber census size differs')
    controls = {k:v for k,v in controls.items() if k not in ('seconds','sanitizers')}
    representatives = []
    for family in classification['families']:
        for index, orbit in enumerate(family['orbits']):
            c.check_star(orbit['representative'])
            representatives.append(dict(leave=family['index'],hub=family['prefix_index'],orbit=index,**orbit))
    c.require(len(representatives) == 8, 'eight representatives required')
    return dict(agent='six-reviewer-2',role='independent mathematical reviewer',
                status='COMPLETE independent eight-class, corrected-symmetry and row-count audit',
                target_expected_sha256=TARGET_SHA256,native_source_sha256=NATIVE_SHA256,
                census_sha256=c.digest(census),classification_sha256=c.digest(classification),
                leave_types=len(census['leaves']),legal_hub_prefixes=sum(h['valid_partitions'] for h in census['hub_carriers']),
                hub_orbits=sum(len(h['orbits']) for h in census['hub_carriers']),
                native_states=census['total_states'],max_native_states=census['max_states'],
                first_hub_normalized_covers=census['total_covers'],
                fixed_profile_labeled_packings=classification['fixed_profile_labeled_packings'],
                incidence_states=classification['incidence_states'],packing_states=classification['packing_states'],
                stabilizer_closure_states=classification['closure_states'],
                fiber_stream_sha256=c.digest(census['fibers']),
                fibers=[{k:f[k] for k in ('index','prefix_index','matrix_pairs','candidates','proof_covers','restored_covers','native_states')} for f in census['fibers']],
                representatives=representatives,controls=controls,counting=validate())

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--work',type=Path,required=True)
    p.add_argument('--target',type=Path,required=True)
    p.add_argument('--record',action='store_true',help='Explicitly replace this directory baseline after an audited run')
    a=p.parse_args()
    value=compact(a.work.resolve(),a.target.resolve())
    encoded=(json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()
    expected=HERE/'expected.json'
    if a.record:
        expected.write_bytes(encoded)
    else:
        c.require(encoded == expected.read_bytes(), 'complete stable record differs from published reviewer baseline')
    (a.work/'verified-record.json').write_bytes(encoded)
    print(json.dumps({'status':value['status'],'expected_sha256':sha256(encoded).hexdigest(),'record_bytes':len(encoded),'classes':len(value['representatives']),'fibers':value['hub_orbits'],'orders':[o['automorphism_order'] for o in value['representatives']]},indent=2))

if __name__=='__main__':
    main()
