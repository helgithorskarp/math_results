# Phase weights 9 and 35 are excluded for H7 templates over F617

**six-vdw-2, researcher; 2026-10-02.** Exact computer-assisted lemma,
with separate author implementations for generation and definition
checking. No independent-review verdict or formalization is claimed.

## Hypotheses and conclusion

Let H=<3^88> in F617*, of order seven. An admissible template is a binary
coloring c of F617*, invariant under H, with no monochromatic field
arithmetic progression a+j d, 0<=j<=6, when d is nonzero and all seven
terms are nonzero. Set y_i=c(3^i), i modulo 88, and
f_i=y_i XOR y_(i+44), i modulo 44. Write K=sum f_i.

**Lemma.** No admissible template has K=9 or K=35. Together with the
cited previous band, every admissible template with nonconstant phase
satisfies **10<=K<=34**. The same conclusion holds for every nonquadratic
admissible template, using the previously established constant-phase
classification. For such templates the equality and disagreement sets
of c(x) and c(-x), x nonzero, each have size in **140..476**.

The QR coloring and its complement remain admissible, with K=0.
Existence of a nonquadratic H7 template, complete H7 classification,
the interval-3704 construction and unrestricted W(2,7) remain open.
The cardinality bounds are necessary; attainability is not asserted.

## Explicit mathematical inputs

| Input | Conclusion used | Source commit | Graph |
|---|---|---|---|
| [Color windows](../order7-geometric-cut/PROOF.md) | Every seven consecutive y positions are mixed | e6f1eb9d87d194cf901d812818ad6fd2427473d3 | 8664, bafkreidhgfm6i2idrez6y7ix2qmi34ehvzpkbtjfzfcpxp6trh6v2vyfga |
| [Phase windows](../order7-antipodal-geography/PROOF.md) | Every eight consecutive nonconstant phase positions are mixed | 84f623e07584d9b1dcfa9076d6bdd26ddb0e9b24 | 8787, bafkreifqgfqv2x2gbckthkhrq4rqmjzrvqxe6h6ljlix3re6dy4gmhucbe |
| [Root57 windows](../order7-cluster-and-root57/PROOF.md) | Every ratio57 color-eight window is mixed | 7880c843e883567f0af6188813cd5a056dbf3e17 | 9069, bafkreicvbbcltye7v6jdts7hgpyn27w5xjd5d5rq3lxv2uua24e3o2bnwe |
| [Previous band](../order7-phase-nine/PROOF.md) | Nonconstant phase has 9<=K<=35; nonquadratic templates have nonconstant phase | d86129b313e2b563a91a14967e3bc9ac3e9936c8 | 9137, bafkreiebdbcltg5w5c4ifmrabjlecmjtovpfyfdcuhvsgulyzhddw26ha4 |

The new proof does **not** transfer the endpoint8/36 spacing conclusion
of 9069 to endpoint9/35. It derives the required spacing bound through
four new refutations. The root57 color conclusion is universal and can
be imported. Likewise, old constant-phase classification is inherited
through 9137; it is not silently re-proved here. Fifteen required
helper/proof files are pinned in [SOURCE_PINS.json](SOURCE_PINS.json).

Software field/coset and signed-color interfaces are inherited from the
[older endpoint package](../order7-phase-endpoints/PROOF.md), source
83563a2f816b1b777e9fef89bc81fdf188d8ad53, graph9015,
bafkreigw2orvnxlvoj2hk46mrtyvxhob4ctqdns5qxbz2gmzzp4xsyb3aq.
The current coarse-band input is 9137.

## Complete minimum-distance reduction

For K=9 let b=0, and for K=35 let b=1. There are nine minority positions
with phase 1-b. List their successive positive forward distances d_i.
They sum to 44, so min d_i<=4. Put g_i=d_i-1: the nine majority gaps
sum to 35, and each is at most seven by the imported phase windows.

For minimum distance d in {4,3}, choose a closest successive minority
pair and rotate its first point to zero. The anchors 0 and d are minority.
Every other point at circular distance less than d from either anchor
is majority. All pairs of minority positions globally must have
distance at least d. In particular f_43=b. This is a complete
normalization for the specified minimum-distance branch.

There are N=33 free phase positions for d=4 and N=36 for d=3.
Exactly seven further minorities are needed. For each d and each b,
keep all 44 lower color orientations X_i=y_i, the N free upper colors
U_i=y_(i+44), and N phase variables S_i=X_i XOR U_i. Fixed upper colors
are substituted by signed lower literals. Global color exchange sets
X_0=0 and preserves f. Exact seven-count thresholds use eight levels:

    C_(i,k) <=> C_(i-1,k) OR (m_i AND C_(i-1,k-1)),
    C_(i,0)=true, C_(i,k)=false for k>i,
    C_(N,7)=true, C_(N,8)=false.

The minority predicate m_i is S_i when b=0 and NOT S_i when b=1.
Four simplified clauses encode each equivalence. Prefix induction gives
its exact threshold semantics and unique extension. There are 8N-28
counter cells and 16+10N variables, namely 346 and 376.
All four models strictly refute. The pigeonhole bound and the two
excluded minimum distances therefore imply **min d_i<=2**, or min g_i<=1.

This small-gap conclusion also implies max g_i>=5: otherwise the
smallest gap contributes at most one, and the other eight at most four,
giving sum g_i<=33<35. Thus max g_i is five, six or seven.

## Maximum majority gaps of seven are excluded

Normalize any longest majority run of length seven to phase positions
0,...,6. Its two adjacent minorities are 43 and 7. There are N=35
free phases and seven further minorities. Both 366-variable models
use the same exact-seven counter, all actual field constraints, and
the maximum-majority-run restriction. Both strictly refute.
Hence any hypothetical endpoint template has max g_i in {5,6}.

## Fourteen branches exclude a maximum gap of six

Normalize any longest majority run of six to 0,...,5, with minorities
43 and 6. Let j be the next minority after 6. Since the maximum
majority gap is six, j lies in 7,...,13. Fix the intervening positions
7,...,j-1 to b and position j to 1-b.

There are N=42-j free phase positions and six further minorities.
Seven-level thresholds now impose C_(N,6) and NOT C_(N,7), with
7N-21 counter cells and 23+9N=284,...,338 total variables.
For each j and both b, the model prohibits any all-majority
seven-position window. It does not prohibit a minority run of seven;
only the separately imported eight-position phase windows use both signs.
All fourteen branches strictly refute. Their normalized alternatives
cover every template with maximum majority gap six, so max g_i=5.

## Four branches and a directed pairing exclude the maximum five

Choose **any** majority gap of five and rotate its run to positions
0,...,4. Adjacent minorities are 43 and 5. Let j be the next minority
after 5. If its following majority gap is at least four, then j=10
or j=11, since the maximum is five. Four models, those two j values
and both b, retain all color orientations and exactly six further
minorities. Their dimensions are 311 and 302. All four strictly refute.

Thus every gap of five must be followed by a gap at most three:

    g_i=5 implies g_(i+1)<=3.

Let k be the number of gaps of five. It is positive because the maximum
is five. Pair each such gap with its following gap. The k successors
are distinct and cannot themselves equal five. Hence these k pairs
occupy 2k distinct slots, and all remaining slots have gaps at most four.
Each pair sums to at most 5+3=8, so the nine gaps sum to at most

    8k+4(9-2k)=36.

But one gap is at most one, as proved above. It is either a selected
successor, whose allowance was three, or a remaining gap, whose
allowance was four. It lowers the bound by at least two in either
case. Therefore sum g_i<=34, contradicting sum g_i=35.
This excludes K=9 and K=35 without needing the other eight possible
length-five next-minority certificates.

The independent audit also enumerates ten indistinguishable deficit
units in nine slots, with u_i=5-g_i in 0,...,5. It obtains 39294 rooted
gap tuples with sum35 and maximum5. Of these, 20952 have minimum at
most one. The directed successor condition leaves **zero** survivors.
The tuple (5,4,5,4,1,4,4,4,4) is a positive control for the looser
successor bound four, showing that this numerical condition cannot
simply be weakened. It is an integer-gap control, not a field coloring.
The finite census supplements the general pairing proof above.

## Exact field definitions and certificate boundary

Every retained field AP receives both signs of its color disjunction.
Repeated cosets collapse, opposite literals give tautologies and
identical clauses are deduplicated. Every model includes the imported
color-seven, root57 color-eight and phase-eight constraints, the exact
XOR relations at free phase indices, the required spacing or maximum-run
clauses, the complete counter and the single color-normalization unit.
Root57 has quotient exponent19 modulo88; the generator uses that stride,
and the auditor reconstructs windows by actual multiplication by57.

The generator uses pinned log/scaling helpers. Separate auditors
construct literal H-cosets and visit every 617*616 ordered(a,d) with
d nonzero. Exactly 4312 APs pass through zero; 375760 remain, giving
26488 distinct signed supports. They compare the **entire** written
clause multiset, dimensions, units, phase semantics and free domain.
XORs are checked by their eight truth assignments; counter clauses
are accounted for by their newest output and their full local truth
relations. Complete small controls check the prefix induction.

Normalization uses only scalar multiplication and global color
exchange. It uses neither reflection nor phase exchange. Scalar
rotation may swap lower/upper representatives, but all color
orientations remain free. Phase periodicity never imposes orientation
periodicity. Both b values are separate cases throughout.

| Group | Cases | Variables | Checked additions | Propagation hints |
|---|---:|---|---:|---:|
| Minimum distance4/3 | 4 | 346,376 | 99038 | 1783632 |
| Maximum majority seven | 2 | 366 | 66700 | 1132469 |
| Maximum six, next minority7..13 | 14 | 284..338 | 199948 | 3207400 |
| Maximum five, next minority10/11 | 4 | 302,311 | 34882 | 548901 |
| Total | **24** | | **400568** | **6672402** |

[EXPECTED.csv](EXPECTED.csv) records canonical CNF/proof digests and
counts. Native CaDiCaL195 and drat-trim are untrusted proof proposers.
The pinned positive-only RUP-LRAT kernel checks actual unit propagation,
live clause IDs and a checked empty conclusion in normal and optimized
Python. Unsupported RAT, absent/deleted hints, malformed domains and
incomplete proofs reject. Its original provenance is graph7835,
bafkreidlaq5uknmu22tpadoyvxe537hkgubmpyhynlekstrengbvtjlvti.
Hashes and stored native statuses do not establish any refutation.

An earlier unsplit maximum-six b=0 model returned UNKNOWN at 50000
conflicts. It supplies no exclusion and was not retried or given
larger caps. The new finite next-minority reduction uses different
models. Large generated models, traces and exploratory corpora stay
outside Git; the compact source regenerates the canonical instances.
Remaining trust includes the cited results, written normalization and
counting/induction bridges, the exact source/checker, and runtime.

## Consequences and primary context

The previous 9..35 band and the newly excluded endpoints give 10..34.
Each phase position is a J=H union(-H) coset of fourteen nonzero points,
so the antipodal disagreement and equality sizes are 14K and 14(44-K),
each in 140..476. The next unresolved phase endpoints are 10 and 34.

[Monroe, Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
lists the inspected two-color/seven-term seed >3703 and prime617.
Monroe writes length before color count, reversing this packet's
W(colors,length) convention. The [author's repository](https://github.com/hmonroe/vdw),
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf),
and [Heule et al., Section4.3](https://www.cs.cmu.edu/~mheule/publications/JOC_08_03_A01.pdf)
provide construction/search context. The Monroe article and repository
were rechecked2026-10-02. No verified later interval record is used;
a bounded check does not prove its absence. The asymmetric three/seven
parameter is different. Novelty is relative to the inspected campaign
phase frontier, not an exhaustive historical-priority assertion.
