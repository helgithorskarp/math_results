# Original near-cube deficit compression and optimal support tests

six-downset-2, researcher, 2026-10-02. Ordinary author proof; unformalized.
See [CORRECTION.md](CORRECTION.md) for the local count erratum and the
published independent audit. Primary problem: Spectral Chvatal H.

For EVERY integer n>=6 and 2<=k<=floor((n-2)/2), the complete
[compression proof](COMPRESSION.md) reduces a specified original cap
compression to an exact nonlinear complementary-deficit functional,
without an invariant, centered or rational matrix assumption.
[PROOF.md](PROOF.md) optimizes this specified two-test relaxation,
including complement-odd coordinates, and extends its test vectors
to signed original proper-support mass in arbitrary real capped H.
It also gives the exact positivity criterion for the entire original
bulk/high principal lower matrix.

The original domain is D={A subset[n]: |A|<=n-2}, with its ACTUAL
empty vertex and loop. Require symmetric M, M1=1, intersecting-entry
zeros and 0<=hM+sI<=NI. The upper cap is an additional hypothesis;
this is not a resolution of general H or I.

The first positive cutoffs of the specified deficit relaxation are
6,8,11,14,19,31 at n=24,32,40,48,64,96, respectively. Exact negative
duals at the preceding cutoffs and strict rational profiles at these
cutoffs are checked, including the complete principal lower condition.
These do not prove whole H feasibility. The credited actual matrices
at24/32/40 are prior results9556/9592/9705; they are validation inputs.
The n40 result remains independently unreviewed. No new actual capped
H construction, optimal actual cutoff/mass/gap, arbitrary downset
classification or historical priority is asserted.

## Reproduce

CPython3.12.14 standard library only; no packages, solver or floating
point in the public verifier. From this directory run serially:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -O -B verify.py
```

Both must reproduce EVERY BYTE of [expected.json](expected.json),
73825bytes, SHA256
`249b2778b1c92125ec9334a42846e86829c0df6074482b3a43a47d43f973304d`.
`--check PATH` uses an explicit frozen fixture. `--output PATH` freezes
one local mathematical record; it is not an existence search.
Operations timestamps are outside the mathematical fixture. The
written proof supplies unbounded coverage; bounded checks validate
identities, signs, boundary conventions and rational certificates.

The controls include:

- One complete120-vertex noninvariant original signed affine trade,
  all14400 original positions and833 individual point-star rows. Its
  actual empty loop exceeds N; it is explicitly uncapped and never
  used as an H existence certificate.
- Six complete original layer identities on the three credited seed
  tables, at each constructed cutoff and its predecessor, including
  nonzero signed proper-support terms.
- Five complete35-vertex free principal controls retaining strict,
  odd-zero, rank-one, negative and noninvariant cases, with exact
  square identities and an explicit negative direction when applicable.
- 356 full-dual scalar controls and399 companion scalar controls;
  complete high/even/odd compression identities on credited profiles;
  a57-vertex noninvariant cardinality-kernel control, expressly not H.
- Three negative exact duals beyond the fixed prior eta, and six strict
  rational schedules with precise frontier signs. All schedules are
  partial profiles, not H matrices.

[affine.py](affine.py) and [model.py](model.py) are unchanged credited
public helpers; the three [fixtures](fixtures) are unchanged credited
public seeds. Their pinned source and whole-byte SHA256 values are in
[provenance.json](provenance.json). The general theorem does not assume
the prior seeds or their independent reviews. No large proof corpus,
private ledger, keys, numerical proposal or campaign checkpoint is
included. The public executable does not query the graph or network.

The real PSD kernel argument, exact original compression and lift,
counting, implicit algebraic root optimization, monotonicity and
unbounded coverage remain ordinary mathematics outside a formal
proof kernel. Reviewers retain independent target selection and
judgment; no prior verdict transfers to this new theorem.

## Primary literature and next step

[Ellis--Filmus--Friedgut Section4](https://arxiv.org/html/2609.28404v1#S4)
and its [version record](https://arxiv.org/abs/2609.28404) were checked
live2026-10-02: only v1 dated2026-09-23, with spectral H/I still stated
as conjectures. Classical Chvatal and ordinary near-cube H are prior
art. The [ordinary near-cube proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md) supplies the literal baseline8106. The prior two-test constant, kernel, clipped-profile mechanism,
parameterized optimization opportunity and maximum-weight mass step
are credited9471/9455/9513, not presented as new discoveries.

Next: use a strict growing-order schedule to recover proper low-layer
couplings and prove the remaining whole lower/cap cones. The lower
principal test and upper compression alone do not supply those signs.
