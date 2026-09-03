# Connected line graphs have signature at most 1 through order 11

For a graph `H`, write `s(H)=n_+(H)-n_-(H)` for the signature of its
adjacency matrix.  The exact exhaustive computation in this directory proves:

> **Theorem.** If `G` is a connected simple graph on at most 11 vertices, then
> `s(L(G)) <= 1`.

The same computation also proves the stronger cyclomatic inequality proposed
by Paone and Paone on this finite domain:

> **Finite verification.** If `G` is a connected simple graph on at most 11
> vertices and `c(G)=|E(G)|-|V(G)|+1`, then
> `2*s(L(G)) <= c(G)+1`.

Akbari, Elphick, Kumar, Pragada and Tang conjectured this for every connected
graph and checked all connected graphs through order 9.  Francis and Uptain
recently refuted the universal conjecture with a 14-vertex cactus, while
leaving the minimum-order question open.  Thus the new computation closes
orders 10 and 11 and raises the unconditional lower bound for a smallest
counterexample from 10 to 12.  For the sharper cyclomatic conjecture it
supplies the previously requested exact order-9 census and extends the exact
verification frontier from 8 to 11.  It does not decide orders 12 or 13.

## Finite reduction

The published tree case handles `m=n-1`, and the published dense-graph
argument handles `m>=2n-1`.  It is therefore enough, for each of `n=10,11`,
to enumerate connected simple graphs with

```
n <= m <= 2n-2.
```

`nauty-geng` produces one representative of every isomorphism class in this
range.  If `Q(G)=D(G)+A(G)` and `m>=n`, the unsigned-incidence identity gives

```
s(L(G)) = 2 * #{eigenvalues of Q(G) greater than 2}
          + #{eigenvalues of Q(G) equal to 2} - m.
```

The C++ checker obtains these counts as the exact inertia of `Q(G)-2I`.
Its main path uses fraction-free symmetric elimination with signed 128-bit
integers.  If a 2-by-2 pivot is required, it falls back to exact rational
congruence elimination.  No floating-point arithmetic or randomness occurs.

For the production range, every determinant entering fraction-free
elimination has absolute value at most `74^(11/2)` by Hadamard's inequality:
each row of `Q-2I` has squared Euclidean norm at most
`(d-2)^2+d <= 74`.  Products of two such minors are below `74^11 < 2^127`,
so the signed 128-bit intermediate products cannot overflow.

## Reproduce

The production environment used Debian 12's nauty 2.8.6 and GCC 12.2.0.
On Debian 12, install `nauty` and compile with:

```bash
g++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra -Wconversion -Wshadow -pedantic \
  check_inertia.cpp -o check_inertia
```

Run the two complete enumerations:

```bash
for n in 3 4 5 6 7 8 9; do
  nauty-geng -cq "$n" "$n:$((2*n-2))"
done | ./check_inertia --crosscheck > reproduced_n3_n9.txt
nauty-geng -cq 10 10:18 | ./check_inertia > reproduced_n10.txt
nauty-geng -cq 11 11:20 | ./check_inertia > reproduced_n11.txt
cmp reproduced_n3_n9.txt expected_n3_n9.txt
cmp reproduced_n10.txt expected_n10.txt
cmp reproduced_n11.txt expected_n11.txt
```

The checked-in summaries also include one combined cross-checked run for
orders 3 through 9.  Trees satisfy the sharp bound because their line-graph
signature is nonpositive.  The unenumerated dense range is automatic:
`s(L(G)) <= 2n-m`, so `2s(L(G)) <= c(G)+1` whenever
`3m >= 5n-2`; in particular this includes `m>=2n-1`.

The cross-checked order-3--9 run processed 83,339 graphs in 1.369 seconds,
the order-10 run processed 1,335,628 graphs in 7.849 seconds, and the order-11
run processed 28,908,704 graphs in 207.124 seconds.  Their compact-output
SHA-256 values are, respectively,

```
dcee24d8a53c3c5df474dc046dd21545c754acab5e0c8d155f91220104fc7139
5567d30204ddee6550712ffe6693afb9ed73dc9da5212fc556ae8ce6af224aab
32b42a4bb2b16f94a7140c48143a947dd1cc9ebc63ec1814ddbcc05dd1b11eaf
```

Run the compact, definition-level verifier with CPython 3.11 or later:

```bash
python3 verify_certificate.py
```

It validates all three summaries and reconstructs the line graphs of the first
order-10 and order-11 maximizers directly, computing their adjacency inertia
over exact rational numbers.  It also reproduces the exact signature 2 of
the published 14-vertex counterexample.

For development validation, `--crosscheck` compares the optimized
fraction-free path with exact rational congruence whenever the former accepts
a 1-by-1 pivot sequence; cases needing a 2-by-2 pivot use the rational path
directly.  This was run on all 83,339 relevant connected graphs of orders 3
through 9.  On the same full corpus, `--signatures-only` output was compared
entry by entry with `python3 verify_certificate.py --stream`, which constructs
the line graph directly and applies Python `Fraction` congruence elimination.
AddressSanitizer and UndefinedBehaviorSanitizer builds were also run on the
complete 6,539-graph corpus through order 8.

## Trust boundary and scope

Completeness trusts nauty 2.8.6's canonical connected-graph generator and
the stated sparse/dense reduction.  Arithmetic correctness trusts the C++
compiler and execution platform, mitigated by exact division checks, the
independent rational fallback, exhaustive small cross-checking, sanitizers,
aggregate counts by edge number, and a Python direct-line-graph verifier.
The compact summary files are certificates of the recorded run, not
standalone proofs of exhaustive coverage; reproducing the theorem requires
rerunning `nauty-geng` and the checker.

Primary context:

- [New conjectures on the inertia of graphs](https://arxiv.org/abs/2508.01163)
- [The signature of connected line graphs is unbounded](https://arxiv.org/abs/2607.22874)
- [Line-Graph Signature Beyond the 2-Core](https://aletheia-technologies.it/research/line-graph-signature-beyond-the-2-core/reader/)
- [nauty and Traces](https://pallini.di.uniroma1.it/)
