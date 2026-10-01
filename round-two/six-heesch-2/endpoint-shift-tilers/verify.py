"""Solver-free checks of the periodic formulas and one six-disc certificate."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import resource
import time

from tilings import affine, periods, poses, predicted_first_cluster, prototype, quotient, require
from coronas import coronas, component, holes, isometry

HERE=Path(__file__).resolve().parent


def sha(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':'),sort_keys=True).encode()).hexdigest()


def independent_tiling(k, motions, basis):
    """Direct lattice-difference membership, independent of quotient()."""
    tile=prototype(k)
    (a,b),(c,d)=basis
    det=a*d-b*c
    require(det!=0 and abs(det)==len(motions)*len(tile), 'Wrong fundamental area')
    points=[]
    for g in motions:
        require(isometry(g), 'The motif uses a nonisometric motion')
        points.extend(affine(tile,g))
    for i,(x,y) in enumerate(points):
        for u,v in points[:i]:
            dx,dy=x-u,y-v
            require((d*dx-c*dy)%det!=0 or (a*dy-b*dx)%det!=0,
                    'Two motif cells occupy the same lattice coset')
    # Equal area and no repeated coset imply all grid cells are covered once.
    return len(points)


def rejection_control(function):
    try:
        function()
    except ValueError:
        return 1
    raise ValueError('Malformed control unexpectedly passed')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--max-k',type=int,default=64)
    args=parser.parse_args()
    require(1<=args.max_k<=64, 'The documented sanity-check range is 1..64')
    start=time.monotonic()
    summaries=[]
    for k in range(1,args.max_k+1):
        tile=prototype(k)
        require(component(tile,min(tile))==set(tile) and not holes(tile), 'Invalid prototype topology')
        gs=poses(k)
        cluster=[q for g in gs[:3] for q in affine(tile,g)]
        actual=tuple({z for x,z in (quotient(q,k) for q in cluster) if x==r} for r in (0,1))
        expected=predicted_first_cluster(k)
        require(actual==expected and sum(map(len,actual))==len(cluster), 'Symbolic first-cluster table mismatch')
        residues=[quotient(q,k) for g in gs for q in affine(tile,g)]
        require(len(set(residues))==len(residues)==6*len(tile), 'Explicit six-copy quotient tiling failed')
        points=independent_tiling(k,gs,periods(k))
        summaries.append([k,len(tile),points,sha(residues)])
    certificate=json.loads((HERE/'six-disc-k4.json').read_text())
    require(certificate['parameter']==4 and certificate['claim']=='six strict disc coronas; plane tiler',
            'Wrong positive certificate scope')
    raw_to_canonical=(0,-1,-1,0,5,-7)
    require(tuple(map(tuple,certificate['tile']))==affine(prototype(4),raw_to_canonical),
            'The six-disc prototype is not P4')
    stats=coronas(certificate['tile'],certificate['placements'])
    require(stats==certificate['coronas'] and max(r['level'] for r in stats)==6, 'Six-disc counts mismatch')
    controls=0
    controls+=rejection_control(lambda:prototype(0))
    controls+=rejection_control(lambda:independent_tiling(4,poses(4),((2,5),(0,58))))
    controls+=rejection_control(lambda:independent_tiling(4,poses(4)[:-1],periods(4)))
    duplicated=list(poses(4));duplicated[-1]=duplicated[0]
    controls+=rejection_control(lambda:independent_tiling(4,duplicated,periods(4)))
    shifted=list(poses(4));g=list(shifted[1]);g[4]+=1;shifted[1]=tuple(g)
    controls+=rejection_control(lambda:independent_tiling(4,shifted,periods(4)))
    stretched=list(poses(4));stretched[0]=(2,0,0,1,0,0)
    controls+=rejection_control(lambda:independent_tiling(4,stretched,periods(4)))
    deleted=copy.deepcopy(certificate['placements']);deleted.pop(next(i for i,r in enumerate(deleted) if r['level']==1))
    controls+=rejection_control(lambda:coronas(certificate['tile'],deleted))
    gap=copy.deepcopy(certificate['placements'])
    for row in gap:
        if row['level']==6:row['level']=7
    controls+=rejection_control(lambda:coronas(certificate['tile'],gap))
    repeated=copy.deepcopy(certificate['placements']);repeated.append(copy.deepcopy(repeated[-1]))
    controls+=rejection_control(lambda:coronas(certificate['tile'],repeated))
    evidence={'agent':'six-heesch-2','role':'researcher','parameter_checks':args.max_k,
              'parameter_range':[1,args.max_k], 'infinite_claim':'Written symbolic quotient proof; finite checks are sanity checks',
              'first_cluster_and_lattice_difference_checks':True,'six_disc_k4':stats,
              'six_disc_k4_sha256':sha(certificate),'summary_sha256':sha(summaries),
              'malformed_controls':controls,'plane_tiling':True,'finite_heesch_record_claim':False}
    expected_file=HERE/'expected.json'
    if args.max_k==64 and expected_file.exists():
        require(json.loads(expected_file.read_text())==evidence, 'Expected deterministic evidence differs')
    print(json.dumps({'evidence':evidence,'evidence_sha256':sha(evidence),
                      'seconds':round(time.monotonic()-start,3),
                      'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))


if __name__=='__main__':
    main()
