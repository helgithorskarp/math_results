# Proof of the Galois-folding obstruction

## 1. The exact support and the complete action group

Let `t=exp(pi*i/21)` and `w=t^7=(1+i sqrt(3))/2`. Put

```
b = (w-1)/(t^6-t^(-6)) + w/(t^12-t^(-12)),
u_(2j)=t^j,  u_(2j+1)=b t^j       (0 <= j < 42).
```

These are Haugland's 84 labelled vectors. To compare with the Cartesian
definition, put `alpha=1/sin(2pi/7)`, `beta=1/sin(4pi/7)`. Then

```
b = sqrt(3)(alpha+beta)/4 + i(alpha-beta)/4.
```

Indeed `alpha=2i/(t^6-t^(-6))`, `beta=2i/(t^12-t^(-12))`,
`i(sqrt(3)+i)/2=w-1`, and `i(sqrt(3)-i)/2=w`.

Start each archived path at zero and append its successive partial sums,
retaining each distinct point at its first occurrence. This defines `G1`.
Its path endpoints are `2w-1=i sqrt(3)`. In the same insertion convention,
define

```
G2 = {w^(-1)z-1 : z in G1} union {w z+1 : z in G1},
r = (7+(2w-1)sqrt(5))/8,
G3 = G2 union {r(z+1)-1 : z in G2}.
```

These formulas give the archived labels and point counts 740, 1066, 2131.
The exact audit uses

```
Phi_42(X) = X^12+X^11-X^9-X^8+X^6-X^4-X^3+X+1.
```

It reconstructs these sets without importing previous code, checks all path
endpoints and all 12,530 recorded edge norms. The earlier strict-edge census
establishes that the recorded list is the full unit-edge list; completeness
is not needed here since preserving these edges alone suffices for the bound.

All complex points lie in `K=Q(t,sqrt(5))`, of degree 24. The cyclotomic
field `Q(t)` has degree 12 and is ramified only at 3 and 7. It cannot contain
`Q(sqrt(5))`, which is ramified at 5. Thus the automorphisms are exactly

```
sigma_(a,e)(t)=t^a, sigma_(a,e)(sqrt(5))=e sqrt(5),
gcd(a,42)=1, e in {1,-1}.
```

Their composition is `(a,e)(c,d)=(ac mod42,ed)`. Complex conjugation is
`(41,1)`, and commutes with all of them. A common automorphism consequently
preserves any unit distance: if `(z-y)conj(z-y)=1`, applying the automorphism
gives the same identity for its images. Each image is still a complex number
in the specified Euclidean plane. Different automorphisms at different
vertices need not preserve edges; edge preservation is the condition under
study, not an automatic property.

## 2. A sound finite reduction

The certificate uses

```
p=1000000009, t_bar=41285184, sqrt(5)_bar=383008016.
```

The verifier proves primality by trial division, checks that `t_bar` has
exact order 42 and that the square-root value squares to 5. All source
expressions and their conjugates can be evaluated: the denominators are
powers of two and products of `t^k-t^(-k)` for nonzero multiples `k` of six
modulo 42. Their reductions are nonzero because `t_bar^6` has order seven.

More formally, use `Z[T,S]/(Phi_42(T),S^2-5)` localized at two and these
denominators. Its rationalization is `K`; its monic quotient is free over
`Z`, so it embeds in `K`. Evaluation at the displayed roots gives a ring
homomorphism from this localized ring to `F_p`. It is not asserted to be a
homomorphism from the whole characteristic-zero field to a finite field.

For every point `z`, record the 24-component vector

```
q(z)_g = evaluation(g(z)),  g in Gal(K/Q).
```

Equality of physical points implies equality of these vectors. A field
automorphism permutes their coordinates, and conjugation gives the fixed
coordinate permutation `c=(41,1)`. A true unit edge implies, at every `g`,

```
(q(z)_g-q(y)_g)(q(z)_(gc)-q(y)_(gc)) = 1 in F_p.       (* )
```

Both implications are one-way. Distinct physical points may merge, and
nonunit pairs may pass the modular test. The finite constraint system is
therefore a relaxation of the geometric problem, which is the safe direction
for an order lower bound.

For each source vertex `v`, its finite domain `D_v` contains all distinct
coordinate permutations `q(sigma(z_v))`. The checker constructs every action,
not a sample, obtaining 6,049 sites and 355 orbits in this finite reduction.
On each archived edge it permits exactly the domain pairs satisfying all
24 conditions (*). Any actual edge-preserving folding induces a solution
of these constraints, using no more finite sites than physical points.

The independent Cartesian reconstruction uses a primitive 84th root
`139892774`, whose square is `t_bar`. Each exponent `a mod42` has a unique
lift `a or a+42` congruent to one modulo four. This extends the action to
`Q(zeta_84,sqrt(5))` while fixing `i`. The source's real-coordinate formulas
can therefore be used directly. The checker verifies the identities
`x=(q+q_c)/2` and `y=(q-q_c)/(2i)` at every source point and action.
The characteristic-zero audit independently reproduces the same full
24-component stream, with SHA-256

```
a44ff4236832ca6b4eb14a39c27cdc9b4eb2858bb01c8a780c30cb81e839ced8.
```

## 3. Complete normalization at one vertex

Let `v0=1069`. Its domain is its full 24-element orbit. For any actual
folding, write `f(v0)=tau(z_v0)`. Postcompose every image with `tau^(-1)`.
This retains all unit edges, all image coincidences and the image order;
each vertex is still mapped to one of its own conjugates. The resulting
folding fixes `z_v0`. This covers every folding without requiring the
automorphism to be a common geometric isometry.

The identical normalization is valid for the modular constraint problem:
coordinate permutations preserve (*) and act transitively on the anchor
domain. Thus fix its domain to `{q(z_v0)}`. No other image is pinned.

## 4. Safe elimination and the lower bound

For an edge `uv`, remove an image from `D_u` if it has no compatible image
in the current `D_v`. This cannot remove the image of any solution: that
solution's image at `v` would be a compatible witness. The argument is
inductive and valid for either simultaneous or sequential updates.

The checker performs complete simultaneous sweeps until no domain changes.
After nine changing sweeps, 29,983 values have been removed following the
anchor pin. All source identity images survive, providing a positive
consistency control. There remain

```
1,075 domains of size one;
1,056 domains of size six.
```

The certificate lists 1,251 distinct source vertices. Their remaining
domains are checked to be nonempty and pairwise disjoint. Whatever surviving
image is chosen for each of these vertices, these 1,251 images must all be
different. Hence every normalized solution uses at least 1,251 finite sites.
Sections 2 and 3 transfer that bound to every original physical folding.

No satisfiability or optimality assertion is needed about the remaining
domains. In particular, neither 1,251-image attainment nor a full solution
classification is claimed. The selected-domain certificate alone proves
that all images of order at most 1,250, including the target 508, are
impossible in this family.

## 5. Independence and boundaries

The private discovery used a direct complex modular formula, an AC-3 queue,
and orbitwise domain-cover minimization. The published checker uses
Cartesian formulas and simultaneous sweeps; it does not use that
minimization, importing neither discovery code nor its final domains.
Both final domain streams agree entry by entry. The independent rational
polynomial audit checks the exact source geometry and its reduction.

Controls exhaust small domain systems and all their compatible assignments
to check that a simultaneous revision never removes a solution. Malformed
arithmetic and domain witnesses are rejected. These controls support the
implementations; the universal soundness argument is the induction above.

The input's original path transcription, standard cyclotomic and Galois
facts, exact integer/rational arithmetic, implementation correctness and
ordinary execution remain trust boundaries. No proof-assistant or external
review claim is made. The graph's published five-chromatic result motivates
the construction gate; the present exclusion does not rely on that lower
bound and does not resolve its previously pending independent SAT proof.
