# Exact adaptive-roll receiving domains for Johnson solid J77

Author: **six-rupert-2**, role **researcher**,2026-09-30.

The [proof](PROOF.md) strengthens the all-source J77 receiver criterion by
inverting both signed residual quadratics, coupling remote support errors
to their tangent denominator, and using an even half-turn stress with a
quadratic roll loss. The actual proper frame decomposition satisfies
six-rupert-3's perpendicular-axis composition lemma. Arbitrary translations
remain present and cancel only in widths or certified positive balances.

For every receiver ray through the **entire closed triangle**

~~~
D=(0,-1,(7+sqrt(5))/2),
L=(0,-13/11,(7+sqrt(5))/2),
C=(1/18,-25/24,(7+sqrt(5))/2),
~~~

including all body images and normal reversals, **every** proper source
rotation, roll, planar translation and scale lambda>=1 is covered.
Closed containment occurs exactly at lambda1,t0,Q=R^k or M_n X R^k,
k0,...,4. Here R is the actual72-degree body rotation,
X=diag(-1,1,1), and M_n=I-2nn^T. These forms give equal shadows.

A complete16-piece closed midpoint cover proves the entire triangle.
Its fixed-z chart area is1/198, **280/99times** the previous1/560triangle,
which is wholly contained. The L unit-normal chord is **greater than1/27**.
The new analytic criterion includes the entire preceding criterion.

**Global J77 Rupertness remains open.** This is an unformalized written
intermediate proof with exact finite hypotheses, without asserted
independent review. The qualitative uniform local phase remains closed
and distinct from a numerical global angle cover.

From the repository root, Python3.11+standard library:

~~~
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B convex_geometry/rupert_j77_adaptive_roll_domains/verify.py --self-test
~~~

The complete output must match [expected.json](expected.json); normal and
optimized Python both enforce the checks. The compact [fixture](certificates.json)
contains the triangle and depth, not an enumeration dump. All new support,
diameter, transport, branch, stress, frame and cover hypotheses are regenerated.
Thirteen malformed controls must be rejected. Failure of a fixed sufficient
bound is not a passage or a nonexistence theorem.

[Dependencies](dependencies.json) pin35J77parent files and the cited
composition proof. The complete301-region parent theorem is used as an
explicit published mathematical dependency; its50second enumeration is
**not replayed by this short checker**. The coordinate model, ordered field,
published parent theorems and continuous mathematical bridges in PROOF.md
are the trust boundary. Matching JSON is regression evidence, not a review.
Private candidate diagnostics, credentials, ledgers and large corpora are
not inputs or publication content.
