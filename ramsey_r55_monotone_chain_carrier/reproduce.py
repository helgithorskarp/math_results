"""Exact count/partition/protocol controls. No target search or queue writes."""
import argparse
from collections import Counter
import copy
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import tempfile
import chains
import check
import counts
import receiver

HERE = Path(__file__).resolve().parent


def must(test, text):
    if not test:
        raise ValueError(text)


def rejected(packet):
    try:
        check.check(packet)
    except (ValueError, KeyError, TypeError, IndexError):
        return True
    return False


def controls(cache_dir=None, drat_trim=None):
    rectangles = 0
    for a in range(1, 21):
        for b in range(1, 21):
            seen = set()
            for t in range(min(a, b)):
                seq = chains.hook(a, b, t)
                must(len(seq) == a+b-1-2*t, 'hook length')
                must(sum(seq[0])+sum(seq[-1]) == a+b-2, 'rank symmetry')
                for h, point in enumerate(seq):
                    must(point not in seen, 'hook overlap')
                    seen.add(point)
                    must(chains.hook_address(a, b, *point) == (t, h), 'rectangle rank')
                    must(chains.hook_inverse(a, b, t, h) == point, 'rectangle unrank')
            must(seen == set(product(range(a), range(b))), 'rectangle coverage')
            rectangles += len(seen)
    partitions, states_checked = 0, 0
    patterns = [cs for m in range(4) for cs in product((0, 1), repeat=m)]+[(0, 1, 0, 1)]
    for cs in patterns:
        p = chains.Product(cs)
        seen = set()
        for index in range(p.size):
            path, length = p.path(index)
            previous = None
            for h in range(length):
                state = p.state(index, h)
                must(state not in seen and p.address(state) == (index, h), 'product bijection')
                if previous is not None:
                    must(all(x & ~y == 0 for x, y in zip(previous, state)), 'red monotonicity')
                    must(sum((x^y).bit_count() for x, y in zip(previous, state)) == 1, 'saturation')
                seen.add(state)
                previous = state
        domains = [range(15) if c else range(1, 16) for c in cs]
        must(seen == set(product(*domains)), 'entire star-product coverage')
        partitions += 1
        states_checked += len(seen)
    results = counts.calculate()
    # Complete small physical class: all eight graphs on the three core vertices.
    # All chain obligations and all original star states are checked literally.
    class_states, class_chains = 0, 0
    statuses = Counter()
    for core in range(8):
        es = receiver.edges(7)
        lookup = {e: k for k, e in enumerate(es)}
        fixed = sum(1 << lookup[e] for e in combinations(range(4), 2))
        fixed |= sum((core >> j & 1) << lookup[e] for j, e in enumerate(combinations(range(4, 7), 2)))
        frame = receiver.Frame(7, 1, 1, format(fixed, 'x'))
        for index in range(frame.product.size):
            pkt = frame.decide(index)
            verdict, _, _ = check.check(pkt)
            statuses[verdict['status']] += 1
            _, _, pairs, ids, states, _ = check.expand(pkt)
            good_positions = [h for h, word in enumerate(states)
                if all(len({word >> ids[e] & 1 for e in combinations(s, 2)}) == 2
                       for s in combinations(range(7), 5))]
            must(bool(good_positions) == (pkt['status'] == 'GOOD_GRAPH'), 'complete physical decision')
            class_states += len(states)
            class_chains += 1
    must(class_states == 8*15**3, 'whole small physical class cardinality')
    fixtures = {}
    proof_runs = []
    for name in ('INTERIOR', 'FULL43', 'CORE4', 'POSITIVE42'):
        raw = json.loads((HERE/(name+'.json')).read_text())
        pkt = raw['packet'] if name == 'POSITIVE42' else raw
        verdict, cnf, drat = check.check(pkt)
        generated = receiver.Frame(**pkt['frame']).decide(pkt['chain_index'])
        must(generated == pkt, 'deterministic fixture receiver')
        fixtures[name] = verdict
        if cnf is not None and drat_trim:
            with tempfile.TemporaryDirectory(prefix='r55-chain-') as tmp:
                f, d = Path(tmp)/'chain.cnf', Path(tmp)/'chain.drat'
                f.write_text(cnf)
                d.write_text(drat)
                run = subprocess.run([drat_trim, str(f), str(d), '-U'], capture_output=True, text=True)
                must(('s VERIFIED' in run.stdout) and (run.returncode == 0 or
                     (run.returncode == 1 and 'c trivial UNSAT' in run.stdout)), 'external DRAT replay')
                proof_runs.append(dict(fixture=name, cnf_sha256=hashlib.sha256(cnf.encode()).hexdigest(),
                                       drat_sha256=hashlib.sha256(drat.encode()).hexdigest(),
                                       status='VERIFIED_RUP_ONLY'))
    packet = json.loads((HERE/'INTERIOR.json').read_text())
    mutations = []
    bad = copy.deepcopy(packet); bad['blue'] = [0, 1, 2, 3, 4]; mutations.append(bad)
    bad = copy.deepcopy(packet); bad['red'] = [4, 5, 6, 7, 8]; mutations.append(bad)
    bad = copy.deepcopy(packet); bad['cut'] = 0; mutations.append(bad)
    bad = copy.deepcopy(packet); bad['chain_index'] += 1; mutations.append(bad)
    bad = copy.deepcopy(packet); bad['path'][0] = [6, 0]; mutations.append(bad)
    bad = copy.deepcopy(packet); bad['length'] += 1; mutations.append(bad)
    bad = copy.deepcopy(packet); bad['red'] = [0, 1, 2, 3]; mutations.append(bad)
    must(all(rejected(x) for x in mutations), 'false certificate accepted')
    bridge_rows = []
    physical_rows = []
    rejected_scopes = 0
    active_M8_controls = []
    if cache_dir:
        import bridge
        for q in range(7, 11):
            for r in range(5, q+1):
                task = bridge.OriginalTask(f'bo1-q{q}-r{r}-c000000', cache_dir)
                row = next(x for x in results['original_macros'] if (x['q'], x['r']) == (q, r))
                must(task.size == row['new_per_task'], 'exact old/new indexing bridge')
                for old_index in (0, task.old.size//2, task.old.size-1):
                    graph = task.old.unrank(old_index)
                    new_index, position = task.address_old(graph)
                    fi, ci = divmod(new_index, task.chains_per_frame)
                    frame = task.frame(fi)
                    must(frame.graph(ci, position) == int(graph['red_hex'], 16), '903-bit roundtrip')
                wrapper = task.decide(0)
                packet = wrapper['packet']
                verdict, _, _ = task.check(wrapper)
                bad = copy.deepcopy(wrapper); bad['task_chain_code'] += 1
                try:
                    task.check(bad)
                except ValueError:
                    rejected_scopes += 1
                else:
                    raise ValueError('wrong original-task chain accepted')
                if q == 8:
                    f = packet['frame']; word = int(f['fixed_hex'], 16)
                    pair_ids = {e: k for k, e in enumerate(receiver.edges(43))}
                    full_core = [(1 if word >> pair_ids[e] & 1 else -1)*(802+j)
                                 for j, e in enumerate(combinations(range(32, 43), 2))]
                    for size in (7, 8, 55):
                        must(bridge.physical_guard(packet, full_core[:size]), 'physical guard')
                    wrong = full_core[:7]; wrong[0] *= -1
                    try:
                        bridge.physical_guard(packet, wrong)
                    except ValueError:
                        pass
                    else:
                        raise ValueError('wrong core guard accepted')
                bridge_rows.append(dict(q=q, r=r, original_graph_roundtrips=3,
                                        verdict=verdict['status'], chain_obligations=task.size))
        for r in range(5, 9):
            for g in (7, 8):
                guard = [(1 if i % 2 else -1)*(802+i) for i in range(g)]
                cohort = bridge.PhysicalCohort(r, guard)
                row = next(x for x in results['physical_q8_rows']
                           if x['r'] == r and x['guard_size'] == g)
                must(cohort.size == row['new_per_cohort'], 'complete physical index size')
                signatures = []
                for code in (0, cohort.size//2, cohort.size-1):
                    wrapper = cohort.decide(code)
                    pkt = wrapper['packet']
                    must(bridge.physical_guard(pkt, guard), 'full physical decoder guard')
                    verdict, _, _ = cohort.check(wrapper)
                    bad = copy.deepcopy(wrapper); bad['guard'][0] *= -1
                    try:
                        cohort.check(bad)
                    except ValueError:
                        rejected_scopes += 1
                    else:
                        raise ValueError('wrong physical cohort identity accepted')
                    signatures.append(dict(code=code, frame_sha256=hashlib.sha256(
                        json.dumps(pkt['frame'], sort_keys=True).encode()).hexdigest(),
                        status=verdict['status']))
                physical_rows.append(dict(r=r, guard_size=g, size=cohort.size, controls=signatures))
        for g in (7, 8):
            guard = [802+i for i in range(g)]
            cohort = bridge.PhysicalCohort(8, guard, require_edge119=True)
            must(cohort.block_frames == results['active_M8_positive_edge119']['retained_fixed_frames'],
                 'active M8 frame count')
            for code in (0, cohort.size//2, cohort.size-1):
                wrapper = cohort.decide(code)
                verdict, _, _ = cohort.check(wrapper)
                active_M8_controls.append(dict(guard_size=g, code=code,
                    status=verdict['status'], positive_edge119=True))
    return dict(rectangle_points=rectangles, complete_product_patterns=partitions,
                complete_product_states=states_checked,
                complete_small_physical_class=dict(core_graphs=8, original_states=class_states,
                    chains=class_chains, outcomes=dict(statuses)),
                fixtures=fixtures, rejected_corruptions=len(mutations),
                exact_q_ratios=[dict(q=x['q'], display=x['ratio_display'],
                    proven_strict_gain=x['strict_integer_gain']) for x in results['levels']],
                original_complete_tasks=results['original_tasks'], physical_cohorts=956,
                target_solver_invocations=0, original_task_retirements=0,
                bridge_controls=bridge_rows, physical_adapter_controls=physical_rows,
                rejected_obligation_scopes=rejected_scopes,
                active_M8_controls=active_M8_controls,
                external_rup_replays=proof_runs)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--catalog')
    p.add_argument('--drat-trim')
    p.add_argument('--counts', action='store_true')
    a = p.parse_args()
    print(json.dumps(counts.calculate() if a.counts else controls(a.catalog, a.drat_trim),
                     indent=2, sort_keys=True))
