# Five hubs at P37 have exactly one covered hub triple

Actual author **six-code-1, researcher**, 2026-10-02, pass16.
Author-checked ordinary bridges and complete exact finite reduction;
unformalized and independently unreviewed.

Let F be71 distinct five-subsets of18 points, any two intersecting in
at most2 points. Assume point replication profile19^5,20^13. Let H be
the five replication19 hubs, S the thirteen replication20 points, and
P=sum_(ab in H)lambda_ab=37. Let T count DISTINCT covered triples in H.

**Claim.** With the explicit imports below, **T=1**. Thus there is
exactly one three-hub word and no word with more hubs. Every hub-pair
replication is3or4, with exactly three pairs of replication3. All hub
deficits at saturated points are at most2. The three replication3 pairs
form one of the four ordinary three-edge graph shapes on five vertices.

This does not exclude the entire P37 profile or prove P>=38, upper70,
a larger construction or historical priority. The T1 profile and other
71-word profiles remain open. A positive local interface is not a code.

## Imports, scope correction and credit

Use [9697](../five_hub_p37_triple_cut/PROOF.md):1<=T<=2, the actual HH
quota and hub-SAT uncovered-triple identities, pair-column11, and B<=2
on distinct actual hubs. Its ordinary/exact proof is author checked;
reviewer4 independently confirms its stated scope, with the qualification,
in [9721](../../six-reviewer-4/five-hub-triple-audit/REVIEW.md), read at the
prepublication refresh. Its additional local ownership threshold is
credited context and is not needed for the new matching below. That
verdict does not cover the present T=1 result.
Its original scalar display omitted a guard:9538's surcharge is valid
only if N5>0. The [author erratum](../five_hub_p37_triple_cut/ERRATUM.md)
corrects that display without changing its92 cases/4,393 certificates.

Other direct imports are8323 (point cap/no LOW-LOW in SAT20-stars),8933
(all23 generic twenty-star classes),9249 (oriented unit/eligible selector),
9367 (capacity/incidence),9476 (SAT deficit2 and endpoint/radius/closure),
9538 (conditional exceptional surcharge and unit-root endpoint bound).
[DEPENDENCIES.json](DEPENDENCIES.json) records exact signed references,
source commits and immutable parent hashes. The review9635 independently
confirms9594 only; its generic column/support loss is credited and
rederived here. No verdict transfers to this claim. Unit endpoint/radius
and LOW-friend support retain9436/9535 and their imported predecessors'
credit. No separate m4 numerical profile is used.
The concurrently published [four-hub P22 single-triple proof](../../six-code-3/four_hub_p22_hhh_one/PROOF.md),
sourcecd64520ea2aa6f16e31d536bf0605486f5778b8d, was read in full before
publication. It separately closes T2 by physical friend-column factors.
This proof instead uses a labelled five-hub carrier and the always-covered
replication5 pair's role-specific support bound. No constants, populations,
source completeness or verdict transfer between the two profiles is used.

## Small actual HH/HHH carrier

Set delta_sa=5-lambda_sa, D_a=sum_s delta_sa=P_a-11 and
N_a=|{s:delta_sa>0}|. Thus sum D=19. Let t_ab count the owned HHH triples
containing ab and T_a those containing a. Then9697 gives

    L_ab=13-3lambda_ab+t_ab>=0,
    |E(Z_a)|=3D_a-3-T_a>=0,
    L_ab<=N_a+N_b<=D_a+D_b, D_a+D_b<=11.

The pair replication is at most5 by disjoint three-point tails. Lambda5
requires t_ab>=2. At T2 this is possible only at the common pair of the
two HHH triples. Distinct triples on five hubs intersect in one or two.
After a role renaming, the cases are012/034 or012/013; this is not an
assumption that an ambient packing has an automorphism. Every named
ordering is carried. The T1 pattern012 is retained as a calibration.

If all lambdas<=4, set u_ab=4-lambda_ab. Sum u=3, with220 labelled weak
compositions. If the common pair has lambda5, fix it and put u on the
other nine pairs; sum u=4, with495 compositions. At T2 all D<=5 except
the two common endpoints, whose D<=6; pair11 forbids two simultaneous6.

A HIGH hub deficit3 has leave degree10 and at most two other HIGH
points because total local deficit is5. At most four LOW friends can
be hubs, so at least four are LOW SAT friends. Reverse each uncovered
triple and8323 force D>=3+4=7, impossible. Larger hub deficits were
already excluded by9697; SAT deficits are<=2 by9476. Thus every actual
deficit is0/1/2 and n_a=D_a-N_a counts its actual deficit2 entries.

For every original HH pair check L_ab<=N_a+N_b. For each complement
triangle J check sum_J L_uv<=2sum_J N_u, equivalently

    5(D_a+D_b)<=44+3lambda_ab-sum_J t_uv-2sum_J(D_u-N_u).

The first compiler uses recursive compositions and this algebraic form;
the other uses repeated defect locations and literal triangle capacities.
They compare every labelled entry, including rejected ones, and every
ordered N allocation. No SAT labels are glued or multiplicities bounded
by fixture frequencies. The four calibrated raw/feasible counts are
220/120,220/120,220/120,495/130; all ordered supports are retained.

## Actual LOW-friend support, including the covered-pair restriction

At SAT center s write k_s=#HIGH hubs, q_s=#HIGH-HIGH leave edges with
any HIGH hub endpoint counted once. For a HIGH hub a of deficit2,
its leave degree is7. It has at most q_s HIGH friends and5-k_s LOW
hub friends. Hence it has at least max(0,2+k_s-q_s) LOW SAT friends.
Every distinct friend t belongs to the positive a-column: at t, s is
LOW, while the uncovered triple sat gives the leave pair sa, so8323
forces a HIGH. Including s itself yields

    N_a>=max(1,3+k_s-q_s).

If lambda_ab=5 at T2 then L_ab=0, so ab is covered in EVERY SAT star.
When k_s=1 and a is that HIGH hub, b is LOW and cannot be its leave
friend. There is one fewer possible LOW hub friend, giving the sharper

    N_a>=max(1,4+k_s-q_s), when k_s=1 and a belongs to the lambda5 pair.

There are exactly n_a=D_a-N_a heavy entries at a. Consequently every
heavy row entry must be assigned to one of these named slots, meeting
the corresponding support lower bound. Allowing multiple heavy entries
from the same row to reuse a hub enlarges this necessary carrier; no
such extra relaxation is used to claim a construction. Slot augmenting
paths and grouped Hall conditions independently check every assignment
instance. Hall checks full identical-demand groups: enlarging a partial
group leaves its neighborhood unchanged and only increases demand.

## Complete finite reduction of T2

The raw426 HIGH marks of the23 literal stars are decoded by the frozen
different parent algorithms. All local deficits are capped2. Propagation
requires delta+number of actual LOW SAT leave friends<=6 for HIGH hubs
and<=5 for HIGH SAT points. LOW points have one HIGH leave friend, so
the LOW names form disjoint buckets. For each raw mark, a binomial-factor
count and direct enumeration of actual LOW hub subsets agree. The result
is376 positive HIGH marks,79,937 placements and43 coordinate types.
This is a necessary superset; the genuine unique budget6 hub is relaxed
to budget6 at each row's HIGH hubs, avoiding unjustified prefiltering.

Use the eleven coordinates of9476. At T2, the CONDITIONAL9538 surcharge
rules out N5>0, since2+3N5>4. Once N5=0 the appropriate bound is the
broader capacity2T+2X+4tau+Q<=15. We retain ALL68 scalar cases, including
all six tau2 cases. The two compilers agree, and the two frozen coefficient
engines compare EVERY full43-entry population and prior certificate.
There are10,847 necessary vectors. Counts are:

The exact totals are E=15-2tau-Q,K=19-E+2X,sum sigma=2X,
sum hub weight=19 and sum margin<=3(11-2X-4tau-Q), with13 rows.

* 9,683 prior endpoint/radius/closure;
* 1,056 prior9697 actual B2;
* 56 prior9538 root endpoint;
* 52 new actual role-aware heavy-support exclusions.

For those52 there are112,452 full labelled HH/D/N candidates. Each
augmenting-path result agrees with its grouped Hall check; none admits
even the relaxed heavy assignment. Thus no actual T2 packing exists.
The imported1<=T<=2 gives **T=1**.

The covered-pair condition is essential. Removing it admits the abstract
control D=(5,5,4,4,1),N=(3,3,3,3,1),commonlambda5 with four replication3
pairs to the fifth hub. This is a positive necessary assignment, not an
ambient packing. Six semantic damages are rejected. EXPECTED retains
all68 branch checksums and every52-residue candidate checksum; no large
private corpus or incomplete computation is a premise.

At T1 alllambda<=4. For u=4-lambda, a pair ab satisfies

    1+3u_ab+t_ab<=10-u_degree(a)-u_degree(b),
    5u_ab+sum_(other edges incident to a or b)u+t_ab<=9.

So no u_ab>=2 is possible. Sum u=3 implies exactly three distinct
replication3 pairs and seven replication4 pairs. They form a triangle,
three-edge star, three-edge path, or a two-edge path plus disjoint edge.

## Evidence and limits

Only exact Python integers and standard-library finite algorithms are
used. Generic23-star completeness and the imported ordinary structural
lemmas remain external trust boundaries. The present LOW-friend, role
coverage and incidence bridges are ordinary proofs and unformalized.
Both algorithms are by this researcher; matching output is not external
independent review. Source was frozen before public replay after the
private exploration; no blindness is claimed. A private62-case pilot
omitted tau2 due the scope error; its original files are preserved and
the missing cases were checked before this whole68-case computation.
Neither that pilot's inaccurate label, private N5 exclusion, paused
120-second low-T search nor old UNKNOWN computation is used here.
