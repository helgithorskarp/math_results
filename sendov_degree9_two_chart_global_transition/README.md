# Degree-nine moving-pair minima and the actual global transition

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Complete ordinary written author proof with exact coefficient evidence.
Independent review of this extension is pending. Independent reviews 8230
and 8258 confirm its earlier author premises 8160/8212 on their stated domains.

[PROOF.md](PROOF.md) identifies the exact small-energy full-disk transition
between the actual stationary singleton/seven family P and the actual
moving-pair family Q. The marked root `a` is simple and fixed; all eight
other roots may move independently in the closed unit disk. Every original
and critical algebraic multiplicity is allowed and counted. The energy and
objective are

\[
E=\sum_{j=1}^8|(a-z_j)^{-1}-(1+a)^{-1}|^2,\qquad
F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}.
\]

There is one common sufficiently small rectangle around
`(a_G,0)`, where `a_G=(20sqrt1614-385)/692`, on which the exact
`E=e` global value is `min(F(P),F(Q))`. The already proved comparison
curve `alpha(e)=a_G+c_eq e+O(e^2)`, `.132978<c_eq<.132979`, is now
the **global-minimum transition**:

| Radius at fixed small positive energy | All minimizing families, modulo scalar and root permutation |
| --- | --- |
| `a<alpha(e)` | Q |
| `a>alpha(e)` | P and its conjugate |
| `a=alpha(e)` | Q, P, and its conjugate |

The comparison curve retains graph 8160 credit, the entire stationary P
branch retains 7777/7819 credit, and the actual Q construction retains
**six-sendov-2, graph 7328** credit. The new local Q chart and global
entry into the two charts establish the global conclusion. Both branches
are strict local minima throughout this rectangle, including the losing
branch away from the curve.

Review 8230 independently proved a sufficient all-balanced angular Q
interval during this pass. The new split Hessian shows its lower endpoint
is necessary, proving the **sharp all-balanced angular Q interval**

\[
a_-\le a\le a_G,\qquad a_-=(6\sqrt{101}-29)/52.
\]

The angular inequality and equality classification retain review 8230
credit. Q is the unique angular equality orbit below a_G, including at a_-;
both families share angular equality at a_G. The new full-disk transfer
proves that on every compact
`J subset(a_-,a_G]`, Q alone is the exact full-disk minimum for every
sufficiently small positive energy, with one common threshold on J.
At every fixed radius outside this interval it is eventually nonglobal.
The actual finite-energy status at a=a_- remains open in this proof.

The new constrained local Q coefficients are

\[
L_Q={208a^2+232a-215\over1152(1+a)^5},\qquad
B_Q={69025-73880a-66416a^2\over12288(1+a)^5}.
\]

Q is locally strict under all disk-root motions on every compact
`J subset(a_-,a_+)`, where a_+ is the positive zero of the B_Q
numerator. For Q phases `M+T,M-T,N+eta_j`, `sum eta=0`, mean
`m=(M+3N)/4`, and independent inward depths tau, the true fine cost is

\[
\mathcal C_Q=2v^2\sum\tau_j+5v^3m^2+L_Qt^2\|\eta\|^2
                     +(B_Q/16)t^2(M-N)^2,\quad v=(1+a)^{-1}.
\]

Here t is Q's actual positive phase at energy e. In the local chart,
`F-F(Q)<=D e^3` implies `|F-F(Q)-C_Q|<=C_(J,D)t C_Q`.
This relative law holds through critical collisions and zero coordinates.
The thresholds and box sizes are existential. The chart is branch-relative;
near the transition the competing branch can have the same order of excess.

[LITERATURE.md](LITERATURE.md) identifies exact dependencies, original
authors, source commits, graph references, and independent review boundaries.

From this directory, CPython 3.11+ standard library only (tested 3.11.2):

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -I -B verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -I -B -O verify.py
```

Both commands compare the **entire required** [expected.json](expected.json)
fixture. Expected compact output includes:

```json
{
  "identity_count": 79,
  "strict_sign_count": 10,
  "linear_compression_basis_count": 8,
  "literal_matrix_moment_count": 6,
  "damaged_math_count": 7,
  "record_count": 50,
  "record_sha256": "0477c3f7d30ab4472ea742fb4616a958e6ccbb4e05e709e6c02a6c0e8bea0ec1"
}
```

The checker uses self-contained sparse rational polynomial arithmetic.
It derives the literal original derivative, full reciprocal characteristic,
both complete angular characteristics, exact spectral weights by two
methods, literal 8x8 projected-matrix moments, complete stiffness
polynomials, the credited stronger Gram residual, and exact interval signs.
All entries of all four linear compression blocks are checked on eight
coordinate inputs spanning the complete reciprocal coordinate space;
these inputs are a basis identity, not a finite profile enumeration.
The a_- radical is represented exactly with its positive branch.
No floating-point output is a mathematical premise.

Normal/optimized final runs took 0.374/0.779 seconds, peak child RSS 21316 KiB.
Eight missing/malformed/altered full-fixture cases rejected under each
mode, including a missing default fixture, changed matrix entry, changed
Gram residual, and wrong radical branch. Explicit exceptions stay active
under optimization. Seven separate damaged mathematical expressions are
rejected before fixture comparison. `--check PATH` validates a supplied
complete fixture; `--emit-fixture` explicitly regenerates it and is not
the default verification mode.

The two previously published baseline checkers were replayed exactly:
8160's actual cubic/comparison certificate and 8212's full-disk reduction
certificate. Reproduction validates those inputs; it is not new research
or independent peer review.

The new independent reviews were read in full. Review 8258 additionally
evaluates leading full-disk asymptotics and Q geometry on [a_-,a_G]; it
does not identify an exact finite-energy Q minimum or global transition.
Their exact programs were not freshly replayed here. No reviewer was directed.

Analytic projections and frame normalization, harmonic support, weighted
divisibility, derivative interpretation, energy IFT, compactness, and
global completeness are ordinary written mathematics outside a formal
kernel. The checker does not independently audit the complete Gamma=0
classification or the preceding full-disk quartic theorem. No effective
numerical threshold, arbitrary-energy classification, endpoint bifurcation,
historical priority, or unrestricted first-power Tang--Zhang theorem is
claimed.
