"""Independent small-graph controls, basis identities and certificate faults."""
import copy
import itertools
import json

import geometry as producer
import independent_field as exact
import verify as v


def chromatic_three_by_inclusion_exclusion(n,edges):
    total = 0
    for mask in range(1<<len(edges)):
        roots = list(range(n))

        def find(x):
            while roots[x]!=x:
                x = roots[x]
            return x

        for k,(a,b) in enumerate(edges):
            if mask&(1<<k):
                roots[find(a)] = find(b)
        components = len({find(i) for i in range(n)})
        total += (-1 if mask.bit_count()%2 else 1)*3**components
    return total


def run():
    graphs = 0
    for n in range(6):
        possible = list(itertools.combinations(range(n),2))
        for mask in range(1<<len(possible)):
            edges = [e for i,e in enumerate(possible) if mask&(1<<i)]
            expected = chromatic_three_by_inclusion_exclusion(n,edges)>0
            model,_ = v.three_colour(n,edges)
            v.require((model is not None)==expected,'independent small graph control')
            if model is not None:
                v.require(all(model[a]!=model[b] for a,b in edges),'small positive model')
            graphs += 1
    products = 0
    for i in range(16):
        x = producer.basis(i)
        v.require(exact.double_change_basis(producer.conjugate(x))
                  ==exact.bar(exact.double_change_basis(x)),'conjugation basis control')
        for j in range(16):
            y = producer.basis(j)
            v.require(exact.times(2,exact.double_change_basis(producer.mul(x,y)))
                      ==exact.product(exact.double_change_basis(x),exact.double_change_basis(y)),
                      'independent basis multiplication control')
            products += 1
    v.require(632**2*33>3320**2,'mixed signature inequality')
    raw = (v.HERE/'certificate.json').read_bytes()
    certificate = json.loads(raw)
    first_four = next(i for i,row in enumerate(certificate['cases']) if row[3]==4)
    rejected = []

    def reject(name,mutation):
        trial = copy.deepcopy(certificate)
        mutation(trial)
        try:
            v.verify(trial)
        except (ValueError,KeyError,TypeError) as error:
            rejected.append({'case':name,'reason':str(error)})
        else:
            raise ValueError('accepted corrupt certificate: '+name)

    reject('boolean version',lambda x:x.update(version=True))
    reject('incomplete',lambda x:x.update(complete=False))
    reject('wrong family',lambda x:x.update(family='another family'))
    reject('wrong address order',lambda x:x.update(address_order='seed first'))
    reject('wrong seed hash',lambda x:x.update(seed_sha256='0'*64))
    reject('missing case',lambda x:x['cases'].pop())
    reject('duplicated case',lambda x:x['cases'].__setitem__(1,x['cases'][0]))
    reject('boolean centre',lambda x:x['cases'][0].__setitem__(0,False))
    reject('invalid base64',lambda x:x['cases'][0].__setitem__(2,'?'))
    reject('short word',lambda x:x['cases'][0].__setitem__(2,'AA=='))
    reject('monochromatic word',lambda x:x['cases'][0].__setitem__(2,'A'*59+'='))
    reject('wrong chromatic label',lambda x:x['cases'][0].__setitem__(3,2))
    reject('nonunit seed triangle',lambda x:x.update(seed_triangle=[0,1,2]))
    reject('duplicate lower address',lambda x:x['cases'][first_four][4].__setitem__(1,x['cases'][first_four][4][0]))
    reject('negative lower address',lambda x:x['cases'][first_four][4].__setitem__(0,-1))
    reject('boolean lower address',lambda x:x['cases'][first_four][4].__setitem__(0,False))
    reject('three-colourable lower core',lambda x:x['cases'][first_four].__setitem__(4,[0,1,2,3]))
    c = certificate['cases'][first_four][0]
    reject('coincident lower points',lambda x:x['cases'][first_four].__setitem__(4,[c,c+29,(c+1)%29,(c+2)%29]))
    # Nonzero unused high bits in the final byte must not be ignored.
    import base64
    def padding(x):
        word = bytearray(base64.b64decode(x['cases'][0][2]))
        word[-1] |= 128
        x['cases'][0][2] = base64.b64encode(word).decode()
    reject('nonzero padding',padding)
    original_roots = v.ROOTS
    try:
        v.ROOTS = (original_roots[0]+1,)+original_roots[1:]
        try:
            v.context()
        except ValueError:
            rejected.append({'case':'invalid residue root','reason':'residue equations'})
        else:
            raise ValueError('invalid root accepted')
    finally:
        v.ROOTS = original_roots
    return {'verified':True,'all_simple_graphs_through_five_vertices':graphs,
            'independent_basis_products':products,'conjugation_basis_vectors':16,
            'rejected_faults':rejected,'rejection_count':len(rejected)}


if __name__ == '__main__':
    print(json.dumps(run(),indent=2))
