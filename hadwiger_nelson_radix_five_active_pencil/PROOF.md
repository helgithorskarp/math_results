# Exact classification of the five-active residue-cover frontier

## 1. Inherited finite setting

For a noncircle displacement event in the five-digit radix architecture, the
256 additive F4 colour words fail on one affine hyperplane

```text
H(n,c) = {w in F4^4 : n dot w = c}.
```

HN3 h4135 and the independently accepted HN2 h4151 reconstruct 85 projective
normal directions and 340 theoretical affine hyperplanes. Exactly 336 types
are realized by noncircle event curves. The four absent types are
`H(e_j,0)`, one for each coordinate normal; these are the merged radial
monomials. A non-four-colourable active set must cover all 256 words.

The collision and unit-circle branches are already closed. HN2 h4167,
independently accepted at h4169, further removes 432 whole global pair systems
and supplies pair/triple incidence exclusions valid at all higher active
counts. We classify exactly five active noncircle curves after these filters.

## 2. Five-cover classification

We use the following elementary lemma with `q=4`.

**Lemma.** A set of `q+1` distinct affine hyperplanes covering `F_q^n` either
contains all `q` parallel sections of one direction, or is the full pencil of
`q+1` hyperplanes through one affine codimension-two flat.

**Proof.** If a parallel class has `q` members, those members already partition
the space and the first alternative holds. Suppose no class has `q` members.
Choose a listed hyperplane `H` and a parallel translate `J` which is not in
the list. If the parallel class of `H` has size `r`, those `r` hyperplanes miss
`J`. The other `q+1-r` hyperplanes cut `J` in hyperplanes. Covering the affine
space `J` needs at least `q` such sections, since each has one `q`th of its
points. Hence `r<=1`, and so every listed hyperplane has a distinct direction.

The other `q` hyperplanes cut `J` in exactly `q` sections. Equality in the
point-count bound forces these sections to be disjoint, hence parallel inside
`J`. Their normals modulo the normal of `H` are therefore proportional. All
`q+1` original normals lie in a common two-dimensional dual subspace and,
being distinct projective directions, exhaust its projective line.

Quotient by their common codimension-two direction. We obtain `q+1` affine
lines of distinct directions in `F_q^2`. Their total incidence count is
`q(q+1)`, so a cover of `q^2` points has excess `q`. If an intersection point
has multiplicity `m`, put `a=m-1`. Every pair of directions intersects once,
so

```text
sum a = q,
sum a(a+1)/2 = C(q+1,2).
```

Thus `sum a^2=q^2`. With nonnegative integers summing to `q`, equality is
possible only when one value is `q`; all lines are concurrent. Conversely,
all directions through one point cover the plane. Pulling back gives the
claimed pencil. QED.

There are `(4^4-1)/(4-1)=85` projective normal directions. The partition form
therefore gives `85*(340-4)=28,560` abstract five-sets. The number of
two-dimensional normal subspaces is the Gaussian binomial

```text
[4 choose 2]_4 = ((4^4-1)(4^4-4))/((4^2-1)(4^2-4)) = 357.
```

Each has 16 affine constant functionals, giving `357*16=5,712` pencils and
34,272 abstract five-covers in total.

Only 81 parallel partitions are fully realized, so the realized partition
branch has `81*(336-4)=26,892` sets. Among the pencils, 5,382 contain no missing
type, 324 contain one, and six contain two. Hence exactly 32,274 five-covers
use only realized signatures.

## 3. Removing the partition branch and lifting pencils

Every realized partition-plus-extra set contains four curves from the four
sections of a single projective normal. HN3 h4165 proves that no such quartet
is concurrent, even over the complex parameter plane and even when additional
curves are active. The partition branch is therefore impossible. Every
exactly-five-active possible counterexample must use one curve from each of
the five distinct directions of one of the 5,382 realized pencils.

The curve buckets over these signatures have sizes 2, 4, 8, or 16. Multiplying
the five bucket sizes in every pencil gives 136,094,976 raw curve quintets.
The complete support-profile census is recorded entrywise in
`certificate.json`.

All 3,006 h4151 K4 incidence sets use curves whose signatures have one common
projective normal. A pencil has five distinct projective normals, so none of
the h4151 sets can occur in a pencil lift. This exact orthogonality explains
why those accepted constraints do not further reduce the five-active layer.

The union of h4167's collision-forcing and monic-parameter pair rules has 8,376
distinct pairs. None occurs across two pencil buckets, so it removes zero raw
pencil lifts. Of h4167's 176,420 collision-forcing triples, the relevant ones
remove 3,862,080 lifts after overlaps are handled exactly. The remaining
count is

```text
132,232,896.
```

Every one of the 5,382 pencils retains at least one lift. This is a survivor
interface only: avoiding the known conjunctions does not prove that the five
event curves concur at a complex parameter, nor that a resulting physical
graph is non-four-colourable.

## 4. Effect on the global pair frontier

The h4117 quotient has 132,130 global pair-system representatives. The
accepted unit-circle result removes 342 and h4167 removes another 432, leaving
131,356 with conservative allowance 7,754,528.

For an exact-five-active parameter, the two curves of its pair system must lie
in one realized pencil. The classification gives:

| mode | pair orbits | conservative allowance |
|---|---:|---:|
| realized-pencil compatible | 128,616 | 7,585,472 |
| parallel signatures | 2,096 | 129,952 |
| pencil has an unrealized type | 644 | 39,104 |

Thus 2,740 pair orbits, allowance 169,056, move out of the exact-five layer and
require at least six active curves. They remain in the architecture-wide
frontier because a six-or-more cover need not contain a five-cover.

The checker applies every D3 curve action to every representative and verifies
that the three modes are invariant. It also finds a deterministic curve-level
extension avoiding all h4151/h4167 conjunctions for every one of the 128,616
compatible representatives. Consequently the current constraints do not
remove a further whole pair orbit from that mode.

As in h4117, the representatives are global: solving only these canonical
pairs is complete over the whole parameter plane. They must not be combined
with a simultaneous fundamental-chamber restriction; using the chamber
requires the full D3 closure.

## 5. Computation and trust boundary

The producer derives curve signatures from displacement residues and generates
pencils by two-dimensional algebraic spans. The verifier instead constructs
all 256 colourings, checks every actual event edge, and reconstructs each
pencil as the five theoretical hyperplanes containing a common 16-point affine
flat. They regenerate byte-identical 6,200,577-byte interfaces.

Both paths reconstruct the h4151 and h4167 interfaces from their checked source
rather than reading private exports. They use different predecessor producer
and verifier paths. The finite count uses CPython arbitrary-precision integer
bit sets; there is no floating point, randomness, CAS, SAT solver, or external
data. The controls exhaust all `C(20,5)=15,504` five-line subsets of `AG(2,4)`,
recovering 80 partition-plus-extra covers and 16 pencils.

The h4105 curve inventory, h4117 quotient, h4165 four-section nonconcurrence,
h4151/h4163 K4 interface, accepted h4139 circle closure, and independently
accepted h4167/h4169 incidence rules remain explicit dependencies. This package
is author-checked internal team evidence pending independent review. It establishes no physical
non-four-colourable member and no improvement to the 509-vertex record.
