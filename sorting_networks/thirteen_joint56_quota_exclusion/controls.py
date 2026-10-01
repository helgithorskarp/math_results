"""Twelve actual positive sorters and semantic rejection of altered evidence."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import resource
import time

from audit_data import LOWER, load_inputs, replay, sha, original_pool, check_obstruction, check_internal_bound
from audit_encoding import Audit
from encoding import Encoding
from verify import bounded, read_cnf
from watched_rup import replay as rup_replay

HERE = Path(__file__).resolve().parent


def reject(name,call):
    try:
        bounded(call)
    except AssertionError:
        return dict(control=name,status='MALFORMED_CERTIFICATE_REJECTED')
    raise AssertionError(('Malformed certificate accepted',name))


def main():
    assert __debug__, 'Run with assertions enabled'
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent',type=Path,default=HERE)
    parser.add_argument('--out',type=Path,default=HERE/'out')
    parser.add_argument('--repository',type=Path,default=HERE.parents[1])
    args = parser.parse_args()
    start = time.monotonic()
    fixture,certificate = load_inputs(args.parent)
    data = json.loads((args.out/'data.json').read_text())
    insertion = [[i,i+1] for end in range(1,9) for i in range(end-1,-1,-1)]
    assert len(insertion) == 36
    positives = []
    for expected in certificate['records']:
        instance = next(r for r in data['instances'] if
                        (r['record']['parent_index'],r['record']['image']) == (expected['parent_index'],expected['image']))
        def one():
            full = instance['prefix13']+[[a+2,b+2] for a,b in insertion]
            total = len(full)
            for original in range(8192):
                values = [original >> i & 1 for i in range(13)]
                output,spent = replay(values,full)
                assert output == sorted(values)
                if original not in (0,8191):
                    for p in (0,1):
                        assert spent[p] <= total-LOWER[sum(v != p for v in values)]
            enc = Encoding(9,36,'g4')
            try:
                for row in instance['record']['rows9']:
                    enc.add_row(row)
                for row,p,cap,*_ in instance['caps']:
                    enc.touch_bound(row,cap+total-44,p)
                assert enc.solver.solve(assumptions=enc.assume_gates(insertion)) is True
                assert list(map(list,enc.decode())) == insertion
            finally:
                enc.solver.delete()
            return dict(parent_index=expected['parent_index'],image=expected['image'],total_size=total,
                        original_inputs=8192,status='FORCED_INSERTION_SORTER_SAT_AND_SCALAR_VERIFIED')
        positives.append(bounded(one))
        print(json.dumps(positives[-1]),flush=True)
    negative = []
    counters = dict(original_prefix_inputs=0,actual_marked_free_assignments=0,B11_prefix_inputs=0,
                    shorter_internal_words=0,distinct_internal_bound_instances=0)
    first_instance = data['instances'][0]
    altered = copy.deepcopy(first_instance)
    altered['caps'][3][2] += 1
    altered['caps_sha256'] = sha(altered['caps'])
    negative.append(reject('wrong_touch_cap_with_updated_digest',lambda:
                           original_pool(fixture,altered['record'],altered,counters)))
    internal = next(r for r in fixture['obstructions'] if r['obstruction'] and
                    r['obstruction']['kind'] == 'fixed_internal_count' and 0 < r['obstruction']['internal_minimum'] < 5)
    altered_bound = copy.deepcopy(internal['obstruction'])
    altered_bound['internal_minimum'] += 1
    altered_bound['positive_internal_word'].append([0,1])
    negative.append(reject('inflated_internal_minimum',lambda: check_internal_bound(altered_bound,counters)))
    movement = next(r for r in fixture['obstructions'] if r['obstruction'] and
                    r['obstruction']['kind'] == 'single_control_movement')
    item = next(r for r in data['instances'] if (r['record']['parent_index'],r['record']['image']) ==
                (movement['parent_index'],movement['image']))
    prefix,pool = bounded(original_pool,fixture,item['record'],item,counters)
    wrong = copy.deepcopy(movement['obstruction'])
    wrong['crossing_deficit'] += 1
    wrong['required_touches'] += 1
    negative.append(reject('inflated_movement_deficit',lambda:
                           check_obstruction(wrong,item['record']['rows9'],pool,prefix,counters)))
    first = certificate['records'][0]
    stem = args.out/f"class{first['parent_index']}_image{first['image']}"
    meta = json.loads(stem.with_suffix('.metadata.json').read_text())
    lines = stem.with_suffix('.cnf').read_text().splitlines(keepends=True)
    literals = lines[1].split()
    assert literals[-2] == '36'
    literals.pop(-2)
    lines[1] = ' '.join(literals)+'\n'
    bad_cnf = args.out/'invalid_choice.cnf'
    bad_cnf.write_text(''.join(lines))
    changed_meta,changed_expected = copy.deepcopy(meta),copy.deepcopy(first)
    changed_meta['cnf_sha256'] = changed_expected['cnf_sha256'] = hashlib.sha256(bad_cnf.read_bytes()).hexdigest()
    changed_meta['clause_stream_sha256'] = changed_expected['clause_stream_sha256'] = hashlib.sha256(''.join(lines[1:]).encode()).hexdigest()
    negative.append(reject('invalid_exact_one_with_updated_digests',lambda: Audit(changed_meta,bad_cnf,changed_expected).run()))
    n,core = read_cnf(HERE/first['core_file'])
    empty = args.out/'invalid_empty.rup'
    empty.write_text('0\n')
    negative.append(reject('premature_empty_RUP_step',lambda: rup_replay(n,core,empty)))
    fixture_raw = json.loads((HERE/'fixture.json').read_text())
    missing_class = copy.deepcopy(fixture_raw)
    missing_class['classes'].pop(0)
    from verify_reduction import load_premises
    scope = argparse.Namespace(repository=args.repository)
    negative.append(reject('omitted_complete_quota',lambda: load_premises(missing_class,scope)))
    assert len(positives) == 12 and len(negative) == 6
    report = dict(agent='six-sorting-1',role='researcher',positive=positives,negative=negative,
                  status='TWELVE_POSITIVE_SORTERS_AND_SIX_SEMANTIC_CONTROLS_VERIFIED',
                  seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (args.out/'controls.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)


if __name__ == '__main__':
    main()
