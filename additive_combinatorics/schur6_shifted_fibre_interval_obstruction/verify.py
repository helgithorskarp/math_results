"""Independent full-word verifier; imports no SAT encoder or solver."""
import json
from pathlib import Path

def verify_word(data):
    """Definition-level integer checks, not a solver/model evaluation."""
    a, p, word = (data['axis_factor'], data['short_factor'], data['word'])
    n, t = (a * p, (p - 1) // 2)
    assert a >= 3 and a % 2 and (p in (5, 7)) and (len(word) == n - 1)
    assert all((type(c) is int and 0 <= c < 6 for c in word))
    row = [-1] + word
    common = set(range(t, 6))
    fibre = [row[p * q + 1] for q in range(a)]
    assert fibre[0] == 0 and all((c == 0 or c in common for c in fibre))
    for q in range(a):
        for b in range(1, t + 1):
            expected = fibre[q] if fibre[q] else b - 1
            assert row[p * q + b] == expected
            assert row[n - p * q - b] == expected
    assert all((row[x] == row[n - x] for x in range(1, n)))
    ordinary = modular = 0
    for c in range(6):
        values = [x for x in range(1, n) if row[x] == c]
        occupied = set(values)
        for j, x in enumerate(values):
            for y in values[j:]:
                if (x + y) % n in occupied:
                    raise ValueError(('monochromatic modular equation', x, y, (x + y) % n))
                if x + y < n and x + y in occupied:
                    raise ValueError(('monochromatic integer equation', x, y, x + y))
    for x in range(1, n):
        for y in range(x, n):
            modular += (x + y) % n != 0
            ordinary += x + y < n
    return dict(status='SHIFTED_WORD_OK', endpoint=n - 1, class_sizes=[word.count(c) for c in range(6)], modular_pairs=modular, ordinary_pairs=ordinary, residual_size=fibre.count(0))


def check_control(data):
    report=verify_word(data)
    a,p=data['axis_factor'],data['short_factor']
    t=(p-1)//2;row=[-1]+data['word']
    E=[{q for q in range(1,a) if row[p*q]==c} for c in range(6)]
    Q=[row[p*q+1] for q in range(a)]
    C={c:{q for q in range(a) if Q[q]==c} for c in (0,*range(t,6))}
    sf=lambda S:all((x+y)%a not in S for x in S for y in S)
    diff=lambda S:{(x-y)%a for x in S for y in S}
    assert all(sf(S) for S in E)
    assert not set().union(*E[:t])&diff(C[0])
    for c in range(t,6):
        assert sf(C[c])
        assert all((-1-x-y)%a not in C[c] for x in C[c] for y in C[c])
        assert not E[c]&diff(C[c])
    if data.get('full_middle_third_colour') is not None:
        c=data['full_middle_third_colour']
        I={q for q in range(a) if a<3*q<2*a}
        assert C[c]==I
        first=next(x for x in range(1,a*p) if row[x]==c)
        assert first>=p*((a-1)//3)
        report['full_middle_third_colour']=c
        report['first_occurrence']=first
    return report


def run():
    controls=json.loads(Path(__file__).with_name('controls.json').read_text())
    return [check_control(data) for data in controls]


if __name__=='__main__':
    reports=run()
    expected=json.loads(Path(__file__).with_name('expected.json').read_text())
    assert reports==expected['controls']
    print(json.dumps({'status':'PASS','controls':reports},indent=2))
