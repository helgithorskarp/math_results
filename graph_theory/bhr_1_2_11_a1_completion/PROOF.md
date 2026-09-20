# Proof, finite reduction, and trust boundary

## 1. Admissibility on the `a=1` face

For `L={1,2^b,11^c}`, put `v=b+c+2`. The length bound is `v>=22`.
For a divisor `d` of `v`, only `d=2` and `d=11` can divide a member of the
support nontrivially. The `d=2` condition is automatic because
`b<=v-2=b+c`. If `11|v`, the `d=11` condition is

```text
c <= v-11 = b+c-9,
```

equivalently `b>=9`. Thus the condition in the README is exact.

## 2. Sound prior cover

The proof combines previously checked transition-closed families. Their
Discovery Net references are:

- finite source paths and one-mode rays:
  `bafkreicxvyw74shmrdag6mjxb6k2qawrcscz7a53q3vtad5wte7b7jzdiy`;
- the objection separating the valid finite certificate from the invalid
  general cross-growth assertion:
  `bafkreie7zy3t5aejqdd6avfbn5rawarep7fxlffrm5fj3mtmwxelpgtiga`;
- safe-margin cross-growth repairs:
  `bafkreic2hfwbjcnyygvvhvu5ug4bqzh577apoziiazjpiq7gndtsdfzhci`;
- complete 22-cap orthants:
  `bafkreiaqo3f2m6yqfn6hrjje4pfqzdhjr2yh44l3fzrwjbgpmkgyu7lyry`;
- complete positive `c=1` slice:
  `bafkreigcfhhsbxhxqcjlri5bnmuyu3ziasbzmz36hvw5pmq3goul3xhhzi`;
- the `c=3 mod 11` small-`a` slab:
  `bafkreib2v4u2zot7xfnsx4hs6pqfybd6f75gwakr5r5s7rivivjzdcxsx4`;
- the eleven-residue odd-`b` mantle:
  `bafkreidfnmvhvbsbzw6livdvaagxu4pbu7shs4u2dyhc4n7koyc7xw4spi`.

Only statements proved after the cross-growth objection are used for
multi-mode iteration. From the original finite certificate, the audit uses
only exact displayed paths and repeated growth in one mode, both of which were
independently checked and are unaffected by the objection.

For each parity of `b` and residue of `c mod 11`, the pinned source
certificate gives coordinate maxima. Values through a maximum are listed
individually; the next value is a high sentinel representing that value and
every larger value in the same residue class. This yields 502 admissible
symbolic cells on the `a=1` face. Every prior family is either an exact point,
a one-mode ray, or an explicitly transition-closed orthant, so membership of
a high sentinel proves membership of its entire tail.

`build_coverage_data.py` extracts only the counts, growth-mode sets, and
orthant minima needed for this finite cover. It pins the full upstream inputs
by SHA-256. `audit_coverage.py` reconstructs all 502 cells from these data and
applies the prior families in dependency order. Exactly 29 cells remain,
with canonical SHA-256

```text
7d6b7ae4fb95c220d9a0a11835baaf1fc3aef8216be3db36445f7122a671c88c.
```

They comprise precisely:

| residue class `(a,b,c)` | missing symbolic region |
|---|---|
| `(1,2,1)` | even `b>=12`, `c>=23`, with the finite/high representatives |
| `(1,2,6)` | even `b>=10`, `c>=28` |
| `(1,2,7)` | even `b>=10`, high `c>=29` |
| `(1,2,8)` | even `b>=10`, high `c>=30` |
| `(1,2,10)` | high even `b>=14`, `c>=21` |

The “finite/high” wording describes the clamped audit; in every row the
displayed lower corner generates the full mathematical orthant.

## 3. Five safe seeds

The five paths are stored in `certificate.json`. The checker verifies from the
definition that each is a permutation of `0,...,v-1`, has exactly the stated
cyclic edge-length multiset, and is simultaneously growable in modes 2 and 11
at the stored cuts.

For every seed, the two critical intervals are disjoint. Every edge has length
at most `D=11`, and every seed order is at least 37. Therefore

```text
2D+2+11 = 35 <= v.
```

Mark the unique shorter circular arc of each path edge. After inserting both
gaps, such an arc has length at most `D+2+11`, while its complement has length
at least `v-D`; the inequality prevents a shorter-arc reversal. Consequently
a gap changes exactly the marked arcs crossing it. Subdivision at the two
disjoint critical intervals is order-independent, preserves the transported
growth incidences, and creates only edges of old length, 2, or 11. The same
margin persists because the order increases.

Induction therefore proves that a seed `(1,B,C)` supplies a realization of

```text
{1, 2^(B+2q), 11^(C+11r)}
```

for every `q,r>=0`. These five orthants cover all 29 residual cells, and the
audit returns `final_residual_patterns=0`. The 502-cell cover is exhaustive,
so every admissible member of the `a=1` face is realized.

## 4. Validation and trust

`verify.py` checks 245 derived family paths and 180 commuting squares at its
default grid. `independent_check.py` reimplements cyclic distance and gap
insertion, checks twenty definition-level growth operations and the five
source commuting squares, and imports no producer module. The coverage audit
reconstructs the finite quotient rather than reading a claimed residual list.
Mutation tests reject a duplicate vertex, an illegal cut, and a missing seed.

The universal theorem trusts the written clamping and safe-margin arguments,
the cited prior transition-closed theorems, the five explicit paths, the
compact extraction, Python integer/file semantics, CPython, and inspection of
the checkers. It does not trust CP-SAT, floating point, randomness, a bounded
grid as an induction proof, or the invalid cross-preservation assertion in
the original proof attempt.
