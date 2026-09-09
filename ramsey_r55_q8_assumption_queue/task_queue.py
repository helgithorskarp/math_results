"""Exact q8 queue transport. A task stays UNKNOWN until a checked certificate."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import time

HERE = Path(__file__).resolve().parent
COUNT = 546356
CORE_MAGIC = b'Q8CORE1\n'
JOB_MAGIC = b'Q8JOB1\n\0'
JOB = struct.Struct('<BIQ')


def specs():
    return json.loads((HERE/'DEPENDENCIES.json').read_text())['catalog']


def catalog_words(path):
    raw = Path(path).read_bytes()
    s = specs()
    if len(raw) != s['bytes'] or hashlib.sha256(raw).hexdigest() != s['sha256']:
        raise ValueError('Pinned q8 catalog mismatch')
    words = []
    pairs = [(i, j) for j in range(1, 11) for i in range(j)]
    lex = {(i, j): k for k, (i, j) in enumerate((i, j) for i in range(11) for j in range(i+1, 11))}
    for line in raw.splitlines():
        if len(line) != 11 or line[0] != 74 or any(not 63 <= b <= 126 for b in line):
            raise ValueError('graph6 syntax')
        data = line[1:]
        if (data[-1]-63) & 31:
            raise ValueError('graph6 padding')
        word = sum((((data[k//6]-63) >> (5-k%6)) & 1) << lex[e] for k, e in enumerate(pairs))
        words.append(word)
    if len(words) != COUNT or len(set(words)) != COUNT:
        raise ValueError('Catalog count or literal uniqueness')
    return words


def read_words(path):
    raw = Path(path).read_bytes()
    if raw[:8] != CORE_MAGIC or len(raw) != 12+8*COUNT or struct.unpack_from('<I', raw, 8)[0] != COUNT:
        raise ValueError('Core stream framing')
    words = [v[0] for v in struct.iter_unpack('<Q', raw[12:])]
    if any(v >= 1 << 55 for v in words) or len(set(words)) != COUNT:
        raise ValueError('Core stream values')
    return words


def parameters(name):
    m = re.fullmatch(r'bo1-q8-r([5-8])-c([0-9]{6})', name)
    if not m or int(m[2]) >= COUNT:
        raise ValueError('Only canonical, in-range q8 task IDs are admitted')
    return int(m[1]), int(m[2])


def assumptions(word):
    if type(word) is not int or not 0 <= word < 1 << 55:
        raise ValueError('55-bit core word')
    return [(802+k)*(1 if word >> k & 1 else -1) for k in range(55)]


def match_mask(a):
    if not isinstance(a, list) or any(type(x) is not int or not 802 <= abs(x) < 857 for x in a):
        raise ValueError('A cover certificate may assume only physical core edges')
    if len({abs(x) for x in a}) != len(a):
        raise ValueError('Duplicate or contradictory assumption')
    mask = sum(1 << (abs(x)-802) for x in a)
    value = sum(1 << (x-802) for x in a if x > 0)
    return mask, value


def matching(words, a):
    mask, value = match_mask(a)
    return [c for c, word in enumerate(words) if word & mask == value]


def prepare(catalog, output):
    start = time.monotonic()
    output = Path(output)
    words = catalog_words(catalog)
    with (output/'cores.u64le').open('xb') as f:
        f.write(CORE_MAGIC+struct.pack('<I', COUNT))
        for word in words:
            f.write(struct.pack('<Q', word))
    digest = hashlib.sha256()
    with (output/'queue.records').open('xb') as f:
        f.write(JOB_MAGIC+struct.pack('<I', 4*COUNT))
        for r in range(5, 9):
            for c, word in enumerate(words):
                f.write(JOB.pack(r, c, word))
                digest.update(f'bo1-q8-r{r}-c{c:06d} {word:014x}\n'.encode())
    return dict(tasks=4*COUNT, classes=4, core_records=COUNT, assumption_literals=4*COUNT*55,
                dispatch_identity_sha256=digest.hexdigest(),
                files={p.name: dict(bytes=p.stat().st_size, sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                       for p in [output/'cores.u64le', output/'queue.records']},
                preparation_seconds=time.monotonic()-start, initial_status='UNKNOWN',
                target_solver_calls=0, new_task_exclusions=0, candidates=0)


def request(name, directory, certificate_path=None):
    r, c = parameters(name)
    d = Path(directory)
    expected = json.loads((HERE/'EXPECTED.json').read_text())
    meta = expected['bases'][str(r)]
    digest = hashlib.sha256()
    with (d/f'q8-r{r}.cnf').open('rb') as f:
        for chunk in iter(lambda: f.read(1048576), b''):
            digest.update(chunk)
    if digest.hexdigest() != meta['sha256']:
        raise ValueError('Audited base identity')
    core_path = d/'cores.u64le'
    if hashlib.sha256(core_path.read_bytes()).hexdigest() != expected['queue']['files']['cores.u64le']['sha256']:
        raise ValueError('Audited core queue identity')
    words = read_words(core_path)
    result = dict(task=name, r=r, core=c, base=f'q8-r{r}.cnf', base_sha256=meta['sha256'],
                  variables=meta['variables'], assumptions=assumptions(words[c]), status='UNKNOWN')
    if certificate_path:
        import certificate
        cert = json.loads(Path(certificate_path).read_text())
        if cert.get('r') != r:
            raise ValueError('Certificate belongs to another base')
        receipt = certificate.verify_cover(d, cert)
        mask, value = match_mask(cert['assumptions'])
        result['checked_cover'] = receipt
        if words[c] & mask == value:
            result['status'] = 'CERTIFIED_UNSAT'
            result['assumptions'] = None  # No target solve is dispatched for a closed task.
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest='command', required=True)
    a = sub.add_parser('prepare'); a.add_argument('catalog'); a.add_argument('output')
    a = sub.add_parser('request'); a.add_argument('task'); a.add_argument('directory'); a.add_argument('--certificate')
    a = p.parse_args()
    result = prepare(a.catalog, a.output) if a.command == 'prepare' else request(a.task, a.directory, a.certificate)
    print(json.dumps(result, indent=2))
