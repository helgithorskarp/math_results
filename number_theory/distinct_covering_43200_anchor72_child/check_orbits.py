"""Independent ordinary-remainder replay of the declared missing72 action."""
from hashlib import sha256
from math import lcm
from pathlib import Path
from time import monotonic
import argparse
import json
import orbits as model


def verify():
    start=monotonic()
    N,Q=model.N,model.Q
    divisors=[m for m in range(1,N+1) if N%m==0]
    coordinates={p:{period:{(x%(period//power),x%power):x for x in range(period)}
                       for period,power in ((N,64 if p==2 else 27),(Q,16 if p==2 else 27))}
                 for p in (2,3)}
    known_checks=physical_points=projection_points=partition_checks=0
    event=sha256()
    maps=[]
    for p,k,u,v in model.GENERATORS:
        power=64 if p==2 else 27
        values=[]
        for x in range(N):
            leaf=x%power
            raw=leaf%(p**k)
            changed=leaf+v-u if raw==u else leaf+u-v if raw==v else leaf
            y=coordinates[p][N][x%(N//power),changed]
            if model.physical(N,x,p,k,u,v)!=y:
                raise ValueError('Formula differs from physical CRT lookup')
            smallpower=16 if p==2 else 27
            smallleaf=x%smallpower
            changed_small=smallleaf+v-u if raw==u else smallleaf+u-v if raw==v else smallleaf
            if y%Q!=coordinates[p][Q][x%(Q//smallpower),changed_small]:
                raise ValueError('Projection does not commute')
            values.append(y);physical_points+=1;projection_points+=1
        if len(set(values))!=N or any(values[values[x]]!=x for x in range(N)):
            raise ValueError('Generator is not an involutive bijection')
        for m in divisors:
            # Every cofactor is fixed. Check the complete p-primary partition.
            local=1
            while m%(local*p)==0:local*=p
            buckets={}
            for leaf in range(power):
                raw=leaf%(p**k)
                changed=leaf+v-u if raw==u else leaf+u-v if raw==v else leaf
                previous=buckets.setdefault(leaf%local,changed%local)
                if previous!=changed%local:
                    raise ValueError('A prime-power divisor class splits')
            if len(set(buckets.values()))!=local:
                raise ValueError('Local divisor partition is not permuted')
            partition_checks+=1
        for parent in model.PARENTS:
            if {a%8 for m,a in zip(model.BASE,parent) if m%8==0}!=model.BINARY_PINS:
                raise ValueError('Binary pins differ')
            if {a%9 for m,a in zip(model.BASE,parent) if m%9==0}!=model.TERNARY_PINS:
                raise ValueError('Ternary pins differ')
            for m,a in zip(model.BASE,parent):
                for x in range(a,N,m):
                    if values[x]%m!=a:raise ValueError('A full prescribed class moves')
                    known_checks+=1
        maps.append(values)
        event.update(json.dumps([p,k,u,v,values],separators=(',',':')).encode()+b'\n')
        if monotonic()-start>=20:raise RuntimeError('Incomplete action check under20s cap')
    # Enumerate generator graph independently of the representative formula.
    connected=list(range(72))
    def root(x):
        while connected[x]!=x:x=connected[x]
        return x
    for values in maps:
        for a in range(72):
            one,two=root(a),root(values[a]%72)
            if one!=two:connected[two]=one
    groups={}
    for a in range(72):groups.setdefault(root(a),[]).append(a)
    if (len(groups)!=42 or any(len({model.representative(a) for a in g})!=1 for g in groups.values())
            or sorted(model.representative(g[0]) for g in groups.values())!=list(model.REPRESENTATIVES)):
        raise ValueError('The declared subgroup orbits differ')
    transporter_points=0
    for a in range(72):
        r=model.representative(a)
        if r not in groups[root(a)] or model.representative(r)!=r:
            raise ValueError('Representative leaves its generated orbit')
        # All72 phase class points, not just one phase witness.
        for x in range(a,N,72):
            y=model.transport(N,x,a)
            if y%72!=r or y%Q!=model.transport(Q,x%Q,a):
                raise ValueError('Class transporter or projection failed')
            transporter_points+=1
    if lcm(*model.BASE)!=Q or Q%72:
        raise ValueError('Missing72 must divide the already prescribed actualLCM')
    invalid=0
    for operation in (lambda:model.representative(-1),lambda:model.representative(72),
                      lambda:model.physical(N,0,3,2,2,4),lambda:model.physical(720,0,2,3,1,5)):
        try:operation()
        except ValueError:invalid+=1
        else:raise ValueError('Malformed symmetry input accepted')
    # An inadmissible pinned-leaf swap must visibly move a prescribed class.
    if all(model.physical(N,x,3,2,1,4)%45==19 for x in range(19,N,45)):
        raise ValueError('Pinned-leaf negative control did not move the known45 class')
    invalid+=1
    return {'agent':'six-covering-3','role':'researcher','independent_reviewer':False,
            'N':N,'Q':Q,'placed_moduli':list(model.BASE),'parents':[list(p) for p in model.PARENTS],
            'binary_pins':sorted(model.BINARY_PINS),'ternary_pins':sorted(model.TERNARY_PINS),
            'generators':model.GENERATORS,'declared_subgroup_phase_orbits':sorted(groups.values()),
            'orbit_count':len(groups),'representatives':list(model.REPRESENTATIVES),
            'physical_generator_points':physical_points,'projection_points':projection_points,
            'full_prescribed_class_points':known_checks,'divisor_partition_checks':partition_checks,
            'raw72_class_transport_points':transporter_points,'invalid_controls_rejected':invalid,
            'physical_map_event_sha256':event.hexdigest(),'actual_LCM_preserved':True,
            'covering_equivalence_proved_by_written_argument':True,'maximal_stabilizer_claim':False,
            'parent_exclusion':False,'root_exclusion':False,'whole_cap_seconds':20,
            'elapsed_seconds':monotonic()-start}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    if args.out.exists():raise ValueError('Preserve immutable action evidence')
    result=verify();args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
