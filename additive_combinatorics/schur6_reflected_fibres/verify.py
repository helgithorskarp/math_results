"""Definition-level verification of the reflected-fibre construction.

Standard library only. The all-parameter proof is in README.md. Tests do not
establish a new Schur-number bound or exhaust all members of the family.
"""
import argparse
import itertools
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


def inspect_fixture(data):
    checked=check(data);a=data['axis_factor'];n=5*a;row=[-1]+data['word']
    u=5*pow(5,-1,a);v=a*pow(a,-1,5)
    E=[-1]+[row[u*x%n] for x in range(1,a)]
    Q=[row[(u*x+v)%n] for x in range(a)]
    # At first-fibre coordinate zero, colour 0 is fixed by reflection.
    # A residual point whose negative has another colour rules out even an
    # arbitrary palette function implementing that same reflection.
    witness=next(x for x in range(1,a) if Q[x]==0 and Q[-x%a]!=0)
    images={c:sorted({Q[-x%a] for x in range(a) if Q[x]==c}) for c in (0,2,3,4,5)}
    if not(len(images[0])>1 and 0 in images[0]):raise ValueError('missing reflection obstruction')
    relabel=lambda c:0 if c in (0,1) else c-1
    projected=[-1]+[relabel(E[x%a] if x%2==0 else Q[x%a]) for x in range(1,2*a)]
    bad=[(x,y,(x+y)%(2*a)) for x in range(1,2*a) for y in range(x,2*a)
         if (x+y)%(2*a) and projected[x]==projected[y]==projected[(x+y)%(2*a)]]
    if checked['special_axis_mergeable'] and not bad:
        raise ValueError('the designated projection-failure fixture changed')
    middle={x for x in range(a) if a<3*x<2*a}
    intervals={k:{k*x%a for x in middle} for k in range(1,(a+1)//2)
               if math.gcd(k,a)==1}
    covers={}
    for c in (2,3,4,5):
        C={x for x in range(a) if Q[x]==c};B=C|{-x%a for x in C}
        covers[c]=[k for k,I in intervals.items() if B<=I]
    return dict(word=checked,reflection_obstruction=dict(axis_points=[0,witness],
                original_colour=0,reflected_colours=[0,Q[-witness%a]]),
                first_fibre_reflection_images=images,old_projection_defects=len(bad),
                first_projection_defect=list(bad[0]) if bad else None,
                common_support_middle_third_dilations=covers)


def one_colour_audit():
    a=7;cases=0
    for emask in range(8):
        E={x for u in range(1,4) if emask>>(u-1)&1 for x in (u,a-u)}
        for qmask in range(64):
            C={x for x in range(1,a) if qmask>>(x-1)&1}
            for kind in (0,1,2):
                if kind==2:
                    B=C|{-x%a for x in C}
                    points={(x,0) for x in E}|{(x,b) for x in C for b in (1,2)}|{(-x%a,b) for x in C for b in (3,4)}
                    expected=(all((x+y)%a not in E for x in E for y in E)
                              and all((x+y)%a not in B for x in B for y in B)
                              and all((x-y)%a not in E for x in C for y in C))
                else:
                    R=C|{0};b=kind+1
                    points={(x,0) for x in E}|{(x,b) for x in R}|{(-x%a,-b%5) for x in R}
                    expected=(all((x+y)%a not in E for x in E for y in E)
                              and all((x-y)%a not in E for x in R for y in R))
                actual=all(((x+u)%a,(b+v)%5) not in points for x,b in points for u,v in points)
                if actual!=expected:raise ValueError('one-colour criterion mismatch')
                cases+=1
    return cases


def main():
    root=Path(__file__).resolve().parent
    fixtures=json.loads((root/'fixtures.json').read_text())
    report=dict(status='PASS',fixtures=[inspect_fixture(data) for data in fixtures],
                complete_one_colour_cases=one_colour_audit(),new_s6_bound=False)
    # JSON-normalize integer map keys before comparing a saved JSON report.
    report=json.loads(json.dumps(report))
    if (root/'expected.json').exists() and report!=json.loads((root/'expected.json').read_text()):
        raise ValueError('expected complete report differs')
    print(json.dumps(report,sort_keys=True))


if __name__=='__main__':main()
