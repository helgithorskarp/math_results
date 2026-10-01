"""Original-input and actual distinct-marker audits; imports no generator/solver."""
import hashlib
import itertools
import json
from pathlib import Path
from collections import Counter
import time

HERE = Path(__file__).resolve().parent
LOWER = (0, 0, 1, 3, 5, 9, 12, 16, 19, 25, 29, 35, 39)


def sha(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def replay(values, gates):
    values, spent = list(values), [0, 0]
    for a, b in gates:
        operands = values[a], values[b]
        spent[0] += 0 in operands
        spent[1] += 1 in operands
        if values[a] > values[b]:
            values[a], values[b] = values[b], values[a]
    return values, spent


def actual_marker_check(prefix, witness, polarity, spent, counter):
    """Every free Boolean assignment with distinct constant extreme labels."""
    marked = [i for i in range(13) if (witness >> i & 1) == polarity]
    free = [i for i in range(13) if i not in marked]
    labels = list(range(2, 2 + len(marked))) if polarity else list(range(-len(marked), 0))
    constants = dict(zip(marked, labels))
    constants_set = set(labels)
    membership, _ = replay([(witness >> i) & 1 for i in range(13)], prefix)
    expected = {i for i, v in enumerate(membership) if v == polarity}
    for assignment in range(1 << len(free)):
        row = [None] * 13
        for i, v in constants.items():
            row[i] = v
        for bit, port in enumerate(free):
            row[port] = assignment >> bit & 1
        charged = 0
        for a, b in prefix:
            charged += row[a] in constants_set or row[b] in constants_set
            if row[a] > row[b]:
                row[a], row[b] = row[b], row[a]
        assert charged == spent
        assert {i for i, v in enumerate(row) if v in constants_set} == expected
        counter['actual_marked_free_assignments'] += 1


def local_cut_controls():
    pairs = list(itertools.combinations(range(9), 2))
    count = 0
    for polarity, cut, singleton, sorted_singleton in [(0, {0, 1}, 509, 510), (1, {7, 8}, 128, 256)]:
        internal = tuple(sorted(cut))
        for integer in range(512):
            row = [(integer >> i) & 1 for i in range(9)]
            before = sum(row[i] == polarity for i in cut)
            for a, b in pairs:
                output, _ = replay(row, [(a, b)])
                after = sum(output[i] == polarity for i in cut)
                touched = row[a] == polarity or row[b] == polarity
                assert before <= after <= before + 1
                crossing = len({a, b} & cut) == 1
                if not crossing:
                    assert before == after
                if after > before:
                    assert crossing and touched
                if (a, b) == internal and before >= 1:
                    assert touched
                count += 1
        row = [(singleton >> i) & 1 for i in range(9)]
        for gate in pairs:
            result, _ = replay(row, [gate])
            actual = sum(v << i for i, v in enumerate(result))
            assert actual == (sorted_singleton if gate == internal else singleton)
    return {'moving_cut_truth_checks': count, 'mandatory_gate_truth_checks': 72}


def load_inputs(path=HERE):
    """Read only compact public fixtures and authenticate their literal bindings."""
    fixture = json.loads((path / 'fixture.json').read_text())
    parent = json.loads((path / 'reduction.json').read_text())
    certificate = json.loads((HERE / 'certificate.json').read_text())
    assert hashlib.sha256((path / 'reduction.json').read_bytes()).hexdigest() == certificate['reduction_sha256']
    assert hashlib.sha256((HERE / 'tail_obstructions.json').read_bytes()).hexdigest() == certificate['obstructions_sha256']
    assert parent['fixture_sha256'] == sha(fixture)
    fixture['tails'] = [r for c in parent['classes'] for r in c['remaining_tails']]
    obstructions = json.loads((HERE / 'tail_obstructions.json').read_text())['records']
    assert len(fixture['tails']) == len(obstructions) == 156
    assert [(r['parent_index'],r['image'],r['budget'],r['case']) for r in fixture['tails']] == [
        (r['parent_index'],r['image'],r['budget'],r['case']) for r in obstructions]
    fixture['obstructions'] = obstructions
    return fixture, certificate


def original_pool(fixture,target,instance,counter):
    prefix = fixture['prefix22'] + [[a+1,b+1] for a,b in target['prefix_B11']]
    assert prefix == instance['prefix13'] and len(prefix)+target['budget'] == 44
    pool, images = {}, set()
    for original in range(8192):
        values = [original >> i & 1 for i in range(13)]
        output, spent = replay(values,prefix)
        ordered = sorted(values)
        assert [output[i] for i in (0,1,11,12)] == [ordered[i] for i in (0,1,11,12)]
        middle = sum(v << i for i,v in enumerate(output[2:11]))
        images.add(middle)
        counter['original_prefix_inputs'] += 1
        if original in (0,8191):
            continue
        for p in (0,1):
            free = sum(v != p for v in values)
            limit = 44-LOWER[free]-spent[p]
            if (middle,p) not in pool or limit < pool[middle,p][0]:
                pool[middle,p] = limit,original,free,spent[p]
    assert sorted(images) == target['rows9'] and sha(target['rows9']) == target['rows9_sha256']
    caps = [[r,p,*pool[r,p]] for r,p in sorted(pool)]
    assert caps == instance['caps'] and sha(caps) == instance['caps_sha256']
    for original in fixture['B11_states']:
        values = [original >> i & 1 for i in range(11)]
        output,_ = replay(values,target['prefix_B11'])
        ordered = sorted(values)
        assert output[0] == ordered[0] and output[10] == ordered[10]
        assert sum(v << i for i,v in enumerate(output[1:10])) in images
        counter['B11_prefix_inputs'] += 1
    return prefix,pool


def small_sorter_check(k,rows,word):
    assert all(0 <= a < b < k for a,b in word)
    return all(replay([r >> i & 1 for i in range(k)],word)[0] ==
               sorted([r >> i & 1 for i in range(k)]) for r in rows)


SMALL_BOUNDS = {}


def check_internal_bound(obstacle,counter):
    """Enumerate every shorter literal word; no BFS or solver is imported."""
    k,q = obstacle['cut_size'],obstacle['internal_minimum']
    rows = tuple(obstacle['restricted_rows'])
    assert k in (3,4) and 0 <= q <= 5
    assert rows == tuple(sorted(set(rows))) and all(0 <= r < (1 << k) for r in rows)
    positive = obstacle['positive_internal_word']
    assert len(positive) == q and small_sorter_check(k,rows,positive)
    key = k,rows,q
    if key not in SMALL_BOUNDS:
        pairs = tuple(itertools.combinations(range(k),2))
        count = 0
        for length in range(q):
            for word in itertools.product(pairs,repeat=length):
                assert not small_sorter_check(k,rows,word), ('smaller internal sorter',k,rows,word)
                count += 1
        SMALL_BOUNDS[key] = count
        counter['shorter_internal_words'] += count
        counter['distinct_internal_bound_instances'] += 1


def check_obstruction(obstacle,rows,pool,prefix,counter):
    p,row = obstacle['polarity'],obstacle['row']
    assert p in (0,1) and row in rows
    cap,witness,free,spent = pool[row,p]
    assert (cap,witness,free,spent) == (obstacle['touch_cap'],obstacle['original_witness'],
                                      obstacle['free_inputs'],obstacle['prefix_passages'])
    assert cap == 44-LOWER[free]-spent
    actual_marker_check(prefix,witness,p,spent,counter)
    cut = set(obstacle['cut'])
    kind = obstacle['kind']
    total = sum((row >> i & 1) == p for i in range(9))
    inside = sum((row >> i & 1) == p for i in cut)
    if kind == 'single_control_movement':
        expected = set(range(9-total,9)) if p else set(range(total))
        deficit = total-inside
        assert cut == expected
        assert total == obstacle['total_middle_marks'] and inside == obstacle['initial_cut_marks']
        assert deficit == obstacle['crossing_deficit'] == obstacle['required_touches'] > cap
    elif kind == 'moving_two_port':
        assert cut == ({7,8} if p else {0,1})
        deficit = min(2,total)-inside
        assert inside == obstacle['initial_cut_marks'] >= 1
        assert total == obstacle['total_middle_marks'] and deficit == obstacle['crossing_deficit']
        assert obstacle['mandatory_row'] == (128 if p else 509) and obstacle['mandatory_row'] in rows
        assert obstacle['mandatory_gate'] == sorted(cut)
        assert obstacle['required_touches'] == deficit+1 > cap
    elif kind == 'fixed_internal_count':
        k = obstacle['cut_size']
        assert k in (3,4) and cut == (set(range(9-k,9)) if p else set(range(k)))
        assert total == inside == k and free == 11-k
        forced = obstacle['forced_cut_row']
        assert forced in rows
        def missing(r):
            total = sum((r >> i & 1) == p for i in range(9))
            inside = sum((r >> i & 1) == p for i in cut)
            return min(k,total)-inside
        crossings = max(map(missing,rows))
        assert crossings == missing(forced) == obstacle['required_crossings']
        ports = sorted(cut)
        outside = set(range(9))-cut
        restricted = sorted({sum((r >> port & 1) << j for j,port in enumerate(ports)) for r in rows
                             if all((r >> port & 1) != p for port in outside)})
        assert restricted == obstacle['restricted_rows']
        check_internal_bound(obstacle,counter)
        assert obstacle['required_touches'] == crossings+obstacle['internal_minimum'] > cap
    else:
        raise AssertionError(('unknown direct obstruction',kind))


def expanded_local_controls():
    """Check each local cut step, fixed controls and restricted projections."""
    pairs = tuple(itertools.combinations(range(9),2))
    movement = fixed = restricted = 0
    for p in (0,1):
        for k in range(10):
            cut = set(range(9-k,9)) if p else set(range(k))
            fixed_control = [p if i in cut else 1-p for i in range(9)]
            for gate in pairs:
                assert replay(fixed_control,[gate])[0] == fixed_control
                fixed += 1
            for integer in range(512):
                row = [integer >> i & 1 for i in range(9)]
                before = sum(row[i] == p for i in cut)
                for a,b in pairs:
                    output,_ = replay(row,[(a,b)])
                    change = sum(output[i] == p for i in cut)-before
                    crossing = (a in cut) != (b in cut)
                    touched = row[a] == p or row[b] == p
                    assert 0 <= change <= int(crossing)
                    if change:
                        assert crossing and touched
                    if k in (3,4) and all(row[i] != p for i in set(range(9))-cut):
                        if a not in cut or b not in cut:
                            assert all(output[i] == row[i] for i in cut)
                            restricted += 1
                    movement += 1
    return dict(all_cut_local_truth_checks=movement,fixed_control_gate_checks=fixed,
                small_restricted_projection_checks=restricted,**local_cut_controls())


def check_transfer(obstacle,rows,fixture,repository,counter):
    pinned = [
        ('sorting13_B11_ten_event_loop_postponement/certificate.json',
         '5360120fc75814699b79879b4fc3a7c43f00a37af0876bf58e0fb8144cc2cdf9'),
        ('sorting13_B11_ten_event_branch_exclusion/certificate.json',
         '47ec194a3decff3508ffb5d0279aea2352de1921b790287a5c2212c62ef74bee'),
        ('sorting13_B11_ten_event_branch_exclusion/PROOF.md',
         '78b383a1509f7f1a391d6c852fc5dd24726f803bc9d67ea31d674b82478b5f7c')]
    values = []
    for relative,expected in pinned:
        raw = (repository / relative).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == expected, ('transfer import bytes changed',relative)
        values.append(json.loads(raw) if relative.endswith('.json') else raw)
    parent,branch,_ = values
    assert branch['complete_branch_enrolled'] is True
    assert obstacle['source_graph_height'] == 8321
    assert obstacle['source_graph_ref'] == 'bafkreifcib3w3cug25defwdez653uh2joxlbfu4ake3zhcargklndfavwi'
    assert obstacle['source_image_id'] == 2 and obstacle['source_image_rows'] == 52
    assert obstacle['proved_minimum'] == 13 and obstacle['image_relation'] == 'equal'
    source = next(r for r in parent['classes'] if r['code'] == obstacle['source_ten_class_code'])
    assert source['image_id'] == 2 and source['events'] == obstacle['source_ten_prefix_B11']
    word = source['events']
    assert len(word) == 10 and all(0 <= a < b < 11 for a,b in word)
    full = fixture['prefix22']+[[a+1,b+1] for a,b in word]
    assert len(full)+12 == 44
    images = set()
    for original in range(8192):
        values = [original >> i & 1 for i in range(13)]
        output,_ = replay(values,full)
        ordered = sorted(values)
        assert [output[i] for i in (0,1,11,12)] == [ordered[i] for i in (0,1,11,12)]
        images.add(sum(v << i for i,v in enumerate(output[2:11])))
    assert rows == parent['images9'][2] == sorted(images)
    # Actual inverse-pair profiles certify that middle comparisons are profile loops.
    from verify_reduction import original_profile
    assert original_profile(full,False) == (((0,1),9),)
    assert original_profile(full,True) == (((11,12),9),)
    counter['transfer_original_prefix_inputs'] += 8192
    counter['transfer_imports'] += 1


def audit_data(fixture,data,certificate,repository,out):
    from verify import bounded
    counter = dict(original_prefix_inputs=0,actual_marked_free_assignments=0,B11_prefix_inputs=0,
                   shorter_internal_words=0,distinct_internal_bound_instances=0,
                   transfer_original_prefix_inputs=0,transfer_imports=0)
    tails,obstructions = fixture['tails'],fixture['obstructions']
    assert len(data['instances']) == len(tails) == 156
    assert [r['record'] for r in data['instances']] == tails
    sat_pairs = {(r['parent_index'],r['image']) for r in certificate['records']}
    assert sat_pairs == {(182,0),(196,0),(270,74),(273,75),(275,40),(288,0)}
    assert {(r['parent_index'],r['image']) for r in obstructions if r['obstruction'] is None} == sat_pairs
    base_images = set()
    full45 = fixture['prefix22']+[[a+1,b+1] for a,b in fixture['B11_known23_control']]
    assert len(full45) == 45
    for original in range(8192):
        row = [original >> i & 1 for i in range(13)]
        output,_ = replay(row,fixture['prefix22'])
        assert output[0] == min(row) and output[12] == max(row)
        base_images.add(sum(v << i for i,v in enumerate(output[1:12])))
        output,spent = replay(row,full45)
        assert output == sorted(row)
        if original not in (0,8191):
            for p in (0,1):
                assert spent[p] <= 45-LOWER[sum(v != p for v in row)]
    assert sorted(base_images) == fixture['B11_states'] and len(base_images) == 158
    checked,types = [],Counter()
    start = time.monotonic()
    for target,instance,record in zip(tails,data['instances'],obstructions):
        def one():
            prefix,pool = original_pool(fixture,target,instance,counter)
            assert instance['caps_sha256'] == record['caps_sha256']
            obstacle = record['obstruction']
            if obstacle is None:
                controls = set()
                for row,p,cap,witness,free,spent in instance['caps']:
                    if cap < target['budget'] and (witness,p) not in controls:
                        actual_marker_check(prefix,witness,p,spent,counter)
                        controls.add((witness,p))
                return 'complete_CNF_RUP'
            if obstacle['kind'] == 'ten_image_transfer':
                assert target['parent_index'] == 192 and target['image'] == 24 and target['budget'] == 11
                check_transfer(obstacle,target['rows9'],fixture,repository,counter)
            else:
                check_obstruction(obstacle,target['rows9'],pool,prefix,counter)
            return obstacle['kind']
        kind = bounded(one)
        types[kind] += 1
        checked.append(dict(parent_index=target['parent_index'],image=target['image'],budget=target['budget'],kind=kind))
        packet = dict(status='PARTIAL_SCALAR_FIRST4_TAIL_AUDIT',completed_tails=len(checked),
                      counters=counter,types=dict(types),seconds=time.monotonic()-start)
        (out / 'tail-audit-partial.json').write_text(json.dumps(packet,indent=2)+'\n')
        print(json.dumps(checked[-1]),flush=True)
    assert dict(types) == dict(single_control_movement=70,moving_two_port=46,fixed_internal_count=33,
                               ten_image_transfer=1,complete_CNF_RUP=6)
    counter.update(bounded(expanded_local_controls))
    counter.update(status='ALL_FIRST4_LITERAL_IMAGES_CAPS_AND_CUTS_INDEPENDENTLY_VERIFIED',types=dict(types),
                   original_base_inputs=8192,known45_original_inputs=8192,
                   pooled_caps=sum(len(r['caps']) for r in data['instances']))
    return counter
