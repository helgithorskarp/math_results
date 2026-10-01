# Validation and evidence boundary

**six-rupert-2, researcher; 2026-10-01.** The ordinary continuum proof
in [PROOF.md](PROOF.md) is unformalized and independently unreviewed.
Exact finite checking does not replace that bridge.

The production checker uses Python3.11.2 and its standard library.
Normal and optimized runs matched their complete entrywise records:
2.870113 seconds /17080KiB peak child RSS, and2.906939 seconds /18848KiB.
They ran sequentially, one process, with numerical-library thread
environment settings1, under the existing1CPU/2GiB scope. No limits or
resource settings were increased. Small files only; private exploratory
outputs and installed numerical packages are not published.

The certificate was discovered using a small floating LP and then
reconstructed over Q(sqrt5). An initial arbitrary pivot selection failed
the positive-weight check. QR-guided variable selection avoided that
conditioning problem; all reconstructed coefficient equations, endpoint
weight signs and polynomial rank bounds were checked exactly. The public
checker reads literal weights and never calls that solver or reconstruction.
Neither floating optimality nor a fitted scalar is a theorem premise.

The complete record checks2160 receiver support comparisons against all60
originals,576 strict corner comparisons,8640 reference-source support
comparisons,240 full-body symmetry vertex matches,72 literal reference
corners and15 force/torque coefficient identities. It expands the selected
five-by-five determinant and all25 cofactors over exact field arithmetic,
and bounds them on the entire real interval by Bernstein coefficients.
Six additional quadratic polynomial bounds locate the entire receiving
arc more than1/3 from every projective minimum.

Four damaged controls are run through the mathematical checks rather
than rejected solely by a checksum: two opposite weight changes preserve
normalization but break force/torque balance; replacing receiver corner23
by58 omits an actual original extremum; a repeated selected minor row
destroys rank; and radius1/500 fails the nonlinear contraction inequality.
Both Python modes reject all four. The immutable certificate checksum is
compared after these checks when matching the whole expected record.

The arithmetic/model pins are byte-matched against original geometry
commit25fc9695745b6832d068d18544452b7852b5847f. The model's independent
cupola construction is prior work credited in the proof; this checker
freshly checks the original circumradius, the full nonlocal shadows,
actual full-body symmetries, contact stresses and bounds. Shared ordered
field arithmetic is a trust dependency, not an independent implementation
or proof-assistant kernel. No formal verification or independent review
of this new result is claimed.

Two finite heuristic construction experiments preceded the certificate:
eight free-receiver starts/2590 LP evaluations (best scale0.9997703869),
then eight fixed nonlocal receivers/3749 evaluations and32 source
refinements (best off-reference scale0.9999989941). Each fit retained all60
original source points, a full numerical receiver hull and actual planar
translation. They completed within bounded one-thread jobs and prove
neither passage nor nonexistence. They are not checker inputs.
