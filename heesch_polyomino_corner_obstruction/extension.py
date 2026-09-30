"""Exact one-step half-grid extension of a specified integer-cell disc prefix.

The mathematical equivalence is the published fixed-prefix corollary. A
negative result excludes only this specified prefix, not every corona of P.
Generated CNF, native proofs and checked placements stay in the chosen scratch directory.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'heesch_polyomino_halfgrid'))
from halfgrid import encode_poses, load_dependencies

SEED_SHA = '24ceb5aefe2e0843d16d7ab7ced16f17356789426a12607b00cf956df02dbe51'
WITNESS_SHA = 'c5f4c30ceff27b40a39ef006960b7b5de22489c52e71b429196d1f51cdc32f04'


def checked_cells(raw):
    cells = [tuple(p) for p in raw]
    if (not cells or len(cells)!=len(set(cells))
            or any(len(p)!=2 or any(type(x) is not int for x in p) for p in cells)):
        raise ValueError('nonempty distinct integer cell pairs required')
    return tuple(sorted(cells))


def scale_cells(cells, factor=2):
    if type(factor) is not int or factor<1:
        raise ValueError('positive integer scale required')
    return tuple(sorted((factor*x+dx, factor*y+dy) for x,y in checked_cells(cells)
                        for dx in range(factor) for dy in range(factor)))


def seed_prefix(prior, motion, level):
    if type(level) is not int or not 0<=level<=3:
        raise ValueError('published prefix level must be zero through three')
    for name, digest in (('kaplan17.json',SEED_SHA),('kaplan17_depth3.witness.json',WITNESS_SHA)):
        if hashlib.sha256((prior/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('published seed input changed')
    tile = motion.normalize(json.loads((prior/'kaplan17.json').read_text())['cells'])
    patch = [p for p in json.loads((prior/'kaplan17_depth3.witness.json').read_text())['patch']
             if p['level']<=level]
    poses = []
    for record in patch:
        cells = checked_cells(record['cells'])
        tx,ty = min(x for x,y in cells), min(y for x,y in cells)
        poses.append(motion.Pose(record['level'],motion.normalize(cells),Fraction(tx),Fraction(ty)))
    rational = motion.check_corona(tile,level,poses,holes_last=False)
    from corona import check_witness
    pixels = check_witness(tile,level,patch,strict_disc=True,holes_last=False)
    union = tuple(sorted({p for pose in poses for p in pose.squares()}))
    if any(x.denominator!=1 or y.denominator!=1 for x,y in union):
        raise ValueError('seed prefix is not integral')
    union = tuple((int(x),int(y)) for x,y in union)
    return tile,poses,union,{'rational_prefixes':rational,'pixel_prefixes':pixels}


def integer_prefix(path, motion):
    """Read an exact independently checked disc-corona certificate."""
    from corona import check_witness
    data=json.loads(path.read_text())
    tile=motion.normalize(checked_cells(data['cells']))
    level=data['depth']
    if type(level) is not int or level<0 or type(data['last_prefix_relaxed']) is not bool:
        raise ValueError('a corona certificate with nonnegative depth is required')
    if 'pose_codes' in data:
        shapes=tuple(sorted(motion.variants(tile)))
        records=[]
        for code in data['pose_codes']:
            if len(code)!=4 or any(type(x) is not int for x in code) or not 0<=code[1]<len(shapes):
                raise ValueError('invalid compact integral pose code')
            records.append({'level':code[0],'shape':shapes[code[1]],'translation':code[2:]})
    else:
        records=data['placements']
    poses=motion.load_poses(tile,records)
    if any(p.tx.denominator!=1 or p.ty.denominator!=1 for p in poses):
        raise ValueError('this driver requires an integer prefix; rational scale not implemented')
    rational=motion.check_corona(tile,level,poses,holes_last=False)
    enlarged,records=motion.rasterize(tile,poses)
    pixels=check_witness(enlarged,level,records,strict_disc=True,holes_last=False)
    root=tuple(sorted({(int(x),int(y)) for p in poses for x,y in p.squares()}))
    return tile,poses,root,level,{'rational_prefixes':rational,'pixel_prefixes':pixels,
                                'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}


def inventory(root,tile,cover,motion,max_candidates=10000):
    """Bounding-box enumeration, retaining every full footprint meeting R1."""
    from corona import orientations,normalize
    root = set(checked_cells(root))
    tile = normalize(checked_cells(tile))
    if not motion.boundary_disc(root)['disc'] or not motion.boundary_disc(set(tile))['disc']:
        raise ValueError('root and neighbor tile must each be discs')
    halo = cover.dilation(root,1)-root
    target = root|halo
    xmin,xmax = min(x for x,y in target),max(x for x,y in target)
    ymin,ymax = min(y for x,y in target),max(y for x,y in target)
    candidates = []
    variants = orientations(tile)
    covers = {}
    for shape in variants:
        width,height = max(x for x,y in shape),max(y for x,y in shape)
        for tx in range(xmin-width,xmax+1):
            for ty in range(ymin-height,ymax+1):
                cells = tuple((x+tx,y+ty) for x,y in shape)
                if root.intersection(cells) or not halo.intersection(cells):
                    continue
                if len(candidates)>=max_candidates:
                    raise RuntimeError('candidate guard; incomplete enumeration')
                # Circuit variable1 is the pinned true constant.
                z = len(candidates)+2
                candidates.append({'shape':shape,'tx':tx,'ty':ty,'cells':cells,'variable':z})
                for cell in cells:
                    covers.setdefault(cell,[]).append(z)
    serialized = json.dumps([[q['shape'],q['tx'],q['ty']] for q in candidates],separators=(',',':'))
    missing = sorted(p for p in halo if p not in covers)
    stats = {'root_cells':len(root),'tile_cells':len(tile),'target_cells':len(target),
             'required_halo_cells':len(halo),'candidates':len(candidates),
             'orientations':len(variants),'full_footprint_cells':len(root|set(covers)),
             'candidate_sha256':hashlib.sha256(serialized.encode()).hexdigest(),
             'uncoverable_halo_cells':missing,
             'halo_owner_counts':dict(sorted(Counter(len(covers.get(p,())) for p in halo).items()))}
    return candidates,halo,covers,stats


def independent_inventory(root,tile,motion):
    """Inverse distance-one test and translation joins, with no box cutoff."""
    root = set(root)
    xmin,xmax = min(x for x,y in root)-1,max(x for x,y in root)+1
    ymin,ymax = min(y for x,y in root)-1,max(y for x,y in root)+1
    halo = {(x,y) for x in range(xmin,xmax+1) for y in range(ymin,ymax+1)
            if (x,y) not in root and any((x+dx,y+dy) in root
                for dx in (-1,0,1) for dy in (-1,0,1))}
    result = set()
    for shape in motion.variants(tile):
        translations = {(x-a,y-b) for x,y in halo for a,b in shape}
        for tx,ty in translations:
            if any((a+tx,b+ty) in root for a,b in shape):
                continue
            result.add((shape,tx,ty))
    return halo,result


def build_formula(candidates,halo,covers,max_clauses=2000000):
    from circuit import Circuit
    from corona import at_most_one
    circuit = Circuit()
    for q in candidates:
        if circuit.new()!=q['variable']:
            raise RuntimeError('primary variable order changed')
    for p in sorted(halo):
        circuit.clause(covers.get(p,()))
    for p in sorted(covers):
        at_most_one(circuit,covers[p])
        if len(circuit.clauses)>max_clauses:
            raise RuntimeError('formula guard; incomplete build')
    return circuit


def check_fixed_cover(root,tile,chosen,motion):
    """Definition-level check independent of candidate/CNF construction."""
    root = set(root);occupied = set(root);variants = motion.variants(tile)
    for q in chosen:
        cells = set(q['cells'])
        if len(cells)!=len(tile) or motion.normalize(cells) not in variants:
            raise ValueError('invalid neighbor congruence')
        if cells&occupied:
            raise ValueError('overlap on full footprint')
        if not any((x+dx,y+dy) in root for x,y in cells for dx in (-1,0,1) for dy in (-1,0,1)):
            raise ValueError('neighbor does not touch fixed prefix')
        occupied.update(cells)
    halo,_ = independent_inventory(root,tile,motion)
    if not halo<=occupied:
        raise ValueError('incomplete fixed-prefix surrounding')
    return {'neighbors':len(chosen),'occupied_cells':len(occupied)}


def solve(tile,poses,candidates,halo,covers,stats,level,motion,work,checker):
    from pysat.solvers import Solver
    from pysat import __version__
    from corona import check_witness
    circuit = build_formula(candidates,halo,covers)
    formula,trace = work/'extension.cnf',work/'extension.drat'
    circuit.write_dimacs(formula)
    stats.update({'variables':circuit.nv,'clauses':len(circuit.clauses),
                  'cnf_sha256':hashlib.sha256(formula.read_bytes()).hexdigest(),
                  'python_sat':__version__,'conflict_budget':10000})
    with Solver(name='glucose4',bootstrap_with=circuit.clauses,with_proof=True) as solver:
        solver.conf_budget(10000)
        start = time.monotonic();sat = solver.solve_limited()
        stats['solve_seconds']=round(time.monotonic()-start,3)
        stats['solver_statistics']=solver.accum_stats()
        if sat is None:
            stats['result']='UNKNOWN; specified extension unresolved'
        elif sat:
            positive = {x for x in solver.get_model() if x>0}
            chosen = [q for q in candidates if q['variable'] in positive]
            root = {cell for pose in poses for cell in scale_cells([(int(x),int(y)) for x,y in pose.squares()])}
            stats['fixed_cover']=check_fixed_cover(root,scale_cells(tile),chosen,motion)
            unscaled = {scale_cells(s):s for s in motion.variants(tile)}
            extended = poses+[motion.Pose(level+1,unscaled[q['shape']],Fraction(q['tx'],2),Fraction(q['ty'],2))
                              for q in chosen]
            relaxed = motion.check_corona(tile,level+1,extended,holes_last=True)
            enlarged,records = motion.rasterize(tile,extended)
            pixel = check_witness(enlarged,level+1,records,holes_last=True)
            stats.update({'result':'SAT; complete relaxed extension checked twice',
                          'rational_prefixes':relaxed,'pixel_prefixes':pixel,
                          'fractional_new_copies':sum(bool(p.tx%1 or p.ty%1) for p in extended if p.level==level+1)})
            certificate = {'cells':tile,'depth':level+1,'last_prefix_relaxed':True,
                           'placements':encode_poses(extended)}
            (work/'witness.json').write_text(json.dumps(certificate,sort_keys=True,indent=2)+'\n')
        else:
            trace.write_text('\n'.join(solver.get_proof() or ['0'])+'\n')
            stats.update({'result':'UNSAT; not yet checked',
                          'proof_sha256':hashlib.sha256(trace.read_bytes()).hexdigest(),
                          'proof_bytes':trace.stat().st_size})
    if sat is False:
        env=os.environ.copy()
        for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
            env[name]='1'
        checked=subprocess.run([str(checker.resolve()),str(formula),str(trace)],
                               capture_output=True,text=True,timeout=30,env=env)
        log=checked.stdout.replace('\r','\n')
        (work/'checker.log').write_text(log+checked.stderr)
        if checked.returncode not in (0,1) or 's VERIFIED' not in log.splitlines():
            raise RuntimeError('specified-extension contradiction not verified')
        stats['result']='UNSAT VERIFIED; this fixed prefix has no real relaxed next corona'
    return stats


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--level',type=int,default=3)
    p.add_argument('--work-dir',type=Path,required=True)
    p.add_argument('--checker',type=Path)
    p.add_argument('--inventory-only',action='store_true')
    p.add_argument('--prefix',type=Path,help='use a checked integer disc-prefix certificate')
    args=p.parse_args()
    prior=ROOT/'heesch_polyomino_euler_cnf'
    cover,motion=load_dependencies(prior,ROOT/'heesch_polyomino_motion_bridge')
    work=args.work_dir.resolve();work.mkdir(parents=True,exist_ok=True)
    start=time.monotonic()
    if args.prefix:
        tile,poses,root,args.level,baseline=integer_prefix(args.prefix,motion)
    else:
        tile,poses,root,baseline=seed_prefix(prior,motion,args.level)
    scaled_root,scaled_tile=scale_cells(root),scale_cells(tile)
    candidates,halo,covers,stats=inventory(scaled_root,scaled_tile,cover,motion)
    halo2,independent=independent_inventory(scaled_root,scaled_tile,motion)
    actual={(q['shape'],q['tx'],q['ty']) for q in candidates}
    if halo!=halo2 or actual!=independent:
        raise RuntimeError('independent candidate inventory disagrees')
    stats.update({'agent':'six-heesch-1','role':'researcher','fixed_prefix_depth':args.level,
                  'old_copies':len(poses),'old_physical_cells':len(root),
                  'independent_inventory_exact_match':True,'baseline':baseline,
                  'inventory_seconds':round(time.monotonic()-start,3)})
    (work/'inventory.json').write_text(json.dumps(stats,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in stats.items() if k not in ('baseline','halo_owner_counts')},sort_keys=True,indent=2),flush=True)
    if not args.inventory_only:
        if args.checker is None:p.error('negative claims require --checker')
        stats=solve(tile,poses,candidates,halo,covers,stats,args.level,motion,work,args.checker)
    stats.update({'total_seconds':round(time.monotonic()-start,3),
                  'peak_self_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
    (work/'result.json').write_text(json.dumps(stats,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in stats.items() if k not in ('baseline','halo_owner_counts')},
                     sort_keys=True,indent=2),flush=True)


if __name__=='__main__':
    main()
