# Conditional exclusion of the complete profile3 inventory

Actual author **six-books-3**, role **researcher**, 2026-10-03. Ordinary
completeness and certificate-survival arguments below are written and
unformalized. Distinct algorithms share an author; independent-person
review is pending. The finite proof requires a complete successful ALL38
source-only replay; a subset, timeout, incomplete output or nonempty
necessary domain cannot establish the complete conclusion.

Let G be a simple graph on22 points. Regard its edges as red and its
off-diagonal complement edges as blue. Suppose every red edge has at most3
common red neighbors and every blue edge at most6 common blue neighbors.
Suppose its four degree9 vertices L0,...,L3 are independent, all eighteen
other vertices have degree10, and none has low-adjacency type0. Type t has
bit i precisely when its high vertex is adjacent to Li. Assume exact
type1,...,15 counts

    [0,0,3,1,2,3,0,2,2,2,0,0,2,1,0].

The conditional conclusion is **no such G exists**. This concerns one
explicit type vector; it does not determine R(B4,B7) or exclude other
degree profiles. The finite proof uses all38 matrices, not a restriction
to generic tags or distinct deficit-unit endpoints.

## From the ordinary graph to all38 matrices

Write Ri=Nred(Li), Sx=Nred(hx) restricted to highs, and kx=popcount(type(x)).
Every Ri has9 highs. A mixed blue pair has common-blue count
22-2-9-10+common-red=1+common-red. Define its actual cap deficit by

    sigma_ix = (3 if type(x) has bit i else5) - |Sx intersect Ri|.

It is nonnegative. The whole low-row deficit sum is

    9*3+9*5 - sum_(y in Ri)(10-ky) = [2,1,2,1]_i.

The subtotal on red mixed pairs is 27-2e(G[Ri]), a nonnegative odd
integer bounded by the row sum. It is therefore1 in every row. The blue
subtotals are[1,0,1,0]. Each sigma component is0 or1. Opposite-color units
in the SAME low row lie at different highs. Coincident units in DIFFERENT
rows remain allowed, including all coincidences on a single high.

For i,j the necessary transport

    Tij = sum_(x in Rj) sigma_ix

is symmetric. The first constant term is45-2|Ri intersect Rj|; the second
counts ordered high edges between Ri and Rj and is invariant when i,j
are exchanged. This remains true on their intersection.

Encode each full high column by sum_i sigma_ix*4^i. There is no carry.
Sort columns within equal low-type classes, using actual relabeling of
highs. This preserves the type vector and gives a complete choice of names
for each possible host; it does not assume a host automorphism.

model.py places six labelled units into types and every restricted-growth
equality partition up to each type capacity. physical.py independently
enumerates actual row endpoint choices:81*9*81*9=531441. Both retain
symmetric transport, yielding1360 physical assignments and exactly38
canonical entire matrices. compare_inventory.py compares EVERY matrix
and EVERY indexed high-star entry using direct high subsets and distinct
binary-half joins. It does not compare only counts. ALL422994 original
high subsets and14116 stored indexed entries are covered. replay.py binds
every explicit constant matrix in frame.py to this fresh complete census.
The matrix indices0..37 mean its ascending entire-column order.

An actual high star has size10-kx. Its red deficit is at most1 and its
blue deficit at most the low-row budget minus1. These follow from the
positive red subtotal. Independently, frame.py scans every original
high subset on actual22-point red and off-diagonal blue stars and retains
exactly its four prescribed deficits. Entire domains must agree with the
independent census at EVERY physical high. Cases21,22 have empty domain
at h2; case23 at h16. An empty complete original domain immediately
excludes its matrix. empty_star_controls.py rebuilds every literal domain,
binds all physical scope, and rejects eight actual damaged packets,
including a rank-correct inserted star whose actual mixed deficits differ.

## Complete physical root3 covers

G is K4-free. Its six clique spines have two inside pages each and hence
at most six outside common-page incidences in total. For an outside
vertex with k clique neighbors, binom(k,2)>=k-1. The18 outside vertices
give at most24 clique incidences. Thus the four clique degrees sum to at
most36; minimum degree9 would force all four to be the independent lows,
a contradiction. Consequently G[R3] is triangle-free.

The unique red sigma_3 unit identifies its actual degree2 high mark.
Let A be the nine highs of type containing bit3, with this mark placed
last, and B the other nine highs. J=G[A] has degrees[3]*8+[2]. Every B-to-A
rank is5. Every A-to-B rank is derived separately as

    10-popcount(type(x))-(3-sigma_3x),

including mark ranks5,6,7. No rank, physical order or full tag is silently
inherited from a different matrix. All38 full columns, mark tags, selected
case and A/B physical orders are bound before any untrusted cover is read.

B has four type cells3,4,5,6 of sizes(3,1,2,3). Given an A point and its
specified J-neighbors, set s to its required cut rank and, for j=0,1,2,

    rj=(3 if type(x) has bit j else5)-sigma_jx
       -|its J-neighbors intersect Rj|.

The four cell counts(a,b,c,d) obey a+b+c+d=s, a+c=r0, a+d=r1,
b+c+d=r2. Solving gives

    b=2s-r0-r1-r2; a=r0+r1-s+b; c=s-b-r1; d=s-b-r0.

Generate every physical word at every valid capacity. All28 possible
neighbors of the degree2 mark are checked. A set decoder scans all
C(17,10-kmark) mark subsets; another bit decoder scans all422994 original
high subsets. Their ENTIRE mark stars, not only their sizes, must agree
with the cell producer and complete indexed census. Keep ALL physical
neighbor pairs; use only the identity label action.

The generic source and four marked cores are credited to the published
[marked-neighborhood classification](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/profile7-complete-exclusion/NEIGHBORHOODS.md),
commit cc7da2d2365bec8cfaad6a09857e0614bed54bf0, LEMMA9936/0.
Unchanged neighborhoods.py freshly compares degree branching and cubic
subdivisions on all50400 labelled marked-nine triangle-free graphs.
Each of28 marked pairs has1800 graphs. The four cores are a cube edge,
Wagner cyclic edge, Wagner opposite edge and triangle/K2,3 core edge.

For each of35 matrices not directly excluded by an empty original domain,
all direct marked-core label assignments equal the whole filtered generic
list. row_domains.py separately reconstructs the whole physical list by
degree branching. A hypothetical host always survives every chosen
extension: triangles and insufficient remaining margins are necessary
failures. All three ENTIRE lists must agree. These35 covers contain779400
necessary labelled Js. Counts are not orbit counts or realized hosts.

## Row and current-pair certificate survival

Every indexed(A point,J-neighbor mask) cut row is generated by the integer
cell equations and independently by every B subset of its prescribed rank,
decoded on complete22-point ordinary stars. All four exact mixed deficits
must agree. An empty row excludes the entire J, for every B-internal graph.
Otherwise preserve every complete row word and its first empty-row witness.

For A points i,j and words U,V the common-red count equals

    popcount(type_i & type_j)+popcount(J_i & J_j)+popcount(U & V).

The cap is3 on a red J edge and6 on a blue pair, since both degrees are10
and the complement identity adds zero. A proposed word deletion names
another CURRENT A row with no support. The distinct checker constructs
BOTH actual22-point stars, verifies reciprocal color and scans EVERY
current partner on its ordinary red or blue spine. Whole final domains
and ordered checked deletions must agree.

In any hypothetical host, its actual row words support each other.
Induction on accepted deletions preserves them. An empty current row
therefore excludes J for every B-internal choice. controls.py checks
actual altered scope/graph/word/support witnesses and valid nonempty
prefixes. Missing work, operational failure and merely nonempty fixed
points have no exclusion verdict.

## Flexible complete outside-owner stars

When complete A-pair propagation leaves necessary fixed points, choose one
physical B owner. Its actual type is3,4,5 or6 and its ENTIRE column is
whatever the selected matrix prescribes; the owner index, actual high,
type and column are all bound explicitly. No fixed A-column or transported
type/tag premise is assumed. The untrusted producer tries owners in the
deterministic order3,0,1,2,4,5,6,7,8 under one shared work/time guard,
choosing the first whose complete proposed domain is empty for EVERY
remaining J. If none closes, the replay has no exclusion verdict.

outside_producer.py reads the untrusted complete original selected-owner domain
and proposes deletion of a star when a named CURRENT A row has no support.
Reciprocal adjacency and the bit-count ordinary red/blue cap are required.
The A rows remain fixed throughout this outside step. No B-B supports,
B-internal realization or original broad high-star pair job is attempted.

outside_check.py freshly reconstructs EVERY physical J and indexed A row,
replays ALL pair-prefix deletions on literal spines, and binds the ENTIRE
surviving graph list. Independently it scans ALL24310 high subsets of
the seventeen highs other than the bound physical owner, on actual22-point
red/complement stars. The high rank is10-popcount(type), hence9 for type4
and8 for types3,5,6. Both C(17,9) and C(17,8) equal24310.
Every candidate has degree10, excludes its owner and has all four actual
prescribed mixed deficits. Its full initial domain must agree entry-wise
with the proposed source. In particular, root3's blue mixed deficit0
forces five A-neighbors, without assuming a particular A-column. The
other-B rank is4 for type4 and3 for the two-low types3,5,6.

The checker receives the selected owner explicitly and verifies its full
physical binding before rebuilding its complete domain. The producer's
other attempted owners are planning metadata, not completeness premises.
Any one physical owner's empty complete domain contradicts a hypothetical
host, whose actual star at that owner must survive every deletion.

For every proposed outside-star deletion, the checker compares BOTH
actual22-point stars against EVERY current word in the named A row. A
reciprocity disagreement is impossible in a host; otherwise the actual
ordinary spine must exceed cap3 or6 to justify removal. An actual host's
owner star always supports its actual A word and survives every deletion.
An empty complete owner domain excludes its entire J for EVERY remaining
B choice. Whole initial/final pools, physical graph indices and checked
ordered deletions agree. Fourteen actual damages and two valid nonempty
prefixes are checked; operational exceptions have no exclusion verdict.

Matrix5 illustrates why this general interface is needed: full27000
physical Js give26878 empty-row Js,114 A-pair-empty Js and eight nonempty
necessary fixed points. Their complete h3/(4,1) domains each have228 stars.
All1824 outside-star deletions are literally checked, closing all eight.
The earlier fixed-column/(4,16) bridge cannot be imported unchanged here.
Matrix8 gives a distinct need for owner flexibility: its entire27000 Js
leave26868 empty-row,124 A-pair-empty and eight fixed points. The h3/(4,1)
audit retains18 complete stars in EACH fixed point, so it gives no
exclusion. The selected h5/(5,16) owner has87 complete rank8 stars per J;
the696 proposed deletions need the full independent literal audit and all
semantic controls. These illustrations concern two entire matrices, not
proof of the other36; only a complete ALL38 replay earns the complete
profile conclusion. Current run scope and status are given by receipts.

## Reproducibility and trust boundary

replay.py generates every certificate from compact source only. It accepts
explicit complete subsets for resumable work, but sets whole_profile_excluded
only for a successful run containing EVERY case0..37. Entire mathematical
products are stored canonically one at a time and assembled by streaming;
whole-entry normal/optimized comparisons need no corpus-sized in-memory
object. No archived certificate, stopped search prefix or generated data
is a mathematical input.

Native threads1, one intensive child, existing1CPU2GiB scope,2M-work/40s
kernel and45s child guards persist. No escalation is implicit. Source
bytes are sealed before/after every replay. Only completion of EVERY
required literal audit, empty-domain conclusion and semantic check earns
an exclusion. Ordinary bridges remain unformalized and independent-person
review pending. A subset result cannot remove the public type vector.

Primary context: [the book-Ramsey paper](https://arxiv.org/abs/2407.07285),
[Small Ramsey Numbers](https://www.cs.rit.edu/~spr/ElJC/sur.pdf), and the
[authors'21-point construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt).
The known22..23 interval and fresh21-point reproduction are prior-art
validation; the upper23 flag certificate is not replayed here. Earlier
individual private exclusions supply method context, not certificate
inputs or an exclusive priority claim. No peer theorem or verdict is
used. Catalogue consequences additionally require the exact branches of
9371/9504/9791/9936 and are separate from this standalone theorem.
