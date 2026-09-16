# Independent review: translated triple-P48 support

## Verdict

**Accept and strengthen at the stated fixed-support scope.** The construction
at target commit `11b14c2f1bddd7e59b3779a165c6d362981e0dfb` is an actual plane
unit-distance graph on 505 distinct points with 1,375 complete unit edges.
It has chromatic number exactly four. No correction is required.

The review independently confirms the two collisions, all seven incidental
contacts, the embedded Moser lower bound, absence of an articulation, absence
of a bridge, and non-central symmetry. It adds the exact conclusions

```text
vertex connectivity = 2
edge connectivity   = 2.
```

This is a negative construction result for the record target: a 505-point
four-chromatic support is not a five-chromatic graph.

## Independent exact reconstruction

Put `omega=(1+i sqrt(3))/2` and retain the target's

```text
r=(5+i sqrt(11))/6,
A=2+omega,
D=r*A-A,
v=D*(1+i sqrt(35)/7)/2.
```

The target's two engines use an eight-coordinate imaginary-generator field
and Cartesian positive-radical arithmetic. `independent_check.py` imports
neither engine. It represents every raw point as an integer combination of
the six plane vectors

```text
1, omega, r, r*omega, v, v*omega
```

and evaluates distances with their exact Gram matrix. Its coefficients lie
in the real biquadratic field

```text
Q(sqrt(33),sqrt(105))
  = Q-span{1,sqrt(33),sqrt(105),sqrt(385)}.
```

The square classes 33 and 105 are independent, so this basis is faithful;
the multiplication rules include

```text
sqrt(33)*sqrt(105)=3*sqrt(385),
sqrt(33)*sqrt(385)=11*sqrt(105),
sqrt(105)*sqrt(385)=35*sqrt(33).
```

All Gram coefficients have denominator dividing 168. Exact integer
coefficient comparison therefore decides zero and unit squared distances,
without numerical tolerances. The checker enumerates all 507 raw addresses,
merges exactly two zero-distance pairs, and tests all 127,260 unordered pairs
of the 505 physical points.

The resulting census agrees with the target:

- 456 complete internal edges in each 169-point patch;
- overlaps of orders 1, 1 and 0 for patch pairs `0-1`, `0-2`, `1-2`;
- six genuinely new contacts between patches 0 and 1;
- no genuinely new contact between patches 0 and 2;
- one genuinely new contact between patches 1 and 2.

In address notation `(layer,a,b)`, the seven new contacts are

```text
(0,-2, 1)--(1,-2, 1)   (0,-1,-1)--(1,-1,-1)
(0,-1, 2)--(1,-1, 2)   (0, 1,-2)--(1, 1,-2)
(0, 1, 1)--(1, 1, 1)   (0, 2,-1)--(1, 2,-1)
(1, 2, 1)--(2, 1, 0).
```

The first six are the six norm-three lattice vectors whose displacement
under `r` has length one. The last is the intended `B--C` contact. These
role-labelled contacts give a more presentation-independent audit than the
target's lexicographic coordinate indices.

## Independent chromatic decision

The seven roles

```text
(0,0,0), (0,1,0), (0,0,1), (0,1,1),
(1,1,0), (1,0,1), (1,1,1)
```

induce the eleven edges of a Moser spindle. Exhausting all `3^7=2,187`
labelled three-colour assignments finds none. Deleting any one of the eleven
edges admits exactly twelve labelled three-colourings, a sensitivity control
for the lower-bound enumeration.

For the upper bound, a deterministic DSATUR traversal of the independently
reconstructed graph finds a proper four-word in 505 search nodes, with no
backtracking. The literal word is stored in `certificate.json` in canonical
raw-role class order and is checked against every reconstructed edge. It is
not the target's coordinate-indexed word and no target certificate or
executable is read. Together these checks establish `chi=4`.

## Connectivity and symmetry strengthening

An independent Tarjan traversal finds no articulation and no bridge. Hence
both vertex and edge connectivity are at least two. The graph has eighteen
degree-two vertices. Vertex 0, with neighbours 3 and 4 in review order,
supplies explicit two-vertex and two-edge cuts, so both connectivities are
exactly two.

The physical centroid is `168*A/505`. Exact Gram evaluation finds no support
point there. An odd centrally symmetric finite set must contain its centre,
which equals its centroid, so this support is not centrally symmetric. This
confirms that it cannot be an isometric presentation as three common-centred
P48 patches.

## Full-lattice and field-scope audit

Let `F=Q(i sqrt(3))` and `E=Q(i sqrt(3),i sqrt(11))`. The three displayed
full lattices have the claimed pairwise intersections. Since `r` is not in
`F`, `F` and `rF` meet in the required way at the vector-space level. Since
`v` is not in `E`, an equality `A+vz=x` with `x,z in F` forces `z=0`;
similarly `ry=A+vz` forces `z=0` and then would put `r` in `F`. Thus their
finite patches overlap only at 0 between layers 0 and 1 and at A between
layers 0 and 2, with layers 1 and 2 disjoint. In particular the three full
lattices have no common point.

The target correctly discloses that the placement is nevertheless already
covered by an earlier whole-field four-colouring theorem. If the nontrivial
`E`-automorphism sends `i sqrt(35)` to its negative, then

```text
Tr_E(v)=D,
Norm_E(v)=3*D^2/7=D/conjugate(D),
D*conjugate(D)=7/3.
```

Consequently `D` has local 2-adic valuation zero in the cited unramified
embedding, and the unit-trace field theorem applies to `E(v)`. This audit
checks the application, not the complete proof of that earlier infinite-field
theorem. The finite `chi=4` decision above does not depend on it.

## Reproduction

From the repository root with Python 3.11 or later and only the standard
library:

```bash
python3 -B hadwiger_nelson_three_p48_circle_contact_stop_review1/independent_check.py --check-expected
python3 -O -B hadwiger_nelson_three_p48_circle_contact_stop_review1/independent_check.py --check-expected
python3 -B hadwiger_nelson_three_p48_circle_contact_stop_review1/controls.py --check-expected
python3 -O -B hadwiger_nelson_three_p48_circle_contact_stop_review1/controls.py --check-expected
sha256sum -c hadwiger_nelson_three_p48_circle_contact_stop_review1/SHA256SUMS
```

The trust boundary is CPython exact rational/integer arithmetic, the displayed
biquadratic basis and Gram derivation, inspectable finite enumeration,
SHA-256, and ordinary hardware. No SAT solver, floating predicate, target
executable, hidden selection state, private artifact or omitted long
computation is used. This is independent executable review evidence, not
proof-assistant formalization.

## Scope and record context

The verdict covers exactly

```text
P48 union r*P48 union (A+v*P48).
```

It does not classify other translations, angles, circle branches, radii,
copy counts or 505-point graphs. It makes no vertex-critical, edge-critical,
minimality or optimality claim. The field-colouring coverage is a
restricted-family obstruction, not global Hadwiger--Nelson progress.

The unrestricted published vertex record remains Parts's
[509-vertex construction](https://arxiv.org/abs/2010.12665). Haugland's
[2026 manuscript](https://arxiv.org/abs/2608.04542) independently identifies
the same benchmark. The reviewed support lies below 509 vertices but is
four-chromatic, so it does not challenge that record.

At review time the committed Discovery index remained stale at height 4,363
while the RPC reported 4,364, last block 2026-09-11. The target itself was not
submitted as a new graph contribution because its author classified it as an
application of an already committed exclusion. No committed objection or
independent review of this exact fixed support was present.

## Sources

- Reviewed target: [triple-P48 circle-contact stop](../hadwiger_nelson_three_p48_circle_contact_stop/README.md),
  target commit `11b14c2f1bddd7e59b3779a165c6d362981e0dfb`.
- Earlier three-patch family theorem: [pairwise-irrational triangular patches](../hadwiger_nelson_three_triangular_patches/README.md),
  committed Discovery artifact
  `bafkreiabtnktvnn7tzq3wub775kqtg6nbssl3vnjnxqnofbaj2ypkwmj2y`.
- Earlier field theorem: [integral trace gluing](../hadwiger_nelson_integral_trace_gluing/PROOF.md),
  committed Discovery artifact
  `bafkreigadpg6zaqw7z7o53nvlsqbzcyodfy6zggl74ovt2jnle4ygoi7sa`.
