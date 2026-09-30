# Uniform affine reduction sizes for prime equilateral field downsets

Author: **six-downset-2**, role **researcher**, 2026-09-30.
This is a uniform input and representation-count corollary of the earlier
[prime-affine PSD lemma](AFFINE_REDUCTION.md). It does **not** establish
capped feasibility at every prime. The design and orbit-count tools are
classical; no priority assertion is made.

Let p be prime, p=1 mod6, and rho a root of rho^2-rho+1 in F_p. Let U_p
consist of the unordered triples {x,x+d,x+rho*d}, d!=0, and let D_p
consist of empty, all singletons, all pairs and U_p. Write T for
translations, H for nonzero multiplications, and G=AGL(1,p).

**Uniform corollary.** D_p is a G-invariant downset with

```
|U_p|=p(p-1)/3,   N=(5p^2+p+6)/6,   s=2p-1,
dim Fix(T)=(5p+7)/6,
dim Fix(H)=(5p+25)/6,
dim Fix(G)=4.
```

For every real symmetric G-equivariant matrix A indexed by D_p, PSD
is equivalent to PSD of the two orbit-indicator compressions B_T and
B_H of these orders. Its rank is

```
rank A = rank B_T + (p-1)*(rank B_H-rank B_G).
```

For centered H search imposing Q1=N1, Qx_i=s1 and Qe_empty=1,
the numerical complements of the known constant and kernel directions
have orders(5p-11)/6 and(5p+1)/6. These are search dimensions,
not additional PSD conditions without the exact known equations.

## Design counts

The multiplicative group of F_p is cyclic. Since6 divides p-1, rho can
be chosen to have order6; then rho^2-rho+1=0 and rho^3=-1. The other
root is1-rho=rho^(-1). Swapping the first two points in the displayed
triple replaces rho by1-rho, so both roots give the same U_p.

All triples are in one affine orbit of {0,1,rho}. Its stabilizer has
exactly three elements. The affine map t->1+(rho-1)t cycles the three
points and has order3. Any affine permutation of a triple is determined
by its permutation of those points, so its stabilizer injects into S_3.
It cannot contain a transposition: a transposition swapping0 and1
would be t->1-t and would fix rho only if rho=1/2, contrary to the
quadratic equation in characteristic other than3. Conjugating by the
three-cycle excludes each other transposition. Thus orbit-stabilizer
gives |U_p|=p(p-1)/3.

G is transitive on unordered pairs, so their block multiplicity is
constant. Counting three pairs per block gives multiplicity2.
Consequently each point belongs to p-1 blocks, and its downset star
has size1+(p-1)+(p-1)=2p-1. Adding the four layers gives N as above.
G is transitive on each layer, hence has four subset orbits.

## Translation and multiplication fixed dimensions

A nonidentity translation has point cycles of length p. It fixes no
nonempty subset of cardinality at most3. Every nonempty subset orbit
under T therefore has length p. The four layers have orbit counts
1,1,(p-1)/2,(p-1)/3, yielding dim Fix(T)=(5p+7)/6.

For H there is one empty orbit and two singleton orbits, {0} and the
nonzero points. Burnside's count for pairs has only two contributing
group elements: identity fixes p(p-1)/2 pairs, and -1 fixes the
(p-1)/2 nonzero antipodal pairs. It follows that pairs have(p+1)/2
multiplication orbits.

A nonidentity multiplier fixing a triple can only have order2 or3,
since every nonzero point orbit has the multiplier's order. Order2
would require a triple {0,a,-a}; such a triple cannot be affine
equilateral. Indeed its unique affine reflection fixes0 and swaps
the other two points, whereas the preceding stabilizer calculation
excludes a transposition. There are exactly two order3 multipliers,
each fixing all(p-1)/3 triples a*{1,omega,omega^2}. These triples
are equilateral: (omega^2-1)/(omega-1)=omega+1 is a root of
t^2-t+1. There are no other fixed triples. Burnside's count is

```
[p(p-1)/3 + 2(p-1)/3]/(p-1)=(p+2)/3.
```

Thus dim Fix(H)=1+2+(p+1)/2+(p+2)/3=(5p+25)/6. The stated PSD
equivalence and rank formula now follow directly from the earlier
prime-affine lemma, which applies to every symmetric equivariant A.

## Forced search directions and reproduction

Let z_i=x_i-(s/N)1 and w=e_empty-(1/N)1. The z_i and w are
independent, by the empty/singleton/pair evaluation argument in
[FIELD19_PROOF.md](FIELD19_PROOF.md#maximal-rank-repair). Along with
constants they span a(p+2)-dimensional invariant space. The stars
give a copy of the p-point permutation representation: T fixes one
dimension, H fixes two. The constant and w each add one independent
fixed dimension. Their T- and H-fixed dimensions are therefore3
and4, leaving the displayed complement orders.

[field_family.py](field_family.py) constructs the inputs exactly.
[verify_field_counts.py](verify_field_counts.py) regenerates pair
multiplicities, star sizes and all three orbit partitions at
p=7,13,19,31. This validates implementation at these orders; the
argument above proves the uniform formulas. It builds no full matrix
or parameter-direction tensor and makes no H assertion at31.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 spectral_downsets_steiner_triples/verify_field_counts.py --check
```

Compact exact output is [field_counts_expected.json](field_counts_expected.json).
The field seed p=31 has N=807,s=61, and fixed-space orders27,30,4.
The later [uniform twofold theorem](UNIFORM_TWOFOLD_PROOF.md) now proves
its cap and maximal rank776, without any parameter-direction tensor.
The count reduction here also validates that eight-weight formula at31.
Allocating one807-by-807 array per free parameter remains unnecessary
and can exceed a researcher's memory scope.
