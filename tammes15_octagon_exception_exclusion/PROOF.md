# Saturation of the exceptional octagon bridge

**six-tammes-2 — researcher — 2026-09-30.** Complete author-audited,
unformalized geometric reduction with exact finite certificates and a
separate symbolic arithmetic implementation. Independent mathematical
review is pending. This is a conditional motif exclusion; global
Tammes-15 bounds are unchanged.

## Statements and hypotheses

For `1/2 < t < 3/5`, a packing means distinct unit vectors in R³ whose
different-point inner products are at most t. Let A prescribe the boundary
and noncrossing diagonals of a combinatorially triangulated octagon. Let B
be a combinatorially triangulated pentagon on **five other original
labels**, disjoint from the eight A labels. Both degree-two B ears have
prescribed contacts to a pair of A labels. A prescribed old neighbor of
an A pair is an A vertex adjacent to both through prescribed A edges.
Additional contacts and points are arbitrary. These triangulations need
not be geometric faces, and no symmetry, full contact graph or
triangle/quadrilateral decomposition is assumed.

**Local theorem.** If at least one attached A pair has no prescribed old
neighbor, there are at most thirteen points in the packing. The bound is
attained within this motif: there is exactly one thirteen-point Gram
configuration up to the indicated relabelings and orthogonal motion. Its
parameter is the unique root θ in `(1/2,3/5)` of

```
P(t) = -1 -17t -69t² +403t³ +4323t⁴ +10179t⁵ -24449t⁶
       -171609t⁷ -279635t⁸ +119709t⁹ +843073t¹⁰ +671593t¹¹
       -148047t¹² +348145t¹³ +1374277t¹⁴ +823837t¹⁵.
```

The thirteen-point configuration admits **no additional unit point**
whose inner product with each core point is at most θ. It is a saturated
core, not a new spherical packing record.

**Tammes-15 corollary.** No fifteen-point packing with separation strictly
larger than the known incumbent contains disjoint A and B as above, with
both B ears contacting arbitrary A pairs. In particular, the earlier
[355-case theorem](../tammes15_reflection_family_exclusion/PROOF.md) no
longer needs its prescribed-old-neighbor hypothesis. Original-label
disjointness remains a hypothesis; copies introduced by a fan
normalization do not establish it.

## Reduction to ten new cases

We use the preceding
[contact-pair closure theorem](../tammes15_contact_pair_closure/PROOF.md)
as a mathematical dependency. For a contact-triangulated octagon it says
that an external point contacting a pair without an old neighbor can
pack only for one dihedral triangulation/marked-pair type. Its edges are

```
01 04 05 06 07 12 13 14 23 34 45 56 67,
```

and its exceptional pair is E=`(2,7)`. There is exactly one compatible
external point at E for each t in the interval.

Every contact vertex has degree at most five: its contact neighbors on
the tangent circle have pairwise azimuthal separation at least
`arccos(t/(1+t)) > π/3`, so six cyclic gaps are impossible. This holds for
any number of packing points in the stated interval.

Every triangulated pentagon is dihedrally equivalent to B with edges

```
01 02 03 04 12 23 34,
```

and ears 1 and 4. The permutation `(0,4,3,2,1)` preserves these edges and
interchanges the ears. We may assign E to ear 1. Ear 4 cannot also attach
to a zero-old pair: closure would give E again, and its unique compatible
position would identify two distinct B labels. Nor can its A pair have
two old neighbors: a non-antipodal pair of unit points has at most two
unit common contact neighbors, already supplied by those distinct A
labels. An antipodal pair cannot have a common contact at t>0.

The remaining attached pair has exactly one old neighbor. Enumerating
all A pairs, and retaining only those for which adding both ears respects
the degree-five bound, gives exactly ten cases. In lexicographic order,
with each row `(i,j,old)`, they are

```
(1,2,3) (1,6,0) (1,7,0) (2,3,1) (3,4,1)
(3,5,4) (4,5,0) (4,7,0) (5,6,0) (6,7,0).
```

The checker regenerates this list, the ear-interchange automorphism, all
24 prescribed edges and the degree constraints. It also checks the
132 octagon triangulations by separate Catalan and noncrossing-diagonal
constructions, retaining 84 degree-compatible triangulations in eight
dihedral orbits. The closure dependency, rather than a guessed symmetry
or geometric occurrence assertion, identifies the exceptional model.

## Forced coordinates, radical and residual

Let `H=(1-t)I+tJ`. Its eigenvalues `1-t,1-t,1+2t` are positive on the
interval. Use an equilateral A anchor basis with Gram H, and coefficient
vectors `a0=e0, a6=e1, a7=e2`. Put `r=2t/(1+t)` and reconstruct

```
a5=r(a0+a6)-a7; a4=r(a0+a5)-a6; a1=r(a0+a4)-a5;
a3=r(a1+a4)-a0; a2=r(a1+a3)-a4.
```

These are forced by the two unit solutions at each old equilateral
triangle: reversing ear removal selects the solution distinct from the
old label. Thus every distinct A realization has these coefficients,
without an embedding or generic-rank premise. Write
`<x,y>H=xᵀHy`, `w=<a2,a7>H`, and

```
c=t/(1+w)(a2+a7),  n=H⁻¹(a2×a7),
Δ=det(H)(1+w-2t²)/((1+w)²(1-w)).
```

The contact-plane/unit-sphere intersections are `c ± sqrt(Δ)n`. Closure
certifies Δ>0 and that **only the plus position** packs with A. Thus the
first B ear is `u=c+sqrt(Δ)n`.

For a second pair `(i,j)` with unique old neighbor o, write
`wij=<ai,aj>H`. Its new neighbor distinct from o is forced to be

```
v=2t/(1+wij)(ai+aj)-ao.
```

An old common neighbor gives `1+wij ≥ 2t² > 0`. A tangent case gives no
new distinct point; retaining the formula still covers it. The checker
verifies the forced norm and contact identities and the divisor sign.
For B, the required ear inner product is

```
κ = t(9t²-2t-3)/(1+t)².
```

Set `α=<c,v>H-κ`, `β=<n,v>H`. The necessary unsquared equation is
`α+sqrt(Δ)β=0`, and hence the necessary rational residual is
`R=α²-Δβ²=0`. For cases 0 through 9 the checker certifies the exact
Bernstein signs of R as

```
+ + + + + - + + 0 -.
```

Here 0 means that this uniform sign test does not decide the function.
The nine strict signs exclude those cases over the entire open interval.
For case 8, `(5,6,0)`, the reduced numerator is **exactly** `(t-1)²P(t)`;
the denominator has a strict uniform sign. Exact signed Sturm sequences
certify one root in the whole interval and in the rational bracket

```
2196767/3802339 < θ < 535329/926590.
```

The endpoints have opposite P signs. Exactly 160 rational bisections
refine this fixed bracket; there is no adaptive “until successful”
precision or unreported parameter search.

For case 8, α<0 and β>0 uniformly. At θ the squared equation therefore
gives `sqrt(Δ)=-α/β` with the correct positive sign. Consequently
`u=c-(α/β)n` is a rational function of θ. The checker directly verifies
both unit ears, the exceptional contacts and `<u,v>H=κ`. This step
resolves the sign lost by squaring; an algebraic root alone is not
accepted as a packing.

## Both complete B realizations

At θ the fixed-ear Gram matrix is positive definite: `1-κ²>0`. An
H-isometry fixing their images has precisely two choices, corresponding
to its action on the one-dimensional orthogonal complement. For B
coefficient `bj`, put

```
β1j=<bj,b1>H, β2j=<bj,b4>H,
λj=det(H) det(b1,b4,bj)/(1-κ²).
```

Every possible B image is

```
xj(ε) = (β1j-κβ2j)/(1-κ²) u + (β2j-κβ1j)/(1-κ²) v
         + ε λj H⁻¹(u×v),                 ε ∈ {-1,+1}.
```

This follows by orthogonal projection on the two fixed ears and their
metric cross normal, whose squared H norm is `(1-κ²)/det(H)`. Both
handedness choices are included; there is no orientation assumption.

The ε=+1 realization fails packing at pair `(0,11)`, with dot strictly
larger than θ. The ε=-1 realization is a distinct thirteen-point packing:
all thirteen norms, all 24 prescribed contacts and all 78 different-pair
inequalities are checked exactly. There are exactly 24 contacts. Since
θ<1, those inequalities also prove label distinctness.

Arithmetic uses Q[t]/(P), with inverses produced by exact extended
Euclidean division. No irreducibility assertion about P is needed:
each modular identity is valid at θ, and every inverse identity excludes
a zero divisor value there. Nonzero signs use rational Horner enclosures
at the certified root bracket; unresolved signs would fail the checker.

## Complete extension obstruction

In the A basis an additional coefficient vector y must lie in

```
D = { y : aiᵀHy ≤ θ for i=0,...,12 }
```

and satisfy `yᵀHy=1`. Four core labels `(0,1,4,8)` have a strictly
positive convex combination equal to zero. The checker regenerates its
weights from alternating 3×3 cofactors, certifies their strict positivity
and verifies the exact origin relation. The nonzero cofactors also give
rank three. Any recession vector has four nonpositive dot products whose
positive weighted sum is zero; all four vanish, and rank three forces
the vector to vanish. Thus D is bounded. It is full-dimensional because
zero satisfies every inequality strictly.

Every vertex of this three-dimensional polytope has three independent
active constraints. The checker examines **all 286 triples**, using exact
Cramer solves and all thirteen feasibility inequalities. A singular
triple would be omitted only when its determinant is exactly zero; here
none is singular. A vertex with more than three active constraints is
covered by each independent triple, then deduplicated exactly. Pairwise
coordinate sign checks at the certified real root also prove that the
remaining quotient representatives are distinct as real vertices;
irreducibility of P is not assumed for this count. The complete partition is

| Active triples | Exact result |
|---:|---|
| 262 | Violates at least one core inequality |
| 24 | Feasible; gives 21 distinct vertices |

Every feasible vertex has squared H norm **strictly below 199/200**.
The squared norm is convex, so the same bound holds throughout D by
expressing each point as a convex combination of vertices. Hence D
contains no unit point. There is no additional point to append to the
valid thirteen-point core. This proves the local theorem.

## Strict-improvement corollary and limits

The known fifteen-point incumbent has cosine τ, the unique interval
root of `13t⁵-t⁴+6t³+2t²-3t-1`, with τ<3/5. For a hypothetical strict
improvement, fifteen disjoint open caps of half the separation give
`t ≥ 113/225 > 1/2`, and improvement gives `t<τ`. Thus the present
interval applies. These incumbent facts are certified in
[the earlier exact incumbent work](../tammes15_contact_pattern_obstruction/README.md).

If one attached A pair has no old neighbor, the local theorem forbids
fifteen points. Otherwise both have old neighbors, and the previous
355-case theorem forbids a strict improvement. This proves the corollary
without the old-neighbor premise. Its scope remains **strict improvement**:
the older theorem contains incumbent boundary cases and is not an
all-interval exclusion. No result here proves that an arbitrary optimum
contains disjoint original-label A and B. In particular,
[six-tammes-1's fan normalization](../tammes15_eight_quad_reduction/TOPOLOGY.md)
can reuse original vertices; its seven conditional profiles do not supply
that missing global occurrence or disjointness theorem.

## Reproduction, independent arithmetic and prior art

`python3 -B tammes15_octagon_exception_exclusion/check.py` regenerates
all ten residuals, the root certificate, both frames and the complete
extension polytope using only Python integer and Fraction arithmetic.
`--selftest` rejects false root, polynomial, orientation, witness,
tetrahedron and weak norm-bound certificates and checks Sturm endpoint
and multiple-root behavior. Assertions are not used as proof checks.
The compact certificate contains no coordinate or enumeration dump.

The optional SymPy1.14.0 generator reads no local kernel, certificate,
expected output, coordinate fixture, scratch file or network. It derives
the patch coordinates explicitly in a separate Q(t) representation,
uses SymPy root counts and ANP quotient arithmetic, checks both frames,
and independently repeats every extension triple and the same bound.
Its dot formula and arithmetic implementation differ from the checker.
It regenerates the certificate byte-for-byte. Mathematical formulas and
proof seeds are shared; this is separate arithmetic verification, not
independent mathematical review or proof-assistant formalization.

The [Cohn table](https://cohn.mit.edu/spherical-codes/) and
[current coordinate archive](https://spherical-codes.org/data/3/15)
retain the known unstarred fifteen-point entry; both were refreshed this
pass, with the coordinate bytes unchanged. [Musin–Tarasov](https://arxiv.org/abs/1410.2536)
proves the fourteen-point problem. Incumbent prior art includes
Kottwitz (1991), DOI10.1107/S0108767390011370,
[Buddenhagen–Kottwitz](https://web.archive.org/web/20210507001707/http://www.buddenbooks.com/jb/pack/sphere/toggles7.pdf)
Section4 pp7–11, and [Hars](https://www.hars.us/Papers/Numerical_Tammes.pdf)
Section10.15. No identical exception/saturation theorem was found in
bounded primary searches; no historical-priority or packing-record claim
is made. The new step closes the exceptional-pair boundary left by our
preceding contact-pair closure result.

Dependencies: contact-pair closure, source
d0e9574dd3699f4ab6fc636f84f43070d49903f7, graph h7430
`bafkreiglj3fpqibmepcmkilp6ykjz2qknysdepz3zlcrpi3hx7lry3nvmm`;
old-neighbor octagon/pentagon exclusion, source
335ef56bbea29fdf0071fee6521866c452b749e9, graph h7324
`bafkreiga3kccvkjwrb7ndahtn4bpxoqh5orgmhxd6r4ylw3hgdzn5rp3wu`;
incumbent relevance, source 7b0ad2db768b22ee83dc4ce4c92c2e7b142f1779,
graph h7170 `bafkreiclb5l3bki6mutmsa36pkkt4zw7hf4noeaqtjsa4wr7em3q7zchty`.
The latter two are corollary dependencies. Complementary h7412,
source b3995d988480906e6929caf25e465d74c359e734, is context only.
The remaining trust boundaries are the unformalized geometric argument,
the exact arithmetic software and ordinary Python execution.
