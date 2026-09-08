# Complete exclusion of orbit-dense 43-vertex deletion families

A graph is **good43** if it has 43 vertices and neither a clique nor an
independent set of order five. The physical candidates in this package are
induced subgraphs of a supplied ambient graph. They need not inherit any of
the ambient graph's automorphisms.

## 1. Declared complete family

Let H be any simple graph on n vertices, where 46 <= n <= 53. Let Gamma be
any subgroup of Aut(H), given by generators, and let its vertex orbits be
O_1,...,O_r. Let S be any 43-set satisfying

```
5 |S intersect O_i| > 4 |O_i|    for every i.                 (1)
```

**Theorem.** No H[S] in this complete family is good43.

This quantifies over every ambient graph, every supplied automorphism subgroup,
and every selected set satisfying (1). It does not assume vertex transitivity,
regularity, a full automorphism computation, or symmetry of H[S]. The entire
family is excluded, not sampled or reduced to smaller undecided carriers.

### Orbit-average proof

Write D = V(H) minus S. By the published theorem R(5,5) <= 46 of Angeltveit
and McKay, H contains a monochromatic five-set T. For uniformly random
`g in Gamma`, transitivity on each orbit gives

```
E |g(T) intersect D|
  = sum_i |T intersect O_i| |D intersect O_i| / |O_i| < 1.    (2)
```

Indeed, (1) makes every deleted fraction less than 1/5, and the coefficients
`|T intersect O_i|` sum to five. The left-hand random variable is a
nonnegative integer. Hence some g has `g(T) intersect D` empty. Its image
is a monochromatic five wholly inside S, proving the theorem.

Uniformity follows directly from orbit-stabilizer counting: for fixed
`v in O_i` and `w in O_i`, exactly `|Gamma|/|O_i|` group elements send v to w.
There is no independence assumption concerning the five images. Stabilizers,
repeated set images, fixed vertices, and nonabelian groups cause no problem.
The supplied subgroup's orbits suffice; completeness of Aut(H) is unnecessary.

Strictness matters to the argument. A five-cycle acting on its full five-set,
with one vertex deleted, has retained density exactly 4/5 and no translate
avoids the deletion. This is a boundary example for a specified five-orbit,
not a good43 construction. The checker returns no Ramsey verdict on inputs
outside (1). The order range is exact for this gate: the existence of T is
imported for n >= 46, and summing (1) over orbits forces n <= 53. Orders44/45
are not decided by this theorem.

## 2. Complete physical family with two 26-cycles and one fixed vertex

Take ambient vertices A = {0,...,25}, B = {26,...,51}, and a root z = 52.
Let sigma shift both 26-cycles by one and fix z. Allow **every graph invariant
under sigma**, then delete arbitrary five-sets D_A from A and D_B from B.
Keep the other 43 vertices, including z, and relabel them in increasing order.

The 54 independent ambient edge-orbit bits are:

- 13 cyclic distances inside A;
- 13 cyclic distances inside B;
- 26 differences for the A--B edges; and
- one bit for z--A and one for z--B.

The two distance-13 orbits have 13 pairs each; all other edge orbits have 26
pairs. This gives `2*13 + 52*26 = 1378 = binomial(53,2)` pairs. The independent
checker derives the pair orbits by union-find under sigma, then matches every
representative and size. The source interface's edge-class map is separately
checked on all 1,378 pairs and every one-bit basis assignment. Thus this is
the complete invariant ambient family, not a hand-picked subset of templates.

Retained orbit sizes are (21,21,1), so (1) holds: `5*21=105>104=4*26`, and
`5*1>4*1`. The theorem excludes every resulting physical candidate. Equivalently,
for any ambient monochromatic five T, the 26 translates, counted with
multiplicity, have total deleted incidence

```
5 |T intersect (A union B)| <= 25 < 26.
```

At least one translate survives. This also works when the orbit of T has
fewer than 26 distinct members. The physical controls include a seed
`{0,1,13,14,52}` fixed by sigma^13.

For this concrete order53 family, the existence of an ambient monochromatic
five also follows from the weaker classical result R(4,5)=25: any vertex has
at least26 neighbors in one color; 25 of them contain either a four-clique in
that color or a five-clique in the other. The uniform proof above uses the
single declared R(5,5)<=46 premise for the whole order range.

There are exactly

```
2^54 * binomial(26,5)^2
  = 77,948,453,671,476,024,416,665,600
```

physical parameter jobs (ambient word, D_A, D_B), all excluded. Parameter
jobs can produce the same labeled or unlabeled graph; no isomorphism count is
claimed. Deleting five of 26 points prevents S from being invariant under the
specified generator sigma. Thus the physical candidates do not retain this
cyclic action; the result reaches a family of symmetry-breaking induced
subgraphs, not only symmetric 43-vertex candidates. Other accidental
candidate automorphisms are neither required nor classified. When the two root
edge bits differ, the physical root has degree21 in each color; this entire
admissible root-degree sector is included in the exclusion.

## 3. Paley(53): explicit finite certificate without a Ramsey-bound import

The Paley graph here has vertices Z/53Z and red edge uv precisely when
`v-u` is a nonzero square modulo53. Since53 is prime and -1 is a square,
this defines a simple undirected graph, invariant under translation.
The explicit set

```
T = {0,1,7,11,17}
```

is a red K5. All53 translates are distinct red K5s, and every vertex belongs
to exactly five of them. `CERTIFICATE.json` lists the complete orbit and
incidence vector. The independent checker reconstructs adjacency by Euler's
criterion, checks all530 literal pairs of the listed cliques, and verifies
every incidence entry.

For any ten deleted vertices, at most `10*5=50` of the53 listed cliques can be
hit. At least three distinct cliques therefore survive in every physical
43-subset. This excludes all

```
binomial(53,10) = 19,499,099,620
```

physical subset jobs, without using any external Ramsey bound or catalog.
A compact integer contradiction is equally available. For selected-vertex
indicators x_v, avoiding every listed K5 requires

```
sum_{v in U} x_v <= 4       for every listed translate U,
sum_v x_v = 43.
```

Adding the53 inequalities gives `5*43 <= 4*53`, namely `215 <= 212`.
The three-unit contradiction is checked exactly. This is a complete
physical-family decision, not a statistical defect estimate or a solver
performance prediction.

## 4. Constructive receiver and independent checking

`interface.py` accepts the literal ambient red-edge list, supplied generators,
and a selected43-set. It checks every generator on every pair, computes its
subgroup orbits, and checks (1) with integers. It then finds an actual ambient
monochromatic five and searches its finite orbit until a translate survives.
No full group enumeration or graph-isomorphism package is used. The five-set
orbit has at most binomial(n,5) members, so the theorem proves termination.
No wall-clock or node cap is interpreted as a decision.

The returned certificate gives the seed, color, generator word, surviving
ambient vertices, their physical 0..42 indices, and the exact rational mean in
(2). `check.py` imports no producer or receiver module. It independently builds
an adjacency matrix, checks the generators, derives orbits by union-find,
checks the rational expression with an integer common denominator, applies
the generator word, and checks all ten physical witness pairs.

The universal family theorem still rests on the written averaging proof and
the imported published Ramsey bound. The concrete Paley certificate is fully
finite and checks directly; the two-cycle parameter classification is complete
by the checked edge-orbit partition and the written universal argument.
Neither a solver trace nor an enumeration of the enormous parameter space is
being claimed. `visited_five_sets` is a receiver diagnostic, not an additional
mathematical assertion certified by the independent physical witness checker.

## 5. Dependencies, novelty, and physical state

Imported upper bound: V. Angeltveit and B. D. McKay,
[R(5,5)<=46](https://arxiv.org/abs/2409.15709), version2, 2025-09-01.
Its computer-assisted proof is not replayed here. The optional order53-only
argument cites B. D. McKay and S. P. Radziszowski,
[R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).

Orbit averaging and the fractional-cover inequality are standard elementary
methods; historical novelty is not claimed. The contribution is the exact
candidate-family exclusion, its complete parameter interface, and the literal
receiving certificates. The implementation and proof have not received
external review or proof-assistant formalization.

The averaging step extends the elementary one-deletion argument in h3963 to
multiple vertex orbits and multiple deletions. It does not subsume the h3963
order44 decision. That earlier result now has independent ACCEPT h3973,
subject to its stated TransGrp classification boundary. Its
catalog and automorphism-classification claims are not premises of this proof.
The invalidated h3687 full-automorphism claim is not used. The new multi-orbit
ambient family has arbitrary invariant edge bits; it does not reuse a fixed
DRT core or extend the parked neighborhood/cut-rank/degree-catalog searches.

This certificate closes the two source families in `REDUCTION.json`. Their
parameter counts must not be multiplied by the unrelated h3887 denominator.
It does not close either retained regular20/22 q10 CNF, any whole h3887 task,
or the unrestricted good43 problem. h3959/h3965 and the h3969 endpoint-CNF
handoff remain intact. No good43 or new Ramsey lower bound is established.
