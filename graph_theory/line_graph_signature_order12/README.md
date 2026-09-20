# Connected line graphs have signature at most 1 through order 12

For a graph `X`, write `s(X)=n_+(X)-n_-(X)` for the signature of its
adjacency matrix. This directory supplies the exact computation for the new
order in the following theorem.

> **Theorem.** If `G` is a connected simple graph on at most 12 vertices, then
> `s(L(G)) <= 1`.

Francis and Uptain give a connected 14-vertex graph with signature two.
Consequently, the minimum order of a connected graph whose line graph has
signature at least two is either 13 or 14.

The theorem depends on two previously accepted exact results: the complete
bound through order 11 and the check that none of the 72 order-11 maximizers
has a signature-two one-vertex extension. Their Discovery Net references are
`bafkreibrzfblwn3xld5jxyqlsg7kiwq5cpavl2dvciqhhxi345tj3ynw5u` and
`bafkreib3xmdbfswxmrmf7yaasamvxcpw7tjvlqcux6fnhmkenj3agkvtyq`.

## Reduction to minimum degree two

Only order 12 needs consideration. If `G` has a leaf `v`, then `H=G-v` is
connected and `L(H)` is obtained from `L(G)` by deleting the single vertex
corresponding to the pendant edge. Cauchy interlacing gives

```text
s(L(G)) <= s(L(H)) + 1.
```

The order-11 theorem gives `s(L(H))<=1`. If it is at most zero, interlacing
finishes the proof. If it equals one, the accepted one-vertex-extension
theorem gives `s(L(G))<=1`. Thus a counterexample of order 12 would have
minimum degree at least two.

Write `n=|V(G)|` and `m=|E(G)|`. Trees are already known to satisfy the
bound. If `m>=2n-1=23`, the unsigned incidence identities

```text
B B^T = Q(G),       B^T B = A(L(G)) + 2I
```

give `s(L(G))<=2n-m<=1`. It therefore remains to enumerate connected simple
graphs with

```text
n=12, minimum degree at least 2, and 12 <= m <= 22.
```

`nauty-geng` produces exactly 308,913,398 isomorphism classes in this range.
There are no signature-two examples. The maximum is one, attained by 39
classes.

## Exact inertia computation

If `(p,z,r)` is the inertia of `Q(G)-2I`, the incidence identities give

```text
s(L(G)) = 2p + z - m.
```

`check_order12.cpp` computes this inertia without floating point. Its fast
path uses fraction-free symmetric elimination with signed 128-bit integers.
For order 12 every row of `Q-2I` has squared norm at most
`(11-2)^2+11=92`; Hadamard's inequality bounds each product of minors used by
the elimination by `92^12 < 2^79`, safely inside the signed 128-bit range.
Cases needing a 2-by-2 pivot use exact rational congruence with Boost
arbitrary-precision integers. The complete run used this fallback on
5,354,397 graphs.

The census was split by edge count. `SHARD_MANIFEST.tsv` records graph
counts, fallback counts, maxima, one exact witness per shard, and the SHA-256
of each complete output. `EXPECTED_OUTPUT.txt` records the merged histogram.
The compact Python verifier checks their internal totals, reconstructs every
listed line graph, recomputes its inertia over exact `Fraction` arithmetic,
and also checks the published order-14 upper-bound witness.

## Reproduce

The production run used Debian 12, nauty 2.8.6, GCC 12.2.0, and Boost 1.74.
Install `nauty`, `g++`, and the Boost development headers, then compile:

```bash
g++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra -Wconversion -Wshadow -pedantic \
  check_order12.cpp -o check_order12
```

Run the eleven independent shards. They may be run concurrently on machines
with sufficient cores.

```bash
mkdir -p reproduced
for m in $(seq 12 22); do
  nauty-geng -cq -d2 12 "$m:$m" \
    | ./check_order12 > "reproduced/result_m${m}.txt"
done
python3 verify_certificate.py --results-dir reproduced
```

For a compact definition-level check that does not rerun the census:

```bash
python3 verify_certificate.py
```

As development validation, `--crosscheck` compared the fast path with the
arbitrary-precision rational path on all 83,339 sparse-range connected graphs
of orders 3 through 9. An UndefinedBehaviorSanitizer and signed-overflow build
passed the same complete corpus. The resulting summary SHA-256 was
`f99a357ac40d899df44c48ee6675a91e0dd30032020934e16e5bcd233b4605c6`.

## Scope and trust boundary

Completeness trusts nauty 2.8.6's isomorph-free generation and the two cited
accepted finite theorems. Arithmetic correctness trusts GCC, Boost, CPython,
the operating system, and hardware, mitigated by the proved fast-path bound,
arbitrary-precision fallback, exact cross-checking, sanitizer run, shard
hashes, aggregate identities, and the independent direct-line-graph verifier.
The compact files authenticate the recorded run; full proof reproduction
requires rerunning the generator and checker.

This theorem does not decide order 13 and does not prove the conjectural
cyclomatic inequality `2s(L(G))<=c(G)+1`.

Primary context:

- [Akbari--Elphick--Kumar--Pragada--Tang](https://arxiv.org/abs/2508.01163)
- [Francis--Uptain](https://arxiv.org/abs/2607.22874)
- [Paone--Paone](https://doi.org/10.5281/zenodo.21706797)
