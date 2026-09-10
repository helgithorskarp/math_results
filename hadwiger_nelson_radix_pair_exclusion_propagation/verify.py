#!/usr/bin/env python3
"""RREF pencil enumeration, literal obstruction checks and Cartesian-product witnesses."""
import argparse
import hashlib
import itertools
import json
import math
import time
from pathlib import Path
import common as C

TABLE = ((0,0,0,0),(0,1,2,3),(0,2,3,1),(0,3,1,2))


def normalize(normal,constant):
    inverse = (0,1,3,2)[next(v for v in normal if v)]
    return tuple(TABLE[inverse][v] for v in normal),TABLE[inverse][constant]


def rref_catalogue(buckets):
    """Every rank-two RREF normal plane and every affine constant functional."""
    all_pencils = set();matrices = 0
    for i,j in itertools.combinations(range(4),2):
        free = [(0,k) for k in range(i+1,4) if k != j]+[(1,k) for k in range(j+1,4)]
        for values in itertools.product(range(4),repeat=len(free)):
            rows = [[0]*4,[0]*4];rows[0][i] = rows[1][j] = 1
            for (r,k),v in zip(free,values):rows[r][k] = v
            matrices += 1
            for u,v in itertools.product(range(4),repeat=2):
                sections = []
                for a,b in ((1,0),(0,1),(1,1),(1,2),(1,3)):
                    n = tuple(TABLE[a][x]^TABLE[b][y] for x,y in zip(*rows))
                    sections.append(normalize(n,TABLE[a][u]^TABLE[b][v]))
                C.need(len(set(sections)) == 5,'five RREF-generated sections')
                all_pencils.add(tuple(sorted(sections)))
    C.need(matrices == 357 and len(all_pencils) == 5712,'complete distinct rank-two affine pencils')
    realized = sorted(p for p in all_pencils if all(s in buckets for s in p))
    C.need(len(realized) == 5382,'complete realized catalogue')
    residual = []
    for p in realized:
        support = 0
        for n,c in p:
            for i,v in enumerate(n):
                if v:support |= 1<<i
        if support.bit_count() <= 2:continue
        if any(n == (1,0,0,0) for n,c in p):continue
        residual.append(p)
    C.need(len(residual) == 5112,'precisely the h4185 residual, with retired pencils omitted')
    return residual


def run(frontier,incidence,certificate,export=None):
    started = time.monotonic()
    data = json.loads(Path(certificate).read_text())
    C.need(data['schema'] == 'hn-radix-pair-exclusion-propagation-v1','schema')
    C.need(data['input_frontier_sha256'] == C.INPUT_SHA and data['incidence_sha256'] == C.INCIDENCE_SHA,
           'exact source interfaces')
    source,factors,sigs,buckets,old_pairs,triples,new_pairs,rowids = C.inputs(frontier,incidence)
    for row,c in rowids.items():
        values = [(a%2)+2*(b%2) for a,b in row]
        C.need(normalize(tuple(values[1:]),values[0]) == sigs[c],
               'independent table arithmetic gives the same residue signature')
    pencils = rref_catalogue(buckets)
    C.need(C.digest(pencils) == data['pencil_catalogue_sha256'],'entrywise source catalogue agreement')
    # Independent relevance enumeration: inspect all pairs of bucket choices,
    # rather than assigning each supplied exclusion to its generated pencil.
    affected = {};cross_pairs = 0
    for i,p in enumerate(pencils):
        found = set()
        for s,t in itertools.combinations(p,2):
            for a,b in itertools.product(buckets[s],buckets[t]):
                pair = (min(a,b),max(a,b));cross_pairs += 1
                C.need(pair not in old_pairs,'old pair exclusions cannot occur in any retained pencil')
                if pair in new_pairs:found.add(pair)
        if found:affected[i] = sorted(found)
    C.need(C.digest([[i,affected[i]] for i in sorted(affected)]) == data['affected_pair_assignment_sha256'],
           'every applicable exclusion assigned to its complete unique pencil')
    C.need(sum(map(len,affected.values())) == len({p for ps in affected.values() for p in ps}),
           'each applicable pair has a unique pencil')
    cores = data['three_section_cores']
    C.need([r[0] for r in cores] == sorted(affected),'exactly one obstruction for every affected pencil')
    triple_choices = 0
    for index,positions in cores:
        C.need(positions == sorted(set(positions)) and len(positions) == 3 and
               all(type(k) is int and 0<=k<5 for k in positions),'three distinct valid section indices')
        domains = [buckets[pencils[index][k]] for k in positions]
        for values in itertools.product(*domains):
            triple_choices += 1
            C.need(any((min(a,b),max(a,b)) in new_pairs for a,b in itertools.combinations(values,2)),
                   'every transversal of the three witness sections contains a proven forbidden pair')
    # The complete changed subset is counted directly from its Cartesian
    # products. The unchanged total imports the accepted h4185 baseline.
    changed = []
    for i in sorted(affected):
        p = pencils[i];raw = math.prod(len(buckets[s]) for s in p);before = 0
        for values in itertools.product(*(buckets[s] for s in p)):
            ordered = sorted(values)
            if not any(t in triples for t in itertools.combinations(ordered,3)):before += 1
        changed.append([i,raw,before])
    C.need(changed == data['closed_pencils_index_raw_before'],'every changed pencil count agrees entrywise')
    # The inherited global quotient convention is respected. No chamber
    # restriction or additional quotient is imposed on representative pairs.
    group,sig_actions = C.actions(factors,sigs,rowids)
    pen_set = set(pencils);closed_set = {pencils[i] for i in affected}
    for g,action in zip(group,sig_actions):
        C.need({tuple(sorted((g[a],g[b]))) for a,b in new_pairs} == new_pairs,
               'new physical pair exclusions are D3 invariant')
        C.need({tuple(sorted(action[s] for s in p)) for p in pen_set} == pen_set,
               'baseline pencil family is D3 invariant')
        C.need({tuple(sorted(action[s] for s in p)) for p in closed_set} == closed_set,
               'new pencil closure descends to global pair representatives')
    for row in source['remaining_exact']+source['remaining_six']:
        a,b,mask,bound,allowance = row
        orbit = [tuple(sorted((g[a],g[b]))) for g in group]
        C.need((a,b) == min(orbit) and sum(1<<i for i,p in enumerate(orbit) if p == (a,b)) == mask == 1,
               'all inherited representatives have the exact trivial stabilizer')
    pencil_by_sections = {tuple(sorted((s,t))):i for i,p in enumerate(pencils)
                          for s,t in itertools.combinations(p,2)}
    masks = {s:sum(1<<c for c in cs) for s,cs in buckets.items()}
    all_pairs = old_pairs|new_pairs
    moved = [];retained = [];witness_hash = hashlib.sha256();extension_trials = 0
    for row in source['remaining_exact']:
        a,b = row[:2];sections = {sigs[a],sigs[b]}
        C.need(len(sections) == 2,'distinct defining sections')
        i = pencil_by_sections[tuple(sorted(sections))]
        if i in affected:moved.append(row);continue
        remaining_sections = sorted((s for s in pencils[i] if s not in sections),
                                    key=lambda s:(len(buckets[s]),masks[s]))
        C.need(len(remaining_sections) == 3,'complete three-coordinate extension product')
        witness = None
        for choices in itertools.product(*(buckets[s] for s in remaining_sections)):
            extension_trials += 1;trial = sorted((a,b)+choices)
            if any(p in all_pairs for p in itertools.combinations(trial,2)):continue
            if any(t in triples for t in itertools.combinations(trial,3)):continue
            witness = trial;break
        C.need(witness is not None,'each retained pair has an actual constraint-avoiding extension')
        retained.append(row);C.digest_line(witness_hash,[row[:2],witness])
    witness_sha = witness_hash.hexdigest()
    output = C.export_result(source,pencils,affected,moved,retained,new_pairs,witness_sha)
    expected = {'schema':'hn-radix-pair-exclusion-propagation-v1',
                'input_frontier_sha256':C.INPUT_SHA,'incidence_sha256':C.INCIDENCE_SHA,
                'pencil_catalogue_sha256':C.digest(pencils),
                'affected_pair_assignment_sha256':C.digest([[i,affected[i]] for i in sorted(affected)]),
                'applicable_new_pairs':sum(map(len,affected.values())),
                'closed_pencils_index_raw_before':changed,'three_section_cores':cores,
                'baseline_lifts':128871936,
                'remaining_lifts':128871936-sum(r[2] for r in changed),
                'remaining_pencils':len(pencils)-len(affected),
                'moved_pairs':len(moved),'moved_allowance':sum(r[4] for r in moved),
                'remaining_exact_pairs':len(retained),'remaining_exact_allowance':sum(r[4] for r in retained),
                'remaining_six_pairs':len(output['remaining_six']),
                'remaining_six_allowance':sum(r[4] for r in output['remaining_six']),
                'global_pairs':len(retained)+len(output['remaining_six']),
                'global_allowance':sum(r[4] for r in retained+output['remaining_six']),
                'witness_count':len(retained),'witness_transcript_sha256':witness_sha,
                'row_hashes':{k:C.digest(output[k]) for k in
                              ('new_closed_pencils','remaining_pencil_signatures','moved','remaining_exact','remaining_six')},
                'export_canonical_sha256':C.digest(output),'record_improvement':False}
    C.need(expected == data,'all compact certificate fields verified')
    if export:
        with Path(export).open('x') as f:json.dump(output,f,sort_keys=True,separators=(',',':'));f.write('\n')
    result = {'verified':True,'baseline_pencils':5112,'closed_pencils':len(affected),
              'remaining_pencils':len(pencils)-len(affected),
              'closed_raw_lifts':sum(r[1] for r in changed),
              'closed_h4167_admissible_lifts':sum(r[2] for r in changed),
              'remaining_h4167_and_pair_admissible_lifts':expected['remaining_lifts'],
              'applicable_new_pair_exclusions':expected['applicable_new_pairs'],
              'cross_section_pair_checks':cross_pairs,'three_section_transversals_checked':triple_choices,
              'moved_pairs':len(moved),'moved_allowance':expected['moved_allowance'],
              'remaining_exact_five_pairs':len(retained),'remaining_exact_five_allowance':expected['remaining_exact_allowance'],
              'remaining_at_least_six_pairs':expected['remaining_six_pairs'],
              'remaining_at_least_six_allowance':expected['remaining_six_allowance'],
              'global_pairs_unchanged':expected['global_pairs'],'global_allowance_unchanged':expected['global_allowance'],
              'constructive_extension_witnesses':len(retained),'extension_product_trials':extension_trials,
              'all_affected_pencils_closed':True,'no_other_pair_mode_moves':True,'D3_invariant':True,
              'export_canonical_sha256':C.digest(output),'record_improvement':False}
    return result,{'elapsed_seconds':time.monotonic()-started}


if __name__ == '__main__':
    p = argparse.ArgumentParser();p.add_argument('--frontier',type=Path,required=True)
    p.add_argument('--incidence',type=Path,required=True)
    p.add_argument('--certificate',type=Path,default=C.HERE/'certificate.json')
    p.add_argument('--export-interface',type=Path);p.add_argument('--check-expected',action='store_true');a = p.parse_args()
    result,timing = run(a.frontier,a.incidence,a.certificate,a.export_interface)
    if a.check_expected:C.need(result == json.loads((C.HERE/'EXPECTED.json').read_text()),'expected exact outcome')
    print(json.dumps(result,indent=2,sort_keys=True))
