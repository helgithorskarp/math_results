"""Ordinary-remainder full ambient action checks, independent of formulas."""
from hashlib import sha256
import json
from math import lcm
from time import monotonic


def verify():
    import orbits100 as model
    start=monotonic();N,Q=model.N,model.Q
    divisors=[m for m in range(1,N+1) if N%m==0]
    coordinates={period:{(x%(period//25),x%25):x for x in range(period)} for period in (N,Q)}
    known_checks=physical_points=projection_points=partition_checks=0
    event=sha256();phase_maps=[]
    for u,v in model.GENERATORS:
        values=[]
        for x in range(N):
            leaf=x%25
            changed=v if leaf==u else u if leaf==v else leaf
            y=coordinates[N][x%(N//25),changed]
            if model.physical(N,x,u,v)!=y:
                raise ValueError('Formula differs from physical CRT lookup')
            if y%Q != coordinates[Q][x%(Q//25),changed]:
                raise ValueError('Projection does not commute')
            values.append(y);physical_points+=1;projection_points+=1
        if len(set(values))!=N or any(values[values[x]]!=x for x in range(N)):
            raise ValueError('Generator is not an involutive bijection')
        for m in divisors:
            local=1
            while m%(local*5)==0:local*=5
            buckets={}
            for leaf in range(25):
                changed=v if leaf==u else u if leaf==v else leaf
                previous=buckets.setdefault(leaf%local,changed%local)
                if previous!=changed%local:raise ValueError('A divisor class splits')
            if len(set(buckets.values()))!=local:
                raise ValueError('Local divisor partition is not permuted')
            partition_checks+=1
        for parent in model.PARENTS:
            if {a%25 for m,a in zip(model.BASE,parent) if m%25==0}!=model.QUINARY_PINS:
                raise ValueError('Pinned quinary leaves differ')
            for m,a in zip(model.BASE,parent):
                for x in range(a,N,m):
                    if values[x]%m!=a:raise ValueError('A full prescribed class moves')
                    known_checks+=1
        phase_maps.append([values[a]%100 for a in range(100)])
        event.update(json.dumps([u,v,values],separators=(',',':')).encode()+b'\n')
        if monotonic()-start>=20:raise RuntimeError('Incomplete action check under20s cap')
    connected=list(range(100))
    def root(x):
        while connected[x]!=x:x=connected[x]
        return x
    for values in phase_maps:
        for a in range(100):
            one,two=root(a),root(values[a])
            if one!=two:connected[two]=one
    groups={}
    for a in range(100):groups.setdefault(root(a),[]).append(a)
    if (len(groups)!=32 or any(len({model.representative(a) for a in g})!=1 for g in groups.values())
            or sorted(model.representative(g[0]) for g in groups.values())!=list(model.REPRESENTATIVES)):
        raise ValueError('Generated subgroup orbits differ')
    transporter_points=0
    for a in range(100):
        r=model.representative(a)
        if r not in groups[root(a)] or model.representative(r)!=r:
            raise ValueError('Representative leaves its generated orbit')
        for x in range(a,N,100):
            y=model.transport(N,x,a)
            if y%100!=r or y%Q!=model.transport(Q,x%Q,a):
                raise ValueError('Full class transporter or projection failed')
            transporter_points+=1
    if lcm(*model.BASE)!=Q or Q%100:
        raise ValueError('Missing100 does not divide the prescribed actualLCM')
    invalid=0
    for op in (lambda:model.representative(-1),lambda:model.representative(100),
               lambda:model.physical(N,0,2,4),lambda:model.physical(720,0,1,6)):
        try:op()
        except ValueError:invalid+=1
        else:raise ValueError('Malformed symmetry input accepted')
    if all(model.physical(N,x,3,18)%25==3 for x in range(3,N,25)):
        raise ValueError('Pinned-leaf negative control did not move the known25 class')
    invalid+=1
    return {'agent':'six-covering-3','role':'researcher','independent_reviewer':False,
            'N':N,'Q':Q,'placed_moduli':list(model.BASE),'parents':[list(p) for p in model.PARENTS],
            'quinary_pins':sorted(model.QUINARY_PINS),'generators':model.GENERATORS,
            'declared_subgroup_phase_orbits':sorted(groups.values()),'orbit_count':len(groups),
            'representatives':list(model.REPRESENTATIVES),'physical_generator_points':physical_points,
            'projection_points':projection_points,'full_prescribed_class_points':known_checks,
            'divisor_partition_checks':partition_checks,'raw100_class_transport_points':transporter_points,
            'invalid_controls_rejected':invalid,'physical_map_event_sha256':event.hexdigest(),
            'actual_LCM_preserved':True,'maximal_stabilizer_claim':False,'parent_exclusion':False,
            'root_exclusion':False,'whole_cap_seconds':20,'elapsed_seconds':monotonic()-start}
