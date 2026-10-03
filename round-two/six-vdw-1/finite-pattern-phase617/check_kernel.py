"""Independent compact certificate: literal Gauss field inputs and original APs."""
import hashlib
import json
from pathlib import Path

from strict_rup import verify


def need(ok, message):
    if not ok:
        raise ValueError(message)


def bind(record, cnf):
    need(record['schema'] == 'ORIGINAL_FINITE68_SMALL_RUP_KERNEL_V1'
         and record['q'] == 617 and record['N'] == 3704 and record['roots'] == [0, 1, 4]
         and record['phase_period'] == 6 and record['variables'] == 68,
         'chosen original fixed0,1,4 finite pattern x phase6 family')
    # Gauss's lemma, computed from literal nonzero field residues.
    character = {x: sum((j*x) % 617 > 308 for j in range(1, 309)) % 2
                 for x in range(1, 617)}
    actual_roots = [n for n in range(3704) if n % 617 in (0, 1, 4)]
    need(len(actual_roots) == 20, 'all original root occurrences retained')
    root_variables = {n: 49+i for i, n in enumerate(actual_roots)}
    all_tags = []
    for n in range(3704):
        if n in root_variables:
            all_tags.append(root_variables[n])
        else:
            r = n % 617
            inputs = [character[r], character[(r-1) % 617], character[(r-4) % 617]]
            key = 4*inputs[0]+2*inputs[1]+inputs[2]
            all_tags.append(key*6+n % 6+1)
    need(set(all_tags) == set(range(1, 69)), 'all48 regular pattern/phase and20 independent root variables realized')
    leaves = record['original_integer_AP_leaves']
    need(type(leaves) is list and leaves, 'nonempty actual original AP kernel')
    lines = ['p cnf 68 %d\n' % len(leaves)]
    original_pairs, seen_ids = set(), set()
    for leaf in leaves:
        a, d = leaf['original_AP']
        need(type(a) is int and type(d) is int and a >= 0 and d > 0 and a+6*d < 3704,
             'each actual nonconstant integer AP lies in zero[0,3703]')
        need(type(leaf['polarity']) is int and leaf['polarity'] in [-1, 1],
             'each original clause has one actual monochromatic color polarity')
        cid = leaf['original_clause_id']
        need(type(cid) is int and 1 <= cid <= 1316800 and cid not in seen_ids,
             'distinct recorded original clause provenance')
        seen_ids.add(cid)
        ns = [a+j*d for j in range(7)]
        support = sorted({all_tags[n] for n in ns})
        literals = [leaf['polarity']*v for v in support]
        need(leaf['literals'] == literals,
             'literal original seven-point support including every root occurrence and actual phase')
        lines.append(' '.join(map(str, literals))+' 0\n')
        original_pairs.add((a, d))
    rebuilt = ''.join(lines).encode()
    need(rebuilt == cnf, 'whole original signed compact CNF equality')
    digest = hashlib.sha256(rebuilt).hexdigest()
    need(digest == record['kernel_cnf_sha256'], 'actual compact original CNF hash')
    return {'q': 617, 'N': 3704, 'variables': 68, 'regular_pattern_phase_bits': 48,
            'all_original_independently_free_root_positions': actual_roots,
            'original_signed_leaf_clauses': len(leaves), 'distinct_original_integer_APs': len(original_pairs),
            'literal_AP_leaf_points': 7*len(leaves), 'maximum_actual_endpoint':
            max(a+6*d for a, d in original_pairs), 'kernel_cnf_sha256': digest}


def check(here):
    record = json.loads((here/'kernel.json').read_bytes())
    binding = bind(record, (here/'kernel.cnf').read_bytes())
    proof = here/'kernel.lrat'
    need(hashlib.sha256(proof.read_bytes()).hexdigest() == record['kernel_lrat_sha256'],
         'actual compact proof bytes')
    replay = verify(here/'kernel.cnf', proof)
    need(replay['variables'] == 68 and replay['initial_clauses'] == binding['original_signed_leaf_clauses']
         and replay['checked_additions'] == record['proof_additions'], 'whole actual compact proof scope')
    return {'author': 'six-vdw-1', 'role': 'researcher',
            'status': 'EXACT_LITERAL_ORIGINAL_AP_KERNEL_EXCLUDES_FIXED_FINITE_PHASE6_FAMILY_AT3704',
            'original_AP_binding': binding, 'strict_compact_RUP_replay': replay,
            'mathematical_exclusion': True,
            'exclusion_scope': 'fixedF617 roots0,1,4 with arbitrary six independent8-bit phase tables and20 free actual root bits',
            'unrestricted_W_bound_established': False, 'valid3704_coloring': False,
            'external_review_claimed': False}


if __name__ == '__main__':
    print(json.dumps(check(Path(__file__).resolve().parent), sort_keys=True))
