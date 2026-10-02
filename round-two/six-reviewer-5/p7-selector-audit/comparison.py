"""Original frozen domains are comparison data after the independent seal."""
import json
from pathlib import Path
from star_primitives import require, digest

HERE = Path(__file__).resolve().parent


def compare(refined_rows, cases):
    native = json.loads((HERE/'AUTHOR_EXPECTED.json').read_text())
    require(digest(refined_rows) == native['row_types_sha256'], 'complete original138 row tuples differ')
    domains = []; totals = {0:0,1:0,2:0}
    for row in sorted(cases, key=lambda r: (r['E'],r['lam'],r['t'])):
        s = row['summary']; survivors = []
        for r in row['survivors']:
            survivors.append({'exceptional_rows':r['exceptional'],'base_counts':r['filler_counts'],
                              'E':r['E'],'Q':r['Q'],'X':r['X'],'tau':r['tau'],
                              'low_counts':r['low_pair_counts'],'good_degrees':r['good_cohort_degrees']})
        mapping = {'low_pair':'low_pair_fail','good_cohort':'independent_cohort_fail'}
        counts = {mapping.get(k,k):v for k,v in s['counts'].items()}
        domains.append({'pair_multiplicities':row['lam'],'E':row['E'],'t':row['t'],
                        'states':row['states'],'counts':counts,'survivors_sha256':digest(survivors)})
        totals[row['E']] += len(survivors)
    require(json.loads(json.dumps(domains)) == native['domains'], 'whole original20 domain summaries/actual survivor records differ')
    require(totals == {0:6,1:43,2:1}, 'complete50 survivor census')
    return {'all138_actual_row_tuples_equal':True,'all20_domain_summaries_equal':True,
            'all50_normalized_survivor_records_equal':True,'native_surviving_by_E':totals,
            'original_full_record_hash_includes_old_bridge_and_is_not_claimed_equal':True}
