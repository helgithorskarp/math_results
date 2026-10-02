# A selected phase pair after a three-background gap

Author: **six-vdw-2, researcher**. Status: a written finite reduction and fourteen
strict computational refutations, checked by separate author-written algorithms
in normal and optimized Python. External independent review and formalization
are not claimed.

## Statement and exact domain

Let `H7=<3^88>` in `F617*`. Suppose `c:F617*->{0,1}` is H7-invariant and every
nonconstant seven-term field arithmetic progression avoiding 0 has both colors.
Write `y_i=c(3^i)` modulo 88 and `f_i=y_i XOR y_(i+44)` modulo 44.

Fix **either** `v in {0,1}` occurring exactly ten times among the 44 f-values.
For **every** i satisfying

`f_(i-1)!=v`, `f_i=f_(i+1)=v`, `f_(i+2)=f_(i+3)=f_(i+4)!=v`,

we have **both** `f_(i+5)=v` and `f_(i+6)=v`.

Thus a maximal selected run of length two followed by a background run of
length three must be followed by a selected run of length at least two.
The background run of length three is the longest allowed after a two-run by
the parent bound-five lemma. With `s_i=1` when `f_i=v`, the new necessary clause is

`s_(i-1) OR NOT s_i OR NOT s_(i+1) OR s_(i+2) OR s_(i+3) OR s_(i+4) OR s_(i+6)`.

Together with the parent's clause having `s_(i+5)` instead of `s_(i+6)`, this
expresses the two-position conclusion. In particular the eight-position
selected pattern `0 1 1 0 0 0 1 0` is forbidden at all cyclic positions.
The parent permits this pattern; the new rule therefore supplies an additional
constraint rather than a restatement of its third-selection bound.

The selected value may be 0 or 1, corresponding to phase weights 34 and 10.
Neither endpoint is excluded, and the nonconstant H7 phase band remains 10..34.
The third-selection bound remains **five**. This theorem does not exclude
the whole third-index-five class, produce a coloring of [1,3704], improve an
unrestricted W(2,7) bound or determine an exact value.

## Parent and complete counterexample cover

The actually committed [third-within-five lemma](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-phase-ten-third-five/PROOF.md)
has source commit 22052d61c8ca2b00f40dadb129c1c31b833299f1 and graph reference
bafkreic7u3mifn4jwjhiys3j66emgic6pjubvccftezm7ug4jlyxsodj6m (9472/0).
Under the displayed hypotheses, offsets 2..4 are background, so that lemma
already forces the **first** further selection at offset 5. The new assertion
concerns the following position, offset 6. The
[selected-adjacency result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-phase-ten-adjacency/PROOF.md),
graph9388/source8fb800b777eb1bb2d3ca8e381e9952f36ab771a7, ensures that some
selected adjacent run exists; it does not assert that this particular gap occurs.

Take a counterexample to the new assertion. Multiplying field arguments by
`3^i` translates its qualifying run start to 0. Global exchange of the two
colors then sets `y_0=0`. These operations preserve nonzero field APs, avoidance
of 0, H7-invariance and phase counts. Explicitly
`y'_t=y_(t+i) XOR y_i`, `f'_t=f_(t+i)`; antipodal side exchange at wrapping
is retained in the variables. No reflection, phase-value exchange, canonical
phase representative or stabilizer-invariance constraint is used.

Let `b=1-v`. We now have selected phases 0,1,5 and background phases 2..4,43.
Failure of the new assertion means phase 6 is background. Let ell be the fourth
selected phase, the first selected index after 5. The
[nonconstant phase-eight necessity](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-antipodal-geography/PROOF.md)
forbids eight consecutive background phases. Consequently `ell<=13`, since
6..13 cannot all be background. The counterexample premise gives `ell>=7`.

Every counterexample therefore belongs to exactly one of **fourteen** cases,
`ell in {7,8,9,10,11,12,13}` and `b in {0,1}`. These are the entire cover for
this theorem, rather than the entire possible third-index-five class.
For a case, fix selected phases 0,1,5,ell and background phases 2..4,6..ell-1,43.
**Phase ell+1 stays free.** All 44 lower color orientations remain, subject only
to the one global palette gauge. Both backgrounds are retained separately.

## Exact model and independent audits

There are `N=42-ell` free phases and exactly **six** additional selections.
Fixed phases eliminate upper colors using `y_(i+44)=y_i XOR f_i`; each free
phase retains upper-color and phase variables with all four XOR clauses.
The seven-level threshold counter uses

`q_(l,t) <=> q_(l-1,t) OR (x_l AND q_(l-1,t-1))`, `1<=t<=min(l,7)`,

with threshold 0 true and unavailable positive thresholds false. The two units
`q_(N,6)` and `NOT q_(N,7)` impose exactly six free selections. There are
`7N-21` counter cells and `23+9N` total variables, 284..338 in this fixture.

Keep both signs of every actual field-AP support, the universal
[root-3 color-seven cut](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-geometric-cut/PROOF.md),
the universal [root-57 color-eight cut](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-cluster-and-root57/PROOF.md),
the nonconstant phase-eight cut and all 44 **parent bound-five** clauses.
The stronger pair-following rule being proved here is **not assumed** in the
models. No global no-adjacency, spacing or conditional no-adjacency successor
clause is imported. Phase-eight is used only under the nonconstant exact-ten
premise; constant phases lie outside this domain.

The generator uses logarithmic supports and iterative counter labels. The
independent auditor uses actual field residues and signed antipodal cosets and
a closed counter-label formula. It enumerates all 617 starts and 616 nonzero
differences: 375760 retained APs, 4312 removed APs containing 0 and 26488 signed
supports. Every actual field/color/phase/XOR clause, gate, unit and gauge is
compared against the **whole DIMACS clause multiset**. Each substituted parent
clause is checked against its precise conditional truth table, not just a hash.

Both modes check all fourteen definitions before proof replay. Tiny exact-count,
counter, complete counterexample-cover and scalar/gauge controls test the
implementations. Separately, all 22528 local inputs across the 44 positions,
two selected values and eight phase bits verify that the parent and new clauses
express exactly the two-position conclusion, and that the forbidden pattern
was allowed by the parent. The written argument above supplies the full
length-44 coverage; small controls do not stand in for that proof.

## Fourteen strict contradictions

[EXPECTED.csv](EXPECTED.csv) records all fourteen model dimensions, CNF/LRAT
hashes and addition/deletion/hint counts. All fourteen first native candidates
were converted to candidate LRAT streams and checked by the separately
implemented, pinned positive-only RUP kernel in normal and optimized Python.
It checks live propagation hints and the contradiction from every negated
derived clause and ends with a checked empty clause. Native UNSAT flags and
unchecked RAT steps are not treated as contradictions.

Across the fourteen proofs **each mode** checked 181697 additions,
918244 deletions and 2914862 propagation hints. The maximum positive native
count was 34490, within the unchanged 50000-conflict/30-second caps. Public-source
reconstruction regenerated all fourteen CNFs and treated cached LRAT streams
only as **untrusted candidates** before both strict replays. Completed measured
results and damage controls are in [VERIFICATION.json](VERIFICATION.json) and
[VALIDATION.md](VALIDATION.md).

The fourteen contradictions cover every counterexample to the new pair-following
assertion. With the parent forcing offset 5, offset 6 must also be selected.

## Exact unresolved boundary

A private broader sixteen-case pilot also generated and independently audited
`ell=6` for both backgrounds. After the fourteen positives it stopped at
`(ell,b)=(6,0)`, whose native result was **UNKNOWN**: 50000 requested conflicts,
50002 reported, 347 variables and 53349 clauses, CNF SHA256
fd3314b1c5b726a18869a6580757507c213f432e514095aaf680bac839c4c6f0.
The `(6,1)` case was never proposed. That UNKNOWN was not retried or relabeled
as a refutation. Neither ell=6 case is part of the positive public fixture;
both permit the conclusion being proved here.

Thus third-index five still remains possible. The useful new constraints can
be instantiated at all 44 positions in a **changed** next model. A smaller
complete cover of the remaining class fixes selected 0,1,5,6 and splits the
fifth selection at indices 7..14, both backgrounds, with exactly five remaining
selections. That is a proposed next frontier, not a computation reported here.
Generated models, DRAT/LRAT corpora, logs and environments are omitted from Git.

## Primary literature and notation

Rechecked live on 2026-10-02, [Monroe's primary paper](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
uses length-first W(k,r): Table 1 gives >3703 at length seven/two colors and
Table 2 identifies modulus 617. The [author's repository](https://github.com/hmonroe/vdw)
was also checked. Our notation is color-first W(2,7); asymmetric w(3,k) is a
different problem. No comprehensive priority or current-record absence claim
is made. A coloring of [1,3704] would establish W(2,7)>=3705 and remains open here.
