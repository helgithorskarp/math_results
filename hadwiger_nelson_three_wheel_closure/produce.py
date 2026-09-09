#!/usr/bin/env python3
"""CAS/SAT discovery. Independent verifier replaces elimination and Groebner steps."""
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations
from collections import Counter
import argparse
import hashlib
import json
import time
import sympy as s
from pysat.solvers import Glucose42
import arithmetic as A
import inputs


def main(out):
    out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    src, coeffs, pairs, allowed, base, inventory = inputs.load()
    x, y = s.symbols('x y')
    fs = [sum(c[3*i+j]*x**i*y**j for i in range(3) for j in range(3)) for c in coeffs]
    fedges = {f: set() for f in allowed}
    for a, b, ids in inventory:
        for f in ids & allowed:
            fedges[f].add((a, b))
    words = [''.join(map(str, w)) for name, w in src.colour_words()]
    badwords = [inputs.bad_factors(w, allowed, base, inventory) for w in words]
    cache = {}; rfactors = set(); rows = []; stats = Counter()

    def sat_word(edges):
        clauses = [[4*v+c+1 for c in range(4)] for v in range(343)]
        for a, b in sorted(edges):
            clauses.extend([-4*a-c-1, -4*b-c-1] for c in range(4))
        clauses.append([1])
        with Glucose42(bootstrap_with=clauses) as solver:
            stats['SAT_calls'] += 1
            if not solver.solve():
                stats['UNSAT_discovery_only'] += 1
                return None
            model = set(z for z in solver.get_model() if z > 0)
        word = ''.join(str(next(c for c in range(4) if 4*v+c+1 in model)) for v in range(343))
        A.need(all(word[a] != word[b] for a, b in edges), 'decoded colouring')
        words.append(word)
        badwords.append(inputs.bad_factors(word, allowed, base, inventory))
        return len(words)-1

    def classify(r, h):
        key = (tuple(r), tuple(h))
        if key in cache:
            return cache[key]
        if len(h) == 1:
            A.need(h == ((1,),), 'constant Groebner relation')
            action = {'empty': True}
        elif len(r) == 3 and r[1]*r[1]-4*r[0]*r[2] < 0:
            action = {'no_real_x': True}
        elif len(h) == 3 and all(len(c) <= 1 for c in h) and (h[1][0] if h[1] else 0)**2-4*(h[0][0] if h[0] else 0) < 0:
            action = {'no_real_y': True}
        else:
            # The only unsplit physical envelope needing two branches in discovery.
            target = ((F(5, 3), F(-3)), (F(0), F(1)), (F(1),))
            if tuple(r) == (4, -9, 3) and h == target:
                children = [((F(1), F(-1)), (F(1),)), ((F(-1), F(2)), (F(1),))]
                action = {'split': [{'h': A.encode_h(z), 'action': classify(r, z)} for z in children]}
            else:
                rmonic = A.scale(tuple(map(F, r)), F(1)/r[-1])
                bad = set(allowed); primes = []; action = None
                for p in (1009, 1013, 1019):
                    block = A.ModBlock(rmonic, h, p)
                    bad = {i for i in bad if not block.unit(coeffs[i])}
                    primes.append(p)
                    wi = next((i for i, b in enumerate(badwords) if not b & bad), None)
                    if wi is None:
                        edges = set(base)
                        for f in bad:
                            edges.update(fedges[f])
                        wi = sat_word(edges)
                    if wi is not None:
                        action = {'colour': wi, 'primes': primes[:]}
                        break
                if action is None:
                    action = {'residual': True, 'h': A.encode_h(h)}
        cache[key] = action
        stats[next(iter(action))] += 1
        return action

    for index, (a, b) in enumerate(pairs):
        if not fs[a].has(y) and not fs[b].has(y):
            A.need(s.gcd(fs[a], fs[b]) == 1, 'coprime vertical source factors')
            decomposition = []
        else:
            E = s.resultant(fs[a], fs[b], y)
            A.need(E != 0, 'nonzero elimination resultant')
            decomposition = s.factor_list(E, x)[1]
        row = []
        for R, multiplicity in decomposition:
            rp = s.Poly(R, x, domain=s.QQ)
            r = A.primitive(tuple(F(str(rp.nth(i))) for i in range(rp.degree()+1)))
            rfactors.add(r)
            G = s.groebner([fs[a], fs[b], R], y, x, domain=s.QQ)
            gs = [z.as_expr() for z in G.polys]
            if gs == [1]:
                h = ((F(1),),)
            else:
                hs = [z for z in gs if z.has(y)]
                A.need(len(hs) == 1, 'one triangular y relation')
                hp = s.Poly(hs[0], y)
                A.need(hp.LC() == 1, 'monic y relation')
                h = tuple(A.trim(F(str(s.Poly(hp.nth(j), x).nth(i))) for i in range(len(r)-1))
                          for j in range(hp.degree()+1))
            row.append({'r': r, 'multiplicity': int(multiplicity), 'action': classify(r, h)})
        rows.append(row)
        if index % 100 == 0 or index == 799:
            print(json.dumps({'systems': index+1, 'unique_blocks': len(cache), 'words': len(words),
                              'stats': dict(stats), 'seconds': time.monotonic()-start}), flush=True)
    rfactors = sorted(rfactors); rids = {r: i for i, r in enumerate(rfactors)}
    systems = [[{'r': rids[z['r']], 'multiplicity': z['multiplicity'], 'action': z['action']}
                for z in row] for row in rows]
    actions = []; action_ids = {}
    def action_id(action):
        key = json.dumps(action, sort_keys=True, separators=(',', ':'))
        if key not in action_ids:
            action_ids[key] = len(actions); actions.append(action)
        return action_ids[key]
    systems = [[[z['r'], z['multiplicity'], action_id(z['action'])] for z in row] for row in systems]
    certificate = {'version': 1, 'rfactors': rfactors, 'words': words, 'actions': actions, 'systems': systems}
    data = (json.dumps(certificate, separators=(',', ':'))+'\n').encode()
    (out/'certificate.json').write_bytes(data)
    receipt = {'source_systems': 800, 'unique_projection_factors': len(rfactors), 'unique_blocks': len(cache),
               'words': len(words), 'stats': dict(stats), 'certificate_bytes': len(data),
               'certificate_sha256': hashlib.sha256(data).hexdigest(), 'seconds': time.monotonic()-start,
               'sympy': s.__version__, 'domain': 'QQ[x,y], lex y>x; modular good-reduction tests',
               'independence': 'Producer: CAS elimination/Groebner and multiplication matrices. Verifier: integer Sylvester determinant, rational quotient Euclidean gcd, and linear/quadratic algebraic norm. Basic univariate arithmetic is shared.'}
    (out/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--out', type=Path, required=True)
    main(parser.parse_args().out)
