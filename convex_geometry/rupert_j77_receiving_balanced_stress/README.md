# J77: receiving-balanced mirror reduction on the whole 1/1000 cap

Author **six-rupert-2**, role **researcher**, 2026-09-30.

For the original asymmetric 55-vertex Johnson solid J77, this
[written proof](PROOF.md) constructs positive receiving-dependent
stresses on the ENTIRE physical chord cap 1/1000 around its five
projective C5 mirror axes. Every original proper source rotation,
planar roll, arbitrary translation and scale>=1 is included in the
necessary reduction.

Exact receiving normal and axial torque balance remove translation
and the axial linear stress, leaving the universal identity

    sum omega_i F_i=D[p^T A(u) ptilde-h(u)rho rhotilde].

All 42 receiving weights are>1/25, all 28 actual tangent-ray pairings
are>1/100, and 99/100<h<101/100 on the whole stated cap. A nine-variable
degree-five polynomial replay checks the identity exactly.

If BOTH tangent motions lie in the exact critical cone, the proof
forces unit scale, zero translation and one of the two equal-shadow
motions, up to an actual right C5 body gauge. Hence every other closed
containment in this cap has a NEGATIVE tangent coordinate in at least
one reflected motion.

The signed region remains open. **The whole 1/1000 cap is NOT excluded;
global J77 Rupert property is OPEN.** The preceding complete 1/100000 cap
classification remains the unconditional receiving exclusion. This
contribution is an author-checked, unformalized intermediate reduction,
independently unreviewed; no historical priority is asserted.

Python3.11+, standard library, single numerical thread, repository root:

```sh
python3 -B convex_geometry/rupert_j77_receiving_balanced_stress/verify.py --self-test
python3 -B -O convex_geometry/rupert_j77_receiving_balanced_stress/verify.py --self-test
```

Each run matches all 69,495 bytes of [expected.json](expected.json):
SHA256 `19a26bc5dadae7a9f80f15c7f9acdd9860bdd3b5986559d116571d609a734e42`.
Normal replay: 18.048116 seconds / 21,780 KiB peak RSS; optimized:
19.852408 seconds / 23,944 KiB. Each used one numerical thread under
an unchanged 55-second deadline. The independent sign audit includes
5,382 distinct field values, including all prerequisites.

The [compact fixture](certificates.json) freezes seven four-column
balance bases;[dependency pins](dependencies.json) bind all eight
files of the published bilinear parent. Its complete finite, all-roll
and physical-area evidence is replayed. All field signs have independent
rational positive-sqrt5enclosure audits, and five malformed controls
reject. The continuous Neumann and conditional cone arguments remain
the written proof's trust boundary. No private ledger, credentials,
solver transcript, search corpus or large artifact is included.
