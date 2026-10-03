"""Recover every literal right interface from the complete actual37 domain."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time
from model import Budget, Guard, digest, encode, literal37, load, need, validate
from partitions import key


def put(path, value):
    path.write_bytes(encode(value) + b'\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spec', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--input', type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    spec = json.loads(args.spec.read_bytes())
    for pin in spec['input_pins']:
        raw = Path(pin['path']).read_bytes()
        need(len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256'], 'whole input pin')
    data, input_sha = load(args.input)
    baseline = Budget('entire actual owner source validation')
    owners = validate(data, baseline)
    cases = [json.loads(line) for line in Path(spec['complete_case_stream']).read_text().splitlines()]
    need([r['case_index'] for r in cases] == list(range(data['representative_whole_case_count'])),
         'all frozen original-root/free-binding cases completed')
    certs = json.loads(Path(spec['whole_actual37_certificate_pool']).read_bytes())
    all_pairs = [(c['case_index'], p) for c in cases for p in c['whole_solution_maps']]
    need(sorted((c['case_index'], c['point_map']) for c in certs) == sorted(all_pairs),
         'entire completed point-map certificate multiset')
    rows = []
    active = None
    progress = {'complete': False, 'status': 'INCOMPLETE_NOT_ABSENCE', 'completed_certificates': 0}
    put(args.out / 'progress.json', progress)
    try:
        for i, cert in enumerate(certs):
            if time.monotonic() - start > 60:
                raise Guard('original60s focused interface child')
            active = Budget('whole actual37 right-interface certificate ' + str(i))
            owner_rank, rem = divmod(cert['case_index'], 2592)
            orientation, free_rank = divmod(rem, 1296)
            u, v = data['source_root_orientations'][orientation]
            owner_index = sorted(owners)[owner_rank]
            need(cert['original_owner_row_index'] == owner_index and
                 cert['source_root_orientation'] == [u, v] and cert['free_rank'] == free_rank,
                 'all certificate original case bindings')
            image = cert['point_map']
            words = literal37(data['whole_original_Q4_quadruples'], owners[owner_index], image, u, v, active)
            need(words['whole37_union'] == cert['whole37_union'], 'entire recovered original37 word union')
            F = sorted(sorted(image[a] for a in q if a != v)
                       for q in data['whole_original_Q4_quadruples'] if v in q)
            need(len(F) == 3 and all(len(f) == 3 for f in F) and
                 len(set().union(*(set(f) for f in F))) == 9 and
                 set().union(*(set(f) for f in F)) <= set(range(15)), 'actual right triple partition')
            M = data['target_mate_triples']
            union_sets = [set(w) for w in words['whole37_union']]
            physical_F = sorted(sorted(w - {15, 17}) for w in union_sets if {15, 17} <= w)
            physical_M = sorted(sorted(w - {16, 17}) for w in union_sets if {16, 17} <= w)
            need(physical_F == F and physical_M == sorted(M), 'whole-word and source-root interfaces identical')
            free_union = set().union(*(set(f) for f in F))
            counts = sorted(len(set(m) & free_union) for m in M if set(m).isdisjoint(range(5)))
            physical_counts = sorted(len((w - {16, 17}) & free_union) for w in union_sets
                                     if {16, 17} <= w and (w - {16, 17}).isdisjoint(range(5)))
            need(counts == physical_counts and len(counts) == 2, 'whole SAT-only mate/free incidences')
            rows.append({'certificate_index': i, 'case_index': cert['case_index'], 'owner_row': owner_index,
                         'source_roots': [u, v], 'actual_right_F': F,
                         'whole_actual_right_canonical_key': key(M, F, active),
                         'SAT_only_mate_free_union_intersection_sizes': counts})
            progress['completed_certificates'] = len(rows)
            put(args.out / 'progress.json', progress)
            active = None
        controls = []
        for name, field in [('missing original Q word', 'whole_original_Q4_quadruples'),
                            ('missing original owner word', 'whole_original20_quadruples'),
                            ('false original Hub-role image', 'original17_point_map')]:
            damaged = json.loads(json.dumps(data))
            if field == 'whole_original_Q4_quadruples':
                damaged[field].pop()
            elif field == 'whole_original20_quadruples':
                damaged['all_original_owner_rows'][0][field].pop()
            else:
                values = damaged['all_original_owner_rows'][0][field]
                roles = damaged['all_original_owner_rows'][0]['complete_original_decorated_owner_record'][0][3]
                values[roles[0]], values[roles[1]] = values[roles[1]], values[roles[0]]
            try:
                validate(damaged, baseline)
            except ValueError:
                controls.append(name)
            else:
                raise ValueError('semantic damage accepted: ' + name)
        if certs:
            cert = certs[0]
            wrong = cert['point_map'].copy()
            u, v = cert['source_root_orientation']
            wrong[u], wrong[v] = wrong[v], wrong[u]
            try:
                literal37(data['whole_original_Q4_quadruples'], owners[cert['original_owner_row_index']], wrong, u, v, baseline)
            except ValueError:
                controls.append('false original-root image')
            else:
                raise ValueError('semantic damage accepted: false original-root image')
            try:
                need(literal37(data['whole_original_Q4_quadruples'], owners[cert['original_owner_row_index']],
                               cert['point_map'], u, v, baseline)['whole37_union'] == cert['whole37_union'][:-1],
                     'entire claimed37 union required')
            except ValueError:
                controls.append('missing claimed37 word')
            else:
                raise ValueError('semantic damage accepted: missing claimed37 word')
        distinct = sorted({encode(r['actual_right_F']): r['actual_right_F'] for r in rows}.values())
        mathematical = {'actual_agent': 'six-code-1', 'role': 'researcher', 'complete': True,
                        'original_type_id': data['original_type_id'], 'all_original_owner_rows': data['owner_row_indices'],
                        'representative_whole_cases': data['representative_whole_case_count'],
                        'raw_representative_map_domain': data['representative_whole_case_count'] * 720,
                        'raw_all_original_owner_map_domain': data['all_original_owner_whole_case_count'] * 720,
                        'actual37_map_count': len(certs), 'literal_distinct37_unions': len({encode(c['whole37_union']) for c in certs}),
                        'literal_distinct_right_interfaces': len(distinct), 'all_distinct_literal_right_F': distinct,
                        'all_actual37_right_interface_records': rows,
                        'all_actual_SAT_only_incidence_patterns': sorted({tuple(r['SAT_only_mate_free_union_intersection_sizes']) for r in rows}),
                        'semantic_damages_rejected': controls, 'ordinary_completeness_bridge': 'unformalized',
                        'independent_person_review': 'pending', 'global_endpoint_change': False,
                        'direct_input_sha256': input_sha}
        put(args.out / 'mathematical-record.json', mathematical)
        progress.update(complete=True, status='COMPLETE_LITERAL_SCOPE', mathematical_sha256=digest(mathematical))
        put(args.out / 'progress.json', progress)
        summary = {'mathematical_record': mathematical, 'mathematical_sha256': digest(mathematical),
                   'elapsed_seconds': time.monotonic() - start,
                   'peak_rss_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
        put(args.out / 'summary.json', summary)
        print(json.dumps({'complete': True, 'actual37_maps': len(certs), 'literal37_unions': mathematical['literal_distinct37_unions'],
                          'literal_right_interfaces': len(distinct), 'actual_SAT_patterns': mathematical['all_actual_SAT_only_incidence_patterns'],
                          'mathematical_sha256': digest(mathematical)}))
    except BaseException as exc:
        progress.update(error_type=type(exc).__name__, error=str(exc), active_case=active.receipt() if active else None)
        put(args.out / 'progress.json', progress)
        put(args.out / 'completed-classification-prefix.json', rows)
        raise


if __name__ == '__main__':
    main()
