# Single-anchor field escape: the individual colour gate fails

No five-chromatic graph or vertex-record improvement is claimed. This package
settles the individual-copy gate for a proposed physical construction on at
most 508 points. Interacting copies remain open.

Let alpha=i sqrt3, beta=i sqrt11, E=Q(alpha,beta), and K=E(sqrt5).
Let M be the standard seven-point Moser spindle and G the ten-point Golomb
unit graph given in `common.py`. Fix the exact 490-point seed

```
u = (7 + alpha sqrt5)/8,
v = (-1 + alpha sqrt5)/4,
B = G + u M + v M.
```

The complete strict unit graph on B has 2435 edges and a checked four-colouring.
This is the GMM seed from the preceding
[mixed-atom package](../hadwiger_nelson_mixed_atom_record_search/README.md).

**Exact finite result.** Let C be a congruent or reflected copy of M or G
that shares a point p with B. Require its unit multiplier to lie outside K,
and require at least four distinct old vertices, including p, to be incident
with its new vertices. Then **every proper four-colouring of B extends to
B union C**. In fact the extension works for every assignment of four
colours to those old contact vertices, even without requiring that assignment
to be proper on the old boundary.

There is exactly one shared point: a second coincidence would express the
multiplier as a quotient of two nonzero K elements. Thus one M copy adds six
points, and one G copy adds nine. The prospective record-sized constructions
were B plus three M copies, or B plus two G copies; both have at most 508
points after exact collision merging. The result does **not** exclude these
unions, because edges and coincidences between new copies can couple them.

| Motif | Contact equations | Retained modular groups | Outside-K polynomial cases | Old boundary sizes | Certificate templates |
|---|---:|---:|---:|---|---:|
| M |20,127,240|29,888|1,672|4|8|
| G |43,129,800|82,941|5,424|4 or5|48|

These are counts of anchored, oriented polynomial recipes. Each irreducible
polynomial has two physical unit roots. Symmetries can duplicate physical
copies; the table does not count distinct physical graphs. No quotient by
unproved symmetry is used in the census.

The public certificate gives an extension for each possible old-boundary
colour pattern, including the restriction of the archived seed word. The M templates
cover 120 canonical/2048 labelled assignments; the G templates cover 1152
canonical/21504 labelled assignments. The certificate is checked directly
on every labelled assignment, including colour-name permutations.

## Exact reduction and completeness

All arithmetic uses rational coefficients in the specified radical basis.
Write an anchored motif as `p + z b_j`, where `b_0=0` and `|z|=1`.
For an old point r different from p put `a=p-r`, `c=conjugate(a)*b_j`,
and `h=|a|^2+|b_j|^2-1`. Since a and b_j are nonzero, c is nonzero.
The contact equation is exactly

```
c z^2 + h z + conjugate(c) = 0,
z^2 - T z + J = 0,
T = -h/c,   J = conjugate(c)/c.
```

If z lies outside K, this quadratic is irreducible over K. Every other
old-to-new contact must therefore give the same monic polynomial. The
census considers every old anchor, both motif orientations, every motif
anchor and every nonzero motif offset, against every other old point.
A qualifying placement has at least three distinct non-anchor old contacts,
so its polynomial must be in one of the retained groups.

For each witness equation set `D=4|a|^2|b_j|^2-h^2`. Physical outside-K unit
roots exist exactly when D is positive and D/3 has no square root in the real
subfield Q(sqrt33,sqrt5). They are

```
z = T/2 +/- alpha sqrt(D/3)/(2c).
```

Both have modulus one and the same contact graph. D=0 gives a K root;
D<0 gives no unit root. The nested quadratic square-root test in `common.py`
is complete: for `(x+y sqrt5)^2=A+B sqrt5`, it tests both signs of the square
root of `A^2-5B^2` in Q(sqrt33), then tests the corresponding rational
quadratic square roots. Zero-component cases are handled separately.

To avoid rational divisions on 63 million equations, the first grouping is
in the prime field of order1,000,000,021. Primality is checked by trial
division and the three radical images are verified by squaring. Every
original rational denominator, every conjugate seed difference and every
nonzero motif offset has nonzero image. Thus equality of exact monic
polynomials implies equality of modular keys. A modular collision can add
work but cannot discard a qualifying exact group. Every retained group is
then partitioned by its full exact T,J pair. In this run no retained group
split: all 29,888 M and 82,941 G groups were exact single groups.

The inside-K / no-outside-root / outside-K partitions are respectively
27,598 /618 /1,672 for M and74,937 /2,580 /5,424 for G. Complete old-to-new
adjacency follows from exact polynomial equality; adjacency to the shared
anchor is determined by `|b_j|=1`. Internal adjacency follows from the motif
isometry. No sampled distance test enters this reduction.

## Certificate and physical controls

For each case, delete the shared anchor from the motif. Record the induced
new-vertex graph and, for each old boundary vertex, its new-neighbour bit
mask. Sorting the old masks merely relabels boundary vertices. Equal such
templates have exactly the same list-extension question. The public positive
certificate gives a new-vertex colouring for every canonical old-colour
assignment. The checker enumerates all labelled old assignments and checks
every new edge and every contact directly. It also requires exact template
coverage of the regenerated census.

`verify.py` separately rebuilds all 119,805 seed pairs using the real-coordinate
metric `x^2+3y^2` in Q(sqrt33,sqrt5), checks the archived seed word, and
constructs one actual outside-K image for each motif. For those 496- and
499-point fixtures it checks every old-to-new and new-to-new pair in the
16-dimensional radical representation. Exact unit norm, quadratic identity,
distinctness, irreducibility, contact completeness and a full physical
four-colouring are checked. Six corrupted positive-certificate controls
must fail; twenty exact-square extraction controls must pass.

The full modular census was replayed with undefined-behaviour checking and
compared entry by entry against a Python reference enumeration. Signed
native products are below `(1,000,000,021)^2 < 2^63`; hash multiplication uses
unsigned arithmetic. There is no floating-point or SAT verdict in the
certificate trust boundary. This is author-side verification, not external
review or a formal proof-assistant theorem.

## Reproduce

Use a complete checkout with the two dependencies hash-pinned in
`SOURCE_PINS.json`. CPython 3.11.2 and g++ 12.2.0 were used; only the Python
standard library is needed. From this directory, create a fresh work path:

```sh
mkdir -p /tmp/hn-single-anchor
c++ -std=c++17 -O2 -Wall -Wextra -fsanitize=undefined -fno-sanitize-recover=all mod_census.cpp -o /tmp/hn-single-anchor/census
python3 -O -B census.py --work /tmp/hn-single-anchor --native /tmp/hn-single-anchor/census --reference
python3 -O -B verify.py --work /tmp/hn-single-anchor
python3 -B build_certificate.py --work /tmp/hn-single-anchor
cmp certificate.json /tmp/hn-single-anchor/certificate.json
sha256sum -c SHA256SUMS
```

The census commands write complete transient streams into the work path.
`EXPECTED.json` pins their canonical exact-record hashes and the compact
verification result; `VALIDATION.json` records the measured replay.
The certificate producer is optional for checking, but its deterministic
output should match byte for byte. Raw census streams and logs stay outside
Git. Failure, singular reduction, incomplete output or certificate mismatch
raises an error; no such run is a completed exclusion.

## Construction decision

The first checkpoint required a new individual-copy colour obstruction
before a larger host or combination search. Both motifs fail that gate in
the strongest boundary sense above. No Moser host or Golomb pair search was
launched, and no computation remains running at this checkpoint.

This does not close contacts with fewer than four old boundary vertices,
phases inside K, other motifs, different seeds, or interacting new copies.
A concrete next test should require a *joint* colour obstruction from two
outside-K anchored Golomb copies with mutual unit edges, while keeping their
physical union within508 points. Its exact field compositum, cross-copy
collisions and all cross-copy edges must be reconstructed before promotion.
The isolated-copy result provides a filter: any such obstruction must use
those interactions. [JOINT_FILTER.md](JOINT_FILTER.md) proves that points in
different quadratic extensions can be unit adjacent only at a common
root-pair midpoint, with perpendicular displacements whose squared radii
sum to one. It supplies the exact next census filter. That proposed paired
construction has not been tested.

The unrestricted comparison remains Parts's 509-vertex/2442-edge construction
([primary paper](https://arxiv.org/abs/2010.12665)), still identified as the
record in [Haugland's 2026 manuscript](https://arxiv.org/html/2608.04542v4).
Sources were refreshed on 2026-09-13. The native-host independent review, T375 degree-four/five closure, and the
new fixed native503-plus-five repair closure at eec9c10 were consumed for
coordination. The last result retires that particular R2 repair family;
it does not close R2 geometry changes or this single-anchor lane. Discovery Net's local committed index was stale at 4363, so
post-cutoff evidence came from the authorized durable repository. Pending
broadcasts are preserved as pending, with no resubmission.
