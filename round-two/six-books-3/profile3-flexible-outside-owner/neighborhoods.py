"""Complete labelled cubic-eight and distinct triangle-free marked-nine inventories.

This is a local neighborhood classification, not a whole Ramsey host search.
All generated graphs stay private. Degree branching and subdivision coverage
have ordinary proofs in NEIGHBORHOODS.md. Each recursion/branch/witness is
charged; the unchanged guard is2M units/40s, inside a45s serial child.
"""
import collections
import hashlib
import itertools
import json
import time


def require(ok,message):
    if not ok:raise ValueError(message)


def adjacency(n,edges):
    result=[0]*n
    for u,v in edges:
        require(0<=u<n and 0<=v<n and u!=v,'Bad simple edge')
        require(not result[u] & (1<<v),'Repeated edge')
        result[u]|=1<<v;result[v]|=1<<u
    return tuple(result)


def triangles(a):
    return [(u,v,w) for u in range(len(a)) for v in range(u+1,len(a))
            if a[u] & (1<<v) for w in range(v+1,len(a))
            if a[u] & a[v] & (1<<w)]


def image(a,phi):
    require(sorted(phi)==list(range(len(a))),'Vertex image not a bijection')
    result=[0]*len(a)
    for u,row in enumerate(a):
        result[phi[u]]=sum(1<<phi[v] for v in range(len(a)) if row & (1<<v))
    return tuple(result)


def subdivide(a,e):
    u,v=e;result=list(a)+[(1<<u)|(1<<v)]
    require(a[u] & (1<<v),'Subdivided edge is absent')
    result[u]=(result[u] & ~(1<<v)) | (1<<8)
    result[v]=(result[v] & ~(1<<u)) | (1<<8)
    return tuple(result)


CUBE=adjacency(8,[(u,v) for u in range(8) for v in range(u+1,8)
                  if (u^v) in (1,2,4)])
WAGNER=adjacency(8,[(i,(i+1)%8) for i in range(8)]+[(i,i+4) for i in range(4)])
TRIANGLE=adjacency(8,[(0,1),(1,2),(0,2),(0,3),(1,4),(2,5)]
    +[(u,v) for u in (6,7) for v in (3,4,5)])
CORES={'cube-edge':(CUBE,(0,1)),'wagner-cycle':(WAGNER,(0,1)),
       'wagner-opposite':(WAGNER,(0,4)),'triangle-edge':(TRIANGLE,(0,1))}


def run(return_inventory=False):
    started=time.monotonic();work=0;phase='normal-forms'
    statistics=collections.Counter();marked=set();direct=set();classes=collections.Counter();graph_classes={}

    def tick():
        nonlocal work
        if work>=2000000 or time.monotonic()-started>=40:
            raise ValueError('Operational local classification guard; incomplete: '+phase)
        work+=1

    def mapping(a,b):
        # Both target regular cores are vertex-transitive; a map may fix0.
        for tail in itertools.permutations(range(1,8)):
            tick();phi=(0,)+tail
            if image(a,phi)==b:return phi
        raise ValueError('Normalized double-four-cycle graph has no asserted image')

    first_cycle=[(0,1),(1,2),(2,3),(0,3)]
    matching=[(i,i+4) for i in range(4)]
    outside=[[(4,5),(5,6),(6,7),(4,7)],
             [(4,5),(5,7),(6,7),(4,6)],
             [(4,6),(5,6),(5,7),(4,7)]]
    normalized={}
    for k,edges in enumerate(outside):
        a=adjacency(8,first_cycle+matching+edges)
        b=CUBE if k==0 else WAGNER
        normalized[a]=(k==0,mapping(a,b))

    def classify(a,e):
        tick()
        tri=triangles(a)
        if tri:
            require(len(tri)==1 and set(e)<=set(tri[0]),
                    'Admissible cubic core outside the ordinary triangle classification')
            t=(e[0],e[1],next(v for v in tri[0] if v not in e))
            attach=[]
            for u in t:
                neighbors=[v for v in range(8) if a[u] & (1<<v) and v not in t]
                require(len(neighbors)==1,'Triangle vertex does not have one attachment')
                attach.append(neighbors[0])
            require(len(set(attach))==3,'Triangle attachments are not distinct')
            vertices=list(t)+attach+[v for v in range(8) if v not in set(t)|set(attach)]
            phi=[vertices.index(v) for v in range(8)];key='triangle-edge'
        else:
            cycle=None
            for u in range(8):
                for v in range(u+1,8):
                    common=[w for w in range(8) if a[u] & a[v] & (1<<w)]
                    if not a[u] & (1<<v) and len(common)>=2:
                        cycle=(u,common[0],v,common[1]);break
                if cycle:break
            require(cycle is not None,'Triangle-free cubic-eight graph has no four-cycle')
            external=[]
            for u in cycle:
                neighbors=[v for v in range(8) if a[u] & (1<<v) and v not in cycle]
                require(len(neighbors)==1,'Four-cycle vertex has wrong external rank')
                external.append(neighbors[0])
            require(len(set(external))==4,'The two four-cycles do not have a perfect matching')
            vertices=list(cycle)+external
            normalization=[vertices.index(v) for v in range(8)]
            is_cube,to_standard=normalized[image(a,normalization)]
            phi=[to_standard[normalization[v]] for v in range(8)]
            u,v=phi[e[0]],phi[e[1]]
            if is_cube:
                delta=u^v
                require(delta in (1,2,4),'Cube mark not a coordinate edge')
                k=delta.bit_length()-1
                def auto(z):
                    z^=u
                    if k and bool(z&1)!=bool(z&(1<<k)):z^=1|(1<<k)
                    return z
                phi=list(map(auto,phi));key='cube-edge'
            else:
                if (v-u)%8==1:offset=u;key='wagner-cycle'
                elif (u-v)%8==1:offset=v;key='wagner-cycle'
                else:
                    require((v-u)%8==4,'Wagner mark is neither cyclic nor opposite')
                    offset=u;key='wagner-opposite'
                phi=[(z-offset)%8 for z in phi]
        representative,edge=CORES[key]
        require(image(a,phi)==representative and {phi[e[0]],phi[e[1]]}==set(edge),
                'Literal complete marked-core transport differs')
        result=subdivide(a,e)
        require(image(result,phi+[8])==subdivide(representative,edge),
                'Literal complete marked-neighborhood transport differs')
        return key,result

    # All labelled simple cubic-eight graphs. No triangle or connectedness
    # pruning is used in this producer domain.
    a=[0]*8
    phase='all-labelled-cubic-eight'
    def cubic(v):
        tick();statistics['cubic_nodes']+=1
        if v==8:
            statistics['labelled_cubic_graphs']+=1
            frozen=tuple(a)
            require(all(row.bit_count()==3 for row in a),'Cubic leaf degree mismatch')
            tri=triangles(a)
            edges={(u,w) for u in range(8) for w in range(u+1,8) if a[u] & (1<<w)}
            admissible=edges
            for t in tri:admissible=admissible & set(itertools.combinations(t,2))
            for edge in sorted(admissible):
                key,neighborhood=classify(frozen,edge)
                require(not triangles(neighborhood),'Subdivided admissible core has a triangle')
                require(neighborhood not in marked,'Repeated labelled subdivision')
                marked.add(neighborhood);classes[key]+=1;graph_classes[neighborhood]=key
            return
        need=3-a[v].bit_count()
        candidates=[w for w in range(v+1,8) if a[w].bit_count()<3]
        if not 0<=need<=len(candidates):return
        for chosen in itertools.combinations(candidates,need):
            tick();statistics['cubic_branches']+=1
            for w in chosen:a[v]|=1<<w;a[w]|=1<<v
            remaining=[3-a[w].bit_count() for w in range(v+1,8)]
            positive=sum(d>0 for d in remaining)
            if all(0<=d<=max(0,positive-1) for d in remaining):cubic(v+1)
            for w in chosen:a[v]^=1<<w;a[w]^=1<<v
    cubic(0)

    # Distinct physical domain: choose the marked degree-two point's two
    # neighbors, then fill the eight remaining degree margins while rejecting
    # a triangle immediately on adding its final edge. No cubic data is read.
    phase='direct-labelled-triangle-free-nine'
    b=[0]*9
    def nine(v):
        tick();statistics['nine_nodes']+=1
        if v==8:
            require([row.bit_count() for row in b]==[3]*8+[2] and not triangles(b),
                    'Direct marked-nine leaf violates physical degree/triangle scope')
            record=tuple(b)
            require(record not in direct,'Repeated physical nine-point graph')
            direct.add(record);statistics['labelled_nine_graphs']+=1
            return
        need=3-b[v].bit_count()
        candidates=[w for w in range(v+1,8) if b[w].bit_count()<3 and not b[v]&b[w]]
        if not 0<=need<=len(candidates):return
        for chosen in itertools.combinations(candidates,need):
            tick();statistics['nine_branches']+=1
            for w in chosen:b[v]|=1<<w;b[w]|=1<<v
            remaining=[3-b[w].bit_count() for w in range(v+1,8)]
            positive=sum(d>0 for d in remaining)
            if all(0<=d<=max(0,positive-1) for d in remaining):nine(v+1)
            for w in chosen:b[v]^=1<<w;b[w]^=1<<v
    for u,v in itertools.combinations(range(8),2):
        require(not any(b),'Direct generator has unreverted edges')
        b[8]=(1<<u)|(1<<v);b[u]=1<<8;b[v]=1<<8
        nine(0)
        b[8]=b[u]=b[v]=0
    require(marked==direct,'Whole distinct labelled marked-neighborhood inventories differ')
    encoded=json.dumps(sorted(direct),separators=(',',':')).encode()
    representatives={name:list(subdivide(graph,edge)) for name,(graph,edge) in CORES.items()}
    require(set(classes)==set(CORES),'One of the four ordinary classes is missing')
    result=dict(agent='six-books-3',role='researcher',
        status='COMPLETE_DISTINCT_LOCAL_NEIGHBORHOOD_CLASSIFICATION',
        hypotheses='Triangle-free simple nine-point graph with distinguished degree2 point8 and all other degrees3',
        representatives=representatives,labelled_class_counts=dict(classes),
        complete_labelled_graphs=len(direct),statistics=dict(statistics),
        whole_inventory_bytes=len(encoded),whole_inventory_sha256=hashlib.sha256(encoded).hexdigest(),
        every_marked_core_literal_transport_checked=True,
        work_units=work,work_guard=2000000,internal_seconds_guard=40,
        ordinary_completeness_and_classification_formalized=False,
        actual_host_automorphism_assumed=False,whole_Ramsey_host_exclusion=False)

    return (result, sorted(direct), graph_classes) if return_inventory else result


if __name__=='__main__':print(json.dumps(run(),sort_keys=True,separators=(',',':')))
