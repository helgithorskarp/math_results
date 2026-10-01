"""Complete fixed-shift cyclic13 triple-design generator, standard library.

Twenty-two13-block triple orbits and six pair orbits. Two halves of2048
subsets cover all2^22 simple invariant families exactly by pair signatures.
No full isomorphism census or design novelty claim. six-downset-2, researcher.
"""
from collections import defaultdict
from itertools import combinations


def mask(xs):
    return sum(1<<x for x in xs)


def translate(a,j):
    return mask((x+j)%13 for x in range(13)if a>>x&1)


def orbit_partition():
    triples={mask(t)for t in combinations(range(13),3)}
    groups={min(translate(a,j)for j in range(13)):
            frozenset(translate(a,j)for j in range(13))for a in triples}
    orbit=sorted(groups.items())
    assert len(orbit)==22 and all(len(o)==13 for _,o in orbit)
    assert sum(len(o)for _,o in orbit)==len(set().union(*(o for _,o in orbit)))==286
    assert set().union(*(o for _,o in orbit))==triples
    sig=[tuple(sum(int(a&(1|(1<<d))==(1|(1<<d)))for a in o)for d in range(1,7))
         for _,o in orbit]
    assert all(sum(s)==3 for s in sig)
    return orbit,sig


def half_subsets(signatures):
    out=[((0,)*6,0)]
    for i,s in enumerate(signatures):
        out += [(tuple(x+y for x,y in zip(v,s)),m|(1<<i))for v,m in out[:]]
    assert len(out)==1<<len(signatures)
    return out


def balanced_masks(lambdas=(4,5,6)):
    orbit,sig=orbit_partition();left=half_subsets(sig[:11]);right=half_subsets(sig[11:])
    lookup=defaultdict(list)
    for v,m in right:lookup[v].append(m)
    families={}
    for lam in lambdas:
        assert type(lam)is int and 0<=lam<=11
        out=[]
        for v,m in left:
            target=tuple(lam-x for x in v)
            out += [m|(n<<11)for n in lookup.get(target,())]
        assert all(a.bit_count()==2*lam for a in out)
        assert len(out)==len(set(out));families[lam]=sorted(out)
    return orbit,sig,families


def blocks_from_mask(a,orbit):
    assert type(a)is int and 0<=a<1<<22
    return sorted(set().union(*(o for i,(_,o)in enumerate(orbit)if a>>i&1)))
