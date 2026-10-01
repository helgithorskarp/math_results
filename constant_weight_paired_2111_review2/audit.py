"""Complete independent raw two-star census and literal certificate check.

The eight-class theorem is imported from the prior independently reviewed
classification. Published coloring partitions are UNTRUSTED inputs, checked
from sets; no author executable code is imported or run.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import os
import resource
import subprocess
import time
from incidence import canonical, image, need

BASE = Path(__file__).resolve().parent
CERT_SHA = '43a3abc63f75013b5601c4ba5c1d227bff5d7f8befcbf8af10887535e875ce76'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def points(w, n=18):
    return frozenset(z for z in range(n) if w >> z & 1)


def union_check(left, right):
    words = tuple(sorted(set(left) | set(right)))
    literal = [points(w) for w in words]
    need(len(left) == len(right) == 20 and len(set(left) & set(right)) == 3 and len(words) == 37, 'bad joint-star coverage')
    need(all(len(w) == 5 for w in literal) and all(len(a & b) <= 2 for a, b in combinations(literal, 2)), 'invalid literal joint code')
    for x in (0, 17):
        need(sum(x in w for w in literal) == 20, 'unsaturated center')
        row = sorted(5 - sum(x in w and y in w for w in literal) for y in range(18) if y != x)
        need(row == [0]*13 + [1,1,1,2], 'bad literal center deficit row')
    return words


def check_partition(candidates, partition):
    need(isinstance(partition, list) and partition and all(isinstance(c, list) and c for c in partition), 'malformed partition')
    flat = [z for c in partition for z in c]
    need(all(type(z) is int for z in flat) and sorted(flat) == list(range(len(candidates))), 'partition does not cover the complete domain exactly once')
    for c in partition:
        need(all(len(candidates[a] & candidates[b]) >= 3 for a, b in combinations(c, 2)), 'nonconflicting words share a partition class')
    return len(partition)


def run(target, work, raw_input=None):
    started = time.monotonic()
    work.mkdir(parents=True, exist_ok=True)
    raw = (target/'certificates.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == CERT_SHA, 'target certificate provenance mismatch')
    authored = json.loads(raw)
    stars = [tuple(q) for q in json.loads((BASE/'templates.json').read_text())]
    need(len(stars) == 8, 'wrong template carrier')
    target_stars = [tuple(o['representative']) for f in json.loads((target/'expected.json').read_text())['packing_families'] for o in f['orbits']]
    need(stars == target_stars, 'imported representatives differ')
    groups, group_states = [], []
    for star in stars:
        need(len(star) == len(set(star)) == 20 and all(len(points(w,17)) == 4 for w in star), 'invalid template')
        need(all(len(points(a,17) & points(b,17)) <= 1 for a,b in combinations(star,2)), 'template pair conflict')
        need([sum(w >> z & 1 for w in star) for z in range(17)] == [3,4,4,4]+[5]*13, 'template profile mismatch')
        result = canonical(star, 17, ((0,), (1,2,3), tuple(range(4,17))))
        groups.append(tuple(p+(17,) for p in result['automorphisms']))
        group_states.append(result['states'])
    need([len(g) for g in groups] == authored['star_automorphism_orders'], 'complete group orders differ')
    data = '\n'.join(' '.join(map(str, s)) for s in stars)+'\n'
    (work/'templates.txt').write_text(data)
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
    stream = work/'raw.txt' if raw_input is None else raw_input
    native_start = time.monotonic()
    if raw_input is None:
        subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic','-Werror',str(BASE/'raw_pairs.cpp'),'-o',str(work/'raw_pairs')], check=True, env=env, timeout=60)
        with (work/'templates.txt').open('rb') as f, stream.open('wb') as out:
            subprocess.run([str(work/'raw_pairs'),'0','64','200000','10'],stdin=f,stdout=out,check=True,env=env,timeout=300)
    native_seconds = time.monotonic()-native_start
    families, counts, summaries = {}, [[0]*8 for _ in range(8)], []
    mapping_digest = hashlib.sha256()
    maps = set()
    for line in stream.read_text().splitlines():
        fields = line.split()
        if fields[0] == 'MAP':
            need(len(fields) == 20, 'bad native mapping output')
            i,j = map(int, fields[1:3]); p = tuple(map(int, fields[3:]))
            need(0 <= i < 8 and 0 <= j < 8 and p[0] == 17 and sorted(p[1:]) == list(range(1,17)), 'bad full point bijection')
            key = (i,j,p)
            need(key not in maps, 'duplicate native raw labeling')
            maps.add(key)
            mapping_digest.update((line+'\n').encode())
            left = tuple(sorted(w | (1<<17) for w in stars[i]))
            right = tuple(sorted(1 | sum(1<<p[z] for z in range(17) if w >> z & 1) for w in stars[j]))
            union_check(left, right)
            normal = min(image(right, a) for a in groups[i])
            families.setdefault((i,j), {}).setdefault(normal, 0)
            families[(i,j)][normal] += 1
            counts[i][j] += 1
        else:
            need(fields[0] == 'PAIR' and len(fields) == 9 and fields[-1] == 'COMPLETE', 'INCOMPLETE native record')
            i,j,nine,tail,assignments,accepted,positive = map(int, fields[1:-1])
            need([nine,tail,assignments] == [362880,1296,6531840] and accepted == counts[i][j], 'incomplete native pair coverage')
            need(i*8+j == len(summaries), 'missing or unordered pair record')
            summaries.append(dict(first=i, second=j, nine_permutations=nine, aligned_tails=tail, assignments=assignments, accepted=accepted, positive_raw_fibers=positive))
    need(len(summaries) == 64 and counts == authored['raw_compatible_counts'] and len(maps) == authored['raw_compatible_maps'], 'raw compatibility census differs')
    classes, table = [], [[0]*8 for _ in range(8)]
    for i in range(8):
        left = tuple(sorted(w | (1<<17) for w in stars[i]))
        for j in range(8):
            family = families.get((i,j), {})
            table[i][j] = len(family)
            for right, multiplicity in sorted(family.items()):
                words = union_check(left,right)
                stabilizer = [p for p in groups[i] if image(right,p) == right]
                need(multiplicity * len(stabilizer) == len(groups[i])*len(groups[j]), 'raw orbit-stabilizer mass differs')
                classes.append(dict(index=len(classes),first=i,second=j,left=left,right=right,raw_multiplicity=multiplicity,center_fixing_order=len(stabilizer)))
    need(len(classes) == 128 and table == authored['ordered_joint_counts'], 'ordered-center class census differs')
    certificates = authored['color_certificates']
    need(len(certificates) == len(classes), 'certificate carrier mismatch')
    domains, checks, unordered, ordered = [], [], {}, set()
    total_pairs, incidence_states, max_states = 0, 0, 0
    for entry, cert in zip(classes, certificates):
        i,j = entry['first'],entry['second']
        need([cert['index'],cert['first'],cert['second']] == [entry['index'],i,j], 'certificate class indexing differs')
        words = union_check(entry['left'], entry['right'])
        fixed = tuple(points(w) for w in words)
        candidates = [frozenset(c) for c in combinations(range(1,17),5) if all(len(set(c)&w) <= 2 for w in fixed)]
        # Certificate indices use lexicographic FIVE-SUBSET order, with the
        # original labels 1,...,16. Numeric mask sorting would change indices.
        masks = [sum(1<<z for z in c) for c in candidates]
        need(len(candidates) == cert['candidates'] and hashlib.sha256(json.dumps(masks,separators=(',',':')).encode()).hexdigest() == cert['candidate_sha256'], 'literal residual domain differs entrywise')
        upper = check_partition(candidates, cert['partition'])
        need(upper == cert['certified_residual_upper'] and 37+upper == cert['certified_code_upper'] and upper <= 29, 'bad certificate bound')
        total_pairs += sum(len(c)*(len(c)-1)//2 for c in cert['partition'])
        marked = canonical(words,18,((0,),(17,),tuple(range(1,17))))
        unmarked = canonical(words,18,((0,17),tuple(range(1,17))))
        need(marked['order'] == entry['center_fixing_order'], 'independent full-incidence stabilizer differs')
        need(marked['canonical'] not in ordered, 'ordered classes duplicate under full incidence')
        ordered.add(marked['canonical'])
        group = unordered.setdefault(unmarked['canonical'], [])
        group.append(entry['index'])
        swapped = [p for p in unmarked['automorphisms'] if p[0] == 17]
        need(unmarked['order'] == marked['order']*(2 if swapped else 1), 'center-swap group index differs')
        if swapped:
            need(i == j, 'swap interchanges nonisomorphic star templates')
        incidence_states += marked['states']+unmarked['states']
        max_states = max(max_states,marked['states'],unmarked['states'])
        checks.append(dict(index=entry['index'],first=i,second=j,candidates=len(candidates),candidate_sha256=cert['candidate_sha256'],residual_upper=upper,code_upper=37+upper,raw_multiplicity=entry['raw_multiplicity'],center_fixing_order=marked['order'],center_set_order=unmarked['order'],admits_center_swap=bool(swapped),marked_states=marked['states'],unmarked_states=unmarked['states']))
        domains.append(masks)
    need(len(ordered) == 128 and all(1 <= len(v) <= 2 for v in unordered.values()), 'bad named-to-unordered quotient')
    for indexes in unordered.values():
        a = checks[indexes[0]]
        need((len(indexes) == 1) == a['admits_center_swap'], 'swap fixed-point quotient mismatch')
    result = dict(agent='six-reviewer-2',role='independent mathematical reviewer',status='COMPLETE direct all-labeling audit',
                  imported_eight_class_completeness=True,certificate_sha256=CERT_SHA,
                  group_orders=[len(g) for g in groups],group_states=group_states,
                  total_nine_permutations=sum(s['nine_permutations'] for s in summaries),
                  raw_fibers=sum(s['aligned_tails'] for s in summaries),
                  raw_assignments=sum(s['assignments'] for s in summaries),
                  compatible_maps=len(maps),raw_mapping_stream_sha256=mapping_digest.hexdigest(),
                  raw_counts=counts,raw_pair_coverage=summaries,ordered_joint_classes=len(classes),ordered_counts=table,
                  unordered_center_classes=len(unordered),center_swap_fixed_ordered_classes=sum(q['admits_center_swap'] for q in checks),
                  unordered_orbits=sorted(sorted(v) for v in unordered.values()),
                  ordered_class_sha256=digest(classes),residual_domains_sha256=digest(domains),
                  candidate_range=[min(q['candidates'] for q in checks),max(q['candidates'] for q in checks)],
                  complete_candidate_universes=len(classes)*4368,total_candidates=sum(q['candidates'] for q in checks),
                  literal_partition_pairs=total_pairs,maximum_code_upper=max(q['code_upper'] for q in checks),
                  bound_histogram={str(k):v for k,v in sorted(Counter(q['code_upper'] for q in checks).items())},
                  incidence_total_states=incidence_states,incidence_max_states=max_states,classes=checks,
                  guards=dict(native_fiber_nodes=200000,native_fiber_seconds=10,incidence_nodes=200000,incidence_seconds=10))
    expected = json.loads((BASE/'expected.json').read_text())
    need(digest(result) == expected['audit_record_sha256'], 'independent complete audit record differs from frozen expectation')
    for key in ('raw_mapping_stream_sha256','ordered_class_sha256','residual_domains_sha256','raw_assignments','compatible_maps','ordered_joint_classes','unordered_center_classes','center_swap_fixed_ordered_classes','maximum_code_upper'):
        need(result[key] == expected[key], 'independent result field differs: '+key)
    (work/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
    (work/'joint-classes.json').write_text(json.dumps(classes,indent=2)+'\n')
    metrics=dict(seconds=time.monotonic()-started,native_seconds=native_seconds,raw_reused=raw_input is not None,parent_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,child_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    (work/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','raw_assignments','compatible_maps','ordered_joint_classes','unordered_center_classes','center_swap_fixed_ordered_classes','maximum_code_upper')}),flush=True)
    print(json.dumps(metrics),flush=True)
    return result


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--target',type=Path,required=True)
    p.add_argument('--work',type=Path,required=True)
    p.add_argument('--raw-input',type=Path,help='recheck a saved COMPLETE raw census; does not rerun enumeration')
    a=p.parse_args()
    run(a.target.resolve(),a.work.resolve(),None if a.raw_input is None else a.raw_input.resolve())
