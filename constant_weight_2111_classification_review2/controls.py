"""Definition-level cover controls and incidence-conjugacy controls."""
from pathlib import Path
from itertools import combinations, permutations
import argparse
import json
import subprocess
import time
import carrier as c
from incidence import canonical

def check(binary, inp, out, cap='200000', good=True):
    p = subprocess.run([str(binary), str(inp), str(out), cap], capture_output=True, text=True, timeout=20)
    c.require((p.returncode == 0) == good, 'native control returned wrong completion status: ' + p.stderr)
    return p

def run(work, target, sanitizers=False):
    start = time.monotonic()
    work.mkdir(parents=True, exist_ok=True)
    binary = work / 'partition'
    c.require(binary.exists(), 'compiled native census required')
    cols = tuple(sorted(c.word(q) for q in [(0,1,2,3),(0,4,5,6),(1,4,7,8),(0,2,4,8),(1,2,5,7),(2,3,6,8),(0,3,5,7),(1,3,4,6),(2,4,5,8)]))
    pp = tuple(combinations(range(9), 2))
    edges = [c.covered_pairs((w,)) for w in cols]
    truth = {}
    targets = []
    for mask in range(1 << len(cols)):
        words = tuple(w for j, w in enumerate(cols) if mask >> j & 1)
        required = c.covered_pairs(words)
        targets.append(required)
        if len(required) == 6 * len(words):
            truth.setdefault(required, set()).add(words)
    inp, out = work / 'controls-subsets.input', work / 'controls-subsets.jsonl'
    lines = ['9 9 512', *map(str, cols)]
    for index, required in enumerate(targets):
        missing = [i for i, pair in enumerate(pp) if pair not in required]
        lines.append(str(index) + ' ' + str(len(missing)) + ' ' + ' '.join(map(str, missing)))
    inp.write_text('\n'.join(lines) + '\n')
    check(binary, inp, out)
    answers = [json.loads(line) for line in out.read_text().splitlines()]
    c.require(len(answers) == 512, 'native subset controls incomplete')
    for index, answer in enumerate(answers):
        actual = set(map(tuple, answer['covers']))
        c.require(answer['index'] == index and actual == truth.get(targets[index], set()), 'native subset control differs from exhaustive literal truth')

    external = json.loads(target.read_text())
    fixtures = [tuple(o['representative']) for f in external['packing_families'] for o in f['orbits']]
    canonical_keys, conjugacies, states = [], 0, 0
    for star in fixtures:
        base = canonical(star)
        canonical_keys.append(base['canonical'])
        states += base['states']
        for high in permutations((1, 2, 3)):
            point = (0,) + high + tuple(range(4, 17))
            moved = c.image_star(star, point)
            other = canonical(moved)
            conjugated = {c.compose(point, c.compose(a, c.inverse(point))) for a in base['automorphisms']}
            c.require(other['canonical'] == base['canonical'] and set(other['automorphisms']) == conjugated, 'high relabeling changes canonical form or automorphism conjugacy')
            states += other['states']
            conjugacies += 1
        for low in (tuple(list(range(5, 17)) + [4]), tuple(reversed(range(4, 17)))):
            point = tuple(range(4)) + low
            other = canonical(c.image_star(star, point))
            conjugated = {c.compose(point, c.compose(a, c.inverse(point))) for a in base['automorphisms']}
            c.require(other['canonical'] == base['canonical'] and set(other['automorphisms']) == conjugated, 'low relabeling changes canonical form or automorphism conjugacy')
            states += other['states']
            conjugacies += 1
    c.require(len(set(canonical_keys)) == 8, 'distinct fixtures merged by incidence certificate')
    rejections = 0
    for bad in (fixtures[0][:-1], fixtures[0][:-1] + (fixtures[0][0],), (True,) + fixtures[0][1:], (1 << 17,) + fixtures[0][1:], (15,) + fixtures[0][1:]):
        try:
            canonical(bad)
        except ValueError:
            rejections += 1
        else:
            raise ValueError('corrupt incidence fixture was accepted')
    try:
        canonical(fixtures[0], cap=0)
    except ValueError as e:
        c.require('INCOMPLETE' in str(e), 'incidence zero guard did not report INCOMPLETE')
    else:
        raise ValueError('incidence zero guard completed')

    malformed = [
        '18 0 1\n0 0\n',
        '17 2 1\n15\n15\n0 0\n',
        '17 1 1\n15\n0 1 136\n',
        '17 1 1\n15\n0 2 135 135\n',
        '17 841 0\n',
    ]
    for i, text in enumerate(malformed):
        bad = work / ('control-bad-' + str(i) + '.input')
        bad.write_text(text)
        check(binary, bad, work / 'control-bad.out', good=False)
    # Empty uncovered domain is a genuine empty cover, so cap=0 must fail there.
    zero = work / 'control-zero.input'
    zero.write_text('0 0 1\n0 0\n')
    p = check(binary, zero, work / 'control-zero.out', cap='0', good=False)
    c.require('INCOMPLETE' in p.stderr, 'native zero guard did not report INCOMPLETE')
    check(binary, zero, work / 'control-zero.out', cap='200001', good=False)

    boundary = sorted(c.word(q) for q in combinations(range(15), 4))[:839]
    final = c.word((13, 14, 15, 16))
    boundary.append(final)
    required = c.covered_pairs((final,))
    missing = [i for i, pair in enumerate(c.PAIRS) if pair not in required]
    bound = work / 'control-840.input'
    bound.write_text('\n'.join(['17 840 1', *map(str, boundary), '0 ' + str(len(missing)) + ' ' + ' '.join(map(str, missing))]) + '\n')
    check(binary, bound, work / 'control-840.out')
    c.require(json.loads((work / 'control-840.out').read_text())['covers'] == [[final]], 'column840 / pair135 boundary cover failed')
    if sanitizers:
        sanitized = work / 'partition-sanitized'
        source = Path(__file__).resolve().parent / 'partition.cpp'
        subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer',str(source),'-o',str(sanitized)],capture_output=True,text=True,check=True,timeout=30)
        p = check(sanitized, bound, work / 'control-840-sanitized.out')
        c.require(not p.stderr and json.loads((work / 'control-840-sanitized.out').read_text())['covers'] == [[final]], 'sanitizer diagnostics or boundary mismatch')
    summary = {'status':'COMPLETE independent controls','literal_subset_cases':512,'incidence_conjugacies':conjugacies,'incidence_control_states':states,'malformed_incidence_rejections':rejections,'malformed_native_rejections':len(malformed)+1,'visible_INCOMPLETE_guards':2,'column840_pair135_positive':True,'sanitizers':sanitizers,'seconds':time.monotonic()-start}
    (work / 'controls.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--work',type=Path,required=True)
    p.add_argument('--target',type=Path,required=True)
    p.add_argument('--sanitizers',action='store_true')
    a=p.parse_args()
    run(a.work.resolve(),a.target.resolve(),a.sanitizers)
