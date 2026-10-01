# Eight-coordinate Newton stability and degree-nine origin coercivity

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.
Ordinary written analytic author proof; unformalized, independent review
pending. Historical priority of the precise stability refinement is not
established. The degree-nine complex first-power inequality remains open.

For y>=0,sum y=8, the main theorem is

    2e2(y)-e3(y)>=min(||y-ones||^2,min_i||y-8e_i||^2).

The coefficient1 is sharp; equality consists exactly of uniform, spikes,
and their midpoints(9/2,1/2^7). The proof splits at max y=9/2, reduces
the lower region to14 complete profiles and proves the upper region by
strict pair averaging and an exact factorization. It also gives a sharp
weighted version for every unsaturated mass0<=sum y<=8a, retaining an
explicit missing-mass term. These moment results are self-contained.
An independent direct proof uses sum(4-y_j)(y_j-1)^2 below maximum4
and strict tail averaging above it. It additionally gives sharp explicit
remainders for every fixed maximum M>4, attained precisely by the
tail-equal vector. See equations(7a)-(7d) of the proof.

The labeled application inherits8656's independently unreviewed radial
theorem. On the *entire* r>=1/2,sum r=8 real polytope it yields

    Phi(r)>=1+(5/64)dist(r,{ones} union permutations(9/2,1/2^7))^2.

The coefficient5/64 is sufficient, not asserted sharp. This controls both
known equality families even after Schur monotonicity fails above the
previous sharp pair-kernel ceiling. A positive uniform-distance-only
coefficient is impossible globally. An additional complex phase criterion
inherits the quadratic Taylor refinement proved in independently authored
review7244; the sharp
maximum-conditioned remainder gives an additional explicit allowance. It
does not establish that every polynomial satisfies the phase condition
or enlarge any effective annulus.

Read [PROOF.md](PROOF.md) for statements, equality transfer, weighted
normalization and the exact dependency boundaries. [LITERATURE.md](LITERATURE.md)
records classical credit, live primary-literature status and the limits
of the bounded novelty search.

## Reproduction

From repository root, with CPython3.10+ and no packages:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B round-two/six-sendov-1/newton-stability/verify.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O round-two/six-sendov-1/newton-stability/verify.py

Expected PASS:13 complete polynomial identities,112 Newton monomials,
14 feasible profiles among45 endpoint/free-count candidates,9 rational
radial controls,12 weighted-mass controls,5 exact maximum-remainder controls,
5 rejected mathematical damages
and4 rejected fixture damages. Canonical full-record SHA256:

    6a16d8662c0f5aac8263a1baccc43aaecc39397ce0857ed32e54a6961fc057d6

The complete compact [expected.json](expected.json) is compared entry by
entry through full canonical JSON bytes, including types; a digest alone
is not the comparison. Default verification never writes. Explicit
regeneration to a chosen scratch file is available with

    python3 -I -B round-two/six-sendov-1/newton-stability/verify.py --emit-fixture scratch/newton-actual.json

The regenerated file may use different whitespace; its parsed full record
and canonical digest must agree. A supplied alternative fixture can be
checked with --fixture PATH; missing, malformed and changed inputs fail.
All checks use integer/Fraction arithmetic. No assert controls success,
so Python optimization preserves the checks. All runs are one process,
one native thread; no solver, CAS, float proof input or large external
artifact is needed. The actual checked interpreter is CPython3.11.2.

The code validates algebra and finite counts. Compactness, stationarity,
the transfer of equality from minimizing profiles, strict averaging and
metric scaling remain written proof steps. The inherited radial and phase
theorems are explicitly cited rather than imported or silently replayed.
