"""Reproduce twelve additional depth-free nine-wire size12 exclusions.

Author/executing agent: six-sorting-2, researcher. Generated certificates
stay in the ignored output directory; solver UNSAT alone is not the proof.
"""
import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import resource
import threading
import time

for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[name] = '1'
import pysat
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
from audit_data import audit_data, check_model, check_dependencies

HERE = Path(__file__).resolve().parent
P = HERE.parent
DAG = P / 'sorting13_B11_ten_event_matching_dags'
ACTIVITY = P / 'sorting13_B11_pruning_saturation_activity'
PAIRS = tuple(itertools.combinations(range(9), 2))
SIZES = (0,0,1,3,5,9,12,16,19,25,29,35,39)


def record(image_id):
    check_dependencies()
    selected = json.loads((HERE / 'certificate.json').read_text())['records']
    expected = next(r for r in selected if r['image_id'] == image_id)
    cert = json.loads((P / 'sorting13_B11_ten_event_loop_postponement/certificate.json').read_text())
    item = next(r for r in cert['classes'] if r['code'] == expected['code'])
    assert item['obstruction'] is None and item['image_id'] == image_id
    image = cert['images9'][item['image_id']]
    assert len(image) == expected['rows']
    return dict(code=item['code'], partner=item['partner'], kind=item['kind'],
                canonical_events=item['events'], image9=image, image9_rows=len(image))

def scalar(row, word):
    for a, b in word:
        if row >> a & 1 and not row >> b & 1:
            row ^= (1 << a) | (1 << b)
    return row


def sorted9(row):
    return ((1 << row.bit_count()) - 1) << (9 - row.bit_count())


def normalize(word):
    word = list(map(tuple, word))
    while True:
        change = False
        for i in range(len(word) - 1):
            if word[i] > word[i + 1] and set(word[i]).isdisjoint(word[i + 1]):
                word[i], word[i + 1] = word[i + 1], word[i]
                change = True
        if not change:
            return word


def data(record, budget):
    fixture = json.loads((DAG / 'fixture.json').read_text())
    events = list(map(tuple, record['canonical_events']))
    prefix = fixture['prefix22'] + [(a + 1, b + 1) for a, b in events]
    assert len(prefix) == 32
    caps = {}
    for original in range(1, 8191):
        row = original
        charges = [0, 0]
        for a, b in prefix:
            A, B = row >> a & 1, row >> b & 1
            charges[0] += not (A and B)
            charges[1] += bool(A or B)
            if A and not B:
                row ^= (1 << a) | (1 << b)
        projected = row >> 2 & 511
        for mode, k in ((0, 13 - original.bit_count()), (1, original.bit_count())):
            cap = 32 + budget - SIZES[13 - k] - charges[mode]
            key = projected, mode
            caps[key] = min(cap, caps.get(key, 32 + budget))
    domains = []
    for family in json.loads((ACTIVITY / 'certificate.json').read_text())['families']:
        if family['final_D'] != 9:
            continue
        for domain, original in zip(family['domains'], family['original_representatives']):
            image = sorted({scalar(row, events) >> 1 & 511 for row in domain})
            assert set(image) <= set(record['image9'])
            domains.append(dict(mode=family['mode'], partner=family['partner'],
                                original=original, image9=image))
    assert len(domains) == 12
    return prefix, caps, domains


class Encoding:
    def __init__(self, record, budget, path, activity=True):
        self.record, self.budget, self.path = record, budget, path
        self.top = self.count = 0
        self.rows, self.swaps = {}, {}
        self.body = path.with_suffix('.body').open('w')
        self.solver = Solver(name='g4', with_proof=True)
        self.choice = [[self.new() for _ in PAIRS] for _ in range(budget)]
        self.used = [[self.new() for _ in range(9)] for _ in range(budget)]
        self.sections = {}
        for t in range(budget):
            self.card(self.choice[t], 1, True)
            for i in range(9):
                choices = [self.choice[t][j] for j, gate in enumerate(PAIRS) if i in gate]
                for c in choices:
                    self.add([-c, self.used[t][i]])
                self.add([-self.used[t][i]] + choices)
        self.sections['gate_choices'] = self.count
        start = self.count
        for row in record['image9']:
            if row == sorted9(row):
                continue
            bits = [[self.new() for _ in range(9)] for _ in range(budget + 1)]
            swaps = [self.new() for _ in range(budget)]
            self.rows[row], self.swaps[row] = bits, swaps
            for i in range(9):
                self.add([bits[0][i] if row >> i & 1 else -bits[0][i]])
                self.add([bits[-1][i] if sorted9(row) >> i & 1 else -bits[-1][i]])
            for t in range(budget):
                s = swaps[t]
                for j, (a, b) in enumerate(PAIRS):
                    c, x, z = self.choice[t][j], bits[t][a], bits[t][b]
                    self.add([-c, -s, x])
                    self.add([-c, -s, -z])
                    self.add([-c, -x, z, s])
                for i in range(9):
                    u, x, y = self.used[t][i], bits[t][i], bits[t + 1][i]
                    for clause in ([u, -x, y], [u, x, -y], [s, -x, y], [s, x, -y],
                                   [-u, -s, x, y], [-u, -s, -x, -y]):
                        self.add(clause)
        self.sections['Boolean_shared_swaps'] = self.count - start
        self.prefix, self.caps, self.domains = data(record, budget)
        self.hit_flags = []
        start = self.count
        for (row, mode), cap in sorted(self.caps.items()):
            if cap >= budget:
                continue
            flags = [self.new() for _ in range(budget)]
            self.hit_flags.append([row, mode, cap, flags])
            for t in range(budget):
                for i in range(9):
                    mark = self.rows[row][t][i] if row in self.rows else bool(row >> i & 1)
                    if not mode:
                        mark = not mark if isinstance(mark, bool) else -mark
                    unmarked = not mark if isinstance(mark, bool) else -mark
                    self.add([-self.used[t][i], unmarked, flags[t]])
            self.card(flags, cap)
        self.sections['one_sided_pruning'] = self.count - start
        start = self.count
        if activity:
            assert budget == 12
            for domain in self.domains:
                for t in range(budget):
                    self.add([self.swaps[row][t] for row in domain['image9'] if row in self.swaps])
        self.sections['saturated_slice_activity'] = self.count - start
        start = self.count
        for t in range(budget - 1):
            for j, a in enumerate(PAIRS):
                for k, b in enumerate(PAIRS[:j]):
                    if set(a).isdisjoint(b):
                        self.add([-self.choice[t][j], -self.choice[t + 1][k]])
        self.sections['adjacent_disjoint_normalization'] = self.count - start
        self.body.close()
        with path.open('w') as stream:
            stream.write(f'p cnf {self.top} {self.count}\n')
            with path.with_suffix('.body').open() as body:
                for line in body:
                    stream.write(line)
        self.metadata = dict(record=record, budget=budget, variables=self.top, clauses=self.count,
                             choices=self.choice, used=self.used, rows=self.rows, swaps=self.swaps,
                             prefix=self.prefix, caps=[[r, p, c] for (r, p), c in sorted(self.caps.items())],
                             hit_flags=self.hit_flags, domains=self.domains, activity=activity,
                             sections=self.sections, cnf_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        path.with_suffix('.metadata.json').write_text(json.dumps(self.metadata, separators=(',', ':')) + '\n')

    def new(self):
        self.top += 1
        return self.top

    def add(self, clause):
        if any(x is True for x in clause):
            return
        clause = [x for x in clause if x is not False]
        self.solver.add_clause(clause)
        self.body.write(' '.join(map(str, clause)) + ' 0\n')
        self.count += 1

    def card(self, flags, cap, exact=False):
        if cap < 0:
            self.add([])
            return
        if not exact and cap >= len(flags):
            return
        routine = CardEnc.equals if exact else CardEnc.atmost
        cnf = routine(lits=flags, bound=cap, top_id=self.top, encoding=EncType.seqcounter)
        self.top = max(self.top, cnf.nv)
        for clause in cnf.clauses:
            self.add(clause)

    def fixed(self, word):
        return [self.choice[t][PAIRS.index(tuple(gate))] for t, gate in enumerate(word)]

    def limited(self, seconds, conflicts=None, assumptions=()):
        if conflicts is not None:
            self.solver.conf_budget(conflicts)
        timer = threading.Timer(seconds, self.solver.interrupt)
        timer.daemon = True
        timer.start()
        start = time.monotonic()
        try:
            return self.solver.solve_limited(assumptions=list(assumptions), expect_interrupt=True), time.monotonic() - start
        finally:
            timer.cancel()
            timer.join()
            self.solver.clear_interrupt()


def add_suffix(enc):
    old_count = enc.count
    enc.body = enc.path.with_suffix('.body').open('a')
    boundary = [[enc.new() for _ in range(8)] for _ in range(enc.budget + 1)]
    for flag in boundary[-1]:
        enc.add([-flag])
    for t in range(enc.budget - 1, -1, -1):
        for i in range(8):
            choices = [enc.choice[t][j] for j, (a, b) in enumerate(PAIRS) if a <= i < b]
            current, following = boundary[t][i], boundary[t + 1][i]
            enc.add([-current, following] + choices)
            enc.add([current, -following])
            for choice in choices:
                enc.add([current, -choice])
        for j, (a, b) in enumerate(PAIRS):
            for i, k in itertools.combinations(range(a, b), 2):
                enc.add([-enc.choice[t][j], boundary[t + 1][i], boundary[t + 1][k]])
    enc.body.close()
    with enc.path.open('w') as target:
        target.write(f'p cnf {enc.top} {enc.count}\n')
        with enc.path.with_suffix('.body').open() as source:
            for line in source:
                target.write(line)
    enc.sections['attributed_suffix_interval_components'] = enc.count - old_count
    enc.metadata.update(boundary=boundary, variables=enc.top, clauses=enc.count,
                        sections=enc.sections,
                        suffix_source='https://arxiv.org/abs/1411.6408 Theorem11',
                        cnf_sha256=hashlib.sha256(enc.path.read_bytes()).hexdigest())
    enc.path.with_suffix('.metadata.json').write_text(json.dumps(enc.metadata, separators=(',', ':')) + '\n')


def main():
    assert __debug__, 'Assertions are required'
    assert pysat.__version__ == '1.8.dev24', 'Use the pinned PySAT version'
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=HERE / 'generated')
    parser.add_argument('--image', type=int, help='One listed parent image; omit to generate all twelve')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    expected_records = json.loads((HERE / 'certificate.json').read_text())['records']
    selected = [r for r in expected_records if args.image is None or r['image_id'] == args.image]
    assert selected, 'Image is not one of the twelve certified instances'
    started = time.monotonic()
    instance = record(selected[0]['image_id'])
    # A genuine full-input positive control for the Boolean/pruning kernel.
    word = normalize([(j - 1,j) for i in range(1,9) for j in range(i,0,-1)])
    positive = Encoding(instance,36,args.output / 'positive36.cnf',activity=False)
    add_suffix(positive)
    audit_data(positive.metadata)
    answer, seconds = positive.limited(15,assumptions=positive.fixed(word))
    assert answer is True, ('positive control incomplete or failed',answer)
    control = check_model(positive.metadata,word,positive.solver.get_model(),positive.path)
    positive.solver.delete()
    results = []
    for expected in selected:
        instance = record(expected['image_id'])
        target = Encoding(instance,12,args.output / f"case{expected['image_id']:03d}.cnf")
        add_suffix(target)
        data_check = audit_data(target.metadata)
        assert target.metadata['cnf_sha256'] == expected['cnf_sha256']
        assert (target.top,target.count) == (expected['variables'],expected['clauses'])
        answer, seconds = target.limited(40,30000)
        if answer is not False:
            target.solver.delete()
            raise RuntimeError(f'No exclusion established by this run: solver returned {answer!r}')
        proofpath = target.path.with_suffix('.drat')
        proofpath.write_text('\n'.join(target.solver.get_proof()) + '\n')
        proof_hash = hashlib.sha256(proofpath.read_bytes()).hexdigest()
        assert proof_hash == expected['raw_drat_sha256'], 'Unexpected trace: do not claim the pinned certificate reproduced'
        stats = target.solver.accum_stats()
        target.solver.delete()
        result = dict(agent='six-sorting-2',role='researcher',image_id=expected['image_id'],
                      status='UNSAT_CERTIFICATE_GENERATED_NOT_YET_INDEPENDENTLY_REPLAYED',
                      cnf_sha256=expected['cnf_sha256'], raw_drat_sha256=proof_hash,
                      independent_prefix_data=data_check,solve_seconds=seconds,stats=stats)
        results.append(result)
        print(json.dumps(result),flush=True)
    output = dict(agent='six-sorting-2',role='researcher',positive_control=control,results=results,
                  total_seconds=time.monotonic()-started,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (args.output / 'generation.json').write_text(json.dumps(output,indent=2)+'\n')


if __name__ == '__main__':
    main()
