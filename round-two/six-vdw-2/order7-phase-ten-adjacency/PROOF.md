# Selected adjacency at the H7 phase-ten endpoints

six-vdw-2, researcher; 2026-10-02. Author-checked computer-assisted lemma.
The model generator and actual-residue auditor use separate algorithms. The
certificate kernel checks positive RUP propagation explicitly. External
independent review and formalization are not claimed.

Let `H7=<3^88>` in `F617*`. Suppose a binary coloring `c:F617* -> {0,1}`
is constant on every H7 coset and is mixed on every seven-term field
arithmetic progression `(a,a+d,...,a+6d)` with `d!=0` and all terms nonzero.
Use positive base-3 logarithmic order:

    y_i=c(3^i), i modulo88;
    f_i=y_i XOR y_(i+44), i modulo44.

**Lemma.** For each `v in {0,1}`, if exactly ten indices satisfy `f_i=v`,
there is an index `i` with `f_i=f_(i+1)=v`.

Equivalently, at phase weights `K=sum_i f_i` equal to 10 or 34, the phase
value occurring ten times has an adjacent cyclic pair. This excludes the
no-adjacency subclass at those two endpoints. It does not exclude the
endpoints themselves or strengthen the inherited phase band `10<=K<=34`.
It supplies a necessary structural condition within H7/F617; no global
van der Waerden bound, length-3704 witness or exact value follows.

## Complete fourteen-case counterexample cover

Assume, for contradiction, that the ten selected phases (those equal to
`v`) have no adjacency. Write their positive cyclic gaps as
`g_0,...,g_9`, so their sum is 44, and put `b=1-v`.

The [phase-eight lemma8787](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-antipodal-geography/PROOF.md)
gives `g_i<=8`: a larger gap contains eight consecutive background phases.
No adjacency gives `g_i>=2`. The
[close-pair lemma9219](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-uniform-close-pairs/PROOF.md)
gives a gap two. The
[gap-successor lemma9291](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-phase-ten-gap-successors/PROOF.md)
says every gap two is followed by two or three, under exactly the current
count-ten/no-adjacency hypotheses.

Some consecutive gap pair must be `(2,3)`. Otherwise, beginning at a gap
two and applying9291 repeatedly forces all ten gaps to equal two, whereas
their sum would then be 20. This is the existential normalization of the
[published rotation-cover lemma9347](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-phase-ten-rotation-cover/PROOF.md).

Choose such a pair and scalar-rotate the field coloring to place its first
selected phase at zero. The first selected indices are `0,2,5`. Let `k`
be the next selected index. Its gap from five is between two and eight, so

    k in {7,8,9,10,11,12,13}.

Fix selected phases `0,2,5,k`, every phase strictly between five and k
as background, and all radius-one neighbors of those four selected
indices as background. The complete fixed domain is `{0,...,k+1,43}`;
four of its entries are selected. The free phase domain is
`{k+2,...,42}`, of size `N=41-k`, and exactly SIX of these entries must
be selected. Retaining both `b=0` and `b=1` gives all fourteen cases.

Scalar rotation preserves the whole field AP hypothesis and translates
the phases. All 44 lower color-orientation bits remain available. The
global exchange of both colors permits `y_0=0` and does not exchange
phase values. No reflection, exchange of phase values, least-rotation
condition or invariance of the orientations under a phase stabilizer is
imposed. Thus every counterexample to the lemma maps to an included case.
The previous127049 candidate phase-rotation classes per background all
belong to this excluded no-adjacency subclass; their earlier necessary
count never asserted field extendibility.

## Models and independent definition audit

There are 44 lower color variables. At a fixed phase `i`, the upper color
is the signed lower color determined by that phase. At each free phase,
use separate upper-color and phase variables and four clauses defining
their exact XOR relation to the lower color.

Each model includes both signed clauses for every actual field AP support.
It also retains the cited universal necessities:

- root-3 color-seven from [8664](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-geometric-cut/PROOF.md);
- root-57 color-eight from [9069](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-cluster-and-root57/PROOF.md), with `57=3^19 mod617`;
- phase-eight from8787;
- no selected adjacency;
- all 44 conditional successor clauses from9291.

For the last item let `s_i` indicate `f_i=v`. The shifted clause is

    NOT s_i OR NOT s_(i+2) OR s_(i+4) OR s_(i+5).

Its mathematical premise is exactly ten selected phases with no adjacency,
which is the counterexample hypothesis. Root-57 color-eight is universal;
no endpoint-specific cluster condition from9069 is transferred here.

A seven-level prefix counter defines `C(i,t)` as at least t selected
entries among the first i free entries. Every cell is constrained by the
full equivalence

    C(i,t) <-> C(i-1,t) OR (selected_i AND C(i-1,t-1)).

Constants `C(i,0)=true` and unavailable thresholds false are simplified
exactly. The final units `C(N,6)` and `NOT C(N,7)` require precisely six
free selected phases. There are `7N-21` counter cells, hence

    variables = 44+2N+7N-21 = 23+9N = 275..329.

The [independent auditor](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-phase-ten-adjacency/head_audit.py)
does not import the generator or its discrete-log helpers. It reconstructs
cosets from actual residues and enumerates all `617*616=380072` start-step
pairs:4312 meet zero and375760 are wholly nonzero, with26488 distinct
signed coset supports. Quadratic-residue colors give a positive field
control. It reconstructs the full DIMACS clause multiset independently,
checks every exact-six gate on all local Boolean assignments, and checks
every substituted successor clause against its value-level truth table.

Normal and Python `-O` audits agree on all fourteen models,39704 counter
gate truth rows and6056 substituted successor truth rows. Small independent
controls check172540 threshold cells,4092 exact-count inputs,1254 cyclic
head inputs covering all fourteen branches, and32 unsubstituted successor
truth rows. These finite controls supplement the general44-cycle coverage
argument above; they are not its substitute. The common field helpers and
their premise proofs are byte-pinned in
[SOURCE_PINS.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-phase-ten-adjacency/SOURCE_PINS.json).

## Fourteen exact refutations

Every case has a complete strict positive-RUP certificate checked normally
and under Python `-O`. The positive-only RUP kernel is credited to graph7835
(`bafkreidlaq5uknmu22tpadoyvxe537hkgubmpyhynlekstrengbvtjlvti`). The
[pinned8664 checker](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-geometric-cut/check_rup_lrat.py)
used here rejects negative RAT hints and require explicit live propagation hints,
proper domains, deletions, fresh addition identifiers and a final empty
clause. Native UNSAT and DRAT conversion supply candidate bytes only.

| k | b | variables | clauses | checked additions | checked hints |
|---:|---:|---:|---:|---:|---:|
|13|0|275|52878|8857|119331|
|13|1|275|51072|5096|69420|
|12|0|284|52951|7930|108095|
|12|1|284|51365|4668|68189|
|11|0|293|53000|7999|125208|
|11|1|293|51644|7517|103500|
|10|0|302|53067|8686|136549|
|10|1|302|51931|7300|111564|
|9|0|311|53124|11010|167072|
|9|1|311|52214|8817|143507|
|8|0|320|53185|13974|241982|
|8|1|320|52499|13903|236260|
|7|0|329|53239|19443|338876|
|7|1|329|52779|15844|290557|

Together these traces check141044 additions and2260110 propagation hints
PER MODE. The canonical CNF/proof hashes are in
[EXPECTED.csv](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-phase-ten-adjacency/EXPECTED.csv).
The new pilot used unchanged50000-conflict/30-second native guards; the
largest native count was19007 conflicts. Converter guards were25 seconds
internal/30 external, exact replay30 seconds per mode, and definition
stages55 seconds. All jobs were serial, solver/BLAS/OpenMP threads one,
within the standing1CPU/2GiB scope. None of the old UNKNOWN heads was
retried or treated as a refutation.

Every counterexample maps to one of the fourteen refuted models. This
contradiction proves the lemma. The ten cases `k>=9` alone would exclude
third gaps at least four after `(2,3)`; the four extra cases `k=7,8`
complete the stronger no-adjacency exclusion established here.

## Reproduction, provenance and trust

See [README.md](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-phase-ten-adjacency/README.md)
for exact reproduction with Python3.11.2, python-sat1.8.dev24, six1.17.0,
CaDiCaL195 and the pinned drat-trim C source. Compact source reconstructs
all models and traces; CNFs, DRAT/LRAT corpora, logs, binaries and local
environments remain scratch-only. Optional cached candidate traces are
always replayed by the strict checker and are never trusted by filename.
Adversarial controls repair digests and clause counts when corrupting
model semantics, ensuring that hashes alone do not supply the audit.

The written scalar-rotation, cardinality, premise-transfer and complete-cover
bridges; cited mathematical inputs; pinned model auditor and exact RUP
kernel; and runtime execution remain trust boundaries. Same-author
algorithmic independence does not constitute an external reviewer verdict.

Primary family sources remain
[Monroe's Tables1 and2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
and the [author source](https://github.com/hmonroe/vdw), live rechecked
2026-10-02. Table1 lists two colors/seven terms `>3703`, and Table2 uses
modulus617. Monroe writes length-first `W(7,2)`; this lane uses color-first
`W(2,7)`. This check is not an exhaustive current-record or historical
priority claim. The asymmetric red-three/blue-seven problem is different.

Mathematical parent provenance:

| parent | graph height | source commit |
|---|---:|---|
|phase-eight|8787|84f623e07584d9b1dcfa9076d6bdd26ddb0e9b24|
|close pair|9219|e52646ec53af7b36721b340d40502de1b3793328|
|gap-two successor|9291|a4de996554b311d5876f255f5f3d9d031a599c05|
|(2,3) normalization and phase cover|9347|04ed2a789c31730eed4ce7014ac9205a4530654a|
|root-3 color-seven|8664|e6f1eb9d87d194cf901d812818ad6fd2427473d3|
|universal root-57 color-eight|9069|7880c843e883567f0af6188813cd5a056dbf3e17|

The [endpoint software9015](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-phase-endpoints/PROOF.md)
is credited for reusable exact field and gate mechanisms; the current
fourteen-case audit is new. The
[phase band9187](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-phase-ten/PROOF.md)
is context, not a strengthened conclusion. Published complementary XOR618
work and private unknown models are not premises of this proof.
