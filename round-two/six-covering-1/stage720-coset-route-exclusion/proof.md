# No period-720 stage confines all holes to an 18-coset and a 6-coset

Actual author: **six-covering-1, researcher**, 2026-10-01. This is a
computer-assisted construction-route lemma, with an unformalized counting
proof and separate same-author algorithms. No independent reviewer verdict
or historical-priority claim is made.

Let

\[
D=\{m:m\mid720,\ m\ge8\}
=\{8,9,10,12,15,16,18,20,24,30,36,40,45,48,60,72,
80,90,120,144,180,240,360,720\}.
\]

**Lemma.** For every choice of one congruence class at each original label
in D, and every a modulo 18 and c modulo 6, there is a residue modulo 720
outside both the chosen classes and

\[
U=(a\bmod18)\cup(c\bmod6).
\]

The same conclusion holds for at most one class at each label, by adjoining
arbitrary classes at omitted labels. These are original distinct resources;
reducing a class to a cofactor never produces an additional resource.
The two allowed-hole cosets U describe a target set, not extra distinct
covering resources.

This closes the specified first-stage route toward a minimum-exactly-eight
cover at 15120: the 24 labels dividing720 cannot leave all holes inside one
18-coset and one6-coset, even if the 29 labels 7d, d|720, d>=2 would cover only
the **actual** holes outside the18-coset. Their ability to cover that partial
set is not a premise of this exclusion. This does not exclude arbitrary
15120 coverings, provide a new covering, or improve a global L_min(8) bound.

**Normalization and the credited finite reduction.** A translation s with

\[
s\equiv5-a_8\pmod8,\qquad s\equiv6-a_9\pmod9
\]

exists by coprimality and sends the two chosen classes to8:5 and9:6.
It also sends every other original class and both target cosets to classes
of the same modulus. Thus these fixed phases lose no generality.

The earlier [twelve-shape reduction](../stage720-six-orbit-reduction/proof.md),
source commit `c87f46d672552ca570cd7bc0293969a4e3688c17`, graph
`bafkreibhwbabvc6mqjab3riotqp33y52r73wffazskkh7rcpbhwadaz76m`
(9049, transaction index1), proves that H subset U requires one of twelve
target pairs. Its 96 exclusions and the 102-hole lower bound are imported
proof premises. They are not claimed to be new or rederived by this checker.
The pinned prior certificate has SHA256
`99c433aad2c1f5a6d7246fb619efef9b387de021ddeccac8fe4d4bd59d96cbf2`.

The six representatives are

\[
(0,2),(0,4),(3,1),(3,2),(3,4),(3,5).
\]

The affine map x ->17x+48 modulo 720 preserves8:5 and9:6 and sends these,
respectively, to

\[
(12,4),(12,2),(9,5),(9,4),(9,2),(9,1).
\]

Because17 is a unit modulo 720, the map permutes every original congruence
family. It suffices to exclude the six representatives. Both checkers
test all 2397 original phase images, the six literal target-set images,
and all 72 possible8/9-anchor translations.

**Consume a phase before bounding the remaining resources.** First fix
the actual phase b of ORIGINAL 12. Remove that label from the free pool and
remove its entire literal class from the points that still need coverage:

\[
R=\mathbb Z/720\mathbb Z\setminus
\bigl((5\bmod8)\cup(6\bmod9)\cup U\cup(b\bmod12)\bigr).
\]

There are 21 remaining original labels. For six prefixes that survive this
bound, additionally fix the actual phase f of ORIGINAL 16, remove its label,
and delete its literal class from R. There are then 20 remaining labels.
The resource 12 or 16 is never reused in the bound. This phase conditioning
is why the old nonstrict root envelopes need not stay nonstrict.

For each R partition the points into its odd and even sets O,E. Reserve
the 12 lowest remaining labels as a low pool S; the other 9 or 8 labels form
a high pool T. For each original phase of m record its actual counts on
O,E. For each distinct pair i,j in S enumerate EVERY i*j pair of original
phases and record the counts of their actual union, with overlaps counted
once. These profiles use physical720-point progressions; no floating-point
optimizer or solver status enters the proof.

**The count-threshold induction.** For the high pool let B_empty(t) be
the maximum SUM of even counts over high phase choices whose SUM of odd
counts is at least t. If there is no such choice the value is undefined.
These sums are upper bounds for unions, not claims of attainable joint
coverage. For a nonempty even-sized low pool S, take its lowest label i and
define

\[
B_S(t)=\min_{j\in S\setminus\{i\}}
\max_{(o,e)\in P_{ij}}
\left[e+B_{S\setminus\{i,j\}}(\max(0,t-o))\right].
\]

Undefined children are omitted from the maximum. If any partner j has no
defined candidate, the parent is undefined. P_ij is the complete actual
pair-union profile list, optionally with coordinatewise dominated profiles
removed.

For every placement of the remaining resources, if their odd union covers
at least t points, their even union has at most B_S(t) points. At S empty,
actual odd union <= summed odd counts and actual even union <= summed even
counts. For the induction, let the actual i,j phases have profile(o,e).
The remaining odd union is at least max(0,t-o), since the whole odd union is
at most o plus that remaining union. Apply the child bound; the whole even
union is at most e plus its remaining even union. Maximizing over phase
pairs bounds every actual placement, and every choice of partner j gives
a valid bound, so their minimum does too. An undefined value means the odd
threshold is provably unattainable in this relaxation, not that a computation
timed out.

Each B_S is nonincreasing in t. Therefore increasing either coordinate of
a profile cannot reduce its candidate upper bound, justifying removal of
dominated profiles. The production checker also stops a count state when
t exceeds the sum of all remaining singleton maximum odd counts; this is
the elementary union bound. The separate audit uses tuple resource pools,
physical sets and a differently pruned high-pool state table without this
early-stop optimization.

Coverage of R would require both its |O| odd points and its |E| even points.
Hence undefined B_S(|O|), or B_S(|O|)<|E|, excludes that actual prefix.
All computed bounds in this artifact are defined integers.

**Complete phase split.** The [certificate](certificate.json) records all 72
representative/original 12 cases as
`[a18,c6,b12,odd_demand,even_demand,even_upper]`. Exactly 66 are strict.
The six nonstrict parents are

\[
(0,2;12{:}4),(0,2;12{:}10),(0,2;12{:}11),
(0,4;12{:}2),(0,4;12{:}7),(0,4;12{:}8).
\]

All sixteen ORIGINAL 16 phases at EACH of these parents are enumerated.
Every one of the 96 children is strict. They are stored as
`[a18,c6,b12,f16,odd_demand,even_demand,even_upper]`.
There are 162 strict leaves in 168 evaluated prefixes, and the smallest
strict integer gap is 2. For example, at(0,2;12:4;16:1), R has 200 odd points
and 100 even points, while the remaining 20 original labels have an even
upper bound 98 conditional on covering those200 odd points.

The complete profiles enumerate 11724888 original pair-phase combinations.
Every original 12 choice either reaches a strict first leaf or reaches a
parent whose EVERY original 16 choice reaches a strict child. Thus every
phase placement at each representative is excluded. Affine transfer and
the credited96 earlier exclusions cover all 108 target pairs after
normalization. Translation proves the unrestricted-phase lemma. The search
does not enumerate all full24-label assignments and does not need to: the
written upper-bound induction and the complete12/16 phase split give the
justified reduction.

**Checks and context.** Standard-library `check.py` uses bit sets and
integer count states; `audit.py` imports no production code and reconstructs
physical sets and tuple-pool recurrences. Both compare with a summary frozen
before their public comparison runs. `controls.py` rejects twelve semantic
damages, including retention of consumed resources and omitted phase branches.
See [README](README.md) and [manifest](manifest.json) for actual runs. This
is same-author algorithm independence, not independent peer review or a
formal proof kernel. An interrupted run establishes no exclusion.

Union budgets and weighted resource capacities are credited methods; see
[7174](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_residual_weight_duals).
The [8973 whole-coset obstruction](../seven-lift-coset-obstruction/proof.md)
previously excluded the route when the seven labels must cover a WHOLE 6-coset.
The present lemma instead excludes this 720 first stage even with a proper
6-coset hole subset. The separate [9065 original parity lemma](../../six-covering-2/ten-twelve-parity/proof.md)
concerns10080 and leaves 13 open five-class forms; it is context, not a proof
premise here. The campaign frontier10080/15120/20160 is unchanged, with only
20160 witnessed and minimum-exactly-eight kept separate from at-least-eight.

Primary literature checked live 2026-10-01:
[Zhang–Zhang](https://arxiv.org/html/2607.19029) claims L_min(7)=10080 using
numerical final exclusions; [Harrington–Klein–Lowrance–Trifonov](https://arxiv.org/html/2605.18644)
treats restricted 2,3,5 support and gives a minimum-eight 172800 construction.
Their numerical conclusions are not premises of this conditional lemma.
