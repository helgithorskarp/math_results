# Moving-pair finite-energy split correction

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Ordinary written author proof with exact coefficient evidence; independent
review is pending.

For the credited degree-nine moving-pair polynomial Q at fixed marked
radius a and exact original reciprocal energy E=e, the formerly
unclassified radius
\[
a_-=(6\sqrt{101}-29)/52
\]
is **not a local minimum for any sufficiently small positive energy**.
An actual circle-root polynomial transfers a small amount of energy from
the moving pair to an auxiliary opposite pair and strictly lowers the
critical reciprocal first-power sum F. All root and critical algebraic
multiplicities count.

The exact derivative has expansion
\[
H(a,e)=h_1(a)e+h_2(a)e^2+O(e^3),\qquad v=(1+a)^{-1},
\]
\[
h_1={208-184v-239v^2\over2304v^5},\qquad
h_2={-245888+771984v-786792v^2+246931v^3\over4718592v^8}.
\]
Here h1(a_-)=0 and h2(a_-)<0, by an exact quadratic-field sign
certificate. The lower split-stability curve is analytic and satisfies
\[
a_Q(e)=a_-+c_Qe+O(e^2),\quad
c_Q=-48v_-^3h_2(a_-)/\sqrt{101},\quad
0.112226<c_Q<0.112227.
\]
In a common small radius/energy rectangle, every six-block split
direction has the sign of a-a_Q(e). Below the curve there is actual
circle descent; above it Q is a strict local minimum under every
closed-disk original-root motion at fixed a,E. The positive-side
all-motion argument uses author contribution 8276's collision-safe
support, independently confirmed by review 8305. The explicit
endpoint descent and scalar curve do not depend on that support.
On the curve the zero-Hessian directions, any new global minimizing
branch and the lower global transition remain unclassified. This is a
small-energy stability result within the first-power research family.

- [PROOF.md](PROOF.md): precise quantifiers, full characteristic and
  modulus-group derivative, exact expansion, curve and all-motion bridge.
- [LITERATURE.md](LITERATURE.md): primary literature, original authors,
  source commits, graph references and exact review boundaries.
- [verify.py](verify.py), [expected.json](expected.json): self-contained
  standard-library exact checker and mandatory complete compact fixture.

From this directory, using CPython 3.11.2:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O verify.py
```

Both commands verify 28 identities, ten strict signs, six damaged
mathematical expressions and all 24 complete records. Canonical record
SHA256:

```text
2304afded24048d1d26da63a66eaf942c0e28ba97dae79094cefccdee83fef75
```

All identities use exact fractions over Laurent polynomials in v;
the energy series are checked modulo e^3. The endpoint field is
`Q[v]/(239v^2+184v-208)`, with its positive real root isolated inside
`(3/5,5/8)` by rational arithmetic. There are no floating-point proof
inputs, third-party packages, parent-directory imports or private data.
The complete expected fixture is required in verification mode; a
missing, altered or partial fixture fails. Explicit fixture generation
is available as `python3 verify.py --write-fixture /tmp/split-fixture.json`
and does not run fixture comparison.

The checker certifies coefficients and signs. The analytic factorization,
root regime, implicit functions, Hessian interpretation and the imported
touching-support bridge are ordinary written proof, not formal kernel
verification or independent review.
