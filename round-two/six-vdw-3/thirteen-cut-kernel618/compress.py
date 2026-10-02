#!/usr/bin/env python3
"""Construct a small pair model and an explicit positive-RUP cut extension.

No native solver is invoked. Proof generation uses a two-branch rooted parity
argument to derive each needed triangle, then the supplied field-seven witness.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError(message)


def write_cnf(path, variables, rows):
    raw = ('p cnf ' + str(variables) + ' ' + str(len(rows)) + '\n' +
           ''.join(' '.join(map(str, row)) + ' 0\n' for row in sorted(rows))).encode()
    path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()


def construct(lam, census, output):
    q = 103
    case = next(c for c in census['classes'] if c['lambda'] == lam)
    holes = {0, 1, lam}
    regular = tuple(x for x in range(q) if x not in holes)
    root = regular[0]
    labels = {pair: i+1 for i, pair in enumerate(itertools.combinations(regular, 2))}
    def edge(x, y):
        return labels[tuple(sorted((x, y)))]
    def clause(*values):
        return tuple(sorted(values))
    base = set()
    for x, y in itertools.combinations(regular[1:], 2):
        a, b, c = edge(root, x), edge(root, y), edge(x, y)
        base.update((clause(-a,b,c), clause(a,-b,c), clause(a,b,-c), clause(-a,-b,-c)))
    cycle_count = len(base)
    ordered_sevens = {}
    for slope in range(1, 52):
        for start in range(q):
            ap = tuple((start+j*slope) % q for j in range(7))
            if holes.intersection(ap):
                continue
            ordered_sevens[tuple(sorted(ap))] = ap
            ladder = clause(*(edge(ap[j], ap[j+3]) for j in range(4)))
            base.add(ladder)
            base.add(clause(*(-x for x in ladder)))

    pattern = set(range(-2, 7)) | {j*pow(2,-1,q) % q for j in (1,3,5,7)}
    cores = {}
    templates = census['field_sevens_in_pattern']
    for slope in range(1, 52):
        for start in range(q):
            seed = tuple(sorted((start+j*slope) % q for j in range(5)))
            if holes.intersection(seed):
                continue
            core = tuple(sorted({(start+x*slope) % q for x in pattern} - holes))
            witnesses = [tuple(sorted((start+x*slope) % q for x in support))
                         for support in templates
                         if not holes.intersection((start+x*slope) % q for x in support)]
            cores[core] = min(witnesses) if witnesses else None
    exceptional = {tuple(row['core']) for row in case['exceptional_cores']}
    need({core for core, witness in cores.items() if witness is None} == exceptional, 'Wrong retained kernel')
    star = {core: clause(*(edge(core[0], x) for x in core[1:])) for core in cores}
    compressed = base | {star[core] for core in exceptional}
    full = base | set(star.values())
    output.mkdir(parents=True, exist_ok=True)
    compressed_sha = write_cnf(output/'compressed.cnf', len(labels), compressed)
    full_sha = write_cnf(output/'full.cnf', len(labels), full)
    clause_id = {row: i+1 for i, row in enumerate(sorted(compressed))}
    next_id = len(compressed)
    additions = 0
    hint_count = 0
    triangles = 0
    derived_cuts = 0
    with (output/'extension.lrat').open('w') as proof:
        def add(row, hints):
            nonlocal next_id, additions, hint_count
            need(row not in clause_id, 'Attempted duplicate extension row')
            need(hints and all(h > 0 for h in hints), 'Nonpositive/empty RUP hints')
            next_id += 1
            proof.write(str(next_id) + ' ' + ' '.join(map(str, row)) + ' 0 ' + ' '.join(map(str, hints)) + ' 0\n')
            clause_id[row] = next_id
            additions += 1
            hint_count += len(hints)
            return next_id
        def triangle(s, x, y):
            nonlocal triangles
            psx, psy, pxy = edge(s,x), edge(s,y), edge(x,y)
            target = clause(psx, psy, -pxy)
            if target in clause_id:
                return clause_id[target]
            need(s != root and x != root and y != root, 'Unexpected absent root triangle')
            a, b, c = edge(root,s), edge(root,x), edge(root,y)
            positive = add(clause(*target, a), [clause_id[clause(a,-b,psx)],
                                              clause_id[clause(a,-c,psy)],
                                              clause_id[clause(b,c,-pxy)]])
            negative = add(clause(*target, -a), [clause_id[clause(-a,b,psx)],
                                               clause_id[clause(-a,c,psy)],
                                               clause_id[clause(-b,-c,-pxy)]])
            triangles += 1
            return add(target, [positive, negative])
        for core in sorted(cores):
            cut = star[core]
            if cut in clause_id:
                continue
            witness = cores[core]
            need(witness is not None, 'Kernel cut missing from compressed input')
            ap = ordered_sevens[witness]
            s = core[0]
            hints = []
            for j in range(4):
                x, y = ap[j], ap[j+3]
                if s not in (x,y):
                    hints.append(triangle(s,x,y))
            ladder = clause(*(edge(ap[j], ap[j+3]) for j in range(4)))
            hints.append(clause_id[ladder])
            add(cut, hints)
            derived_cuts += 1
    need(full <= set(clause_id), 'Extension does not cover every full-model row')
    return {'lambda': lam, 'variables': len(labels), 'root': root,
            'root_cycle_clauses': cycle_count, 'seven_ladders': len(ordered_sevens),
            'compressed_clauses': len(compressed), 'full_clauses': len(full),
            'retained_kernel_cuts': len(exceptional), 'derived_local_cuts': derived_cuts,
            'derived_triangle_clauses': triangles, 'proof_additions': additions,
            'written_positive_hints': hint_count, 'compressed_sha256': compressed_sha,
            'full_sha256': full_sha, 'proof_sha256': hashlib.sha256((output/'extension.lrat').read_bytes()).hexdigest(),
            'empty_clause_proposed': False, 'mathematical_exclusion_claimed': False,
            'native_solver_invoked': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--census', type=Path, required=True)
    parser.add_argument('--lambda', dest='lam', type=int, required=True)
    parser.add_argument('--output-directory', type=Path, required=True)
    args = parser.parse_args()
    result = construct(args.lam, json.loads(args.census.read_text()), args.output_directory)
    (args.output_directory/'proposal.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))
