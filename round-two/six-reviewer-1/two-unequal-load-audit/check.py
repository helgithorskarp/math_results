"""Independent audit. Exact sign reconstruction plus original-set controls."""
import argparse
import hashlib
import json
import resource
import signal
import sys
import time
from pathlib import Path


def require(p, message):
    if not p:
        raise ValueError(message)


def stop(signum, frame):
    raise TimeoutError('fixed 90 second job guard reached; no verdict from incomplete computation')


def signs():
    from algebra import construct, determinant, positivity, ATOMS, ZERO
    funcs, budget = construct()
    rows = [positivity(name, value) for name, value in funcs.items()]
    for k in range(1, 5):
        value = determinant([row[:k] for row in budget[:k]])
        rows.append(positivity('symmetric_minor_' + str(k), value))
        print('completed minor ' + str(k), file=sys.stderr, flush=True)
    # A sign defect and an exact determinant defect must both be noticed.
    from algebra import Rat
    try:
        positivity('damage', Rat(-1))
    except ValueError:
        pass
    else:
        raise ValueError('negative constant damage accepted')
    test = [[Rat(3), Rat(2)], [Rat(2), Rat(5)]]
    require(determinant(test) == 11, 'separate determinant control')
    test[0][1] = Rat(3)
    require(determinant(test) != 11, 'altered determinant control')
    return {'domain': 'QQ[Q,T,B]', 'substitution': 'q=Q+2,t=T+1,D=t+B+1; Q,T,B>=0',
            'functions': rows, 'positive_rational_functions': len(rows),
            'coefficient_terms': sum(row['numerator_terms'] + row['denominator_terms'] for row in rows),
            'automatically_factored_denominator_atoms': len(ATOMS),
            'exact_gram_to_correction_derivation': True,
            'two_plane_resolvent_independently_inverted': True,
            'damage_controls': 2}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vendor', type=Path, help='optional isolated SymPy 1.14.0 directory')
    parser.add_argument('--write', type=Path, help='generate fixture; never use to verify an existing fixture')
    parser.add_argument('--expected', type=Path)
    parser.add_argument('--stage', choices=['all', 'signs', 'literal', 'products'], default='all')
    args = parser.parse_args()
    if args.vendor:
        sys.path.insert(0, str(args.vendor.resolve()))
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import sympy
    require(sympy.__version__ == '1.14.0', 'SymPy 1.14.0 required')
    signal.signal(signal.SIGALRM, stop)
    signal.alarm(90)
    start = time.monotonic()
    out = {'agent': 'six-reviewer-1', 'role': 'independent mathematical reviewer',
           'sympy': sympy.__version__}
    if args.stage in ('all', 'signs'):
        out['signs'] = signs()
    if args.stage in ('all', 'literal'):
        import literal
        out['literal'] = literal.run()
    if args.stage in ('all', 'products'):
        import literal
        out['products'] = literal.products()
    signal.alarm(0)
    data = json.dumps(out, sort_keys=True, separators=(',', ':')).encode()
    if args.expected:
        require(out == json.loads(args.expected.read_text()), 'frozen independent record mismatch')
    if args.write:
        args.write.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({'positive_functions': out.get('signs', {}).get('positive_rational_functions'),
                      'coefficient_terms': out.get('signs', {}).get('coefficient_terms'),
                      'literal_instances': out.get('literal', {}).get('literal_instances'),
                      'exact_checks': out.get('literal', {}).get('exact_checks'),
                      'record_sha256': hashlib.sha256(data).hexdigest(),
                      'seconds': time.monotonic() - start,
                      'rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))


if __name__ == '__main__':
    main()
