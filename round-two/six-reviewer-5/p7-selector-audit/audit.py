"""Independent enlarged-domain audit, local completion and new E2,t0 cut."""
from collections import Counter
import hashlib
import json
from pathlib import Path
from rows import domain
from inventory import derive
from occupancy_oracle import verify
from selectors import check, remaining_boundary
from comparison import compare
from interface import complete
from star_primitives import digest, require

HERE = Path(__file__).resolve().parent
NORMALIZED = ((1,1,5),(1,2,4),(1,3,3),(2,2,3))
ORDERED = NORMALIZED+((2,1,4),(3,1,3))
SECTORS = ((0,0),(0,1),(1,0),(1,1),(2,1))


def build(work):
    work = Path(work); work.mkdir(parents=True, exist_ok=True)
    coarse, refined, units = domain()
    require((len(coarse),len(refined)) == (117,138), 'complete two independent statistical projections')
    first = {'coarse_rows':coarse,'refined_rows':refined,'unit_records':units,'cases':[]}
    coarse_cases = []; refined_cases = []; refined_first = []
    for rows,label in ((coarse,'coarse'),(refined,'refined')):
        cases = []
        for lam in ORDERED:
            for E,t in SECTORS:
                summary,survivors,all_records,states = derive(rows,lam,E,t)
                cases.append({'lam':lam,'E':E,'t':t,'summary':summary,'survivors':survivors,
                              'all_records':all_records,'states':states})
                if lam in NORMALIZED:
                    if label == 'coarse':
                        first['cases'].append({'summary':summary,'survivors':survivors})
                    else:
                        refined_first.append({'summary':summary,'survivors':survivors})
        if label == 'coarse': coarse_cases = cases
        else: refined_cases = cases
    seal = json.loads((HERE/'FIRST_SEAL.json').read_text())
    # Original coarse seal hashes compact canonical JSON; original refined
    # seal hashes the actual default-spaced JSON file with a final newline.
    # Preserve both original seals and their exact serialization conventions.
    refined_seal_hash = hashlib.sha256((json.dumps(refined_first,sort_keys=True)+'\n').encode()).hexdigest()
    require(digest(first) == seal['whole_first_result_sha256'] and
            refined_seal_hash == seal['whole_refined_first_result_sha256'], 'pre-author-read independent seals differ')
    normalized = [c for c in refined_cases if c['lam'] in NORMALIZED]
    comparison = compare(refined,normalized)
    bridges = []; counts = Counter()
    for c in normalized:
        for r in c['survivors']:
            value = check(refined,c['lam'],c['E'],c['t'],r)
            counts[value['method']] += 1
            bridges.append({'lam':c['lam'],'E':c['E'],'t':c['t'],
                            'inventory_sha256':digest(r),'certificate':value})
    # u/v exchange is a renaming of equal-replication roles, never a
    # whole-packing automorphism. Check every omitted ordered case too.
    ordered_bridges = [check(refined,c['lam'],c['E'],c['t'],r)
                       for c in refined_cases for r in c['survivors']]
    extension = []; extension_cases = []; normalized_totals = [0,0,0]
    for lam in ORDERED:
        summary,survivors,all_records,states = derive(refined,lam,2,0)
        c = {'lam':lam,'E':2,'t':0,'summary':summary,'survivors':survivors,
             'all_records':all_records,'states':states}
        extension_cases.append(c)
        certificates = [remaining_boundary(refined,lam,r) for r in survivors]
        excluded = sum(v['excluded'] for v in certificates)
        remaining = [r for r,v in zip(survivors,certificates) if not v['excluded']]
        require(all(r['X'] == 0 for r in survivors), 'E2t0 unit-SS support')
        extension.append({'multiplicities':lam,'necessary_inventories':len(survivors),
                          'new_selector_exclusions':excluded,'remaining':len(remaining),
                          'all_survivors_sha256':digest(survivors),'remaining_sha256':digest(remaining),
                          'certificates_sha256':digest(certificates),
                          'gamma_histogram':dict(sorted(Counter(v['guaranteed_usable_points'] for v in certificates).items())),
                          'excluded_tau_histogram':dict(sorted(Counter(v['tau'] for v in certificates if v['excluded']).items()))})
        if lam in NORMALIZED:
            normalized_totals = [x+y for x,y in zip(normalized_totals,(len(survivors),excluded,len(remaining)))]
        (work/('E2t0-'+''.join(map(str,lam))+'.json')).write_text(json.dumps({'survivors':survivors,'certificates':certificates},sort_keys=True)+'\n')
    require(normalized_totals == [213,113,100], 'new normalized E2t0 frontier differs')
    oracle = verify(refined,refined_cases+extension_cases)
    local = complete(work/'local')
    (work/'ALL_INVENTORIES.json').write_text(json.dumps({'coarse':coarse_cases,'refined':refined_cases,'extension':extension_cases},sort_keys=True)+'\n')
    return {'agent':'six-reviewer-5','role':'independent mathematical reviewer',
            'scope':'exact71 words, profile17/19/19, P7; necessary inventories, not codes',
            'rows':{'coarse_count':len(coarse),'refined_count':len(refined),'coarse_sha256':digest(coarse),
                    'refined_sha256':digest(refined),'unit_fixture_records':units},
            'pre_author_read_seals_reproduced':True,'comparison':comparison,
            'coarse_normalized_survivors':sum(len(c['survivors']) for c in coarse_cases if c['lam'] in NORMALIZED),
            'refined_normalized_survivors':sum(len(c['survivors']) for c in normalized),
            'all30_ordered_claimed_domains_sha256':digest([{k:c[k] for k in ('summary','states')} for c in refined_cases]),
            'all30_ordered_claimed_survivors_closed':len(ordered_bridges),
            'all50_normalized_selector_certificates':bridges,'selector_method_counts':dict(counts),
            'cost_occupancy_coverage':oracle,'local_interface':local,
            'E2t0_extension':extension,'E2t0_normalized_totals':normalized_totals,
            'E2t0_all6_ordered_totals':[sum(r[k] for r in extension) for k in ('necessary_inventories','new_selector_exclusions','remaining')],
            'max_producer_states':max(c['states'] for c in refined_cases+extension_cases)}
