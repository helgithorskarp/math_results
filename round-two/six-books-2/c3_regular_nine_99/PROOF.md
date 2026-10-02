# No nine-regular Book Ramsey host with cycle type 3^7 1

Actual author **six-books-2**, role **researcher**, 2026-10-02.
The campaign shares one signing identity; that is not independent authorship.

Call a simple red graph G on22 vertices **valid** if every red edge has at
most3 common red neighbors and every blue complement-edge has at most6
common blue neighbors. These are ordinary books; page-to-page edges are
irrelevant.

**Theorem.** No valid nine-regular red graph on22 vertices has an
automorphism consisting of seven three-cycles and one fixed vertex.

Nine-regularity means EVERY red degree is9, so the graph would have99 red
edges. The theorem covers this entire automorphism/regularity cohort,
without choosing a Kneser seed, an edit budget, a boundary parent or a
special induced root graph. It does not exclude irregular99-edge hosts,
102-edge hosts, other cycle types or arbitrary22-point colorings. It does
not determine R(B4,B7).

This is an author-checked exact computational lemma. Distinct algorithms
are by the same author; ordinary completeness/relabeling/code bridges
below are unformalized. Independent peer review is pending.

## 1. The exact regular root cut

Let x be the fixed vertex, A=N_R(x), and B=N_B(x). Regularity gives
|A|=9 and |B|=12. Both blocks are unions of free three-cycles: three in A
and four in B. Label a free orbit by (i,t), t modulo3, so the automorphism
adds1 to t. No orientations or additional automorphisms are assumed.

Put H=G[A], K=G[B], h_a=d_H(a). The red spine xa has h_a red pages, so
h_a<=3. Every a has8-h_a red B neighbors. The blue spine xb has exactly
11-d_K(b) blue pages in B, with none in A, so d_K(b)>=5. Therefore b has
at most4 red A neighbors. The red cut c=e(A,B) satisfies

    45 <= c = 72-2e(H) <= 48.

Every edge orbit in H has size3, so e(H) is divisible by3; equivalently
c is divisible by6. The only possibility is

    c=48, e(H)=12, d_K(b)=5, |N_R(b) intersect A|=4 for EVERY b.

The three constant orbit degrees of H sum to8 and each is at most3.
They are consequently (2,3,3), up to orbit ordering. Normalize the unique
degree-two orbit to i=0. The three per-vertex red B margins are(6,5,5).
In particular e(K)=30 and the total is9+12+48+30=99. This reduction uses
only the stated regularity, automorphism and book caps; no global degree
or edge-floor theorem is a premise.

## 2. Every possible A graph and necessary incidence cuts

There are twelve free H edge orbits: three internal triangles, and for
each i<j three matchings joining(i,t) to(j,t+s), s=0,1,2. Word bits0,1,2
are the internal triangles; bits3..5,6..8,9..11 are the respective01,02,12
cross masks. All oriented masks remain free. Exactly four edge orbits
are red since e(H)=12, giving binomial(12,4)=495 words.

For a in A put S_a=N_R(a) intersect B and s_a=8-h_a. For an A-pair u,v,
let c_H(u,v)=|N_H(u) intersect N_H(v)|. If uv is red, its root page x
and H pages give

    |S_u intersect S_v| <= 2-c_H(u,v).

If uv is blue, the common blue pages inside A number
7-h_u-h_v+c_H(u,v), and the B pages number
12-s_u-s_v+|S_u intersect S_v|. The root is red to both endpoints.
The blue cap thus gives

    |S_u intersect S_v| <= 3-c_H(u,v).

Denote the appropriate bound by lambda_uv. It must also be at least
max(0,s_u+s_v-12), the elementary intersection lower bound.

For ANY subset T of A let S=sum_(u in T) s_u=12q+r, 0<=r<12. If l_b
counts the red T neighbors of column b, then

    sum_(u<v in T) |S_u intersect S_v| = sum_(b in B) binomial(l_b,2)
                                      >= 12*binomial(q,2)+r*q.

Moving one unit from a load at least two larger than another decreases
the pair sum, so the last expression is its minimum at balanced loads.
Therefore sum_(u<v in T) lambda_uv must be at least this lower bound.
We impose every pair test and every subset test for |T|=3..9. The
independent checker instead computes the minimum by a finite dynamic
program over twelve labeled loads in{0,...,|T|}. These are necessary
cuts, not a sufficient construction test.

The allowed A relabelings permute its three cycles, translate their
phases independently, and multiply ALL phases by the COMMON multiplier
1 or2. A relabeling with multiplier2 extends to B by that same multiplier;
independently reversing some cycles is not allowed. All these maps
extend to whole-host relabelings. A-permutations move its unique local
degree-two orbit to0; this is a local mark, not a global degree mark.

`projection.py` chooses all495 four-orbit words, obtains174 degree
matches,174 pair matches and108 subset survivors, and canonizes each.
`audit.py` independently constructs ALL4096 words by a literal pair
predicate, uses the load DP, and then expands each representative's
entire relabeling orbit. The entire surviving word sets and relabeling
groups agree, with representatives

| H word | Labeled H words in its declared relabeling orbit |
| --- | ---: |
| 78 | 27 |
| 540 | 54 |
| 1616 | 27 |
| total | 108 |

These are representatives under the stated group; no claim about full
unmarked graph isomorphism classes is needed.

## 3. Complete A-to-B incidence coverage

A B-vertex has exactly four red neighbors in A. There are126 possible
four-subsets. In one B triple, the three columns are simultaneous
phase-translates of the first. No four-subset is fixed by a simultaneous
three-cycle, because a fixed set would have size divisible by3.
Thus there are42 column-triple types. Relabeling the B triple can select
the least integer column mask among its three translates. Each such
phase relabeling also relabels the unknown K; its entire word domain
remains available.

All four B orbits have the same global degree9 and K degree5. Permuting
them is permitted. Enumerate every nondecreasing multiset of four types:
binomial(45,4)=148,995 per H representative. Require the exact(6,5,5)
row margins and every A-pair intersection bound. `incidences.py` traverses
these complete multisets. Independently `audit.py` joins two ordered
pairs of column types with complementary row margins and the boundary
condition that the second left type is at most the first right type.
Every nondecreasing four-tuple has one such split. Both recover the
ENTIRE incidence sets, with all typed primary column/row/intersection
fields rebound to the independent literal definition.

| H word | Multisets | Row-margin matches | Entire surviving incidences |
| --- | ---: | ---: | ---: |
| 78 | 148,995 | 10,387 | 6 |
| 540 | 148,995 | 10,387 | 13 |
| 1616 | 148,995 | 10,387 | 18 |
| total | 446,985 | 31,161 | 37 |

The checker orders the actual integer column masks; the producer's
type-index order can differ. They compare the complete four-column
multisets after this permitted B-orbit reordering. `frames.txt` is
regenerated, not an external catalogue input. Its entire37-frame SHA256 is
`6c60d1377a19bc7a06a7da0e8aaf3f7f13399d49ab44ab3411794d86d1601f56`.
The full compact typed frames also appear in `EXPECTED.json`.

## 4. Every outside graph and completion

An invariant K has four internal triangle bits and six cross masks:
22 edge-orbit bits in total. It is five-regular. Its red spines have
at most3 pages inside K. On a blue K spine, x supplies one blue page;
the two endpoints each have FIVE blue A neighbors among nine points,
so there is at least one common blue A neighbor. Thus a blue K spine
has at most4 common blue neighbors inside K. These are necessary
outside-graph screens.

`block.py` enumerates the16 internal assignments and all4^6 cross-mask
weight tuples, then expands EVERY mask of each selected weight. There
are65,536 weight frames,116 degree-matching frames and16,536 actual
five-regular K words. The local caps retain15,768 words. Independently
`direct.cpp` traverses EVERY one of the2^22=4,194,304 K words, computes
its degrees and literal K page counts, and recovers the SAME entire
sorted15,768-word list, not merely its count or checksum. Its SHA256 is
`b55ea7aec99edb7b23aeb97d7883d038f633d31f3ac20a42a53f4746d8e9fce6`.

For each of the37 regenerated incidence frames, EVERY K candidate is
tested:37*15,768=583,416 completion choices. `block.py` counts the known
A pages and unknown K pages separately on B-B and mixed A-B spines.
On blue B-B spines it adds the common root page; on mixed spines the
root contributes none. A-A and root caps have already been checked
exactly or forced by the degrees above.

`direct.cpp` independently reconstructs every full22-point adjacency
matrix and applies the literal red/common-blue predicate. A failed
colored cap may stop at its first violating spine; we do not claim
every physical spine was executed on every rejected graph. Its
406,025 red-first and177,391 blue-first rejections sum to583,416.
Both algorithms return ZERO valid completions. Their complete
one-byte-per-choice outcome streams agree entrywise; SHA256
`c7c2254c70b4a6737240dec0b18fa3849888c882dc44570e9b88b4fda24a14c2`.

Every hypothetical graph under the theorem normalizes to one of the
three H representatives, one of its37 total incidence templates and
one of the15,768 K words. No positive completion exists. This proves
the theorem. The count is completion choices, not distinct hosts or
isomorphism classes; repeated coverage is harmless to the exclusion.

## 5. Reproduction and trust boundaries

[README.md](README.md) gives the cold and validation commands. The
programs use exact integers, Boolean graphs and standard libraries:
CPython3.11.2 and g++12.2.0/C++17. Native adjacency masks use unsigned
32-bit integers, with only22 vertex bits or22 orbit bits. Shift counts
are at most22; graph/count bounds are below2^64. No floating point,
solver, external graph catalogue or timeout is a mathematical premise.

`EXPECTED.json` was frozen before the standalone cold run. Its SHA256,
also the whole typed mathematical-summary SHA256 in normal and
optimized Python, is
`f79fab2dec8d86ed6731e7177aaa73475595a0781787f10e27238fa9cfccb32d`.
The complete normal/optimized replays took7.018/7.706 seconds, with
largest recorded child119,984KiB. Whole ASan/UBSan native enumeration
replays all4,194,304 K words and583,416 completion choices; every
semantic native field and both complete streams agree with release.
Its program time was1.414 seconds; validation wall10.820 seconds,
largest recorded child230,244KiB, including compilation. Seventeen
native/projection/typed-fixture damages reject. Literal set/bitset/block
counts agree on all14,784 colored spines of64 varied controls, with
positive/negative graph threshold calibrations and the primary21 fixture.

All work is serial, threads1, within the unchanged1CPU2GiB scope and
fixed25-second program/30-second child guards. An earlier Python
whole-graph-rebuild prototype reached its25-second soft guard before
finishing; that incomplete run proves nothing. Its completed candidate
list was preserved. The final component and separate native algorithms
finish the WHOLE domain under unchanged limits. No resource settings
were increased. Checksums are regression evidence, not standalone
proofs. Correctness trusts the programs/toolchains and the written
coverage, normalization and code-decoding argument. Same-author
algorithmic independence is not independent peer review.

The root/subset/phase-incidence method builds on this author's
[105-edge C3 packet, lemma8971](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/c3_free_seven_105/PROOF.md).
The new result is the complete99-edge all-degree9 cohort, not a replay
of that105-edge theorem. The older conditional theorem or its imported
global degree bounds are NOT mathematical premises here. The earlier
[boundary-repair lemma9392](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/kg_c3_boundary_repair_barrier/PROOF.md)
covers monotone descendants of Kneser boundary parents; the present
cohort is specified without any seed or parent and needs no premise
from that packet.

The [primary paper, Table1](https://arxiv.org/pdf/2407.07285), reopened
live2026-10-02, still gives22<=R(B4,B7)<=23. The known
[primary21 matrix](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
is reproduced exactly:93 red edges, red page maximum3, blue maximum6.
Raw1 denotes BLUE; the packaged binary rows are its off-diagonal red
complement, with SHA256
`4f1dd2bc743590a0553107936656e469db6e7d742db0456d697353ce50aac5ec`.
This is credited baseline validation. The upper23 flag certificate was
not independently replayed. No exclusive historical-priority claim,
full99/C3 exclusion or Ramsey endpoint is asserted.
