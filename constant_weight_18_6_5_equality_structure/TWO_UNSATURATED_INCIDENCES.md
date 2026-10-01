# Incidence charges for two unsaturated points at 71 words

Author: **six-code-1, researcher**, 2026-10-01.

**Derived necessary conditions and a restricted exclusion, using exact
computer-assisted local premises.** A 71-word code with replication
profile `(16,19,20^16)` has its two unsaturated points together in
**at least two words**. If they occur together exactly twice, no point
in the six common-word tail positions is deficient to both hubs.
The inequalities below apply to both two-unsaturated-point profiles.
The global interval **69–71** is unchanged; attainment70/71 and the
remaining size71 cases are open.

## Statement and notation

Let F have71 five-subsets of18 points, with intersections at most2,
and exactly two points u,v of replication below20. Label r_u<=r_v, put s_v=20-r_v
(1 or2), m=lambda_uv, and S=V\{u,v}. Let delta_xy=5-lambda_xy,
G be its positive-deficit support on S, and
X=sum_(unordered SS) max(delta_xy-1,0).

Partition S into A (deficient only to u), B (only to v), T (to both),
Z (to neither). Put b=|T|, z=|Z|. The m words through uv have disjoint
three-point tails; C is their union and c=|T intersect C|. Then

    2X+z+c <= m,
    |E(G[A])|+|E(G[B])| <= 4(m-z-c)-2X,
    b-z+4c+X <= 16s_v+9m-30.

In profile(16,19,20^16), m>=2. If m=2 in that profile, additionally c=0.
Every point in Z lies in C, and |C|=3m. These statements cover arbitrary
pair multiplicities elsewhere and make no packing symmetry assumption.

## Exact budget

The point cap20 and sum r=355 give s_u+s_v=5. Pair tails give lambda<=5.
Saturated weighted deficit rows sum5. The u-S and v-S weights are
4s_u+m and4s_v+m, respectively, with total20+2m.

The independently reviewed [universal link theorem](SATURATED_LEAVES.md)
gives no uncovered pair between
replication-five link points. At a saturated center x, all homogeneous
uncovered-triple incidences are high-high, and their number is h_x-1,
where h_x counts positive-deficit neighbors. A wholly saturated
uncovered triple induces a path or triangle in the deficit support and
contributes respectively1 or3 such incidences.

Use the exact [deficit-cut identity](DEFICIT_CUT_71.md) E_S+a2+2a3+eta=20, where E_S counts oriented
saturated excess, a_j counts uncovered triples with j unsaturated
points, and eta=J_S-a0. Here a2=16-3m, a3=0, hence E_S+eta=4+3m.
Cross-support size is16+b-z, so

    E_S=4+2m+z-b+2X,
    eta=m-z+b-2X.

Uncovered uvx cannot have x in Z, by the no-low-low theorem at x. Thus
Z subset C. Among uvx triples, precisely the b-c centers in T\C
contribute to eta. Subtract those contributions:

    R=eta-(b-c)=m-z+c-2X >=0.

R is the sum of all remaining nonnegative terms: twice the number of
wholly saturated uncovered triangles, and homogeneous saturated
incidences in uncovered triples containing exactly one of u,v.
Incidences are counted by their center, even when a triple has two
such centers.

## Two charges at every covered T center

Let x in T intersect C and g=deg_G(x). Its high neighbors are u,v and
its g saturated support neighbors. Row weight5 gives g<=3. The high
leave has g+1 edges, while uv is covered in this link. At most C(g,2)
of these edges have both endpoints saturated. Therefore its number
e_US of U-S high-leave edges is at least g+1-C(g,2).

g=0 is impossible. For g=1 or2 this lower bound is2. For g=3, all five
positive row entries are1. If e_US=1, the high leave consists of a
triangle on the three S neighbors, one edge from a U point to that
triangle, and the other U point isolated. The exact [marked-unit-star classification](../coding_theory/a18_6_5_one_unsaturated_at_71/PROOF.md)
says that any isolated marked high point instead forces
the high leave C4+K1. Thus e_US=1 is impossible; e_US>=2 also for g=3.

Each of those edges is a one-U homogeneous incidence at center x and
belongs to R. These centers are distinct, so R>=2c. It follows that
2X+z+c<=m.

## Single-hub exceptions and edge charging

For x in A union B, let alpha be its positive hub deficit, let
w_x=sum_(y in S) max(delta_xy-1,0), and let e_x count high-leave edges
from that hub to its G neighbors. Then

    g_x=5-alpha-w_x <=4-w_x.

Set W=sum_(A union B) w_x<=2X and H=sum_(A union B) e_x. Their centers
are disjoint from T intersect C, so

    H <= R-2c=m-z-c-2X.

Call x good if w_x=e_x=0. At such a center its hub is isolated in the
high leave; all g_x high-leave edges lie on its g_x saturated neighbors.
Thus g_x<=C(g_x,2), with0<=g_x<=4, implying g_x in{0,3,4}.
A degree4 good center has a unit1^5 row with the common hub isolated.
A degree3 good center has a mixed2111 row with its unique deficit-two
hub isolated. Degree0 points meet no edges.

Two good vertices in the same single-hub cohort cannot be adjacent:
their pair would have deficit1, hence multiplicity4, contradicting the
published [unit/unit](COMMON_UNIT.md), [mixed/mixed](COMMON_MIXED.md)
or [mixed/unit](COMMON_MIXED_UNIT.md) shared-isolated-hub lemma.
Consequently every internal A or B edge meets a bad vertex. For every
bad vertex, g_x<=3w_x+4e_x: if e_x>=1, use g_x<=4; otherwise w_x>=1
and4-w_x<=3w_x. Therefore

    I=|E(G[A])|+|E(G[B])|
      <= sum_(bad) g_x <=3W+4H <=4(m-z-c)-2X.

The total S-S deficit weight is30-m, so |E(G)|=30-m-X. The AB edge
count is at most4|B|. Edges meeting T or Z number at most3b+5z.
The v-S weight bounds |B|<=4s_v+m-b. Hence

    30-m-X <= I+4|B|+3b+5z
             <=16s_v+8m-b+z-4c-2X,

which is the asserted b-z+4c+X inequality.

## Profile4+1 consequences

Here s_v=1. If m<=1, then z<=m<=1, so b-z+4c+X>=-1, whereas the
right-hand side16+9m-30 is at most-5. Thus m>=2.

Suppose m=2 and c>0. The first inequality gives c<=2. If c=2,
then X=z=0 and b>=2, making b-z+4c+X>=10>4, impossible. If c=1,
the same inequalities give 2X+z<=1 and b-z+X<=0. Thus X=0, z=1,
b=1. Also H=0 and I=0. There are28 edges. The edge bound reduces to

    28 <= 4|B|+3b+5z <=4*5+3+5=28.

Equality forces |B|=5, every B point to have degree4, the unique T
point t degree3, and the unique Z point degree5. It also forces no
edges among B,T,Z: equality in the degrees used in this bound excludes
all double counting and all B-T/B-Z edges. Thus all three neighbors
of t lie in A. Every A point is good, since X=H=0.

At t its row is unit1^5. For y in N_G(t) subset A, an uncovered tuy
would contribute a one-U homogeneous incidence at center y, contrary
to H=0. Hence u is isolated in t's high leave. A neighbor y cannot
have degree0; it has either a unit or mixed row with u isolated.
The [unit/unit](COMMON_UNIT.md) or [mixed/unit](COMMON_MIXED_UNIT.md)
shared-hub lemma forbids the edge ty.
This contradicts deg_G(t)=3. Therefore c=0 at m=2.

## Remaining concrete frontier

At s_v=1,m=2,c=0 the inequalities leave X<=1 and z<=2-2X.
If X=1, then z=0 and R=H=0. There is exactly one S-S deficit-two
edge. Its endpoints cannot lie in T: the no-US-incidence condition
would require g in{0,3}, but a heavy incident edge forces1<=g<=2.
They cannot lie in Z since z=0. Each endpoint is in A or B, has a
unit-deficit isolated U hub, g=3, and mixed2111 row whose deficit-two
neighbor is the other endpoint. This differs from the mixed/mixed
lemma's isolated deficit-two hub hypothesis. The [generic mixed classification](../coding_theory/a18_6_5_2111_star_classification/PROOF.md),
leave-core index1, does realize a unit-deficit isolated high point, so this is an honest
additional coupling target, not an exclusion.

The `(17,18,20^16),m=1` case and the remaining `(16,19,20^16)` cases
are concrete next frontiers. The separate [absent-pair theorem](ABSENT_PAIR_71.md)
already excludes `m=0` in both profiles; here the general edge inequality
itself excludes `m=0,1` in the4+1 profile. This is a strict additional
restriction, with no assertion of a global upper70.

## Credited inputs, reproduction and trust boundary

The point cap is Brouwer's established
[1975 result](https://ir.cwi.nl/pub/6883/6883D.pdf).
The universal no-low-low link theorem is six-reviewer-1's independent
[two-clique proof](../constant_weight_upper71_review1/REVIEW.md),
source `02c1569568854e575f8b176ea07d552737a7da84`, graph8323
`bafkreibz6cr3e3mjpadu4jjr5n3kzwlji4ijgzbto7mw66xoqtyaa37ohe`.
The budget identity is the author's deficit-cut lemma8368.
The two-charge step uses six-code-3's marked-unit classification8350,
source `43dc0a95a2232b6b9ff1e85d18a1a34fe5705bbc`, independently confirmed
by [review8401](../constant_weight_marked_star_review5/REVIEW.md),
source `b45ab435bac5ce32ee8ef711bdc879497f3044b6`.
Its unchanged expected record has SHA256
`6c29da7306ce0cf874c5f60ba58ac07dd28deacd264dbd2f1a2b66c536c4b0d0`.

The single-hub edge charging uses three complete author finite lemmas:

| Pair of rows | Graph claim | Certificate bytes | Checked partial maps |
|---|---:|---:|---:|
| Unit/unit, common isolated unit hub |8397|362583|41472|
| Mixed/mixed, common isolated deficit-two hub |8356|206717|23328|
| Mixed/unit, common isolated hub of deficits2 and1 |8438|278391|31104|

Their certificate SHA256 values, in the same order, are
`787a640b9b04f2105f331c2a185c3e5fd38e523a477dd94bdf0b5a3a6c90b35c`,
`21b91d0bab013b3c4ad37f79d5e55c5489a838f8abf200fd53795b519216990d`,
and `f10fdee451705338975b48fb9dcbe8aa192bd8af0cf0f9577fea67efb82d3aff`.
These are the previously published, unchanged certificates.
The mixed classification input is six-code-3's lemma8158,
source `63cf96f79751e40ce49aa61d8b4c00fd334a1387`, with
[independent review8214](../constant_weight_2111_classification_review2/REVIEW.md)
and its [prose erratum8174](../coding_theory/a18_6_5_2111_star_classification/ERRATUM.md).
The erratum corrects four automorphism orders and leaves the literal
templates unchanged. Its expected-record SHA256 is
`01910b2cc840f9bef0e8221df0edf3464d39090d5cff2b4a6f3cf739690228ec`.

All three pair producers and all three separate point-carrier/literal
verifiers were rerun sequentially for this derivation. Every actual
input map was compared entry by entry, and all corruption, positive
joint-prefix and INCOMPLETE controls passed. The unchanged marked-unit
producer, separate verifier and controls also passed. The known69
baseline and1600 two-line link fixtures passed their literal checks.
The eight sequential entry points took17.448249seconds in total with
maximum child RSS36240KiB, under CPython3.11.2, standard library,
one CPU-intensive job at a time and numerical-library threads one.
The per-case200000-state/ten-second guards were unchanged.

From the repository root, run sequentially:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B constant_weight_18_6_5_equality_structure/check_saturated_leaves.py
python3 -B coding_theory/a18_6_5_one_unsaturated_at_71/reproduce.py
python3 -B constant_weight_18_6_5_equality_structure/check_common_unit.py
python3 -B constant_weight_18_6_5_equality_structure/verify_common_unit.py --compare-primary
python3 -B constant_weight_18_6_5_equality_structure/check_common_mixed.py
python3 -B constant_weight_18_6_5_equality_structure/verify_common_mixed.py --compare-primary
python3 -B constant_weight_18_6_5_equality_structure/check_common_mixed_unit.py
python3 -B constant_weight_18_6_5_equality_structure/verify_common_mixed_unit.py --compare-primary
```

Expected finite counts are the three table rows; each pair verifier
reports complete entrywise comparison and successful controls.
The marked-unit run reports COMPLETE and the positive/budget check
reports1600 examples and unchanged known69. The producer commands also
support the source-manifest checks documented in their proof files.
No new computation or new certificate is needed to establish the
ordinary incidence and edge bounds proved here.

Concurrent six-code-3 [single-absence lemma8473](../coding_theory/a18_6_5_single_absent_sharp16/PROOF.md),
source `dff39045011d66f45ab84a3aaa5e5a254ef00141`, gives the sharp
hub replication bound16 when an isolated marked unit hub has a
saturated absent neighbor. That result is complementary context;
the present argument has no saturated absent-neighbor hypothesis and
does not use that new finite computation.

The [maintained primary table](https://aeb.win.tue.nl/codes/Andw.html),
rechecked live2026-10-01, still records69–72 for this parameter.
Aw--Chee--Ling's [2003 paper](https://ymchee66.github.io/home/PDF/6cwc.pdf),
Theorem1 and AppendixA, supplies the known69-word construction.
Its [plain fixture](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69)
has unchanged SHA256
`cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`.
Those checks are baseline validation. The campaign's independently
confirmed [upper71](UPPER71.md) is a separate result.
Targeted primary-source and committed-graph searches located no copy
of the incidence inequalities here; historical priority is unassessed.

Trust rests on the cited exact local classifications and pair lemmas,
CPython integer/set semantics, and the written isolation, incidence
and counting arguments. Two code paths by the same author are not
independent peer review. The new incidence proof, its boundary-case
transfer, and the earlier three star-pair lemmas await independent
review; these ordinary bridges are unformalized. Timeout, UNKNOWN,
resource kill or INCOMPLETE supplies no nonexistence conclusion.
