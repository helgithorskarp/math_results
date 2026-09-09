"""A complete q8,r8 negative-branch verdict using RUP plus R(4,5)<=25.

This is deliberately not an LRAT refutation: the final step imports the
published Ramsey theorem. It never closes an original fixed-core task.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / 'ramsey_r55_q8_assumption_queue'
sys.path.insert(0, str(PARENT))
import certificate as parent_certificate
import worker

R = 8
NC = 1502521
NV = 946
BASE_SHA = 'ba96586572a831dbc6a12329515cad3d11779a1ea01b3242e981a2c1f539c2d1'
PREMISE = dict(red_clique=5, blue_clique=4, order=25,
               source='https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf',
               citation='B. D. McKay and S. P. Radziszowski, R(4,5)=25, Journal of Graph Theory 19 (1995), 309-322')


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''):
            h.update(b)
    return h.hexdigest()


def physical_map():
    # Independent physical reconstruction, not the parent variable dictionary.
    result = {}
    next_variable = 2
    for u in range(43):
        for v in range(u+1, 43):
            if u < 32 and u//4 == v//4:
                continue
            result[u, v] = next_variable
            next_variable += 1
    if next_variable != 857:
        raise ValueError('Physical variable count')
    return result


def load_base(directory):
    check_parent()
    path = Path(directory)/'q8-r8.cnf'
    h = hashlib.sha256()
    selected = {}
    count = 0
    with path.open('rb') as f:
        header = f.readline()
        h.update(header)
        if header != f'p cnf {NV} {NC}\n'.encode():
            raise ValueError('Complete M8 header')
        for count, raw in enumerate(f, 1):
            h.update(raw)
            if count <= 2521 or count > NC-546:
                a = [int(x) for x in raw.split()]
                if not a or a[-1] or any(not x or abs(x)>NV for x in a[:-1]):
                    raise ValueError('Strict selected clause')
                selected[count] = a[:-1]
    if count != NC or h.hexdigest() != BASE_SHA:
        raise ValueError('Exact full physical M8 identity')
    return selected


def check_parent():
    dep = json.loads((HERE/'DEPENDENCIES.json').read_text())
    manifest = PARENT/'SHA256SUMS'
    if sha(manifest) != dep['parent_manifest_sha256']:
        raise ValueError('Pinned parent source manifest')
    for line in manifest.read_text().splitlines():
        digest, name = line.split('  ',1)
        if sha(PARENT/name) != digest:
            raise ValueError('Pinned parent source bytes: '+name)


def produce(directory):
    db = load_base(directory)
    edge = physical_map()
    unit = edge[3, 4]
    if unit != 119:
        raise ValueError('Physical branch identity')
    original = dict(db)
    db[NC+1] = [-unit]
    proof = []

    def add(c, hints):
        c = sorted(c)
        if not parent_certificate.rup(c, hints, db, NV):
            raise ValueError('Producer inference failed')
        i = NC+2+len(proof)
        proof.append(dict(clause=c, hints=hints))
        db[i] = c
        return i

    # Resolve six lower signature bits. The remaining binary implication says
    # that a later column cannot have top bit 1 when the preceding one has 0.
    for col in range(3):
        lookup = {tuple(sorted(c)): i for i,c in original.items()
                  if 2+120*col <= i <= 1+120*(col+1)}
        fixed = {edge[3, 4+col]: False, edge[3, 5+col]: True}
        lower = [edge[u, v] for v in (4+col, 5+col) for u in range(3)]
        def resolve(k, assignment):
            clause = sorted(v if not value else -v for v,value in assignment.items())
            if k == len(lower):
                return lookup[tuple(clause)]
            x = lower[k]
            a = dict(assignment); a[x] = False
            left = resolve(k+1, a)
            a[x] = True
            right = resolve(k+1, a)
            return add(clause, [left, right])
        resolve(0, fixed)

    # Record every unit-propagation inference as a separately checked RUP step.
    units = {1: (True, 1), unit: (False, NC+1)}
    stable = list(db.items())
    changed = True
    while changed:
        changed = False
        for i,c in stable:
            if any(abs(x) in units and units[abs(x)][0] == (x>0) for x in c):
                continue
            free = [x for x in c if abs(x) not in units]
            if not free:
                raise ValueError('Unexpected propositional contradiction; inspect proof')
            if len(free) == 1:
                lit = free[0]
                hints = [units[abs(x)][1] for x in c if abs(x) in units]+[i]
                j = add([lit], hints)
                units[abs(lit)] = (lit>0, j)
                changed = True
    needed = [-edge[3, v] for v in range(4, 32)]
    if any(units.get(-x, (True,))[0] for x in needed):
        raise ValueError('Ordering did not force all 28 blue neighbors')
    result = dict(format='q8-r8-rup-ramsey-branch-v1', r=8,
                  base_sha256=BASE_SHA, assumptions=[-119], proof=proof,
                  vertex=3, blue_neighbors=list(range(4,32)),
                  ramsey_subset=list(range(4,29)), premise=PREMISE,
                  conclusion='UNSAT_NEGATIVE_PHYSICAL_BRANCH', implied_unit=119)
    verify_loaded(original, result)
    return result


def verify_loaded(base, cert):
    expected = {'format','r','base_sha256','assumptions','proof','vertex',
                'blue_neighbors','ramsey_subset','premise','conclusion','implied_unit'}
    if not isinstance(cert, dict) or set(cert) != expected:
        raise ValueError('Branch theorem schema')
    if (cert['format'] != 'q8-r8-rup-ramsey-branch-v1' or type(cert['r']) is not int
        or cert['r'] != 8 or cert['base_sha256'] != BASE_SHA
        or cert['assumptions'] != [-119] or cert['vertex'] != 3
        or cert['blue_neighbors'] != list(range(4,32))
        or cert['ramsey_subset'] != list(range(4,29)) or cert['premise'] != PREMISE
        or cert['conclusion'] != 'UNSAT_NEGATIVE_PHYSICAL_BRANCH'
        or type(cert['implied_unit']) is not int or cert['implied_unit'] != 119):
        raise ValueError('Changed physical scope or imported theorem')
    proof = cert['proof']
    if not isinstance(proof, list) or not proof:
        raise ValueError('Normalization proof required')
    parent_certificate.verify_steps(base, NC, NV, [-119], proof, proof[-1]['clause'])
    established = set(cert['assumptions'])
    established.update(c['clause'][0] for c in proof if len(c['clause']) == 1)
    edge = physical_map()
    if not all(-edge[3, v] in established for v in cert['blue_neighbors']):
        raise ValueError('Unproved blue neighborhood')
    # M8 forbids both colors of K5. R(5,4)<=25 on this blue neighborhood
    # forces a red K5, or a blue K4 which extends by vertex 3 to a blue K5.
    return dict(status='CERTIFIED_UNSAT_USING_IMPORTED_RAMSEY_THEOREM',
                family='M8 AND -119', normalization_rup_steps=len(proof),
                blue_neighbors=28, ramsey_vertices=25, implied_unit=119,
                original_task_exclusions=0, candidates=0,
                trust='Published M8 encoding and R(4,5)<=25; not a full LRAT refutation')


def verify(directory, cert):
    return verify_loaded(load_base(directory), cert)


class Dispatcher:
    """A verified session routes actual full physical workers, not residuals."""
    def __init__(self, directory, cert):
        self.directory = Path(directory)
        self.receipt = verify(self.directory, cert)
        self.closed = 0
        self.materialized = 0

    def dispatch(self, job, output):
        worker.checked_job(job)
        if job['r'] != 8 or job['edge_cube'] not in ([119], [-119]):
            raise ValueError('Only the two certified q8,r8 physical siblings')
        if job['edge_cube'] == [-119]:
            self.closed += 1
            return dict(status='CERTIFIED_UNSAT_USING_IMPORTED_RAMSEY_THEOREM',
                        job=job, materialized=False, original_task_status='UNKNOWN')
        receipt = worker.materialize(self.directory, job, output)
        self.materialized += 1
        return dict(status='READY_FULL_PHYSICAL_WORKER', **receipt,
                    original_task_status='UNKNOWN', materialized=True)


def request(directory, cert, stream, name):
    import task_queue
    r,c = task_queue.parameters(name)
    if r != 8:
        raise ValueError('This active stream owns only original q8,r8 tasks')
    theorem = verify(directory, cert)
    result = task_queue.request(name, directory)
    if sha(stream) != '2a8d4e12f1c358a5cc63fcf2286f1cd7344f50f1bfdbccb18523a557fcc64cf6':
        raise ValueError('Verified complete physical dispatch stream')
    with Path(stream).open('rb') as f:
        if f.read(12) != b'Q8UNIT1\n'+struct.pack('<I',546356):
            raise ValueError('Dispatch stream framing')
        f.seek(12+14*c)
        index, word, unit = struct.unpack('<IQh',f.read(14))
    if index != c or unit != 119 or task_queue.assumptions(word) != result['assumptions']:
        raise ValueError('Dispatched original task identity')
    return dict(original_task=name, status='UNKNOWN',
                worker_job=dict(r=8, core_assumptions=result['assumptions'], edge_cube=[119]),
                base_sha256=BASE_SHA, certified_negative_sibling=theorem,
                target_solver_calls=0)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('command', choices=['produce','verify','request'])
    p.add_argument('directory'); p.add_argument('certificate')
    p.add_argument('--task'); p.add_argument('--stream')
    a = p.parse_args()
    if a.command == 'produce':
        c = produce(a.directory)
        with Path(a.certificate).open('x') as f:
            f.write(json.dumps(c, separators=(',', ':'))+'\n')
    else:
        c = json.loads(Path(a.certificate).read_text())
    if a.command == 'request':
        if not a.task or not a.stream:
            p.error('request requires --task and --stream')
        result = request(a.directory,c,a.stream,a.task)
    else:
        result = verify(a.directory,c)
    print(json.dumps(result, indent=2))
