# No first stage in the specified minimum-eight route

Actual author: **six-covering-1**, role **researcher**, 2026-10-02.
Exact finite certificate and complete written CRT/symmetry/capacity argument;
unformalized, with two different same-author checks and no independent verdict.

**Theorem.** No family of congruences with at most one at each ORIGINAL
divisor of720 at least8, containing `5 mod8` and `6 mod9`, leaves its
uncovered residues confined to `3 mod18 union0 mod4`.

This excludes this entire first-stage construction route, irrespective of
its number of even holes or its subsequent tail. It does not exclude
arbitrary coverings of period15120, omit other first-stage possibilities,
or improve the global minimum-EXACTLY-eight bound. At-least-eight remains
separate. The previous actual-hole interval99..110 in this owned route
has no realization; the positive [standalone tail interval82..110](../four-coset-tail-overlap/proof.md) remains valid.

## Necessary core restrictions

Put `R={x mod720:x!=5 mod8,x!=6 mod9,x!=3 mod18}`, of size530,
`S={4t:t mod180,t!=6 mod9}`, of size160, and `F=R minus S`, of size370.
The first stage must cover EVERY point ofF. The fixed8/9 classes cover
none ofF orS. Its22 remaining ORIGINAL resources partition as

```
G0=(10,12,15,16,18,20),
G1=(24,30), G2=(36,40), G3=(45,48), G4=(60,72),
G5=(80,90), G6=(120,144), G7=(180,240), G8=(360,720).
```

Credited [9329](../stage720-four-hole-bound/proof.md) gives maximum gains
`48,36,25,22,14,11,7,3` onF for the last eight blocks. They total166,
so the actual core must cover at least204 points ofF. Only these pair
maxima are imported; neither the99-hole conclusion nor attainability is assumed.

For p=0,1 and b=1,2, define

```
B_(p,b)={4t:t!=6 mod9,t!=p mod2,t!=b mod3}, size50,
B_V={4t:t!=6 mod9,t=0 mod3}, size40.
```

Credited [9377](../stage720-tail-copy-occupancy/proof.md) bounds the entire
first-stage union on these five targets by `34,34,34,34,27`.
Precisely, if actual even holes4K are confined to the complement support,
the required compulsory counts420 or410 exceed available capacities404 or397.
For arbitraryK, subtract its holes outside that support: the same capacity
bound gives at least16 or13 such holes, hence these34 or27 covered-point caps.
This step uses9377's compulsory-complement calculations only, not its
three-classes-per-copy consequence or imported99-hole floor.

Original12 must occur with a nonzero residue. If12:0 occurs, all even
points with t=0mod3 are covered, leaving K inside the forbidden supportV.
If12 is missing, adjoining12:0 preserves distinct ORIGINAL labels,
fixed classes and hole confinement, causing the same contradiction.
This consequence was also written in
[9463](../stage720-weighted-block-barrier/proof.md).

Thus any actual core is a choice of phases or omissions at its six
ORIGINAL moduli, with12 present/nonzero, coreFgain>=204, and all five caps.
These are necessary conditions. They are not an assumption that all
independently allowed core configurations extend to a first stage.

## Complete core classification by symmetry

CRT identifies720 with144 times5. Moduli not divisible by5 depend on
`y=x mod144`; an ORIGINAL5d class selects one fibre`f=x mod5` and one
residue modulo d|144. Therefore arbitraryS5 permutations of the five
fibres transport every selected class to a class at the SAME original
modulus. The24 affine maps

```
y -> (1+12k)y +36(k mod2)+72e mod144,
k=0,...,11, e=0,1,
```

fix the prescribed8/9 classes, the18-hole class, the4-coset and all12
residues. They permute the four34-cap targets within their equal caps
and fix the27-cap target. They preserveR,F,S and every original modulus.
Their product withS5 gives2880 invertible maps preserving the full stage
problem. The multiplier is a unit modulo144. This is the same action
credited in9463, here retaining relative ORIGINAL phases.

The three left labels10/15/20 have cofactors2/3/4 and use one fibre each;
12/16/18 are identical on all five fibres. Up toS5, increasing first-use
fibre names give restricted-growth patterns. Including all omissions,
there are182 left cofactor-phase profiles with total raw multiplicity3696
`=(10+1)(15+1)(20+1)`. Right phases12=1..11,16=0..15 or omitted,
18=0..17 or omitted have3553 tuples. Their complete product accounts for
`3696*3553=13131888` ORIGINAL core choices. No right phases are normalized.

Checking the necessary conditions retains2560 raw ORIGINAL choices,
48 after fibre normalization, in14 affine/S5 classes. Every retained
core has all SIX original resources present. The following rows give
the canonical phases in order10/12/15/16/18/20; raw orbit sizes and every
phase witness are also in [certificate.json](certificate.json).

| Core phases | Core Fgain | Remaining F | Completion capacity | Strict deficit |
|---|---:|---:|---:|---:|
|0,7,11,1,5,2|206|164|146|18|
|0,7,11,1,9,2|211|159|146|13|
|0,7,11,2,9,2|205|165|161|4|
|0,11,1,1,1,2|206|164|146|18|
|0,11,1,1,9,2|211|159|146|13|
|0,11,1,2,9,2|205|165|161|4|
|5,2,1,1,0,7|205|165|149|16|
|5,2,1,1,12,7|205|165|149|16|
|5,7,11,2,9,2|205|165|145|20|
|5,7,11,2,9,10|205|165|145|20|
|5,10,11,1,0,7|205|165|149|16|
|5,10,11,1,12,7|205|165|149|16|
|5,11,1,2,9,2|205|165|145|20|
|5,11,1,2,9,10|205|165|145|20|

Completeness has two different finite checks. Python explicitly visits
182*3553=646646 cofactor-profile/right-phase pairs with exactS5
multiplicities, canonicalizes through the24 maps, and checks all
48 normalized tuples, split among the14 orbits. C++ visits ALL13131888 original phase/omission
tuples directly. Separately it expands the14 displayed representatives
under ALL2880 physical maps; the resulting2560 distinct tuples are
disjoint by row and equal the complete raw accepted list. Thus the
certificate does not presume an unverified small list is exhaustive.

## Completion bounds retain the fixed core

For a canonical coreC, writeD=F minusC. An actual stage with that core
must cover all ofD using the remaining eight ORIGINAL pairs. For each
pairG, allow every phase or omission at its two moduli, but require
`C union A_G` to satisfy the five caps. This is necessary because that
union is a subset of the actual full stage. Define

```
M_G(C)=max |A_G intersect D|
```

over this complete domain. Any actual completion covers at most
`sum_G M_G(C)` points ofD. These independently maximized point incidences
may overlap; the sum is an upper bound, not an assertion of simultaneous
attainment. The caps are imposed onC union EACH pair, never on sums of
overlapping target incidences.

The compact certificate records ALL112 maxima, their maximizing original
phases, and accepted/rejected raw phase counts. They sum to the completion
capacities in the table. All14 totals are strictly smaller than their
remaining demands; the smallest deficit is4. Hence no canonical core
can extend. Every eligible raw core is a resource-preserving image of
one of them, so no first stage satisfying the theorem exists. QED.

## Reproduction and trust boundary

Python uses exact physical720 masks, explicit omissions with counted
aliases, CRT fibre profiles and exact affine canonicalization. It
regenerates all14 rows and112 pair maxima, with10 semantic damage tests.
C++ uses720-bit physical progressions and no restricted-growth profiles
or canonicalization. It expands all2880 maps, inspects2073600 physical
permutation points,103680 generator original-phase transport points and
12136320 original core progression points. It then visits all13131888
raw cores and4729438 raw pair tuples, including omissions, and compares
every maximum and accepted count. Four damaged text certificates reject
in each ordinary audit-driver mode. Its text certificate encoding is
checked against JSON before use. All arithmetic is exact bounded counts
or arbitrary-precision Python integers; no solver or tolerance is a premise.

From the repository root with Python3.11+ standard library and g++12/C++17:

```sh
python3 round-two/six-covering-1/stage720-core-obstruction/verify.py
```

This runs five sequential normal/O/sanitizer replays, with20-second child
guards,12-second compilation and10-second C++ execution guards, and one
native thread. The ordinary CRT/symmetry/completion bridge is unformalized.
CPython and the C++ compiler/runtime remain trust boundaries. Distinct
same-author algorithms are not independent peer review or formalization.
A failed process, incomplete enumeration or UNKNOWN is not used as exclusion.

## Position and next construction

The [7174 point-capacity method](../../../number_theory/distinct_covering_residual_weight_duals/proof.md)
is classical. The new contribution is this complete14-core ORIGINAL-phase
classification and whole-route exclusion, without a historical priority claim.
The [9465 sparse-parent classification](../../six-covering-3/sparse-parent-kernels/proof.md)
concerns a different free10080 tail inventory and is complementary context;
no numerical fixture or audit is imported. Global candidates10080/15120/20160,
only20160 witnessed in credited work, remain unchanged.
Primary context refreshed2026-10-02 is
[Zhang--Zhang](https://arxiv.org/html/2607.19029) for minimum-seven10080 and
[Harrington--Klein--Lowrance--Trifonov](https://arxiv.org/html/2605.18644) for
restricted2/3/5-prime coverings; their numerical results are not proof premises.

The constructive next route replaces the odd18-hole class3 by1. Under
affine maps preserving the prescribed9:6 class, `gcd(q-6,9)` is invariant
for the odd18-hole phaseq. It is3 atq=3 and1 atq=1, so these routes cannot
be conflated by the affine normalization above. No old34/27 caps, core204
cut or nonexistence conclusion is transferred to the new target. Recompute
its necessary gains and search for an actual first stage before tail completion.
