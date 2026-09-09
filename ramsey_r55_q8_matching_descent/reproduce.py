"""Verify saved construction evidence; --search also regenerates trajectories."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path
import subprocess

import audit
import verify

HERE = Path(__file__).resolve().parent


def prepare(out):
    data = json.loads((HERE / 'INPUTS.json').read_text())
    for record in data['trials']:
        r = record['r']
        text = record['core_graph6']
        if ord(text[0]) - 63 != 11:
            raise ValueError('core order')
        raw = [(ord(c) - 63 >> s) & 1 for c in text[1:] for s in range(5,-1,-1)]
        core = {}
        pos = 0
        for v in range(11):
            for u in range(v):
                core[u,v] = raw[pos]
                pos += 1
        core_adj = [sum(core[tuple(sorted((u,v)))] << v for v in range(11) if u != v) for u in range(11)]
        if verify.cliques(core_adj,(1<<11)-1,4) or verify.cliques(verify.complement(core_adj),(1<<11)-1,4):
            raise ValueError('not a Ramsey(4,4) core')
        state = 0x5235350000000000 + r
        mask64 = (1 << 64) - 1
        bits, fixed = [], []
        for u,v in it.combinations(range(43),2):
            if u >= 32:
                color, pin = core[u-32,v-32], True
            elif v < 32 and u//4 == v//4:
                color, pin = int(u//4 < r), True
            else:
                state = (state + 0x9E3779B97F4A7C15) & mask64
                z = state
                z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & mask64
                z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & mask64
                z ^= z >> 31
                color, pin = z & 1, False
            bits.append(str(color))
            fixed.append(str(int(pin)))
        bits, fixed = ''.join(bits), ''.join(fixed)
        payload = f'43 5 {4*r}\n{bits}\n{fixed}\n'
        if bits != record['initial_red_pair_bits'] or fixed != record['fixed_pair_bits'] or hashlib.sha256(payload.encode()).hexdigest() != record['input_sha256']:
            raise ValueError('initialization mismatch')
        (out / f'trial-r{r}.txt').write_text(payload)
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('out',type=Path)
    parser.add_argument('--search',action='store_true',help='Regenerate the four trajectories, not required to check saved evidence')
    args = parser.parse_args()
    args.out.mkdir()
    prepare(args.out)
    subprocess.run(['g++','-std=c++20','-O3','-Wall','-Wextra',str(HERE/'certify.cpp'),'-o',str(args.out/'certify')],check=True)
    expected = json.loads((HERE/'EXPECTED.json').read_text())
    if args.search:
        subprocess.run(['g++','-std=c++20','-O3','-Wall','-Wextra',str(HERE/'descent.cpp'),'-o',str(args.out/'descent')],check=True)
        verify.controls((args.out/'descent').resolve(),args.out/'controls')
    checked = []
    for record in expected['trials']:
        r = record['r']
        run = args.out / f'run-r{r}'
        if args.search:
            subprocess.run([str((args.out/'descent').resolve()),'run',str(args.out/f'trial-r{r}.txt'),str(run)],check=True)
            producer = json.loads((run/'RESULT.json').read_text())
            for k in ('initial','final','sweeps','accepted_moves'):
                if producer[k] != record[k]:
                    raise ValueError(('trajectory result changed',r,k))
        else:
            run.mkdir()
            source = verify.read(args.out / f'trial-r{r}.txt')
            (run/'endpoint.txt').write_text(f'43 5 {4*r}\n'+record['endpoint_red_pair_bits']+'\n'+source[-1]+'\n')
            accepted = {}
            for line in (HERE/'paths'/f'r{r}.tsv').read_text().splitlines()[1:]:
                sweep,m,before,after,mask = map(int,line.split())
                if (sweep,m) in accepted:
                    raise ValueError('duplicate path step')
                accepted[sweep,m] = (before,after,mask)
            score = record['initial']
            with (run/'trace.tsv').open('w') as f:
                f.write('sweep\tmatching\tbefore\tafter\tmask\n')
                for sweep in range(1,record['sweeps']+1):
                    for m in range(43):
                        before,after,mask = accepted.pop((sweep,m),(score,score,0))
                        if before != score:
                            raise ValueError('path cost')
                        f.write(f'{sweep}\t{m}\t{before}\t{after}\t{mask}\n')
                        score = after
            if accepted:
                raise ValueError('unconsumed path steps')
        n,k,tail,pairs,a,fixed = verify.read(run/'endpoint.txt')
        literal = verify.literal_cost(a,k,tail)
        if n != 43 or literal != record['costs'] or audit.bit_string(a,pairs) != record['endpoint_red_pair_bits']:
            raise ValueError('literal endpoint')
        receipt = {'initial':record['initial'],'final':record['final'],
                   'accepted_moves':record['accepted_moves'],'exact_kernels':record['exact_matching_minimizations'],
                   'independent_literal_endpoint_costs':literal}
        (run/'EXECUTION_RECEIPT.json').write_text(json.dumps(receipt)+'\n')
        result = audit.audit_one(args.out,r,(args.out/'certify').resolve())
        for key,value in record.items():
            if key == 'stationarity_nodes':
                # Node order is fixed for this source but is not mathematical evidence.
                continue
            if result[key] != value:
                raise ValueError(('audit mismatch',r,key))
        checked.append({k:v for k,v in result.items() if k not in ('accepted_path','endpoint_red_pair_bits','matching_sizes')})
    status = {'status':'REPRODUCED_NONZERO_CONSTRUCTION_BOUNDARY','search_regenerated':args.search,
              'trials':checked,'good43_count':0,'original_task_exclusions':0}
    (args.out/'REPRODUCTION.json').write_text(json.dumps(status,indent=2)+'\n')
    print(json.dumps(status,indent=2))


if __name__ == '__main__':
    main()
