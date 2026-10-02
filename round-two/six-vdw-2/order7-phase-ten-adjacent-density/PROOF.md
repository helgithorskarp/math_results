# A third selection near every phase-ten adjacent-run start

Author: **six-vdw-2, researcher**. Status: a written finite reduction with six
strict computational refutations, checked by separate author-written algorithms
in normal and optimized Python. External independent review and formalization
are not claimed.

## Statement and domain

Let `H7=<3^88>` in the multiplicative group of F617. Let
`c:F617*->{0,1}` be H7-invariant, and suppose each nonconstant seven-term field
arithmetic progression avoiding 0 has both colors. Define, with indices cyclic,

`y_i=c(3^i)` for i modulo 88, and
`f_i=y_i XOR y_(i+44)` for i modulo 44.

Fix **either** v in {0,1}, and assume exactly ten of the 44 phase values equal
v. For every i such that `f_(i-1)!=v` and `f_i=f_(i+1)=v`, there is a j in
{2,3,4,5,6} such that `f_(i+j)=v`.

Writing `s_i=1` when `f_i=v`, the equivalent necessary clause at every i is

`s_(i-1) OR NOT s_i OR NOT s_(i+1) OR s_(i+2) OR ... OR s_(i+6)`.

Thus the eight-position selected pattern `0 1 1 0 0 0 0 0` cannot occur.
The previously committed [selected-adjacency lemma](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-phase-ten-adjacency/PROOF.md)
ensures that at least one selected run of length at least two exists. Its source
commit is 8fb800b777eb1bb2d3ca8e381e9952f36ab771a7 and its graph reference is
bafkreiggjniutvkw2cbufivvjakhlx3uze3pcgkslofzvhtoeeycgm3wx4, committed at
9388/0. This use of the parent supplies existence; the present conditional
constraint applies to **every** qualifying run start.

The two selected-value choices give phase weights 10 and 34, respectively.
Neither endpoint is excluded. The previous nonconstant H7 phase band 10..34
remains unchanged. No interval coloring or global W(2,7) upper bound follows
from this restricted-domain lemma.

## Complete reduction of the forbidden pattern

Take any qualifying i. Multiplying field arguments by `3^i` translates its
phase index to 0. This preserves nonzero field differences, avoidance of 0,
H7-invariance and exact phase counts. Global exchange of the two colors then
sets `y_0=0`, without changing any f-value. Algebraically the transformed word is
`y'_t=y_(t+i) XOR y_i` and `f'_t=f_(t+i)`; wrapping by 44 can exchange the two
antipodal color sides, which the retained variables allow. There is no reflection,
phase-value exchange, canonical-word restriction or imposed stabilizer symmetry.

Let `b=1-v`. We now have selected phases 0,1 and background phase 43. Let k be
the first selected index after 1. The phase is nonconstant because the counts
are ten and 34. The [nonconstant phase-eight necessity](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-antipodal-geography/PROOF.md)
forbids eight consecutive background phases, so `2<=k<=9`. If the displayed
necessary clause were false, phases 2..6 would all be background, forcing
`k in {7,8,9}`. Conversely every counterexample to the clause has one of these
three k-values and one of the two b-values. These six cases are the complete
finite coverage being refuted here.

For a case `(k,b)`, fix phases to v at 0,1,k and to b at 2..k-1 and 43.
**The phase at k+1 stays free.** There are `N=42-k` free phases, of which exactly
seven equal v. No minimum-distance-two neighborhood or global spacing clause
is valid in this class. The conditional successor lemma for the globally
no-adjacency class is likewise inapplicable and is never encoded.

## Exact model

Keep the 44 lower color variables `y_0,...,y_43`. A fixed phase eliminates its
upper color using `y_(j+44)=y_j XOR f_j`. Every free index has its own upper
color and phase variables, linked by all four clauses of the XOR truth table.
All 44 lower color orientations remain, subject only to the one global color
gauge. Both backgrounds are retained separately.

The field constraints encode both signs of every actual seven-term AP support
avoiding 0. Duplicate supports are collapsed; a support with opposing literals
is tautological under the fixed phases and can be omitted. The independent
auditor constructs H7 and signed antipodal cosets with actual residues, without
using the generator's logarithm/support helpers. It enumerates all 617 starts
and 616 nonzero differences: 375760 retained APs, 4312 removed APs containing
0, and 26488 signed supports. All original AP clauses are represented after
exact substitution, simplification and duplicate removal.

Also retain the universal [root-3 color-seven cut](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-geometric-cut/PROOF.md),
the universal [root-57 color-eight cut](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-cluster-and-root57/PROOF.md),
and the nonconstant phase-eight cut. The root-57 cut is the universal color
necessity, rather than a special endpoint clustering condition. Phase-eight is
used only under the present nonconstant exact-ten premise; a constant-zero
quadratic-residue phase does not satisfy that premise. All premise/helper bytes
used by this computation are pinned before mathematical imports.

For the free phases, let `x_l=1` mean that free input l equals v. Use threshold
cells `q_(l,t)` for `1<=t<=min(l,8)`, with the exact recurrence

`q_(l,t) <=> q_(l-1,t) OR (x_l AND q_(l-1,t-1))`,

where threshold 0 is true and unavailable positive thresholds are false. Encode
the full four-clause equivalence, simplifying only these Boolean constants.
The units `q_(N,7)` and `NOT q_(N,8)` enforce **exactly seven** selected free
phases. The counter has `8N-28` cells, hence `16+10N` total variables.

The generator uses iterative cell numbering. The auditor reconstructs cell
labels by a closed formula and checks every gate's complete truth table and
every unit. It compares the **entire** DIMACS clause multiset against the
independently reconstructed field/color/phase/XOR/counter clauses and the gauge.
Repaired hashes and clause counts therefore cannot conceal a semantic mutation.

## Six exact refutations

[EXPECTED.csv](EXPECTED.csv) gives the dimensions, exact CNF and LRAT hashes and
checked addition/deletion/hint counts of all six cases. The dimensions are:

| k | b | variables | clauses | native conflicts |
|---:|---:|---:|---:|---:|
| 9 | 0 | 346 | 53464 | 10372 |
| 9 | 1 | 346 | 52338 | 10609 |
| 8 | 0 | 356 | 53529 | 19222 |
| 8 | 1 | 356 | 52629 | 18041 |
| 7 | 0 | 366 | 53592 | 32388 |
| 7 | 1 | 366 | 52916 | 33671 |

Each first native proposal produced a DRAT stream. The pinned converter produced
an LRAT candidate, and the pinned [positive-only RUP kernel](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-geometric-cut/check_rup_lrat.py)
checked each proof in normal and optimized Python. It requires every live
positive propagation hint, checks assignments and conflicts from the negation
of each proposed clause, and ends with a verified empty clause. It does not
accept a native UNSAT flag or unchecked RAT steps as evidence.

Across the six proofs, **each Python mode** checked 125492 additions, 443708
deletions and 2094091 propagation hints. Public-source reconstruction regenerated
all six CNFs byte-for-byte and copied the private LRAT streams only as untrusted
candidates before repeating both strict replays. Proof hashes and expected counts
matched. The maximum resource use and damage controls are in
[VERIFICATION.json](VERIFICATION.json) and [VALIDATION.md](VALIDATION.md).

These six contradictions rule out every counterexample to the displayed
conditional clause, completing its proof. A full endpoint exclusion is not
part of this inference.

## Remaining frontier and publication boundary

A private sixteen-case first-next cover also generated and audited k=2..6.
The serial pilot stopped at `(k,b)=(6,0)`, whose requested conflict budget was
50000 and whose native counter reported 50002. Its result was **UNKNOWN** in
6.224514 seconds, not a refutation. The other nine remaining cases were never
proposed. The UNKNOWN CNF digest is
ffef8a3b8e849b52e89f55ec2f342abd7ccd28519fc3b710df62636e9a5cc14c.
It is absent from the positive reproduction fixture and will not be retried
unchanged or relabeled as excluded. This result supplies new, rigorously valid
conditional constraints for a **changed** next model.

Source and compact summaries are published; the generated models, DRAT/LRAT
corpora and logs remain outside Git. [README.md](README.md) gives exact commands,
required versions, caps and the untrusted candidate-cache option. Trust remains
in the written coverage/substitution arguments, the cited universal necessities,
the separately implemented pinned checker, Python and execution. No separate
person's review or proof-assistant audit is asserted.

## Literature and notation

This concerns color-first W(2,7), the symmetric two-color/seven-term problem.
The asymmetric w(3,k) literature addresses a different family. Rechecked live
on 2026-10-02, [Monroe's primary paper](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
uses length-first W(k,r): Table 1's length-seven/two-color entry is >3703,
and Table 2 records modulus 617. The [author's source repository](https://github.com/hmonroe/vdw)
was also checked. These are incumbent context rather than an exhaustive
historical-priority claim. The existing H7 band and this conditional lemma are
restricted-family mathematical progress; a coloring of [1,3704] would instead
establish W(2,7)>=3705 and remains unresolved here.
