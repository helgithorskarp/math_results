"""Independent complete-word checker for two reflected common fibres.

Standard library only. Global reflection is required; independent coordinate
reflection is not. All modular and ordinary Schur sums include equal summands.
"""
import argparse
import json
import math
from pathlib import Path


def check(data):
    a=data['axis_factor'];n=data['modulus'];word=data['word']
    if a<3 or a%2==0 or math.gcd(a,5)!=1 or n!=5*a:
        raise ValueError('bad CRT factors')
    if len(word)!=n-1 or any(type(c) is not int or not 0<=c<6 for c in word):
        raise ValueError('bad full word')
    row=[-1]+word;u=5*pow(5,-1,a);v=a*pow(a,-1,5)
    E=[-1]+[row[u*x%n] for x in range(1,a)]
    Q=[row[(u*x+v)%n] for x in range(a)]
    if Q[0]!=0 or 1 in Q:raise ValueError('bad first fibre')
    for x in range(1,n):
        if row[x]!=row[n-x]:raise ValueError('global reflection fails')
        aa,b=x%a,x%5
        if b==0:expected=E[aa]
        else:
            state=Q[aa if b in (1,2) else -aa%a]
            expected=state if state else (0 if b in (1,4) else 1)
        if row[x]!=expected:raise ValueError('reflected fibre rule fails')
    axis=[{x for x in range(1,a) if E[x]==c} for c in range(6)]
    fibres={c:{x for x in range(a) if Q[x]==c} for c in (0,2,3,4,5)}
    sf=lambda B:all((x+y)%a not in B for x in B for y in B)
    diff=lambda B:{(x-y)%a for x in B for y in B}
    if not all(sf(B) for B in axis):raise ValueError('axis not sum-free')
    if any(not sf(fibres[c]|{-x%a for x in fibres[c]}) for c in (2,3,4,5)):
        raise ValueError('a common symmetric support is not sum-free')
    if (axis[0]|axis[1])&diff(fibres[0]):raise ValueError('residual-axis collision')
    if any(axis[c]&diff(fibres[c]) for c in (2,3,4,5)):
        raise ValueError('common-axis collision')
    integer_pairs=modular_pairs=0
    for x in range(1,n):
        for y in range(x,n):
            z=(x+y)%n
            if z:
                modular_pairs+=1
                if row[x]==row[y]==row[z]:raise ValueError(('modular violation',x,y,z))
            if x+y<n:
                integer_pairs+=1
                if row[x]==row[y]==row[x+y]:raise ValueError(('integer violation',x,y,x+y))
    asymmetric=sum(Q[x]!=Q[-x%a] for x in range(1,(a+1)//2))
    if data.get('require_asymmetric') and not asymmetric:raise ValueError('symmetric fibre was excluded')
    if data.get('normalize_axis') and E[1]!=0:raise ValueError('axis normalization fails')
    return dict(status='REFLECTED_SHARED_WORD_OK',modulus=n,endpoint=n-1,colours=6,
                class_sizes=[word.count(c) for c in range(6)],integer_pairs=integer_pairs,
                modular_pairs=modular_pairs,asymmetric_fibre_pairs=asymmetric,
                special_axis_mergeable=sf(axis[0]|axis[1]),residual_size=len(fibres[0]),
                common_sizes=[len(fibres[c]) for c in (2,3,4,5)])


def check_control(data):
    report = check(data)
    a, n = data["axis_factor"], data["modulus"]
    row = [-1] + data["word"]
    u, v = 5 * pow(5, -1, a), a * pow(a, -1, 5)
    E = [{x for x in range(1, a) if row[u*x % n] == c} for c in range(6)]
    C = {c: {x for x in range(a) if row[(u*x+v) % n] == c}
         for c in (0, 2, 3, 4, 5)}
    I = {x for x in range(a) if a < 3*x < 2*a}
    absent = data["absent_axis_colour"]
    if E[absent]:
        raise ValueError("specified axis class is not empty")
    if data["family"] == "full middle third":
        if C[2] != I or absent != 2:
            raise ValueError("the common fibre is not the full middle third")
        report["full_middle_third_size"] = len(I)
    elif data["family"] == "noninterval absent axis":
        for c, k in zip((2, 3, 4), data["interval_dilations"]):
            if math.gcd(k, a) != 1 or not C[c] <= {k*x % a for x in I}:
                raise ValueError("specified interval support fails")
        cover = [k for k in range(1, a) if math.gcd(k, a) == 1
                 and C[5] <= {k*x % a for x in I}]
        if cover or absent != 5:
            raise ValueError("free common support has an interval cover")
        # I is symmetric, so testing C is equivalent to testing C union -C.
        report["free_support_interval_dilations"] = cover
        report["interval_dilations"] = data["interval_dilations"]
    else:
        raise ValueError("unknown fixture family")
    report["absent_axis_colour"] = absent
    return report


if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    controls = json.loads((folder / "controls.json").read_text())
    report = {"status": "PASS", "controls": [check_control(c) for c in controls]}
    expected = json.loads((folder / "expected.json").read_text())["controls"]
    if report != expected:
        raise RuntimeError(("control report differs", report))
    print(json.dumps(report, indent=2))
