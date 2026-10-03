"""Derive every stage input from completed outputs and canonical source only."""
import argparse
import hashlib
import json
import time
from pathlib import Path

START = time.monotonic()
STATES = 0


def require(ok, message):
    if not ok:
        raise ValueError(message)


def tick():
    global STATES
    STATES += 1
    if STATES > 500000 or time.monotonic() - START > 20:
        raise RuntimeError('INCOMPLETE: original500000/20 guard')


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', type=Path, required=True)
    ap.add_argument('--stage', required=True)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    root = Path(__file__).resolve().parent
    parameters = json.loads((root / 'PARAMETERS.json').read_text())
    stage = a.stage
    require(stage in parameters['stages'], 'declared input stage')
    target = root / stage
    generated = []

    def put(name, value, compact=False):
        tick()
        if compact:
            (target / name).write_text(json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n')
        else:
            write(target / name, value)
        generated.append(name)

    def predecessor(name, kernel='literal'):
        tick()
        return json.loads((a.work / name / (kernel + '.json')).read_text())

    put('EXPECTED.json', parameters['stages'][stage]['expected'])
    if stage in ['ordered', 'full', 'rooted']:
        anchor = predecessor('anchor')
        require(anchor['common_math_sha256'] == parameters['expected_math']['anchor'],
                'canonical anchor stage completed')
        put('INPUT.json', anchor['mathematics'])
    if stage == 'filter':
        for key, name in [('ANCHORS', 'anchor'), ('ORDERED', 'ordered'),
                          ('FULL', 'full'), ('STAR', 'rooted')]:
            result = predecessor(name)
            require(result['common_math_sha256'] == parameters['expected_math'][name],
                    'complete canonical precursor: ' + name)
            put(key + '.json', result)
    if stage in ['rooted', 'images', 'pairs']:
        fixture = (root / 'FIXTURES.json').read_bytes()
        require(hashlib.sha256(fixture).hexdigest() == parameters['fixture_file_sha256'],
                'whole credited public23-fixture file')
        (target / 'FIXTURES.json').write_bytes(fixture)
        generated.append('FIXTURES.json')
    if stage == 'images':
        anchors = predecessor('anchor')['mathematics']['records']
        full = predecessor('full')['mathematics']
        rooted = predecessor('rooted')['mathematics']
        filtered = predecessor('filter', 'filter')
        require(filtered['whole_result_math_sha256'] == parameters['expected_filter_whole_result_sha256'],
                'complete all-three-root filter')
        reps = [q['representative_index'] for q in filtered['full_class_summaries']
                if q['required_all_roots_locally_possible']]
        require(reps == [0, 10], 'two necessary representatives, all original roles retained')
        put('INPUT.json', dict(agent='six-code-3', role='researcher',
            anchors=[dict(representative=rep, anchor=anchors[rep]['anchor']) for rep in reps],
            application_review=parameters['input_metadata']['application_review'],
            source_anchor_theorem=parameters['input_metadata']['images_source_anchor_theorem']))
        controls = []
        for rep in reps:
            case = next(c for c in rooted['pair_cases']
                        if any(p['anchor_index'] == rep for p in c['positive_anchors']))
            positive = next(p for p in case['positive_anchors'] if p['anchor_index'] == rep)
            for c_root in [1, 2, 3]:
                tick()
                transport = next(t for t in full['all_transports']
                    if t['source'] == rep and t['target'] == rep and t['point_image'][1] == c_root)
                image = transport['point_image']
                fixed = sorted(sorted(image[p] for p in w) for w in case['fixed_star'])
                union = sorted(sorted(image[p] for p in w) for w in positive['full24'])
                controls.append(dict(C_root=c_root, anchor_representative=rep,
                    anchor_stabilizer_transport=transport, full20_star=fixed, full24_control=union,
                    heavy_missing_W_points=[p for p in range(4, 18)
                        if not any(0 in w and p in w for w in fixed)],
                    original17_point_image=[image[p] for p in case['point_image']],
                    source_fixture_index=rooted['fixture_index'], source_old_C_pair=case['old_C_pair'],
                    status='LITERAL_POSITIVE_LOCAL_GEOMETRY_CONTROL_ONLY_NO_K17_REALIZATION'))
        put('GEOMETRY_CONTROLS.json', controls)
    if stage == 'pairs':
        images = predecessor('images')
        require(images['common_math_sha256'] == parameters['expected_math']['images'],
                'complete original physical-map census')
        math = images['mathematics']
        image_input = json.loads((root / 'images/INPUT.json').read_text())
        groups = []
        for g in math['groups']:
            candidates = []
            for i, c in enumerate(g['candidates']):
                tick()
                candidates.append(dict(id=i, full20=c['full20'], missing_W=c['missing_W'],
                    origins=[dict(parent_map_id=mid, point_image=math['maps'][mid]['point_image'])
                             for mid in c['map_ids']]))
            groups.append(dict(anchor=g['anchor'], root=g['root'], candidates=candidates))
        put('INPUT.json', dict(agent='six-code-3', role='researcher', anchors=image_input['anchors'],
            complete_parent_manifest_sha256=parameters['input_metadata']['original_image_manifest_sha256'],
            complete_parent_math_sha256=images['common_math_sha256'], groups=groups), compact=True)
    records = []
    for name in generated:
        data = (target / name).read_bytes()
        records.append(dict(path=str(Path(stage) / name), bytes=len(data),
                            sha256=hashlib.sha256(data).hexdigest()))
    write(a.output, dict(agent='six-code-3', role='researcher', stage=stage,
        status='COMPLETE_CANONICAL_INPUT_MATERIALIZATION', files=records, states=STATES,
        private_generated_inputs_read=False, historical_metadata_is_not_a_file_dependency=True,
        guard_states=500000, guard_seconds=20))
    print(json.dumps(dict(stage=stage, generated_files=len(records), states=STATES), sort_keys=True))


if __name__ == '__main__':
    main()
