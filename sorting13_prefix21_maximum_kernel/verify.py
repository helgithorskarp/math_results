"""Definition-level independent replay; does not import the generator."""
import hashlib
import itertools
import json
from pathlib import Path


def digest(values):
    return hashlib.sha256(json.dumps(values,separators=(',',':')).encode()).hexdigest()


def simulate(bits,network):
    for a,b in network:
        if bits[a] > bits[b]:bits[a],bits[b] = bits[b],bits[a]
    return bits


def check():
    base=Path(__file__).resolve().parent
    f=json.loads((base/'fixture.json').read_text())
    c=json.loads((base/'certificate.json').read_text())
    assert f['channels']==c['channels']==13
    assert f['prefix_length']==c['prefix_length']==21
    network=f['incumbent'];prefix=network[:21]
    assert len(network)==45
    assert all(len(g)==2 and 0 <= g[0] < g[1] < 13 for g in network)
    image=set()
    for inp in itertools.product((0,1),repeat=13):
        output=simulate(list(inp),network)
        assert output==sorted(inp),'fixture is not a sorting network'
        out=simulate(list(inp),prefix)
        assert out[12]==max(inp),'prefix does not fix the global maximum'
        image.add(sum(out[i] << i for i in range(12)))
    image=sorted(image)
    assert len(image)==c['residual_count']==157
    assert digest(image)==c['residual_sha256']
    candidates=[i for i in range(12) if 1 << i in image]
    assert candidates==c['maximum_candidates']==[6,9,10,11]
    assert len(c['pruning_witnesses'])==4
    assert [w['output_holes'][0] for w in c['pruning_witnesses']]==candidates
    for w in c['pruning_witnesses']:
        A=w['inputs'];holes=w['output_holes']
        assert len(A)==2 and A==sorted(set(A)) and all(0 <= i < 13 for i in A)
        assert holes==[holes[0],12]
        assert w['deleted_gates']==7 and len(w['retained_network'])==14
        assert sorted(w['output_order'])==list(range(11))
        assert all(len(g)==2 and 0 <= g[0] < 11 and 0 <= g[1] < 11 and g[0]!=g[1]
                   for g in w['retained_network'])
        source=set()
        for inp in itertools.product((0,1),repeat=11):
            # Known maxima have value 2; all unknowns have values 0 or 1.
            original=[];j=0
            for i in range(13):
                if i in A:original.append(2)
                else:original.append(inp[j]);j+=1
            touched=0
            for a,b in prefix:
                touched += original[a]==2 or original[b]==2
                if original[a] > original[b]:original[a],original[b] = original[b],original[a]
            assert touched==7
            assert [i for i,x in enumerate(original) if x==2]==holes
            expected=[x for i,x in enumerate(original) if i not in holes]
            retained=simulate(list(inp),w['retained_network'])
            actual=[retained[i] for i in w['output_order']]
            assert actual==expected,'pruned network differs from direct marker execution'
            source.add(sum(x << i for i,x in enumerate(actual)))
            thresholded=[int(x>0) for x in original]
            residual=sum(thresholded[i] << i for i in range(12))
            assert residual in image and thresholded[holes[0]]==1
        target=set()
        for x in image:
            bits=[(x >> i)&1 for i in range(12)]
            if bits[holes[0]]:
                del bits[holes[0]]
                target.add(sum(b << i for i,b in enumerate(bits)))
        assert source <= target
        assert len(source)==w['source_image_count'] and digest(sorted(source))==w['source_image_sha256']
        assert len(target)==w['target_image_count'] and digest(sorted(target))==w['target_image_sha256']
    # Enumerate labelled matchings via a different convention; root is forced
    # to compare the surviving larger channel of each of the two pairs.
    kernels=set()
    for pairing in itertools.permutations(candidates):
        p=tuple(sorted(pairing[:2]));q=tuple(sorted(pairing[2:]))
        children=tuple(sorted((p,q)))
        root=tuple(sorted((p[1],q[1])))
        kernels.add((children,root))
    actual={(tuple(tuple(x) for x in w['child_gates']),tuple(w['root_gate']))
            for w in c['maximum_kernels']}
    assert len(actual)==3 and actual==kernels
    # Positive control: the known 24-gate completion has a permitted kernel.
    supports={i:{i} for i in candidates};merges=[];unary=0
    for a,b in network[21:]:
        sa=supports.get(a,set());sb=supports.get(b,set())
        if sa and sb:merges.append((a,b))
        elif sa or sb:unary+=1
        supports[a]=set();supports[b]=sa|sb
    assert supports[11]==set(candidates) and unary==0 and len(merges)==3
    assert (tuple(sorted(merges[:2])),merges[2]) in actual
    for i in candidates:
        bits=[int(j==i) for j in range(12)];depth=0
        for a,b in network[21:]:
            depth += bool(bits[a] or bits[b])
            if bits[a] > bits[b]:bits[a],bits[b] = bits[b],bits[a]
        assert depth==2 and bits==[0]*11+[1]
    return {'boolean_inputs':8192,'residual_states':157,
            'marker_inputs_checked':4*(1 << 11),'pruned_prefix_sizes':[14]*4,
            'deleted_counts':[7]*4,'maximum_candidates':candidates,
            'maximum_kernels':3,'incumbent_kernel':merges}


if __name__=='__main__':
    print(json.dumps(check(),sort_keys=True))
