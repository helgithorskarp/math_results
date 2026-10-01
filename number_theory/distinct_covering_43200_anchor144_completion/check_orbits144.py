"""Independent ordinary-CRT replay of all ten product generators at fullN."""
import argparse
from hashlib import sha256
import json
from math import lcm
from pathlib import Path
from time import monotonic

import orbits144 as model


def need(condition, message):
    if not condition:
        raise ValueError(message)


def verify():
    start = monotonic()
    N,Q = model.N,model.Q
    coordinates = {p: {(x%(64 if p==N else 16),x%27,x%25): x for x in range(p)}
                   for p in (N,Q)}
    divisors = [m for m in range(1,N+1) if N%m==0]
    for local,pins in ((8,model.BINARY_PINS8),(16,model.BINARY_PINS16),
                       (9,model.TERNARY_PINS9),(27,model.TERNARY_PINS27)):
        need({a%local for m,a in zip(model.BASE,model.PARENT) if m%local==0} == pins,
             'Declared prescribed pins differ')
    events = sha256()
    physical_points = projection_points = known_points = partitions = 0
    maps = []
    for family,k,u,v in model.GENERATORS:
        prime = 2 if family=='binary' else 3
        axis = 64 if family=='binary' else 27
        images = []
        for x in range(N):
            binary,ternary,quinary = x%64,x%27,x%25
            leaf = binary if family=='binary' else ternary
            raw = leaf%(prime**k)
            changed = leaf+v-u if raw==u else leaf+u-v if raw==v else leaf
            if family=='binary': binary=changed
            else: ternary=changed
            y = coordinates[N][binary,ternary,quinary]
            need(model.physical(N,x,family,k,u,v)==y, 'Formula differs from ordinary CRT lookup')
            need(y%Q==coordinates[Q][binary%16,ternary,quinary]
                 and model.physical(Q,x%Q,family,k,u,v)==y%Q, 'Projection differs')
            images.append(y)
            physical_points += 1
            projection_points += 1
        need(len(set(images))==N and all(images[images[x]]==x for x in range(N)),
             'Generator is not an involutive bijection')
        # Other primary coordinates are fixed. Checking the moving primary
        # partition suffices for each divisor class by ordinary CRT uniqueness.
        for m in divisors:
            local = 1
            while m%(local*prime)==0: local*=prime
            buckets = {}
            for leaf in range(axis):
                raw = leaf%(prime**k)
                changed = leaf+v-u if raw==u else leaf+u-v if raw==v else leaf
                need(buckets.setdefault(leaf%local,changed%local)==changed%local,
                     'A moving primary divisor class splits')
            need(len(set(buckets.values()))==local, 'Primary partition is not permuted')
            partitions += 1
        for m,a in zip(model.BASE,model.PARENT):
            for x in range(a,N,m):
                need(images[x]%m==a, 'A prescribed full class moves')
                known_points += 1
        maps.append([images[a]%144 for a in range(144)])
        events.update(json.dumps([family,k,u,v,images],separators=(',',':')).encode()+b'\n')
        need(monotonic()-start<20, 'Incomplete action check under20s cap')
    links = list(range(144))
    def root(a):
        while links[a]!=a: a=links[a]
        return a
    for images in maps:
        for a in range(144):
            one,two=root(a),root(images[a])
            if one!=two: links[two]=one
    groups = {}
    for a in range(144): groups.setdefault(root(a),[]).append(a)
    need(len(groups)==63 and len(model.REPRESENTATIVES)==63
         and all(len({model.representative(a) for a in g})==1 for g in groups.values())
         and sorted(model.representative(g[0]) for g in groups.values())==list(model.REPRESENTATIVES),
         'Generated product phase orbits differ')
    transported = 0
    for a in range(144):
        r=model.representative(a)
        need(r in groups[root(a)] and model.representative(r)==r, 'Representative leaves its orbit')
        for x in range(a,N,144):
            y=model.transport(N,x,a)
            need(y%144==r and y%Q==model.transport(Q,x%Q,a), 'Raw144 full class transport fails')
            transported += 1
    need(lcm(*model.BASE)==Q and Q%144==0, 'Missing144 must divide prescribedLCM')
    controls = 0
    for op in (lambda:model.representative(-1), lambda:model.representative(144),
               lambda:model.physical(N,0,'binary',4,1,2),
               lambda:model.physical(N,0,'other',3,1,5),
               lambda:model.physical(720,0,'binary',3,1,5)):
        try: op()
        except ValueError: controls+=1
        else: raise ValueError('Malformed action accepted')
    for family,k,u,v,m,a in (('binary',4,4,12,16,4), ('binary',4,6,14,48,14),
                             ('ternary',2,4,7,72,31)):
        need(any(model.physical(N,x,family,k,u,v)%m!=a for x in range(a,N,m)),
             'Pinned negative control failed to move a known full class')
        controls += 1
    need(monotonic()-start<20, 'Incomplete product check under20s cap')
    return {'agent':'six-covering-3','role':'researcher','independent_reviewer':False,
            'N':N,'Q':Q,'placed_moduli':list(model.BASE),'parent':list(model.PARENT),
            'generators':model.GENERATORS,'binary_pins8':sorted(model.BINARY_PINS8),
            'binary_pins16':sorted(model.BINARY_PINS16),'ternary_pins9':sorted(model.TERNARY_PINS9),
            'ternary_pins27':sorted(model.TERNARY_PINS27),'binary16_orbit_count':9,
            'ternary9_orbit_count':7,'declared_subgroup_phase_orbits':sorted(groups.values()),
            'orbit_count':len(groups),'representatives':list(model.REPRESENTATIVES),
            'physical_generator_points':physical_points,'projection_points':projection_points,
            'full_prescribed_class_points':known_points,'divisor_partition_checks':partitions,
            'raw144_class_transport_points':transported,'invalid_controls_rejected':controls,
            'physical_map_event_sha256':events.hexdigest(),'actual_LCM_preserved':True,
            'maximal_stabilizer_claim':False,'parent_exclusion':False,'root_exclusion':False,
            'whole_cap_seconds':20,'elapsed_seconds':monotonic()-start}
