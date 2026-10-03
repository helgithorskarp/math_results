# Four isolated deficit-two rows force support at least seventeen

Actual author **six-code-3**, role **researcher**, 2026-10-03.
This is an ordinary conditional author proof with two exact finite checks.
Its mathematical bridges are unformalized; independent-person review is
pending. Shared signing identity does not establish independent authorship.

## Statement and definitions

Let F consist of 71 distinct five-subsets of an eighteen-point set, any two
intersecting in at most two points. Assume its replication profile is
(18,19,19,19,20^14). Label the four unsaturated points H={0,1,2,3}, with
r_0=18 and r_1=r_2=r_3=19, and the fourteen remaining points S. Write
lambda_xy for the number of words containing x,y. Set

    P = sum_{a<b in H} lambda_ab = 23,
    T = sum_{a<b<c in H} number of words containing a,b,c = 0.

Thus no word contains three hubs. Define delta_sa=5-lambda_sa,
N_a=#{s in S: delta_sa>0}, D_a=sum_{s in S}delta_sa, and K=sum_a N_a.
The three-point tails of words through any pair are disjoint, so every
lambda_xy<=floor(16/3)=5; in particular 0<=delta_sa<=5.

Shortening at s means deleting s from every word containing it. For s in S
this gives twenty quadruples on seventeen points, with every pair in at
most one quadruple. Its **leave** is the graph of uncovered pairs. A point
x is LOW if lambda_sx=5 and HIGH otherwise. Its leave degree is
16-3lambda_sx=1+3(5-lambda_sx).

The only imported mathematical premise is the universal **no LOW--LOW
leave edge** theorem for a twenty-block shortened star, actual graph
lemma 8323, proved by six-reviewer-1 in the
[two-anchor certificate proof](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_upper71_review1/REVIEW.md).
Its source commit is 02c1569568854e575f8b176ea07d552737a7da84 and reference is
`bafkreibz6cr3e3mjpadu4jjr5n3kzwlji4ijgzbto7mw66xoqtyaa37ohe`.
This packet imports that premise; it does not recheck its certificates.

A **C row** is a saturated point s whose shortened star has exactly four
HIGH points, exactly one of them a hub a, with delta_sa=2 and a isolated
in the graph induced on HIGH points. Call a its center. This definition
does not assume completeness of any local-star inventory.

**Lemma.** Under these hypotheses, at least four C rows imply K>=17.
Equivalently, K<=16 implies at most three C rows.

## C rows and the two carriers

In a C row centered at a, the hub a has leave degree seven. Its neighbors
are LOW because it is isolated among HIGH points. Let d count its other
hub neighbors and f its saturated-point neighbors. Then d+f=7 and d<=3.
For each such saturated neighbor t, lambda_st=5, so s is LOW in the
twenty-block star at t. The leave edge sa in that star represents the same
uncovered triple {s,t,a}. The imported no LOW--LOW theorem makes a HIGH
there, hence delta_ta>0. These f friends are distinct positive entries in
column a besides s. Therefore f<=N_a-1, N_a>=5, and

    d >= max(0,8-N_a).

The other hubs are LOW in the row, so no leave edge joins two of them:
the HH leave is a star at a. If m_a of four selected C rows have center a,
their distinct positive slots also each use one unit of excess, since
delta_sa=2. Thus m_a<=min(N_a,D_a-N_a).

At T=0 a word through hubs a,b contains three saturated points. These
tails are disjoint, so lambda_ab<=4. Since P=23, exactly one pair has
lambda_ab=3 and the other five have lambda_ab=4. Incidence at each hub gives

    D_a = 70 - 4r_a + sum_{b!=a}lambda_ab.

There are L_ab=14-3lambda_ab uncovered triples {a,b,s}, s in S. Merely
relabeling the three equal degree-nineteen roles gives two carriers:

| Carrier | Pair with lambda=3 | D | L on that pair | L elsewhere |
| --- | --- | --- | --- | --- |
| A | 01 | (9,5,6,6) | 5 | 2 |
| B | 12 | (10,5,5,6) | 5 | 2 |

This relabels the hypotheses; it assumes no automorphism of F. HH leave
edges in distinct saturated rows use distinct uncovered triples and hence
have the stated capacities L_ab.

## The degree-nineteen support obstruction

Shorten at a light hub a. Its nineteen quadruples have leave G_a with
total degree 17*16-12*19=44. The 14-N_a zero-deficit saturated points have
degree one. The other N_a+3 vertices are its positive saturated points and
the other three hubs, since every HH lambda<=4. Their degree sum is
30+N_a, bounded above by

    (N_a+3)(N_a+2) + (14-N_a).

This excludes N_a=0,1. At N_a=2 the sum and bound both equal 32. Equality
forces the five HIGH vertices to induce K5 and every one of the twelve
LOW vertices to attach to them. In particular, the two positive saturated
points each give an uncovered triple with a and every other hub b.

When lambda_ab=4, these two saturated points fill the entire L_ab=2 budget.
A C row centered at b is a different saturated point: its only positive
hub column is b, so its deficit at a is zero. That C row cannot use HH
leave edge ab. The conclusion uses actual uncovered triples, not a bound
on frequencies in a local-star catalogue.

A light C center b has D_b either five or six. Its positive slot and excess
token, together with N_b>=5, force D_b=6, N_b=5. All pairs incident to b
then have lambda=4; its C row uses all three HH edges. The obstruction just
proved forces every other light hub to have N_a>=3.

For the finite checks, the same total-degree inequality at the heavy hub
has 42+N_0 on the left; it excludes N_0<=3. Thus N_0>=4, independently of
whether that column contains a selected C row.

## Four-row argument

If there are at least four C rows, select four. All preceding slot,
excess, degree and capacity bounds persist for this subfamily.

In carrier A, light hub 1 has no C row and hubs 2,3 have at most one each.
Four heavy C rows force N_0=5 by m_0<=D_0-N_0. Each then uses all three
HH edges, exceeding L_02=L_03=2. The selection therefore has either
three heavy and one light C, or two heavy and two light C.

Three heavy C force N_0<=6. N_0=5 again exceeds a capacity-two edge, so
N_0=6. The light C center has support five and both other light columns
have support at least three. Hence K>=6+5+3+3=17. With two light C
centers, even the elementary bound gives K>=5+5+5+3=18.

In carrier B only light hub 3 can carry C, and at most one. Four heavy C
would give N_0<=6 and need at least eight HH edges incident to 0, exceeding
their total capacity six. Thus the selection has three heavy C and one C
at 3. N_0=5 exceeds L_03=2. At N_0=6 the heavy rows need six incident
edges and the light C uses 03 once more. Consequently N_0>=7 and
K>=7+5+3+3=18. This proves the lemma.

## Exact finite checks and their bridge

The two programs independently reconstruct both carriers and all 5,712
integer tuples 0<=N_a<=D_a. Every tuple is paired with all 35 four-part
compositions m of four, giving 199,920 cases: 102,900 for A and 97,020
for B. Both retain the slot/excess inequalities, N>=5 at C centers, and
the degree and capacity-two column obstructions proved above.

[literal.py](literal.py) searches actual allowed HH-star assignments for
four rows. Each row needs at least d=max(0,8-N_a) distinct incident edges.
Dropping surplus edges preserves a necessary relaxation, so assigning
exactly d edges suffices here. It does not classify actual full mate sets.

[dual.py](dual.py), importing no producer, tests all 64 edge-subset cuts.
The flow network has a row of demand d, capacity one from that row to each
allowed incident edge, and edge capacity L to the sink. For an edge subset
I, row demand left after using edges outside I is
max(0,d-#{allowed edges outside I}). The sum of these quantities, with
row multiplicities m, must not exceed sum_{e in I}L_e. Minimizing cuts
over row vertices gives these inequalities; integer max-flow/min-cut
makes them sufficient for this finite relaxation.

[verify.py](verify.py) compares the entire masks and all feasible records,
rebuilds their mask indexing and validates all 39 literal positive HH-star
witnesses, every capacity and forbidden edge. The minimum relaxed K is 17.
It also checks 1,024 labelled graphs on five HIGH vertices and seven
possible LOW matching-edge counts: HIGH degree sum32 occurs only for K5
and zero LOW matching edges. This is 7,168 degree identities, not a
classification of seventeen-point shortened stars.

The K17 control N=(6,3,5,3), m=(3,0,1,0), carrier A is feasible in the
relaxation. Its K15 counterpart N=(6,2,5,2) is infeasible, and becomes
feasible when only the new column prohibition is deleted. These are
relaxation controls, not packing constructions or sharpness examples.
The verifier rejects damaged witness coverage, duplicate edges and the
actual forbidden-edge counterfactual. Whole outputs must agree between
ordinary and optimized Python; checks do not depend on assertions.

## Attribution, status and use

The prior C5, positive-support, excess and Hall/minmax methods are credited
to actual graph results 9535, 9570, 9754, 9803 and 9884. The prior
[four-hub P22 proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/four_hub_p22_exclusion/PROOF.md)
records that context. Their conclusions, the generic local classification,
and the unit/eligible theorem are not premises of this lemma. No method
priority or historical priority is claimed. Review9938 checks that earlier
P22 result; it does not review this support lemma.

The [maintained table](https://aeb.win.tue.nl/codes/Andw.html), checked live
2026-10-03, records 69--72. The campaign already has the independently
checked upper71 proof8323. The established lower construction comes from
[Aw--Chee--Ling, 2003, Theorem1/AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf);
its primary 69-word certificate was rechecked in this pass. That check is
validation, not a new lower bound. This lemma leaves the unrestricted
endpoint unchanged and does not exclude P23/T0 or assert an embedding.

The proof is ordinary and unformalized. Exact CPython integer computation
checks the declared relaxation; it does not formalize the shortening,
friend reversal, incidence, HIGH clique, role relabeling, four-row
selection or max-flow bridge. All finite checks are by the author, using
different algorithms; independent-person review remains pending. The
source-only commands and expected fingerprints are in [README.md](README.md).
Full column/mate realization, global gluing and the three-C frontier remain
unresolved. No private scalar census is a premise or delivered certificate.
