#!/usr/bin/env python3
"""Unpublished next-domain generator: X20, Y18, lambda4, four fixed Y words.

This selected subfamily does not cover every70-word code. Generated anchors
remain private. No residual clique exclusion or independent census is claimed.
"""
from pathlib import Path
from hashlib import sha256
import argparse
import json
import sys
import time
SOURCE = Path(__file__).resolve().parent.parent / 'two_fixed_saturated_upper60'
sys.path.insert(0,str(SOURCE))
import model as M
import seeds
import second_stars as S


def run(output):
    M.require(not output.exists(),'use new inventory output')
    roots,_ = seeds.root_cases()
    resources,rows = M.orbit_carrier()
    records,anchors = [],[]
    started = time.monotonic()
    for root in roots:
        domains = seeds.y_domains(root['anchor'],resources,rows)['configurations']
        for j,c in enumerate(domains):
            fives,nodes = S.cliques(c['adjacency'],5)
            sizes = []
            for q in fives:
                words = tuple(sorted(root['anchor']+c['fixed_words']+
                                     tuple(w for i in q for w in c['rows'][i]['words'])))
                stats = M.check_code(words)
                M.require(len(words)==34 and stats['replications'][16:]==(20,18) and
                          stats['fixed_words']==8,'bad positive34-word anchor')
                leftover = tuple(r for r in M.residual(words,resources,rows) if r['replications'][16:]==(0,0))
                M.require(all(r['weight']==2 for r in leftover),'free residual orbit')
                sizes.append(len(leftover))
                anchors.append(dict(case=len(anchors),fixture=root['fixture'],matching=j,five=q,
                                    words=words,finite_residual_orbits=len(leftover)))
            records.append(dict(fixture=root['fixture'],matching=j,anchors34=len(fives),nodes=nodes,
                                min_finite_orbits=min(sizes,default=0),max_finite_orbits=max(sizes,default=0)))
    M.require(len(anchors)==392 and len({tuple(r['words']) for r in anchors})==392,'complete positive-anchor count')
    result=dict(agent='six-code-2',role='researcher',status='COMPLETE scoped positive-anchor inventory',
                scope='g2^8*1^2, X20, Y18, lambdaXY4, four fixed Y words; selected subfamily',
                residual_search_status='NOT RUN; no70 exclusion',records=records,anchors=anchors,
                anchors_sha256=sha256(M.encoded(anchors)).hexdigest(),
                target_residual_clique=18,finite_pair_deficit_sum_at70=4,
                deficit_compositions=330,seconds=time.monotonic()-started)
    output.write_bytes(M.encoded(result))
    best=max(anchors,key=lambda r:r['finite_residual_orbits'])
    print(json.dumps(dict(status=result['status'],anchors=len(anchors),
                          max_residual_orbits=best['finite_residual_orbits'],best_case=best['case'],
                          best_fixture=best['fixture'],best_matching=best['matching'],
                          anchors_sha256=result['anchors_sha256'],seconds=result['seconds']),sort_keys=True))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    run(p.parse_args().output)
