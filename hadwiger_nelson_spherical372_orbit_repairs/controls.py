"""Independent finite coverage and geometric/combinatorial negative controls."""
import copy
import json
import tempfile
from itertools import product
from pathlib import Path
from generate import maximal_masks
from verify import (HERE,N,read_graph,group_elements,orbits_from_group,
                    neighbourhood_cycles,wheel_mask,check_colouring,verify,require)


def rejects(call):
    try:
        call()
    except ValueError:
        return
    raise ValueError('corrupted input accepted')


def run():
    hypergraphs=0
    for n in range(4):
        nonempty=list(range(1,1<<n))
        for family in range(1<<len(nonempty)):
            clauses=[c for k,c in enumerate(nonempty) if family>>k&1]
            for impossible in (False,True):
                fs=clauses+([0] if impossible else [])
                feasible=[m for m in range(1<<n) if all(m&f!=f for f in fs)]
                expected=[m for m in feasible if not any(m!=q and m&q==m for q in feasible)]
                require(maximal_masks(n,fs)==expected,'generic maximal-support coverage')
                hypergraphs+=1
    edges=read_graph(HERE/'source.edges')
    cert=json.loads((HERE/'certificate.json').read_text())
    forbidden=[w['mask'] for w in cert['wheels']]
    support=0
    for f in forbidden:
        support|=f
    bits=[k for k in range(29) if support>>k&1]
    feasible=0
    for small in range(1<<len(bits)):
        mask=sum(1<<k for j,k in enumerate(bits) if small>>j&1)
        admitted=all(mask&f!=f for f in forbidden)
        covered=any(mask&item['mask']==mask for item in cert['colourings'])
        require(admitted==covered,'direct 13-selector coverage')
        feasible+=admitted
    require(len(bits)==13 and feasible==729,'coverage census')
    # Exact angle-walk obstruction: odd +/-1 walks cannot return modulo six.
    odd_walks=0
    for n in (3,5,7,9,11):
        for signs in product((-1,1),repeat=n):
            require(sum(signs)%6!=0,'odd unit-circle walk closed')
            odd_walks+=1
    require(sum([1]*6)%6==0,'hexagonal positive control')
    require(sum([1]*5)%5==0,'spherical pentagonal angle contrast')
    # A four-colourable odd wheel is still geometrically forbidden.
    wheel=sorted([(0,v) for v in range(1,6)]+[(v,v+1) for v in range(1,5)]+[(1,5)])
    check_colouring(6,wheel,'012123')
    require(neighbourhood_cycles(wheel,6)==[(0,(1,2,3,4,5))],'odd-wheel extraction')
    square=[(0,1),(0,3),(1,2),(2,3),(0,2),(1,3)];square=sorted(square)
    dihedral=group_elements([[1,2,3,0],[0,3,2,1]],square,4)
    require(len(dihedral)==8 and sorted(map(len,orbits_from_group(square,dihedral)))==[2,4],
            'dihedral group/orbit control')
    failures=0
    with tempfile.TemporaryDirectory(prefix='hn372-controls-') as folder:
        path=Path(folder)/'bad.json'
        variants=[]
        c=copy.deepcopy(cert);c['colourings'].pop();variants.append(c)
        c=copy.deepcopy(cert);c['colourings'][1]=copy.deepcopy(c['colourings'][0]);variants.append(c)
        c=copy.deepcopy(cert);c['colourings'][0]['word']='0'*N;variants.append(c)
        c=copy.deepcopy(cert);c['colourings'][0]['word']=c['colourings'][0]['word'][:-1];variants.append(c)
        c=copy.deepcopy(cert);c['colourings'][0]['word']='4'+c['colourings'][0]['word'][1:];variants.append(c)
        c=copy.deepcopy(cert);c['colourings'][0]['mask']=1<<29;variants.append(c)
        c=copy.deepcopy(cert);c['colourings'][0]['mask']=True;variants.append(c)
        c=copy.deepcopy(cert);c['wheels'].pop();variants.append(c)
        c=copy.deepcopy(cert);c['wheels'][0]['rim'][0]=c['wheels'][0]['centre'];variants.append(c)
        c=copy.deepcopy(cert);c['wheels'][0]['rim']=c['wheels'][0]['rim'][:4];variants.append(c)
        c=copy.deepcopy(cert);c['wheels'][0]['mask']^=1;variants.append(c)
        c=copy.deepcopy(cert);c['unknown']=1;variants.append(c)
        for c in variants:
            path.write_text(json.dumps(c));rejects(lambda:verify(path));failures+=1
        bad_edges=Path(folder)/'bad.edges';bad_edges.write_bytes((HERE/'source.edges').read_bytes()+b'\n')
        rejects(lambda:read_graph(bad_edges));failures+=1
    generators=json.loads((HERE/'generators.json').read_text())
    bad=copy.deepcopy(generators);bad[0][0]=bad[0][1]
    rejects(lambda:group_elements(bad,edges));failures+=1
    bad=[list(range(N))];bad[0][0],bad[0][1]=bad[0][1],bad[0][0]
    rejects(lambda:group_elements(bad,edges));failures+=1
    return dict(generic_hypergraphs_checked=hypergraphs,actual_constrained_selectors_checked=1<<len(bits),
                actual_feasible_constrained_assignments=feasible,odd_angle_walks_checked=odd_walks,
                malformed_inputs_rejected=failures,dihedral_group_and_orbits=True,
                four_coloured_odd_wheel_control=True)


if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
