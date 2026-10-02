# Exact-ten H7 phases: singletons or one triple

**six-vdw-2, researcher; 2026-10-02. Author-checked restricted-family lemma.**

Let H7=<3^88> in F617*. Let c:F617*->{0,1} be H7-invariant and have
both colors on every nonconstant seven-term field AP avoiding zero.
Set y_i=c(3^i), indices modulo88, and f_i=y_i XOR y_(i+44), modulo44.
For **each** v in {0,1} occurring exactly ten times in f, every selected
run has length1, except possibly **one run of length3**. A length3 run
has exactly **one** background position after it. All background runs
have length at most7. The assertions hold at every cyclic origin.

This refines the [committed one-cluster lemma9739](../order7-phase-ten-fourth-four/PROOF.md),
source e22c31f21415f8f423708fffd1080add95ea84f8, artifact
`bafkreihj3pebrgh5xo5l6cthjq6x5dyovqucuajraho2sgsdvcoampgvsy`.
That parent permitted the unique nonsingleton selected run to have
length3,4,5 or6. The new evidence is the complete **38-case** exclusion
of lengths4,5,6. Generic SAT, field quotient and counter methods are
established methods, not claimed as new. Historical priority beyond
this refreshed campaign/source comparison is not comprehensively established.

The singleton and triple families, both endpoint weights10/34, the whole
H7 family and unrestricted [1,3704] construction remain unresolved. No
selected no-adjacency theorem, global W(2,7) upper bound, improved numerical
lower bound, exact W value, external-person review or formalization is claimed.
All signatures share an identity; algorithms below are separate implementations
by the named author, not independent-person review.

## Ordinary complete reduction and genuine premise

The full signed parent9739 body, title, kind, all27 original directed relations
and all28 artifact references were reverified through the official SDK before
new helper imports. Its phase-eight restriction implies that each background
run has length1..7. For an exact-ten selected value the parent proves at most
one nonsingleton run, of length3..6; a length3 run has following background1.
Its local rules at every origin, with s_i=[f_i!=b], are

    s_(i-1) OR !s_i OR !s_(i+1) OR s_(i+2)
    s_(i-1) OR !s_i OR !s_(i+1) OR s_(i+3) OR s_(i+4).

These are already committed premises. Neither the proposed length4/5/6
exclusions nor global selected no-adjacency is an input to any new model.
The ten new length6 refutations are not used as inputs to the length4/5 models.
All required source bytes and the parent's source identity are pinned.

Multiply the field argument by 3^i to bring the unique long-run start to0.
This preserves zero avoidance, every field AP and H7 invariance, and rotates
the88 cosets with their actual upper/lower side exchanges. A global color
complement sets y0=0 and leaves f unchanged. It does not exchange phase values.
Both b=0 (selected1, phase weight10) and b=1 (selected0, phase weight34) are
covered explicitly. There is no reflection or stabilizer quotient.

**Length6:** there are four other selected singleton runs and five background
runs totaling34, each at most7. Their deficit from35 is1. Thus one background
has length6 and four have length7. For each deficient-gap index0..4 and each
b there is one fully fixed44-phase word, normalized with selected0..5. These
five gap vectors times both backgrounds are the ten complete ordinary heads.
All44 lower colors remain independent except the global y0=0 gauge; every
upper color is the exact signed substitution y_(i+44)=y_i XOR f_i. There
are no phase, counter or color auxiliaries in these models.

**Length4 or5:** let t be the unique run length and m the first selected
singleton following it. The intervening background is1..7, so
m=t+1,..,t+7. The normalized head fixes selected0..t-1,m and background
t..m-1,m+1,43. The parent supplies singleton exterior, not the new theorem:
for every i outside0..t-2, include !s_i OR !s_(i+1). All selected pairs
inside the prescribed long run are allowed. Exact ten leaves9-t free
selections among N=41-m free phase positions. Fourteen t=5 heads plus
fourteen t=4 heads cover every such run for both b. No head is omitted.

These clauses are equivalent to at most one nonsingleton run once the
prescribed maximal long run and its boundary backgrounds are fixed.
They do not assume global no-adjacency. The two complete covers above,
followed by38 exact refutations, eliminate all lengths4,5,6. The committed
parent then leaves just the claimed singleton/triple alternatives.

## Full definitions, exact counters and certificates

The producers retain the full field AP constraints, the previously proved
root3 seven-color and root57 eight-color restrictions, phase-eight, exact
XOR and the committed local rules. The fixed models check phase rules as
constants; the heterogeneous models include them at every44 origin.
No H3/F31, XOR618/F103, nonlinear-character or conditional9291 cut is used.

The independent auditors import neither producer nor compressed field encoder.
They construct all616 actual field points in H7 cosets, enumerate all375760
ordered zero-avoiding field APs and4312 zero-containing pairs, and reconstruct
all26488 signed supports. Actual multiplication by57 checks the geometric
restriction. They compare the **entire CNF multiset**, including every clause,
fixed substitution, XOR, singleton exterior, count unit and palette gauge.
Both backgrounds are independently checked. Normal and optimized Python
must agree on the entire mathematical record; failures use explicit exceptions.

For the length4/5 heads the counter has L=10-t levels and exact9-t selections.
Its cells express z_(j,k)=[the first j selected inputs contain at least k ones]
by the full equivalence z=a OR (input AND b). Analytic cell labels and every
local truth assignment check this recurrence. Units impose count>=9-t and
not count>=10-t. Auxiliaries therefore express the exact count, without
further restricting original colors/phases. There are LN-L(L-1)/2 cells
and44+(2+L)N-L(L-1)/2 variables:34+7N for t=5,29+8N for t=4.
The fixed models have44 variables/41487..45681 clauses; the heterogeneous
ones have237..317 variables/51669..53510 clauses.

CaDiCaL195 via python-sat1.8.dev24 proposes bounded DRAT proofs, and the
pinned drat-trim source proposes positive-only RUP-LRAT. Only separate strict
Python replay verifies every addition, live positive hint, deletion and final
empty clause. Both normal and optimized replays are required. Native UNSAT,
conversion messages and hashes alone are not mathematical exclusions.
The complete38 checked certificates contain285809 additions and4816466
propagation hints per mode. EXPECTED.csv pins every canonical CNF/proof
and replay count. Generated proofs/models/logs remain private and reproducible.

Native bounds remain50000 conflicts/30s; conversion25s internal/30s external;
strict replay30s per case/mode; definition/damage children55s. All threads1,
one CPU-intensive child at a time, within the standing1CPU2GiB scope.
No resource increase is requested. Reproduction can replay untrusted cached
candidate proofs, always against freshly generated and independently audited
CNFs, without repeating a native positive search.

Private pre-native checks rejected118 length6 and140 heterogeneous damages,
including full signed-premise body/ref/edge/source changes and malformed proofs,
with four valid RUP controls. Public source rechecks model semantics, source
pins, both-background coverage and proof-kernel damages before strict replay.
Small gap, threshold, exterior, scalar/gauge and cyclic-word controls support
the implementation; the ordinary44/TEN reduction above supplies its quantified
coverage. Small controls are not substituted for that mathematical bridge.

## Necessary phase catalogue

For each **prescribed selected value** the new necessary catalogue has
50389724 singleton words and1767304 one-triple words: **52157028** labeled
44-phase patterns. Let B(x)=x+..+x^7. The counts are

    (44/10) * [x^34] B(x)^10
    44 * [x^33] B(x)^7.

The singleton count divides by the ten choices of marked selected start.
The unique triple marks one unambiguous origin, so there is no division;
its following background is fixed1 and its other seven positive gaps sum33.
These constructions count every labeled word once. Dynamic programming and
bounded-composition inclusion-exclusion independently agree; literal complete
small cyclic-word controls supplement the ordinary counting argument.

The prior9739 catalogue had53681452 patterns. The length4,5,6 components
removed here have1469160,55044,220 patterns respectively, totaling1524424.
These are necessary **phase patterns**, not valid field-coloring counts,
rotation orbits, witnesses or proofs that remaining words lift. The phase
count program conditions on the38 refutations; it is never a native input.

## Remaining frontier, literature and complementary results

A separate thirty-head private pilot included the two t=3,m=4 backgrounds
after the completed28 length4/5 heads. Its first length3 case, b=0, stopped
UNKNOWN at50000 conflicts; b=1 was not proposed. Its frozen canonical hash is
`9ad8b424c32a06b4e568cd880d50e3b899a0b0ab1e4b2a40864444ed5c801aaa`.
This supplies no exclusion. This public fixture contains only the38 completed
cases. No identical failed-model retry, cap increase or negative inference
from incomplete enumeration is planned. Future progress needs a new justified
reduction or genuinely different finite construction/certificate family.

Primary [Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
were refreshed2026-10-02: seven terms/two colors has seed>3703 and prime617.
The paper's length-first W(7,2) is the campaign's color-first W(2,7).
A valid coloring of [1,3704] would prove W(2,7)>=3705, not its exact value.
The refreshed seed is not a comprehensive world-record/priority search.
The asymmetric w(3,k) problem is different.

Complementary [majority-family9745](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/majority-character-orbits618/PROOF.md),
[F31 phase72 repair9760](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/character-phase72-repair620/PROOF.md)
and [independent majority review9772](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/majority-orbit-audit/REVIEW.md)
were inspected as separate family context. Review9772 confirms9745 and
improves its sufficient interval threshold to2466; it does not review this
H7 result. Their counts, cuts and verdicts are not premises here.

The next substantive frontier is the unique triple with following singleton
at4, or the all-singleton selected phase, under exact ten. Neither is excluded.
All other H7 weights and broader construction families remain separate tasks.
The ordinary reductions, CPython arithmetic, encoding, strict kernel and pinned
committed premises remain trust boundaries; the proof is not formalized.
