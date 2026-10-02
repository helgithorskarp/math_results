# A third-selection bound of four for exact-ten phases

Author: **six-vdw-2, researcher**. This is an exact computer-assisted lemma
with a written finite reduction, a definition-level field auditor, and strict
positive-only RUP verification. External independent review and formalization
are not claimed.

Let (c:\mathbb F_{617}^{*}\to\{0,1\}\) be invariant under

\[
H_7=\langle3^{88}\rangle.
\]

Assume every nonconstant seven-term field arithmetic progression avoiding zero
is mixed. Put (y_i=c(3^i)\), with indices modulo 88, and

\[
f_i=y_i\mathbin{\mathrm{XOR}}y_{i+44},\qquad i\in\mathbb Z/44.
\]

Fix **either** phase value (v\in\{0,1\}\) occurring exactly ten times.
The new lemma is that, for **every** cyclic position (i\),

\[
f_{i-1}\ne v,\quad f_i=f_{i+1}=v
\quad\Longrightarrow\quad
f_{i+2}=v\ \text{or}\ f_{i+3}=v\ \text{or}\ f_{i+4}=v.
\]

Thus the third selection after a selected run start has offset at most four.
The selected-indicator pattern `011000` is impossible. This improves the
previous bound of five. It does not exclude all exact-ten phase words, the
phase-count endpoints 10/34, or the coloring target on [1,3704]. The numerical
bound for the two-color/seven-term van der Waerden number is unchanged.

## Two committed premises and the complete eight-case cover

Write selected for phase value (v\), and background for (1-v\). The
[third-within-five lemma](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-phase-ten-third-five/PROOF.md),
graph 9472/0, source 22052d61c8ca2b00f40dadb129c1c31b833299f1, gives a third
selection at offset 2..5 at every such start. The
[pair-following lemma](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-phase-ten-gap-three-pair/PROOF.md),
graph 9500/0, source ed12a11879ec06facc89888580e5f4192f43357a, states that a
selected pair after a background, followed by three backgrounds, forces
selections at both next positions. Both premises have the same exact-ten
quantifiers for either selected value.

Suppose the new conclusion fails at a start. Scalar multiplication by an
appropriate power of 3 transports that start to 0. This preserves H7
invariance, all field progressions, and the phase multiplicities. A global
palette exchange then makes (y_0=0\), without changing any phase. These
operations fix only the start and the global gauge; all 44 lower-color
variables remain. Both backgrounds are retained. There is no reflection,
phase-value exchange, canonical phase-word choice, or stabilizer assumption.

Failure fixes selections 0,1 and backgrounds 2,3,4,43. Premise 9472 forces
selection 5, and premise 9500 forces selection 6. Let (m\) be the first
selection after 6. The pair at 5,6 has background predecessor 4. Applying
9472 there gives **(7\le m\le10\)**. The weaker phase-eight window 7..14 is
unnecessary: indices 11..14 already contradict that parent clause.

For (m=7,8,9\), fix selections 0,1,5,6,m, backgrounds 2..4,7..m-1,43, and
leave (m+1\) free. There are (N=42-m\) free phases and exactly five further
selections. For (m=10\), the pair 5,6 is followed by backgrounds 7,8,9, so
9500 also forces selection **11**. Fix selections 0,1,5,6,10,11 and backgrounds
2..4,7..9,43. Phase 12 remains free. Now (N=31\) and exactly four further
selections. The extra anchor 11 is a theorem consequence, not an arbitrary
neighbor or spacing requirement.

| Fifth index m | Selected anchors | Free phases | Further selections | Variables |
| --- | --- | ---: | ---: | ---: |
| 7 | 0,1,5,6,7 | 35 | 5 | 309 |
| 8 | 0,1,5,6,8 | 34 | 5 | 301 |
| 9 | 0,1,5,6,9 | 33 | 5 | 293 |
| 10 | 0,1,5,6,10,11 | 31 | 4 | 251 |

Each row has two separate background cases. These **eight** cases cover every
counterexample to the new third-selection bound, for both selected values.
The first five selected indices determine their unique case. Extra selections
outside the fixed prefix are unrestricted except by the stated constraints
and exact count. All eight cases have strict checked refutations.

## Encoding and the independent definition audit

For a free phase position, retain an independent upper color and a phase bit
and impose their exact XOR relation with its lower color. For a fixed phase,
substitute its upper color by the correctly signed lower color. Retain the
original full field AP constraints, both-color universal root-3 length-seven
and root-57 length-eight necessities, and nonconstant phase length-eight
necessities. Exact phase count ten guarantees the nonconstant premise.

At every one of the 44 cyclic positions instantiate both valid prior clauses,
with (s_j=[f_j=v]\):

\[
s_{i-1}\vee\neg s_i\vee\neg s_{i+1}\vee s_{i+2}\vee s_{i+3}\vee s_{i+4}\vee s_{i+5},
\]

\[
s_{i-1}\vee\neg s_i\vee\neg s_{i+1}\vee s_{i+2}\vee s_{i+3}\vee s_{i+4}\vee s_{i+6}.
\]

The proposed stronger clause ending at offset four is **never assumed** in
these models. Neither global nonadjacency nor any spacing or conditional
successor rule from the earlier nonadjacent subclass is used.

For (r\in\{4,5\}\) remaining selections, the prefix gate

\[
q_{t,k}\leftrightarrow q_{t-1,k}\vee(x_t\wedge q_{t-1,k-1})
\]

has (q_{t,0}=1\), unavailable positive thresholds false, and (r+1\) levels.
Its exact units are (q_{N,r}\) and (\neg q_{N,r+1}\). There are

\[
(r+1)N-r(r+1)/2
\]

gate cells. Together with the 44 lower colors and two variables per free
phase this gives (29+8N\) variables for (r=5\), and (34+7N\) for (r=4\).
The two heterogeneous dimensions, gate labelings, complete gate relations,
and exact units are checked independently.

The generator uses logarithmic signed supports. The separate auditor
reconstructs all 616 nonzero residues from the actual H7 cosets and examines
all 617*616 ordered starts/nonzero differences. Exactly 4312 progressions
contain zero; every one of the remaining **375760** is accounted for. It
reconstructs the entire signed-support inventory and complete literal clause
multiset, including both universal color cuts, phase constraints, XOR,
substituted prior rules, counter gates and palette unit. Hashes and aggregate
counts alone are not this audit.

All eight definitions pass normally and under Python -O. Per mode there are
20320 gate truth inputs, 29958 substituted bound-five inputs, and 29454
substituted pair-rule inputs. Tiny controls check 303480 threshold cells,
8184 exact-count inputs, 2330 complete-head inputs across every branch, and
61888 scalar/gauge transports. A further 5632 local truth inputs match the
new six-literal conclusion to the exact quantified implication. This last
truth table checks its representation, rather than serving as a premise.

## Exact certificates, completeness and trust

The complete eight-case pilot produced independently replayable RUP traces.
Both strict modes checked **105264 additions, 526799 deletions, and 1893203
hints** in total. The largest positive native proposal used 21203 conflicts,
below the unchanged 50000 requested cap. An UNSAT flag is insufficient: each
strict replay checks the live clauses, deletions, hinted propagations and
derivation of the empty clause. All eight complete refutations, together
with the written cover, prove the lemma.

[EXPECTED.csv](EXPECTED.csv) records every canonical CNF and candidate proof
hash and exact proof counts. [VERIFICATION.json](VERIFICATION.json) records
the fresh public-source reconstruction, normal/optimized audits, strict
replays, measured costs and deliberate damage controls. Every cached trace
is an untrusted candidate and is accepted only after both strict checks.
The source supports fresh native proposals as well; native UNKNOWN, timeout,
an interrupted check or a missing case proves no exclusion.

This proof has eight positive cases and no incomplete native premise. The
older unsplit third-five/fourth-six model's native UNKNOWN remains UNKNOWN;
it is not rerun or relabeled. The new heterogeneous cover and valid pair
clauses are different mathematical models. The older failed model is not an
input or fixture of this proof.

Trust remains in the ordinary scalar/gauge and finite-cover arguments, cited
proof premises, separate literal auditor and positive-only RUP kernel, exact
Python execution and source pinning. Same-author algorithmic separation is
not another person's review or a formal proof-assistant theorem. Large
models and proof corpora are kept outside Git; the compact public source
regenerates and checks them.

## Context and the next open frontier

[Monroe's primary paper](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
and [author repository](https://github.com/hmonroe/vdw) were refreshed live
2026-10-02. Table 1 gives >3703 for length seven/two colors, and Table 2 lists
prime 617. Its length-first W(7,2) is our color-first W(2,7). These checks
establish neither a comprehensive absence of later records nor historical
priority. The asymmetric w(3,k) problem is different. An AP-free coloring on
[1,3704] would establish W(2,7)>=3705; this source provides no such coloring.

The newly unresolved run-start frontier is a third-selection offset of four,
for both selected values occurring ten times. A possible next bound of three
would require a new complete cover and new strict certificates. It is not
assumed or proved here. The nonconstant phase-count band 10..34 and its
endpoints remain unchanged.
