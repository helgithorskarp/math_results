# Exact order-eight exclusion

Let `F=F_617` and `H=<3^77>`. A coloring `c:F^*->{0,1}` is admissible
if for every `(a,d) in F x F^*` such that all seven terms `a+j*d`,
`0<=j<=6`, are nonzero, these seven terms do not all have one color.
The hypothesis is punctured-field admissibility, not just avoidance of
integer progressions lying in one chosen interval.

**Theorem.** No admissible coloring is H-invariant.

## 1. Exact quotient hypergraph

Trial division through 24 verifies that 617 is prime. Enumerating the
616 powers of 3 verifies that 3 is primitive. Consequently H has order
eight and its cosets are `3^i H`, indexed by `i mod77`. Invariance is
equivalent to assigning a binary word `y_i=c(3^i)`.

For each admissible `(a,d)`, let `E(a,d)` be the set of coset indices of
the seven terms. A set rather than a tuple is sufficient: repeated coset
indices repeat the same color. Admissibility is exactly the conjunction
of the two clauses

```
OR_{i in E(a,d)} y_i ,    OR_{i in E(a,d)} (NOT y_i).
```

The independent auditor runs every `617*616=380072` ordered pair `(a,d)`.
It discards exactly 4312 progressions containing zero, retains 375760,
and finds 23177 distinct supports: 77 of size 4, 231 of size 5, 4543 of
size 6, and 18326 of size 7. Labeling uses the Euler quotient map `x->x^8`:
its kernel is H, and `x^8=3^(8i)` gives coordinate i. No logarithm or
spacing-one reduction is used in this auditor.

The separate generator uses the spacing-one progressions and all cyclic
shifts. This is exact: multiply `a/d,a/d+1,...,a/d+6` by `d!=0` to obtain
the general field progression; multiplying nonzero terms adds the coset
coordinate of d. The auditor compares complete clause multisets, with
literal order ignored but duplicate clauses retained, for every case.
An equality of support counts alone would not establish the reduction.

## 2. Complete longest-run cover

The progression with `a=3,d=34` is

```
3,37,71,105,139,173,207.
```

Its coset coordinates are `1,8,1,2,0,18,8`, giving support
`{0,1,2,8,18}`. Each multiplication by `3^s` is a nondegenerate
punctured-field AP with support `s+{0,1,2,8,18}` modulo 77. The auditor
checks the seven ordered terms and their labels for all 77 scalings.

If a cyclic word contains a monochromatic run of length at least 19
starting at s, every coordinate of that shifted support lies in the
run, producing a forbidden AP. Thus its maximum cyclic run length L is
at most 18. This also excludes constant words. An odd cycle of binary
colors cannot alternate: successive flips around 77 edges would return
the opposite color to the starting vertex. Hence L is at least 2.

Select a longest run, rotate its initial vertex to zero, and if necessary
exchange the colors so that the selected run is zero. These operations
preserve every AP constraint: rotation is field scaling, and color
exchange preserves not-all-equal. The run is maximal and shorter than
the whole cycle, so its neighbors have color one. Therefore

```
y_0=...=y_(L-1)=0,    y_76=y_L=1.
```

No cyclic window of `L+1` consecutive vertices is monochromatic. Conversely,
the two not-all-equal clauses for each such window impose maximum run at
most L, while the fixed prefix and neighbors exhibit a run of length L.
Thus the case CNF describes exactly the normalized admissible words with
maximum run L. There are 77 variables and `46510+L` clauses: 46354 field
clauses, 154 window clauses, and `L+2` normalization units.

This proves a complete cover: every admissible H-invariant coloring has
an equivalent representative in one of the **seventeen** cases
`L=2,...,18`. No quotient orbit count, primality-based approximation or
unproven canonical representative is being substituted for coverage.

## 3. Exact refutations

Each case has a complete refutation by positive reverse unit propagation
(RUP), checked by `check_rup_lrat.py`. CaDiCaL195 and drat-trim propose
the traces but are outside the soundness trust boundary.

For each added clause C, the checker temporarily assigns the negation of
every literal of C, then follows the supplied sequence of active clause
IDs. Each unsatisfied hint must be unit or conflicting; a unit forces
its remaining literal, and a conflicting clause closes the temporary
assumptions. Thus every accepted addition is implied by the active clauses.
A tautological addition is automatically valid. Removing clauses is
harmless for the claim that the original formula implies every accepted
active clause. Induction shows that the checked empty clause is implied
by the original CNF, so the original CNF is unsatisfiable.

The checker requires fresh increasing addition IDs and a checked empty
conclusion. It rejects unknown/deleted hint IDs used in propagation, out-of-domain literals,
unsupported negative RAT hints, malformed syntax and incomplete proofs.
Its tests use explicit `require`, not Python assertions removed by `-O`.
All seventeen traces passed both normal and optimized replay. The
reference traces total **88429** checked additions and **1297242**
propagation hints. Complete per-case CNF hashes, proof hashes and counts
are recorded in `expected.json`. Alternative generated traces may have
different hashes, but must independently verify against the exact audited
CNFs to establish UNSAT.

Sections 1 and 2 transfer the seventeen exact UNSAT statements back to
every H-invariant punctured-field coloring, proving the theorem. This
covers all `2^77=151115727451828646838272` labeled coset colorings,
including the constants and long-run cases excluded in Section 2.

## 4. Imported stabilizer corollary

Let `S(c)={u in F^*:c(ux)=c(x) for all x in F^*}`. This is a subgroup
of the cyclic multiplicative group of order `616=2^3*7*11`. The published
order-at-least-11 classification states that an admissible coloring with
`|S(c)|>=11` is the quadratic-residue coloring up to color exchange.
This result is explicitly imported; it is not silently assumed from a
failed search. Its complete source and graph reference are in README.md.

For a nonquadratic admissible coloring, that classification implies
`|S(c)|<=8`. If `|S(c)|=8`, uniqueness of the order-eight subgroup in a
cyclic group gives `S(c)=H`, contradicting our theorem. Therefore
`|S(c)|<=7`; divisibility by 616 leaves only orders `1,2,4,7`.
Equivalently, an admissible coloring invariant under a subgroup of order
at least eight must be quadratic up to color exchange. The generator
`3^77` of H is a nonsquare, so quadratic coloring is itself not H-invariant.

No statement here asserts existence of nonquadratic colorings at any of
the remaining orders. Order seven/index 88 is the next unresolved
stabilizer frontier. No interval upper bound or construction on
`[1,3704]` follows from this theorem.
