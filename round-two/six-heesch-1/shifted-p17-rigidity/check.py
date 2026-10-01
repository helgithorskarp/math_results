"""Solver-free checker for the stated finite P17 mask/pose rigidity lemma."""
import argparse
import copy
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
from model import (HERE,ROOT,require,load,compile_formula,scaled_cells,dimacs,RupChecker)
from contact import Tile, halo


def validate(data, source):
    require(data['scale']==2 and data['width']==12 and data['height']==10 and
            data['anchor']==[2,0], 'changed problem scope')
    require(data['shifts']==[list(s) for s in sorted(product((-1,0,1),repeat=2))],
            'changed pose-option family')
    require(sorted(map(tuple,data['cells']))==sorted(map(tuple,source['cells'])),
            'changed source prototype')
    tile = Tile(data['cells'])
    expected = []
    for level,o,x,y in source['known_three_corona_poses']:
        require(len(tile.frames[o])==1, 'source frame is not unique')
        g,b = tile.frames[o][0]
        expected.append([level,list(g),[int(x+b[0]),int(y+b[1])]])
    require(data['base_network']==expected, 'physical source poses changed')
    require(expected[0]==[0,[1,0,0,1],[0,0]],'root is not identity')
    return tile


def square_image(mask,g,t):
    """Transform four geometric vertices of each cell; avoid model.image()."""
    a,b,c,d = g
    result = set()
    for x,y in mask:
        vs = [(a*(x+i)+b*(y+j)+t[0],c*(x+i)+d*(y+j)+t[1])
              for i,j in product((0,1),repeat=2)]
        lo = min(u for u,v in vs),min(v for u,v in vs)
        require(set(vs)=={(lo[0]+i,lo[1]+j) for i,j in product((0,1),repeat=2)},
                'motion is not a unit-square isometry')
        result.add(lo)
    require(len(result)==len(mask),'motion collapsed cells')
    return result


def control_geometry(data,tile,source,corners):
    n = data['scale']
    mask = scaled_cells(data)
    footprints = []
    for (level,g,t),row in zip(data['base_network'],source['known_three_corona_poses']):
        physical = square_image(mask,g,(n*t[0],n*t[1]))
        expected = {(n*x+i,n*y+j) for x,y in tile.pixels(tuple(row[1:]),1)
                    for i,j in product(range(n),repeat=2)}
        require(physical==expected,'scaled literal/physical footprints differ')
        footprints.append(physical)
    require(all(a.isdisjoint(b) for a,b in combinations(footprints,2)),
            'whole control copies overlap')
    stats,old = [],set()
    for k in range(4):
        prefix = set().union(*(fp for row,fp in zip(data['base_network'],footprints)
                              if row[0]<=k))
        require(corners.disc(prefix),'control prefix is not a closed disc')
        if k:
            require(halo(old)<=prefix,'control prefix is not strictly surrounded')
            # Separate vertex/cell test of the eight-neighbor collar.
            require(all((x+dx,y+dy) in prefix for x,y in old
                        for dx,dy in product((-1,0,1),repeat=2)),
                    'independent control collar failed')
            for row,fp in zip(data['base_network'],footprints):
                if row[0]==k:
                    require(not halo(fp).isdisjoint(old),'new control copy misses prior prefix')
        stats.append(dict(level=k,copies=sum(r[0]<=k for r in data['base_network']),
                          cells=len(prefix)))
        old = prefix
    return stats


def reject(fn):
    try:
        fn()
    except ValueError:
        return 1
    raise ValueError('malformed control accepted')


def check(dependency_root):
    data = json.loads((HERE/'input.json').read_text())
    for name,digest in json.loads((HERE/'dependencies.json').read_text()).items():
        p = ROOT/name if name.startswith('round-two/six-heesch-1/') else dependency_root/name
        require(hashlib.sha256(p.read_bytes()).hexdigest()==digest,'dependency changed: '+name)
    source = json.loads((ROOT/data['source_input']).read_text())
    tile = validate(data,source)
    Circuit = load(dependency_root/'heesch_polyomino_euler_cnf/circuit.py',
                   'p17_mask_pinned_circuit').Circuit
    corners = load(dependency_root/'heesch_polyomino_corner_obstruction/corners.py',
                   'p17_mask_pinned_disc')
    control = control_geometry(data,tile,source,corners)
    forward,domain,ids,options,maps = compile_formula(data,Circuit)
    inverse,domain2,ids2,options2,maps2 = compile_formula(data,Circuit,inverse=True)
    require(domain==domain2 and ids==ids2 and options==options2 and maps==maps2,
            'forward and inverse geometric incidences differ')
    require(forward.nv==inverse.nv and forward.clauses==inverse.clauses,
            'forward and inverse formulas differ')
    cert = json.loads((HERE/'certificate.json').read_text())
    require(hashlib.sha256(dimacs(inverse)).hexdigest()==cert['cnf_sha256'],
            'compiled formula changed')
    proof = (HERE/'mask.rup').read_text()
    require(len(proof.encode())<=250000,'proof guard; incomplete')
    require(hashlib.sha256(proof.encode()).hexdigest()==cert['proof_sha256'],
            'certificate changed')
    replay = RupChecker(inverse.clauses,inverse.nv).verify(proof)
    require(replay['additions']==cert['RUP_additions'],'RUP additions changed')
    base,_,base_ids,base_options,_ = compile_formula(data,Circuit,exclude_control=False)
    control_mask = scaled_cells(data)
    assignment = {ids[p]:p in control_mask for p in domain}
    assignment.update({o['selected']:o['shift']==(0,0) for o in options if o['copy']})
    require(base.evaluate(assignment),'valid three-corona control fails necessary model')
    bad = copy.deepcopy(data)
    bad['base_network'][1][1]=[1,1,0,1]
    controls = reject(lambda:validate(bad,source))
    full_box = set(domain)
    def false_overlap_control():
        fps = [square_image(full_box,o['matrix'],o['translation']) for o in base_options
               if o['shift']==(0,0)]
        require(all(a.isdisjoint(b) for a,b in combinations(fps,2)),
                'filled-box copies overlap')
    controls += reject(false_overlap_control)
    checker = RupChecker(base.clauses,base.nv)
    require(not checker.rup([-base_ids[tuple(data['anchor'])]])[0],
            'false literal accepted on satisfiable control model')
    controls += 1
    controls += reject(lambda:checker.verify(f'{base.nv+1} 0\n0\n'))
    result = dict(agent='six-heesch-1',role='researcher',scale=2,prototype_pool=len(domain),
                  anchor=data['anchor'],designated_copies=19,pose_options=len(options),
                  shifts_per_nonroot_copy=9,variables=inverse.nv,clauses=len(inverse.clauses),
                  no_area_constraint=True,inverse_incidence_cells=sum(len(d) for d in maps2),
                  RUP_additions=replay['additions'],proof_bytes=len(proof.encode()),
                  control_prefixes=control,rejected_controls=controls,
                  claim='Within the stated pool and 19-copy pose family, two disc coronas force the doubled P17 mask.',
                  scope='Explicit finite family, no arbitrary-placement Heesch bound or new record.')
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dependency-root',type=Path,default=ROOT)
    args = parser.parse_args()
    print(json.dumps(check(args.dependency_root.resolve()),indent=2,sort_keys=True))


if __name__=='__main__':
    main()
