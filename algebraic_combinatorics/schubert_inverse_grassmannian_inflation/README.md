# Identity inflation for inverse-Grassmannian permutations

For a permutation \(w\), let

\[
 \Upsilon_w=\mathfrak S_w(1,1,\ldots)
\]

be the principal specialization of its Schubert polynomial, and let
\(w\otimes1_k\) be identity-block inflation.  Morales--Pak--Panova
conjectured the case \(k=2\) of

\[
 \Upsilon_{w\otimes1_k}\geq\Upsilon_w^{k^2}. \tag{1}
\]

## Result

Define

\[
 R_k(w)=\frac{\Upsilon_{w\otimes1_k}}{\Upsilon_w^{k^2}}.
\]

For every permutation \(w\) and every \(k\geq1\),

\[
 \boxed{R_k(w^{-1})=R_k(w).} \tag{2}
\]

Consequently, if \(w\) is **inverse Grassmannian**--that is, \(w^{-1}\)
has at most one descent--then (1) holds for every \(k\geq1\).

If \(w^{-1}\) has its only descent at \(d\) and padded Grassmannian
partition

\[
 \lambda=(\lambda_1\geq\cdots\geq\lambda_d\geq0),
\]

then for \(k>1\) equality holds exactly when all padded parts of
\(\lambda\) are equal.  The identity is included as the empty-partition
case.

The transfer is structural.  Reversing a reduced word is a
weight-preserving bijection for Macdonald's formula, proving
\(\Upsilon_w=\Upsilon_{w^{-1}}\), while transposing permutation matrices
proves

\[
 (w\otimes1_k)^{-1}=w^{-1}\otimes1_k.
\]

The Grassmannian inequality itself follows by pairing opposite residue
factors in Weyl's dimension product.  See [PROOF.md](PROOF.md).

This class has unbounded ordinary descent number.  In particular,

\[
 z_m=(m+1,1,m+2,2,\ldots,2m,m)
\]

has \(m\) descents, whereas \(z_m^{-1}\) is Grassmannian of staircase
shape \((m,m-1,\ldots,1)\).  These are support-connected examples, so
they are not obtained from the previously proved parabolic-product
closure.  The first nontrivial member is \(3142\), for which
\(\Upsilon_{3142}=2\) and
\(\Upsilon_{3142\otimes1_2}=20>2^4\).

## Reproduction

The evidence uses only the Python 3.11 standard library and exact integers
and fractions:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B verify.py | diff -u EXPECTED_OUTPUT.txt -
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v
sha256sum -c SHA256SUMS
```

The checker compares the Lascoux transition recurrence with Macdonald's
weighted reduced-word recurrence, audits inversion on every permutation
through \(S_8\), checks the Grassmannian shape inflation and direct
Schubert values on bounded inverse-Grassmannian cases, and separately
tests the exact Weyl pairing and equality criterion on a box of partitions.
Those computations check conventions and examples; the universal theorem
is the written argument.

## Scope and trust boundary

This proves the all-\(k\) conjecture for inverse-Grassmannian permutations
and records the general inversion closure (2).  It does not prove (1) for
all \(321\)-avoiding or all Boolean permutations, nor for arbitrary
support-connected permutations.

The proof imports Macdonald's weighted reduced-word identity, the standard
Grassmannian Schubert-to-Schur identification, and Weyl's dimension
formula.  The finite audit additionally trusts the readable source,
CPython, its exact integer and `Fraction` semantics, the interpreter,
operating system, and hardware.  It uses no solver, floating point,
randomness, external data, generated catalogue, or omitted certificate.

Primary sources and the bounded literature search are recorded in
[SOURCES.md](SOURCES.md).
