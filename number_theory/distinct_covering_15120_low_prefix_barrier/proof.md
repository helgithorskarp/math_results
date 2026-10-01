# An 84-hole obstruction requiring two changes below modulus360

Actual author **six-covering-1**, role **researcher**, 2026-10-01.
Status: written computer-assisted conditional lemma, with complete exact
author checks. Independent review and formalization are pending.

Let N=15120 and D={m:m divides N, m>=8}. The file `seed.tsv` gives one
phase s_m for every m in D, in rows `phase modulus`.
There are73 distinct labels, their minimum is exactly8, and their actual
LCM is N. This assignment has84 uncovered residues modulo N. It is a
near-cover. Let A={m in D:m<360}; |A|=48. The other25 labels form B.

**Lemma.** Among all completed assignments which differ from s_m at at
most one label of A, with completely arbitrary phases at every label
of B, the minimum number of uncovered residues modulo N is exactly84.

**Corollary.** A distinct covering with all moduli dividing N and at
least8 cannot contain47 or more of the48 seed prescriptions indexed
by A. In particular every completed covering selects at most46 of
these48 prescribed phases. This does not exclude the entire period N
and does not improve the global bounds for L_min(8).

## Complete finite reduction

For a set F of free labels, fix every other seed class, and let R be
the ordinary residues of {0,...,N-1} not covered by these fixed classes.
For each m in F define

    H_m(a)=|{x in R:x mod m=a}|,  C_m=max_{0<=a<m} H_m(a).

If a choice of the free phases leaves at most h=83 holes, its union
on R has size at least |R|-h. Counting overlap with multiplicity only
increases size, so

    |R|-h <= sum_{m in F} H_m(a_m) <= S=sum_{m in F} C_m.

Thus |R|-S>h is an exact exclusion. Otherwise put
delta=S-|R|+h>=0. Since every deficit C_m-H_m(a_m) is nonnegative,
any feasible assignment must satisfy

    H_m(a_m) >= C_m-delta                 for every m in F.

This proves the phase pruning used below. Capacities are recomputed
literally at every node, with exact nonnegative integer arithmetic.

When R is nonempty, a zero-footprint phase at a selected free label
can be replaced by any positive-footprint phase: nothing is uncovered
outside R, where the already fixed classes cover, and nothing inside
R was covered by that zero footprint. If zero passes the displayed
threshold, the threshold is nonpositive, so the replacement passes it
as well. Consequently, for existence of an h-hole repair it suffices
to branch over every positive phase with

    H_m(a) >= max(1,C_m-delta).

For each such phase remove its footprint from R and remove m from F.
Distinctness remains intact. This reduces the number of free labels
by one. A strict capacity leaf excludes that branch. Checking every
child of every branch therefore gives a well-founded complete proof.
No claim that the retained phase choices represent a maximal symmetry
group is required; the zero-footprint replacement is a covering
domination argument. An incomplete tree proves no negative statement.

## Exhaustion of the stated neighborhood

First take F=B. Its R has419 points. The complete tree has36 nodes,
26 branches and10 strict capacity leaves. Each leaf has |R|-S>=84.
Thus fixing all48 A phases cannot leave at most83 holes.

Next, for each of the48 possible labels t in A, take F=B union {t}.
This includes every assignment which changes only that lower label;
the t phase is arbitrary, including its old value. Exact root
capacities show that40 of these cases force the old phase s_t for any
83-hole assignment. The checker tests **every** phase at t, including
zero footprints. Once t is fixed at s_t, the baseline case just proved
applies. The remaining eight cases are precisely

    t=135,140,180,189,252,270,280,315.

Their complete trees have respectively39,39,111,125,107,194,108,90 nodes.
Together with the baseline, there are849 nodes:596 branches and253
strict capacity leaves. Every leaf has |R|-S>=84. `input.json` stores
only the preorder branch modulus, its exhaustive phase list, and a
leaf marker. `check.py` independently reconstructs every physical
residual with ordinary remainders, recomputes all capacities, checks
every phase list, and requires every child and every node to be consumed.
It never assumes that a generator's reported bound is correct.

These40 root reductions and eight exhaustive trees cover all48 cases,
with the baseline covering zero lower changes. No assignment in the
lemma's stated family can leave at most83 holes. The seed itself has84
holes and lies in that family, so the minimum is exactly84.

For the corollary, suppose a covering contains at least47 A seed
prescriptions. Adjoin every missing eligible divisor at its seed phase.
Coverage and distinctness persist. The full assignment differs from
the seed at at most one A label, contradicting the lemma. When only an
ambient period is assumed, completion can increase a smaller original
actual LCM; the corollary concerns moduli dividing N. If the original
actual LCM is N, that LCM is preserved. The prescribed8 class forces
the minimum exactly8 whenever it is present.

For a construction model one may adjoin a missing9 class and translate
all phases so that8:5 and9:6 hold. CRT gives exactly one shift modulo72
for every initial pair of phases. Applying the corollary to this
normalized completed assignment gives the necessary constraint

    sum_{m in A minus {8,9}} X_(m,s_m) <= 44.

No additional phase is fixed by this argument.

## Reproduction and trust

Run Python>=3.11, standard library only, from this directory:

    python3 -B check.py --controls
    python3 -O -B check.py --controls
    python3 -B generate.py generated/input.json

The two checker runs return the same exact summary and reject12 damaged
fixtures or malformed seeds. The generator reproduces the fixture hash
in `expected.json`. It uses different bit-mask residuals; the checker
uses ordinary physical tuples and remainder histograms. A generator has
10s/5000-node limits per tree; the checker has a20s deadline. An error,
timeout or incomplete tree is not nonexistence. All jobs used one
numerical thread and at most one intensive process at a time under the
standing1CPU/2GiB limits. No floating solver output or private trace is
a premise. Compact source does not itself replace the written reduction.

The proof trusts ordinary exact Python integer arithmetic, the compact
finite fixture, and the written counting, domination and completion
arguments; these are not checked by a formal proof kernel. Independent
author representations are not independent reviewer acceptance.

Context: [Zhang--Zhang's minimum-seven paper](https://arxiv.org/html/2607.19029)
claims L_min(7)=10080, a different question. The
[pure235 covering paper](https://arxiv.org/html/2605.18644) has a separate
prime restriction. Their numerical computations are not premises here.
General residual-capacity methods are established counting arguments;
the team's weighted obstruction framework is credited to six-covering-2,
[source](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md),
source commit b9d39eb740a866e07237be1c78b834d1ab6ea718, graph7174.
The present finite seed and conditional neighborhood are six-covering-1's
construction research. No algorithmic priority or literature-absence
claim is made. Global exactly-eight candidates remain
{10080,15120,20160}, with only20160 witnessed by the team.
