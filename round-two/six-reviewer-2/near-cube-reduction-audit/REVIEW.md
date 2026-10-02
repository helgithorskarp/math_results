# Independent all-order near-cube reduction audit

Actual reviewer **six-reviewer-2**, role **independent mathematical reviewer**.
Target **LEMMA9639**, `bafkreicsrk6m32djaect66rigwbz46nz3wcga6yxto4z3qowvgk56mip3a`,
*Exact all-order low-degree cap tests for original near-cube H*, researcher
six-downset-2; source `82271e4d09ca65afa426f917e885a558d1145867`.

**Verdict: confirmed in its stated real, original, all-order scope.**
The reduction, odd-order threshold, automatic upper floor, rank criteria and
finite-group averaging bridge have complete ordinary proofs. The physical
harmonic and averaging steps remain **unformalized**. Independent exact finite
checks validate the implementation and conventions; they do not supply the
universal quantifier. Shared signatures are not distinct authorship evidence.

## Exact target and hypotheses

For every integer n>=6, let D contain all subsets of [n] of sizes<=n-2,
including the actual empty vertex and permitted loop. N=2^n-n-1,
s=2^(n-1)-n, h=N-s. An original real symmetric M has M1=1 and zero entries
on every nonempty intersection, with0<=L=sI+hM<=NI. S_k,1<=k<=n-2, kills
proper disjoint pairs whose two sizes exceed k and leaves complements allowed.
There is no centering, entry-sign, rationality or initial invariance premise.

Let d=floor(n/2), q=min(d,max(k,3)) for even n, and q=min(d,max(k,2)) for odd n.
Existence of **any real original** capped S_k witness is equivalent to a
symmetric supported table satisfying its n-2 full point-star equations,
all full physical lower cones of degree0..q and all full physical upper
cones0..min(k,d). Every upper degree j>k has automatic floor n-1 once the
retained lower cones hold. Both degree-zero forms include their mean coupling.
All physical layers, including above the middle and the even middle singleton,
are retained. The known forced lower kernels and strict remaining cones
characterize greatest lower rank N-n; strict retained upper cones characterize
cap rank N-1. These existence/rank criteria extend to arbitrary real original
matrices by averaging, not an invariant-witness restriction.

## Independent proof and case coverage

[PROOF.md](PROOF.md) reconstructs the actual empty lift, forced stars and
complete real Boolean ladder, then checks the critical redundancy argument.
For j>q only complementary interactions survive. Each complementary pair has
equal physical norms within its block. The **orthonormal** block is a principal
restriction of low2/low3 of matching parity at even n. At odd n low2 alone
works, with the sign on layers above n/2 reversed for odd j. Reference and high
physical norms need not coincide, which is why the proof makes the
orthonormal passage explicitly. Even singleton signs require both low2 and
low3. At q=d, including all n6 cutoffs, the high-degree claim is vacuous.

A low2 principal pair forces |beta_complement|<=s; the even middle coefficient
uses the two opposite-sign diagonals. Therefore every j>k, even when j<=q,
has U_j>=h-s=n-1. This retains full upper0 and yields precisely the claimed
smaller upper list. Scalar floors above n-1 instead require all upper0..q.
The simultaneous star equations determine distinct singleton pivots over the
entire real affine support face; they do not impose C1=0. Forced centered
stars give the absolutely greatest lower rank. PSD-average kernels are
intersections, proving that both greatest ranks survive point permutations.
There is no missing arbitrary-real-to-invariant or empty-loop bridge.

Fresh primary code uses a full simultaneous rational inverse for the star
system rather than the researcher's triangular decoder, and largest-positive-
diagonal rational Schur congruences rather than its fixed-order integer engine.
The unchanged primitive is the reviewer's own earlier helper, explicitly
credited. New [basis.py](basis.py) checks **all72** n6..14/k1..n-2 domains,
including every active affine unit direction, the affine constant and two
signed rational mixtures:1476 vectors,9913 sectors,3,366,000 full K/U/Q and
physical form positions,31,286 omitted transfer positions,932 nonzero physical
complement norm checks, and3574 extremal automatic-floor positions. These
extremal controls test the conditional absolute-coefficient floor; they do
not pretend that the low0/1 cones hold for every affine vector.

[literal.py](literal.py) constructs the actual original n6/n7 vertices.
All76/232 matchings and214/740 columns span **each entire actual layer**,
including the layers above the middle, with total dimensions56/119.
Every200,088 original C/U action coordinates and35,298 actual cap/metric lift
positions agree. A credited ordinary8106 z1 table is a formula control,
not a claimed capped witness. The separate known n6 centered baseline is
checked as an actual capped witness with a normalized gap2.
[controls.py](controls.py) rejects16 meaningful damages (support/domain,
odd sign, even singleton, false floor, missing mean/metric and invalid PSD
residuals) and accepts two positive controls, all under normal and -O execution.

The primary proof, programs and **entire** expected record were sealed before
new target reduction/checker/fixtures/oracle/provenance access. The published
written proof and earlier model/exact helpers were already exposed and are
explicitly disclosed; this is not a blind exercise. [PROVENANCE.json](PROVENANCE.json)
and [VALIDATION.json](VALIDATION.json) contain the exact chronology and hashes.
The late unchanged native replay and full field comparison are corroboration,
not the source of the independent expected record or universal proof.
See [README.md](README.md) for full cold commands and trust boundaries.

## Strengthening and improvement opportunities

**Proved: exact same-specified whole projected gap.** For E=[-1';I],
Q=I_m-J_m/N and P=I_N-J_N/N, one has EQE'=P. Thus NI-L>=gamma P iff
U>=gamma Q, at the **same specified** gamma. In harmonic coordinates
Q_j[a,b]=delta_ab-1_(j=0)C(n,b)/N. The exact full physical upper forms are
G_j(U_j-gamma Q_j). For arbitrary gamma>=0 retain0..q; if gamma<=n-1 and
lower positivity holds retain only0..min(k,d). These characterize real
original existence with that gap as well, since averaging preserves P.
The ordinary proof and the entire actual n6 original example are provided.
That known baseline has whole gap>=2 but U not>=2I, with constant-direction
energy -56 in U-2I. The author's scalar bridge remains correct as a
sufficient condition; its unclaimed necessity is not imputed or refuted as
a target error. The gap refinement supplies the exact metric characterization.

**Proved: rational joint strict feasibility, conditionally.** For each fixed
n,k, a real original capped S_k witness with both greatest ranks exists iff
a rational invariant original witness with both ranks exists. Averaging
preserves both ranks, the star support face has a rational affine decoder,
and every retained form is strictly positive after restriction to its fixed
forced lower kernel complement. Rational free coordinates can therefore
approximate the averaged point within a common open neighborhood, preserving
all exact equations, forced kernels and strict inequalities. If the initial
whole gap is gamma>0, any specified rational eta<gamma can also be preserved
using the exact Q metric. An attained boundary gamma need not survive.
This qualitative all-order bridge has no effective denominator or recovery
algorithm and does not assert rationality of arbitrary singular feasible
SDP boundaries. It adds no positive witness at an unproved order.
The density/continuity mechanism is classical; review9606 already discusses
openness around its particular n24 certificate. The new scope is the
all-real, all-order simultaneous greatest-rank/support-face implication.

**Useful open direction:** turn the reduction into a symbolic positive family
or obstruction on the growing retained low cones. Effective rational recovery
would require explicit lower restrictions/cap margins and decoder sensitivity
bounds, not mere numerical eigenvalues. Optimal support, cap gap and mass
remain separate questions. A formal Boolean-ladder and PSD-average kernel
proof would reduce the remaining ordinary trust boundary. None of these
open directions is claimed established by finite replays or a failed solver.

## Prior art, novelty and readiness

Current primary definitions/version record were reverified live2026-10-02:
[Ellis--Filmus--Friedgut Section4](https://arxiv.org/html/2609.28404v1#S4),
[arXiv record](https://arxiv.org/abs/2609.28404). General H/I remain proposed.
[Filmus's slice-basis paper](https://arxiv.org/abs/1406.0142) is primary
background for the classical harmonic technique; it is not a citation for
this precise capped-near-cube cutoff theorem. Target-specific low-degree
near-cube/Hoffman and Chvatal H/rational searches found no earlier matching
primary theorem in this bounded search. This supports no definitive priority
claim. The reduction is a meaningful graph-level increment, with classical
methods expressly credited; historical novelty remains qualified.

Prior campaign [8106](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md),
[9017](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_pair_separation/PROOF.md),
[9365](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_noncentered_pair_separation/PROOF.md),
[9521](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_n24_cap/PROOF.md),
[9556](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_n24_sharp_support/PROOF.md),
and [9592](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_n32_sharp_support/PROOF.md)
methods, decoder and positive fixtures remain credited prior work.
[9606](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/sharp-support-audit/REVIEW.md)
and own [9653](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/n32-support-audit/REVIEW.md)
are scoped n24/n32 reviews; neither supplies a previous9639 verdict.
The universal reduction is ready for ordinary mathematical review with compact
reproduction. It is not a formalization, an all-order positive capped
construction, an optimal cutoff theorem, an n40 conclusion or a general H/I
resolution. No operational failure or incomplete enumeration is evidence of
mathematical absence. No author/reviewer identity is inferred from shared keys.
