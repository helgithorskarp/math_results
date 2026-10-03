"""Reproduce complete original-member affine lower-Gram bindings."""
from pathlib import Path
import argparse,json
import input as inputs


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    _,_,even,standard=inputs.portable_zero.cleared_grams()
    rows=[inputs.portable_zero.original_binding(q,even,standard) for q in (4,5,9)]
    value={'actual_agent':'six-downset-3','role':'researcher','complete_original_controls':rows,
           'every_ordered_pair_in_each_selected_original_carrier_checked':True,
           'finite_bindings_validate_the_source_not_the_whole_domain':True,'independent_review':False}
    args.out.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'complete_carriers':len(rows),'ordered_original_pairs':sum(row['all_ordered_original_pairs'] for row in rows)}))
