# Gaussian majorisation for hemispherical and four-cap reflections

For disjoint reflected caps of a compact convex body in R3, this package
proves full Gaussian majorisation in two cases: **arbitrarily many caps
whose normals lie in one closed hemisphere**, and **any four caps** without
that restriction. The conclusions hold for every probability law on the
body, every Gaussian variance, and every hinge threshold. They also give
both ball-union and ball-intersection Kneser--Poulsen inequalities with
arbitrary individual radii and any finite number of centers.

The [proof](PROOF.md) discharges the finite auxiliary-vector condition from
the team's [three-cap theorem](../gaussian_disjoint_cap_reflections/PROOF.md).
Normalized projection handles hemispherical normals. Four general normals
reduce to an exhaustive four-branch affine certificate. An explicit map
with four active reflection planes extends the earlier seven-site example
beyond finite chains of strong contractions.

An exact twelve-normal winding certificate shows that the sufficient
normal-only condition is not universally feasible. This is **not** a
Gaussian counterexample or a general motion obstruction: shallow caps
with those very normals have a separately proved R4 contracting motion.

**Status:** complete author proof; independent correctness and historical
priority review pending. The unrestricted dimension-three question remains
open. The broad cap class, the particular finite controls, and the obstruction
to a sufficient certificate have different scopes.

## Replay

Only the Python standard library is needed. CPython 3.11.2 and 3.12.14
were checked. From this directory:

```sh
python3 verify.py
python3 independent_check.py
python3 -O verify.py
python3 -O independent_check.py
python3 check_controls.py
sha256sum -c SHA256SUMS
```

The primary audit must report `EXACT_CAP_CERTIFICATES_PASS`, with record hash
`0ec7f205c15d3127d69f68aebdc80ebdf375f57fb2b5c4617d11b620cd59c6dc`.
It checks 24 rational Farkas identities covering all four max branches,
six cap-separation inequalities on an eight-vertex convex hull, all 28
pair-distance polynomials for the entire motion, paired affine rank six,
polar and tetrahedral controls, and the exact antipodal triangle-chain
certificate on twelve normals. There are 15 tight and 13 strict pairs in
the eight-site control. No time sampling is used.

The separate checker must report `SEPARATE_WINDING_ROWSPACE_PASS`. It covers
the **obstruction**, using 20 triangle equations and 15 antipodal-edge
equations on 30 angular edge variables. Their rank is 25. It derives an
explicit 13-term rational dual forcing the half-cycle sum to zero; the
dual hash is
`344d88fd698834395e7997ca37121fc39bf0b77619bb9fc65c878916fde12638`.
It imports no primary code and never reads the disk-chain certificate.
It does not independently audit the positive-class analytic proof.

The damaged controls must report six rejections. The primary checker rejects
a negative Farkas multiplier and a false hemisphere witness; both checkers
reject a missing icosahedral triangle and a broken antipodal cycle. All
checks remain active under Python `-O`. Each complete audit takes under one
second on the author's host; no substantial search or external data are
required.

## Files and trust boundary

| File | Obligation |
| --- | --- |
| [PROOF.md](PROOF.md) | Universal projection and four-normal lemmas; full-time motion; winding proof; Gaussian and ball transfers |
| [CERTIFICATE.json](CERTIFICATE.json) | Rational duals, exact cap data, and golden-ratio triangle chain |
| [verify.py](verify.py) | Primary exact finite audit in Q, Q(sqrt(2)), and Z[phi] |
| [independent_check.py](independent_check.py) | Separate rational row-space proof of the finite winding obstruction |
| [check_controls.py](check_controls.py) | Malformed mathematical certificate rejection |
| [EXPECTED.json](EXPECTED.json) | Deterministic primary audit output |
| [SOURCES.md](SOURCES.md) | Attributed premises, scope comparisons, and source revisions |
| [SHA256SUMS](SHA256SUMS) | File integrity manifest |

The signed affine combinations are checked directly, not accepted from an
LP status. Discovery used floating linear programming to find these small
rational combinations; neither that solver nor its output tolerance is a
proof premise. The public certificate supplies every multiplier, and the
checker rebuilds all hypotheses, branches and target forms before exact
substitution. Coordinates, graph edges, triangle coverage, orientations and
antipodal identifications are likewise checked entry by entry.

The analytic sign arguments, interpretation of angular winding, and the
cited transfer theorems remain written mathematics, not a proof-assistant
formalization. Python exact arithmetic and the checking programs are trusted.
Two author algorithms and source publication do not constitute independent
mathematical acceptance. No Gaussian quadrature, omitted corpus, moment
enclosure, or private input is used by the proof.
