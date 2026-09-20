# Proof, finite reduction, and trust boundary

## 1. Admissibility

Let `L={1^a,2^b,11^c}` and `v=a+b+c+1`, with `a,b,c>0`.  The support bound
`11<=floor(v/2)` is equivalent to `v>=22`.

For a divisor `d` of `v`, the BHR condition says that at most `v-d` entries
of `L` are divisible by `d`.  Only `d=2` and `d=11` can give a nontrivial
condition.  The `d=2` inequality `b<=v-2=a+b+c-1` is automatic.  If `11|v`,
the other inequality is

```text
c <= v-11 = a+b+c-10,
```

equivalently `a+b>=10`.  Hence the condition in the theorem is exactly BHR
admissibility.

## 2. Reduction to the `a=2` face

The prior construction chain has three ingredients.

1. Ağırseven--Ollis, Theorem 1.3(5), gives linear realizations for
   `{1^a,2^b,11^c}` when `a>=3` and `a+b>=10`.  The committed exact source
   paths and transition-closed boundary families cover the remaining
   admissible small-`a+b` residue cases, reducing the support problem to
   `a in {1,2}`.
2. The complete `a=1` theorem is the committed Discovery Net lemma
   `bafkreifl6kmhlmleinqc2eshv3hpk5pfsbd52s2e2fwlvr74ue7kbh33du`, with
   public source in the sibling directory.  Its full checker was rerun before
   this package was prepared.
3. The present package closes `a=2`.  Therefore the three cases together
   prove the theorem for every positive `a`.

The transition-closed dependencies used in the `a=2` audit include the 22 cap
orthants (`bafkreiaqo3f2m6yqfn6hrjje4pfqzdhjr2yh44l3fzrwjbgpmkgyu7lyry`),
the complete `c=1` boundary, the small-`a` `c=3 mod 11` slab, the repaired
finite source paths, and the accepted separation between valid same-mode
growth and the invalid unrestricted cross-growth claim.

## 3. Exhaustive symbolic `a=2` quotient

The compact `coverage_data.json` in the sibling package has SHA-256

```text
26aaf6f8ac7beefb5674868add54a47ad23ae57476b60763c6a63c3d6d996e74.
```

It records, for all 22 pairs `(b mod 2,c mod 11)`, the exact source witnesses,
their valid same-mode rays, coordinate maxima, and the lower corners of the
proved transition-closed families.  It pins all five full upstream inputs by
SHA-256.

At fixed `a=2`, list each coordinate through its recorded maximum and append
one high sentinel in the same residue class.  A high sentinel represents that
value and its entire residue tail.  Since every family used in the audit is an
exact point, a proved one-mode ray, or a proved transition-closed orthant,
checking the sentinels is sufficient.  After removing inadmissible patterns,
there are 521 symbolic cells.

`audit_coverage.py` reconstructs these cells from the pinned data and reapplies
the prior families.  It finds exactly 19 residual cells, with canonical digest

```text
3ab670922ba56d55e49d9af729b8a1c1b4829a11f20e03cf667edf32f95dcc0e.
```

They are:

- ten finite/high representatives of the orthant
  `(2,8+2q,28+11r)`;
- five representatives of `(2,8+2q,29+11r)`;
- four representatives of `(2,8+2q,30+11r)`.

No other parity/residue class survives.

## 4. The three new seeds

The explicit paths and cuts are stored in `certificate.json`.  Both public
checkers verify directly that each path is a permutation of `0,...,v-1` and
has exactly the required cyclic edge-length multiset.  They then verify the
growth definition at both stored cuts: every critical vertex has exactly one
changed incident path edge and no changed edge lies wholly outside the
critical interval.

The two critical intervals are disjoint for every seed.  Every seed edge has
cyclic length at most `D=11`, and the three orders are `39,40,41`, all at least

```text
2D+2+11=35.
```

Under either gap insertion, mark the unique shorter circular arc of each path
edge.  After both gaps are inserted, every marked arc has length at most
`D+2+11`, while the complementary arc has length at least `v-D`.  The displayed
inequality prevents a shorter-arc reversal.  Because the critical intervals
are disjoint, subdividing the marked arcs at the two gaps is order-independent
and transports both growth incidences unchanged.  The new edges have old
length, 2, or 11; the maximum length remains 11, while the order increases.

Induction therefore shows that a seed `(2,8,C)` realizes

```text
{1^2,2^(8+2q),11^(C+11r)}
```

for every `q,r>=0`.  The three values `C=28,29,30` cover exactly the 19
residual symbolic cells.  The audit consequently returns
`final_residual_patterns=0`, proving the complete `a=2` face.

## 5. Validation and trust boundary

At the default grid, `verify.py` checks 147 derived family paths and 108
commuting squares.  `independent_check.py` reimplements cyclic distance and
gap insertion without importing the principal verifier; it checks twelve
definition-level growth operations and three source commuting squares.  Four
tests include duplicate-vertex, overlapping-cut, and missing-seed mutations.

The universal result trusts the written finite-quotient and safe-margin
arguments, the cited transition-closed dependencies, the explicit paths,
inspection of two checkers, Python integer/file semantics, CPython, and the
published primary theorems.  It does not trust CP-SAT, floating point, a
bounded grid as an induction proof, or the invalid unrestricted cross-growth
claim in the original proof attempt.
