"""Corruption and partial-run controls for the certificate interface.

Run after generate.py. These are interface tests, not an additional
independent proof algorithm. All checks remain active under Python -O.
"""
import argparse
import contextlib
import copy
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import verify

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--literal', type=Path, default=Path('literal_results.json'))
    args = parser.parse_args()
    original = json.loads(args.literal.read_text())
    expected = json.loads((HERE / 'expected.json').read_text())
    with contextlib.redirect_stdout(io.StringIO()):
        verify.check_certificates(args.literal, expected)
    # This admissible degree-nine generator must not be filtered away.
    verify.decode(['D', 2, 1, 1, 1, 3, 26, 3, 3])
    names = []
    with tempfile.TemporaryDirectory(prefix='book-c5-controls-') as temporary:
        directory = Path(temporary)
        fixture = directory / 'altered.json'

        def reject(name, alter):
            data = copy.deepcopy(original)
            alter(data)
            fixture.write_text(json.dumps(data, separators=(',', ':')) + '\n')
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    verify.check_certificates(fixture, expected)
            except ValueError:
                names.append(name)
                return
            raise ValueError('Accepted corrupted report: ' + name)

        reject('missing-record', lambda d: d['records'].pop())
        reject('duplicate-key', lambda d: d['records'].__setitem__(1, copy.deepcopy(d['records'][0])))
        reject('invalid-mask-shape', lambda d: d['records'][0][0].__setitem__(6, 0))
        reject('boolean-key', lambda d: d['records'][0][0].__setitem__(1, True))
        reject('alternate-generator-outside-degree-nine', lambda d: d['records'][0][0].__setitem__(1, 2))
        reject('wrong-color', lambda d: d['records'][0][1].__setitem__(2, 1 - d['records'][0][1][2]))

        def reverse_spine(d):
            w = d['records'][0][1]
            w[0], w[1] = w[1], w[0]

        reject('reversed-spine', reverse_spine)
        reject('endpoint-as-page', lambda d: d['records'][0][1][3].__setitem__(0, d['records'][0][1][0]))
        reject('repeated-page', lambda d: d['records'][0][1][3].__setitem__(-1, d['records'][0][1][3][0]))

        def wrong_page(d):
            key, w = d['records'][0]
            P, fixed = verify.decode(key)
            _, pages = verify.literal_pages(verify.neighbors(P, fixed), w[0], w[1])
            other = next(k for k in range(22) if k not in pages and k not in w[:2])
            w[3][0] = other

        reject('non-page-vertex', wrong_page)
        reject('wrong-advertised-digest', lambda d: d.__setitem__('records_sha256', '0' * 64))

        def wrong_order(d):
            import hashlib
            d['records'][0], d['records'][1] = d['records'][1], d['records'][0]
            d['records_sha256'] = hashlib.sha256(json.dumps(d['records'], separators=(',', ':')).encode()).hexdigest()

        reject('changed-record-order-with-rehashed-report', wrong_order)
        reject('incomplete-count', lambda d: d.__setitem__('templates_scanned', 18249))
        reject('partial-status', lambda d: d.__setitem__('status', 'partial'))
        reject('wrong-method', lambda d: d.__setitem__('method', 'heuristic'))
        reject('unaccounted-survivor', lambda d: d.__setitem__('survivors', [d['records'][0][0]]))
        reject('changed-family-count', lambda d: d['counts'].__setitem__('D', 10249))
        reject('changed-histogram', lambda d: d['first_violation_histogram'][0].__setitem__(1, 0))

        prefix = directory / 'literal_prefix.json'
        subprocess.run([sys.executable, '-B', '-O', str(HERE / 'generate.py'), '--limit', '17', '--output', str(prefix)],
                       check=True, capture_output=True, text=True)
        prefix_data = json.loads(prefix.read_text())
        require(prefix_data['status'] == 'partial' and prefix_data['templates_scanned'] == 17, 'Producer prefix status')
        try:
            verify.check_certificates(prefix, expected)
        except ValueError:
            names.append('actual-incomplete-producer')
        else:
            raise ValueError('Accepted actual partial producer')

        phase = directory / 'orbit_prefix.json'
        subprocess.run([sys.executable, '-B', '-O', str(HERE / 'verify.py'), '--literal', str(args.literal.resolve()),
                        '--limit', '17', '--output', str(phase)], check=True, capture_output=True, text=True)
        phase_data = json.loads(phase.read_text())
        require(phase_data['status'] == 'partial' and phase_data['templates_scanned'] == 17, 'Phase prefix status')
        names.append('actual-phase-prefix-labelled-partial')

        for script, limit in [('generate.py', 0), ('generate.py', 18251), ('verify.py', 0), ('verify.py', 4562501)]:
            result = subprocess.run([sys.executable, '-B', '-O', str(HERE / script), '--controls', '--limit', str(limit)],
                                    capture_output=True, text=True)
            require(result.returncode != 0, 'Accepted out-of-range limit')
            names.append(script + '-invalid-limit-' + str(limit))
    require(len(names) == 24, 'Failure-control coverage')
    print(json.dumps({'status': 'pass', 'controls': names, 'admissible_degree_nine_alternate_retained': True}, indent=2))


if __name__ == '__main__':
    main()
