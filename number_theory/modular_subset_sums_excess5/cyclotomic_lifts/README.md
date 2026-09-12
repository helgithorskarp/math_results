# Cyclotomic lifts: a complete polynomial criterion and an unsuccessful closure route

For coprime integers `0<u<v`, the reciprocal five-term polynomial

```
P(u,v) = 1 + X^(v-u) + X^v + X^(v+u) + X^(2v)
```

has only roots of unity among its unit-circle zeros exactly when
`(u,v)=(1,2),(1,3),(3,4)`. These are also exactly its cyclotomic-product
cases. The [proof](proof.md) combines the classical five-root vanishing
classification, a uniform elementary sign-change bound for `v>=10`,
and 27 exact finite cases. No priority claim is made for the
cyclotomic-product classification; the [source trail](literature.md)
identifies the existing ingredients.

For the excess-five modular subset-sum problem, this says that existence
of an essentially atoral lift, after any unit dilation of the centered
holes, is **equivalent to the original three-type classification**.
It supplies no new elimination from the unresolved modular residual.
The fixed bivariate polynomial `1+X+X^-1+Y+Y^-1` fails the essential
atorality hypothesis of the checked Dimitrov--Habegger theorem.

Two exact controls expose stronger invalid shortcuts:

* An actual known five-element set modulo 37 has normalized hole lift
  `(1,12)`, which is not essentially atoral.
* At order 41, the core `{0,+/-1,+/-9}` has circulant determinant five
  but no unit dilation with a cyclotomic lift. **41 is outside
  `N=2^n+5`; this is not a counterexample to the selected conjecture.**

The final research-pass gate was missed. The unrestricted `O(N^3)`
count, complete classification for `5<=n<=14`, and scalar residual
`n>=15` from [the preceding package](../global_reduction) are unchanged.
This lane is parked for problem-level reassessment and literature-first
reselection. The polynomial criterion records the obstruction to the
attempt; it is not presented as a solution of the modular problem.

## Reproduction

From this directory, with Python 3.11 or later and no third-party packages:

```bash
python3 verify.py
sha256sum -c SHA256SUMS
```

Expected output:

```
PASS: 27 primitive pairs; 24 non-torsion exclusions; 3 factorizations;
      independent Sturm counts; N37 subset-sum control;
      N41 Bezout identity, determinant 5, and complete unit-orbit separation.
Scope: polynomial theorem and method controls; modular residual unchanged.
```

`python3 verify.py --emit` regenerates the exact contents of
`expected.json`. The normal command compares them with the saved file.
On CPython 3.11.2, the complete check takes well below one second.

The checker uses integer midpoint tests and exact monic divisions;
independently, rational Sturm sequences count distinct roots of the
associated cosine polynomials. It checks every coefficient of the
integer Bezout certificate in `norm_counterexample.json` and also
computes the full 41-by-41 circulant determinant by fraction-free
elimination. The order-37 check enumerates all 32 subset sums.

The trust boundary is the written infinite argument, the cited
vanishing-sum theorem, ordinary Python integer/rational arithmetic,
and the explicitly enumerated small box. The code does not verify the
external theorem or the infinite argument formally. No floating-point
root computation, SAT/MILP verdict, large hidden certificate, external
runtime input, independent peer review, or proof-assistant check is
claimed.
