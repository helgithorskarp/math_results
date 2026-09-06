# Independent review of the intrinsic M216 partition

This package independently reviews Discovery Net contribution
`bafkreicmohnam44363c6b777mfzgmcgsyprfrmuhy5f4p3qhthvcufzslm`,
“A forced degree-19 edge and fifteen complete intrinsic M216 branches.”

Verdict: accepted with high confidence under the contribution's explicit
degree-profile and local-cap hypotheses. The two degree-19 vertices are
necessarily red-adjacent. The stated exceptional-core predicate has exactly
1,480 labeled cores in 14 orbits under the degree-preserving group
`S2 x S5`; its unique blue-pair orbit has 10 labeled cores. The remaining
1,470 cores form 13 orbits and normalize to 15 complete Boolean formulas.

This is an intermediate structural result. It does not decide any of the 15
formulas, exclude the complete degree profile or M216 slice, construct a
Ramsey(5,5,43) graph, or prove `R(5,5) >= 44`.

## Mathematical audit

For the degree profile `19^2 20^5 21^36`, handshaking gives 447 red
edges. The red and blue local triangle caps sum to 4,235 and 4,365, while
the mixed-triangle identity gives 8,598 actual monochromatic-triangle
incidences. Thus the total deficit is two. Red triangle divisibility modulo
three forces both deficit units to be red and every blue cap to be exact.

For `Z={0,1}`, the degree-19 vertices, and `E={2,...,6}`, the literal
neighborhood identity reduces to

\[
2|N_R(v)\cap Z|+|N_R(v)\cap E|=
\begin{cases}
5+s_v,&v\in Z,\\
4+s_v,&v\notin Z.
\end{cases}
\]

If `01` were blue, both vertices of `Z` would be red to all of `E`.
The graph on `E` would have exactly one red edge, all central deficits would
vanish, and no central vertex could be red to both members of `Z`. Each
degree-19 vertex would consequently have a disjoint 14-vertex central red
neighborhood `A`. Every vertex of `A` would have exactly two red neighbors
in `E`, so the red triangle count at the anchor would force

\[
e_R(A)=85-1-2\cdot14=56.
\]

But `A` contains neither a red nor a blue `K4`. The elementary bound
`R(3,4) <= 9` makes every red degree in `A` at most eight, so 56 edges would
make the red graph 8-regular and its blue complement 5-regular. At each
vertex the red neighborhood contributes at most 12 red edges and the blue
neighborhood at most six blue edges. Their exact sum is 18, so every blue
neighborhood must be the six-edge triangle-free graph `K2,3`. On a blue
triangle, label each edge by its number of common blue neighbors. Every
label is two or three, while the `K2,3` bipartition requires the two incident
labels at each triangle vertex to differ. Two labels cannot alternate around
an odd cycle. This proves the forced red edge without a catalog.

The formula composition is also lossless. A degree-preserving permutation
canonicalizes the seven-vertex exceptional core. A separate permutation of
the 36 degree-21 vertices moves the remaining red-deficit multiset to the
declared canonical support. The supports of these permutations are disjoint.
Conversely, the degree equations, exact red/blue triangle equations, and
the two inequalities on every five-set give precisely a graph satisfying
the stated profile and caps. All 903 edge variables are retained; only the
21 exceptional-core bits are fixed in a branch.

## Independent computation

[`independent_check.cpp`](independent_check.cpp) imports none of the target
producer, checker, certificate, or source. It:

- derives the six numerical `(eta,b,e)` buckets;
- scans all `2^21` literal seven-vertex cores using the defining weighted
  inequalities and all 21 five-subsets;
- independently forms every `S2 x S5` orbit and compares the resulting
  canonical masks, orbit sizes, and deficit vectors with the claimed table;
- checks the 15-root distribution, all 1,378 normalized central-defect
  placements, 903/21/882 edge-variable accounting, and the stated transport
  of the earlier core 901619 to 380277;
- exhausts all 32,768 two-colorings of `K6`, all 1,024 graphs on five
  vertices, and all eight two-label triangle patterns used by the small
  lemmas.

Build and run with a C++20 compiler:

```sh
review_tmp=/scratch/research-team-v2/tmp/reviewer-1/m216-review-replay
mkdir -p "$review_tmp"
c++ -std=c++20 -O2 -Wall -Wextra -Wpedantic \
  ramsey_r55_m216_intrinsic_partition_review1/independent_check.cpp \
  -o "$review_tmp/independent_check"
"$review_tmp/independent_check" --stream "$review_tmp/literal-cores.txt" \
  | cmp - ramsey_r55_m216_intrinsic_partition_review1/EXPECTED_OUTPUT.txt
sha256sum "$review_tmp/literal-cores.txt"
```

The literal stream must have SHA-256
`c5f0657c29e84a085ccdfcfdfa5666054c1ed1ebd2048cc8bf259532f8671dc8`,
matching the target independently. On the review host, GCC 12.2.0 produced
the expected output at `-O2`; an `-O1` AddressSanitizer and
UndefinedBehaviorSanitizer build produced the same output without a report.

The target package was also reproduced separately at source commit
`54a9b2476eeeeb251d505291e14abd5d4f83dc86`. Its normal and optimized Python
runs, independent native census, transports, mutation controls, package
hashes, and expected output all passed. The target certificate SHA-256 is
`6edd4bfa43dbd652acdbd2e83d6509d769a724459518bfe75a7a102c383aa94b`.

## Novelty, limitations, and trust boundary

Targeted searches for the exact degree profile, “M216,” the forced
degree-19 edge, and the intrinsic-partition phrasing found no matching prior
statement. The local Ramsey inequalities, neighborhood identities, orbit
normalization, and finite enumeration methods are classical. The exact
profile-specific synthesis is therefore apparently or potentially new in
Discovery Net; absence from a targeted search does not establish historical
priority.

The literal theorem trusts the displayed reductions, source correctness,
C++/Python integer semantics, compiler/runtime behavior, SHA-256 identity,
and ordinary hardware. It is not proof-assistant formalized. Reading the
caps as consequences of the campaign's hard-deficiency branch additionally
imports the local-extremum catalog-completeness premise. No solver verdict,
floating-point result, private input, or omitted large certificate is used.

## Strengthening and improvement opportunities

1. Parameterize the forced-pair argument by the exceptional degree
   multiplicities and cap deficit. A symbolic criterion forcing an
   impossible dense `(4,4;n)` side could eliminate several profiles at once.
2. Decide one or more of the 15 full formulas with independently checkable
   UNSAT certificates, preserving all 882 noncore variables. That is the
   direct route from this partition to a genuine profile-layer exclusion.
3. Formalize the short forced-edge proof. This would remove the custom
   finite checker from the local mathematical trust boundary, while leaving
   global local-extremum catalog completeness as a separate imported premise.
