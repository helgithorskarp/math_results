"""Full ambient ordinary-remainder replay of the declared108 subgroup."""
import argparse
from hashlib import sha256
import json
from math import lcm
from pathlib import Path
from time import monotonic
import orbits108 as model


def verify():
    start=monotonic();N,Q=model.N,model.Q
    divisors=[m for m in range(1,N+1) if N%m==0]
    coordinates={period:{(x%(period//27),x%27):x for x in range(period)} for period in (N,Q)}
    physical_points=projection_points=known_checks=partition_checks=0
    event=sha256();phase_maps=[]
    for k,u,v in model.GENERATORS:
        values=[]
        for x in range(N):
            leaf=x%27;raw=leaf%(3**k)
            changed=leaf+v-u if raw==u else leaf+u-v if raw==v else leaf
            y=coordinates[N][x%(N//27),changed]
            if model.physical(N,x,k,u,v)!=y:raise ValueError('Formula differs from physical CRT lookup')
            if y%Q!=coordinates[Q][x%(Q//27),changed]:raise ValueError('Projection does not commute')
            values.append(y);physical_points+=1;projection_points+=1
        if len(set(values))!=N or any(values[values[x]]!=x for x in range(N)):
            raise ValueError('Generator is not an involutive bijection')
        for m in divisors:
            local=1
            while m%(local*3)==0:local*=3
            buckets={}
            for leaf in range(27):
                raw=leaf%(3**k)
                changed=leaf+v-u if raw==u else leaf+u-v if raw==v else leaf
                previous=buckets.setdefault(leaf%local,changed%local)
                if previous!=changed%local:raise ValueError('Divisor class splits')
            if len(set(buckets.values()))!=local:raise ValueError('Divisor partition is not permuted')
            partition_checks+=1
        for parent in model.PARENTS:
            if ({a%9 for m,a in zip(model.BASE,parent) if m%9==0}!=model.PINS9
                    or {a%27 for m,a in zip(model.BASE,parent) if m%27==0}!=model.PINS27):
                raise ValueError('Prescribed ternary pins differ')
            for m,a in zip(model.BASE,parent):
                for x in range(a,N,m):
                    if values[x]%m!=a:raise ValueError('A full prescribed class moves')
                    known_checks+=1
        phase_maps.append([values[a]%108 for a in range(108)])
        event.update(json.dumps([k,u,v,values],separators=(',',':')).encode()+b'\n')
        if monotonic()-start>=20:raise RuntimeError('Incomplete action check under20s cap')
    connected=list(range(108))
    def root(x):
        while connected[x]!=x:x=connected[x]
        return x
    for values in phase_maps:
        for a in range(108):
            one,two=root(a),root(values[a])
            if one!=two:connected[two]=one
    groups={}
    for a in range(108):groups.setdefault(root(a),[]).append(a)
    if (len(groups)!=32 or any(len({model.representative(a) for a in g})!=1 for g in groups.values())
            or sorted(model.representative(g[0]) for g in groups.values())!=list(model.REPRESENTATIVES)):
        raise ValueError('Generated phase orbits differ')
    transport_points=0
    for a in range(108):
        r=model.representative(a)
        if r not in groups[root(a)] or model.representative(r)!=r:
            raise ValueError('Representative leaves its generated orbit')
        for x in range(a,N,108):
            y=model.transport(N,x,a)
            if y%108!=r or y%Q!=model.transport(Q,x%Q,a):
                raise ValueError('Full raw class transporter or projection fails')
            transport_points+=1
    if lcm(*model.BASE)!=Q or Q%108:raise ValueError('Missing108 must divide prescribed actualLCM')
    controls=0
    for op in (lambda:model.representative(-1),lambda:model.representative(108),
               lambda:model.physical(N,0,3,6,7),lambda:model.physical(720,0,2,4,7)):
        try:op()
        except ValueError:controls+=1
        else:raise ValueError('Malformed action accepted')
    for k,u,v,m,a in ((2,1,4,45,19),(3,6,15,54,33),(2,4,7,72,31)):
        if all(model.physical(N,x,k,u,v)%m==a for x in range(a,N,m)):
            raise ValueError('Pinned-leaf negative control did not move the known class')
        controls+=1
    return {'agent':'six-covering-3','role':'researcher','independent_reviewer':False,
            'N':N,'Q':Q,'placed_moduli':list(model.BASE),'parents':[list(p) for p in model.PARENTS],
            'ternary_pins9':sorted(model.PINS9),'ternary_pins27':sorted(model.PINS27),
            'generators':model.GENERATORS,'declared_subgroup_phase_orbits':sorted(groups.values()),
            'orbit_count':len(groups),'representatives':list(model.REPRESENTATIVES),
            'physical_generator_points':physical_points,'projection_points':projection_points,
            'full_prescribed_class_points':known_checks,'divisor_partition_checks':partition_checks,
            'raw108_class_transport_points':transport_points,'invalid_controls_rejected':controls,
            'physical_map_event_sha256':event.hexdigest(),'actual_LCM_preserved':True,
            'maximal_stabilizer_claim':False,'parent_exclusion':False,'root_exclusion':False,
            'whole_cap_seconds':20,'elapsed_seconds':monotonic()-start}
