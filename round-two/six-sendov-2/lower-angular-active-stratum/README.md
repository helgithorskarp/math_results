# Lower degree-nine angular collision frontier

Actual agent **six-sendov-2**, role **researcher**, 2026-10-01.
Ordinary author proof; independent review pending; not formalized.

The [proof](PROOF.md) establishes a nonzero, existential interval below
the first spectral-square collision radius
\(a_L=(10\sqrt{305}-105)/164\). Every global collapsed-angular optimizer
there has two double outer slopes and four simple inner slopes. Its
polynomial is
\[
(z^2-r(R))^2[z^4-(1/2-2r(R))z^2+t(R)],
\quad R=\frac{16(48(1+a)^2-40(1+a)-53)}{(4(1+a)+1)^2}.
\]
The analytic branch is uniquely specified by the explicit rational
stationary equations and
\[
r(R)=11/56+(25/6048)\delta+O(\delta^2),\quad
t(R)=11/9408-(25/124416)\delta+O(\delta^2),
\quad\delta=R+112/25.
\]
Its loss from the formal spectral-square bound is
\(3025\delta^2/3048192+O(\delta^3)\). Uniform root-distance stability is
quadratic with coefficient proportional to \(-\delta\), together with a
fourth-power bound that remains valid and is sharp at the collision.

A further exactly attained radius is
\(a_3=(3\sqrt{29}-11)/16\), with profile
\((z^2-9/56)^3(z^2-1/56)\). The formal equality polynomial has four
nonreal roots throughout \((a_3,a_L)\); its upper value is strictly
unattained there. Only a nonzero portion adjacent to \(a_L\) has its
actual optimizer evaluated by this contribution. No effective interval
length, finite-energy optimizer, or unrestricted first-power theorem is
claimed. [Literature and dependencies](LITERATURE.md) retain prior credit.

From the repository root, run:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B round-two/six-sendov-2/lower-angular-active-stratum/verify.py
```

Expected summary:

```json
{"checks": 51, "damage_controls": 4, "record_sha256": "a34826814d83ebec68e1a91cb2edce48042d3f9a3fc5565ca0eae500b7fae716", "status": "all exact checks passed"}
```

The checker is standalone Python standard-library code, validated on
CPython 3.11.2. It verifies the full two-parameter compression polynomial,
moment identities, two independent exact Hessian calculations, response
coefficients, splitting signs, collision derivatives and equality-point
factorizations. One Hessian calculation differentiates rational Taylor
jets; the other computes the compression-root residue trace in an exact
polynomial quotient ring. No floating roots enter either calculation.
The analytic factorization, implicit-function, concavity, compactness
and stability proof is in the written source, outside the checker.

Normal and optimized (`-O`) execution give the same output. Four internal
damage controls and an independently damaged expected fixture are rejected.
`--write-expected` is a maintainer fixture-generation flag; reproduction
does not use it. The committed fixture contains only compact exact data.
The discovery derivation additionally used SymPy 1.14.0 in workspace
scratch; it is neither a reproduction dependency nor a proof oracle.
