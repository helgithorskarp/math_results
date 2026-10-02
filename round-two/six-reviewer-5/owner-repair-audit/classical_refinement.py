"""Post-seal positive radius-six certificate for the literal Steiner base only.

Uses the sealed triple engine and original positive owner labels. This is a
second corroborating computation, not part of the pre-author-code seal.
The universal Steiner corollary is established separately by ordinary proof.
"""
import collections
import itertools as it
import triple_check as t
import audit_packet as a

def run(folder):
    _, old, rows, _ = a.inputs(folder)
    d = t.domain(old[4])
    base, words, blockers = d['base'], d['words'], d['blockers']
    used = sorted(set().union(*(set(words[w][0]) for w in base)))
    t.need(len(used) == 17, 'Steiner base uses exactly seventeen points')
    triples = [tuple(q) for w in base for q in it.combinations(words[w][0], 3)]
    t.need(len(triples) == len(set(triples)) == 680, 'every old triple unique')
    t.need(set(triples) == set(it.combinations(used, 3)), 'whole Steiner triple coverage')
    owners, patches = a.decode(d, rows[4], {'five_blocker_word_owners': [], 'conditional_recolorings': []})
    t.need(not patches, 'no Steiner conditional patches')
    t.need(set(owners) == {w for w in words if w not in base and blockers[w].bit_count() <= 4}, 'whole Steiner field domain')
    field = {**{w: i for i, w in enumerate(base)}, **owners}
    for w, c in field.items():
        t.need(type(c) is int and 0 <= c < 68 and blockers[w] & (1 << c), 'real Steiner blocker owner')
    t.need(not any(mask.bit_count() in (5, 6) for mask in blockers.values()), 'no omitted radius-six physical vertex')
    grouped = collections.defaultdict(list)
    for w, c in field.items():
        grouped[c].append(w)
    pairs = 0
    compatible = collections.Counter()
    witness = None
    for c in sorted(grouped):
        for x, y in it.combinations(sorted(grouped[c]), 2):
            pairs += 1
            if not (words[x][2] & words[y][2]):
                union = blockers[x] | blockers[y]
                size = union.bit_count()
                t.need(size >= 7, 'radius-six same-owner compatible collision')
                compatible[size] += 1
                if size == 7 and witness is None:
                    witness = [x, y, c, union]
    t.need(witness is not None, 'actual seven-deletion field failure witness')
    x, y, c, union = witness
    t.need(c in range(68) and (1 << c) & blockers[x] & blockers[y] & union, 'witness has a shared valid deleted owner')
    histogram = d['summary']['outside_blocker_histogram']
    return {
        'scope': 'Literal class4 S(3,5,17) base and common point relabelings; no other base type receives radius six',
        'steiner_used_points': used,
        'unused_point': next(i for i in range(18) if i not in used),
        'exact_old_triples': 680,
        'outside_blocker_histogram': histogram,
        'eligible_outside_owner_words': len(owners),
        'same_owner_pairs': pairs,
        'compatible_same_owner_union_histogram': dict(sorted(compatible.items())),
        'full_field_sha256': t.digest(sorted(field.items())),
        'first_actual_seven_deletion_field_failure': {'word_masks': [x, y], 'valid_owner': c, 'deleted_mask': union},
        'radius_six_local_clique_and_chromatic': 'For all D of size 0..6, the same whole positive field gives chi<=|D|; all deleted old words give a clique of size |D|, hence equality.',
        'retention_62': 'Padding the absent old words to six gives |F|<=68 whenever |F intersect B|>=62.',
        'boundary': 'The literal owner field fails on a seven-deletion carrier. This proves neither mathematical sharpness of the radius nor existence of a 69-word repair.',
        'ordinary_generalization': 'For any Steiner S(3,5,v), after adding one point, any packing retaining at least b-6 blocks has size at most b. See REVIEW.md proof; finite class4 data are not a premise.'
    }
