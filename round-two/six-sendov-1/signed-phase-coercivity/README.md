# Signed phase coercivity near the real unit tuple

Actual **six-sendov-1**, role **researcher**, 2026-10-03.
Complete ordinary author lemma, **unformalized and independently unreviewed**.

For O_a(z)=9 integral_0^1 product_j(1-a s z_j) ds, every finite complex8tuple
with R=|z|, Delta=sum(R-Re z)<=1/1000 and Y=Im sum z satisfies

    norm_2(R-1)<=1/16  => O_1(R)-Re O_1(z)<=-Delta/8+Y^2/56,
    norm_2(R-1)<=1/40  => O_1(R)-Re O_1(z)<=-7Delta/48+Y^2/56.

Both bounds are strict when Delta>0; all thresholds are closed. At Delta0,
zero phase is included directly. No conjugacy, separation or original-disk
feasibility hypothesis is required for these standalone bounds. The entire
analytic proof and correctly ordered actual corollaries are in [PROOF.md](PROOF.md).

For actual complex degree nine under ALL9 original closed-disk hypotheses,
ALL8 critical multiplicities, 0<eta<=1/12000 and ONLY F<=8+3eta, the broad
corollary follows AFTER9930 H37/polar entry. The fine corollary additionally
uses the fully proved9974 LC tuple (same conclusion already9954) and gives

    O_a(r)-Re O_a(q)<-7a Delta_q/48+(8/7)a^2 eta^2.

Original communication transfers this to O_a(r)-product r. A nonnegative
radial gap then forces Delta_q<(384/49)a eta^2, CONDITIONAL on that gap sign.
The gap sign is not established universally here. No new entry interval,
full first-power inequality, physical/motion theorem or optimality is asserted.
Coherent unit phases prove the mean term necessary; the balanced4+4 family
has limiting coercivity9/56, an algebraic-envelope barrier only.

## Reproduction and complete finite evidence

CPython3.11+ standard library only (observed3.12.14); no external package.
All children run serially with fixed45s timeouts and all native threads1.
From this directory:

    python3 -I -B verify.py
    python3 -I -B -O verify.py
    python3 -I -B validate.py

The validator sets OPENBLAS_NUM_THREADS, OMP_NUM_THREADS, MKL_NUM_THREADS,
NUMEXPR_NUM_THREADS, VECLIB_MAXIMUM_THREADS and BLIS_NUM_THREADS to1. It retains
current process CPU/memory limits; no resource settings are raised.

[arithmetic.py](arithmetic.py) constructs the ENTIRE deterministic typed record:
all45 general-a shifted coefficients by two routes; all36 mixed majorant
coefficients; every margin in both complete endpoint budgets and actual
receiving inequalities; the whole16-real-variable phase identity's3025
nonzero coefficients (1792/1120/112/1 at orders2/4/6/8); the full balanced
bivariate product and integrated polynomial; and six literal Gaussian controls,
with EVERY one of their nine complex product coefficients independently rebuilt
by iterative multiplication and complete subset enumeration. This evidence
contains no sampled universal inequality or actual disk-feasible tuple assertion.

[EXPECTED.json](EXPECTED.json) holds the complete compact common coefficient
record, not a summary checksum. [verify.py](verify.py) regenerates it before
requiring equality of every recursively typed field, list entry and coefficient.
Its six mathematical damage modes reject WITHOUT consulting the fixture:
wrong fourth-order sign, omitted eighth-order map, insufficient Hessian scale,
wrong Hessian center, removed imaginary-mean term and invalid fixedH radius.
Malformed external record and source-byte controls also reject.
[validate.py](validate.py) compares WHOLE records in normal, optimized and fresh
isolated source-only directories, six serial children total; [VALIDATION.json](VALIDATION.json)
records observed performance and complete damage outcomes.
[MANIFEST.json](MANIFEST.json) pins the nine defining proof/source/data files.
The manifest itself and validation receipt are not self-pinned. Joint replacement
of source, fixture and manifest is outside this byte-integrity guarantee.

## Trust, attribution and frontier

The backend and reused9974 typed/source validation scaffolding are SAME-AUTHOR
corroboration, not independent evidence. No executable/fixture from another
researcher or reviewer was imported. Universal subset/Maclaurin inequalities,
path norms/signs, full Taylor identity, ordinary integration and actual domain
implication/adoption remain ordinary mathematical arguments, not Lean theorems.
[dependencies.json](dependencies.json) and [LITERATURE.md](LITERATURE.md) give exact
parent sources and review scopes. Parent9954 now has independent9988 confirmation;
that verdict does not assess9974 or this leaf. Its173/190 refinement is unused.

The useful next question is whether actual original-disk feasibility supplies
a radial-gap lower bound strong enough to combine with this negative phase term,
or another estimate that turns the conditional O(eta^2) phase concentration into
an unconditional low-arm reduction. It cannot be answered by declaring the
radial gap nonnegative or by optimizing these finite budgets alone.
