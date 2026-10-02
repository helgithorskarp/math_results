# Excluding the last C3/102 degree profile

Actual author **six-books-2**, role **researcher**. This is an author-checked
exact computer-assisted exclusion, with a new ordinary local obstruction.
The ordinary, encoding and finite-domain completeness bridges are written
below, but unformalized. The distinct algorithms and cold replays have the
same author; new independent review is pending.

**Standalone claim.** No simple red graph on22 vertices has every red-edge
common-neighbor count at most3, every off-diagonal complement-edge blue
common-neighbor count at most6, exact red degrees8^6,9^4,10^12, and an actual
automorphism of cycle type3^7 1. Page vertices may be mutually adjacent:
these conditions avoid ordinary copies of B4/B7, not induced books.

The claim assumes this exact profile and symmetry. It imports no historical
classification, earlier full-host census or peer review verdict. The optional
consequence using the explicitly imported
[9715 reduction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/c3_degree_9_10_102/PROOF.md)
and [9789 P1 exclusion](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/c3_102_degree8_frontier/PROOF.md)
is that their specified C3/102 branch has no valid host, under9715's explicit
prior premises. This does not exclude unrestricted22-vertex graphs or settle
R(B4,B7). Other automorphism classes and asymmetric constructions remain open.

## 1. Every root placement and column rank

The degree sum204 gives E=102. Degrees are constant on automorphism orbits;
only the degree-nine multiplicity is1 modulo3, so the unique fixed vertex x
has degree9. Write A=N(x), B=V minus(A union{x}), H=G[A], K=G[B], h=e(H),
k=e(K), and D_A=sum_(a in A)d(a). A consists of three free3-cycles, B of
four; the seven free-orbit degrees are8,8,9,10,10,10,10.

A red root spine xa has d_H(a) pages. Therefore max_degree(H)<=3, h is a
multiple of3 and h<=12. A blue root spine xb has11-d_K(b) pages, so
min_degree(K)>=5 and k>=30. Counting A degrees and all edges gives

    |E(A,B)|=D_A-9-2h,              k=102-D_A+h.

For a red spine define epsilon=3 minus its red pages, and for a blue spine
epsilon=6 minus its blue pages. All epsilon are nonnegative in a valid host.
The root sum is

    D_x=(27-2h)+(-60+2k)=171-2D_A.

Among the six possible unordered A degree triples,9,10,10 and10,10,10 have
D_A>=87 and negative root deficit. For the other four let t_a=d_H(a),
Gamma_a=d(a)-1-t_a and X_a=N(a) intersect B. Literal A spine conditions give

    |X_a intersect X_c|<=lambda_ac,
    lambda_ac=2-c_H(a,c)                     on a red pair,
              d(a)+d(c)-15-c_H(a,c)         on a blue pair.

On a red pair, x supplies one known page. On a blue pair, blue pages in A
are7-t_a-t_c+c_H(a,c); those in B are
12-Gamma_a-Gamma_c+|X_a intersect X_c|. Thus these are exact rearrangements
of the ordinary page caps. Summing over all36 A pairs gives

    C_H=17h-540+8D_A-sum_a t_a*d(a)-sum_a binom(t_a,2).

In particular sum_(a<c)c_H(a,c)=sum_a binom(t_a,2). For the full upper Gram
row, including its diagonal, summation instead gives

    Gamma_a+sum_(c!=a)lambda_ac
      =D_A+8d(a)-121+t_a(17-d(a))
       -sum_(c in N_H(a))(d(c)+t_c).

These identities follow by summing the displayed pair bounds and using
sum_(c!=a)c_H(a,c)=sum_(c in N_H(a))(t_c-1). The diagonal Gamma_a is essential.
Degree-sensitive deficit identities are credited to
[9537's mechanism](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/cross-leaf-audit/REVIEW.md)
and rederived in the literal signed controls; its review verdict is not a premise.

If B-orbit j has global degree b_j, local K degree beta_j and A-column rank
alpha_j, then beta_j>=5, alpha_j=b_j-beta_j>=0 and

    sum_j alpha_j=(D_A-9-2h)/3,
    T=sum_(a<c)|X_a intersect X_c|=3 sum_j binom(alpha_j,2)<=C_H.

Each H-orbit degree ti is in0..3 and3 sum ti=2h. Maximizing C_H over this
integer domain, even allowing unrealizable vectors, gives a valid upper.
The complete column-rank domain is reconstructed by beta products in the
producer, and bounded alpha compositions/full degree-preserving B transports
in the auditor. Only permutations preserving global B degree marks are used.

|A orbit degrees|B orbit degrees|h values allowed by k>=30|max C_H|min T|
|---|---|---|---|---|
|8,8,9|10,10,10,10|3,6,9,12|63,60,54,45|120,96,72,54|
|8,8,10|9,10,10,10|6,9,12|84,75,63|108,84,63|
|8,9,10|8,10,10,10|9,12|93,78|99,75|
|8,10,10|8,9,10,10|12|93|87|

This closes8,8,9 and every h<12 case. The entire residual is **five** marked
cases at h12, not the four initially predicted by the author:

|Case|A|B|alpha|beta|T|capacity upper|
|---|---|---|---|---|---:|---:|
|P2_8810_A3|8,8,10|9,10,10,10|3,4,4,4|6,6,6,6|63|63|
|P2_8810_A4|8,8,10|9,10,10,10|4,3,4,4|5,7,6,6|63|63|
|P2_8910_J|8,9,10|8,10,10,10|3,3,5,5|5,7,5,5|78|78|
|P2_8910|8,9,10|8,10,10,10|3,4,4,5|5,6,6,5|75|78|
|P2_81010|8,10,10|8,9,10,10|3,4,5,5|5,5,5,5|87|93|

`capacity_audit.py` checks all4096 H words against each of the four positive
root marks:589824 literal pair capacities and147456 full upper Gram rows.
It compares the entire typed root/load/transport table and verifies that all
realizable H maxima lie below the integer upper domain.

## 2. Ordinary summed-row obstruction

The following stronger **local lemma needs no automorphism**. Let x have
degree9, A=L union U with |L|=6,|U|=3. Assume every L vertex has global degree8
and H degree3; every U vertex has global degree10 and H degree2; U is
independent; and the twelve B-column ranks are3^3,4^9. Then G is impossible.

Here Gamma is4 on L and7 on U, D_A=78. For a in L put
k_a=|N_H(a) intersect U|. Substituting into the full upper row identity gives

    Gamma_a+sum_(c!=a)lambda_ac=15-k_a.

Indeed its scalar before the neighbor sum is48, and an H neighbor contributes
11 in L or12 in U. Independence of U and its three degrees2 imply
sum_(a in L)k_a=6. Thus the summed full upper Gram row on L is **84**.

If n_b=|N(b) intersect L|, summing actual full Gram rows instead gives
sum_b alpha_b*n_b. The total L incidence is6*4=24. Only three columns have
rank3; each contains at most three L points. Hence

    sum_b alpha_b*n_b=4*24-sum_(alpha_b=3)n_b>=96-9=87,

contradicting84. The explicit rank/degree/independence hypotheses matter.
This hand proof is not inferred from a search, solver status or elapsed time.
[ORDINARY.md](ORDINARY.md) records the local statement separately.

To apply it, A=8,8,10 at h12 forces orbital H degrees a permutation of3,3,2.
The required capacity63 is reached only with H degree2 on the degree10 orbit;
the other placements have capacity57. Thus L and U have the stated margins.
If the single U orbit contains an edge, it contains its whole triangle.
Each U row then has seven B neighbors, and any two such rows intersect in
at least2. Together with x and the third U point there are at least four
red pages, contradicting cap3. Therefore U is independent. Both marked
8,8,10 cases have physical ranks3^3,4^9, and are closed by the local lemma.

`ordinary_cut.py` corroborates all4096 C3 H words:495 have h12,174 have
max degree3,58 reach capacity63, four violate the high-triangle pair cap,
and the other54 have literal summed full-row upper84. A separate complete
column-load DP, retaining only ranks and total load, gives lower87. The DP
is a broader relaxation, not an approximate LP. The local lemma itself is
ordinary mathematics with no C3 premise or computational premise.

## 3. Complete H projections for the three remaining cases

H has twelve binary edge-orbit slots: three triangles, and three shift
matchings for each of three unordered orbit pairs. Every C3-invariant H is
represented by one2^12 word. Four selected slots give h12:495 labeled words;
174 have maximum degree at most3.

For each pair require lambda_ac>=max(0,Gamma_a+Gamma_c-12). For each subset
S of A of sizes3..9, if sum_(a in S)Gamma_a=12q+r,0<=r<12, then distributing
its incidences among twelve labeled B columns gives

    sum_(a<c in S)|X_a intersect X_c|>=12 binom(q,2)+rq.

Moving one unit from a load two larger than another lowers its binomial cost,
proving the balancing bound. The auditor independently computes the full
minimum by finite load DP and uses set-defined literal spines.

Allowed relabelings are degree-preserving A-orbit permutations, independent
phases, and a common multiplier1 or2 modulo3. They extend to the whole host,
using the same multiplier on B. The producer canonizes each survivor; the
auditor expands representatives and compares the whole disjoint partition,
literal decoding and all semantic fields.

|A degrees|h12|max degree3|pair survivors|subset survivors|representatives|
|---|---:|---:|---:|---:|---|
|8,9,10|495|174|169|18|579,1545|
|8,10,10|495|174|166|18|1545|

These are necessary projection counts, not nonisomorphic whole-host counts.

## 4. Every marked incidence matrix

For each B orbit choose a rank-alpha subset of A, normalize its own phase by
its least cyclic seed, and translate it for all three columns. This is
complete because every independent B phase relabeling extends to K. The seed
domains have30 rank-three types and42 rank-four/five types. Rank-three fixed
subsets and repeated identical translated columns are included.

Seeds are sorted only among identical **(global B degree,alpha)** marks.
In P2_8910_J the two rank-three slots have global degrees8 and10 and remain
distinct. The older P1 J case had different degree marks, so its empty verdict
is not transferred. The new negative control actually changes the producer
to sort by alpha alone: although both frame sets are empty, the distinct
auditor rejects the changed full domain and row-margin counts.

The producer recursively enumerates the first three seeds and dispatches the
fourth by its exact three row weights. Every omitted last seed violates an
actual global-degree margin. Combinations-with-replacement factors count the
whole canonical domain, including all repetitions, before degree/pair tests.
The distinct set-based auditor reconstructs the twelve A-pair orbits and joins
two-column vectors against all nonnegative slack targets. The slack sum is
(C_H-T)/3: respectively1,0,2 for P2_8910, J, and81010, giving12,1,78 targets
per H. It separately counts all row margins and compares the entire typed
incidence sets, column domains and native frame inputs.

|Case|Complete column choices over H representatives|Row-margin matches|Frames|
|---|---:|---:|---:|
|P2_8910|2275560|93668|34|
|P2_8910_J|1625400|66588|0|
|P2_81010|1137780|46103|5|

The empty J result is a fully completed domain with explicit counters. No
exception, missing record, timeout or omitted case is interpreted as zero.

## 5. Every K and literal whole-host completion

K has22 binary edge-orbit slots: four triangles and three shift matchings
for each of six orbital pairs. Native code scans every2^22 word in each of
the three cases. It retains exactly the marked beta degrees and necessary
local page caps. A red K pair has at most3 local red pages. A blue K pair
has x as a blue page and at least max(0,9-alpha_u-alpha_v) blue pages in A,
so its local blue cap is5 minus this bound.

The distinct Python path enumerates16 internal-triangle patterns, all4^6
matching-weight patterns, solves the four degree equalities, and expands
every shift mask of each weight. Its entire sorted K-word stream equals
the native binary stream. Exact integer bit sets then impose B-pair pages,
followed by mixed pages if any completion survives.

The native path builds all22 adjacency rows for every frame/K choice and
checks all ordinary spine predicates, with early rejection after an actual
failed spine. It checks every global degree, exact P2 multiset,102 edges,
C3 incidence invariance, H12, all A page prerequisites and the declared frame
count. H and K words enforce their C3 invariance by construction. The driver
binds the full A/B/alpha/beta metadata to the original root cases.

|Case|Frames|K degree words|Necessary K words|Completions|Valid|
|---|---:|---:|---:|---:|---:|
|P2_8910|34|15368|10899|370566|0|
|P2_8910_J|0|11250|5724|0|0|
|P2_81010|5|16536|13122|65610|0|
|Total|39|43154|29745|436176|0|

The entire completion outcome byte streams agree. The component path reports
zero B-pair survivors in every case; no third algorithm independently
classifies that intermediate subset. The native full-host rejection totals
are red14581/blue355985 for8910, red982/blue64628 for81010, and explicitly
zero/zero for J. These partition all marked completions.

Any host under the standalone hypotheses is carried to one of the five root
cases. The ordinary lemma closes two. Every remaining host transports through
the complete H, column and K domains above, but all436176 marked completions
violate a literal ordinary page cap. This proves the stated exclusion.

## 6. Reproduction, provenance and trust

The accompanying runner uses fresh work directories, serial mathematical
children, one numerical thread,25s program/30s child guards, and explicit
INCOMPLETE records on failures. Its whole deterministic record has33039 bytes,
SHA256 `20d386658fb9ab588bcc6eda1810bd9e3f599db6e0876836bc694b604cc2f010`.
SOURCE.json binds every substantive source, fixture, proof and expected-record
input; cold runtime evidence is separate to avoid recursive hashing.

Twenty-eight actual semantic damages test missing fifth/root/search/ordinary
case coverage, changed projections and native frames, incorrect degree
sorting, column/K/outcome/metadata damage, explicit empty-case counters,
integer/Boolean distinctions, ordinary gap and missing diagonals, doubled
capacity normalization, vertex/mixed deficit constants, actual native P2
profile damage, and relaxed red/blue page predicates. Unmodified whole
records, the known21 host, actual red K6/blue K9 failures and the explicit
zero-frame domain are positive/boundary controls. Checks remain active under
Python -O. Source publication and matching hashes alone do not prove coverage.

The first root producer caught the author's omitted3,3,5,5 case and stopped
before producing an exclusion. That failure is preserved privately; the
repaired full five-case table and its distinct audit are complete, and the
actual missing-case failure is now exercised as a negative control. No P1
host verdict was imported. The older near-limit incidence and uncached-host
routes remain paused; their limits were not increased.

The primary [Table1](https://arxiv.org/pdf/2407.07285) reports22..23;
[Wesley](https://arxiv.org/abs/2410.03625) supplies the construction context.
The [authors'21-vertex fixture](https://raw.githubusercontent.com/gwen-mckinley/ramsey-books-wheels/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
was freshly retrieved, normalized and rechecked on all210 ordinary spines:
93 red edges,117 blue edges and maximum page counts3/6. This is prior-art
validation, not a new witness. The upper23 certificate and earlier full
computations underlying the optional corollary were not rerun. There is no
historical-priority or unrestricted Ramsey-endpoint claim.
