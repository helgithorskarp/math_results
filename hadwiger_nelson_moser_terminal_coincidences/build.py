"""Generate the complete 147-pair coincidence exclusion certificate."""
import argparse, hashlib, importlib.util, json, time
from itertools import combinations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / 'hadwiger_nelson_moser_all_terminal_contacts/certificate.json'
PRIOR_SHA = 'bddb9275204535cccce1d66bd2ad1415040a6807fdffb7902dec31fd57126a98'
FIELD = HERE.parent / 'hadwiger_nelson_long_terminal_gluing/verify.py'
FIELD_SHA = '61c91721d8764a743fa0ffc8a5a3b08e39402d09ea36857125f4353c3c38a7db'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def generate():
    need(hashlib.sha256(PRIOR.read_bytes()).hexdigest() == PRIOR_SHA, 'prior changed')
    need(hashlib.sha256(FIELD.read_bytes()).hexdigest() == FIELD_SHA, 'field changed')
    spec = importlib.util.spec_from_file_location('prior_tower', FIELD)
    field = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(field)
    prior = json.loads(PRIOR.read_bytes())
    M = prior['M']
    D = [prior['C'][i] for i in prior['D_indices']]
    mm = [[i, j, *field.distance(M[i], M[j])] for i, j in combinations(range(7), 2)]
    md = [[i, j, *field.distance(M[i], D[j])] for i, j in product(range(7), range(18))]
    need(all(tuple(row[2:]) not in ((1008, 0, 0, 0), (1296, 0, 0, 0)) for row in mm + md), 'long pair found')
    return {'prior_sha256': PRIOR_SHA, 'squared_distance_scale': 144,
            'basis': ['1', 'sqrt3', 'sqrt11', 'sqrt33'], 'M_M': mm, 'M_D': md}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    parser.add_argument('--discover', action='store_true')
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    raw = (json.dumps(generate(), sort_keys=True, separators=(',', ':')) + '\n').encode()
    if not args.discover:
        need(raw == (HERE / 'certificate.json').read_bytes(), 'certificate mismatch')
    (out / 'certificate.json').write_bytes(raw)
    result = {'status': 'PASS', 'exact_pair_norms': 147,
              'certificate_bytes': len(raw), 'certificate_sha256': hashlib.sha256(raw).hexdigest(),
              'native_solver_calls': 0, 'seconds': time.monotonic() - start}
    (out / 'build.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))

if __name__ == '__main__':
    main()
