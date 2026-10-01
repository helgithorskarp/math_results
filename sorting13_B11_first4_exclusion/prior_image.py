"""Independently audit one exact literal-image import, not prior proof replay."""
import json
from shared import HERE,all_tails,arguments,digest,inputs,program,read


def main():
    assert __debug__
    args=arguments();f,_,_,_=inputs(args.repository)
    current=next(t for t in all_tails(args.output) if t['parent_index']==192)
    assert (current['image'],current['case'],current['budget'])==(24,301,11)
    prior=read(args.repository/'sorting13_B11_ten_event_branch_exclusion/certificate.json')
    assert prior['proof_status']=='ALL_RECORDS_ACTUALLY_SCALAR_CLAUSE_NATIVE_AND_PYTHON_CHECKED'
    record=next(r for r in prior['records'] if r['image_id']==2)
    assert record['method']=='whole' and record['rows']==52
    loops=read(args.repository/'sorting13_B11_ten_event_loop_postponement/certificate.json')
    old=next(r for r in loops['classes'] if r['code']==record['code'])
    assert old['image_id']==old['minimal_image_id']==2 and old['obstruction'] is None
    rows=loops['images9'][2]
    assert current['rows9']==rows and len(rows)==52
    coverage=next(r for r in prior['coverage'] if r['code']==record['code'])
    assert coverage['image_id']==coverage['proved_image_id']==2
    v=program(args.repository,'verify')
    new_full=v.original_image(f,current['prefix_B11'],rows)
    old_full=v.original_image(f,old['events'],rows)
    assert len(new_full)==33 and len(old_full)==32
    assert prior['tail_transfer']['rows9_sha256']==digest(rows)
    # The old ordinary at-most12 tail exclusion is absolute: any sorter
    # of this exact row set would lift its certified old prefix to <=44.
    result=dict(agent='six-sorting-2',role='researcher',
        status='EXACT_LITERAL_IMAGE_AND_ORIGINAL_PREFIX_IMPORT_ACTUALLY_CHECKED',
        parent_index=192,image=24,budget=11,case=301,rows=52,
        rows_sha256=digest(rows),prior_graph_height=8321,prior_image_id=2,
        imported_ordinary_lower_bound=13,original_prefix_inputs=16384,
        current_full_prefix_size=33,prior_full_prefix_size=32,
        trust='Imports written independently checked8321 row-set theorem; exact equality/two original-prefix images checked here, prior proof suite not replayed')
    (args.output/'prior-image-summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
