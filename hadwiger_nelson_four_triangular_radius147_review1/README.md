# Independent review: four concurrent P147 patches

## Verdict

**ACCEPT with high confidence for the exact restricted-family theorem**, at
target mathematical commit
`53386581d0ba3df106e7c3a6dc96bda335e27ef5`.

Let

```text
omega = (1+i*sqrt(3))/2,
P_N = {a+b*omega : a^2+a*b+b^2 <= N}.
```

For arbitrary unit complex numbers `alpha_0,...,alpha_3`, the complete strict
plane unit-distance graph on the physical union of the four concurrent
patches `alpha_i P_147` is four-colourable. Equal physical points are merged
and every pair at distance exactly one is an edge.

The exact record-relevant corollary is also accepted: every four translated,
rotated, or reflected copies of `P_36` with a common physical point have a
four-colourable complete strict unit-distance graph, on at most 505 vertices.

This is a continuum restricted-family exclusion. It is not a global lower
bound, does not produce a five-chromatic graph, and does not improve the
unrestricted record.

Reviewed package:
[`hadwiger_nelson_four_triangular_radius147`](../hadwiger_nelson_four_triangular_radius147/README.md).
The substantive independent-review source is commit
`bea545fe011a3fbe9497391ddb74569d884e8599`.

## Proof reduction audited

The residue `r(a+b*omega)=a-b mod 3` splits each patch into two disjoint
two-colour palettes. A layer has a sign bit for its two nonzero residue
classes and a zero-class bit for its nonorigin zero-residue points; the common
origin has a fixed colour. Internal unit edges are proper for every choice.
Every cross edge or collision imposes at most one XOR equation in each bit
channel, while a mixed-residue edge is automatically proper.

For nonzero `u,v`, the condition `|u-beta*v|=1`, with
`beta=x+i*sqrt(3)y`, is exactly a rational line in `(x,y)` intersected with
`x^2+3*y^2=1`. The independent checker derives its zero, one, or two roots
from every ordered point pair. Origin contacts are treated separately and
collisions are independently generated from equal-norm ratios. Hence the
finite inventory covers every relative rotation at which the strict physical
graph changes.

After identical physical patch sets are contracted, an inconsistent XOR
system on at most four layer vertices has a shortest inconsistent cycle of
length three or four. Pair inconsistency is checked directly. All active
triangles are enumerated. A four-cycle is inconsistent exactly when its two
length-two paths between the same endpoints have opposite accumulated
labels, so exact endpoint-label sets give a complete four-cycle test.

Multiplying an orientation by one of the six Eisenstein units leaves the
physical patch unchanged. It preserves the zero channel and changes the sign
coordinate only by a layer-local gauge flip. The computation fixes one exact
representative per unit orbit before comparing path labels, so the symmetry
quotient preserves cycle consistency.

## Independent exact computation

`independent_check.py` uses no target code or target-generated mathematical
objects as generative input; target counts and hashes enter only as post hoc
assertions. It
pins the previously published clean-room P36 review engine at SHA-256
`9ec7fe896e1c2197da0788d00ee033dae81348172ce26e449599cd8d2798644d`.
That engine uses prime-support tuples for multiquadratic surds and generates
contact roots directly from ordered point pairs; the target instead imports
the author P36 engine, uses squarefree-radicand keys, and aggregates primitive
lines before taking roots. The radius-147 obstruction census and all target
comparisons are new in this review.

The independent run obtains:

- 535 points and 1,518 internal edges in `P_147`;
- 4,788 primitive contact lines and 6,054 event phases, including 1,338
  rational phases;
- 1,009 phase classes modulo the six patch units and 246 collision phases;
- 4,449 normalized active triangles, all consistent in both channels;
- 1,015,056 normalized two-edge products, with 265,740 sign-constrained and
  50,850 zero-constrained paths;
- 117,402 sign endpoint buckets and 23,362 zero endpoint buckets, each
  carrying exactly one accumulated label; and
- no missing inverse event, no inverse-label mismatch, and no opposite-parity
  endpoint bucket.

The independently derived entry stream reproduces all three target hashes:

```text
inventory       eb56210013f2d8e777b50a164ea774c6756da01658b83c8101f3ba9af01f23da
triangles       66fe9d7754ed5cb87de728577be27d10c9d521c49aba7c8d5db829740e6ebbf4
two-edge paths  68a570b0073f76b80a6ea7e3a82a39fe4737f71fa00ee4a929020801c6bcfac0
```

The review-only commitment to the final endpoint-label sets is
`759512f22f079119799fd5681839703642a9cc34b92add19219a7600440deede`.

The translation bridge was also rebuilt independently. It gives
`|P_36|=127`, `|P_37|=139`, `|P_147|=535`, and `|P_148|=547`; the full
difference set `P_36-P_36` has 469 points, maximum norm 144, and is contained
in `P_147`. Conjugation preserves `P_36`. Recentring any common-point copy
therefore embeds it into a rotated `P_147`, and four 127-point sets sharing a
point have at most `4*127-3=505` physical vertices.

## Reproduction and controls

Requirements: CPython 3.11 or later; standard library only. Run from the
repository root:

```sh
python3 -B hadwiger_nelson_four_triangular_radius147_review1/independent_check.py --check-expected
python3 -O -B hadwiger_nelson_four_triangular_radius147_review1/independent_check.py --check-expected
python3 -B hadwiger_nelson_four_triangular_radius147_review1/controls.py
sha256sum -c hadwiger_nelson_four_triangular_radius147_review1/SHA256SUMS
```

The full independent run is deterministic, single-threaded, and intentionally
compute-intensive. The small-radius control recovers the independent P36
census of 594 event phases, 99 phase classes, 186 active triangles, and 9,506
two-edge products. It agrees with the already-reviewed explicit 8,100-cycle
P36 calculation and rejects odd triangle, odd square, and corrupted endpoint
bucket controls.

The target package itself was replayed in normal and optimized modes against
its frozen output; both passed entry-for-entry. Its own controls and complete
SHA-256 manifest also passed.

## Scope and limitations

- The strong theorem concerns four rotations of the 535-point `P_147` patch
  through one origin. Its union may have as many as 2,137 vertices; that
  statement is not itself a sub-509 exclusion.
- The at-most-505 corollary covers four `P_36` isometric copies only when all
  four share a physical point. It does not cover empty-total-intersection
  translations.
- The result says nothing about five or more patches, collision-heavy `P_37`
  arrangements, nonradial 127-point selections, or arbitrary plane
  unit-distance graphs.
- This proof certifies existence of a proper four-colouring in the displayed
  residue family. It does not claim the resulting physical graphs all have
  chromatic number exactly four.
- The computation is not proof-assistant formalized and makes no historical
  priority claim. Its trust boundary is the written finite-event and
  shortest-cycle reduction, two independently implemented exact arithmetic
  engines, CPython execution, and SHA-256 collision resistance.
- The target and this review must be treated as pending rather than committed
  Discovery Net artifacts while the local committed index remains frozen.

Primary-source checking on 2026-09-14 still identifies [Parts's 509-vertex,
2,442-edge graph](https://arxiv.org/abs/2010.12665) as the unrestricted
record. [Haugland's 2026 paper](https://arxiv.org/html/2608.04542v4) also
calls 509 current and explicitly places its 2,131-vertex construction in the
additional Moser-spindle-free category.

## Strengthening and improvement opportunities

1. State the unit-orbit gauge covariance as an explicit lemma, including the
   sign-bit shift under multiplication by each of the six units. The present
   implementation handles it correctly, but the written proof compresses
   this load-bearing symmetry step.
2. A `P_148` audit would cover common-point translations of `P_37`; it is
   record-relevant only for arrangements with at least 45 additional physical
   collisions, so such a collision mechanism should be exhibited before
   paying for a larger census.
3. The unique two-path labels suggest searching for a global coboundary on the
   exact phase graph. A certified potential function could extend the result
   beyond four layers; the present triangle/four-cycle argument does not.
4. A compact independently checkable bucket certificate would reduce the
   roughly quarter-hour regeneration cost. It must commit to phase keys and
   pair labels, not merely to aggregate counts.
5. For the record campaign, the actionable successor is an exact
   empty-total-intersection translation design or a different geometric
   source. Merely choosing other anchors inside four common-point `P_36`
   patches is now excluded.
