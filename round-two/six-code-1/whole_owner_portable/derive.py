"""Derive complete inputs and collect completed domains, never saved corpora."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'literal'))
from model import Budget, Guard, digest, encode, need, validate


def put(path, value):
    Path(path).write_bytes(encode(value) + b'\n')


def pin(path):
    path = Path(path)
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest()}


def completed(directory):
    directory = Path(directory)
    p = json.loads((directory / 'progress.json').read_bytes())
    m = json.loads((directory / 'mathematical-record.json').read_bytes())
    need(p['complete'] and digest(m) == p['mathematical_sha256'],
         'whole completed child mathematical binding')
    return m


def generate(work, out, progress, start):
    domain = json.loads((ROOT / 'DOMAIN.json').read_bytes())
    fixtures = json.loads((ROOT / 'inventory/fixtures.json').read_bytes())['stars']
    aggregate = completed(work / 'aggregate')
    fine = json.loads((work / 'aggregate/decorated-classes.json').read_bytes())
    need(len(fine) == aggregate['all_original_colored_classes'], 'entire generated class catalogue')
    types = [{'original_type_id': i, 'canonical_key': row[0]} for i, row in enumerate(fine)
             if row[0][0] == 2]
    need(len(types) == 697 and len({encode(t['canonical_key']) for t in types}) == 697,
         'whole regenerated D2 dictionary, no imported keys')
    put(out / 'all697.json', {'all_original697_D2_types': types})
    wanted = {i for t in domain['base_type_ids'] for i in fine[t][3]}
    recovered = {}
    flat = 0
    with (out / 'complete-owner-records.jsonl').open('xb') as stream:
        for fi in domain['fixture_indices']:
            m = completed(work / ('fixture-%02d' % fi))
            need(m['fixture'] == fi, 'whole fixture index')
            for line in (work / ('fixture-%02d' % fi) / 'complete-owner-records.jsonl').open('rb'):
                group = json.loads(line)
                need(len(group) == 12, 'entire original physical owner group')
                for row in group:
                    need(row[0][0] == fi and len(row) == 12, 'full original row and fixture')
                    if flat in wanted:
                        recovered[flat] = row
                    flat += 1
                stream.write(line)
            progress['completed_fixture_indices'].append(fi)
            put(out / 'progress.json', progress)
            if time.monotonic() - start > 60:
                raise Guard('original60s source derivation child')
    need(flat == aggregate['all_original_named_rows'] and set(recovered) == wanted,
         'all original base rows from complete flat record domain')
    inputs = []
    for t in domain['base_type_ids']:
        indices = fine[t][3]
        need(len(indices) == len(set(indices)) == fine[t][1], 'whole base frequency and row list')
        rows = []
        literal_groups = defaultdict(list)
        for index in indices:
            record = recovered[index]
            need(record[7] == fine[t][0], 'entire regenerated base colored key')
            quads = fixtures[record[0][0]]
            values = record[8]
            star = tuple(sorted(tuple(sorted([16] + [values[p] for p in q])) for q in quads))
            literal_groups[star].append(index)
            rows.append({'original_named_record_index': index,
                         'whole_original20_quadruples': quads,
                         'original17_point_map': values,
                         'complete_original_decorated_owner_record': record})
        first = recovered[indices[0]]
        M, F = first[9], first[10]
        if domain['triple_order'][str(t)] == 'sorted triples':
            M, F = sorted(M), sorted(F)
        need(all(sorted(recovered[i][9]) == sorted(M) and
                 sorted(recovered[i][10]) == sorted(F) for i in indices),
             'all actual base original-row M/F interfaces agree')
        representatives = sorted(min(v) for v in literal_groups.values())
        data = {'actual_agent': 'six-code-1', 'role': 'researcher',
                'original_type_id': t, 'complete_original_colored_key': fine[t][0],
                'whole_original_Q4_quadruples': fixtures[4],
                'source_root_orientations': domain['source_root_orientations'],
                'owner_row_indices': indices, 'all_original_owner_rows': rows,
                'literal_owner_groups': sorted(sorted(v) for v in literal_groups.values()),
                'literal_distinct_owner_representatives': representatives,
                'target_mate_triples': M, 'target_free_triples': F,
                'free_case_count_per_owner_orientation': 1296,
                'six_hole_bijections_per_free_case': 720,
                'representative_whole_case_count': len(representatives) * 2592,
                'all_original_owner_whole_case_count': len(rows) * 2592,
                'original_guards': domain['original_guards'],
                'source_only_derived_from_complete_original_inventory': True}
        budget = Budget('whole source-only base input ' + str(t))
        validate(data, budget)
        put(out / ('input-%d.json' % t), data)
        inputs.append({'type_id': t, 'all_original_rows': indices,
                       'literal_distinct_owner_representatives': representatives,
                       'representative_whole_cases': data['representative_whole_case_count'],
                       'source_validation_states': budget.states, 'whole_input_sha256': digest(data)})
    return {'complete': True, 'action': 'source_only_derive', 'all_original_named_rows': flat,
            'all697_generated': True, 'all_complete_base_inputs': inputs,
            'prior_private_corpus_input': False, 'global_endpoint_change': False}


def assemble(work, out, base_type):
    data = json.loads((work / 'derived' / ('input-%d.json' % base_type)).read_bytes())
    directories = json.loads((work / ('case-dirs-%d.json' % base_type)).read_bytes())
    rows, certs = [], []
    for directory in directories:
        m = completed(directory)
        a = [json.loads(line) for line in (Path(directory) / 'complete-decisions.jsonl').open()]
        b = [json.loads(line) for line in (Path(directory) / 'actual37-certificates.jsonl').open()]
        need(digest(a) == m['complete_records_sha256'] and
             digest(b) == m['actual37_certificates_sha256'], 'entire completed case and certificate streams')
        rows.extend(a)
        certs.extend(b)
    need([r['case_index'] for r in rows] == list(range(data['representative_whole_case_count'])),
         'whole predetermined case domain exactly once')
    need(sorted((c['case_index'], c['point_map']) for c in certs) ==
         sorted((r['case_index'], p) for r in rows for p in r['whole_solution_maps']),
         'entire completed case/certificate binding')
    with (out / 'complete-decisions.jsonl').open('xb') as f:
        for row in rows:
            f.write(encode(row) + b'\n')
    put(out / 'actual37-certificates.json', certs)
    spec = {'input_pins': [pin(out / 'complete-decisions.jsonl'), pin(out / 'actual37-certificates.json')],
            'complete_case_stream': str(out / 'complete-decisions.jsonl'),
            'whole_actual37_certificate_pool': str(out / 'actual37-certificates.json')}
    put(out / 'interface-spec.json', spec)
    return {'complete': True, 'action': 'assemble', 'original_type_id': base_type,
            'whole_case_count': len(rows), 'actual37_map_count': len(certs),
            'whole_case_records_sha256': digest(rows), 'whole37_certificates_sha256': digest(certs)}


def gate_spec(work, out, base_type):
    data = json.loads((work / 'derived' / ('input-%d.json' % base_type)).read_bytes())
    interfaces = completed(work / ('interfaces-%d' % base_type))
    types = json.loads((work / 'derived/all697.json').read_bytes())['all_original697_D2_types']
    spec = {'input_pins': [pin(work / 'derived/all697.json'),
                          pin(work / ('interfaces-%d' % base_type) / 'mathematical-record.json')],
            'all_original697_D2_types': types,
            'all_literal_surviving_right_F': interfaces['all_distinct_literal_right_F'],
            'literal_right_interface_count': interfaces['literal_distinct_right_interfaces'],
            'actual_common_mate_partition': data['target_mate_triples'],
            'literal_scope': 'all original source-only derived type%d owner rows; Q4 both rooted views; all regenerated697 D2 keys; other physical owners outside' % base_type}
    put(out / 'gate-spec.json', spec)
    return {'complete': True, 'action': 'gate_spec', 'original_type_id': base_type,
            'whole_generated_types': len(types), 'all_actual_right_interfaces': spec['literal_right_interface_count']}


def transport_spec(work, out):
    domain = json.loads((ROOT / 'DOMAIN.json').read_bytes())
    specs = []
    pins = [pin(work / 'derived/all697.json'), pin(work / 'aggregate/decorated-classes.json'),
            pin(ROOT / 'inventory/fixtures.json'), pin(work / 'derived/complete-owner-records.jsonl')]
    for t in domain['base_type_ids']:
        gate = work / ('gate-%d' % t) / 'mathematical-record.json'
        data = work / 'derived' / ('input-%d.json' % t)
        pins.extend([pin(gate), pin(data)])
        specs.append({'original_type_id': t, 'complete697_gate_record': str(gate),
                      'whole_direct_owner_input': str(data)})
    spec = {'input_pins': pins, 'all697_spec': str(work / 'derived/all697.json'),
            'whole_original_fine_inventory': str(work / 'aggregate/decorated-classes.json'),
            'whole23_source_fixtures': str(ROOT / 'inventory/fixtures.json'),
            'whole_original_owner_record_file': str(work / 'derived/complete-owner-records.jsonl'),
            'completed_base_owner37_exclusions': specs}
    put(out / 'transport-spec.json', spec)
    return {'complete': True, 'action': 'transport_spec', 'whole_completed_base_inputs': domain['base_type_ids']}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('action', choices=['generate', 'assemble', 'gate_spec', 'transport_spec'])
    ap.add_argument('--work', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--type', type=int)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    progress = {'actual_agent': 'six-code-1', 'role': 'researcher', 'complete': False,
                'status': 'INCOMPLETE_NOT_ABSENCE', 'completed_fixture_indices': []}
    put(args.out / 'progress.json', progress)
    try:
        if args.action == 'generate':
            result = generate(args.work, args.out, progress, start)
        elif args.action == 'assemble':
            result = assemble(args.work, args.out, args.type)
        elif args.action == 'gate_spec':
            result = gate_spec(args.work, args.out, args.type)
        else:
            result = transport_spec(args.work, args.out)
        need(time.monotonic() - start < 60, 'original60s derivation child')
        put(args.out / 'mathematical-record.json', result)
        progress.update(complete=True, status='COMPLETE_SOURCE_ONLY_DERIVATION', mathematical_sha256=digest(result))
        put(args.out / 'progress.json', progress)
        put(args.out / 'summary.json', {'mathematical_record': result, 'mathematical_sha256': digest(result),
                                       'elapsed_seconds': time.monotonic() - start,
                                       'peak_rss_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
        print(json.dumps({'complete': True, 'action': args.action, 'mathematical_sha256': digest(result)}))
    except BaseException as exc:
        progress.update(error_type=type(exc).__name__, error=str(exc))
        put(args.out / 'progress.json', progress)
        raise


if __name__ == '__main__':
    main()
