# Curvature resources for finite Heesch obstructions

Actual agent **six-heesch-3**, role **researcher**. Round two, 2026-10-01.

[The written proof](proof.md) gives a finite-depth obstruction for arbitrary
piecewise regular C2 Jordan tiles: every bounded odd function of signed
curvature supplies a reflection-invariant boundary resource. If its
positive arclength mass exceeds its negative mass, complete corona copy
counts grow exponentially and eventually exceed planar area capacity.
Partial contacts and subdivisions of a prototype arc are permitted.

A second lemma proves a sharp upper bound of three for every imbalanced
equal-radius circular-bow regular hexagon with endpoint angle beta in
(0,pi/6). An angle-star and half-arc curvature
argument locks complete coronas to hexagonal cell balls, including the
last layer, without starting from a whole-arc matching assumption. Excess
two has upper one, and excess at least three has upper zero. Curvature
matching excludes the five exceptions left by angle arithmetic alone.
Balanced words remain outside this classification.

The explicit word (0,+,+,+,-,-), at radius13/10 and sagitta1/10, has
**Hc=Hh=3**, with 37 checked copies. The word (+,+,+,+,-,-) has
**Hc=Hh=1**. The words are descriptions of actual unmarked circular curves;
no external edge labels or matching rules restrict physical placements.
Arbitrary translations, rotations and reflections are covered by the
upper proof. The lower certificates work throughout the stated parameter
family.

This is a structural obstruction and calibration, not a new Heesch record.
Smooth-curvature cancellation and bump/nick imbalance are established prior
art, as is Epstein's marked-hex upper3 count reported by Mann. They are
credited in the proof. The new scope is the continuous resource and
explicit all-motion circular-arc bridge. The finite-seven construction is
still missing.

From the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B round-two/six-heesch-3/curvature_capacity/check.py --expected
```

CPython3.11.2 standard library only; compatible Python3.10+ suffices.
The small reader checks integer cell/vertex incidences, all side matchings,
disk prefixes, strict-nesting vertex stars, complete angle-only enumeration
and elimination of its five possible exceptions,
the guarded shell interfaces at depths1,2,4, the charge contradictions,
and malformed controls. No proof search is needed to reproduce it.

Expected principal output: cumulative copies1,7,19,37; ninety matched
internal sides in the three-corona fixture; ball4 has61 copies,54 boundary
sides and24 guarded shell interfaces. The general curvature-capacity
certificate separately excludes depth18:2397 required copies exceed2196.
[expected.json](expected.json) records exact output and witness hashes.

Trust boundary: continuous local-interface, angle-locking and deformation
arguments are written proofs, not formal verification or independent review.
The integer checker establishes the finite claims in that reduction.
No numerical solver, floating-point geometry, external input or large
certificate is required. Runtime is less than one second on the campaign's
single-CPU process scope.
