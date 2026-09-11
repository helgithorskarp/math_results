"""Replay the finite checks supporting upper_bound72.md.

The imported classification/support theorems and the written mathematical
bridges are explicit premises, not assertions proved by this program.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys
import time
from projective import points,lines,hyperplanes

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,default=Path('build/upper72'))
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    source=Path(__file__).resolve().parent
    started=time.monotonic()
    executable=(args.out/'plane_caps').resolve()
    subprocess.run(['g++','-O3','-std=c++20','-Wall','-Wextra','-Wconversion',
                    str(source/'plane_caps.cpp'),'-o',str(executable)],check=True)
    planar=subprocess.check_output([str(executable)])
    assert planar==(source/'expected_planar.json').read_bytes()
    results={}
    for script,expected in [('check_reduction.py','expected_reduction.json'),
                            ('check_exceptional.py','exceptional_expected.json'),
                            ('check_lifted.py','lifted_expected.json')]:
        raw=subprocess.check_output([sys.executable,str(source/script)])
        assert raw==(source/expected).read_bytes()
        results[script]=json.loads(raw)

    # Compare the span-of-two-points and intersection-of-two-planes constructions.
    pg=points(4);ls=lines(4);hs=hyperplanes(4)
    intersections={tuple(sorted(set(a)&set(b))) for a,b in combinations(hs,2)}
    assert intersections==set(ls) and len(ls)==806
    point_counts=Counter(p for h in hs for p in h)
    pair_counts=Counter(pair for h in hs for pair in combinations(h,2))
    assert len(point_counts)==156 and set(point_counts.values())=={31}
    assert len(pair_counts)==156*155//2 and set(pair_counts.values())=={6}
    for l in ls:
        pencil=[h for h in hs if set(l)<=set(h)]
        assert len(pencil)==6
        multiplicities=Counter(p for h in pencil for p in h)
        assert all(multiplicities[p]==(6 if p in l else 1) for p in range(len(pg)))

    # Exact local inequalities in the final extension argument.
    assert 73+5*4>12+5*16
    assert 74+5*4>13+5*16
    second_arc_plane_sizes=(1,9,10,11,14,15,16)
    assert {(16-m)%5 for m in second_arc_plane_sizes}=={0,1,2}
    assert (16-1)%5==0 and (6*16-74)%5==2
    assert 6*74+25>31*15
    assert 74+5*5>6*16
    answer={'status':'FINITE_CHECKS_FOR_UPPER_BOUND_72_PASSED',
      'parameter':'r_5(F_5^3)','bounds':[70,72],
      'planar':json.loads(planar),'projective_points':156,'projective_lines':806,
      'projective_planes':156,'all_projective_pencil_identities_checked':True,
      'known70_verified':results['check_reduction.py']['known70_checked'],
      'exceptional128_marked_points_excluded':len(results['check_exceptional.py']['marked_points']),
      'lifted_cases_all_excluded_or_full_support':True,
      'full_support_branch':'excluded by the written strong2-dual extension argument',
      'solver_verdict_used':False,
      'external_premises':['Elsholtz et al. Theorem1.5: r_5(F_5^3)<=73',
        'Kurz–Landjev–Rousseva Theorem5.2 and Tables4–7: strong3-arc classification',
        'Kurz–Landjev–Rousseva Theorem3.9: strong2-arcs have full-plane support'],
      'proof_assistant_formalization':False}
    (args.out/'verified.json').write_text(json.dumps(answer,indent=2)+'\n')
    metadata={'seconds':time.monotonic()-started,'python':sys.version,
      'compiler':subprocess.check_output(['g++','--version'],text=True).splitlines()[0]}
    (args.out/'run_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(json.dumps(answer,indent=2))

if __name__=='__main__':main()
