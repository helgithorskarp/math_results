#!/usr/bin/env python3
"""Independent field geometry BFS, character transport, positive witness replay."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


def demand(ok, why):
    if not ok:
        raise ValueError(why)


def verify(cover, folder):
    p = 617
    demand(cover['schema'] == 'boolean617-field-geometry-cover-v1' and cover['prime'] == p, 'schema/prime')
    # A two-generator breadth-first closure, not the producer's six permutations.
    unseen = set(range(2, p))
    components = {}
    histogram = Counter()
    while unseen:
        first = min(unseen)
        reached = {first}
        queue = [first]
        while queue:
            t = queue.pop()
            for u in ((1-t) % p, pow(t, -1, p)):
                if u not in reached:
                    reached.add(u)
                    queue.append(u)
        demand(reached <= unseen, 'distinct geometry components')
        unseen -= reached
        for t in reached:
            components[t] = first
        histogram[len(reached)] += 1
    geometries = sorted(set(components.values()))
    demand(len(geometries) == 103 and histogram == {3: 1, 6: 102}, 'complete root geometry cover')
    demand(cover['geometries'] == geometries, 'canonical representatives')
    maps = cover['maps']
    demand(len(maps) == 615 and [m['t'] for m in maps] == list(range(2, p)), 'all original normalized geometries')
    squares = {x*x % p for x in range(1, p)}
    demand(len(squares) == 308, 'square-set size')
    def bit(z):
        demand(z % p != 0, 'undefined original root')
        return int(z % p not in squares)
    data = {}
    for t in geometries:
        data[t] = json.loads((folder/f't{t:03}.json').read_text())
        demand(data[t]['roots'] == [0,1,t], 'geometry source identity')
        receipt = json.loads((folder/f't{t:03}-check.json').read_text())
        demand(receipt['status'] == 'EXACT_CORE_FILTER_CHECKED' and receipt['t'] == t, 'full core checker receipt')
        demand(receipt['transcript_sha256'] == data[t]['transcript_sha256'], 'source/checked transcript match')
    coordinates = abstract_entries = points = raw_blocked = raw_survivors = 0
    projected = [170, 204, 240]
    transport_stream = hashlib.sha256()
    for row in maps:
        t, u = row['t'], row['representative']
        demand(u == components[t], 'BFS component mismatch')
        roots = (0,1,t)
        order = row['root_order']
        demand(sorted(order) == [0,1,2], 'root permutation')
        shift, scale = row['inverse_map_shift'], row['inverse_map_scale']
        demand(type(shift) is int and type(scale) is int and 0 <= shift < p and 1 <= scale < p, 'affine map')
        target = (0,1,u)
        for i in range(3):
            demand((shift+scale*target[i]) % p == roots[order[i]], 'all three affine root identities')
        epsilon = bit(scale)
        inverse = pow(scale, -1, p)
        for x in range(p):
            if x in roots:
                continue
            y = (x-shift)*inverse % p
            demand(y not in target, 'regular coordinate maps to a free root')
            for i in range(3):
                demand(bit(y-target[i]) == (bit(x-roots[order[i]]) ^ epsilon), 'actual character coordinate transport')
                coordinates += 1
        for word in range(0,256,2):
            values = []
            for new_index in range(8):
                old_index = 0
                for i in range(3):
                    v = new_index // (2**i) % 2
                    old_index += (v ^ epsilon) * (2 ** order[i])
                values.append(word // (2 ** old_index) % 2)
                abstract_entries += 1
            flip = values[0]
            changed = sum((v ^ flip) * (2 ** i) for i,v in enumerate(values))
            demand(changed % 2 == 0, 'output gauge')
            if changed in data[u]['survivor_words']:
                # This deduction uses the complete independently replayed AP scan.
                demand(word in projected, 'a nonprojection rule survives the canonical core')
                raw_survivors += 1
                continue
            demand(str(changed) in data[u]['witnesses'], 'missing positive source AP')
            a, d = data[u]['witnesses'][str(changed)]
            old_a = (shift + scale*a) % p
            old_d = scale*d % p
            demand(old_d != 0, 'transported AP became constant')
            if old_d > 308:
                old_a = (old_a+6*old_d) % p
                old_d = p-old_d
            colors = []
            for k in range(7):
                x = (old_a+k*old_d) % p
                demand(x not in roots, 'transported positive AP meets an original free root')
                index = sum(bit(x-r) * (2 ** j) for j,r in enumerate(roots))
                colors.append(word // (2 ** index) % 2)
                points += 1
            demand(len(set(colors)) == 1, 'literal raw-state witness failed')
            demand(1 <= old_d <= 308, 'short-step witness')
            transport_stream.update(f'{t},{word},{old_a},{old_d}\n'.encode())
            raw_blocked += 1
    demand(raw_blocked + raw_survivors == 615*128, 'all raw truth states covered')
    return {'schema':'boolean617-field-cover-check-v1', 'status':'COMPLETE_RAW_THREE_ROOT_CORE_CLASSIFICATION',
            'geometry_count':103, 'geometry_size_histogram':dict(sorted(histogram.items())),
            'canonical_truth_states':103*128, 'raw_truth_states':615*128,
            'raw_states_with_literal_positive_witness':raw_blocked,
            'raw_core_survivors':raw_survivors, 'literal_raw_witness_points':points,
            'actual_character_coordinate_identities':coordinates,
            'abstract_truth_entries':abstract_entries,
            'raw_witness_transcript_sha256':transport_stream.hexdigest(),
            'only_possible_gauged_survivors':projected,
            'scope':'Necessary regular cyclic617 core; not a full interval quotient or a 3704 coloring.'}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--cover',type=Path,required=True)
    parser.add_argument('--data',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    receipt=verify(json.loads(args.cover.read_text()),args.data)
    args.output.write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps(receipt))


if __name__=='__main__':
    main()
