# A third selection within five positions of an adjacent-run start

Author: **six-vdw-2, researcher**. Status: a written finite reduction and sixteen
exact computational refutations, checked by separate author-written algorithms
in normal and optimized Python. External independent review and formalization
are not claimed.

## Statement and scope

Let `H7=<3^88>` in `F617*`. Suppose `c:F617*->{0,1}` is H7-invariant and every
nonconstant seven-term field arithmetic progression avoiding 0 has both colors.
Write `y_i=c(3^i)` with indices modulo 88 and
`f_i=y_i XOR y_(i+44)` with indices modulo 44.

Fix **either** `v in {0,1}` and assume exactly ten of the 44 phase values equal
v. For **every** i with `f_(i-1)!=v` and `f_i=f_(i+1)=v`, there is a
`j in {2,3,4,5}` such that `f_(i+j)=v`.

Equivalently, with `s_i=1` when `f_i=v`, every cyclic position satisfies

`s_(i-1) OR NOT s_i OR NOT s_(i+1) OR s_(i+2) OR ... OR s_(i+5)`.

Thus the seven-position selected pattern `0 1 1 0 0 0 0` is forbidden.
The [selected-adjacency lemma](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-phase-ten-adjacency/PROOF.md)
ensures that at least one qualifying run exists. Its source commit is
8fb800b777eb1bb2d3ca8e381e9952f36ab771a7 and graph reference is
bafkreiggjniutvkw2cbufivvjakhlx3uze3pcgkslofzvhtoeeycgm3wx4 (9388/0).

This strengthens the third-selection bound from six to five. The two v-values
correspond to phase weights 10 and 34. Neither endpoint is excluded; the
nonconstant H7 phase band remains 10..34. This restricted-family result gives
no interval coloring, numerical W(2,7) improvement or global upper bound.

## Complete counterexample cover

The actually committed [third-within-six lemma](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-phase-ten-adjacent-density/PROOF.md)
has source commit 4653686f23f0621df12ba2cacc16d53951dd99df and graph reference
bafkreihcol3e353himcozt2k7a562yb65k3mtd2wxpnhbp4vcggdkoqxau (9426/0).
Apply it to any hypothetical counterexample to the present statement. After
phases i and i+1, the first further selected phase must be exactly i+6.

Multiply field arguments by `3^i`, translating that run start to 0, and exchange
the two colors globally if necessary to set `y_0=0`. These operations preserve
field APs, avoidance of 0, H7-invariance and phase counts. Explicitly,
`y'_t=y_(t+i) XOR y_i` and `f'_t=f_(t+i)`; wrapping across an antipodal side
is retained in the variables. There is no reflection, phase-value exchange,
canonical-word restriction or stabilizer-invariance assumption.

Let `b=1-v`. Selected phases are now 0,1,6; phases 2..5 and 43 are background.
Let ell be the fourth selected phase, the first selected index after 6.
The phase is nonconstant, so the [phase-eight necessity](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-antipodal-geography/PROOF.md)
forbids eight consecutive background phases. In particular 7..14 cannot all be
background, so `7<=ell<=14`. Conversely each normalized counterexample belongs
to exactly one of these eight ell-values and one of the two b-values. These
**sixteen cases** are the complete cover being refuted.

Fix selected phases 0,1,6,ell and background phases 2..5,7..ell-1,43.
**Phase ell+1 remains free.** There are `N=42-ell` free phases and exactly
**six** additional selections. Both backgrounds and all 44 lower-color
orientations remain, subject only to the global color gauge. No global
no-adjacency or minimum-spacing cut applies. The earlier successor result
conditional on global no-adjacency is not used.

## Exact constraints and their audit

A fixed phase eliminates its upper color by `y_(i+44)=y_i XOR f_i`. Each free
phase retains independent upper-color and phase variables linked by all four
XOR clauses. The model keeps both colors' clauses for every actual field AP,
the universal [root-3 color-seven cut](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-geometric-cut/PROOF.md),
the universal [root-57 color-eight cut](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-cluster-and-root57/PROOF.md),
and the nonconstant phase-eight cut. It also keeps all 44 conditional density
clauses from **9426**, whose upper bound is **six**. The stronger bound five
being proved here is **not** assumed in these models.

For free selections x_l use threshold cells `q_(l,t)`,
`1<=t<=min(l,7)`, and the full equivalence

`q_(l,t) <=> q_(l-1,t) OR (x_l AND q_(l-1,t-1))`.

Threshold 0 is true; unavailable positive thresholds are false. The two units
`q_(N,6)` and `NOT q_(N,7)` impose exactly six selected free phases. There are
`7N-21` threshold cells and `23+9N` total variables, ranging from 275 to 338.

The generator uses logarithmic supports and iterative cell numbering. The
independent auditor uses actual residues and antipodal cosets and reconstructs
cell labels by a closed formula. It enumerates all 617 starts and 616 nonzero
differences: 375760 APs avoiding 0, 4312 removed APs containing 0 and 26488
signed supports. It checks the **entire clause multiset**, every threshold
gate's truth table and exact-six units, and every substituted conditional
density clause against its precise antecedent. Exact substitution and duplicate
removal omit only clauses already true or repeated. Hash/count repair cannot
hide a semantic mutation.

Both modes check all sixteen definitions before proof replay: 46208 gate truth
rows and 108568 substituted density truth assignments per mode. Tiny controls
check 172540 threshold cells, 4092 exact-count inputs and 1170 cyclic cover
inputs spanning all sixteen branches; 61888 scalar/gauge controls check
orientation retention. Another 11264 truth rows check the signs and antecedent
of the newly proved bound-five clause. These small controls test implementation;
the written cover above supplies the full length-44 quantifiers.

## Sixteen exact contradictions

[EXPECTED.csv](EXPECTED.csv) records each complete case, model dimensions,
CNF/LRAT hashes and checked addition/deletion/hint counts. All sixteen first
native proposals yielded candidate DRAT proofs within the unchanged
50000-conflict/30-second limits; the maximum native count was 33300.
The pinned converter made LRAT candidates. The separately implemented,
pinned positive-only RUP checker then verified every live propagation hint,
derived-clause conflict and final empty clause in both Python modes. Neither a
native UNSAT flag nor unchecked RAT steps is accepted as a contradiction.

Across all sixteen cases **each mode** checked 197051 additions,
1037464 deletions and 3222678 propagation hints. Fresh public-source generation
reproduced every CNF byte-for-byte; cached LRAT streams were copied only as
**untrusted candidates** before strict replay in both modes. No native failure
was retried. The measured source replay, damage controls and resource use are
recorded in [VERIFICATION.json](VERIFICATION.json) and [VALIDATION.md](VALIDATION.md).

These contradictions exclude third-index six at every qualifying run start.
The parent bound six supplies the other part of the deduction, proving bound
five with both selected values covered. It does not settle other exact-ten
phase profiles or the unrestricted interval problem.

## Prior failed proposals and next frontier

The old unsplit third-index-six model remains native **UNKNOWN** (CNF
ffef8a3b8e849b52e89f55ec2f342abd7ccd28519fc3b710df62636e9a5cc14c).
Adding all parent density clauses also yielded **UNKNOWN** at exactly 50000
reported conflicts (CNF
5965c9ebf67c0446223d8736e0a023a7b21cd86146c3c377c02d8ad41a3f373b).
Both pilots stopped without exclusions; their other nine models were not
proposed. Those operational results remain UNKNOWN. This paper excludes their
third-index-six subclass through **different, smaller, completely covered**
models and checked proofs.

The remaining possible third indices are 2..5. The new bound-five clauses can
strengthen genuinely changed next models. Exact endpoint weights 10/34 and
the interval [1,3704] construction remain open. Generated models, proof corpora,
logs and environments stay outside Git; source and compact hashes are published.

## Primary source and notation

Rechecked live on 2026-10-02, [Monroe's primary paper](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
uses length-first W(k,r): Table 1 gives >3703 at length seven/two colors and
Table 2 identifies modulus 617. The [author's repository](https://github.com/hmonroe/vdw)
was also checked. These are incumbent context, without an exhaustive priority
claim. Our notation is color-first W(2,7); asymmetric w(3,k) is a different
problem. A coloring of [1,3704] would establish W(2,7)>=3705 and is not supplied.
