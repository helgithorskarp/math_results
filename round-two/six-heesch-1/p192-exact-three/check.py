"""Solver-free exact-three reader, with independent finite inventories."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import time
import phase
from upper import Geometry,Cover,disc,halo,require

HERE=Path(__file__).resolve().parent


def reject(call):
    try:call()
    except ValueError:return 1
    raise ValueError('false or malformed control accepted')


def catalog(raw):
    return {tuple(sorted(tuple(p) for p in star)) for star in raw}


def lower(g,levels):
    require(levels and levels[0]==[list(g.root)],'wrong lower root')
    old=[];statistics=[]
    for k,raw in enumerate(levels):
        added=[tuple(p) for p in raw];previous=g.union(old) if old else set()
        occupied=g.union(old+added)
        if k:
            require(halo(previous)<=occupied,'lower collar incomplete')
            require(all(g.pixels(p)&halo(previous) for p in added),'lower copy misses preceding prefix')
        require(disc(occupied),'lower prefix is not a closed disc')
        statistics.append(dict(level=k,copies=len(old)+len(added),cells=len(occupied)))
        old+=added
    return statistics


def check(progress=False):
    started=time.monotonic()
    data=json.loads((HERE/'input.json').read_text());cert=json.loads((HERE/'certificate.json').read_text())
    phase_result=phase.check()
    g=Geometry(data['cells'])
    require(g.shapes==phase.Tile(data['cells']).orientations,'independent orientation conventions disagree')
    lower_stats=lower(g,data['known_levels'])
    require(len(lower_stats)==4,'missing three-corona witness')
    require(len(g.integer_contacts)==352,'changed integer contact inventory')
    bad={tuple(r['pose']) for r in cert['corner_pairs']}
    require(len(bad)==len(cert['corner_pairs'])==209 and bad<=g.integer_contacts,'invalid corner-pair catalog')
    forced=0
    for record in cert['corner_pairs']:forced+=g.corner([g.root,tuple(record['pose'])],record)
    require(all(g.relative(p,g.root) in bad for p in bad),'nonreciprocal excluded pairs')
    # Check cached integer transport against the separately pinned exact frame.
    t=phase.Tile(data['cells'])
    for ao in range(len(g.shapes)):
        for bo in range(len(g.shapes)):
            a=(ao,2,-3);b=(bo,-4,6);r=g.relative(a,b)
            require(t.relative_type(a,b)==(r[0],2*r[1],2*r[2]),'relative isometry audit failed')
    for a in [(o,2,-3) for o in range(len(g.shapes))]:
        for p in g.integer_contacts-bad:require(g.relative(a,g.transport(a,p))==p,'transport inverse failed')
    root_model=Cover(g,[g.root],bad)
    first_catalog=cert['first_stars'];actual_first=root_model.enumerate()
    require(actual_first==catalog(first_catalog) and len(actual_first)==len(first_catalog)==310,'incomplete or duplicate first catalog')
    first_bad={r['index']:r for r in cert['first_corner_exclusions']}
    require(len(first_bad)==len(cert['first_corner_exclusions'])==159 and set(first_bad)<=set(range(len(first_catalog))),'invalid first exclusions')
    second_catalog=cert['second_stars']
    require(all(str(j) not in second_catalog for j in first_bad),'second catalog indexed an excluded first star')
    cover_nodes=root_model.nodes;second_count=0;second_negative=0
    fixed_seconds={}
    for j,star in enumerate(first_catalog):
        require(time.monotonic()-started<90,'wall guard; incomplete verification')
        fixed=[g.root]+[tuple(p) for p in star]
        if j in first_bad:
            forced+=g.corner(fixed,first_bad[j]);continue
        model=Cover(g,fixed,bad);answers=model.enumerate();cover_nodes+=model.nodes
        supplied=second_catalog.get(str(j),[])
        require(answers==catalog(supplied) and len(answers)==len(supplied),'incomplete or duplicate second catalog')
        if not answers:second_negative+=1
        second_count+=len(answers)
        for k,second in enumerate(supplied):fixed_seconds[j,k]=fixed+[tuple(p) for p in second]
        if progress and j%25==0:print('checked first-prefix lift',j,flush=True)
    require(len(second_catalog)==23 and second_count==276 and second_negative==128,'changed second-prefix inventory')
    second_bad={(r['first'],r['second']):r for r in cert['second_corner_exclusions']}
    require(len(second_bad)==len(cert['second_corner_exclusions'])==232 and set(second_bad)<=set(fixed_seconds),'invalid second exclusions')
    third_negative=0
    for key,fixed in fixed_seconds.items():
        require(time.monotonic()-started<90,'wall guard; incomplete verification')
        if key in second_bad:forced+=g.corner(fixed,second_bad[key]);continue
        model=Cover(g,fixed,bad);answers=model.enumerate(first_only=True);cover_nodes+=model.nodes
        require(not answers,'a third interior cover survived: no exact-three proof')
        third_negative+=1
    require(third_negative==44,'incomplete final rejection coverage')
    controls=0
    controls+=reject(lambda:require(actual_first==catalog(first_catalog[:-1]),'missing first case'))
    unique=217
    fixed=[g.root]+[tuple(p) for p in first_catalog[unique]]
    controls+=reject(lambda:require(not Cover(g,fixed,bad).enumerate(),'missing second case'))
    for record in cert['corner_pairs']:
        if record['steps']:
            damaged=deepcopy(record);damaged['steps'].pop()
            try:g.corner([g.root,tuple(record['pose'])],damaged)
            except ValueError:
                controls+=1;break
    else:raise ValueError('no damaged corner control rejected')
    old=[tuple(p) for level in data['known_levels'][:3] for p in level]
    final=[tuple(p) for p in data['known_levels'][3]]
    relaxed=Cover(g,old,set())
    controls+=reject(lambda:require(not relaxed.accepts(final),'false rejection of the genuine third corona'))
    result=dict(agent='six-heesch-1',role='researcher',seed_cells=17,primary_zero_based_index=192,Hc=3,Hh=3,plane_tiling_excluded=True,
                motions='All Euclidean rigid motions and reflections',lower_prefixes=lower_stats,
                phase_RUP_additions=phase_result['RUP_additions'],floating_first_support=phase_result['floating_first_support'],reciprocal_floating_support=0,
                integer_pair_exclusions=len(bad),first_surrounds=len(actual_first),first_corner_exclusions=len(first_bad),second_cover_rejections=second_negative,
                second_surrounds=second_count,second_corner_exclusions=len(second_bad),third_cover_rejections=third_negative,
                corner_forced_steps=forced,independent_cover_search_nodes=cover_nodes,rejected_controls=controls+phase_result['rejected_controls'],
                scope='Matches the published grid value under arbitrary motions; no new shape or Heesch record. Unformalized author proof, independent review pending.')
    expected=HERE/'expected.json'
    if expected.exists():require(result==json.loads(expected.read_text()),'expected output mismatch')
    return result


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--progress',action='store_true')
    args=ap.parse_args();print(json.dumps(check(args.progress),indent=2,sort_keys=True))


if __name__=='__main__':main()
