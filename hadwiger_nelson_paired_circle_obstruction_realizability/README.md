# The regular two-variable paired-circle phase obstruction is realizable

Consider four distinct planar centres paired into two unit segments, together
with the four complete unit circles about them.  The accepted
[`four-clause theorem`](../hadwiger_nelson_paired_circle_four_clauses/README.md)
constructs a four-colouring except when four signed orbit clauses have one of
two unsatisfiable Boolean forms.  The later
[`realized-phase result`](../hadwiger_nelson_realized_phase_obstruction/README.md)
realized the three-variable hub form by a continuous exact family and
explicitly left the two-variable form open.

**Exact result.  The two-variable form is also geometrically realizable in
the regular stratum.**  An explicit placement below has all four cross-centre
distances strictly between zero and two and different from `1` and `sqrt(3)`.
Its four actual circle-intersection clauses are

```text
(x=0 or y=0), (x=0 or y=1), (x=1 or y=0), (x=1 or y=1),
```

up to renaming the variables and their truth values.  Hence the coupled phase
formula has zero models.  Together with the preceding three-variable result,
both abstract obstruction types from the accepted classification are now
known to occur in exact Euclidean geometry.

The actual finite patch from the general
[`paired-circle kernel`](../hadwiger_nelson_paired_circle_kernel/README.md)
has **39 vertices and 102 unit edges**, and its chromatic number is exactly
**three**.  It nevertheless fails the kernel's sufficient lists: one patch
point is a common unit neighbour of all four centres, so four pairwise-distinct
centre pins leave it no colour.

This is a physical-realizability theorem and a negative construction gate,
not a five-chromatic graph.  The ordinary three-colouring does not colour the
full infinite circle support.  That full support remains unresolved because
the published continuum extension theorem requires the failed lists.  No
improvement to the 509-vertex record is claimed.

## 1. Exact placement

Put

\[
 \omega=(1+i\sqrt3)/2,
 \qquad (a_0,a_1,b_0,b_1)=
 \left(0,\frac{\sqrt3-i}{2},\omega-i,1-i\right).
\]

Both centre pairs are unit segments:

\[
 a_1-a_0=\frac{\sqrt3-i}{2},\qquad
 b_1-b_0=1-\omega.
\]

In slot order `00,01,10,11`, choose one intersection of the circles about
`a_i,b_j` by giving its unit directions `u` from `a_i` and `v` from `b_j`:

\[
 (u_{00},u_{01},u_{10},u_{11})=(\omega,1,\omega,1),
\]
\[
 (v_{00},v_{01},v_{10},v_{11})=(i,i,i\omega^{-1},i\omega^{-1}).
\]

Direct subtraction gives

\[
 u_{ij}-v_{ij}=b_j-a_i
\]

in all four slots.  Thus `a_i+u_ij=b_j+v_ij` is an actual common circle
point.  The other common point is its reflection in the midpoint of
`a_i,b_j`; the verifier reconstructs and checks both roots.

The four squared cross-centre distances are

\[
 (2-\sqrt3,\ 2,\ 2-\sqrt3,\ 2-\sqrt3).
\]

They belong to `(0,4)` and avoid `1,3,4`, so all cross pairs have two
distinct noncentre intersections and lie in the regular domain of the parent
four-clause theorem.

## 2. The two orbit clauses

Let `U={1,omega,...,omega^5}`.  Every displayed `u` lies in `U` and every
displayed `v` lies in `iU`.  These orbits are distinct: otherwise `i` would
be a sixth root of unity.  Consequently there are exactly two phase variables.

For a mixed root in slot `(i,j)`, write its two directions as
`omega^k x` and `omega^l y`.  The parent theorem assigns the clause

\[
 (X_x=1+i+j+k)\ \lor\ (X_y=i+j+l),
\]

with values modulo two.  Substitution of the four direction pairs gives all
four possible signed clauses on `X_U,X_{iU}`.  Their conjunction has no truth
assignment: for either value of the first variable, the two clauses with the
opposite first literal force contradictory values of the second.

The later independent-phase transfer lemma applies throughout the regular
stratum, so independently selecting the two groups' orbit phases does not
repair this placement.  More strongly, the older kernel lists fail for a
direct geometric reason.  The point

\[
 p=-i
\]

is at unit distance from all four centres.  Under the kernel prescription the
centres are pinned to `(2,3,0,1)`, leaving no colour for `p`.  This is an
obstruction to the lists and pins, not to ordinary graph colouring.

## 3. Exact physical patch and scope

For each cross pair, reconstruct both common points.  Rotate every
owner-relative direction through `U`, adjoin each group's intrinsic segment
orbit, translate the resulting direction set by both group centres, and merge
equal physical points.  This is exactly the finite patch in the published
kernel theorem.

Both direction sets have size 12.  Their four translates merge to 39 physical
points, with every one of the 102 exact unit edges included.  The certificate
contains a proper three-colouring.  Conversely `p,a_0,a_1` form a unit
triangle, proving that two colours do not suffice.  Therefore the patch has
chromatic number exactly three.

| exact quantity | value |
|---|---:|
| cross-orbit variables | 2 |
| phase assignments | 4 |
| satisfying phase assignments | 0 |
| direction-set sizes | 12, 12 |
| physical patch vertices | 39 |
| strict unit edges | 102 |
| ordinary chromatic number | 3 |
| common-neighbour centre incidences | 4 |

This theorem settles existence of a regular realization of the remaining
Boolean *type*.  It does not classify all placements realizing it.  Most
importantly, neither failure of the phase formula nor failure of the kernel
lists is an unrestricted chromatic obstruction.  The exact patch is
three-colourable, and the full four-circle support has not been coloured or
proved non-four-colourable here.

The falsifiable geometry boundary is therefore complete: trying to eliminate
the last Boolean case by Euclidean nonrealizability cannot work.  Any further
progress on this placement needs a new full-support extension allowing
repeated centre colours or another genuinely broader colouring mechanism.

## 4. Reproduction and independent verification

From the repository root, using CPython 3.11 or later and only the standard
library:

```sh
python3 -B hadwiger_nelson_paired_circle_obstruction_realizability/generate.py \
  --out /tmp/paired-circle-two-variable.json
cmp hadwiger_nelson_paired_circle_obstruction_realizability/certificate.json \
  /tmp/paired-circle-two-variable.json
python3 -B hadwiger_nelson_paired_circle_obstruction_realizability/verify.py --check-expected
python3 -O hadwiger_nelson_paired_circle_obstruction_realizability/verify.py --check-expected
sha256sum -c hadwiger_nelson_paired_circle_obstruction_realizability/SHA256SUMS
```

[`generate.py`](generate.py) uses separate real and imaginary coordinates in
`Q(sqrt(3))`.  It reconstructs the complete intersection patch, derives and
enumerates the phase formula, forms every physical unit edge, and searches for
the three-colouring stored in the certificate.

[`verify.py`](verify.py) imports no generator or parent executable.  It uses
the tensor basis `1,sqrt(3),i,i*sqrt(3)` and direct quotient-ring
multiplication.  It independently reconstructs the centres, both roots of
each circle pair, direction orbits, patch points and complete unit graph.  It
checks the formula by exhaustive truth assignments, validates every supplied
colour and edge, proves the triangle lower bound and four-centre ownership of
`p`, and rejects five malformed controls.

All equality and unit-distance decisions are rational coefficient comparisons
in a faithful basis.  The basis is linearly independent because `sqrt(3)` is
irrational and adjoining `i` to its real field is quadratic.  There is no
floating-point geometry, native solver, external coordinate file, unpublished
input or omitted proof trace.  The producer's search correctness is not a
proof dependency: the independent checker validates the positive colouring
directly.

The continuum interpretation and use of the accepted phase theorems are
unformalized mathematical dependencies.  The independent checker is
author-run, not external peer review.  No literature-priority claim is made.
