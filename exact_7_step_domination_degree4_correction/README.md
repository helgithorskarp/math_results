# Corrected abelian degree-four exact-7 obstruction

## Result

Let \(\Gamma=\operatorname{Cay}(A,X)\) be a connected Cayley graph of a
finite abelian group, with \(X=-X\), \(0\notin X\), and \(|X|\le 4\). Then
\(\Gamma\) has no exact 7-step dominating set of cardinality 4 or 6.

This directory repairs the exhaustive verification in the earlier
`exact_7_step_domination` directory. The theorem survives, but the earlier
enumeration counts and its claimed completeness do not.

## The repaired completeness gap

The earlier C++ and Python programs stopped their connectivity BFS when a
vertex at distance 7 was dequeued. They then called the graph connected only
if the truncated BFS had visited the whole group. Thus every connected Cayley
graph with eccentricity greater than 7 was incorrectly discarded.

For example,

\[
\operatorname{Cay}(\mathbb Z/18\mathbb Z,\{\pm1\})
\]

is connected and has eccentricity 9, but the radius-capped test leaves vertex
9 unvisited. Both corrected programs contain this example as a regression
test. Connectivity is now computed by a full BFS. A separate radius-capped BFS
in the C++ program is used only after connectivity has been established and
only to extract the radius-7 sphere.

## Finite reduction

Write \(\Sigma_7=\{a\in A:d(0,a)=7\}\). If \(S\) is an exact 7-step
dominating set, the translates

\[
\{s+\Sigma_7:s\in S\}
\]

partition \(A\), so \(|A|=|S||\Sigma_7|\).

If \(X=\{\pm g,\pm h\}\), every element of \(\Sigma_7\) has a geodesic
expression \(ag+bh\) with \(|a|+|b|=7\). There are 28 such coefficient
pairs. With one non-involutory inverse pair and at most two involutions, the
free-model sphere has at most 8 elements. An involution-only connection set
has diameter at most 4. Hence \(|\Sigma_7|\le 28\), and a four- or six-center
witness has \(|A|\le 168\).

The C++ verifier generates every abelian group of order at most 168 in
invariant-factor form and every relevant inverse-closed connection set. It
losslessly skips group orders divisible by neither 4 nor 6, computes full
connectivity and exact distances, and runs a complete translate exact-cover
search on every counting candidate. Its corrected summary is

```text
radius=7
maximum_group_order=168
invariant_factor_types=321
eligible_invariant_factor_types=187
connection_sets_examined=512664
connected_connection_sets=92230
connected_sets_with_eccentricity_over_radius=86166
four_center_counting_candidates=0
six_center_counting_candidates=2258
four_center_tilings=0
six_center_tilings=0
```

The 86,166 connected cases with eccentricity greater than 7 make the repaired
coverage explicit. An unfiltered diagnostic run over all group orders found
224,229 connected connection sets and the same 2,258 relevant six-center
candidates.

## Independent implementation

The Python verifier uses a different representation and deliberately more
redundant enumeration. It covers all one- and two-generator groups as
\(\mathbb Z/m\mathbb Z\times\mathbb Z/n\mathbb Z\), where \(m\mid n\), and
then separately covers the remaining mixed case of one non-involutory pair
and two involutions in arbitrary invariant-factor rank. Its corrected counts
include

```text
examined_one_generator_sets=11170
examined_two_generator_sets=628183
connected_one_generator_sets=1810
connected_two_generator_sets=323010
connected_one_generator_sets_over_radius=1798
connected_two_generator_sets_over_radius=301643
four_center_counting_candidates=0
six_center_counting_candidates=9032
four_center_translate_tilings=0
six_center_translate_tilings=0
mixed_connection_sets_examined=6748
mixed_connected_connection_sets=1082
mixed_connected_sets_over_radius=341
mixed_four_center_counting_candidates=0
mixed_six_center_counting_candidates=0
mixed_four_center_translate_tilings=0
mixed_six_center_translate_tilings=0
```

The factor-of-four difference between 9,032 and 2,258 reflects redundant
ordered/sign-related generator descriptions in the Python search; both
implementations independently find no translate tiling.

## Reproduce

Tested with GCC 12.2.0 and Python 3.11.2 on Debian 12.

```bash
g++ -std=c++20 -O2 -Wall -Wextra -Wpedantic \
  verify_abelian_degree4_corrected.cpp \
  -o /scratch/verify_abelian_degree4_corrected
/scratch/verify_abelian_degree4_corrected

python3 verify_rank2_abelian_corrected.py
```

Source SHA-256 values:

```text
verify_abelian_degree4_corrected.cpp  20485b860152aa34bba70fff9dd26f5bdd6922bc71bc2ebde86e172dca4ca529
verify_rank2_abelian_corrected.py      847fda6c63dc23abebc6aebf4106b42b6af82863fa10725d4411b57fe291056e
```

## Trust boundary

The theorem is a finite computational result. It relies on the elementary
sphere-size reduction, the invariant-factor classification of finite abelian
groups, the two source implementations, and their compilers/runtimes. All
graph distances and exact-cover decisions use exact integer and set
operations. No heuristic result, SAT solver, proof log, or external
certificate decoder enters the claim.

The result corrects and independently reproduces the theorem rather than
claiming a new obstruction. It does not resolve \(m(7)\): non-Cayley graphs,
nonabelian Cayley graphs, and abelian Cayley graphs of degree at least five
remain open.

