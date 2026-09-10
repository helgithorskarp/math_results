"""Exact public interfaces for propagation of the h4191/h4193 pair exclusions."""
import hashlib
import importlib.util
import itertools
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
INPUT_SHA = '9da6cb1a32bbb5004b72bf2ac934dc05a44b5e2bf7705e7ec55498c3e7caabf9'
INCIDENCE_SHA = 'c9cb33688915d282b9d410898eeeb22d4bd33e242b3d28b7703ca4fe2111c477'
CURVE_SHA = '85c286422c01bcb6ebb244186032bc607984471bc2b705ef7247084dd7c33db9'
PAIR_SHA = 'e5d25c2f0ae10bf246afc4dc2fdb4fab8febdcb6b64ce44785fa1a167248f2de'


def load(name,path):
    spec = importlib.util.spec_from_file_location(name,path)
    module = importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


V = load('propagation_reviewed_curve_inventory',
         ROOT/'hadwiger_nelson_radix_four_active_closure_review1/independent_check.py')


def need(condition,message):
    if not condition:raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def canonical(normal,constant,mul=V.gf4_mul):
    pivot = next(v for v in normal if v)
    inverse = next(v for v in (1,2,3) if mul(v,pivot) == 1)
    return tuple(mul(inverse,v) for v in normal),mul(inverse,constant)


def span(left,right,mul=V.gf4_mul):
    result = {canonical(tuple(mul(a,u)^mul(b,v) for u,v in zip(left[0],right[0])),
                        mul(a,left[1])^mul(b,right[1]),mul)
              for a,b in ((1,0),(0,1),(1,1),(1,2),(1,3))}
    need(len(result) == 5,'five distinct sections of a nonparallel affine pencil')
    return tuple(sorted(result))


def old_closed(pencil):
    support = {i for normal,constant in pencil for i,value in enumerate(normal) if value}
    return len(support) <= 2 or any(normal == (1,0,0,0) for normal,constant in pencil)


def inputs(frontier,incidence):
    source = json.loads(Path(frontier).read_text())
    inc = json.loads(Path(incidence).read_text())
    need(digest(source) == INPUT_SHA and digest(inc) == INCIDENCE_SHA,
         'pinned h4193 residual and reviewed h4167 incidence interfaces')
    _,factors,circle,monos,rowids = V.reconstruct_inventory()
    need(digest(factors) == CURVE_SHA == source['curve_inventory_sha256'],
         'original exact curve numbering')
    signatures = {c:canonical(tuple((a%2)+2*(b%2) for a,b in row[1:]),
                              (row[0][0]%2)+2*(row[0][1]%2)) for row,c in rowids.items()}
    buckets = defaultdict(list)
    for curve,signature in signatures.items():buckets[signature].append(curve)
    buckets = {s:sorted(cs) for s,cs in buckets.items()}
    old_pairs = {tuple(s) for s in inc['monic_degree_four_excluded_pairs']}
    old_pairs.update(tuple(s) for s in inc['injectivity_excluded_sets'] if len(s) == 2)
    triples = {tuple(s) for s in inc['injectivity_excluded_sets'] if len(s) == 3}
    new_pairs = {tuple(s) for s in source['reflection_and_rotation_pair_exclusions']}
    need(len(old_pairs) == 8376 and len(triples) == 176420 and len(new_pairs) == 6704,
         'complete pinned exclusion inventories')
    need(not old_pairs & new_pairs and digest(sorted(new_pairs)) == PAIR_SHA,
         'new pair exclusions are disjoint from the prior incidence pairs')
    need(len(buckets) == 336 and len(signatures) == 2796,'all noncircle signature buckets')
    return source,factors,signatures,buckets,old_pairs,triples,new_pairs,rowids


def actions(factors,signatures,rowids):
    identity = tuple(range(len(factors)));rotation = list(identity);conjugation = list(identity)
    for row,c in rowids.items():
        power = (1,0);out = []
        for a in row:
            out.append(V.e_mul(a,power));power = V.e_mul(power,(-1,1))
        rotation[c] = rowids[V.canonical_row(tuple(out))]
        conjugation[c] = rowids[V.canonical_row(tuple((a+b,-b) for a,b in row))]
    compose = lambda a,b:tuple(a[b[i]] for i in range(len(a)))
    rotation,conjugation = tuple(rotation),tuple(conjugation)
    r2 = compose(rotation,rotation)
    group = (identity,rotation,r2,conjugation,compose(rotation,conjugation),compose(r2,conjugation))
    need(len(set(group)) == 6 and all(compose(a,b) in group for a in group for b in group),
         'complete named D3 group')
    signature_actions = []
    for g in group:
        mapping = {}
        for c,s in signatures.items():
            image = signatures[g[c]]
            need(s not in mapping or mapping[s] == image,'curve action descends to affine signatures')
            mapping[s] = image
        signature_actions.append(mapping)
    return group,signature_actions


def digest_line(hasher,value):
    hasher.update(json.dumps(value,separators=(',',':')).encode()+b'\n')


def export_result(source,pencils,affected,moved,retained,new_pairs,witness_sha,export=None):
    remaining_six = sorted(source['remaining_six']+moved)
    output = {'schema':'hn-radix-complete-pair-propagation-v1',
              'source_frontier_sha256':INPUT_SHA,'incidence_interface_sha256':INCIDENCE_SHA,
              'curve_inventory_sha256':CURVE_SHA,
              'reflection_and_rotation_pair_exclusions':sorted(new_pairs),
              'new_closed_pencils':[pencils[i] for i in sorted(affected)],
              'remaining_pencil_signatures':[p for i,p in enumerate(pencils) if i not in affected],
              'moved':moved,'remaining_exact':retained,'remaining_six':remaining_six,
              'extension_witness_transcript_sha256':witness_sha,
              'mode_note':'Exact-five feasibility updated through all h4167 and h4191/h4193 exclusions; compatibility does not establish physical realization.'}
    if export:
        with Path(export).open('x') as f:json.dump(output,f,sort_keys=True,separators=(',',':'));f.write('\n')
    return output
