# Uniform moving-budget degree-nine original-root motion

Actual **six-sendov-3**, role **researcher**, 2026-10-03.
Complete ordinary author proof, **unformalized and independently unreviewed**.

For the degree-nine reciprocal **first-power** objective, write

\[
F=\sum_{l=1}^8|1-\eta-\zeta_l|^{-1},\qquad
\Delta_\eta=(F-8-C\eta)/\eta^2.
\]

All nine original zeros lie in the closed disk, all eight critical points
count with multiplicity, and the marked original is (1-\eta).
Let (M_D(\eta)) be the largest canonical original-root displacement
from the credited first-motion reference, divided by (\eta^{3/2}),
under the **actual** cut (\Delta_\eta\le D).
The preceding [fixed-budget result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/budget-motion-frontier/PROOF.md)
computed its exact limiting curve (A(D)) for each fixed (D>B_*).

The new theorem supplies one uniform estimate: for every fixed finite
(D_{\max}>B_*), existential constants (\Lambda,L,\eta_0>0) satisfy

\[
|M_D(\eta)-A(D)|\le L\sqrt\eta
\quad\text{for every }0<\eta<\eta_0,
\quad B_*+\Lambda\eta\le D\le D_{\max}.
\]

The class is nonempty throughout this range; actual witnesses have all
nine original zeros strictly inside and simple. Critical collisions,
arbitrary complex tuples and nonsmooth moving profiles are included.
In particular, for **any** (\delta(\eta)\to0) with
(\delta(\eta)/\eta\to\infty),

\[
M_{B_*+\delta(\eta)}(\eta)
 =q\sqrt{H\delta(\eta)/\kappa}\,[1+o(1)].
\]

The relative error is (O(\delta+\sqrt{\eta/\delta})).
This is a joint limit with an exact moving physical budget.
The layer (\delta=O(\eta)), exact minimum-budget feasibility and the
global first-power conjecture remain open here.

Read [PROOF.md](PROOF.md) for the signed constraint-error estimate,
the endpoint-safe quadratic secants of the exact cost curve, uniform
upper bound and all-original actual lower construction.
[LITERATURE.md](LITERATURE.md) distinguishes new consequences from the
credited parity, moment frontier, motion law and actual chart.
[dependencies.json](dependencies.json) pins their whole source bytes.

## Reproduction

Python standard library only; observed Python **3.12.14**. From repository root:

    env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
      python3 -I -B round-two/six-sendov-3/uniform-budget-motion/verify.py \
      --validation-batch --baseline-root .

For an isolated directory, omit `--baseline-root .`; the source-only
record check remains self-contained. For serial normal/optimized and
cold-copy validation with bounded negative controls:

    python3 -I -B round-two/six-sendov-3/uniform-budget-motion/validate.py \
      --baseline-root .

Expected JSON status is `PASS`, entire canonical record SHA256:

    dc93cefad55b1b2ad4cc8ec84bfd1bad876e37a8fa6415034a576a68a98a898f

The exact [curve.py](curve.py) checks every coefficient of the eight-vector
projection identity before constraints are imposed, scalar first-power
Taylor coefficients, cost/secant identities, physical signs and all nine
cubic motion coefficient/norm maps. It uses the unchanged same-author
[arithmetic.py](arithmetic.py), credited in that file, not reviewer code.
The complete typed [EXPECTED.json](EXPECTED.json) and every sealed source
byte must match. Mathematical damages, late fixture alterations and
source-byte corruption reject in normal and optimized modes.
[VALIDATION.json](VALIDATION.json) records measured checks; fixtures and
baseline reproduction are same-author corroboration, not independent review.

Each math child is serial, native threads one, fixed45s guard, unchanged
1CPU2GiB scope. No large corpus, solver, numerical root sample, private
state or credential is a proof input. Exact algebra does not formalize
the ordinary analytic bridges described in the proof.
