"""Local checked reserve-mask transport, with no historical negative corpus."""
from inputs import checked_finite, digest, load, need, static_sources


def prerequisites():
    pins = static_sources()
    prep, prep_o = checked_finite(load('preparation_scalar')), checked_finite(load('preparation_scalar_O'))
    cuts, cuts_o = checked_finite(load('cuts_scalar')), checked_finite(load('cuts_scalar_O'))
    seed, seed_o = checked_finite(load('seed_scalar')), checked_finite(load('seed_scalar_O'))
    reserve, reserve_o = checked_finite(load('reserve_scalar')), checked_finite(load('reserve_scalar_O'))
    need(prep['finite'] == prep_o['finite'] and cuts['finite'] == cuts_o['finite'] and
         seed['finite'] == seed_o['finite'] and reserve['finite'] == reserve_o['finite'],
         'Complete regenerated mathematical input normal/O records differ')
    classification = checked_finite(load('reserve_classifications'))
    rows = classification['classifications']
    need(digest(rows) == classification['finite']['classification_sha256'] ==
         reserve['finite']['complete_classification_sha256'] and
         reserve['finite']['producer_reserve_classification_finite_sha256'] == classification['finite_sha256'] and
         reserve['finite']['scalar_seed_reserve_finite_sha256'] == seed['finite_sha256'],
         'Local actual reserve partition differs')
    certificate = checked_finite(load('public_universal_certificate'))
    need(certificate['finite_sha256'] ==
         'a2faef8075c751886b467a5c2095ad79552e712b3b7ca29256715dd86fe6ed4e' and
         certificate['finite']['cold_source_only_complete'] and
         certificate['finite']['all8_semantic_damages_reject'], 'Public conditional-maximum source replay differs')
    return reserve, load('public_universal_fixture'), pins['public_universal_graph_ref']


def selected_offsets(first, last):
    reserve, fixture, reference = prerequisites()
    cuts = load('cuts')
    classification = load('reserve_classifications')
    rows = classification['classifications']
    need(0 <= first < last <= len(cuts['retained_function_ids']) == 5295 and last-first <= 128 and
         [row['retained_offset'] for row in rows] == list(range(5295)) and
         [row['function_id'] for row in rows] == cuts['retained_function_ids'],
         'Complete local retained-function interval/classification differs')
    remaining = [r['retained_offset'] for r in rows if r['witness'] is None]
    need(len(remaining) == 3197 and digest(remaining) == reserve['finite']['remaining_retained_offsets_sha256'],
         'Actual reserve-open function partition differs')
    return [i for i in remaining if first <= i < last], reserve, fixture, reference
