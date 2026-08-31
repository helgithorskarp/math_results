# Cyclic degree-six obstruction for exact 7-step domination

## Result

Let

\[
\Gamma=\operatorname{Cay}(\mathbb Z/N\mathbb Z,
\{\pm a,\pm b,\pm c\})
\]

be connected and simple, with three distinct non-involutory inverse pairs.
Then \(\Gamma\) has no exact \(7\)-step dominating set of cardinality \(4\)
or \(6\).

Combined with the separately verified degree-at-most-five obstruction, this
excludes every connected Cayley graph of a finite cyclic group with an
inverse-closed connection set of cardinality at most six as a four- or
six-center exact \(7\)-step witness. (A cyclic group has at most one nonzero
involution, while an inverse-closed set of even size has an even number of
involutions, so a degree-six cyclic connection set necessarily has three
non-involutory inverse pairs.)

This does not settle noncyclic abelian Cayley graphs with three generator
pairs, nonabelian Cayley graphs, non-Cayley graphs, or the value of \(m(7)\).

## Finite reduction

Write

\[
\Sigma_7=\{x:d_\Gamma(0,x)=7\}.
\]

If an exact dominating set \(S\) has \(k\) centers, the translates
\(s+\Sigma_7\), \(s\in S\), partition the group. Hence

\[
N=k|\Sigma_7|.
\]

Every element of \(\Sigma_7\) is represented by an integer coefficient
triple of \(\ell_1\)-norm seven. The three-dimensional Lee shell has

\[
|\{(x,y,z)\in\mathbb Z^3:|x|+|y|+|z|=7\}|=4\cdot 7^2+2=198
\]

vectors, so \(|\Sigma_7|\le198\) and \(N\le6\cdot198=1188\). Also \(N\)
must be divisible by four or six.

## Unit-orbit normalization

Represent a non-involutory inverse pair by the unique integer
\(r\) with \(1\le r<N/2\). A triple \(\{a,b,c\}\) generates the cyclic
group exactly when

\[
\gcd(N,a,b,c)=1.
\]

Multiplication by a unit modulo \(N\) is a group automorphism and preserves
the Cayley graph, its radius-seven sphere, and the translate-tiling question.
The enumerator uses the following lossless normalization.

For a generator \(a\), put \(d=\gcd(a,N)\). The unit group acts transitively
on the residues having gcd \(d\) with \(N\), up to sign: there is a unit
\(u\) for which the inverse-pair representative of \(ua\) is \(d\). Choose a
generator whose gcd with \(N\) is numerically minimal. Every unit orbit thus
has a representative containing the divisor \(d\), with both other generator
gcds at least \(d\). The program enumerates exactly these normalized
descriptions and marks all normalized descriptions in each unit orbit before
evaluating it.

The complete counts are

```text
radius=7
maximum_group_order=1188
eligible_orders=396
normalized_descriptions=39806626
generating_normalized_descriptions=29453918
unit_orbits=18339216
four_center_counting_candidates=3535
six_center_counting_candidates=122095
four_center_tilings=0
six_center_tilings=0
```

For each orbit, `enumerate_cyclic_degree6.cpp` computes \(\Sigma_7\) without
graph traversal. It maps all 377 coefficient vectors of \(\ell_1\)-norm at
most six and all 198 vectors of norm seven into the cyclic group; the sphere
is the set of norm-seven images not already represented at smaller norm.

Only the 125,630 orbits satisfying the necessary counting identity enter the
tiling test. Put \(D=\Sigma_7-\Sigma_7\). After fixing one translate at zero,
the remaining \(k-1\) shifts must form a clique under the compatibility
condition that every pairwise difference lies outside \(D\). The counting
identity turns pairwise disjointness into coverage, so this clique search is
equivalent to a translate tiling.

## Independent checker

`check_cyclic_degree6_candidates.cpp` uses different decisive algorithms.

1. It derives the total 18,339,216 generating unit orbits with Burnside's
   lemma. For a unit acting on inverse pairs, a fixed three-subset must be a
   union of permutation cycles of lengths \(1+1+1\), \(1+2\), or \(3\).
   A gcd-state dynamic program retains exactly the generating fixed subsets.
2. It canonicalizes every emitted candidate under all units and rejects a
   duplicate orbit.
3. It recomputes all graph distances with a full BFS, independently of the
   coefficient-image method.
4. It searches directly for an exact cover by sphere translates, independently
   of the enumerator's difference-clique search.

It reports

```text
burnside_unit_orbits=18339216
candidate_unit_orbits=125630
four_center_candidates_checked=3535
six_center_candidates_checked=122095
four_center_tilings=0
six_center_tilings=0
```

The Burnside calculation independently verifies the size of the full orbit
universe. The checker independently validates every emitted counting
candidate and every tiling decision. Selection of the 125,630 counting
candidates from the 18,339,216 orbits remains in the transparent enumerator;
the checker does not rescan all orbit representatives.

## Reproduction

Tested with GCC 12.2.0 on Debian 12. The candidate descriptors and command
output belong under `/scratch` and are not repository artifacts.

```bash
g++ -std=c++20 -O3 -DNDEBUG -march=native \
  -Wall -Wextra -Wpedantic \
  enumerate_cyclic_degree6.cpp \
  -o /scratch/enumerate_cyclic_degree6

g++ -std=c++20 -O3 -DNDEBUG -march=native \
  -Wall -Wextra -Wpedantic \
  check_cyclic_degree6_candidates.cpp \
  -o /scratch/check_cyclic_degree6_candidates

/scratch/enumerate_cyclic_degree6 \
  /scratch/cyclic-degree6-candidates.txt

wc -l /scratch/cyclic-degree6-candidates.txt
sha256sum /scratch/cyclic-degree6-candidates.txt

/scratch/check_cyclic_degree6_candidates \
  /scratch/cyclic-degree6-candidates.txt
```

The generated descriptor file has 125,630 lines and SHA-256

```text
45d5b2367890e5df18d7c79563f61173e1e42d7e430a34978271df46d1199e1f
```

Source SHA-256 values:

```text
enumerate_cyclic_degree6.cpp         15b474c9fa03763911bff7c71d206d29fa5acf344429ff5431effdbcfe5ffbf2
check_cyclic_degree6_candidates.cpp  0da1dc1760d55bfb88a5f86b7764692120f9814ad62f8ba54317d8a3a7519766
```

## Status, trust boundary, and novelty scope

This is an exact computer-assisted theorem. Its trust boundary consists of
the elementary sphere/order reduction, the unit-orbit normalization,
completeness of the C++ enumeration, the independent Burnside universe count,
the two sphere and tiling implementations, and the compiler/runtime. All
arithmetic, graph, and tiling operations are exact. No heuristic result,
solver proof, or external certificate enters the claim.

Targeted searches through 2026-08-31 found the foundational papers below but
no prior exact-seven obstruction for cyclic Cayley graphs. The result is
therefore apparently new to the searched sources, not a claim of priority.

- P. Hersh, *On exact n-step domination*, Discrete Mathematics 205 (1999),
  235--239, <https://doi.org/10.1016/S0012-365X(99)00024-2>.
- L. K. Williams, *On Exact n-Step Domination*, Ars Combinatoria 58 (2001),
  13--22,
  <https://combinatorialpress.com/article/ars/Volume%20058/volume-58-paper-2.pdf>.

The corrected degree-four, verified degree-five, and involutory degree-six
source directories are adjacent directories in this repository.
