# Stable transitivity of tournaments through order seven

## Exact result

Let a `k`-tournament be a complete directed multigraph in which the two
directions on every unordered pair have total weight `k`. It has a
**transitive tournament decomposition** (TTD) if it is the sum of `k`
transitive tournaments on the same labeled vertex set. For an ordinary
tournament `T`, let `m(T)` be the least nonnegative integer `m` for which
there is an `m`-tournament `T'` such that both `T'` and `T+T'` have TTDs, and
put

```text
m(n,1) = max { m(T) : T is a tournament on n vertices }.
```

The computation and certificates here prove:

> **Exact computer-assisted theorem.** Every tournament on at most seven
> vertices becomes a sum of two transitive tournaments after adding one
> transitive tournament. Hence
>
> ```text
> m(n,1) = 0  for n = 1,2,
> m(n,1) = 1  for 3 <= n <= 7.
> ```

The new cases are `n=6,7`. They correct the sentence after the definition of
`m(n,k)` in Davis--Schroeder,
[*Relating tournaments and permutations with xrays*](https://arxiv.org/abs/2606.21532v1)
(2026), which states that Example 3.3 implies `m(n,1)>1` for `n>=6`.

Example 3.3 does prove that a particular `2`-tournament has no TTD. That does
not imply the asserted lower bound: for a fixed ordinary tournament `T`, the
definition of `m(T)>1` requires **every** transitive one-tournament `X` to
fail, whereas one non-TTD `2`-tournament can at most exhibit a particular
failed sum. The certificates here explicitly give a successful `X` for
every tournament through order seven.

This result is apparently new relative to arXiv:2606.21532v1, targeted
primary-source searches performed on 2026-09-03, and the committed Discovery
Net graph through height 1654. This is a search-relative novelty statement,
not a historical-priority claim.

## Finite reduction

Fix the vertex set `[n]={0,...,n-1}` and enumerate the unordered pairs
`(i,j)` in lexicographic order with `i<j`. Encode a tournament `T` by the bit
vector `t`, where `t_ij=1` means `i` beats `j`. Encode a total order in the
same way; its mask is exactly the adjacency vector of the corresponding
transitive tournament.

For transitive tournaments `X,Y,Z`, the identity

```text
T + X = Y + Z
```

holds if and only if, on every pair `i<j`,

```text
t_ij + x_ij = y_ij + z_ij.                 (1)
```

Both sides have total pair weight two, so equality in the reverse direction
then follows automatically. Thus `m(T)<=1` exactly when some order mask `x`
makes the base-four vector `t+x` equal to a sum of two order masks.

The generator performs the following exhaustive computation for `n=7`.

1. Generate all `7!=5040` total orders and all distinct unordered pair sums
   `y+z` (there are 5,844,259).
2. Scan all 21-bit tournament masks in increasing order. On encountering an
   uncovered mask, apply all 5,040 vertex permutations, record its complete
   isomorphism orbit, and mark that orbit covered. Because the scan is
   increasing, each recorded mask is the minimum mask in its orbit.
3. For every nontransitive representative `t`, scan the order masks `x` and
   look up `t+x` among the exact pair sums. Record the first witnesses
   `x,y,z` satisfying (1).
4. Terminate with failure on an overlapping orbit, incomplete coverage, or a
   representative without a witness.

The resulting 456 orbits are disjoint and have total size `2^21=2,097,152`.
There is one transitive orbit and 455 nontransitive orbits with explicit
one-summand witnesses. The analogous order-six certificate has 56 orbits:
one transitive and 55 nontransitive.

Relabeling preserves equation (1), so one witness covers its entire orbit.
The order-seven result implies every smaller upper bound by arbitrarily
extending a smaller tournament to seven vertices and restricting the three
transitive witness tournaments back to the original vertex set. For every
`n>=3`, a tournament containing a directed triangle is nontransitive and
therefore has `m(T)>=1`. This supplies the matching lower bound.

## Independent certificate verification

`generate_certificates.cpp` is the production enumerator. It represents a
pair sum by 21 base-four digits packed into a 64-bit unsigned integer. The
largest used bit position is 41; tournament masks use only 21 bits, and every
stored pair index is below `5040^2`, so the fixed-width bounds are safe.

`verify_certificates.py` does not regenerate the pair-sum table. Instead it:

- reconstructs full adjacency matrices from every representative and total
  order;
- checks every directed entry of `T+X=Y+Z` from the definition;
- independently generates every vertex-relabeling orbit;
- checks the declared orbit sizes, canonical minima, pairwise disjointness,
  and full coverage of all `2^21` labeled tournaments; and
- confirms that the `m=0` class is transitive and every `m=1` representative
  is not.

`exhaustive_labeled.cpp` is a second coverage route: it tests all 2,097,152
labeled tournaments directly, without quotienting by isomorphism. It is not
needed once the compact certificates and Python checker are trusted, but its
matching result guards the symmetry-reduction implementation.

All arithmetic is exact. No solver, randomness, floating point, external
dataset, or uncommitted proof log is used.

## Reproduction

Tested with GCC 12.2.0, `-std=c++20`, and CPython 3.11.2 on Debian 12.

```bash
cd graph_theory/stable_tournaments_order7

g++ -std=c++20 -O3 -DNDEBUG \
  -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
  generate_certificates.cpp -o generate_certificates

./generate_certificates 6 > cert_n6.txt
./generate_certificates 7 > cert_n7.txt

PYTHONDONTWRITEBYTECODE=1 python3 verify_certificates.py cert_n6.txt cert_n7.txt
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verifier.py

g++ -std=c++20 -O3 -DNDEBUG \
  -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
  exhaustive_labeled.cpp -o exhaustive_labeled
./exhaustive_labeled 7

sha256sum -c SHA256SUMS
```

Expected verifier output:

```text
verified n=6: 32768 labeled tournaments in 56 isomorphism classes; m=0 classes=1, m=1 classes=55; sha256=b512c7668435f481fe73f2194f26b9901bc4c99b78cddf1dc6841e4f404026fb
verified n=7: 2097152 labeled tournaments in 456 isomorphism classes; m=0 classes=1, m=1 classes=455; sha256=39ffb0f1a305f072325b5390f3454907b4084a8aa153f102f9e1f9b652679506
```

Expected direct labeled summary:

```text
SUMMARY n=7 represented=2097152 failures=0 lookups=239434139 witness_fnv64=729065742587703121
```

On the test host, the order-seven certificate generator took 5.07 seconds
and reported peak resident memory of 289,248 KiB. The independent Python
verification took 35.37 seconds. The full labeled cross-check took 55.84
seconds. Runtime and hash values are deterministic; timings are descriptive.

## Trust boundary and scope

The theorem trusts the finite reduction above, the inspected C++ certificate
generation, and the much smaller Python definition-level checker. The
checker makes every positive decomposition and all isomorphism-class coverage
independently checkable; it does not prove compiler or hardware correctness.
Sanitizer and standard-library assertion builds were also run on complete
order-six coverage, and a deliberately corrupted certificate was rejected.

No claim is made about `m(8,1)`, the growth of `m(n,1)`, or any `m(n,k)` with
`k>1`.
