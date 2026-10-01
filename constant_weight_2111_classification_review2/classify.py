"""Reviewer-owned Schreier-stabilizer packing orbits and incidence audit."""
from collections import deque
from pathlib import Path
from itertools import combinations
from math import factorial
from fractions import Fraction
import argparse
import json
import resource
import time
import carrier as c
from incidence import canonical, group_invariants

def reduce_generators(candidates, order):
    start, states = time.monotonic(), 0
    candidates = tuple(map(tuple, candidates))
    closure, generators = {c.IDENTITY}, []
    for candidate in sorted(set(candidates)):
        if candidate in closure:
            continue
        generators.append(candidate)
        closure = {c.IDENTITY}
        queue = deque([c.IDENTITY])
        while queue:
            point = queue.popleft()
            states += 1
            c.require(states <= 200000 and time.monotonic() - start <= 10, 'INCOMPLETE stabilizer closure guard')
            for gen in generators:
                target = c.compose(gen, point)
                if target not in closure:
                    closure.add(target)
                    queue.append(target)
        c.require(len(closure) <= order and order % len(closure) == 0, 'Schreier subgroup order impossible')
    c.require(len(closure) == order and set(candidates) <= closure, 'incomplete Schreier stabilizer closure')
    return tuple(generators), states

def packing_orbits(record, hub_orbit, stars):
    start = time.monotonic()
    small_gens, closure_states = reduce_generators(hub_orbit['stabilizer_generators'], hub_orbit['stabilizer_order'])
    generators = list(small_gens)
    cohort = record['cohorts'][0]
    for a, b in zip(cohort, cohort[1:]):
        point = list(c.IDENTITY)
        point[a], point[b] = b, a
        generators.append(tuple(point))
    for gen in generators:
        c.require(sorted(gen) == list(range(c.N)) and c.image_edges(record['leave'], gen) == tuple(map(tuple, record['leave'])) and c.image_star(tuple(hub_orbit['words']), gen) == tuple(hub_orbit['words']), 'false full prefix stabilizer generator')
    full_order = hub_orbit['stabilizer_order'] * factorial(len(cohort))
    words = set().union(*map(set, stars))
    maps = [{w: c.image_word(w, gen) for w in words} for gen in generators]
    unseen, orbits, states = set(stars), [], 0
    while unseen:
        rep = min(unseen)
        orbit = {rep}
        queue = deque([rep])
        while queue:
            star = queue.popleft()
            states += 1
            c.require(states <= 200000 and time.monotonic() - start <= 10, 'INCOMPLETE packing orbit guard')
            for point_map in maps:
                target = tuple(sorted(point_map[w] for w in star))
                c.require(target in stars, 'prefix generator leaves complete native census')
                if target not in orbit:
                    orbit.add(target)
                    queue.append(target)
        c.require(orbit <= unseen and full_order % len(orbit) == 0, 'packing orbit overlap/order impossible')
        unseen.difference_update(orbit)
        direct = canonical(rep)
        c.require(direct['order'] == full_order // len(orbit), 'independent incidence automorphism order differs from packing orbit')
        orbits.append(dict(representative=rep, orbit_size=len(orbit), automorphism_order=direct['order'], orbit_sha256=c.digest(sorted(orbit)), canonical_sha256=c.digest(direct['canonical']), incidence_states=direct['states'], incidence_leaves=direct['leaves'], automorphism_maps_sha256=c.digest(direct['automorphisms']), group_invariants=group_invariants(direct['automorphisms'])))
    c.require(sum(o['orbit_size'] for o in orbits) == len(stars), 'packing orbit coverage incomplete')
    return dict(index=record['index'], prefix_index=hub_orbit['index'], full_prefix_group_order=full_order, generators=len(generators), closure_states=closure_states, packing_states=states, corpus_sha256=c.digest(sorted(stars)), orbits=orbits)

def run(work, target):
    start = time.monotonic()
    census = json.loads((work / 'census.json').read_text())
    c.require(census['status'] == 'COMPLETE independent carrier and native cover census', 'complete native census required')
    expected = json.loads(target.read_text())
    pins = {(f['index'], f['prefix_index']): f for f in expected['packing_families']}
    families = []
    for f in census['fibers']:
        if not f['restored_covers']:
            continue
        index, prefix = f['index'], f['prefix_index']
        stars = set(map(tuple, json.loads((work / ('stars-' + str(index) + '-' + str(prefix) + '.json')).read_text())))
        c.require(len(stars) == f['restored_covers'] and c.digest(sorted(stars)) == f['corpus_sha256'], 'native corpus provenance differs')
        record = census['leaves'][index]
        record['core'] = tuple(map(tuple, record['core']))
        record['leave'] = tuple(map(tuple, record['leave']))
        orbit = census['hub_carriers'][index]['orbits'][prefix]
        family = packing_orbits(record, orbit, stars)
        pin = pins[index, prefix]
        c.require(family['full_prefix_group_order'] == pin['full_prefix_group_order'] and family['corpus_sha256'] == pin['corpus_sha256'] and len(family['orbits']) == len(pin['orbits']), 'independent complete packing quotient differs from compact target')
        for own, original in zip(family['orbits'], pin['orbits']):
            c.require(list(own['representative']) == original['representative'] and own['orbit_size'] == original['orbit_size'] and own['automorphism_order'] == original['packing_automorphism_order'] and own['orbit_sha256'] == original['orbit_sha256'], 'independent packing orbit or representative differs from target')
        families.append(family)
        print(json.dumps(family), flush=True)
        (work / 'classify-progress.json').write_text(json.dumps({'status':'PARTIAL', 'families':families}, indent=2) + '\n')
    all_orbits = [o for f in families for o in f['orbits']]
    c.require(len(all_orbits) == 8 and len({o['canonical_sha256'] for o in all_orbits}) == 8, 'eight intrinsically distinct incidence certificates required')
    by_leaf = {}
    for f in census['fibers']:
        by_leaf[f['index']] = by_leaf.get(f['index'], 0) + f['orbit_size'] * f['restored_covers']
    attachment_total = 0
    for record in census['leaves']:
        m = len(record['matching'])
        attachments = Fraction(factorial(13), 2 ** m * factorial(m))
        for cohort in record['cohorts']:
            attachments /= factorial(len(cohort))
        c.require(attachments.denominator == 1, 'nonintegral attachment count')
        attachment_total += record['orbit_size'] * attachments * by_leaf[record['index']]
    orbit_total = sum(Fraction(factorial(3) * factorial(13), o['automorphism_order']) for o in all_orbits)
    c.require(attachment_total == orbit_total == 66421555200, 'independent labeled count bridges disagree')
    stable = dict(agent='six-reviewer-2', role='independent mathematical reviewer', status='COMPLETE eight packing classes and corrected full automorphism orders', families=families, automorphism_orders=[o['automorphism_order'] for o in all_orbits], canonical_leave_covers=by_leaf, fixed_profile_labeled_packings=int(orbit_total), incidence_states=sum(o['incidence_states'] for o in all_orbits), packing_states=sum(f['packing_states'] for f in families), closure_states=sum(f['closure_states'] for f in families))
    (work / 'classification.json').write_text(json.dumps(stable, indent=2) + '\n')
    metrics = dict(status=stable['status'], seconds=time.monotonic()-start, parent_peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, classification_sha256=c.digest(stable), automorphism_orders=stable['automorphism_orders'], incidence_states=stable['incidence_states'], packing_states=stable['packing_states'], closure_states=stable['closure_states'])
    (work / 'classification-metrics.json').write_text(json.dumps(metrics, indent=2)+'\n')
    print(json.dumps(metrics, indent=2), flush=True)

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--target', type=Path, required=True)
    a=p.parse_args()
    run(a.work.resolve(), a.target.resolve())
