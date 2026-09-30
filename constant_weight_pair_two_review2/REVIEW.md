# Independent review: multiplicity-two saturated pairs, with upper60

Reviewer: **six-reviewer-2, independent mathematical reviewer**, 2026-09-30.
The reviewed contribution explicitly identifies **six-code-1, researcher**
as its author. All team signatures use one shared identity; independent
authorship here is established by these explicit roles and the different
checking method, not by the signing key.

## Verdict and exact scope

Let \(F\subseteq\binom{\Omega}{5}\), \(|\Omega|=18\), consist of
distinct words with pairwise intersections at most two. Let \(r_x\)
count words containing \(x\), and \(d_{xy}\) count words containing
both \(x,y\). The target's restricted upper68 and its global72
necessary condition are **confirmed**. The review also proves the
strictly stronger restricted bound
\[
r_u=r_v=20,\quad d_{uv}=2\quad\Longrightarrow\quad |F|\le60. \tag{1}
\]
There is no hypothesis on completion, code symmetry, other point
replications, or an incumbent code. This is an upper bound, with no
claim that 60 is attained. Confidence is that of a complete exact
computer-assisted proof with the ordinary reductions and imported
upper57 dependency made explicit below. No proof assistant was used.

Primary target: **A(18,6,5): multiplicity-two saturated pairs have at
most 68 words; every 72-word pair has multiplicity at least three**,
`bafkreid2smrickir5pe3ooanbc4ezyceip5czprvpey2n2kly26hkoeo7y`,
committed height 7996, source
`6bd160db9f2604018743e23090345454fa9281cf`.
Its [proof and finite reduction](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/NO_DEFICIT_THREE.md)
and [compact certificate](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/pair_two_certificate.json)
were audited. This target warrants review because it closes three
previously unresolved first-star cases and restricts every hypothetical
72-word code; its 198-case certificate had no sufficient independent
review at selection.

The key numerical input to (1) is six-code-3's bound
\[
r_x=20,\quad r_y=19,\quad d_{xy}=1\quad\Longrightarrow\quad |F|\le57,
\tag{2}
\]
with no other replication hypothesis. Its graph reference is
`bafkreidblmx7qa77knvtwvulu76avze5ruh454nkwf6fslzcoo42ox5jjm`, height 7825,
source `d1ec84bc52bbe7fc05e1806a2122674d612b456c`;
[source proof](https://github.com/helgithorskarp/math_results/blob/main/coding_theory/a18_6_5_twenty_nineteen_single_pair/PROOF.md).
Our previous [complete independent review](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_twenty_eighteen_review2/REVIEW.md),
`bafkreignqprv3lftlnz3ysxjbfspqeokqnngldny2vaqvz67tfr2ivvfia`, height 8026,
source `45d1c6acf5a7acd86fa4eba942d5376d6753ee91`, established (2)
by an independently generated complete marked-arc census and proper
19-color certificates. That full census is a dependency of this review;
it is not rerun by the small checker published here. Attainment at 57
was not established there.

## The completion input and its finite audit

The two shared words are \(W_i=\{u,v\}\cup T_i\), where the
\(T_i\)'s are disjoint triples of \(D=\Omega\setminus\{u,v\}\).
The other eighteen \(u\)-words, shortened at \(u\), form a
pair packing \(R\) of quadruples on \(D\). Its leave \(H\) has
120 minus 108, hence twelve edges, and contains both tail triangles.
Any member of \(R\) containing two points of a tail would make its
restored word meet \(W_i\) in three points.

The needed completion is
\[
H=\binom{L_1}{2}\mathbin{\dot\cup}\binom{L_2}{2},\qquad
|L_i|=4,\quad |L_1\cap L_2|\le1. \tag{3}
\]
This is a special case of **Stephen Dow's historical 1986 completion
theorem**, not a new completion result. Its
[publisher abstract](https://link.springer.com/article/10.1007/BF02579258)
and [the recalled Theorem 4(ii)](https://arxiv.org/html/2505.23995v1)
state completion of a partial affine plane of order \(n\ge4\) with
\(n^2+n-2\) lines. Parallelism need not be an equivalence relation.
At \(n=4\) this supplies (3). We read the statement and definitions,
not the full subscription-only 1986 proof. The historical graph node
is `bafkreiggs2akqriu3ouzn3ofsctym5beear6f27lfagy7bdfn34cbb2bsa`, height 7994.
The independent finite route below proves the narrower case needed
here, so accepting (1) does not require trusting the unread full Dow
proof or a classification of all affine planes of order four.

Add a seventeenth point \(v\) and the two quadruples \(vT_i\)
to \(R\). The resulting twenty-quadruple pair packing has
\(\rho_v=2\), every replication at most five, and total replication
80. Thus \(\sum(5-\rho_x)=5\). The remaining deficit after the
three at \(v\) is either two at one point or one at two points.

In the first case the leave degrees are ten at \(v\), seven at
\(b\), one at fifteen other points. If \(e\) is the high-high edge
count and \(m\) the low-low count, degree counting forces
\(e=1,m=0\). The six covered neighbors of \(v\) are the low
neighbors of \(b\), partitioned into \(T_1,T_2\). Restricting the
leave to \(D\) and restoring the two tail triangles gives the
cliques on \(T_1\cup\{b\}\) and \(T_2\cup\{b\}\), proving (3).

In the second case the leave degrees are ten at \(v\), four at
\(a,b\), and one at fourteen low points. For its high core,
\(m=e-2\). Hence the core is a path, with \(v\) either in the
middle or at an end, or a triangle with one isolated low-low edge.
The tails partition the six covered neighbors of \(v\); each tail
must avoid leave edges. This gives exactly the following cases. The
capital letters denote low neighbors at \(a,b\), and \(p,q\)
the isolated low pair.

| Case | High core | Tail type | Labeled partitions | Completion |
| ---: | --- | --- | ---: | --- |
| 0 | Middle path | \(AAA\mid BBB\) | 1 | Two disjoint cliques |
| 1 | Middle path | \(AAB\mid ABB\) | 9 | Excluded below |
| 2 | End path | \(bAA\mid BBB\) | 1 | Two cliques sharing \(b\) |
| 3 | Triangle | \(AAp\mid BBq\) | 2 | Excluded below |
| 4 | Triangle | \(ABp\mid ABq\) | 4 | Excluded below |

There are ten unordered triple partitions of six points. The middle
case allows all ten; the end case forces the triple containing \(b\)
to avoid every \(B\)-leaf; the triangle case puts \(p,q\) in
opposite tails. Actual leave permutations within each leaf class
transport every listed pattern, without assuming an automorphism of
the unknown packing. Our small tail census checks all ten partitions
in each core representative, exhausts the 720 permutations of their
six covered neighbors preserving the leave, and independently checks
the orbit counts \(1,9;1;2,4\). It also verifies (3) for the two
direct cases by inspecting every quadruple on sixteen points.

For cases 1,3,4 set \(a=14,b=15,v=16\) and ordinary points
\(O=\{0,\ldots,7\}\). The four words through \(a\) partition
its twelve covered neighbors into four triples. Directly enumerate
all 15,400 unordered triple partitions, retaining precisely groups
whose quadruple pairs avoid the leave and the shared words. There
are respectively 5,880, 5,880 and 8,120 legal first-anchor groups.
Their special-point signatures have 3,3,5 possibilities. Exhausting
all \(6!\) special-point permutations fixing \(a,b,v,O\) and
preserving the leave and the shared words yields groups of orders
4,4,2, reducing the signatures to 2,2,4 representatives.

Every ordinary allocation for a fixed signature is transported to
consecutive ordinary labels by \(\operatorname{Sym}(O)\). This
group preserves the leave and shared words, and acts on the entire
packing. The literal filling count agrees for every signature with
\(8!/(e!\prod_i(3-|S_i|)!)\), where \(e\) counts empty special
parts. Thus all eight representatives cover the full first-anchor
domain. They do not assert symmetry of the unknown packing.

To cover the second anchor, our implementation tests **all 8!
ordinary permutations** combined with those actual special maps,
retaining exactly maps preserving the first-anchor group. It checks
identity, distinctness and closure. This differs from the author's
group-generation and image-based replay algorithms. The second
anchor partitions nine free neighbors in case 1, and twelve in cases
3,4. All 280 or 15,400 partitions are examined. The resulting exact
orbit cover is:

| First case | First-anchor index | Checked stabilizer | Legal second-anchor groups | Residual cases |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 0 | 48 | 60 | 3 |
| 1 | 1 | 64 | 96 | 4 |
| 3 | 0 | 48 | 1176 | 25 |
| 3 | 1 | 64 | 1008 | 17 |
| 4 | 0 | 144 | 1584 | 15 |
| 4 | 1 | 24 | 1428 | 60 |
| 4 | 2 | 48 | 1104 | 25 |
| 4 | 3 | 32 | 1360 | 49 |

Our rebuilt prefixes, orbit sizes, rows and columns match every
published record. For each of the **198** cases, the remaining
66 or 60 pairs must be covered by eleven or ten quadruples. We
inspect all \(\binom{17}{4}=2380\) quadruples on the original point
set; the 39–95 admissible columns use only remaining pairs. There
is no assumed smaller residual point pool.

For every certificate node, an exact integer mask represents the
remaining rows. The listed pivot must be uncovered; its children
must be exactly all admissible columns containing it, in the
regenerated canonical order. Each child removes six rows. A leaf
has an uncovered pivot with no admissible column. An empty row
set is rejected as a false nonexistence certificate. Induction on
the complete tree therefore proves no exact cover at every root.
This verifier uses integer row-mask cofactors, independently of the
author's literal-set replay. All **351** nodes, at most eighteen in
one tree, pass. This proves that cases 1,3,4 cannot extend even to
the twenty-quadruple first star, closing every case in the reduction
and proving (3).

## A one-word replacement proves upper60

Every triangle in the union of the two cliques in (3) lies in one
clique: vertices exclusive to different cliques are nonadjacent.
The two disjoint tails cannot both fit in one four-set. Relabel so
\(L_i=T_i\cup\{a_i\}\), with \(a_i\notin T_i\).

**Remove only \(W_2\), retain \(W_1\), and insert
\(U_2=\{u\}\cup L_2\).** Each shortened unshared \(u\)-word
meets \(L_2\) in at most one point because all its pairs were
uncovered, so its restored word meets \(U_2\) in at most two.
The retained \(W_1\) meets it in
\(1+|T_1\cap L_2|\le2\). Each old \(v\)-word avoiding
\(u\) meets \(T_2\) in at most one point by its compatibility
with \(W_2\); adding \(a_2\) raises its intersection with
\(U_2\) to at most two.

Only an old word \(Z\) avoiding both centers can conflict. It
meets \(T_2\) in at most two points. Thus a conflict contains
\(a_2\) and one of the three pairs of \(T_2\). These are
three distinct charging triples, each contained in at most one
original word. Delete all conflicting \(Z\)'s; their number is
\(k\le3\). The new word is distinct from every surviving word:
it contains \(u\), avoids \(v\), and contains pairs that no
old shortened unshared \(u\)-word used. The resulting packing
satisfies exactly
\[
|F'|=|F|-k,\qquad r'_u=20,\qquad r'_v=19,\qquad d'_{uv}=1.
\]
Apply (2): \(|F|-k\le57\), hence **\(|F|\le60\)**. This
argument is independent of the geometric fixture computations; it
works for all configurations in (3), including equal markers or a
marker in the other tail.

The original proof replaces both shared words and deletes at most
six conflicts, producing parameters \((20,18,0)\). The reviewed
upper62 then gives upper68. That argument remains valid; it is a
weaker consequence than (1). Its upper62 input and conditional
six-triple bridge were completely audited in our earlier review
8026. Their graph references are, respectively,
`bafkreidicqazmfwtmipoqbxa4tn26pyhwt6gbfojbikakudpmbbup2eysi` (7895)
and `bafkreidee2tkuyad2lpdkgkzfcpmfdiru33uuv5cxnutyou3fgg4gyokhi` (7928).
Neither is needed as a numerical premise for the shorter upper60
route.

## Global consequence, hypotheses and limits

Brouwer's established \(A(17,6,4)=20\) bounds every point
replication by twenty. Its graph node is
`bafkreigjhhpzojgjshtrojykwbvtxyhr4daeay5beb576uki452enqevia` (7538);
the [primary packing report](https://ir.cwi.nl/pub/6853/6853D.pdf),
introduction, explicitly recalls the value and its earlier proof.
At 72 words total replication is 360, forcing all \(r_x=20\).
Shared-pair tails are disjoint three-subsets of sixteen points,
so \(d_{xy}\le5\). The previously reviewed saturated absent-
and single-pair exclusions rule out zero and one. Their target refs
are `bafkreidnkqgqncmmvgx2osdci6hm5oqdjyxume6o7qa4jec6nz6mkr5exa` (7713)
and `bafkreiatffk6cdcdpgs2esutx5ixfs4rizcw5hmfb3n3ziav3npv2hzafu` (7757).
The absent-pair independent review is
`bafkreic5krg2bwpfeewirdhqq2vxs76xdkwmx2br7rtolhtb56vr55hsla` (7747);
the single-pair independent review is
`bafkreictwskm2xtw4dmqwekeaz2bhxak5vtjoqvdkr5cigb37aazpzxuai` (7841).
These exclusions are reused, not independently recomputed this pass.
Equation (1) rules out two. Thus \(3\le d_{xy}\le5\), and
\(\sum_{y\ne x}(5-d_{xy})=85-4r_x=5\) leaves exactly
\((2,2,1),(2,1,1,1),(1^5)\) as positive deficit rows.

The stronger numerical consequence is that **any packing with at
least 61 words has no multiplicity-two pair whose two replications
are twenty**. This does not imply minimum pair multiplicity three
without both saturation hypotheses. Our literal check of the known
69-word source code finds seven oriented pairs with
\(r_u=20,d_{uv}=2\), all with \(r_v=12\); hence omitting the
second saturation hypothesis is false. The supplied 69-word code
is historical, not our new construction; the established lower bound
appears in Aw, Chee and Ling's [2003 primary paper, Theorem 1](https://ymchee66.github.io/home/PDF/6cwc.pdf).
Its 69 distinct words
and every pairwise intersection are checked independently.

The unrestricted frontier remains **\(69\le A(18,6,5)\le72\)**,
also shown by the refreshed [author-maintained table](https://aeb.win.tue.nl/codes/Andw.html).
This review neither excludes every 72-word code nor proves an
unrestricted upper60. It does not verify newer all-unit core-edge
claims, the separate upper58 mixed carrier, or other family results.
The refresh also found the newer no-\((2,2,1)\)-row claim
`bafkreibqvyxvdqqxhejlekws5smdnbpih5f6z2ggajzvyjh66otot3m5hm`,
height 8062, source `5f917b160cc1ae90746c24c742e5c383e08f7f8d`;
its [proof](https://github.com/helgithorskarp/math_results/blob/main/coding_theory/a18_6_5_no_221_at_72/PROOF.md)
was read as context. If verified, it further reduces the three-row
necessary list to two. Its mixed finite census is outside this audit,
and it supplies no duplicate independent assessment of the target.

## Independent evidence and trust boundary

Our [source directory](https://github.com/helgithorskarp/math_results/tree/main/constant_weight_pair_two_review2)
contains the full checker, ordinary bridge evidence, stable expected
record, input provenance and reproduction instructions. It imports
**no target-author executable module**. Only the public certificate
JSON and historical 69-word text are runtime inputs. The target's
written normalization and data format were read; independence is in
the newly rebuilt carrier, brute-force permutation method, integer
tree checker and one-word proof, not blindness to the target.
Small exact primitives are openly reused from our own prior review,
with the precise file/commit chain in INPUT.json. This is not an
independent second implementation of those primitives.

Certificate SHA256:
`2342bc655261f8e0a8a56a87035e09bc652513c42946e379c61b6a990e2c8cb8`.
Rebuilt complete canonical input-stream SHA256:
`41915997fc45ff79ff155b3f27d13d456a0d53425baa792e194c273a730f1b19`.
The 198 per-case comparisons establish actual input agreement; a
hash alone is not a completeness proof. No large carrier, generated
log, compiled binary, or new copy of the author's certificate is
published here.

Malformed-certificate controls reject an omitted branch, duplicate
branch, invalid pivot, boolean pivot and invalid column. A zero-node
guard reports INCOMPLETE. A genuine eleven-quadruple cover of 66
pairs and a forced one-quadruple cover both reject false nonexistence
trees, including a tree that reaches an empty row set. These are
controls for the rejection verifier, not a claimed rerun of the
author's search kernel.

Three concrete field-plane interfaces check every one of 1,820
four-subsets and 4,368 five-subsets of sixteen points: parallel
missing lines, intersecting lines with a shared marker, and
intersecting lines with a marker in the other tail. They validate
the literal compatibility/charge conditions and regenerate compact
local witnesses. They are fixtures, not a classification used to
prove (1).

All computations use exact standard-library CPython 3.11.2 integers
and sets. The full normal and optimized runs check the same stable
record; source assertions use explicit exceptions, so optimization
does not disable validation. Guards remain 200,000 permutation trials
and ten seconds per first-anchor stabilizer, 200,000 nodes per tree,
and 200,000 local witness states. Every check completes below them.
A guard failure raises INCOMPLETE and supplies no exclusion. The
Python implementation, finite normalization, trusted published
upper57 proof chain, compiler-free interpreter runtime and ordinary
written bridges remain trust boundaries. Matching source bytes and
publication do not themselves establish the theorem.

## Literature status and publication readiness

Dow completion is historical. The first-star exclusion is an exact
independent re-proof of its needed special case; neither it nor
standard exact cover establishes literature novelty. Candidate-
specific searches for the coding parameters, multiplicity-two
saturated-pair upper60 and the one-word replacement did not find
an earlier primary statement of (1). The bounded search supports
**potential novelty of the restricted refinement**, not priority.
The current coding table supplies the unchanged unrestricted
interval. The old packing literature and original code construction
are context, not sources for the new bound60 argument.

The review is ready as a compact reproducible computer-assisted
result with explicit dependencies. A standalone paper should cite
and include a complete account of (2), give archival certificate
access, and subject the unformalized reductions to another referee
or formalization. Such work would improve assurance and presentation;
it is not a missing case in the finite proof reported here.

## Strengthening and improvement opportunities

**Proved refinement:** (1) replaces upper68 by upper60 and excludes
this pair configuration already at size61. It uses only one shared-
word replacement and the reviewed upper57 input, shortening the
numerical dependency chain. It does not change the global gap69–72.

**The three-deletion allowance is sharp from first-star information
alone.** Our field-plane fixtures each contain a valid twenty-word
first star and six mutually compatible residual words. Each missing
line conflicts with exactly three of those six, on its three distinct
charges; the whole 26-word family is a packing. A one-word replacement
deletes three and gives a valid 23-word family. For example, the
parallel fixture has line masks 15 and 240, markers 0 and 4, and
residual masks \(55,880,3248,217,779,3085\). All mask-to-set
decodings and intersections are checked. The other two fixtures
are in expected.json. Their second replication is two, not twenty.
They prove only the local loss boundary, neither attainment60 nor
compatibility with a full saturated second star.

**A bound below60 requires additional structure.** One possible
next lemma would show that at least one of the two replacement
orientations has at most two conflicts when the second star is
also saturated. Another would exclude equality57 in the transformed
family. Either must use the full two-star constraints; reducing
the three-charge count on the first star alone is disproved by
the fixtures. Equality60 would require three distinct conflict
words and an attaining upper57 transformed family, neither supplied
here. The earlier upper68 therefore cannot be attained under the
hypotheses, while sharpness of60 remains open.

**Broader parameter transfer:** the same ordinary replacement
always changes \((r_u,r_v,d_{uv})=(20,s,2)\) to
\((20,s-1,1)\), with loss at most three, whenever the first
star has the completion (3). Thus any independently proved bound
\(B(20,s-1,1)\) transfers to \(B(20,s,2)\le B(20,s-1,1)+3\).
This is a proved conditional transfer, not an assertion that the
needed bounds are known for all \(s\). Extending completion
beyond replication20 would require a new structural lemma; Dow's
particular eighteen-line threshold cannot simply be reused.
