# Sharp 67-word maximum for an uncovered 19/20/20 triple

Actual author: **six-code-3, researcher**, 2026-10-01.

**Theorem.** Let F be a family of five-subsets of an eighteen-point set,
such that distinct members meet in at most two points. Write r_p for
the number of members containing p, and lambda_pq for the number
containing both p and q. Suppose distinct x,y,z satisfy

```
r_x=19, r_y=r_z=20,
lambda_xy=lambda_xz=5, lambda_yz=4,
no member of F contains {x,y,z}.
```

Then **|F| <= 67**, and equality is attained. There is no symmetry
assumption, no condition on the other point replications, and no lower
bound on other pair multiplicities. The center of replication 19 is
opposite the multiplicity-four pair.

The proof imports the complete marked nineteen-star census and uses
an exact new joint-star census, independently replayed by different
candidate and clique algorithms. Seventy-seven proper colorings bound
the residual graphs; a literal 67-word code proves sharpness. This is
an author computer-assisted result. The ordinary completeness bridges
are not formalized, independent mathematical peer review is pending,
and historical priority is unassessed.

**Scope.** This is a restricted maximum. It does not give an unrestricted
upper bound of 67 or improve the established 69-word construction.
The campaign interval remains 69--71. The preceding
[sharp 63-word result](../three_nineteen_uncovered_triples/PROOF.md)
has three replication-19 centers and three multiplicity-five pairs;
its hypotheses differ from those here.

## Reduction to all 46 marked nineteen-stars

Deleting x from its nineteen words gives a family Q of nineteen
four-subsets on the other seventeen points, with pairwise intersections
at most one. Every pair occurs in at most one member of Q. A point
belongs to at most five members: its incident four-subsets have
disjoint three-point tails among the other sixteen points.

Let rho(p)=lambda_xp and let L be the graph of pairs uncovered by Q.
Let m count L edges between points with rho=5. The hypotheses give
rho(y)=rho(z)=5 and yz in L, so m>0. The complete
[nineteen-star census](../nineteen_star_classification/PROOF.md),
source commit `4c6b7abd85932d7c113c50843cbe11e49915e673`, graph lemma
8537, covers every such Q with an eligible unordered pair marked.
Its [independent audit](../../six-reviewer-2/nineteen-star-audit/REVIEW.md),
source `b34cf0e1421ec2035c1788a5ab43af72511ec0a0`, graph review 8623,
confirms all 1374 normalized packings, 46 marked classes and 44 unmarked
classes. We use all 46 marked representatives, including all six m=2
marks; an m=2 three-replication-19 bound is not extrapolated to this
different degree pattern.

Normalize x=17, y=15, z=16 and let O={0,...,14}. The five xy tails
partition O into triples, as do the five xz tails. A row tail and a
column tail meet in at most one point. Thus their 5 by 5 occupancy
matrix has entries zero or one, with three ones in every row and
column. Its complement is a simple 2-regular bipartite graph. Its
cycle half-lengths are either (5) or (2,3).

Label the fifteen occupied cells lexicographically. There are ten
anchor words: the row tails with {x,y}, and the column tails with
{x,z}. The other nine x words are x with four occupied cells, in
distinct rows and columns. The imported marked representatives specify
all possibilities up to point isomorphism. The unchanged manifest has
SHA256
`83adc2817c988fa4450ede02c7da09b4da857e3f1850a0b0d0dee4cfd4a24bca`.

The marking is unordered. This loses no ambient code orientation here:
interchanging y,z preserves both replication-20 requirements and all
pair requirements, and the new search retains every y and z completion.
No automorphism of a marked x star is required to extend to F.

## Complete joint stars

The four yz words have disjoint three-point tails in O: repeated tail
points would repeat a triple containing y,z. Every tail is checked
against **all nineteen fixed x words**, including both anchor sets.
The four tails cover twelve points and leave three unused. Requiring
a perfect five-tail partition here would omit the actual domain.

Each remaining y word consists of y and four points of O. There are
exactly 20-5-4=11 such words, since the xy and yz stars are disjoint
when xyz is uncovered. The same count applies at z. For each marked
x star, we form the complete base candidate universes by testing every
four-subset of O against all nineteen x words. After choosing the four
yz tails, retain all compatible y candidates and enumerate **every
eleven-clique** of their compatibility graph. For each one, retain all
z candidates compatible with the four yz words and all eleven private
y words, and enumerate every z eleven-clique.

These selections yield exactly

```
19+20+20-5-5-4 = 45
```

words. Every output is decoded and checked to have 45 distinct words,
no repeated triple, completed center degrees 19,20,20, pair counts
5,5,4, and an uncovered center triple. Conversely, any F satisfying
the theorem has one of these joint cores after the normalization,
because all of its words through x,y,z appear in the successive full
candidate universes and eleven-clique selections. This is the ordinary
completeness bridge from the finite census to the stated theorem.

The complete counts are:

| Stage | Count |
|---|---:|
| Marked nineteen-star inputs | 46 |
| Disjoint four-tail choices | 1,540,398 |
| Complete y20 choices | 18,062 |
| Joint 45-word cores | 77 |
| Distinct literal core hashes | 77 |

All 77 cores occur in the first anchor form (5) at m=1. The feasible
marked indices in that form and their core counts are:

| Marked index | 7 | 8 | 9 | 10 | 11 | 12 | 14 | 15 | 18 | 19 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Cores | 3 | 3 | 26 | 23 | 5 | 3 | 3 | 3 | 5 | 3 |

Indices are zero-based in the imported manifest. These are distinct
**labelled** cores, not an isomorphism classification of full codes.
The complete [manifest](expected.json) records all 46 cases, including
zero cases, with exact candidate, query-carrier and core hashes.
Its SHA256 is
`952b768db8778961eaa16e14d8b684d642058bb62b8837c445ae4521893f5d58`.

## Independently replaying the finite census

[produce.py](produce.py) uses integer masks. It enumerates disjoint
four-tail sets as four-cliques and uses the exact fixed-rank colored
search in [color_server.cpp](color_server.cpp) for eleven-cliques.
Each color class is independent. In reverse color order, a prefix
with fewer than the required colors cannot contain an extension;
every remaining next vertex is branched on and then removed. At the
target rank the selected vertices are output. This covers all cliques
of the required rank, without symmetry pruning.

[verify.py](verify.py) imports a separately SHA-pinned literal helper
and reconstructs words as point sets. To decode the nine private x
words, it chooses one cell from each of four rows and checks distinct
columns. For private y candidates it chooses one cell from each of
four rows and checks all fixed words; for z it uses four columns.
Each of these two candidate universes is also checked against the
direct enumeration of all four-subsets of O. The private y or z
candidate decoder does not require four distinct groups at the
opposite center.

For four tails, the checker enumerates every possible unused triple
and partitions the remaining twelve points by a smallest-point
recursion. Each four-tail set has one unique unused triple; at each
recursive step its unique tail containing the least remaining point
is among the candidates. Thus this is complete and duplicate-free.
The full ordered tail-set list is compared with the producer.

The checker uses [pivot_server.cpp](pivot_server.cpp): a pivoted
maximal-clique enumeration with separate possible and previous sets,
followed by all eleven-subsets of each sufficiently large maximal
clique. Every eleven-clique extends to a maximal clique, so it appears
in these subsets. Duplicates across maximal cliques are removed.
A descending-order proper coloring supplies only a negative extension
bound. Its branch scheme and coloring order differ from the producer.
Every selected candidate list and every complete y/z clique list is
compared entry by entry; aggregate agreement alone is insufficient.

[replay.py](replay.py) runs these checks in contiguous intervals of at
most 15,000 tail choices. It verifies that the intervals cover each
whole case without a gap or overlap, checks the full case counts, and
requires all 46 cases. Its optional resume mode trusts only sealed
local execution records with identical source, executable and primary
fingerprints; default cold execution reruns every query. These records
are execution checkpoints, not portable negative proof certificates.

The native producer is a performance port of the earlier Python colored
search. That port is validation, not mathematical independence. Three
whole cases, 0,24,25, totaling 100,665 four-tail choices, agree entrywise
with the Python implementation. Mathematical independence here comes
from the literal reconstruction, unused-triple covering algorithm and
pivoted maximal-clique replay over the complete domain.

## Exact residual certificates and sharpness

Fix one of the 77 cores. All its words through x,y,z have already
been included, so every further word of F is a five-subset of O.
Test **all** binomial(15,5)=3003 such subsets against the 45 fixed words.
The residual domains have between 44 and 72 candidates. Their graph
joins candidates exactly when their intersection has size at most two.
Any completion of F is a clique in this complete residual graph.

[residual.json](residual.json) contains one proper coloring for each
core, with the full candidate checksum. The independent
[verify_residual.py](verify_residual.py) decodes the core by literal
triple ownership, reconstructs the candidate universe using set
intersections, reconstructs graph edges using disjoint triple sets,
and checks every color of every vertex and every edge. It imports no
solver bound or floating calculation. A clique uses at most one vertex
of each color, giving the following capacities:

| Number of colors | 17 | 18 | 19 | 20 | 21 | 22 |
|---|---:|---:|---:|---:|---:|---:|
| Number of cores | 6 | 12 | 13 | 10 | 32 | 4 |

Hence every core has at most 22 additional words and |F|<=45+22=67.
The certificate SHA256 is
`c0e000acb663736254eac5a0e2112d837ad703bd226c5baee31dbcd323d31651`.
Normal and Python -O checks give the same exact per-core record SHA256
`b4c04eb32304846365ce5a16b7e06b4b789d823eefa3b48bb8d2db4645bd8864`.

[witness67.json](witness67.json) extends the core at case 10,
four-tail index 30483 by 22 residual words. Its core SHA256 is
`efc2fcc2aa54a7d21e9d0d9bd8a51cfc89c0b4ac239dfda8465bd1634198e2bb`.
[verify_witness.py](verify_witness.py) runs without the private census:
the compact fixture contains both the 45-word core and the full code.
It verifies all 670 triples are distinct, the exact center and pair
counts, the uncovered center triple, all residual indices, and the
core/extension binding. The degree multiset is
`12^1,15^1,17^1,18^2,19^5,20^8`. The witness SHA256 is
`3a732e14d328d895d4529372f9ddf7d1fde4cf3f563eada15ae55867e94f387a`.
This proves attainment and completes the restricted maximum.

## Consequences and trust boundaries

Every F with |F|>=68 avoids the stated uncovered triple. Independently
of size, if that triple occurs then the x link has m=1 and the anchor
occupancy complement is a ten-cycle. Both conclusions follow from the
complete zero/nonzero case inventory, without another degree assumption.
They do not exclude any entire replication profile of a 71-word code.

The mathematical premise is the imported complete nineteen-star census,
with its independently audited completeness. Reused source helpers and
their exact hashes are listed in [DEPENDENCIES.json](DEPENDENCIES.json).
The earlier three-star lemma 8627 supplies implementation helpers, not
its separate mathematical bound. The preceding sharp 63 lemma 8696
supplies native protocol/engine source and context, not a premise about
this degree pattern. No symmetry restriction, heuristic search output,
numerical optimum, incomplete enumeration or guard supplies an exclusion.

All arithmetic for the mathematical predicates is exact. Native graph
sizes are at most 256, and fixed-rank indices and colors fit in ordinary
integers. Guards remain two million nodes and twenty seconds per query,
and sixty seconds per bounded case or replay interval. A guarded child
returns failure and cannot certify a negative result. The first uncolored
independent attempt reached its whole-case guard; adding a proper-color
negative bound changed the algorithm, with no resource limit increase.

The [validation record](VALIDATION.json) gives actual complete stage
coverage. Both native algorithms pass all 1024 five-vertex graphs at
ranks 1 through 5, additional complete-graph ranks including 11, bitset
boundary labels through 255, and malformed/guard controls. Literal
capacity and witness corruption controls reject damaged evidence.
ASan/UBSan builds replay the actual positive witness fiber for both
engines. That bounded sanitized coverage is not full sanitized replay.
All CPU-intensive work is sequential with one thread. Bulky query
carriers, logs, binaries and exploration remain private; the cold source
regenerates them.

The established 69-word lower bound is
[Aw--Chee--Ling2003](https://ymchee66.github.io/home/PDF/6cwc.pdf),
Theorem 1/Appendix A. The maintained
[Brouwer table](https://aeb.win.tue.nl/codes/Andw.html) reports 69--72;
the campaign's independently checked upper 71 is separate prior work.
The known 69 fixture is validation and prior art, not a new construction.
The new theorem's independent peer review and historical priority remain
open. Reproduction commands and omitted-data boundaries are in the
[README](README.md).
