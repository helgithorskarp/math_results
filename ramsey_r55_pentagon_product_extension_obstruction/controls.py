"""Physical43 transports and corrupted proof/input controls."""
from itertools import combinations
from pathlib import Path
import copy
import hashlib
import json
import random
import check
import interface
import verify_certificate


def require(ok, message):
    if not ok:
        raise ValueError(message)


def fixture(tail, transport, complement):
    root=Path(__file__).resolve().parent
    literal=json.loads((root/'CORE.json').read_text())
    core_word=int(literal['red_hex'],16)
    small_pairs=list(combinations(range(25),2))
    small_edges={e for i,e in enumerate(small_pairs) if core_word & (1 << i)}
    pairs=list(combinations(range(43),2));position={frozenset(e):i for i,e in enumerate(pairs)}
    permutation=list(range(43))
    if transport:
        random.Random(1701).shuffle(permutation)
    rng=random.Random(2219);value=0
    for u,v in pairs:
        bit=int((u,v) in small_edges) if v<25 else (tail if tail in (0,1) else rng.getrandbits(1))
        bit ^= int(complement)
        if bit:
            value |= 1 << position[frozenset((permutation[u],permutation[v]))]
    graph=dict(n=43,red_hex=format(value,'0226x'))
    vertices=list(reversed(permutation[:25]))
    return dict(graph=graph,core_vertices=vertices)


def main():
    root=Path(__file__).resolve().parent
    certificate=json.loads((root/'CERTIFICATE.json').read_text())
    outcomes=[]
    for tail in (0,1,2):
        for transport in (False,True):
            for complement in (False,True):
                request=fixture(tail,transport,complement)
                out=interface.reject(request['graph'],request['core_vertices'])
                require(out['status']=='REJECTED_COMPLETE_CORE_EXTENSION_FAMILY','physical family missed')
                verified=verify_certificate.verify(request['graph'],out['certificate'])
                require(verified['pairs_checked']==10,'physical pair count')
                outcomes.append(dict(tail=tail,transport=transport,complement=complement,
                                     certificate=out['certificate']))
    # A changed core is outside this specific family; this is not acceptance
    # of the surrounding graph as a Ramsey target.
    request=fixture(2,False,False)
    changed=copy.deepcopy(request)
    changed['graph']['red_hex']=format(int(changed['graph']['red_hex'],16)^1,'0226x')
    require(interface.reject(changed['graph'],changed['core_vertices'])['status']=='OUTSIDE_SPECIFIED_CORE_FAMILY','changed core recognition')
    mutations={
        'missing_inner_word':lambda c:c['inner'].pop(),
        'uncovered_inner_tag':lambda c:c['inner'][0].update(tag=0),
        'wrong_inner_pair':lambda c:c['inner'][0].update(blue_pair=[0,1]),
        'missing_outer_class':lambda c:c['outer'].pop(),
        'wrong_outer_color':lambda c:c['outer'][0].update(color='blue'),
        'wrong_class_weight':lambda c:c['outer'][0].update(attachment_count=0),
        'wrong_global_free_count':lambda c:c.update(free_43_edges=602),
    }
    rejected=[]
    for name,mutate in mutations.items():
        bad=copy.deepcopy(certificate);mutate(bad)
        try:check.validate(bad)
        except ValueError:rejected.append(name)
        else:raise ValueError('corrupt family certificate accepted: '+name)
    invalid_requests=[]
    for name,mutate in {
        'wrong_n':lambda r:r['graph'].update(n=42),
        'high_bit':lambda r:r['graph'].update(red_hex=format(1 << 903,'0226x')),
        'short_word':lambda r:r['graph'].update(red_hex='0'),
        'duplicate_core_vertex':lambda r:r['core_vertices'].__setitem__(0,r['core_vertices'][1]),
        'boolean_core_vertex':lambda r:r['core_vertices'].__setitem__(0,True),
        'core_vertex_out_of_range':lambda r:r['core_vertices'].__setitem__(0,43),
    }.items():
        bad=copy.deepcopy(request);mutate(bad)
        try:interface.reject(bad['graph'],bad['core_vertices'])
        except ValueError:invalid_requests.append(name)
        else:raise ValueError('bad physical input accepted: '+name)
    output=interface.reject(request['graph'],request['core_vertices'])
    invalid_certificates=[]
    for name,mutate in {
        'opposite_color':lambda c:c.update(color='blue' if c['color']=='red' else 'red'),
        'duplicate_vertex':lambda c:c['vertices'].__setitem__(0,c['vertices'][1]),
        'wrong_graph_digest':lambda c:c.update(red_hex_sha256='0'*64),
        'wrong_order':lambda c:c.update(n=25),
    }.items():
        bad=copy.deepcopy(output['certificate']);mutate(bad)
        try:verify_certificate.verify(request['graph'],bad)
        except ValueError:invalid_certificates.append(name)
        else:raise ValueError('bad physical certificate accepted: '+name)
    rows=interface.parse(request['graph']);mask=(1 << 25)-1
    for u,v in combinations(range(25),2):
        distinguish=((rows[u]^rows[v]) & mask & ~((1 << u)|(1 << v))).bit_count()
        require(distinguish==(2 if u//5==v//5 else 14),'recognizer distinguishing lemma')
    example=json.loads((root/'FIXTURE.json').read_text())
    expected=json.loads((root/'EXAMPLE_CERTIFICATE.json').read_text())
    require(interface.reject(example['graph'],example['core_vertices'])==expected,'saved physical example')
    verify_certificate.verify(example['graph'],expected['certificate'])
    bridge=json.loads((root/'BRIDGE_CONTROL.json').read_text())
    request=bridge['input'];value=int(request['graph']['red_hex'],16)
    order=bridge['induced_P5_order']
    require(len(order)==len(set(order))==5 and set(order)<=set(bridge['old_26_subset']),'bridge path vertices')
    for i in range(5):
        for j in range(i+1,5):
            u,v=sorted((order[i],order[j]));bit=u*(85-u)//2+v-u-1
            require(bool(value & (1 << bit))==(j==i+1),'literal bridge P5')
    require(interface.reject(request['graph'],request['core_vertices'])==bridge['output'],'bridge output')
    verify_certificate.verify(request['graph'],bridge['output']['certificate'])
    print(json.dumps(dict(status='CHECKED_PHYSICAL_EXTENSION_INTERFACE_AND_CONTROLS',
                          physical43_fixtures=len(outcomes),literal_physical_pairs_checked=10*len(outcomes),
                          core_pair_distinguishers_checked=300,changed_core_outside_family=True,
                          rejected_family_certificate_mutations=rejected,
                          rejected_physical_inputs=invalid_requests,
                          rejected_physical_certificates=invalid_certificates,
                          bridge_has_literal_P5_on26_and_literal_K5=True,
                          transport_certificate_digest=hashlib.sha256(json.dumps(outcomes,sort_keys=True).encode()).hexdigest()),
                     indent=2,sort_keys=True))


if __name__=='__main__':
    main()
