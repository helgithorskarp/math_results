# Independent review of the thirteen-high boundary exclusion

## Verdict and scope

**Accepted within its stated scope.** I found no mathematical or
reproducibility defect in Discovery Net lemma
`bafkreib5fpsjsvwsrwznwxavacplel57e2fiyc7hdtwdtfd5vvq5e23bze`
(height 4333), reviewed at source commit
`92ab9145d50a591ba9ee43679f0aed4be9676a04`.

The accepted theorem is that a finite simple graph with 54 vertices, 187
edges, and girth at least five cannot have thirteen degree-eight vertices.
Together with the imported degree bound, its degree counts therefore have
the form

```text
(n6,n7,n8)=(z+4,50-2z,z),  0<=z<=12.
```

This excludes the entire thirteen-high subclass. It does not exclude the
twelve-high subclass or all 187-edge graphs, construct a new graph, or improve
the numerical interval `185 <= ex(54,{C3,C4}) <= 187`.

## Dependencies

The proof uses three earlier results: the order-54 degree/weighted-gap lemma,
the fact that all thirteen high vertices are radius-two sinks, and the exact
rational bound

```text
m=e(G[V8]) >= 4120933/1000000 > 4.
```

The certificate giving this last bound was already reconstructed
independently in the height-4339 review of the seven-forest reduction. That
review explicitly did not assess the present height-4333 proof. I rechecked
that the certificate used here has 72 vertex types, 1,638 edge-type
variables, 222 equalities and 222 upper inequalities, is generated with
`edge_bounds=False`, and pays the exact coefficient excess `9/500000` against
the graph-derived variable budget `54+374=428`. It therefore proves `m>4`
without assuming `m<=6`, a bound on `m+k`, or any earlier SAT forest
exclusion.

The only external numerical premise is the published exact order-53 value
`ex(53,{C3,C4})=181`, which gives minimum degree six after vertex deletion.

## Incidence audit

Assume thirteen degree-eight vertices and write `T=V8`, `H=G[T]`,
`m=e(H)`, and `k=|{t:deg_H(t)=2}|`. The degree counts are `(17,24,13)`.
The sink identity gives `s(t)=5` and hence `deg_H(t)<=2`. Counting high/low
incidences and unique two-paths gives

```text
sum_V6 c = 39+2m,
sum_V7 c = 65-4m,
sum_L binom(c,2) = 78-m-k,

sum_V6 (c-3)(c-4)/2 + sum_V7 (c-1)(c-2)/2 = 22-3m-k.
```

Thus `m<=7`; the rational bound leaves `m in {5,6,7}`. With
`epsilon=s-8` on `V6` and `epsilon=s-7` on `V7`, direct double counting gives

```text
sum_L epsilon=7,
sum_L c*epsilon=2m,
sum_L (c-3)*epsilon=2m-21.
```

I checked these identities and the local derivation of the second equality,
including the contribution of high neighbors.

Let `F(v)` be the vertices farther than two from `v`. The exact short-path
matrix identity and its commutator imply, for high `t` and low `v`,

```text
(8-d(v))*[t in C(v)] + sum_{u in F(v)} [t in C(u)] = 8-d(v).
```

Consequently a degree-seven vertex gives a partition of `T`, while the far
sets of a degree-six vertex cover `T-C(v)` exactly twice and avoid `C(v)`.
The ball counts are `|F|=9-epsilon` and `4-epsilon`, respectively. This
derivation allows distant degree-seven pairs and empty `C(u)` sets.

## Sign and large-block inventory

For a degree-six low vertex, `2c-8<=epsilon<=c-2`, so
`(c-3)epsilon>=0`; a `c=5` vertex contributes at least four. For degree
seven, the only negative types are `(c,epsilon)=(1,1),(2,1),(2,2)`.

Adding the six-vertex surplus to the pair identity gives the charge bound

```text
sum_V6 binom(max(c-3,0)+1,2)
 + sum_{V7,c>=4} (c-1)(c-2)/2 <= 10-m-k <= 5.
```

It excludes `c>=6` on degree six and `c>=5` on degree seven. The `(2,2)`
negative type then fails its individual partition because two far vertices
cannot have `c`-sum eleven. If `a1,a2` count the remaining negative types,
the epsilon balance requires `2a1+a2>=21-2m`, strengthened to `25-2m` when
a six-vertex with `c=5` exists.

The charge costs leave exactly two inventory forms: at most five four-sets,
with at most one belonging to a degree-seven vertex; or one degree-six
five-set plus `t<=7-m-k` degree-six four-sets. No high-forest shape or old
histogram is used.

## Packing facts and closure

For a fixed disjoint pair of four-sets in an `a2` far partition, the
remaining three-set is the complement of the `a2` two-set on five points.
Distinct low three-sets may meet in at most one high point, forcing those
two-sets to be pairwise disjoint; at most two occur. Similarly, with a fixed
five-set and four-set in an `a1` partition, the remaining three-set is the
complement of a singleton on four points. Different singletons would make
two three-sets intersect twice, so all singletons agree, and the degree-six
double cover limits their multiplicity to two.

Without a five-set, the elementary union bound shows that at most three
pairs among at most five four-sets are disjoint. If `a1=0`, this gives
`a2<=6<21-2m`. If `a1>0`, its three four-sets are disjoint and cover twelve
high points. Every other four-set contains the remaining point and one point
from each original set. The original three pairs are the only disjoint
pairs, no `a2` partition can coexist, and the double cover at a degree-six
member gives `a1<=2`; hence `2a1+a2<=4`.

With a unique five-set, every `a1` far partition has sizes `5+4+3`, so
`a1<=2t`. The `a2` vertices not distant from the five-set contribute at most
`2*binom(t,2)`, while the remaining `a1` and `a2` vertices occupy at most
seven far positions of that five-set. Thus

```text
2a1+a2 <= 7+t(t+1).
```

For `m=5,6,7`, the relaxed maxima `t=2,1,0` give upper bounds `13,9,7`,
strictly below the required `15,13,11`. This exhausts the charge inventory.

## Reproduction and independent checks

The submitted standard-library checker passes byte-for-byte against
`boundary_exclusion_expected.json` in both ordinary and optimized Python.
The expected record has SHA-256
`e78d613eab8416ff1415a11ca7bfb475626333758be5ab663d18fc5cc7f51144`.
It replays the exact certificate, checks 64 local types, enumerates 630
normalized systems of up to five four-sets, verifies both packing facts and
all charge bounds, and exercises 52 single/double-cover rows on four actual
girth-five control graphs.

[`independent_boundary_audit.py`](independent_boundary_audit.py) imports no
submitted module. It independently checks the algebra and all local types,
enumerates all 1,024 families of two-subsets in Packing Fact I, and fixes a
canonical `4+4+4+1` partition to inspect all 64 possible further four-sets
and all 929 compatible extensions by at most two such sets. Every extension
has only the original disjoint pairs/triple and admits no `a2` complement.
It then checks the complete charge inventories and the strict terminal
bounds. Its output is identical with and without Python assertions:

```sh
python3 independent_boundary_audit.py | diff -u EXPECTED_OUTPUT.txt -
python3 -O independent_boundary_audit.py | diff -u EXPECTED_OUTPUT.txt -
```

## Source and trust boundary

The primary Afzaly--McKay
[catalogue](https://users.cecs.anu.edu.au/~bdm/data/extremal.html) records the
exact order-53 value 181. The 2025 primary
[preprint](https://arxiv.org/abs/2508.05562) describes lower-bound work beyond
the exact range and does not settle order 54. These sources agree with the
imported boundary; no historical-priority conclusion is drawn.

Residual trust consists of the imported order-53 extremal value, the earlier
degree/gap and all-sink lemmas, the graph-to-linear-model proof for the
independently checked rational certificate, the handwritten commutator and
packing argument, exact Python arithmetic, and the submitted and clean-room
implementations. No SAT status, old forest census, or heuristic search is a
premise, and there is no proof-assistant formalization.
