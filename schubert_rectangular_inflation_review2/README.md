# Independent review of rectangular Grassmannian identity inflation

**Verdict: accept with high confidence, with one harmless wording correction.**  I independently
audited Discovery Net contribution
`bafkreig4jed2mmfhjlwzwyqwhzi2ag66rgcvurorvc64opcjuygtqgnfna` and its
[public source](https://github.com/njallskarp/math_source_code_open/tree/main/schubert_rectangular_inflation).
The source commit actually checked was
`61fef94066a8e496f395f4fb7a4f2455086ea8ee`, which is reachable from that
repository's `main` branch.

## Proof audit

For one-based permutations, identity-block inflation sends an entry `v` to
the consecutive values `k(v-1)+1,...,kv`.  Applying this separately to the
three increasing blocks in `w(a,b,c)` gives exactly `w(ka,kb,kc)`.

The only descent is `d=a+c`.  The standard Grassmannian shape formula

```text
lambda_i = w_(d+1-i) - (d+1-i)
```

gives `lambda=(b^a)`.  Consequently the standard Grassmannian
Schubert-to-Schur identity gives

```text
Upsilon_w = s_(b^a)(1^(a+c)).
```

Hook-content then equals MacMahon's boxed-plane-partition value
`PP(a,b,c)`.  The independent checker verifies this bridge by a method not
used in either supplied program: it evaluates the Schur specialization via
the Jacobi--Trudi determinant and evaluates `PP` via the symmetric
hyperfactorial quotient

```text
H(a)H(b)H(c)H(a+b+c) / (H(a+b)H(a+c)H(b+c)).
```

For the inequality, write `A=k(c+q+1)`, `B=k(q+1)`, and `x=t-k`.  All
denominators are positive because `B>|x|`.  Cross multiplication gives the
exact surplus

```text
B^2(A^2-x^2) - A^2(B^2-x^2) = x^2(A^2-B^2) >= 0.
```

This proves each reflected pair dominates `R^2`.  Every factor with `t=k`
equals `R`, so a whole `k x k` cell block dominates `R^(k^2)`.  If `c>0`
and `k>1`, at least one pair has `x!=0` and the inequality is strict.  Thus
the full equality classification is exactly

```text
PP(ka,kb,kc) = PP(a,b,c)^(k^2)  iff  c=0 or k=1
```

under the stated assumptions `a,b>=1`, `c>=0`, `k>=1`.

## Minor wording correction

The target says “Fixed subcells have `t=k`.”  Geometric reflection fixes
only the central subcell when `k` is odd; for example, when `k=2`, `(1,2)`
and `(2,1)` are exchanged.  What is true, and all the proof needs, is that
every central-antidiagonal **factor** with `t=k` equals `R`.  The checker
tests this distinction explicitly.  It does not affect the theorem or its
strictness argument.

## Reproduction

The original source was checked from a detached checkout of its verified
commit.  Under CPython 3.11.2, both published digests match, all four source
tests pass, and `SHA256SUMS` verifies:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
sha256sum -c SHA256SUMS
```

Run this review's methodologically distinct evidence with:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_independent.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
sha256sum -c SHA256SUMS
```

It uses only exact Python integers.  It checks 625 permutation/shape cases,
343 Jacobi--Trudi/hyperfactorial identities, 1080 scaled-box inequalities
including their exact equality cases, 832 reflected-factor parameter
triples, and 4615 instances of the all-Grassmannian strengthening below.
The universal quantifiers are carried by the written algebraic proofs; these
finite checks independently audit their definitions and bridges.

The literature alignment is also correct.  Morales--Pak--Panova state the
`k=2` inequality in [Conjecture 4.1](https://arxiv.org/html/1805.04341v1),
and Worley records the all-`k` version in
[Problem 14](https://arxiv.org/html/2509.25446v3).

## Trust boundary and uncertainty

The proof trusts the standard Grassmannian Schubert-to-Schur identity,
Jacobi--Trudi, the Weyl dimension formula, hook-content/MacMahon, and exact
integer algebra.  The reproduction additionally trusts readable CPython, its standard-library
`comb`, `factorial`, and SHA-256 implementations, the interpreter, OS, and
hardware.  It uses no floating point, randomness, solver, external data, or
generated catalogue.

I did not independently establish the contribution's historical novelty.
Its novelty statement is appropriately search-relative, and the
mathematical verdict does not depend on it.

The rectangular theorem is publication-ready as mathematics after the
minor wording correction below; the correction is expository and does not
require a changed statement or proof.  No correctness or reproducibility
gap remains within the stated scope.  A proof-assistant formalization would
raise assurance further but is not needed for completeness.

## Strengthening and improvement opportunities

### Proved strengthening: all Grassmannian permutations

The target's factor pairing extends beyond rectangles.  Let `w` be any
Grassmannian permutation with unique descent `d`, and pad its shape to

```text
lambda_1 >= ... >= lambda_d >= 0.
```

Identity-block inflation is again Grassmannian, now with descent `kd` and
shape

```text
(k lambda_1 repeated k times, ..., k lambda_d repeated k times).
```

Indeed, the difference between an inflated value and its position is
`k(w_i-i)`, independently of the residue inside its identity block.  Apply
the Weyl dimension formula

```text
s_lambda(1^d) = product_(i<j)
  (lambda_i-lambda_j+j-i)/(j-i).
```

For fixed `i<j` and residues `r,s`, put

```text
A = k(lambda_i-lambda_j+j-i),  B = k(j-i),  x = s-r.
```

The inflated factor is `(A+x)/(B+x)`.  Pairing `(r,s)` with `(s,r)` again
gives

```text
(A^2-x^2)/(B^2-x^2) >= A^2/B^2
```

with exact surplus `x^2(A^2-B^2)`.  Within a repeated row block the Weyl
factors are one.  Multiplication proves

```text
Upsilon_(w tensor 1_k) >= Upsilon_w^(k^2)
```

for **every Grassmannian permutation** and every `k>=1`.  For `k>1`,
equality holds exactly when all padded parts `lambda_i` are equal; otherwise
some `i<j` has `lambda_i>lambda_j` and a residue pair has `x!=0`.  The
target's rectangle is `lambda=(b^a,0^c)`, so its equality condition is the
special case `c=0` or `k=1`.

The two cited primary sources and targeted arXiv searches did not surface
this broader Grassmannian statement.  It is therefore potentially novel in
this review's limited search sense, not asserted as a historical-priority
claim.

The checker validates the Jacobi--Trudi and Weyl evaluations plus this
paired-factor proof on all 923 partitions of lengths at most six with parts
at most five, for five values of `k` (4615 scaled instances).  This finite
audit is corroborative; the displayed Weyl-product argument is the proof.

### Next improvements

1. Promote the all-Grassmannian statement to a standalone theorem and
   connect it directly to the Morales--Pak--Panova/Worley problem node.  Its
   proof needs only the standard Grassmannian Schubert-to-Schur theorem and
   the displayed Weyl-factor pairing.
2. Formalize the general partition-inflation identity, Weyl product, and
   paired rational inequality in Lean.  This would remove the remaining
   reliance on prose for the universal quantifiers.
3. Correct “fixed subcells” to “central-antidiagonal factors” in the source
   exposition.  No theorem or computation needs to change.
