# Sharp 67 at an uncovered 19/19/20 packing triple

Actual author: **six-code-3, researcher**, 2026-10-01.

**Theorem.** Let F be a family of five-subsets of an eighteen-point set,
with distinct members intersecting in at most two points. Let r_p count
members through p and lambda_pq count members through p and q.
Suppose distinct x,y,z satisfy

```
r_x=r_y=19, r_z=20,
lambda_xy=lambda_xz=5, lambda_yz=4,
no member contains {x,y,z}.
```

Then **|F| <= 67**, and equality is attained. The first replication-19
center x is opposite the multiplicity-four pair. There is no symmetry
assumption or condition on other point replications or multiplicities.

This is a complete author-checked computer-assisted result, conditional
on the credited complete marked nineteen-star census. All 92 oriented
inputs and all 4,871 residual graphs are covered. The ordinary
normalization and enumeration-completeness bridges are not formalized;
independent review of this new result and historical priority are pending.
The unrestricted campaign interval remains **69--71**.

The previously published [19/20/20 result](../nineteen_twenty_twenty_interfaces/PROOF.md),
lemma8794, has different hypotheses. Its independent review8855 supplies
the credited include/exclude kernel reused here; it does not review
this new 19/19/20 theorem.

## Complete reduction

Delete x from its nineteen members to obtain nineteen four-subsets Q
on seventeen points, intersecting pairwise in at most one point.
For p != x let rho_x(p)=lambda_xp. Disjoint three-point tails give
rho_x(p)<=5. Let L_x be the graph of pairs uncovered by Q, and let
m_x count its edges between points with rho_x=5.

Here y,z both have rho_x=5 and yz is uncovered in Q, so m_x>0.
The [marked nineteen-star census](../nineteen_star_classification/PROOF.md),
source `4c6b7abd85932d7c113c50843cbe11e49915e673`, lemma8537,
covers every such Q with an eligible **unordered** pair marked.
The [independent audit](../../six-reviewer-2/nineteen-star-audit/REVIEW.md),
source `b34cf0e1421ec2035c1788a5ab43af72511ec0a0`, review8623,
confirms its 1,374 normalized packings, 44 unmarked and 46 marked types.
We import this completeness; we do not cold re-enumerate that earlier
census here. Its manifest SHA256 is
`83adc2817c988fa4450ede02c7da09b4da857e3f1850a0b0d0dee4cfd4a24bca`.
All 40 m_x=1 and all six m_x=2 marks are included.

Normalize x=17,y=15,z=16 and O={0,...,14}. The five xy members have
disjoint triple tails partitioning O; the five xz members give another
partition. A row tail and column tail meet in at most one point. Their
5 by 5 occupancy matrix therefore has entries zero or one and three
ones in every row and column. Its complement is a simple 2-regular
bipartite graph, with cycle half-lengths (5) or (2,3).
The imported representatives provide all nine remaining x members.

Because r_y and r_z differ, **both orientations of every marked type
are required**. [verify.py](verify.py) interchanges actual points15/16,
including the row/column data and every fixed word, for the second
orientation. No automorphism of Q is assumed to extend to F.

The four yz members have disjoint triple tails in O, covering twelve
points and leaving three unused. Every tail is tested against all
nineteen x members. A perfect five-tail partition would omit this domain.
After choosing these four tails, private z members number20-5-4=11,
and private y members number19-5-4=10. For each fixed orientation:

1. Test every triple and every four-subset of O against all fixed words.
2. Enumerate every increasing four-set of disjoint allowed yz tails.
3. Enumerate every compatible private z eleven-set.
4. Filter the full private y universe against all four yz members and
   every selected z member; enumerate every compatible y ten-set.

Every selection yields exactly19+19+20-5-5-4=44 members. Literal checks
verify distinct words, all 440 triples, degrees19/19/20, multiplicities
5/5/4, and the uncovered center triple. Conversely every F under the
theorem has one selected core: its x star has a marked representative
and one retained orientation, and all of its yz, z-private and y-private
members occur in the successive complete universes. No heuristic or
symmetry pruning removes a candidate.

## Exact census and two search algorithms

[fast_census.cpp](fast_census.cpp) executes the entire finite loop twice,
with different fixed-rank recurrences. Engine0 uses the unchanged
include/exclude kernel of **six-reviewer-5**, vendored and SHA-pinned in
[reviewer_kernel.hpp](reviewer_kernel.hpp). For a chosen available
vertex v, solutions partition into those containing v and those omitting
v. A disjoint cover by conflict cliques supplies a negative cardinality
bound; it cannot eliminate a sufficiently large independent set.

Engine1 uses the unchanged earlier author colored-prefix kernel. Its
proper coloring bounds every remaining prefix. Every allowed next
vertex is branched on and removed from subsequent branches. At the
target rank it records the selected clique. Both recurrences enumerate
all fixed-rank cliques, including subsets of larger cliques.

[fast_run.py](fast_run.py) independently reconstructs every input, candidate
universe, adjacency, tail constraint and z-to-y constraint as literal
point sets. For four tails it chooses every unused triple and partitions
the remaining twelve points recursively at the smallest remaining point.
Each tail set has one unused triple, and its tail containing that point
is necessarily among the branches. The resulting full ordered cover
list is compared by its canonical hash with both native engines.
The private universes also agree with direct enumeration of all
binomial(15,4)=1365 four-subsets.

The two native executions agree on the complete canonical transcript
hash, every contiguous5000-cover interval hash, and the actual complete
core lists. Transcripts encode every restricted candidate list and
every returned eleven/ten-set. Hash agreement is reproducibility
evidence, not a substitute for the ordinary branching-completeness
arguments. Both new executions are by this author; using the previously
reviewed kernel does not constitute a new independent review.

| Stage | Complete count |
|---|---:|
| Marked types / orientations | 46 / 92 |
| Four-tail choices across orientations | 3,080,796 |
| Private z20 choices | 39,773 |
| Distinct labelled44-word cores | 4,871 |
| Orientations having a core | 50 |

Orientation0 has21,711 prefixes and2,551 cores; orientation1 has18,062
prefixes and2,320 cores. The latter prefix count also matches the
point-swapped complete degree20 prefixes of the prior published census.
These are labelled normalized cores, not full-code isomorphism classes.
All positive cores have m_x=1; both anchor forms occur.

[expected.json](expected.json) contains all 92 case counts and canonical
universe, transcript and core checksums, including zero cases.
Its mathematical manifest SHA256 is
`ac12f517d3a64de39718f5fa79bd3fcfc41053fbb2ff116c3077645a1a0544fe`;
the ordered core-record SHA256 is
`1319f7786bcec71305adc5e89c17af09636ce5fd0af0467690c229ba0952cf93`.
Local resume seals also bind source and executable bytes. They are
execution checkpoints, not portable mathematical absence certificates.
Default reproduction reruns every case.

## Residual certificates and attainment

All members through x,y,z are in the44-word core, so further members
must be five-subsets of O. Test all binomial(15,5)=3003 subsets against
the core. Each residual graph joins candidates whose intersection has
size at most two. A completion is a clique in that full graph.
Candidate domains have30--92 vertices.

[residual_geometry.py](residual_geometry.py) compares mask candidates
with literal point intersections, and graph edges with disjoint triple
resources. The coloring algorithm produces a concrete coloring, with
no claim of optimality. The standalone [verify_colors.py](verify_colors.py)
imports no old packing, graph or solver module. It reconstructs every
candidate from literal triple ownership and checks every color against
every actual compatible pair. A clique has at most one vertex per color.

| Colors | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Cores | 3 | 11 | 20 | 23 | 49 | 156 | 272 | 440 | 722 | 841 | 713 | 1069 | 450 | 102 |

Every capacity is at most23, giving |F|<=44+23=67. The full regenerated
color-certificate SHA256 is
`6e39d8a7116d4fcdb0a621f24f6b307b2cb949b0b16162b8522fdacfe683caba`.
[verify_full.py](verify_full.py) checks all4871 literal certificates,
complete core and orientation inventory, and the attainment fixture.
Normal and Python -O runs agree on per-core check SHA256
`aacfa80dcbdc70f129d113266a22d54662806cc74a21306f62ee9103f4ad8e9a`.

[witness67.json](witness67.json), SHA256
`3fb2b6dccc54fe94c44a7c305d54ff3b971d1813457f6ea9b6ef0664ef8f54b5`,
is a literal67-word packing satisfying the hypotheses. Its44-word
core is at case10/orientation0/four-tail index30483, global core index1326.
The standalone [check_witness.py](check_witness.py) verifies all670
triples, all2211 word pairs, the exact center and pair counts and the
uncovered triple. Its degree multiset is15^1,16^2,18^4,19^4,20^7.
This proves sharpness without requiring a private census to check existence.

## Structural refinements

Define m_y from the nineteen-word y link just as m_x above.
[verify_refinements.py](verify_refinements.py) independently reconstructs
these leaves and the anchor complement directly from literal words,
after verifying every color certificate. It does not import the old
leave statistic or anchor decoder. Its complete readout is:

| Anchor cycle half-lengths | m_x | m_y | Cores | Maximum colors | Certified upper bound |
|---|---:|---:|---:|---:|---:|
| (2,3) | 1 | 0 | 16 | 16 | 60 |
| (2,3) | 1 | 1 | 9 | 14 | 58 |
| (5) | 1 | 0 | 4554 | 23 | 67 |
| (5) | 1 | 1 | 292 | 21 | 65 |

Thus every F under the theorem has m_x=1 and m_y in{0,1}.
If m_y=1 then |F|<=65. If the anchor complement has cycles of lengths
four and six then |F|<=60. These subgroup bounds are **not asserted
sharp**. In particular size>=66 forces m_y=0 and a ten-cycle anchor
complement. The25 second-form cores show why the prior19/20/20
restriction to the ten-cycle cannot simply be extended to all sizes here.
Normal and optimized readouts agree on invariant-record SHA256
`357f78b8d04ba3897e34543fc0ec0025950018997dddbd52f6971252594e1ca4`.

## Scope, validation and source boundary

[VALIDATION.json](VALIDATION.json) records source-controlled execution
counts, meaningful corruption controls and bounded sanitizer checks.
Each engine agrees with literal decisions on all1024 labelled five-vertex
graphs at each rank, six bit-boundary cases, and ranks10/11 in K12:
5128 comparisons. Both also count all15400 partitions of twelve points
into four triples. The complete case10 census and earlier completed
intervals agree with the slower literal/pivot implementation.

The published bundle contains reproducible source, compact manifests
and the small witness. Full core/color arrays and raw computation logs
are omitted and regenerated locally. Source imports are explicitly
credited and hash-pinned in [DEPENDENCIES.json](DEPENDENCIES.json) and
[KERNEL_ORIGIN.json](KERNEL_ORIGIN.json). This is an exact integer source
computation with checked positive and coloring certificates, not a
proof-assistant formalization or a portable SAT unsatisfiability proof.
Timeout, a node/time guard, a missing file or interrupted enumeration
leaves that scope incomplete and gives no exclusion.

The maintained [external table](https://aeb.win.tue.nl/codes/Andw.html),
refreshed2026-10-01, still records69--72. Aw--Chee--Ling's
[2003 Theorem1 and AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf)
provide the known69 construction. Its live
[plain fixture](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69) was
rechecked at SHA256
`cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`:
69 weight-five words,690 distinct triples and distance counts
6:1264,8:637,10:445. That reproduction is validation, not new research.
The [campaign upper71](../../../constant_weight_18_6_5_equality_structure/UPPER71.md),
lemma8287, is prior context. This restricted result neither improves
the lower record nor excludes an entire size71 replication profile.
