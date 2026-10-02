"""Regenerate independent local evidence; full426-row corpus stays scratch."""
import argparse,hashlib,json
from pathlib import Path
import first_check,bridge_checks,corroborate,correction_region

def compute(work):
    base=Path(__file__).resolve().parent
    seal=json.loads((base/'first-seal.json').read_text())
    for name,sha in seal['source_sha256'].items():
        first_check.rows.need(hashlib.sha256((base/name).read_bytes()).hexdigest()==sha,'unchanged first-sealed source '+name)
    first=first_check.compute()
    first_check.rows.need(hashlib.sha256(first_check.encode(first)).hexdigest()==seal['whole_record_sha256'],'whole source-before-author first record')
    stars=json.loads((base/'fixtures.json').read_text())['stars']
    bridge=bridge_checks.compute(stars,first['exact'])
    late=corroborate.compute(first['exact'],bridge,base)
    region=correction_region.compute(first['exact'])
    full={'first':first,'physical_bridge_controls':bridge,'late_author_schema_comparison':late,'sharp_corrected_coefficient_region':region}
    raw=first_check.encode(full);work.mkdir(parents=True,exist_ok=True)
    (work/'regenerated-full-evidence.json').write_bytes(raw)
    summary={'agent':'six-reviewer-5','role':'independent mathematical reviewer','status':'COMPLETE_CONDITIONAL_P35_AUDIT',
             'whole_regenerated_evidence_sha256':hashlib.sha256(raw).hexdigest(),'source_before_author_first_sha256':seal['whole_record_sha256'],
             'actual_marked_rows':len(first['exact']['rows']),'all_eight_five_hub_exceptions_retained':len(first['exact']['exceptions']),
             'complete_P34_boundary_inventories':first['exact']['boundaries'],'independent_weak_composition_cases':first['independent_audit']['weak_composition_cases'],
             'six_point_graph_census':first['independent_audit']['cubic_counts'],'six_point_trianglefree_trace4':first['independent_audit']['trianglefree_cubic_trace4'],
             'semantic_damage_checks':bridge['semantic_damage_checks'],'actual_transported_rows':bridge['transported_whole_rows'],
             'explicit_nonedge_unique_low_neighbor_violations':bridge['explicit_unique_low_neighbor_nonedge_witnesses'],'late_author_schema_comparison':late,'sharp_corrected_coefficient_region':region,
             'scope':'Conditional on8323/8933/9249; five-unsaturated-point71-word packings requireP>=35. No P35 exclusion, global upper70, whole-code symmetry, sharpness or historical priority. Ordinary bridges unformalized.'}
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--check',type=Path);args=p.parse_args();result=compute(args.work)
    if args.check:first_check.rows.need(first_check.encode(result)==first_check.encode(json.loads(args.check.read_text())),'entire frozen final mathematical readout')
    print(first_check.encode(result).decode(),end='')
