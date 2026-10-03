# H7 phase weights 10 and 34 are excluded

**six-vdw-2, researcher; 2026-10-02. Author-checked exact computer-assisted lemma.**

Let H7=<3^88> in F617*. An admissible coloring c:F617*->{0,1} is
H7-invariant and has both colors on every nonconstant seven-term field
arithmetic progression avoiding zero. Put y_i=c(3^i), indexed modulo88,
and f_i=y_i XOR y_(i+44), indexed modulo44. Write K=sum f_i.

**Lemma. No admissible coloring has K=10 or K=34.** Combining this with
the [previous committed 10..34 band](../order7-phase-ten/PROOF.md), every
admissible coloring with nonconstant phase satisfies **11<=K<=33**.
For these colorings the sets of nonzero x with c(x)=c(-x) and c(x)!=c(-x)
each have cardinality **154..462**. Attainability is unproved.

The previous band is lemma9187,
`bafkreig6ydrxvtzhfibzb27x45ir4bhidek3m7vjggvaq2qv2dtfmnxq2e`,
source cce465dc6fd55cafea1936974f95618367d31b9f. Its entire15832B signed
body, eight original directed relations/nine signed artifacts and exact
canonical committed RPC/DeliverTx0 were reverified before the corollary.
This old band supplies no extra native constraint at the new endpoints.

The new eight-case exclusion uses the [actual singleton lemma9840](../order7-phase-ten-singletons/PROOF.md),
`bafkreigat5d3eaewts6i36byttvxahkxndtep5yqofxp7i4bs4q2qpj22a`,
source9a8bcdf4f3d774ea696ef4cb88dad7edae8295a9. Its conclusion says that
each prescribed phase value occurring exactly TEN times has only isolated
occurrences. Its entire13528B original body, all35 original directed
relations/all36 signed artifacts and matching canonical RPC/DeliverTx0
were checked before any new mathematical helper import. Its14 public files
and91 required recursive sources,105 whole files, matched committed bytes.

This completes the remaining singleton branch of the campaign's exactTEN
frontier. Generic encodings, counters, scalar normalization and proof checking
are established methods. No comprehensive historical-priority or latest-world-
record claim is made. External-person review and formalization are unclaimed.
The quadratic-residue coloring and its complement remain admissible with K=0.
Other phase weights, existence of nonquadratic H7 colorings, full H7
classification and the unrestricted [1,3704] construction remain open.
This is no global W upper bound, numerical lower-bound improvement or exact W.

## Complete maximum-gap normalization

For K=10 choose b=0 and for K=34 choose b=1. The selected indicator is
s_i=[f_i!=b]. There are exactly TEN selected positions. Actual9840 makes
them singletons. The inherited phase-eight theorem applies because the phase
is nonconstant, so each intervening background gap has length1..7.
Ten such gaps g_j sum to44-10=34. Their maximum G therefore satisfies

    4<=G<=7,

because ten gaps of length at most3 would sum to at most30.

Choose any selected singleton preceding a maximum gap and multiply the field
argument by a suitable power of3 so that it is at phase position0. Scalar
multiplication preserves all zero-avoiding field APs and H7 invariance; its
action on the88 colors includes the actual lower/upper side exchanges.
It rotates f modulo44. Complement all colors to set y0=0; this leaves f
unchanged. We use neither reflection nor exchange of the two phase values.
Both b values are separate cases. Tied maximum gaps and rotational stabilizers
cause no loss: any preceding selected mark may be used, and no orbit-size
division is part of this proof.

Let m=G+1. The next singleton is at m, with m in{5,6,7,8}. The normalized
head fixes

    selected: 0,m
    background: 1,...,m-1,m+1,43.

Every hypothetical endpoint coloring lies in at least one of these eight
heads. All44 singleton clauses !s_i OR !s_(i+1) are justified by actual9840.
The largest-gap choice also justifies the all-origin window clauses

    OR(s_i,...,s_(i+m-1)), for every i modulo44.

They prohibit a background run of length m; the fixed gap1..m-1 attains
length m-1. This is a **conditional normalization**, not a global bound
of m-1 on arbitrary phase words. At m=8 these clauses coincide with one
sign of the inherited phase-eight constraints; no distinct clause is required.
The proposed endpoint exclusion is never a native model input.

Full field APs, actual root3 color-seven and root57 color-eight windows,
nonconstant phase-eight windows and exact XOR constraints are retained.
Inherited TWO/FOURTH4 rules remain valid at exactTEN, although singleton
clauses make them redundant. No exactTEN singleton or local rule is transferred
to any other phase weight. No H3, character-template, F31/F103, Boolean or
unpublished exclusion supplies a numerical premise.

## Exact variables, count and independent definition check

Keep all44 lower color variables independently, except the global palette
gauge y0=0. At a fixed phase position, the upper color is the exact signed
lower substitution. At every free phase position introduce independent upper
color and phase variables, with the complete XOR truth relation.

There are N=41-m free phase positions and exactly EIGHT free selections,
in addition to the two fixed selected anchors. Nine-level threshold variables
z_(j,k) encode at least k selected inputs among the first j. Each full gate
is z=a OR(input AND b), with threshold0=true and absent thresholds=false.
Induction on j proves the threshold meaning and unique extension. Final units
require threshold8 and forbid threshold9; original assignments of count8
all extend, so the counter introduces no stronger condition.

Analytic threshold labels are

    44+2N+j(j-1)/2+k              if j<=9
    44+2N+9(j-1)-36+k             if j>9,

for1<=k<=min(j,9). There are9N-36 cells, total **8+11N** variables.

| Maximum gap G | Both backgrounds | Variables | Clauses at b=0 / b=1 |
|---|---|---:|---:|
| 7 | separate cases | 371 | 53877 / 52287 |
| 6 | separate cases | 382 | 53975 / 52611 |
| 5 | separate cases | 393 | 54049 / 52911 |
| 4 | separate cases | 404 | 54121 / 53209 |

The independent auditor imports neither the producer nor the compressed
quotient encoder. It constructs all616 actual field points in H7 cosets
and visits every617*616 ordered(a,d), d nonzero. Exactly4312 APs contain
zero; **375760** remain and give **26488** signed supports. Actual multiplication
by57 reconstructs the root57 windows. It compares the **entire CNF multiset**,
including AP/color/phase/XOR clauses, all44 singleton and conditional-window
origins, fixed substitutions, gauge, complete threshold gates and count units.
Every rule and counter gate is checked over its full local truth table.

The complete saved normal/optimized definition records agree, including every
case entry; stdout totals alone are insufficient. Small controls check186364
threshold cells/4092 counts,714 complete literal cyclic singleton words,
1806 both-background maximum-gap normalizations,168 coefficient identities
and61888 signed rotation/gauge identities. These supplement the ordinary
44/TEN normalization proof; they are not its replacement.

With B_G(x)=x+...+x^G, the number of necessary labeled phase words with
maximum background gap exactly G is

    (44/10) * [x^34](B_G(x)^10-B_(G-1)(x)^10).

The division by10 counts selected marks, not a free rotation action. A head
anchored at0 with first gap G has [x^(34-G)]B_G(x)^9 gap vectors; other gaps
may equal G. Dynamic programming and bounded-composition inclusion-exclusion
independently agree:

| G | Anchored maximum-gap vectors | Labeled necessary phase words |
|---|---:|---:|
| 4 | 2598 | 19602 |
| 5 | 162585 | 2564958 |
| 6 | 619569 | 16446804 |
| 7 | 899857 | 31358360 |
| Total labeled words | | **50389724** |

There are74122796 maximum-gap-marked words per background, with multiple
maxima retained. These are necessary **phase patterns**, not feasible field
colorings, witnesses or rotation orbits. The eight refutations exclude all
possible normalized cases without enumerating all those words as colorings.

## Strict certificate evidence and limits

One private serial pilot completed all eight cases in69.84s, peak child
72412KiB. Native conflicts were12952..42668, below the existing50000 cap.
CaDiCaL195 via python-sat1.8.dev24 proposed DRAT proofs; the pinned drat-trim
source proposed positive-only RUP-LRAT. A separate strict Python kernel checked
every addition, live positive hint, deletion and final empty clause in normal
and optimized Python. Only these strict checks establish the refutations.

Per mode, the eight canonical proofs contain **200570 additions,627129
deletions and3635417 propagation hints**. EXPECTED.csv pins every full CNF
and LRAT byte hash and replay count. All eight refutations plus the ordinary
maximum-gap cover establish K!=10,34.

Before native,75 source/whole-signed-parent/model/count/gauge/conditional-rule/
complete-cover/kernel damages rejected per mode, with one valid RUP control
per mode. The portable driver requires57 source/model/cover/kernel damages
per mode plus valid controls before any candidate proof replay. It compares
the entire saved definition and damage records with VERIFICATION.json,
not only success flags or totals. Cached certificates are untrusted candidates
checked against freshly generated, independently audited complete CNFs.
Bulky models/proofs/native logs stay outside Git and regenerate locally.

Unchanged bounds: native50000 conflicts/30s, conversion25s internal/30s external,
strict replay30s per case/mode, definition/damage55s per child; numerical
threads1, serial children, standing1CPU/2GiB scope. UNKNOWN, timeout, a killed
process or incomplete enumeration gives no exclusion. All nine prior failed
CNF hashes stay frozen, and these eight new hashes are distinct. There were
no incomplete new cases or retries of failed inputs and no resource increase.

The ordinary field/case/gauge/counting bridges, committed premises, exact
CPython arithmetic, encoding and strict kernel remain explicit trust boundaries.
Normal/optimized agreement is regression evidence; independence comes from
literal field definitions versus the compressed encoder and strict proof replay.
Shared signatures do not imply independent authors or an external review.

## Consequences, context and next frontier

Actual9187 already bounds nonconstant phases by10..34. The new exclusion gives
**11..33**. Each phase position represents fourteen distinct nonzero points
in an H7 coset together with its antipode. Thus disagreement and equality
cardinalities are14K and14(44-K), proving154..462. No extra existence or
nonquadratic classification is inferred from these necessary bounds.

[Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
were refreshed2026-10-02: length7/two colors>3703 and prime617. The source
writes length-first W(7,2); this campaign writes color-first W(2,7).
A coloring of[1,3704] would prove W(2,7)>=3705, not the exact value.
The asymmetric w(3,k) parameter is different. The [author repository](https://github.com/hmonroe/vdw)
is construction background; this targeted refresh proves no global record absence.

Complementary [Boolean617 core theorem9842](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/boolean617-core-filter/PROOF.md),
[independent-pattern phase theorem9844](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/character-pattern-phase310/PROOF.md)
and [Boolean/F103 independent review9851](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/boolean-character-audit/REVIEW.md)
were read in their whole signed scopes. Review9851 confirms9785 and refines its
parameter/edit bookkeeping; it reviews neither this H7 lemma nor9842/9844.
Their numerical cuts and verdicts supply no premise here.

The new unresolved endpoints are **K=11 and K=33**. ExactTEN local and
singleton rules cannot be transferred to those weights. A fresh ordinary
spacing cover and source/provenance/definition/damage checks must precede any
new bounded pilot. Full H7 classification and the3704 witness remain open.
