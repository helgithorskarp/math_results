"""Solver-free P192 interior-integrality certificate reader."""
from copy import deepcopy
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
GENERIC=HERE.parent/'finite-contact-types'
sys.path.insert(0,str(GENERIC))
from contact import Tile,require,check_patch
from local import compile_cnf,dimacs
from audit import audit_pool
from rup import RupChecker
from reader import strict_rectangles


def reject(call):
    try:call()
    except ValueError:return 1
    raise ValueError('false or malformed control accepted')


def support_units(cnf,nv,proof):
    checker=RupChecker(cnf,nv)
    for line in proof.splitlines():
        values=list(map(int,line.split()))
        require(values and values[-1]==0 and 0 not in values[:-1],'bad proof terminator')
        clause=values[:-1]
        require(checker.rup(clause)[0],'non-RUP support step')
        checker.add(clause)
    return {c[0] for c in checker.clauses if len(c)==1}


def witness_support(tile,lookup,witnesses):
    found=set()
    for raw in witnesses:
        poses=[(o,Q(x,2),Q(y,2)) for o,x,y in raw]
        require(poses and poses[0]==tile.root,'witness has wrong root')
        require(all(p in lookup for p in poses[1:]),'noncandidate witness copy')
        check_patch(tile,[tile.root],poses,scale=2)
        require(strict_rectangles(tile,[tile.root],poses),'witness has no exact collar')
        found.update((o,int(2*x),int(2*y)) for o,x,y in poses[1:] if x%1 or y%1)
    return found


def check():
    data=json.loads((HERE/'input.json').read_text())
    cert=json.loads((HERE/'certificate.json').read_text())
    for name,digest in json.loads((HERE/'dependencies.json').read_text()).items():
        require(hashlib.sha256((GENERIC/name).read_bytes()).hexdigest()==digest,'changed dependency: '+name)
    tile=Tile(data['cells'])
    require(len(tile.cells)==17 and data['primary_zero_based_index']==192,'wrong primary seed')
    require(len(tile.frames[tile.root[0]])==1,'unexpected prototype stabilizer')
    pool,cnf,nv=compile_cnf(tile,[tile.root],2)
    audit_pool(tile,[tile.root],2,pool)
    require(hashlib.sha256(dimacs(cnf,nv)).hexdigest()==cert['formula_sha256'],'changed formula')
    lookup={p:i for i,(p,fp) in enumerate(pool,1)}
    floating={i for p,i in lookup.items() if p[1]%1 or p[2]%1}
    supported=set(map(tuple,cert['floating_support']))
    require(witness_support(tile,lookup,cert['first_witnesses'])==supported,'incomplete positive support census')
    proof=(HERE/'floating-support.rup').read_text()
    require(hashlib.sha256(proof.encode()).hexdigest()==cert['proof_sha256'],'changed proof')
    units=support_units(cnf,nv,proof)

    def complete(uu):
        for i in floating:
            p=pool[i-1][0];ty=(p[0],int(2*p[1]),int(2*p[2]))
            require(ty in supported or -i in uu,'missing proved floating exclusion')
    complete(units)
    E0={(p[0],int(2*p[1]),int(2*p[2])) for p,fp in pool}
    require(all(tile.relative_type(tile.pose(t),tile.root) in E0 for t in E0),'nonreciprocal contact inventory')
    reciprocal={t for t in supported if tile.relative_type(tile.pose(t),tile.root) in supported}
    require(not reciprocal,'a floating pair survived both directed supports')
    inverse=[list(tile.relative_type(tile.pose(t),tile.root)) for t in sorted(supported)]
    require(inverse==cert['inverse_floating_support'],'changed reciprocal transport')
    for ty in supported:
        inv=tile.relative_type(tile.pose(ty),tile.root)
        require(-lookup[tile.pose(inv)] in units,'supported type has no proved inverse exclusion')
    controls=0
    truncated='\n'.join(proof.splitlines()[:-1])+'\n'
    controls+=reject(lambda:complete(support_units(cnf,nv,truncated)))
    positive=lookup[tile.pose(sorted(supported)[0])]
    controls+=reject(lambda:support_units(cnf,nv,str(-positive)+' 0\n'))
    damaged=deepcopy(cert['first_witnesses']);damaged[0].pop()
    controls+=reject(lambda:witness_support(tile,lookup,damaged))
    controls+=reject(lambda:check_patch(tile,[tile.root],[tile.root,tile.root],scale=2))
    result=dict(agent='six-heesch-1',role='researcher',primary_zero_based_index=192,seed_cells=17,
                root_orientation=tile.root[0],contact_types=len(pool),floating_types=len(floating),
                floating_first_support=len(supported),proved_floating_exclusions=len(floating)-len(supported),
                reciprocal_floating_support=len(reciprocal),variables=nv,clauses=len(cnf),
                RUP_additions=len(proof.splitlines()),rejected_controls=controls,
                claim='Two contacting strictly surrounded copies have integer relative translation; all prefixes through H-1 are integral in an H-corona packing.',
                scope='No complete upper Heesch bound, new corona construction or record is established by this reader.')
    expected=HERE/'phase-expected.json'
    if expected.exists():require(result==json.loads(expected.read_text()),'expected output mismatch')
    return result


if __name__=='__main__':print(json.dumps(check(),indent=2,sort_keys=True))
