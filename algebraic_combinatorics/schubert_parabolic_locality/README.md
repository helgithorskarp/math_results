# Parabolic locality for Schubert identity inflation

For a permutation \(w\), write

\[
\Upsilon_w=\mathfrak S_w(1,1,\ldots,1)
\]

and let \(\iota_k(w)=w\otimes 1_k\) be identity-block inflation.  Define

\[
R_k(w)=\frac{\Upsilon_{\iota_k(w)}}{\Upsilon_w^{k^2}}.
\]

Morales--Pak--Panova conjectured \(R_2(w)\geq1\); the natural all-\(k\)
version asks for \(R_k(w)\geq1\) for every \(k\geq2\).

## Result

Let \(I_1,\ldots,I_r\) be the connected components of the Coxeter support
of \(w\), and let \(w^{(j)}\) be the factor supported on \(I_j\), embedded
in the same symmetric group as \(w\).  Then, for every \(k\geq1\),

\[
\boxed{
\Upsilon_w=\prod_{j=1}^r\Upsilon_{w^{(j)}},\qquad
\Upsilon_{\iota_k(w)}=
  \prod_{j=1}^r\Upsilon_{\iota_k(w^{(j)})},\qquad
R_k(w)=\prod_{j=1}^rR_k(w^{(j)}).
} \tag{1}
\]

Thus identity inflation is **local on connected Coxeter support**.  In
particular, the conjecture is closed under parabolic products, and it is
enough to study support-connected permutations.

As a concrete all-\(k\) consequence, if every support component
\(w^{(j)}\) is Grassmannian, then

\[
\Upsilon_{\iota_k(w)}\geq\Upsilon_w^{k^2}
\qquad(k\geq1). \tag{2}
\]

This is an unbounded multi-descent class, not a finite specialization
stratum.  For example, the permutation \(13254=s_2s_4\) has two descents
and

\[
\Upsilon_{13254}=8,qquad
\Upsilon_{13254\otimes1_2}=6720>8^4=4096.
\]

More generally, \(s_2s_4\cdots s_{2m}\) has \(m\) Grassmannian support
components and specialization \(2^m m!\), so (2) supplies examples with
arbitrarily many descents and unbounded specialization.

The full proof is in [PROOF.md](PROOF.md).  It uses Macdonald's weighted
reduced-word identity to prove (1), then a paired-factor argument in the
Weyl dimension formula to prove the Grassmannian input in (2).

## Reproduction

The checker uses only the Python 3.11 standard library and exact integers
and fractions.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
sha256sum -c SHA256SUMS
```

The main check compares two different exact computations of \(\Upsilon\)
on all 46,233 permutations through \(S_8\): the Lascoux transition
recurrence and Macdonald's reduced-word recurrence.  It verifies base
factorization on the same set, \(k=2\) inflated factorization on all 873
permutations through \(S_6\), and \(k=3\) inflated factorization on all
153 permutations through \(S_5\).  It separately checks the
Grassmannian/Weyl bridge and the new componentwise class.

These finite checks audit definitions, indexing, factorization, and examples.
The universal quantifiers in (1)--(2) are carried by the written proof, not
by the census.

## Scope and trust boundary

The proof imports Macdonald's reduced-word formula, the standard
Grassmannian Schubert-to-Schur identification, and the Weyl dimension
formula.  The exact checker additionally trusts the readable source,
CPython, its integer and `Fraction` semantics, the interpreter, operating
system, and hardware.  It uses no solver, floating point, randomness,
external dataset, generated catalogue, or omitted certificate.

The theorem does **not** settle support-connected Boolean permutations or
the general identity-inflation conjecture.  It identifies those connected
cases as the irreducible frontier and gives a closure operation for every
class proved in the future.

Primary sources and the search-relative literature audit are in
[SOURCES.md](SOURCES.md).
