#!/usr/bin/env python3
"""Projective-pair enumeration and bitset propagation over the complete frontier."""
import argparse
import hashlib
import itertools
import json
import math
import time
from collections import defaultdict
from pathlib import Path
import common as C


def catalogue(buckets):
    signatures = sorted(buckets)
    all_pencils = {C.span(s,t) for i,s in enumerate(signatures) for t in signatures[i+1:]
                   if s[0] != t[0]}
    realized = sorted(p for p in all_pencils if all(s in buckets for s in p))
    C.need(len(realized) == 5382,'accepted complete realized pencil catalogue')
    return [p for p in realized if not C.old_closed(p)]


def constraint_masks(pairs,triples):
    pair_bad = [0]*2797;triple_bad = defaultdict(int)
    for a,b in pairs:pair_bad[a] |= 1<<b;pair_bad[b] |= 1<<a
    for a,b,c in triples:
        triple_bad[a,b] |= 1<<c;triple_bad[a,c] |= 1<<b;triple_bad[b,c] |= 1<<a
    return pair_bad,triple_bad


def ordered_domains(pencil,masks,omit=()):
    return sorted((masks[s] for s in pencil if s not in omit),key=lambda m:(m.bit_count(),m))


def count(domains,pair_bad,triple_bad):
    def visit(k,selected,bad):
        available = domains[k]&~bad
        if k == 4:return available.bit_count()
        result = 0
        while available:
            bit = available&-available;available ^= bit;curve = bit.bit_length()-1
            new_bad = bad|pair_bad[curve]
            for old in selected:new_bad |= triple_bad.get((min(old,curve),max(old,curve)),0)
            result += visit(k+1,selected+(curve,),new_bad)
        return result
    return visit(0,(),0)


def extension(pair,domains,pair_bad,triple_bad):
    a,b = pair;bad = pair_bad[a]|pair_bad[b]|triple_bad.get((a,b),0)
    def visit(k,chosen,bad):
        available = domains[k]&~bad
        while available:
            bit = available&-available;available ^= bit;curve = bit.bit_length()-1
            if k == 2:return tuple(sorted(chosen+(curve,)))
            new_bad = bad|pair_bad[curve]
            for old in chosen:new_bad |= triple_bad.get((min(old,curve),max(old,curve)),0)
            found = visit(k+1,chosen+(curve,),new_bad)
            if found is not None:return found
        return None
    return visit(0,tuple(pair),bad)


def run(frontier,incidence,export=None):
    start = time.monotonic()
    source,factors,sigs,buckets,old_pairs,triples,new_pairs,rowids = C.inputs(frontier,incidence)
    pencils = catalogue(buckets);C.need(len(pencils) == 5112,'complete surviving pencil frontier')
    ids = {p:i for i,p in enumerate(pencils)}
    masks = {s:sum(1<<c for c in cs) for s,cs in buckets.items()}
    affected = defaultdict(list)
    for a,b in sorted(new_pairs):
        if sigs[a][0] != sigs[b][0]:
            pencil = C.span(sigs[a],sigs[b])
            if pencil in ids:affected[ids[pencil]].append((a,b))
    old_masks = constraint_masks(old_pairs,triples)
    all_pairs = old_pairs|new_pairs
    new_masks = constraint_masks(all_pairs,triples)
    only_new,_ = constraint_masks(new_pairs,set())
    counts = [];closed = [];cores = []
    for i,pencil in enumerate(pencils):
        domains = ordered_domains(pencil,masks)
        before = count(domains,*old_masks)
        after = count(domains,*new_masks) if i in affected else before
        raw = math.prod(len(buckets[s]) for s in pencil)
        counts.append([i,raw,before,after])
        if i not in affected:continue
        C.need(after == 0,'complete closure of every affected pencil')
        closed.append([i,raw,before])
        for positions in itertools.combinations(range(5),3):
            a,b,c = [pencil[k] for k in positions]
            if all((only_new[u]>>v)&1 or not (masks[c]&~(only_new[u]|only_new[v]))
                   for u in buckets[a] for v in buckets[b]):
                cores.append([i,list(positions)]);break
        else:raise ValueError('missing three-section obstruction')
    C.need(sum(r[2] for r in counts) == 128871936,'complete h4185 lift baseline reproduced')
    moved = [];retained = [];witness_hash = hashlib.sha256()
    for row in source['remaining_exact']:
        a,b = row[:2];pencil = C.span(sigs[a],sigs[b]);i = ids[pencil]
        if i in affected:moved.append(row);continue
        domains = ordered_domains(pencil,masks,{sigs[a],sigs[b]})
        C.need(len(domains) == 3,'two distinct defining sections')
        witness = extension((a,b),domains,*new_masks)
        C.need(witness is not None,'every retained exact-five pair has an admissible extension')
        C.need(not any(p in all_pairs for p in itertools.combinations(witness,2)) and
               not any(t in triples for t in itertools.combinations(witness,3)),
               'direct membership check of each constructive extension')
        retained.append(row);C.digest_line(witness_hash,[row[:2],list(witness)])
    transcript = witness_hash.hexdigest()
    output = C.export_result(source,pencils,affected,moved,retained,new_pairs,transcript,export)
    certificate = {'schema':'hn-radix-pair-exclusion-propagation-v1',
                   'input_frontier_sha256':C.INPUT_SHA,'incidence_sha256':C.INCIDENCE_SHA,
                   'pencil_catalogue_sha256':C.digest(pencils),
                   'affected_pair_assignment_sha256':C.digest([[i,affected[i]] for i in sorted(affected)]),
                   'applicable_new_pairs':sum(map(len,affected.values())),
                   'closed_pencils_index_raw_before':closed,'three_section_cores':cores,
                   'baseline_lifts':sum(r[2] for r in counts),
                   'remaining_lifts':sum(r[3] for r in counts),
                   'remaining_pencils':len(pencils)-len(affected),
                   'moved_pairs':len(moved),'moved_allowance':sum(r[4] for r in moved),
                   'remaining_exact_pairs':len(retained),
                   'remaining_exact_allowance':sum(r[4] for r in retained),
                   'remaining_six_pairs':len(output['remaining_six']),
                   'remaining_six_allowance':sum(r[4] for r in output['remaining_six']),
                   'global_pairs':len(retained)+len(output['remaining_six']),
                   'global_allowance':sum(r[4] for r in retained+output['remaining_six']),
                   'witness_count':len(retained),'witness_transcript_sha256':transcript,
                   'row_hashes':{k:C.digest(output[k]) for k in
                                 ('new_closed_pencils','remaining_pencil_signatures','moved','remaining_exact','remaining_six')},
                   'export_canonical_sha256':C.digest(output),'record_improvement':False}
    return certificate,{'elapsed_seconds':time.monotonic()-start,
                        'producer_full_count_transcript_sha256':C.digest(counts)}


if __name__ == '__main__':
    p = argparse.ArgumentParser();p.add_argument('--frontier',type=Path,required=True)
    p.add_argument('--incidence',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--export-interface',type=Path);a = p.parse_args()
    cert,timing = run(a.frontier,a.incidence,a.export_interface)
    with a.out.open('x') as f:json.dump(cert,f,sort_keys=True,separators=(',',':'));f.write('\n')
    print(json.dumps({'certificate_bytes':a.out.stat().st_size,
                      'certificate_sha256':hashlib.sha256(a.out.read_bytes()).hexdigest(),**timing},indent=2))
