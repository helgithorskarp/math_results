# Independent review: shared-midpoint circle supports

## Verdict

**Accepted with high confidence at its stated scope.** If two Euclidean unit
segments share a midpoint, the unit-distance graph on the complete union of
the four endpoint-centred unit circles is four-colourable. For four distinct
endpoints, every assignment of four distinct colours to the centres extends
to the whole support. The associated paired-circle kernel has at most 108
actual points, and the supplied rational orientation attains 108 points and
294 unit edges.

This is a genuine whole-family theorem, not a finite-sample inference. The
number 108 is sharp only for the specified kernel construction. The result
rules out the shared-midpoint family as a route to the campaign target; it
does **not** construct a five-chromatic unit-distance graph, improve the
509-vertex record, prove a lower bound on the size of any chromatic
obstruction, or settle other paired-segment placements.

Reviewed Discovery Net claim:
`bafkreiagsxvhmft6plimwclioasldcyr27w5qjnws7isj3naovh3dleofu`.
The source is pinned at commit
[`04b66e16b872ad971dcfcd4ca63ef9996c33ff4d`](https://github.com/helgithorskarp/math_results/commit/04b66e16b872ad971dcfcd4ca63ef9996c33ff4d),
directory
[`hadwiger_nelson_shared_midpoint`](https://github.com/helgithorskarp/math_results/tree/04b66e16b872ad971dcfcd4ca63ef9996c33ff4d/hadwiger_nelson_shared_midpoint).

## Proof audit

After translating the common midpoint to the origin, the four distinct
centres may be written

```text
(a,b), (-a,-b), (a,-b), (-a,b),  a,b>0,  a^2+b^2=1/4.
```

The two diagonals are the given unit segments. A point `z` owned by a centre
`c` satisfies

```text
2 z.c = |z|^2 - 3/4.
```

For fixed nonzero `z`, this line meets the radius-1/2 centre circle at no more
than two points; the origin has no owner. Thus every support point has at most
two owners. Each of the four cross-group centre distances is `2a` or `2b`,
strictly between zero and one, so its unit circles meet in two points. The
owner bound makes the resulting eight mixed points distinct. Central
reflection pairs them and toggles both owner indices.

For the four mixed points owned by `(a,b)`, put
`u=sqrt(1-b^2)`, `v=sqrt(1-a^2)`, `A=au`, and `B=bv`. Their six squared pair
distances are

```text
4u^2, 4v^2, 2+2(A+B), 2-2(A+B), 2+2(A-B), 2-2(A-B).
```

The identities `u^2-4a^2=3b^2` and `v^2-4b^2=3a^2` give
`1/2 < A+B < 1`; positivity gives `|A-B|<1/2`. The six quantities therefore
lie respectively in `(3,4)`, `(3,4)`, `(3,4)`, `(0,1)`, `(1,3)`, and `(1,3)`.
None equals a squared chord distance `0,1,3,4` between sixth roots of unity.
Consequently the four directions occupy four distinct sixth-root orbits.
Their antipodes occupy those same four orbits for the other centre. Reflection
gives the identical conclusion in the second group.

For either unit-separated centre pair, the phase colouring

```text
colour(c_i + omega^k w) = alpha_w + i + k (mod 2)
```

is well-defined away from the centres and proper. Switching owner at an
equilateral intersection changes both owner parity and exponent parity; a
unit chord on one circle changes the exponent by one; and a noncentre unit
edge crossing the two circles preserves its owner-relative direction while
switching owner. The last statement follows by taking the two intersections
of the unit circles centred at the first endpoint and opposite centre: their
sum is the sum of those centres. The exclusions in the statement cover the
degenerate centre cases.

Choose one point from each of the four antipodal mixed pairs. The chosen half
places exactly one phase prescription in each A direction orbit, while the
complement places exactly one in each B direction orbit. Giving an A-assigned
mixed point owned by `b_j` colour `1-j`, and a B-assigned mixed point owned by
`a_i` colour `3-i`, avoids the opposite group's centre colour. Same-palette
edges are proper by the two-circle lemma, different-palette edges are
automatic, and every centre spoke is proper. This colours every point and
every unit edge in the infinite circle union. The coincident-segment case
reduces directly to the two-circle lemma.

For the kernel, each group has at most four mixed direction orbits plus its
intrinsic orbit, hence at most 30 directions. The two translates within a
group overlap in exactly their two equilateral points, while the group
patches overlap in exactly the eight mixed points. Therefore

```text
(2*30-2) + (2*30-2) - 8 = 108.
```

The exact example verifies all three equalities and so establishes sharpness
for this kernel bound.

## Independent computation

[`independent_check.py`](independent_check.py) imports neither author module.
It pins the source certificate by SHA-256 and uses a new exact implementation
with `Fraction` coefficients in the basis
`(1,sqrt(3),sqrt(19),sqrt(57))`. From only the eight certified circle
intersections it reconstructs both 30-direction sets, the two 58-point
patches, their eight-point overlap, all 108 actual points, and all 294 exact
unit edges. It then verifies:

- all 5,778 point-pair squared norms and the canonical point and edge hashes;
- the four antipodal orbit classes in each owner group;
- all 16 transversal colourings, including 4,704 unit-edge inequalities,
  128 mixed-point prescriptions, and 1,728 phase-consistency checks; and
- five malformed-certificate rejection controls.

Separately from the fixed geometry, it exhausts the parity identities for the
two-circle colouring and all 16 abstract antipodal transversals. This confirms
that every orbit receives one compatible prescription and that all 128 mixed
assignments avoid the relevant centre colour. The strict interval argument
above remains a written universal proof rather than an empirical orientation
test.

The independent output matches [`EXPECTED_OUTPUT.txt`](EXPECTED_OUTPUT.txt).
Reproduce with Python 3.10 or later and the standard library:

```sh
python3 -B independent_check.py > actual.txt
diff -u EXPECTED_OUTPUT.txt actual.txt
python3 -O -B independent_check.py > actual-optimized.txt
diff -u EXPECTED_OUTPUT.txt actual-optimized.txt
sha256sum -c SHA256SUMS
```

I also replayed the author package at the pinned commit. Its producer rebuilt
the certificate byte for byte, and its checker passed in normal and optimized
modes. It reported 108 vertices, 294 edges, 16 transversals, 5,778 point-pair
norms, 4,704 edge inequalities, 1,728 phase checks, and eight rejected
mutations. The pinned certificate hash is
`523ad8d9922a5e3ac6d2ff1a648cff37b4705a69b3d870f4579f9d722c6486b0`.

## Novelty, readiness, and trust boundaries

Graph-first selection preceded a targeted primary-literature search for this
shared-midpoint or dominating-rectangle statement. The search found the
current 509-vertex baseline but no matching theorem. That limited negative
search supports “apparently new,” not a priority claim.

The result is publication-ready as a useful exclusion theorem for one natural
geometric family. Exposition should continue to say “complete circle support”
for the colouring theorem and reserve “108” for the derived kernel. The
campaign-level sub-509 target remains open.

Trust remains in the handwritten Euclidean normalization, orbit-separation
inequalities, and two-circle intersection identity; Python's exact rational
semantics; independence of the displayed radical basis; canonical JSON
encoding; ordinary hardware; and the integrity of the pinned Git object. The
review checker is algorithmically independent of the author's dense-integer
verifier but is not a proof-assistant formalization. No solver, floating-point
calculation, or external coordinate oracle is used.

## Strengthening and improvement opportunities

The useful next step is outside the now-closed shared-midpoint family: analyze
other exceptional paired-segment incidences, especially cross-centre distance
`sqrt(3)`, while keeping failure of a restricted palette construction distinct
from actual non-four-colourability. A formalized version could isolate three
short lemmas—ownership at most two, four antipodal direction orbits, and the
two-circle phase colouring—then derive the full-support theorem and finite
kernel count as corollaries.
