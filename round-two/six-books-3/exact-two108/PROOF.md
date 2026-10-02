# Exactly two one-nine roots are impossible in a four-nine host

Actual author **six-books-3**, role **researcher**, 2026-10-02. Campaign
signatures share an identity; two implementations by this author are not
independent peer review.

A valid graph is a simple red graph on22 points, with at most three common
red neighbors on every red edge and at most six common blue neighbors on
every blue nonedge. Books are ordinary subgraphs: page-page edges are
unrestricted. Degrees are red degrees. A full root is a degree-ten vertex
whose ten red neighbors all have degree ten. A one-nine root has degree ten,
one degree-nine red neighbor, and nine degree-ten red neighbors.

**New finite theorem.** No valid rootless graph of degrees `9^4,10^18` has
exactly two one-nine roots. The two ordinary preliminary cases are excluded
below; the remaining case is covered by six incidence profiles and82
canonical exception templates, with24 empty initial domains,48 static
covers, and10 sequential deletion certificates. These are complete necessary
domains, not a sampled search or a classification of realized hosts.

**Combined consequence.** The earlier
[9199 two-root theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/one-nine-occurrence108/PROOF.md)
gives at least two, so every valid rootless four-nine host has at least
**three** one-nine roots. Every valid108-edge graph on22 points also has at
least three: the imported
[9102 rootlessness theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/four-nine108/PROOF.md)
and its upper-degree-ten premise leave only `9^4,10^18` and `8,9,9,10^19`;
the latter already has at least seven by the credited
[8987 result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/dirty-root-audit/REVIEW.md).
The three-low seven-root bound is not new. No whole108-edge exclusion,
count sharpness,22-point construction or Ramsey endpoint follows.

The ordinary reductions, enumeration correspondence and Python execution
remain unformalized. The new theorem awaits independent review. Inherited
premises retain their exact scopes; no historic minimum-degree classification
is imported. Source publication or digest agreement alone is not a proof.

## 1. The three possible exact-two sectors

Let L be the four degree-nine points, H the eighteen degree-ten points,
q=e(L), and n_t the number of high points meeting t lows. Rootlessness is
exactly n0=0. Counting gives

    sum n_t=18, sum t*n_t=36-2q,
    n1=2q+n3+2n4.

Thus n1=2 permits only `(q,n3,n4)=(1,0,0),(0,2,0),(0,0,1)`.
This occurrence count and its prior retained exception are credited to
[8939](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/rootless108_marked_profiles/PROOF.md),
source `5c04d6aaa9cedc7d8dda6082ef5ac7ae60cc40ae`.
Without rootlessness the count has an additional `-2n0`; that hypothesis
cannot be discarded.

For a blue pair in a graph on22 points, endpoint inclusion-exclusion gives
`c_B=20-d(u)-d(v)+c_R`. This standard interface, credited to
[8541](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md),
source `53fa7ea66251df9d255b7d0ff9d0ff309580d42a`, is rederived by deleting
both endpoints. A mixed9/10 blue pair therefore has red codegree at most5;
a red mixed pair has red codegree at most3.

Put a_i=d_L(i), and let s_i,p_i,f_i count the singleton, triple, quadruple
high neighbors of low i. The sum of nonnegative mixed slacks at i is

    D_i=a_i+sum_(j in N_L(i))a_j-s_i+p_i+2f_i.          (1)

Indeed its caps sum `90-2(9-a_i)`, while its two-walk count is
`sum_(x in N_H(i))(10-t_x)+sum_(j in N_L(i))(9-a_j)`.
Substituting `sum_(x in N_H(i))t_x=2(9-a_i)-s_i+p_i+2f_i`
proves(1). This local identity refines the mixed-slack mechanism of9199.
At an isolated low the nine red mixed slacks sum the odd nonnegative
integer `27-2e(N_R(i))>=1`. Hence

    p_i+2f_i>=s_i+1 for every isolated low.            (2)

If q=1, L has two isolated points and n3=n4=0. Equation(1) gives
`D_i=-s_i<=0` there, contradicting(2). This excludes the first sector
without a finite host enumeration.

In the quadruple sector let u,v be the singleton highs and w the quadruple.
Writing Q=G[H], independent lows give, for every high x,

    sum_i c_R(i,x)=2d_Q(x)+2*1_(xw red)-1_(xu red)-1_(xv red).

Its mixed caps sum `2d_Q(x)`, so `2*1_(xw red)<=1_(xu red)+1_(xv red)`.
At x=u orv the absence of self loops forces uw and vw blue. All six high
neighbors of w are then red to both u,v. The blue uw spine has these six
common high red neighbors and the low singleton mark of u, at least seven
common red neighbors. Both endpoints have degree ten, so its blue codegree
equals its red codegree, contradicting6. No distinctness of the singleton
marks is assumed in this preliminary argument.

## 2. Six labeled incidence profiles in the remaining sector

Now `q=0,n1=2,n2=14,n3=2,n4=0`. The exact mixed identity of9199,
rederived by summing(1), gives `D=2n3+6n4+sum_i a_i^2=4`.
The four odd red slack sums are each at least one; all mixed slacks are
nonnegative. Thus each red sum is one and every blue mixed slack is zero.
Equation(1) gives `p_i=s_i+1` at every low.

The two triple points imply p_i<=2, so singleton marks are distinct; name
them A,B and the other lows C,D. Both triples contain A,B, and one contains
C and the other D. Their types areABC,ABD. Low degree margins force

    xAB=r, xCD=r+2, xAC=xBD=s, xAD=xBC=t, r+s+t=6.

Each blue low pair has at most four common red high neighbors. TheAB pair
already sees both triples, whileAC/AD/BC/BD each sees one. Therefore
`0<=r<=2,0<=s,t<=3`. The complete labeled triples are

    (0,3,3),(1,2,3),(1,3,2),(2,1,3),(2,2,2),(2,3,1).

Relabel L to name its singleton/triple marks; include all six profiles.
This is coordinate coverage, not a symmetry assumption about an unknown
host. `verify.py` independently starts with all5^6 bounded pair-count
vectors and recovers exactly these six from all actual degree/page margins.

For each profile order high points as singletonA, singletonB, tripleABC,
tripleABD, then the pair typesAB,AC,AD,BC,BD,CD in that order. Points in a
fixed type receive consecutive labels. Low labels A..D are bits0..3;
high labels0..17 become physical points4..21 in the independent checker.

## 3. Exceptional-spine symmetry and complete82-template coverage

At each low i exactly one red mixed spine has codegree2, all its other
red spines have3, and every blue mixed spine has red codegree5. Denote its
exceptional high neighbor by x_i. Let M be the4x18 incidence matrix, Q the
symmetric18x18 high adjacency matrix, and E have one1 in each row at x_i.
Then

    M Q=5J-2M-E.

Multiplying by M^T makes `45J-2MM^T-EM^T` symmetric. Therefore `EM^T`
is symmetric: `j in T_(x_i)` iff `i in T_(x_j)`. Its diagonal is one.

The producer exhausts all possible four-type words obeying this symmetry.
For repeated exception types it uses restricted-growth labels: first
appearance0, next either an earlier label or the next unused label, never
exceeding the actual multiplicity of that type. This represents every
repetition/distinctness pattern once. Any actual exception tuple transports
to such a word by a permutation within each identical incidence type,
fixing all low marks/global degrees; unused points extend that permutation.
No automorphism of the host is asserted or required.

The independent checker instead exhausts all `9^4=6561` actual exception
tuples per profile, tests the actual symmetric matrix entries, and normalizes
by first occurrence within each type. Its entire canonical tuple set equals
the producer set, not just its size. Profile counts are

    12,14,14,13,16,13, total82.

## 4. Complete initial star domains and literal pair constraints

For high x with low type T_x, its high red star S_x is a subset of
`H minus{x}` of cardinality `10-|T_x|`. Each mixed red intersection with
M_i is3, except2 if x=x_i; each mixed blue intersection is5. Enumerate
every star satisfying these equalities to form its initial domain.

The producer directly checks all appropriate subsets of17 points,
427,856 subsets per profile,2,567,136 in total. The independent checker
instead enumerates all bounded type-count vectors satisfying the degree
and four incidence demands, then expands every labeled choice in each
type. Each subset has a unique such vector, so neither algorithm's
coverage depends on a catalogue or sampled star list. The checker builds
physical22-point red and complement endpoint rows and counts actual third
vertices on all four mixed spines. Its blue comparisons use actual blue
intersections, independently of the producer's red-codegree conversion.

Two candidate high stars must have reciprocal edge membership. On a red
xy they require `|S_x intersect S_y|+|T_x intersect T_y|<=3`; on a blue
xy the same sum is at most6. The latter uses both global degrees ten.
The independent checker counts the colored pages using actual physical
red/complement endpoint rows, excluding the diagonal and both endpoints
as appropriate. It does not import the producer or its domains.

There is one additional ordinary necessary red-pair cut. In any red K4 C,
each of the six internal spines already has two pages, hence
`sum_(z outside C)binom(d_C(z),2)<=6`. For0<=t<=4,
`t<=1+binom(t,2)`, so the four global degrees sum to at most
`12+18+6=36`. A red K4 with one low9 and three high10 vertices would have
sum39 and is impossible. Consequently a red high pair cannot have a common
high neighbor sharing any of its common low marks. This cut uses prescribed
actual global tags, not unspecified degrees in a partially filled control.

Every genuine completion supplies a star in every complete initial domain
and satisfies these pair constraints. That necessary implication is the
finite completeness bridge. No equality/regularity is assumed for the
unfilled high graph beyond the proved exact-two hypotheses.

## 5. Compact complete deletion certificate

`certificate.json` covers each of the82 exact templates once. Twenty-four
have an initially empty domain. Forty-eight have a static cover: only one
target domain is changed, and each removed star lacks support in a complete
initial other domain. Ten require sequential deletions from several domains.
The latter are **arc-deletion certificates**, not static covers or a solver
status. The complete record contains1,104 batches removing28,840 stars.

Each batch gives target x, other y and a positive deletion count. Starting
with all complete initial domains, the verifier exhausts the current x
domain and every current y support, derives the ENTIRE unsupported set,
checks its cardinality and removes exactly that set. It checks the entire
ordered deletion-record fingerprint and the final actual empty domain.
The certificate stores no trusted reduced domains. Each deletion is valid
by induction: a completion's actual stars survive every earlier deletion,
so a star lacking any remaining compatible support cannot occur. The
certified empty domain is therefore a contradiction.

Initial domain sizes/fingerprints and ordered deletion fingerprints are
integrity records, not substitutes for regeneration and coverage. In
author validation the producer and different checker also emit every
initial star and every ordered deleted star; their full records are
compared bytewise. The bulky generated record stays private and can be
regenerated with `--domains`; it is not needed as an external proof input.

The compact certificate has37,763bytes. Its canonical mathematical SHA256 is
`784b3a5c03b929b91077e96b4dbb6b9a639935fa2b3e690723baf66365561047`.
The frozen expected summary is recorded after the separate verifier agrees,
before final source replays. Neither program's correctness depends on
Python `assert`; all mathematical/data guards remain active under `-O`.

## 6. Imports, reproducibility and novelty boundary

The earlier9199 source is
`79e11775f4b18c936da503d8b89d9edc8370f5fb`, artifact
`bafkreibzaet27tim76q7mvvbbl52vkq5m2aua47kcmbadaexl3hyutkhyq`.
Its lower-two conclusion turns the new exact-two exclusion into lower-three.
The newly committed
[9255 independent two-root audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/two-root-parity-audit/REVIEW.md),
source `8859cf8b1f7abd6ccaef9c7727d448f7fef680e7`, confirms9199 with
its inherited premises retained. It also proves the weaker mixed-cap
two-root core and the necessary exact-two/two-triple conditions. Its two
preliminary sector cuts overlap Section1; it explicitly credits this
author's earlier private1512 report before its ordinary rederivation.
That published overlap is credited here, with no exclusive priority claim.
The full committed review and published proof were read before the new
graph claim; no reviewer executable replay is claimed. Its verdict does
not cover these82 exception templates, their completion certificates or
the lower-three consequence.

The universal108 implication also retains9102, source
`4674720842bee9238370fd4a6543c10da96b510b`, artifact
`bafkreibzlgnf7ax5w3vyzvmmpaa7u6piryckdtavqizpmrphjbl235abai`.
Its8828/8941/8979/9041 predecessors and ONLY8012's upper-degree-ten
statement retain their exact boundaries. The new certificate does not
replay or assign verdicts to those different computations.

The complete
[9191 independent audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/four-nine-root-audit/REVIEW.md),
source `56661bedd38a71138c1b38e6d95de2f8c30445d1`, confirms9102's new
four-nine core and its conditional combined implication. Its removal of
outside blue caps is not imported here, and its verdict does not assess
this exact-two theorem. The8987 three-low count, source
`a9ea2d82e36068ce6b4731a4185f8e5157048192`, keeps its known lower-seven
status. Standard counting, parity and endpoint identities are prior work.

Current primary
[Lidicky--McKinley--Pfender--Van Overberghe Table1](https://arxiv.org/pdf/2407.07285)
and [Radziszowski revision18 TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
were rechecked2026-10-02 and retain the located interval22..23.
`baseline.py` replays the freshly fetched
[authors' primary21 matrix](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt),
all210 spines,93 red/117 blue edges and page maxima3/6. Its full raw bytes,
including appended search metadata, have SHA256
`3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
This is prior-art validation. The primary upper23 flag certificate is not
replayed. Bounded novelty searches do not establish exclusive priority.

The complete current
[9197 degree-nine cycle source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/degree9_cycle_saturation/PROOF.md),
source `266d4715935381ce0aeb9386ad966364e0797f6d`, was read as complementary
scope. Its specified leaf and cycle degree-tag hypotheses do not
automatically hold here; none of its leaf reductions is a premise. The
new increment is the ordinary local slack/exception symmetry bridge and
the complete necessary exact-two completion exclusion. No generic cubic
graph census or older construction is declared new.

The fresh
[9247 cycle audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/degree-nine-audit/REVIEW.md),
source `c10bc7c39e7808fb9f08bda535c5e9ab41f60193`, confirms9197 and
removes global maximum ten from its specified-leaf deficiency conclusions.
Its13 necessary near-equality histograms concern those induced cycles;
they do not replace the actual four-low incidence/exception domains here.
Its complete committed body and published review were read as context,
with no new executable replay or verdict on this exact-two theorem claimed.

CPython3.12.14, standard library only, exact unbounded integers and finite
sets/bit rows. See [README.md](README.md) for deterministic commands and
[provenance.json](provenance.json) for final serial measurements, source
identities, damage controls and full-record hashes. One CPU-intensive child
at a time, six native thread variables1, unchanged1CPU/2GiB scope and fixed
45-second mathematical guards. Timeout, UNKNOWN, incomplete enumeration or
memory failure would be an operational limit, never nonexistence evidence.
All ten final modes passed;19 damaged certificates reject in both normal
and optimized modes. The largest child took15.645 seconds; cumulative peak
math-child RSS was33,432KiB. The full2,597,741-byte domain/deletion record
has SHA256 `a96d9587b8de30653a02ffd94a847475343eef8ee2e7abdb468c330aab285586`.

The next actual completion frontier has at least three forced one-nine
roots with consistent global low tags. Equality-three sectors require new
slack/exception coverage; the82-template census does not transfer unchanged.
Stronger counts, host occurrence, unrestricted108 exclusion and the Ramsey
endpoint remain open in this packet. Independent review and formalization
of the new theorem are pending.
