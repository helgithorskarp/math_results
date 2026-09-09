#!/usr/bin/env python3
"""Check deductions from cited facts, not the facts or a target certificate."""
import json
from pathlib import Path

def main():
    p = Path(__file__).resolve().parent
    f = json.loads((p / 'IMPORTED_FACTS.json').read_text())
    if f != {'r35':14, 'r45_24_minimum_edges':116,
             'r45_24_class_count':352366, 'r45_23_edge_counts':{'101':1,'102':76},
             'r45_23_total_estimate_not_a_proof':'9e10',
             'q8r5_original_task_count':546356}:
        raise ValueError('Imported facts differ from the cited transcription')
    rows = []
    for edges, count in sorted(f['r45_23_edge_counts'].items()):
        bound = int(edges) + f['r35'] - 1
        if bound >= f['r45_24_minimum_edges']:
            raise ValueError('No obstruction follows for this edge count')
        rows.append({'edges':int(edges), 'classes':count,
                     'extension_edge_upper_bound':bound,
                     'required_edges':f['r45_24_minimum_edges']})
    result = {'status':'VERIFIED_CONDITIONAL_COVERAGE_OBSTRUCTION_ONLY',
              'rows':rows, 'imported_nonextendable_23_classes':sum(x['classes'] for x in rows),
              'complete_23_classification_obtained':False,
              'signature_coverage_proved':False, 'core_intersection_computed':False,
              'task_exclusions':0, 'candidates':0, 'target_solver_calls':0}
    expected = json.loads((p / 'EXPECTED.json').read_text())
    if result != expected:
        raise ValueError('Expected result mismatch')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
