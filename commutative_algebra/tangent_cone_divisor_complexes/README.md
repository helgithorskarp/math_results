# Tangent-cone Betti numbers from filtered divisor complexes

This note gives a simplicial-homology formula for every graded Betti number of
the tangent cone of a numerical semigroup, over any field. It includes an explicit
finite cutoff, an absolute-complex version on at most one more vertex than the
embedding dimension, and an extension to positive affine semigroups.

The target is [Problem 1 of Moscariello–Sammartano,
arXiv:2406.00790v2](https://arxiv.org/html/2406.00790v2). The argument is a direct
application and explicit reformulation of the classical relative-divisor-complex
method of [Bruns–Herzog (1997), Proposition 1.1](https://www.home.uni-osnabrueck.de/wbruns/brunsw/pdf-article/SimpSemi.published.pdf).
We give a complete chain-level proof and explain the exact reduction to that
prior work. Novelty and the match to the authors' intended question remain subject
to expert review; no priority or independent peer-review claim is made.

## Mathematical content

[THEOREM.md](THEOREM.md) contains the statement, proof, empty-complex conventions,
finite support bound, prior-work comparison, and a characteristic-independence
corollary for embedding dimension at most four.

For generators $n_1<\cdots<n_e$, let $\operatorname{ord}(a)$ be the maximum
factorization length and $n_F=\sum_{v\in F}n_v$. Set

$$
D_{s,j}=\{F\subseteq[e]:s-n_F\in S,
                    \operatorname{ord}(s-n_F)+|F|\ge j\}.
$$

Then the fine Betti number in degree $(s,j)$ is

$$
\beta_{i,(s,j)}=\dim_k\widetilde H_{i-1}(D_{s,j},D_{s,j+1};k).
$$

For numerical semigroups it suffices to use
$0\le s\le(n_1-1)n_e+\sum_{v=2}^e n_v$ and
$0\le j\le\lfloor s/n_1\rfloor$.
The finite experiments validate implementations; the universal claim rests on
the mathematical proof.

## Reproduction

The Python code uses only the standard library. Tested with CPython 3.11.2 and
3.12.14. Run from this directory:

```sh
python3 betti.py 6 7 15
python3 verify.py
python3 singular_check.py --singular /path/to/Singular
```

The third command requires Singular, tested with version 4.3.1 (4313), Debian
package `1:4.3.1-p3+ds-2`, and its bundled `sing.lib`. A normal installation of
Singular provides the needed library. No Python package installation is needed.
All computations use exact rational or prime-field arithmetic; there is no
floating-point rank estimation. Values of `--characteristic` must be zero or a
prime. The command `python3 betti.py 6 7 15 --characteristic 2` uses the prime field.

The first command returns total Betti numbers `[1, 4, 4, 1]`, with fine and
ordinary graded entries. This is a non-Cohen–Macaulay example.

Expected output of `verify.py`:

```json
{"characteristics": [0, 2, 3], "checks": "PASS", "report_sha256": "d8f23043241fd91671c5b70e006fcca3e78950d54afd24d2470f9c9630e52a5d", "semigroups": 119, "tables": 357, "topological_strands": 4008}
```

Expected output of `singular_check.py`:

```json
{"checks": "PASS", "fine_entrywise_matches": 357, "tables": 357, "tables_sha256": "c07c2d0fff9616455bed7dfe13da4c898b00b14f367be835ea8e4efd13fb46e1"}
```

The two hashes cover different canonical records. The first includes support
bounds, total, graded, and fine tables. The second hashes generator lists,
characteristics, and fine tables reconstructed from Singular's free resolutions.
Every fine entry is compared directly before the second hash is produced.

## What is checked

- The deterministic corpus contains all minimally generated numerical semigroups
  whose generator set is a subset of `{2,...,11}` of size 2 through 4, together
  with `N`, selected examples of embedding dimensions 5 and 6, and the family
  `<a,a+1,2a+3>` for `4 <= a <= 15`. `verify.py:corpus` defines it completely.
- All 119 examples are evaluated over `Q`, `F_2`, and `F_3`. The verifier checks
  Hilbert-series identities and an additional interval above the proved cutoff.
- For seven specified examples over all three fields, 4,008 fine strands are
  checked for simplicial closure, square-zero differentials, the absolute-cone
  conversion, and the common-cone contraction above the cutoff.
- The two-generator case, `<6,7,10>`, a Bresinsky example, and the family in
  [Stamate's survey, Example 7.1 and Theorem 8.1](https://arxiv.org/abs/1801.00153)
  are compared with their stated formulas. The Example 7.1 table is described
  there as experimental, so that particular comparison is a consistency check.
- The independent Singular path eliminates `t` from `(x_i-t^n_i)`, computes
  `tangentcone` using a local standard basis, and calls `mres`. It recovers both
  degree coordinates from every monomial of the resulting differentials, checks
  homogeneity, and compares all 357 fine Betti tables entry by entry.

The complete validation runs took a few seconds on the research host. The
algorithm enumerates subsets of the generators and is exponential in embedding
dimension; its arithmetic cutoff is not asserted to improve on specialized CAS
methods. No exhaustive census beyond the stated regression corpus is claimed.

## Trust and scope

The code trusts Python's integer and rational arithmetic. The independent
comparison additionally trusts Singular's exact algebra algorithms. The proof
is written mathematics, not a proof-assistant formalization. No downloaded
primary-source PDFs, software binaries, raw traces, or private node data are
needed or included here.

Primary methodological dependencies are fully credited in THEOREM.md. The
small-embedding-dimension corollary also uses
[Björner–Tancer's combinatorial Alexander duality](https://arxiv.org/abs/0710.1172).
