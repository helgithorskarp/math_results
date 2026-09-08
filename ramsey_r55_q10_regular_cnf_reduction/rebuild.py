#!/usr/bin/env python3
"""Reproduce the historical files exactly. No solver is imported or invoked."""
import argparse
import hashlib
import json
from pathlib import Path
import frozen_encoder

ROOT = Path(__file__).resolve().parent


def verify_package(repository, row):
    directory = repository / row['directory']
    raw = (directory / 'SHA256SUMS').read_bytes()
    if hashlib.sha256(raw).hexdigest() != row['manifest_sha256']:
        raise ValueError('dependency manifest: ' + row['directory'])
    for line in raw.decode().splitlines():
        digest, name = line.split('  ', 1)
        if hashlib.sha256((directory / name).read_bytes()).hexdigest() != digest:
            raise ValueError('dependency entry: ' + row['directory'] + '/' + name)
    return directory


def rebuild(output):
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise ValueError('rebuild output must be empty')
    inputs = json.loads((ROOT / 'INPUTS.json').read_text())
    for row in json.loads((ROOT / 'DEPENDENCIES.json').read_text()):
        verify_package(ROOT.parent, row)
    if hashlib.sha256((ROOT/'frozen_encoder.py').read_bytes()).hexdigest() != json.loads((ROOT/'PROVENANCE.json').read_text())['frozen_encoder_sha256']:
        raise ValueError('changed historical encoder')
    cache = output / 'cache'
    cache.mkdir()
    (cache / 'r44_3.g6').write_bytes((ROOT / 'r44_3.g6').read_bytes())
    built = frozen_encoder.build(ROOT.parent, cache)
    *parts, meta = built
    base = output / 'base.cnf'
    count = 0
    digest = hashlib.sha256()
    with base.open('xb') as stream:
        header = f'p cnf {meta["variables"]} {meta["clauses"]}\n'.encode()
        stream.write(header); digest.update(header)
        for clause in frozen_encoder.clauses(*parts):
            line = (' '.join(map(str, clause)) + ' 0\n').encode()
            stream.write(line); digest.update(line); count += 1
    expected_base = inputs['base']
    if count != expected_base['clauses'] or base.stat().st_size != expected_base['bytes'] or digest.hexdigest() != expected_base['sha256']:
        raise ValueError('historical base reproduction mismatch')
    result = []
    for row in inputs['rows']:
        suffix = frozen_encoder.exact_degree_units(parts[0], parts[4]['variables'],
                                                   row['red_degree'], row['blue_degree'])
        digest = hashlib.sha256()
        with (output / row['filename']).open('xb') as stream:
            header = f'p cnf {row["variables"]} {count + len(suffix)}\n'.encode()
            stream.write(header); digest.update(header)
            with base.open('rb') as source:
                source.readline()
                while True:
                    chunk = source.read(1024 * 1024)
                    if not chunk:
                        break
                    stream.write(chunk); digest.update(chunk)
            for clause in suffix:
                line = (' '.join(map(str, clause)) + ' 0\n').encode()
                stream.write(line); digest.update(line)
        if digest.hexdigest() != row['sha256'] or (output/row['filename']).stat().st_size != row['bytes']:
            raise ValueError('historical branch reproduction mismatch: ' + row['branch'])
        result.append({'branch': row['branch'], 'sha256': digest.hexdigest()})
    return {'status': 'BYTE_REPRODUCED_FOUR_FROZEN_CNFS', 'base_sha256': expected_base['sha256'],
            'branches': result, 'solver_calls': 0}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    print(json.dumps(rebuild(args.output), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
