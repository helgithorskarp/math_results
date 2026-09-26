"""Replay the entire finite reduction, independently of all lifting verdicts."""
import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction
import hashlib
from itertools import combinations,product
import json
from pathlib import Path
import subprocess
import sys
import time

from certificate_systems import check_lower_bound,check_unique_low
from evidence import DOMAIN_SHA256
from incidence import system
from point_model import POINTS,decode_and_check,fiber_clauses,generate,geometry
from profile_check import check_profiles
from quotients import classify
from pysat.solvers import Solver

HERE=Path(__file__).resolve().parent
SPECTRA_HASH='8e65bcf9fab9c6a75a83368e3bef7339f9411f58f0231f4a3cbb10209be94bc9'
CATALOGUE_HASH='a6d7af5e3cb1c4b6069892164453fed01da96e7ec1718d2333ace123a6909291'
LABELED=[7264,10252,12000,13797,13789,11464,14565,14565,14565,16844,
         13403,15036,17078,17104,16641,18792,18731,21216,21261,21244]
CANONICAL=[252,2496,2765,2950,1345,2254,2517,2242,2009,1978,
           6555,13621,14022,6556,7543,15200,7038,8481,7841,2011]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_geometry():
    lines,planes=geometry()
    indices={p:i+1 for i,p in enumerate(POINTS)}
    pairs={tuple(sorted(indices[tuple((a+t*(b-a))%5 for a,b in zip(p,q))]
                        for t in range(5))) for p,q in combinations(POINTS,2)}
    if pairs!=set(lines) or len(planes)!=155:
        raise RuntimeError('independent line geometry disagrees')
    plane_sets=[frozenset(h) for h in planes]
    line_sets=set(map(frozenset,lines))
    parallel=0;intersecting=Counter()
    for H,G in combinations(plane_sets,2):
        meet=H&G
        if not meet:parallel+=1
        elif meet in line_sets:intersecting[meet]+=1
        else:raise RuntimeError('invalid intersection of affine planes')
    if parallel!=310 or set(intersecting.values())!={15} or len(intersecting)!=775:
        raise RuntimeError('plane-pair identity does not cover every pair exactly once')
    if set(Counter(v for H in planes for v in H).values())!={31}:
        raise RuntimeError('point-plane incidence count is incorrect')
    if set(Counter(pair for H in planes for pair in combinations(H,2)).values())!={6}:
        raise RuntimeError('pair-plane incidence count is incorrect')
    for line in line_sets:
        pencil=[H for H in plane_sets if line<=H]
        count=Counter(v for H in pencil for v in H)
        if len(pencil)!=6 or any(count[v]!=(6 if v in line else 1) for v in range(1,126)):
            raise RuntimeError('six-plane pencil identity failed')
    for n in range(5):
        clauses=fiber_clauses(list(range(1,6)),n)
        for values in product((False,True),repeat=5):
            actual=all(any(values[abs(v)-1]==(v>0) for v in clause) for clause in clauses)
            if actual!=(sum(values)==n):raise RuntimeError('incorrect direct cardinality clauses')
    return {'lines':775,'planes':155,'parallel_plane_pairs':310,
            'intersecting_plane_pairs':11625,'fiber_truth_assignments':160}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--sanitize',action='store_true')
    args=parser.parse_args();out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    started=time.monotonic()
    dependencies=json.loads((HERE/'dependencies.json').read_text())
    for name,expected_hash in dependencies.items():
        if digest(HERE/name)!=expected_hash:
            raise RuntimeError('imported source/control changed: '+name)
    profiles=check_profiles()
    # A complementary complete bridge discovered by Team A researcher 3.
    # Our fixed twenty-type catalogue contains all fifteen of its pair types.
    teammate_out=out/'low_pair71'
    command=[sys.executable,str(HERE.parent/'low_pair71/verify.py'),'--out',str(teammate_out)]
    if args.sanitize:command.append('--sanitize')
    subprocess.run(command,stdout=subprocess.PIPE,check=True)
    teammate=json.loads((teammate_out/'summary.json').read_text())
    if teammate['status']!='LOW_PAIR71_VERIFIED' or teammate['spectra']!=91:
        raise RuntimeError('teammate low-pair reduction did not verify')
    pair_table=json.loads((HERE/'profiles.json').read_text())['pairs']
    covered=[p for p in pair_table if p[1]<5]
    if [p[:2] for p in teammate['profile_audit']['pair_ranges']]!=covered or len(covered)!=15:
        raise RuntimeError('teammate low-pair cover is not contained in the fixed domain')
    if min(map(Fraction,teammate['certificate_audit']['exact_lower_bounds'].values()))<=1:
        raise RuntimeError('two-low-plane lower bound is insufficient')
    flags=['-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer'] if args.sanitize else ['-O3']
    def compile_program(name):
        executable=out/name
        subprocess.run(['g++','-std=c++20','-Wall','-Wextra','-Wconversion',*flags,
                        str(HERE/(name+'.cpp')),'-o',str(executable)],check=True)
        return executable
    outputs={}
    for name in ['enumerate_spectra','enumerate_spectra_independent','deficit_quotients','row_quotients']:
        executable=compile_program(name);path=out/(name+'.txt')
        with path.open('w') as stream:
            subprocess.run([str(executable)],stdout=stream,stderr=subprocess.PIPE,check=True)
        outputs[name]=path
    if outputs['enumerate_spectra'].read_bytes()!=outputs['enumerate_spectra_independent'].read_bytes():
        raise RuntimeError('the two complete planar spectra disagree')
    if digest(outputs['enumerate_spectra'])!=SPECTRA_HASH:
        raise RuntimeError('planar spectra hash changed')
    spectra=[list(map(int,line.split())) for line in outputs['enumerate_spectra'].read_text().splitlines()]
    if len(spectra)!=91:raise RuntimeError('incomplete planar spectrum domain')
    for s in spectra:
        m=s[0];counts=s[1:6]
        if (not 7<=m<=16 or sum(counts)!=30 or s[6]<=0
            or sum(k*counts[k] for k in range(5))!=6*m
            or sum(k*(k-1)//2*counts[k] for k in range(5))!=m*(m-1)//2):
            raise RuntimeError('invalid enumerated planar spectrum')
    basic=json.loads((HERE/'basic_certificates.json').read_text())
    if [c['cutoff'] for c in basic]!=[9,10]:raise RuntimeError('incomplete basic certificates')
    lower=[check_lower_bound(spectra,c) for c in basic]
    conditional=[]
    for size in (8,9):
        c=json.loads((HERE/f'unique_low_{size}_certificate.json').read_text())
        if c['size']!=size:raise RuntimeError('incorrect conditional certificate')
        conditional.append(check_unique_low(spectra,c))
        broken=deepcopy(c);broken['multipliers']=[0]*len(c['multipliers'])
        try:check_unique_low(spectra,broken)
        except ValueError:pass
        else:raise RuntimeError('invalid Farkas certificate was accepted')
    broken=deepcopy(basic[0]);broken['bound_numerator']+=1
    try:check_lower_bound(spectra,broken)
    except ValueError:pass
    else:raise RuntimeError('altered lower bound was accepted')

    first=outputs['deficit_quotients'];second=outputs['row_quotients']
    if first.read_bytes()!=second.read_bytes() or digest(first)!=CATALOGUE_HASH:
        raise RuntimeError('independent quotient enumeration or hash disagrees')
    keys=[(int(parts[0]),parts[1]) for parts in map(str.split,first.read_text().splitlines())]
    if len(keys)!=309611 or [sum(t==i for t,_ in keys) for i in range(20)]!=LABELED:
        raise RuntimeError('incorrect complete typed catalogue')
    representatives=classify(keys)
    if len(representatives)!=109676 or [sum(r['type']==i for r in representatives) for i in range(20)]!=CANONICAL:
        raise RuntimeError('incorrect complete canonical catalogue')
    domain=out/'orbits.json'
    domain.write_text('[\n'+',\n'.join(json.dumps(r,separators=(',',':')) for r in representatives)+'\n]\n')
    if digest(domain)!=DOMAIN_SHA256:
        raise RuntimeError('generated representative domain differs from proof input')
    plain=out/'representatives.txt'
    plain.write_text(''.join(str(r['type'])+' '+r['weights']+' '+str(r['orbit_size'])+'\n' for r in representatives))
    affine=compile_program('full_affine_check')
    affine_result=json.loads(subprocess.check_output([str(affine),str(first),str(plain)],text=True))
    if affine_result!={'status':'FULL_AFFINE_PARTITION_VERIFIED','maps_per_representative':12000,
                       'representatives':109676,'typed_matrices':309611}:
        raise RuntimeError('full affine-group verification failed')
    geometry_result=verify_geometry()
    # The domain generator itself checks every gauge, including the interior bound.
    for r in representatives:
        word=r['weights'];full=[i for i,c in enumerate(word) if c=='4']
        if len(full)<5 or not any(((b//5-a//5)*(c%5-a%5)-(c//5-a//5)*(b%5-a%5))%5
                                  for a,b,c in combinations(full,3)):
            raise RuntimeError('missing three-hole affine gauge')
    controls=[]
    for name in ('known70.json','odd_symmetry/witness70.json','affine_asymmetry71/witness70.json'):
        points=json.loads((HERE.parent/name).read_text())['points']
        word=''.join(str(sum(v//5==i for v in points)) for i in range(25))
        if len(decode_and_check(word,[v+1 for v in points]))!=70:
            raise RuntimeError('incorrect construction control')
        formula,_=generate(word)
        with Solver(name='cadical195',bootstrap_with=formula.clauses) as solver:
            if not solver.solve() or len(decode_and_check(word,solver.get_model()))!=70:
                raise RuntimeError('the direct model rejected a known70 lift')
        controls.append(name)
    columns,names,matrix,rhs=system(spectra)
    result={'status':'COMPLETE_71_POINT_REDUCTION_VERIFIED','spectra':91,'incidence_rows':len(matrix),
            'incidence_columns':len(columns),'low_plane_certificates':lower,'unique_low_exclusions':conditional,
            'profile_normalization':profiles,'typed_quotients':309611,'canonical_classes':109676,
            'labeled_counts_by_type':LABELED,'canonical_counts_by_type':CANONICAL,
            'spectra_sha256':SPECTRA_HASH,'catalogue_sha256':CATALOGUE_HASH,'domain_sha256':digest(domain),
            'full_affine_group':affine_result,'geometry':geometry_result,'positive70_controls':controls,
            'teammate_low_pair71':{'status':teammate['status'],
                'certificate_sha256':teammate['certificate_audit']['certificate_sha256'],
                'covered_pair_types':15,'total_enumerated_pair_types':20},
            'damaged_certificates_rejected':3,'proofs_rechecked':False,
            'scope':'The complete finite reduction is verified. Run replay.py to discharge every lift obligation.'}
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    (out/'timing.json').write_text(json.dumps({'seconds':time.monotonic()-started,'sanitize':args.sanitize},indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
