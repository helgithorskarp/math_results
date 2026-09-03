# Independent audit of the Dean-5 Type-II carrier interfaces

This directory supports a scoped review of the saturated-path carrier chain
in Sections 10.2--10.8 and Propositions B.6--B.8 of Elias Botsford,
*Cycles of length divisible by five in graphs of minimum degree five*,
version 1.0.1 (<https://doi.org/10.5281/zenodo.22182448>).

## Verdict and scope

**The saturated `(3-connected exterior, eta=2)` closure and its universal
graph-to-interface maps are verified with high confidence.**  I reconstructed
the paper proof from the versioned TeX, checked every rooted-path hypothesis,
path/cycle simplicity assertion, contraction lift, arbitrary cap-intersection
case, and finite-state coverage step, reran the complete version-1.0.1
supplement suite, and independently recomputed the central algebraic
reductions with `verify_carrier_algebra.py`.  No gap was found in this chain.

This does not verify the whole paper.  It assumes the normalized Type-II
state and the earlier structural reduction to the saturated phase.  It does
not independently settle the bipartite tetragonal-core census, the Type-I
branch, or every earlier connected/disconnected Type-II case.

## Reconstructed graph-to-interface chain

The input is the induced path

```text
p0-p1-p2-p3-p4 = u-a-m-b-v
```

inside the normalized Type-II graph `H`, with exterior `C=H-V(P)` and no
simple `p0`--`p4` path of residue 3 modulo 5.

1. The proof that `C` is 2-connected is sound.  If `M-{u,v}` had a cut,
   opposite rooted lobes would each provide two residues; the exact internal
   alphabet `024` makes the two same-side cycle constraints inconsistent.
   Adding the surviving part of the shortest odd cycle preserves
   2-connectivity and leaves at least three `C`-neighbors at every `p_i`.
2. The only multicontact types are `02,04,24,024`; a `13` contact is excluded
   by the one-foot law or inducedness.  Each of `A1,A3` consists of at least
   three distinct exact singleton contacts.  Applying Li--Zhan to the four
   adjacent-root hosts gives the exhaustive alternative: three cubic centers
   of exact types `02,04,24`, or a degree-two aligned center of type `024`.
3. The selected-carrier lemma is a valid consequence of the stated
   Watkins--Mesner decomposition.  In its three decomposition cases, row
   fans and minimal column trees give three actual paths with pairwise
   disjoint open interiors.  No virtual edge or positive residue-zero path
   is collapsed to a literal equality.
4. In the cubic alternative, the Watkins--Mesner coordinate system has only
   the two complementary constant solutions.  The odd-singleton fan argument
   rules those out if the centers have no common cycle.  On a common cycle,
   all center paths have residues in `02`, forcing the positive sector word
   `200`.  An on-carrier odd singleton lies strictly inside its residue-two
   sector and splits it as `1+1`.
5. An arbitrary off-carrier odd singleton maps to the raw-cap state by
   truncating a 2-fan at its first carrier visits.  This retains terminal
   equality, both orders in one sector, every different-sector order, all
   positive section residues, both fan-arm residues, and every terminal/type
   assignment.  Omitting unused graph edges only enlarges the finite state.
6. Two independently chosen caps need not be disjoint.  The paper's
   specified-marked-path splice and complete two-cap topology correctly turn
   every intersection pattern into either a serial marked path or two
   internally disjoint marked branches.  On each side the nearest carrier
   interface is exactly private, a literal shared landing, or a positive
   common tail.  The nine ordered side pairs cover all cases, including
   carrier re-entry and positive paths of residue zero.
7. With four distinct private landings the three cyclic orders are disjoint,
   nested, and alternating.  Version 1.0.1 explicitly includes all 216
   alternating records.  Shared landings, a two-source serial cap, one
   on-carrier source, one positive common tail, and the positive/trivial
   parallel-tail cases match the remaining B.6 generators.  If two sources
   lie serially on one cap, the unique surviving row for their common landing
   phases forces the intervening positive segment to have residue zero; the
   checker below verifies this normalization directly.
8. In the aligned alternative, the analogous Watkins--Mesner coordinate
   system has no survivor, so every aligned triple has a `110` carrier.
   Removing the degree-two center gives a zero-residue pole path through each
   selected even/odd pair.  Literal block switching shows that at most one
   block can change this residue.  B.7 then excludes a second degree-two
   `024` center.
9. Contracting `p0p4` in `H+p0p4` and deleting the root edge at the aligned
   center meets the Gao--Li--Ma--Xie degree-sum hypotheses: degree-four
   nonroots are independent, so each nonroot edge has degree sum at least
   nine.  Endpoint restoration is simple even for a common neighbor.  The
   only returned row is `1,3,0`, after which Chiba--Ota--Yamashita forces two
   degree-five common neighbors of exact type `04`.
10. Those two `04` centers and the `024` center again have a positive `200`
    carrier.  The B.8 one-cap generator retains every carrier location,
    equality/order, positive section, center placement, source type, and arm
    residue.  For two surviving caps, the same universal topology maps to
    one of the 13 weak landing orders, a serial record, a one-common-tail
    record, or a positive/trivial parallel-tail record.  Every finite
    forbidden object expands along paths with disjoint open interiors, hence
    remains a simple object in the original graph.

The counting conclusion is then legitimate: B.6 and B.8 each allow at most
one odd singleton on the carrier and at most one off it, whereas the disjoint
classes `A1,A3` contain at least six vertices.

## Independent algebra checker

Requirements: Python 3.10 or newer; no third-party packages.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_carrier_algebra.py
```

Expected output:

```text
PASS Dean-5 Type-II carrier algebra
phase table survivors: 6
cubic Watkins-Mesner coordinate survivors: 2
aligned Watkins-Mesner coordinate survivors: 0
internally admissible one-cap tuples: 8 of 625
serial normalized rows: 3; every middle residue is 0
weak landing orders: 13
```

The checker is clean-room standard-library code.  It directly evaluates the
path-exclusion formula behind Table (9.5), all `5^6` coordinate assignments
for the cubic and aligned Watkins--Mesner systems, all `5^4` reduced one-cap
tuples using independent simple-path/cycle enumeration, every serial-source
decomposition of the three surviving landing-phase rows, and every ordered
partition defining the 13 weak landing orders.  It imports no supplement code
or certificate data.

## Supplement replay and trust boundary

The computational supplement is version 1.0.1 at
<https://doi.org/10.5281/zenodo.22167084>.  Its ZIP had SHA-256
`75b604acc53a38622e0fffddebcb27e3e883f5836d7da7e7ddb45c8378eebed5`,
and all distributed files passed `MANIFEST_SHA256.txt`.  A clean replay of
the complete 47-invocation verification/dependency list also passed.  This
replay is supporting evidence for the finite predicates only; the graph maps
above were audited separately.

The reviewed TeX and PDF had SHA-256 values
`5e06b1e307b0b48c463bddf2880fdb3e9185e9b51f2740f5057e3f14e7aad7e2` and
`abc41317fa70bc781b4b714b2ecf980eeeaf703a3e013aba25641a0779821f18`,
respectively.  The audit treats the cited rooted-path theorems and
Watkins--Mesner theorem as imported results, after checking their quoted
hypotheses; it does not reprove those external theorems.  No downloaded
source, bulk certificate, or proof log is committed here.
