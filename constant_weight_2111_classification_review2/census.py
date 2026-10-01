"""Independent carrier and exact-cover census for shortened (2,1,1,1) stars."""
from pathlib import Path
from itertools import combinations
from hashlib import sha256
import argparse
import json
import resource
import subprocess
import time
import carrier as c

HERE = Path(__file__).resolve().parent

def native(binary, columns, required, work, index, cap=200000):
    c.require(len(columns) <= 840, 'native capacity exceeded; no verdict')
    inp, out = work / ('case-' + str(index) + '.input'), work / ('case-' + str(index) + '.jsonl')
    missing = [i for i, pair in enumerate(c.PAIRS) if pair not in set(required)]
    lines = ['17 ' + str(len(columns)) + ' 1', *map(str, columns), str(index) + ' ' + str(len(missing)) + ' ' + ' '.join(map(str, missing))]
    inp.write_text('\n'.join(lines) + '\n')
    p = subprocess.run([str(binary), str(inp), str(out), str(cap)], capture_output=True, text=True, timeout=15)
    c.require(p.returncode == 0, 'Native census failed / INCOMPLETE: ' + p.stderr)
    summary = json.loads(p.stdout)
    answer = json.loads(out.read_text())
    c.require(summary['status'] == 'COMPLETE' and summary['cases'] == 1 and answer['index'] == index, 'native census output malformed')
    covers = tuple(tuple(w) for w in answer['covers'])
    c.require(covers == tuple(sorted(set(covers))), 'native cover domain duplicated or unsorted')
    available = set(required)
    for cover in covers:
        c.require(len(cover) * 6 == len(required) and set(cover) <= set(columns), 'native cover words/size invalid')
        occupied = c.covered_pairs(cover)
        c.require(len(occupied) == 6 * len(cover) and occupied == available, 'native returned cover has wrong literal pairs')
    return covers, answer['states']

def run(work, target):
    work.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    source = HERE / 'partition.cpp'
    binary = work / 'partition'
    subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic', str(source), '-o', str(binary)], capture_output=True, text=True, check=True, timeout=30)
    expected = json.loads(target.read_text())
    external = {(q['index'], q['prefix_index']): q for q in expected['fibers']}
    leaves = c.leave_carrier()
    carriers, fibers, corpus = [], [], {}
    total_states, total_covers, max_states = 0, 0, 0
    for leave in leaves:
        hub = c.hub_orbits(leave)
        carriers.append(hub)
        for orbit in hub['orbits']:
            index, prefix_index = leave['index'], orbit['index']
            prefix = orbit['words']
            required, columns, matrix_hash = c.matrix(leave['leave'], prefix)
            pin = external[index, prefix_index]
            c.require(matrix_hash == pin['hub_matrix_sha256'] and len(columns) == pin['hub_candidates'], 'independent first-hub matrix differs from authenticated compact source')
            fixed = prefix
            transports = None
            if index == 5 and prefix_index == 0:
                fixed, partitions, transports = c.second_prefix(leave, prefix)
                required, columns, matrix_hash = c.matrix(leave['leave'], fixed)
                c.require(c.digest(partitions) == expected['next_star_normalization']['partition_domain_sha256'], 'second-point partition digest mismatch')
                c.require(c.digest(transports) == expected['next_star_normalization']['transport_maps_sha256'], 'second-point literal transport digest mismatch')
            c.require(matrix_hash == pin['matrix_sha256'] and len(columns) == pin['candidates'] and len(required) == pin['columns'], 'independent proof matrix differs from authenticated compact source')
            covers, states = native(binary, columns, required, work, len(fibers))
            c.require(len(covers) == pin['covers'] and c.digest(covers) == pin['covers_sha256'], 'independent full native cover stream differs from authenticated compact source')
            stars = set()
            for cover in covers:
                star = tuple(sorted(fixed + cover))
                c.check_star(star, leave['leave'])
                if transports is None:
                    stars.add(star)
                else:
                    for point in transports:
                        restored = c.image_star(star, c.inverse(point))
                        c.check_star(restored, leave['leave'])
                        c.require(tuple(sorted(w for w in restored if w & 1)) == prefix, 'second-point reconstruction changes first hub')
                        c.require(restored not in stars, 'second-point restored cover domains overlap')
                        stars.add(restored)
            if transports is not None:
                c.require(len(stars) == 210 * len(covers), 'second-point multiplicity reconstruction incomplete')
            if stars:
                corpus[index, prefix_index] = stars
                (work / ('stars-' + str(index) + '-' + str(prefix_index) + '.json')).write_text(json.dumps(sorted(stars), separators=(',', ':')) + '\n')
            rec = dict(index=index, prefix_index=prefix_index, orbit_size=orbit['orbit_size'], matrix_sha256=matrix_hash, matrix_pairs=len(required), candidates=len(columns), proof_covers=len(covers), covers_sha256=c.digest(covers), restored_covers=len(stars), corpus_sha256=c.digest(sorted(stars)), native_states=states)
            fibers.append(rec)
            total_states += states
            max_states = max(max_states, states)
            total_covers += len(stars)
            print(json.dumps(rec), flush=True)
            (work / 'progress.json').write_text(json.dumps({'status': 'PARTIAL', 'complete_fibers': fibers, 'states': total_states}, indent=2) + '\n')
    c.require(len(fibers) == 75 and sum(h['valid_partitions'] for h in carriers) == 1224, 'independent complete fiber carrier size differs')
    c.require(total_covers == 45504 and len(corpus) == 6 and sum(q['proof_covers'] == 0 for q in fibers) == 69, 'independent cover census differs')
    stable = dict(agent='six-reviewer-2', role='independent mathematical reviewer', status='COMPLETE independent carrier and native cover census', leaves=leaves, hub_carriers=carriers, fibers=fibers, total_covers=total_covers, total_states=total_states, max_states=max_states)
    (work / 'census.json').write_text(json.dumps(stable, indent=2) + '\n')
    metrics = dict(status=stable['status'], seconds=time.monotonic() - started, parent_peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, child_peak_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss, fibers=len(fibers), restored_covers=total_covers, native_states=total_states, max_native_states=max_states, source_sha256=sha256(source.read_bytes()).hexdigest(), census_sha256=c.digest(stable))
    (work / 'metrics.json').write_text(json.dumps(metrics, indent=2) + '\n')
    print(json.dumps(metrics, indent=2), flush=True)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--target', type=Path, required=True)
    a = p.parse_args()
    run(a.work.resolve(), a.target.resolve())
