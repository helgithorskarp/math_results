"""Audit the zero-class lemma, controls, and completed height-80 searches.

--target also reruns the capped, unresolved height-160 experiment at 537.
No SAT solver, external input, or unproved cardinality bound is used.
"""
import argparse
from itertools import product
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent


def valid(word, m):
    if not word or any(type(a) is not int or abs(a) > m for a in word):
        return False
    for x in range(1, len(word)+1):
        for y in range(x, len(word)-x+1):
            a, b, c = word[x-1], word[y-1], word[x+y-1]
            if a == b == c == 0:
                return False
            if a != 0 and b != 0 and c != 0 and a+b != c:
                return False
    return True


def zero_potential(word, m):
    T = [v for v,c in enumerate(word,1) if c == 0]
    if not T:
        return
    potential = [0]+[word[t-T[0]-1] for t in T[1:]]
    assert len(set(potential)) == len(T) <= m+1
    assert max(potential)-min(potential) <= m
    for i,x in enumerate(T):
        for j in range(i+1,len(T)):
            difference = word[T[j]-x-1]
            assert difference != 0
            assert potential[j]-potential[i] == difference


def invoke(exe, n, m, cap=5_000_000):
    result = subprocess.run([str(exe), str(n), str(m), str(cap)], check=True,
                            capture_output=True, text=True)
    row = json.loads(result.stdout)
    assert (row['n'], row['m']) == (n, m)
    if row['status'] == 'SAT':
        assert len(row['labels']) == n and valid(row['labels'], m)
    return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', action='store_true')
    parser.add_argument('--cxx', default='g++')
    args = parser.parse_args()
    expected = json.loads((ROOT/'expected.json').read_text())
    counterexample = [1,0,-2,-1,0,0,-3,-2,-1]
    assert valid(counterexample, 3)
    assert sum(abs(x)==1 for x in counterexample) == 3
    zero_potential(counterexample, 3)
    # A general positive control at the disputed height, checked literally.
    assert valid(list(range(1,161))+[0]*161+list(range(-160,0)), 160)
    with tempfile.TemporaryDirectory(prefix='schur-additive-audit-') as tmp:
        executables = []
        for name in ('propagate', 'audit'):
            exe = Path(tmp)/name
            subprocess.run([args.cxx, '-std=c++17', '-O2', '-Wall', '-Wextra',
                            '-pedantic', str(ROOT/(name+'.cpp')), '-o', str(exe)],
                           check=True)
            executables.append(exe)
        tested = 0
        valid_words = 0
        for row in expected['complete_word_checks']:
            n, m = row['n'], row['m']
            count = 0
            for w in product(range(-m,m+1), repeat=n):
                if valid(w, m):
                    zero_potential(w, m)
                    count += 1
            valid_words += count
            tested += (2*m+1)**n
            assert count == row['valid_complete_words']
            for exe in executables:
                got = invoke(exe,n,m)
                assert got['status'] == ('SAT' if count else 'UNSAT_ENUMERATION')
        assert tested == 626628
        for m in range(1,41):
            for exe in executables:
                assert invoke(exe,3*m+1,m)['status'] == 'SAT'
        for m in range(1,21):
            rows = [invoke(exe,3*m+2,m) for exe in executables]
            assert all(r['status'] == 'UNSAT_ENUMERATION' for r in rows)
            assert rows[0]['nodes'] == rows[1]['nodes']
        print(json.dumps({'complete_assignments':tested,
                          'zero_class_lemma_controls':valid_words,
                          'positive_search_controls':80,
                          'small_exclusions':40,
                          'height160_standard_control':'valid',
                          'false_fibre_bound_counterexample':'valid'}),flush=True)
        for exe in executables:
            row = invoke(exe,242,80,300000)
            reference = expected['height80'][exe.name]
            for key, value in reference.items():
                if key != 'seconds':
                    assert row[key] == value, (exe.name,key,row[key],value)
            assert row['status'] == 'UNSAT_ENUMERATION'
            print(json.dumps({'implementation':exe.name,**row}),flush=True)
        print('Height-80 exclusion reproduced by both implementations.',flush=True)
        if args.target:
            print('Running the capped 537 experiment; UNKNOWN is not an exclusion.',flush=True)
            row = invoke(executables[0],537,160)
            for key,value in expected['target537'].items():
                if key != 'seconds':
                    assert row[key] == value, (key,row[key],value)
            assert row['status'] == 'UNKNOWN'
            print(json.dumps(row),flush=True)


if __name__ == '__main__':
    main()
