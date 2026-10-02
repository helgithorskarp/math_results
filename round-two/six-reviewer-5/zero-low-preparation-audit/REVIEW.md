# Independent HIGH3 preparation audit and a six-comparison word bound

Actual reviewer: **six-reviewer-5**, independent mathematical reviewer,
2026-10-02. Target: committed LEMMA9661/0,
`bafkreibptzddxmwffv2ikkrnukthwoh4wufxqiagtfzmlud2sqrzdpp45i`,
**Native thirteen-input HIGH3: zero-prior-LOW preparations reduce to 181
full functions**, explicitly authored by **six-sorting-2, researcher**.
Target source commit: **16268734027b5bfdb9f8b9e694d623c0ea840989**.
[Target proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-2/high3-zero-low-preparation-cover/PROOF.md).

**Verdict: confirmed in the exact stated preparation-cover scope, with
high confidence.** The entire original-domain census, full-function
closure and all193 arbitrary-suffix exit obstructions reproduce. A new
exact graph-grading check strengthens the theorem: before the first LOW
singleton there are at most **six actual preparation comparisons**, and
the admissible word length is determined by its full function. The target's
at-most-seven replacement statement is valid; seven is the maximum over
the entire cover including excluded functions, rather than its181 retained
functions. This is a strengthening, not a refutation.

The opposite-first-singleton application conditionally imports9529. Its
405-front negative certificate was not independently replayed here; no
new verdict on9529's entire theorem is implied. Likewise the one-sided54
forest frontier9616, the8747 ancestral exclusions and9590's different
singleton/tail barrier are context, not re-reviewed computational theorems.
All global endpoints and all remaining singleton/tail questions stay open.

## Exact statement and hypotheses

Ports are0..12. A standard comparator(a,b), a<b, writes the minimum to a.
The literal P27 is

```
(0,11),(1,7),(2,4),(3,5),(8,9),(10,12),
(0,2),(3,6),(4,12),(5,7),(8,10),
(0,8),(1,3),(2,5),(4,9),(6,11),(7,12),(0,1),(2,10),
(9,11),(11,12),(3,6),
(6,7),(5,7),(9,10),(10,11),(7,11).
```

Assume a standard sorting completion of P27 of total size m<=44. Assume
its first strict increase of the ordinary two-LOW pruning mass is a
singleton and has **zero prior binary LOW merges after P27**. Arbitrary
sequential comparator order, preparation words and repeated gates were
allowed at intake; no depth bound was input. Then its preparation before
that singleton has one of181 complete five-input functions on physical
ports D=(5,6,7,9,10). Function equality means all32 Boolean inputs and
all five outputs, hence all totally ordered inputs by thresholding.
The target proves a count-preserving-or-reducing shortest replacement;
this review additionally proves that the original word itself has length
at most six. Neither statement asserts any retained function completable.

## Independent finite reconstruction

[independent.py](independent.py) was newly written for this target without
importing author code, predecessor code or an earlier reviewer helper.
The original restrictions are the26 single marked inputs and312 two-mark
restrictions, including all LOW/HIGH mixtures. Marks are distinct scalar
ranks below or above every free value. Each restriction retains its
**whole original** Boolean cube. Exactly745,472 assignments are checked.
A gate touching either mark is counted once even if stationary or touching
both; a free gate is deleted only if it is identity on that entire cube.

[controls.py](controls.py) independently reconstructs the retained oriented
free-carrier word for every restriction. It checks all745,472 original
assignments against that word, including6607 retained carrier comparisons
across the338 domains. Marked exchanges transport free carrier identities;
retained oriented pairs are not silently reordered. This finite quotient
check corroborates the imported universal pruning interface; it does not
replace its ordinary standardization proof.

P27 produces exactly136 ten-wire states at physical1..10 and correctly
holds global ranks0/11/12 on all8192 original inputs. The ordinary LOW
secondary costs are1/2:7 and3/4/8:6, mass448. The sole HIGH secondary11
has cost9, mass512. Exactly90 original restrictions are tight:
D+R=5 for twelve free inputs or9 for eleven. Their dead-port projections
give exactly nine activity subsets of the32 five-bit inputs.

We rebuild every full row function starting at identity. Every unblocked
function has all ten possible standard dead-port comparators inspected.
An edge is retained precisely when its swapping inputs intersect every
original activity image. No fixed preparation length is supplied.
The queue exhausts at374 functions,446 directed transitions,193 excluded
functions and181 retained functions. Every original activity subset and
every full function is stored in [EVIDENCE.json](EVIDENCE.json), with
32 row bytes encoded as hex; these are complete data, not truth-table
hashes substituting for equality. The operational20000-state guard was
never approached. Reaching that guard would mean incomplete verification.

All193 cuts are replayed on their entire2048-input original free cubes:
395,264 assignments in total. HH(0,1) certifies180 cuts and HH(8,9)
certifies13. Both have D9,R0 and marked outputs11/12. Physical10 is the
conditional maximum of all unmarked values. Each exit also has an actual
full original13-bit witness with the wrong third-largest bit at10.
That Boolean witness is not required to satisfy the distinct-rank clamping.

A marker-only substitution is concretely unsound: original HH(0,1) and
HH(0,6) both end with marks11/12 and D9,R0, but their projected activity
sets differ:4059103473 versus4042273011. Deduplicating identical projected
activity sets is sound; identifying original cut functions by current
marker positions is not. This countercontrol is checked without native
data. A local reversed-oriented touch also shows why the standard
orientation premise cannot be dropped from the maximum-cut induction.

## Arbitrary-depth reductions and trust boundaries

The ordinary mass transport and whole-original-cube pruning interface of
LEMMA8539 were read and audited. Original domains are transported separately.
A marked-configuration fibre has at most two preimages; a double fibre
charges one deletion and produces weight at least2^u+2^v. Final sorting
has one marked configuration and a free sorting circuit, giving

\[
W_{\rm LOW},W_{\rm HIGH}\le2^{m-S(11)}\le512,
\qquad m\ge D+R+S(k).
\]

The primary imports are S(11)>=35 and S(12)>=39 from
[Harder](https://arxiv.org/html/2012.04400v3). Its large certificate corpus
was not replayed. Harder's standard-form argument is also required when
applying these bounds to the oriented pruned free circuit.

Touching0 doubles448 beyond512, and touching11 or12 doubles512. All
three held ports are frozen. With zero preceding binary LOW events, any
gate before the first strict LOW singleton avoids every live LOW port,
so it is on D. An identity gate on even one tight original cube adds one
free deletion and forces m>=45. Thus every actual preparation edge meets
all ninety original activity constraints. The first singleton has a cost6
live endpoint3/4/8 and one of the five dead partners; a cost7 singleton
would exceed512. This leaves fifteen possible heads, not fifteen excluded
heads.

For a certified exit, suppose m<=44. The first later touch of marked11/12
would add a tenth deletion, contradicting S(11)>=35. Until the first
later touch of10, every gate avoids the marks and10; it preserves the
conditional maximum of10 on every assignment of the whole original cube.
Any first standard touch of10 is therefore an identity on that entire
cube, again adding a tenth deletion. The schedule cannot touch10 at all,
so it cannot repair the supplied full-input wrong-rank witness. This
argument allows every later gate order and depth. It is the maximum
specialization of9616's free-cut proof, which credits9525's minimum lock.
Those mathematical antecedents are explicitly credited; their other
finite applications do not receive transferred verdicts.

Every actually sortable preparation path therefore satisfies the activity
test and avoids the193 exits. Induction embeds it in the completed pruned
graph. The target's shortest full-function replacement preserves its
entire ordered-input function: min/max commute with every order threshold,
and two unequal outputs would give a threshold distinguishing their
Boolean functions. Original conditional domains are preserved too. No
identity of marker configurations or restricted input images replaces
this complete function equality.

These ordinary pruning, standardization, maximum-cut induction and
threshold bridges, and the algorithms' correspondence to the statements,
remain unformalized. No proof assistant, solver UNSAT certificate,
floating-point decision or timeout is a mathematical premise here.

## Strengthening and improvement opportunities

**Proved: actual words have length at most six.** For a full row function f,
let Phi(f) sum the binary inversion count over all32 outputs. Every active
standard comparator(a,b) decreases Phi by exactly

\[
\#\{x:f(x)_a=1,f(x)_b=0\}(b-a)>0.
\]

The identity has Phi=80, giving an acyclic function graph without an input
word cutoff. Longest-path dynamic programming in decreasing Phi and BFS
agree on every374 state. Every one of446 edges increases BFS distance
by exactly one. Consequently every exit-avoiding admissible word has the
same length as its function's shortest representative. The181 retained
functions have distance counts1,5,16,36,57,51,15 at lengths0..6. All
fourteen distance-seven functions are exits. The bound six is attained
within this necessary graph, without an assertion of a feasible sorter.
[REFINEMENTS.md](REFINEMENTS.md) gives the full argument and exact scope.

**Checked but not strengthened:** permitting maximum cuts from all72
tight original domains whose maximum free physical port is10 produces
the same complete cover and193 exits. The negative result of this
sufficient-witness scan gives no feasibility or completeness theorem
about stronger possible obstructions.

**Concrete remaining work:** retain the true prepared operand, and for
each of181 functions inspect all fifteen singleton heads on the whole
original cubes. Rejecting a whole branch requires complete head/tail
normalization and certified bounds for every surviving full target. The
new length grading offers a small exact search interface, but does not
prove those exclusions. A six-port preparation problem after a LOW merge
requires a newly justified full64-input closure and activity constraints;
this five-port count cannot be transferred. Standard orientation and the
zero-prior-LOW condition remain essential to the present reduction.

Formalizing the ordinary free-cut/pruning/threshold bridges would improve
trust. The compact full functions and transition list already permit a
small proof-assistant finite check; the imported S11 corpus remains a
separate named trust boundary. No extra local resources are needed for
reproducing this review.

## Independence, late comparison and reproducibility

The first six-file core/proof seal was **2026-10-02T19:47:44.331986Z**;
target executable/certificate materialization completed
**2026-10-02T19:47:45.338553Z**, afterward. The defining proof, prefix and
aggregate counts were visible throughout. [INDEPENDENCE.json](INDEPENDENCE.json)
records the precise boundary and unchanged file hashes. The first count
guard mistakenly expected retained maximum7; the reconstruction already
matched all374/193/446/181 counts and found retained maximum6. The mistaken
expectation was corrected before native access, retaining seven as the
whole-cover maximum. No native result was used to force a count.

The later [compare_author.py](compare_author.py) imports no target helper.
It compares all11,968 full-function rows, all446 directed transitions,
all374 shortest distances and complete representatives, all193 original
cut records/wrong-rank witnesses, all nine activity images and all136
parent states. The entire native certificate matches the sealed independent
cover; its SHA256 is
`bdfdc23f34cffe622f623d00f4b005d57de1388c307a9662ab93b351c1d37257`.
The initial sealed files remain unchanged. Native generate/verify replay
was strictly serial in normal and optimized Python; whole finite results
and regenerated bytes agree, with all ten native damages rejected for
their intended reasons. Time/RSS telemetry is excluded from mathematical
record comparisons, not from cost reporting.

CPython3.12.14, standard library only, one CPU job/native thread, fixed
45-second per-child guards and unchanged1CPU/2GiB scope. Cold independent
verification passed normally and under-O with395 positive sorter controls,
eight damaged-evidence rejections and full original carrier/cut checks.
Own longest initial cold check12.965s; native longest11.513s/58472KiB.
No timeout, memory kill, resource escalation or overlapping mathematical
children occurred. [VALIDATION.json](VALIDATION.json) records actual costs.

From this source directory, with all native thread environment variables1:

```sh
python3 -B verify.py
python3 -B -O verify.py
```

Expected status: `COMPLETE_ORIGINAL_CUBE_COVER_AND_ACTUAL_SIX_GATE_BOUND_VERIFIED`.
The complete80,790-byte [EVIDENCE.json](EVIDENCE.json) has SHA256
`58fad9b96c9baf378c73d964dbd4429a48607b30e472c6a84c3cf068f809e899`.
Optional exact network-enabled replay of all eleven pinned native files:

```sh
python3 -B reproduce_author.py --scratch /tmp/fresh-high3-preparation-replay
```

Use a fresh empty scratch directory; downloads are checked against complete
source hashes and the four native children run strictly serially. The
independent source never imports native helpers. Credentials, ledgers,
large historical corpora and private prototypes are not needed.

## Literature and publication readiness

Harder's primary paper supplies established small-size bounds and the
standardization/pruning setting. They are prior art, not new results of
this review. The maintained
[Dobbelaere table](https://bertdobbelaere.github.io/sorting_networks.html),
reopened2026-10-02, reports the thirteen-input size interval44..45.
The literal prefix is not a proved normal form for every13-input sorter.

Target-specific searches used HIGH3/181, full-function preparations and
original-domain maximum/identity pruning. They establish no historical
priority. Campaign9525/9616 supply the cut mechanism and9590 the full
function/replacement approach under a different parent. Graph-level
content here is an independent audit plus this literal branch's exact
six-comparison grading, not a newly invented generic comparator potential
or global lower bound. The compact exact evidence supports a scoped
computer-assisted review; ordinary unformalized reductions and imported
results remain explicit publication limitations. Shared signing identity
does not establish distinct authorship. This review's named methodology
and source-access boundary provide the actual independence evidence.
