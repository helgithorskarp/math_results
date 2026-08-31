# Abelian degree-four obstruction for exact 7-step domination

## Result

Let `Cay(A,X)` be a connected Cayley graph of a finite abelian group, where
`X=-X`, `0` is not in `X`, and `|X| <= 4`.  This graph has no exact 7-step
dominating set of cardinality 4 or 6.

Consequently the unresolved alternatives `m(7)=4` and `m(7)=6` in Hersh's
minimum exact-step-domination problem cannot be witnessed by an abelian
Cayley graph of degree at most four.

This is an exact computational theorem, not a construction and not a
resolution of `m(7)`: non-Cayley graphs, nonabelian Cayley graphs, and abelian
Cayley graphs of degree at least five remain possible.

## Finite reduction

Write `Sigma_7` for the sphere of radius 7 about zero.  If `S` is an exact
7-step dominating set in a Cayley graph, the translates

```text
{s + Sigma_7 : s in S}
```

partition `A`.  In particular,

```text
|A| = |S| |Sigma_7|.
```

There are only three forms of inverse-closed connection set of size at most
four.

1. For two non-involutory pairs `{+g,-g,+h,-h}`, every element at distance 7
   has a geodesic representative `a*g+b*h` with `|a|+|b|=7`.  There are only
   `4*7=28` such coefficient pairs.
2. For one pair `{+g,-g}` and at most two involutions, a geodesic uses each
   involution at most once.  The radius-7 sphere has size at most
   `2*(1+2+1)=8`.
3. With involutions only, the diameter is at most four, so the radius-7 sphere
   is empty.

Thus `|Sigma_7| <= 28`.  A four- or six-center witness would have
`|A| <= 6*28 = 168`, reducing the claim to a finite classification.

## Exact enumeration

`verify_abelian_degree4.cpp` independently performs the following steps.

- Generate every finite abelian group of order at most 168 in invariant-factor
  form `Z/d1 x ... x Z/dr`, with `d1 | ... | dr`.
- Generate every relevant inverse-closed connection set: one or two
  non-involutory inverse pairs, with up to two involutions when there is only
  one pair.  Involution-only sets were eliminated above.
- Use breadth-first search to compute the exact radius-7 sphere.
- Retain the necessary counting cases `|A|=4|Sigma_7|` or
  `|A|=6|Sigma_7|`.
- For every counting case, run a complete exact-cover search for four or six
  translates of the sphere.  Translation symmetry fixes the first center at
  zero.  At each branch, the verifier takes the first uncovered group element
  and tries every sphere translate containing it, so the search is complete.

The C++ verifier examines 321 abelian group types and 670,641 raw connection
sets, of which 17,040 are connected.  There are no four-center counting
candidates.  There are 96 raw six-center counting candidates, but none of
their radius-7 spheres tile the group by six translates.

`verify_rank2_abelian_obstruction.py` is an independent implementation.  It
enumerates all one- and two-generator cases through the sharp order bound and
then separately enumerates the only remaining mixed case (one inverse pair
and two involutions).  It independently runs the translate-tiling test.
Its more redundant enumeration finds 384 raw six-center counting candidates
and again zero tilings; it finds no mixed-case counting candidates.

## Reproduction

Tested with GCC 12.2.0 and Python 3.11.2 on Debian 12.

```bash
g++ -std=c++20 -O2 -Wall -Wextra -Wpedantic \
  verify_abelian_degree4.cpp -o /tmp/verify_abelian_degree4
/tmp/verify_abelian_degree4

python3 verify_rank2_abelian_obstruction.py
```

Source SHA-256 values:

```text
verify_abelian_degree4.cpp          fd68fbd0e61ee2bc950c6a62a4b329f41db170aef1762a952abf488da5013f78
verify_rank2_abelian_obstruction.py 3eb3037c69041c8b64435e9077c3dfbae45cbe0bca322d7b4aa432b2bc2e35da
```

The programs use only exact integer arithmetic and standard-library graph
search.  The remaining computational trust boundary is the correctness of
the two implementations, their language runtimes/compilers, and the finite
enumeration argument described above.  No SAT solver, heuristic output, or
external certificate decoder is used in the theorem.

The two `search_circulant*.cpp` programs are exploratory random searches that
led to the sphere-tiling reduction.  They are preserved for reproducibility
but are not used in the theorem.

## Sources and novelty scope

- Patricia Hersh, *On exact n-step domination*, Discrete Mathematics 205
  (1999), 235-239, DOI `10.1016/S0012-365X(99)00024-2`.
- Lauren K. Williams, *On Exact n-Step Domination*, Ars Combinatoria 58
  (2001), 13-22,
  <https://combinatorialpress.com/article/ars/Volume%20058/volume-58-paper-2.pdf>.

Hersh proved the lower bound `floor(log2(n))+2` and that exact-step dominating
sets have even cardinality.  Thus `m(7)` is either 4 or at least 6; the cited
sources leave the strict `m(7)<7` case open.  Targeted searches for exact
7-step domination, exact-step domination in Cayley graphs, and abelian
exact-step domination found no prior version of the obstruction above.  The
result is therefore apparently new to the searched sources, not a claim of
literature priority.
