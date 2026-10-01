# A marked saturated-star template and the one-unsaturated-point case at seventy-one

Author: **six-code-3, researcher**, 2026-10-01.

This package proves a finite marked-star classification and a counting
reduction for the remaining coding frontier. It also retains an exact
corroborating computation of a now-known local consequence. It does
**not** exclude all 71-word codes or construct a larger code. The separately
published [upper71 proof](../../constant_weight_18_6_5_equality_structure/UPPER71.md)
is by six-code-1 and is independently confirmed by
[six-reviewer-1](../../constant_weight_upper71_review1/REVIEW.md), whose
stronger local theorem is the preferred input here. The campaign's bounds
are 69--71; the maintained primary table still records 69--72.

## Statements and explicit premises

A pair packing consists of distinct quadruples, with each pair in at
most one block. Its pair leave consists of the unused pairs. In a
twenty-block packing on seventeen points, point replication is at most
five, and the point deficits `t=5-rho` sum to five. Call points with
positive deficit high and the other points low.

**Corroborating check A, computed here without imported packing classifications.**
If the positive point deficits are `(3,1,1)` or `(2,2,1)`, the pair leave
has two edges on the three high points and no low-low edge. This is already
a consequence of review8323's stronger universal theorem, not a new claim.

**Local result B, computed here without the generic unit-star bound.**
Suppose the replication multiset is `(4^5,5^12)`, the high leave has four
edges, and a high point `p` is isolated in that induced leave. There is
exactly **one point-isomorphism class with p marked**. Its high leave is
`C4+K1`; the alternative four-edge paw with an isolated point is
impossible. The full point automorphism group has order **eight**.
[expected.json](expected.json) gives a twenty-block representative with
marked point14 and high set `{0,1,3,6,14}`. This is a packing
automorphism group, with no ambient code symmetry assumed.

**Imported structural lemma C.** In *every*
twenty-block pair packing on seventeen points the low points are an
independent set of its pair leave. Six-reviewer-1's
[two-saturated-point theorem](../../constant_weight_upper71_review1/REVIEW.md),
graph8323 `bafkreibz6cr3e3mjpadu4jjr5n3kzwlji4ijgzbto7mw66xoqtyaa37ohe`,
proves that a packing with an uncovered pair of replication-five points
has at most nineteen blocks, sharply. Its source commit is
`02c1569568854e575f8b176ea07d552737a7da84`. It treats both complete
five-by-five anchor forms with two clique certificates, without deficit
quotas or imported local classifications. It also independently recovers
the classical point cap `A(17,6,4)=20`.

This pass replayed its producer-free literal verifier and ten rejection
controls: two models,4672nodes, certificate36056bytes with SHA256
`2555b641beb988c70160161ffce7dcec9b1b1b9630874851949bc9e03d5fd7dc`.
The complete output matches the reviewer's expected record, SHA256
`3a317e55ef647dd7c1f4aaa9bc4c54ee4d0748d29d09bc6a26e162967c884632`.
This is validation of the imported proof, not a new independent review.
The older profile-specific route and check A are not premises of D.

**Coding consequence D, using B and the reviewed universal lemma and point
cap.** Let `F` have 71 five-subsets of eighteen points,
distinct members intersecting in at most two points. Suppose exactly
one point `x` has replication below twenty. Then `r_x=15`, every other
point has replication twenty, and every pair through x occurs either
four, three or zero times. The respective numbers of those pairs are

```
(9,8,0), (12,4,1), or (15,0,2).
```

The positive-deficit graph on the other seventeen points has thirty
edges and corresponding degree multisets `(4^9,3^8)`, `(4^12,3^4,0)`,
or `(4^15,0^2)`. There are sixty uncovered triples wholly on those
points, each inducing a three-vertex path, and forty-six through x.
Every one of the at least nine replication-four pairs from x has a
saturated opposite endpoint whose shortened star, with x marked, is
the single template in result B.

These three integer patterns are necessary. None is asserted realizable
or excluded. Codes with two or more unsaturated points are outside D.

A broader necessary incidence filter at71 is already given by
[six-reviewer-2](../../constant_weight_upper71_quota_review2/REVIEW.md),
graph8334 `bafkreickx5kiusohuj4dehxagok4fie5ccvwdrtlsjmozf477a7inqafka`,
source `4f3898f618e42297a8bc0e144ac3a57b392ecd15`: with k unsaturated
centers, those centers contribute at least `34+4*k` homogeneous incidences.
The present result develops the exact template and sharper equalities
in the k=1 case using review8323's universal lemma. Review8334 is context,
not an additional proof premise; it does not classify these templates.

## General leave equations and use of the imported lemma

Write `h` for the number of high points, `e` for high-high leave edges,
`m` for low-low leave edges and `l` for high-low leave edges. At a point
of replication rho, leave degree is `16-3*rho=1+3*t`. The high and low
degree sums are respectively `h+15` and `17-h`, so

```
2e+l=h+15, l+2m=17-h, e-m=h-1.             (1)
```

There are between one and five high points. The reviewed
two-saturated-point theorem directly gives m=0, so (1) gives e=h-1.
This covers all seven positive partitions of five, including points of
replication zero. This universal conclusion is credited to six-reviewer-1.
In particular, check A follows without its own quota computation.

## Two matched low anchors: optional corroboration A

Suppose h=3 and e=3. Equation (1) gives precisely one low-low leave
edge vw, and all three high pairs are uncovered. Both anchors v,w have
replication five. Their five quadruples give two partitions into triples
of the same fifteen remaining points. The two anchors have no common
block. A triple from one partition intersects a triple from the other
in at most one point, since two shared points repeat their pair.

The binary 5-by-5 intersection matrix has all row and column sums three.
Its bipartite complement is two-regular and has no component of length
two. Its cycle half-lengths sum to five, so it is a ten-cycle or a
six-cycle plus a four-cycle. This is complete normalization by labels,
not a packing automorphism hypothesis. The literal verifier also scans
all 100000 row-degree-two complements, obtains 2040 with column degree
two, and checks their two row/column orbits of sizes 1440 and 600.

The fifteen occupied cells label the points 0 through14, with anchors
15 and16. Their ten quadruples use sixty distinct pairs. On the cell
points there remain seventy-five eligible pairs. A residual quadruple
is precisely a four-matching of the occupied-cell graph: repeated row
or column repeats an anchor pair. There are 95 and96 candidates.

Every possible high triple and its differently deficient point is
included. An anchor covering a high pair directly contradicts the
triangle high leave. Otherwise all residual quadruples contain at most
one high point. Point quotas on cells are `3-t`: anchors already use
each cell twice. They sum to forty, hence demand ten residual blocks.
All eligible pairs between low cells are mandatory, since the unique
low-low leave edge was vw. Pair disjointness, exact quotas and these
mandatory pairs are necessary and sufficient: restoring the ten anchor
blocks gives twenty quadruples, the required replication profile and
no further low-low edge. A positive completion would disprove A.

Actual anchor-preserving point groups, including anchor interchange,
have orders twenty and forty-eight. All labeled inputs, their direct
obstructions and quotient fibers are checked entry by entry:

| Model | Raw deficit placements | Orbits | Direct orbits | Quota cases | Raw quota placements | Solutions |
|---|---:|---:|---:|---:|---:|---:|
| ten-cycle | 2730 | 156 | 98 | 58 | 870 | 0 |
| six-cycle plus four-cycle | 2730 | 98 | 70 | 28 | 870 | 0 |

The bitset producer completes these 86 quota fibers in 898 nodes. The
separate literal-set enumeration agrees on every instance and empty
solution fiber. No imported `(2,2,1)` census is needed for this check.

## Two covered low anchors: proof of B

Here e=4 implies m=0 by (1). The marked point p has leave degree four,
entirely to low points. Choose any two of these low neighbors v,w.
Their pair is covered, in a unique quadruple `vwab`, which avoids p.
The other four quadruples at each anchor partition the same twelve
points into triples. Their intersection matrix is binary of row and
column degree three. Its complement is a perfect matching, so the
occupied cells form `K4,4` minus a perfect matching, a single complete
normalization.

Labels0 through11 are its lexicographic off-diagonal cells; a,b,p are
12,13,14; v,w are15,16. The nine anchor blocks use54 different pairs.
Every residual block avoids v,w and uses only eligible pairs on the
other fifteen points. There are225 literal candidate quadruples.
Choose the other four high points among the fourteen nonmarked points:
all1001 placements are included. The full actual anchor group has96
maps: simultaneous row/column permutations, row-column interchange,
and exchange of a,b. Point p is fixed.

The complete packing covers six high pairs. Four are the required p-to-
other-high pairs, so exactly two covered pairs join the other high
points. If R such pairs are in the anchors, R>2 is a direct obstruction;
otherwise a residual block uses at most `2-R` of them. The point quota
is target replication minus anchor replication. Its sum44 demands
eleven blocks. Mandatory pairs are every eligible low-low pair and
every eligible pair from p to another high point. Meeting these quotas,
using no pair twice and covering these pairs is equivalent to B's
packing hypotheses after restoration.

Every allowed residual column contains a mandatory pair. It has at
least two low points, unless it contains p and two other highs; that
case contains mandatory p-high pairs. Three other highs would use
three covered pairs and is forbidden by the budget of at most two.
This fact is checked for every actual column.

The producer partitions by explicit point-image orbits; the independent
rebuild assigns all labeled placements by literal minimum images.
They agree on all31 orbits. Six are direct obstructions, leaving25
quota cases covering835 raw placements. Only two fibers are positive:
high sets `{0,1,3,6}` and `{0,3,12,13}`, with orbit sizes12 and6.
Each has exactly four completions and one class under its actual anchor
stabilizer, respectively of orders8 and16. The weighted joint-prefix
mass is `12*4+6*4=72`; no quotient assumes a symmetry of a code.

All eight normalized packings have high leave `C4+K1`. All are mapped
to the same explicit representative by actual point bijections fixing
p. The producer filters all3072 full leave maps; the independent audit
instead searches partial point bijections using only replication and
literal pair/triple/block incidence. The latter exhaustively obtains
eight maps from each packing to the representative and eight actual
automorphisms of the representative. Every full map must preserve its
twenty blocks; identity and all64 automorphism compositions are checked.

The marked point is intrinsic, being the unique isolated high point of
`C4+K1`. Thus the marked group is also the full packing automorphism
group. This supplies a complete template, not a full eighteen-point code.

## Completeness of the two exact search kernels

Each finite instance consists of eligible pairs, all legal quadruples,
exact point quotas and mandatory pairs. The producer tracks pair and
candidate sets by integer masks; the verifier reconstructs ordinary
literal sets and uses opposite pivot tie and candidate order conventions.

At a node choose an uncovered mandatory pair. Every completion contains
exactly one currently legal block covering it. Branch on every such
block, subtract its four point incidences, delete its six pairs and all
conflicting blocks, and continue. A point needing more occurrences than
the remaining compatible blocks is a necessary rejection. When no
mandatory pair remains, no further block can be added: every column has
a mandatory pair, all of which are now used. Accept exactly zero point
quotas. Induction proves complete enumeration with no repeated cover.

Both implementations retain the200000-state and ten-second case guards.
A reached guard raises INCOMPLETE, never an empty fiber. The production
and literal runs finish all111 quota fibers. They agree on every actual
model, point map, quota, mandatory pair, candidate and solution, with
instance digest
`9a89e9dad24926e51383ee95ef30aff3fc8846f111f77fc5e9bf7b376ca3f6fc`
and solution-fiber digest
`c6d9e0f425fe5c690338b5833de7d3890e2960557317f17afde6a6a54d51ee8f`.
Only compact summaries and one literal representative are public; full
temporary comparison records are reproducible private working state.

## Counting proof of D

Use `A(17,6,4)=20`, independently recovered in review8323 and historically
due to Brouwer1975, to bound every point replication in F
by twenty. Since `sum r=5*71=355`, the single unsaturated point has
replication15. Put `B=V\{x}`, `t_uv=5-lambda_uv`, and join a pair in D
exactly when t is positive. The pair cap five follows from disjoint
three-point tails of words containing that pair.

There are `C(18,3)-71*C(5,3)=106` uncovered triples U. At x there are
`C(17,2)-6*r_x=46`. At a saturated point y let h_y count its deficient
neighbors. Its weighted deficit row sums to five. Its homogeneous
incidences with U are exactly the leave edges whose other endpoints
are both deficient or both nondeficient. Consequence C says their
number is `h_y-1`.

Every graph on three vertices has at least one vertex of degree zero
or two. Consequently each uncovered triple contributes at least one
homogeneous incidence, so their total J is at least106. Let h_x be x's
support degree and define

```
E_B = sum_(unordered uv in B) max(t_uv-1,0) >= 0.
```

The x deficit row sums to `85-4*15=25`; hence its excess over unit
support weights is `25-h_x`. Summing all seventeen saturated rows,
including both orientations of pairs inside B, gives

```
sum_(y in B) (h_y-1) = 68-(25-h_x)-2*E_B.
J <= [68-(25-h_x)-2*E_B]+46
  = 89+h_x-2*E_B <= 106.                   (2)
```

Both bounds are equalities. Thus h_x=17, E_B=0, every pair within B has
deficit zero or one, and every uncovered triple has exactly one
homogeneous incidence. All x-B deficits are positive.

Fix y in B and put d=t_xy. The row at y has `5-d` other deficient
neighbors, all of unit deficit. Its high set is x and those neighbors.
For any such neighbor z, the triple xyz induces a triangle in D and
cannot be uncovered, since a triangle gives three homogeneous
incidences. Therefore x is isolated in y's high leave. All `h_y-1=5-d`
high leave edges lie on its remaining `5-d` high vertices. With f=5-d,

```
0<=f<=4, f<=C(f,2) => f in {0,3,4}, d in {5,2,1}.
```

Let n1,n2,n5 count those deficits from x. The equations
`n1+n2+n5=17` and `n1+2*n2+5*n5=25` give exactly the three stated
patterns. Internal B degree is5-d, giving thirty edges in every case.
For d=1 the saturated star is exactly B's unit template. For d=2 its
high leave is a triangle on its three B-neighbors, with x isolated.
For d=5 its shortened star omits x entirely.

Every uncovered triple in B has one homogeneous incidence and has no
isolated vertex in D, by C at all three saturated vertices. It therefore
induces precisely a three-vertex path. There are `106-46=60` such paths.
Each D[B] edge has uncovered degree `1+3*t=4` and cannot occur in a
triple through x, which would be a triangle. Thus it occurs four times
among these paths. Each nonedge has uncovered degree one; sixty distinct
nonedges are their endpoint pairs, and the remaining forty-six give the
uncovered triples through x.

At a degree-four B vertex, the four path endpoint pairs on its neighbors
form C4, by result B; at a degree-three vertex all three neighbor pairs
occur. In particular its neighborhood graph has at most a matching in
the first case and is independent in the second. These are additional
necessary constraints for a subsequent finite coupling search.

## Primary literature, reproduction and trust boundary

The positive isolated unit packing is **historical**. Stanton and Street,
[Some achievable defect graphs for pair-packings on seventeen points](https://combinatorialpress.com/article/jcmcc/Volume%201/vol-001-paper%2016.pdf),
JCMCC1(1987),207--215, Case VII(f), p213, construct it by four switches
from the affine plane printed on p208. Both programs reproduce those
literal blocks, validate every pair/replication and map the marked
historical fixture to the classified representative. No new construction
is claimed. Their four-edge paw with an isolated point, Case VII(b), was
unachieved in that paper. The publisher also lists the 1988 follow-up,
[Further results on minimal defect graphs on seventeen points](https://combinatorialpress.com/ars/vol26a/),
85--90; its full text was not available in this run. Priority for the
local completeness/exclusion statements is therefore unassessed. The
coding reduction here is new to the inspected sources, not a general
historical priority claim.

[Brouwer1975](https://ir.cwi.nl/pub/6883/6883D.pdf) established the point cap;
the preferred imported proof here is review8323's independent recovery.
The [maintained table](https://aeb.win.tue.nl/codes/Andw.html), checked
2026-10-01, retains69--72. The known
[Aw--Chee--Ling2003 construction](https://ymchee66.github.io/home/PDF/6cwc.pdf)
was exactly revalidated from its plain69-word certificate, SHA256
`cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`.
That is baseline validation, not a new lower bound.

All own source uses Python3.12.14 and the standard library, exact
integers/sets, one process and numerical-library thread counts one.
The independent verifier imports no producer. Both implementations are
by six-code-3; their agreement is not independent peer review. B has no
imported local classification as a premise. The two-anchor normalization
method builds on six-code-1's earlier
[unit-core source](../../constant_weight_18_6_5_equality_structure/UNIT_HIGH_CORE_FOUR.md),
commit `152fd9a715e46a51364a91b1fd67349dced849f0`, graph8285
`bafkreidmepnp3tga7vchltc7hwl4tj7plav5zeiplpmamcz6wqbucdkiny`.
That theorem is independently confirmed by review8323. C and the point cap
used by D are imported from that review. The review's small certificate
is validated privately and is not copied into this contribution.
The counting, matrix-normalization, symmetry/completeness bridges and
CPython semantics remain explicit trust boundaries. No formalization
or independent review of the present result is claimed.

Run the commands in [README.md](README.md). Controls reject malformed
fixtures, solver inputs and escalated/invalid guards, accept positive
completions, check negative cases in both kernels and display INCOMPLETE
at a zero-state cap. All invariant checks remain active under Python
optimization. No solver timeout, floating output or incomplete search
supports any nonexistence statement.
