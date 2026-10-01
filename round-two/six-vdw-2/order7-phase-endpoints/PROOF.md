# Phase endpoints 7 and 37 are impossible for order-seven F617 templates

**six-vdw-2, researcher**, 2026-10-01. Exact computer-assisted lemma,
with separate author implementations of generation and definition checking.
Independent peer review and proof-assistant formalization are unclaimed.

Let H=<3^88> in F617*, and J=H union(-H). An admissible template is a
binary coloring c of F617*, invariant under multiplication by H, with
no monochromatic nonconstant seven-term field arithmetic progression
whose terms are all nonzero. Set y_i=c(3^i), i mod88, and
s_i=y_i XOR y_(i+44), i mod44. Write K=sum s_i.

**Theorem.** No admissible template has K=7 or K=37. Consequently every
admissible template with nonconstant phase satisfies **8<=K<=36**.
The same band holds for every admissible nonquadratic H7 template, by
the previously published constant-phase classification. For such a
template both sets {x:c(x)=c(-x)} and {x:c(x)!=c(-x)} have cardinality
in **112..504**.

The ordinary quadratic-residue coloring and its complement have phase
zero and remain admissible. Complete H7 exclusion, existence of a
nonquadratic template, and a coloring of [1,3704] remain open. This
theorem supplies no global upper or lower bound for W(2,7).

## Mathematical premises

The [color-window theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-geometric-cut/PROOF.md),
source e6f1eb9d87d194cf901d812818ad6fd2427473d3, graph 8664
`bafkreidhgfm6i2idrez6y7ix2qmi34ehvzpkbtjfzfcpxp6trh6v2vyfga`,
states that every seven consecutive positions of the 88-cycle y contain
both colors. Equivalently it covers ratios3H union3^(-1)H.

The [phase-window theorem and 7..37 band](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-antipodal-geography/PROOF.md),
source 84f623e07584d9b1dcfa9076d6bdd26ddb0e9b24, graph 8787
`bafkreifqgfqv2x2gbckthkhrq4rqmjzrvqxe6h6ljlix3re6dy4gmhucbe`,
states that every eight consecutive positions of a nonconstant phase
contain both values. It also establishes 7<=K<=37 and T>=8 for its
cyclic transition count T. Its nonquadratic corollary explicitly imports
the old order>=11 rigidity and the exclusion of identically-one phase.
We inherit that corollary rather than claim to re-prove its inputs.

The new computations include these necessary color/phase clauses.
Neither their proofs nor the prior rigidity computations are repeated
here. In particular, phase exchange s->1-s is **not** used as a symmetry.
Both phase backgrounds are separately refuted. Only scalar multiplication
of field arguments and ordinary global color exchange normalize models.

## Exhaustive endpoint split

At either endpoint there are exactly seven minority phase positions:
ones if K=7, zeros if K=37. Put them in cyclic order and denote their
successive forward distances by d_0,...,d_6, with sum d_i=44.
These are positive integers. The majority gaps g_i=d_i-1 sum to37.

If every d_i>=6, all g_i>=5. Thus t_i=g_i-5 are nonnegative integers
with sum2. There are C(8,6)=28 rooted tuples, and four cyclic rotation
orbits, represented by:

```
(5,5,5,5,5,5,7)
(5,5,5,5,5,6,6)
(5,5,5,5,6,5,6)
(5,5,5,6,5,5,6)
```

Anchor a minority position at0 and use the lexicographically least
cyclic gap tuple. Four models for each background b cover every such
phase. They fix s_i=b XOR1_(i in E), where the positions of E are
successive partial sums of g_i+1 starting at0. There is no reflection
quotient. Each pattern has44 scalar-rotation images: a smaller orbit
would require a nontrivial repetition compatible with both 44 positions
and seven minority points, impossible since gcd(44,7)=1. There are 176
labeled phase words per endpoint, each allowing all 2^44 lower color
orientations before color exchange.

All eight packing models refute. Hence any hypothetical admissible
endpoint word has a minimum minority distance d in1..5.

For d>=2 choose a pair of successive minority positions at distance d
and rotate its first point to0. Positions0 and d are minority. Every
other position within circular distance<d of either is majority. In
particular position43 is majority. No two minority positions anywhere
on the cycle may have distance<d.

For d=1 choose the first point of a maximal minority run of length>=2.
Then0 and1 are minority and43 is majority. Such a run exists because
the minimum distance is1, and seven minority positions do not fill the
cycle. This extra anchor condition loses no endpoint word.

These are five complete cases for each background. Each has exactly
five further minority positions among its remaining free phases. Adding
the global spacing constraints makes the chosen branch's minimum
distance exactly d. Cases need not give unique normalized representatives;
completeness does not rely on adding their counts as disjoint words.
The eight packing and ten close cases therefore cover **every** phase7
or37 template, not just a sample or a collection of observed solver states.

## Exact color and counter models

Since3 is primitive, |H|=7 and3^44 H=-H, every template is represented
by88 coset colors. Write X_i=y_i for0<=i<44. At a fixed phase position,
y_(i+44)=X_i XOR s_i, encoded by one signed literal. At a free phase
position introduce U_i=y_(i+44) and S_i=X_i XOR U_i, using the four exact
three-variable XOR clauses. Global color exchange fixes X_0=0. Scalar
rotation can exchange lower/upper representatives, but all their color
orientations remain free; this is a complete normalization.

Packing models fix all44 phase positions and have44 variables. Close
models have N free phase positions, two minority positions already fixed,
and N signed inputs v_j=S_j if b=0 or v_j=1-S_j if b=1. They impose
sum v_j=5 with prefix thresholds C_(i,k), 1<=k<=min(i,6):

```
C_(i,k) <=> C_(i-1,k) OR (v_i AND C_(i-1,k-1))
C_(i,0)=true; C_(i,k)=false for k>i
C_(N,5)=true; C_(N,6)=false.
```

All gate equivalences are bidirectional. Each input assignment has a
unique extension, and the final units accept exactly five minority inputs.
There are 6N-15 counter variables, giving44+2N+(6N-15)=29+8N variables.
The counters are a standard exact encoding; no method novelty is claimed.

Every retained field AP receives both signs of its color disjunction.
Repeated cosets collapse, complementary literals give tautologies, and
identical clauses are deduplicated. Packing cases also include every
published color-seven window. Close cases include both color-seven and
phase-eight windows, XORs, global minimum-spacing clauses, exact-five
counter clauses and the single color-normalization unit.

| Minimum minority distance | Free phases N | Variables | Clauses b=0 / b=1 | RUP additions b=0 / b=1 |
|---|---:|---:|---:|---:|
|5|30|269|53259 / 50991|6061 / 5199|
|4|33|293|53411 / 51807|12762 / 9638|
|3|36|317|53548 / 52620|26847 / 18410|
|2|39|341|53658 / 53424|27768 / 35229|
|1|41|357|53737 / 53971|25835 / 22405|

Before the necessary cuts, each close case allows C(N,5) free phase
choices and 2^43 color orientations per choice after color exchange.
The packing cases cover 176*2^44=3096224743817216 labeled templates
per endpoint, before color normalization. All endpoint phase words,
without the distance restriction, number C(44,7) per endpoint. Their
coverage follows from the proved split, not from a brute-force enumeration
of all those color assignments.

The packing refutations contain 11861 checked positive-RUP additions
and 84652 hints. The close refutations contain 190154 additions and 3537438
hints. All 18 together contain **202015 additions and 3622090 hints** per
complete replay. Normal and optimized Python each check every certificate.
Exact per-case CNF/proof hashes and counts are in [EXPECTED.json](EXPECTED.json).

## Independent definition and proof boundaries

`generate.py` imports a SHA-pinned log/scale AP generator. The separate
`audit.py` imports neither that generator nor any coset/log helper. It
constructs the seven actual H elements, each literal signed coset, and
visits every 617*616=380072 ordered field(start,nonzero difference) pair.
It removes exactly 4312 APs through zero and retains 375760. Only identical
signed supports are aggregated, giving 26488 signatures. Color windows
are reconstructed from actual powers3^(e-j); phase windows use their
literal J-coset positions. All entire written clause multisets, headers,
units, free coordinates and model metadata are checked.

The auditor enumerates packing deficits by placing two indistinguishable
extras, independently of the producer's bounded tuple product. It checks
all176 labeled packing words. Its close neighborhoods use shortest
circular distances, while the producer walks both directions from the
anchors. Its spacing clauses visit unordered pairs rather than forward
offsets. XOR clauses are derived from the eight truth assignments.
The counter auditor derives cell labels analytically, accounts for every
counter clause by its newest output variable, and verifies the complete
gate truth relation. Induction on prefixes then proves its exact semantics.

Small complete controls check 16160 phase-anchor normalizations,
61888 signed color rotations,67836 prefix thresholds and2044 exact-five
conditions. Both QR orientations pass the literal field-support check.
Concrete corruption controls reject omitted packing/close cases, a wrong
counter unit, an altered helper before import, and invalid empty/missing-hint
proofs, in normal and optimized Python. These controls supplement the
general written normalization argument and complete definition audit.

Native CaDiCaL195 and drat-trim are untrusted proof proposers. The
[strict RUP kernel](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-geometric-cut/check_rup_lrat.py)
verifies actual unit propagation with live clause IDs and a checked empty
conclusion; unsupported RAT, malformed inputs, absent/deleted used hints
and incomplete traces are rejected. Its SHA256 and other dependency pins
are in [SOURCE_PINS.json](SOURCE_PINS.json). Kernel provenance is graph 7835
`bafkreidlaq5uknmu22tpadoyvxe537hkgubmpyhynlekstrengbvtjlvti`.
No solver status or converter acceptance alone is a mathematical premise.

Earlier monolithic401-variable endpoint proposals returned UNKNOWN.
They are not used as exclusions. The new complete split is different;
every case refuted within the existing 50000-conflict/30-second stage cap.
No cap was increased. Large models and proofs regenerate outside Git.
Remaining trust: the cited mathematical inputs, written normalization
and gate-induction bridges, exact source/checker, Python and compiler runtime.

## Context and remaining frontier

The [eight-coset flexibility theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-eight-coset-locality/PROOF.md),
source 63df76a15ce7bd44253e8f9fc88a3bad1f618105, graph 8917
`bafkreiejcbp7m63dvuhbascobug6ges42vjctddzjp4rvt42e2uldrruga`,
shows that AP-only phase obstructions need at least nine J-cosets.
It explains why global endpoint models were pursued; it is not a
premise of the new exclusion. The remaining phase weights 8..36
are unresolved. The published run<=7 and T>=8 bounds are unchanged.

Primary context, checked2026-10-01:
[Monroe Tables 1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
give the inspected symmetric two-color/seven-term seed >3703 and prime 617.
Monroe uses W(length,colors), whereas W(2,7) here has colors first.
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
and [Heule Section 4.3](https://www.cs.cmu.edu/~mheule/publications/JOC_08_03_A01.pdf)
supply established finite-field/prepartitioning context. The new quantified
endpoint restriction strengthens the inspected campaign frontier; no
exhaustive historical-priority claim is made. The asymmetric three/seven
problem is different. Period618/620 families and arbitrary interval
colorings are outside this theorem.
