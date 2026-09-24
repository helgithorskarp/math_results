# A computer-assisted proof that C(13,6,3)=21

A `(v,k,t)` covering is a set of `k`-subsets of a `v`-element set containing
every `t`-subset in at least one block. Its minimum size is `C(v,k,t)`.

**Claim.** No twenty-block `(13,6,3)` covering exists. The explicitly checked
twenty-one-block covering in `UPPER21.json` therefore gives `C(13,6,3)=21`.

This is an exact exhaustive computation with a mathematical completeness
argument and a second algorithm. It is not a proof-assistant formalization.
External review of this argument and the imported 107-class catalogue is
pending at publication. The dependencies and execution trust boundary are
specified below.

## 1. Three profiles and the complete local catalogue

We use the known lower bound `C(12,5,2)>=9`. For a direct literature
specialization, Horsley's Theorem 14(a) applies with
`v=12,k=5,lambda=1,r=3,d=1,n=2`, giving `alpha=11/12,beta=1/3` and

```
ceil((36*(7/12)+11)/(5*(7/12)+1)) = ceil(384/47) = 9.
```

See the [primary paper](https://arxiv.org/html/1409.0485v3#S6).

The blocks through any point `p` of a triple covering, with `p` removed,
cover every pair of the remaining twelve points. Thus every point degree
is at least nine. A twenty-block covering has total degree `6*20=120`,
only three above `13*9=117`. Its degree multiset is exactly one of

```
(12,9^12),  (11,10,9^11),  (10^3,9^10).
```

Call a degree-nine point low, and let `H` be the other points. Write
`e(x)=degree(x)-9`. The nonzero excesses on `H` are respectively `(3)`,
`(2,1)`, or `(1,1,1)`. In particular `|H|<=3`.

The complete nine-block link of each low point belongs to the imported
[classification of nine-block `(12,5,2)` coverings](../covering_design_c12_5_2_classification/).
It has 107 isomorphism classes, each represented by nine distinct five-sets
on `0,...,11`. `LINKS.json` contains exactly these representatives, with the
same numbering and bytes as the preceding profile-exclusion package.
`catalogue.validate()` directly checks every representative and every
automorphism used here. Those checks establish validity of the input
objects; completeness is the upstream classification theorem.

Every point of every link has degree between three and five. The upper
bound comes from the upstream
[maximum-degree-five theorem](../covering_design_c12_5_2_link_degree_bound/),
which is also a dependency of the classification. Consequently, in the
global covering, a pair with at least one low endpoint has multiplicity
at most five. No such bound is imposed on pairs wholly inside `H`: their
permitted multiplicity is twenty. No upper bound on triple multiplicity
is used.

## 2. Complete normalization by two point links

Choose a low point `p` whose link has **maximal catalogue index among all
low points**. This is an arbitrary ordering of isomorphism types, not an
extremal property of a particular labeling. Relabel so that `p=12` and its
link is the corresponding representative `D` on `0,...,11`.

For each `D`, enumerate every excess decoration of the appropriate type.
The primary enumeration keeps one decoration per orbit of the explicitly
verified point automorphisms of `D`. An automorphism takes the prescribed
first link to itself and preserves the excess labels, so this discards no
possible covering. The audit retains every labeled decoration. Its counts
are `107*12`, `107*12*11`, and `107*binom(12,3)`. The primary counts are
954, 8,451, and 12,819.

Choose another low point `r` whose degree in `D` is largest among the
points outside `H`. Let this degree be `k`. If all such points had degree
at most three, the sum of the twelve degrees in `D` would be at most

```
5*|H| + 3*(12-|H|) = 36+2*|H| <= 42,
```

contradicting the actual sum `9*5=45`. The upper bound five gives
`k in {4,5}`. Ties are broken deterministically; different tie-breaking in
the audit changes the counts but not completeness.

The complete link at `r` is another catalogue representative `E`, with
one of its points marked as `p`. The `k` common blocks through `p,r`,
after deleting both points, must be identical four-subsets of the other
eleven points. Enumerate every bijection making these two through-systems
identical. By the choice of `p`, the catalogue index of `E` cannot exceed
that of `D`. Discarding larger indices is therefore sound. We do not impose
the analogous condition on any further low link; retaining those extra
possibilities only enlarges the search.

The primary join enumerates one marked point per point-automorphism orbit
of `E`. For each permutation of the shared rows, points are divided into
cells according to membership in those rows. Every bijection between equal
cells is tried. Any valid point bijection induces a row permutation and
these cell bijections, so all joins occur. The independent join keeps all
marked points and extends a point bijection one point at a time. At each
extension it compares the complete multisets of row projections. A true
bijection passes every prefix check, and at full depth the check is exact.
The invariant used to select candidate pairs of through-systems is only
a necessary condition; it is not treated as a complete isomorphism test.

Both methods merge equal unions of block masks. They check that each union
has `18-k` distinct blocks. The first and second stars have nine blocks
each and intersect precisely in the `k` shared blocks. Repeated descriptions
of the same union do not create new completion possibilities.

## 3. Sound filters and the residual problem

For a joined union `F`, exactly

```
b = 20-|F| = k+2 in {6,7}
```

blocks remain. None may contain `p` or `r`, whose complete stars have already
been specified. The candidate domain therefore consists of all
`binom(11,6)=462` six-subsets avoiding these two points.

For every point `x`, require its remaining degree
`9+e(x)-degree_F(x)` to lie between zero and `b`. Reject any pair already
exceeding its permitted multiplicity. The balanced primary code expresses
these checks as mandatory high points and forbidden high points; the audit
computes the degrees and pair counts directly.

One coarse primary filter is reused across all profiles: it rejects
`degree_F(x)>10` or `<9-b`, and unions requiring more than three high
points. The upper filter is harmless even in the degree-eleven and
degree-twelve profiles. For `x` different from `p,r`, each of the two
links contributes at most five blocks through `x`, and at least one shared
block contains `x`, because the triple `{p,r,x}` must be covered by the
first link. Thus `degree_F(x)<=5+5-1=9`; also `degree_F(p)=degree_F(r)=9`.
The lower filter follows from every target degree being at least nine.
Any pair already occurring more than five times requires both endpoints
to be in `H`, so the mandatory-point filter is also necessary. Exact
profile margins are then imposed without treating a degree-eleven or
degree-twelve point as degree ten.

For every surviving union the residual solver requires:

1. Exactly `b` distinct candidate blocks.
2. The exact remaining degree at every point outside `p,r`.
3. Coverage of all triples not covered by `F`.
4. Total pair multiplicity at most five whenever a pair is not contained
   in `H`.

The two complete links already cover all triples through `p` or `r` and
fix their degrees and incident pair multiplicities. Nevertheless both
solvers represent the full 286-triple universe. These conditions are all
necessary for a twenty-block covering. Exhaustively finding no residual
solution for every union proves nonexistence.

## 4. Primary exhaustive completion

`residual.py` uses arbitrary-precision Python integers as exact bitsets.
At a search state it maintains uncovered triples, a domain of candidate
blocks, exact remaining point degrees, and remaining pair capacities.

Zero point margins remove incident candidates; a margin equal to the number
of blocks left forces every remaining block to contain that point. The
available domain must have enough blocks, both globally and at each point.
A point needing one further block requires that block to cover every
still-uncovered triple through it. Initially, a point needing two further
blocks permits only candidates supported by a distinct companion that
covers the remaining triples through the point. These companions respect
every degree-one and pair-capacity-one restriction. This support check
uses necessary conditions only: it may retain incompatible pairs, but
cannot remove the two blocks of an actual completion.

The search chooses an uncovered triple with a smallest candidate list
and branches on a block covering it. After each alternative, that candidate
is excluded from later alternatives at the same node. No unrelated lower
block indices are excluded. To see completeness, take the first candidate
in this particular branching list that belongs to a proposed completion.
The corresponding branch still retains all its other blocks. If all triples
are covered before the exact block count is reached, branching continues
over the remaining domain to satisfy the prescribed degrees and count.
Success is accepted only with no uncovered triple and all degree margins
zero. Pair capacities are updated and enforced at each addition.

This is a finite search without a time limit, node limit, heuristic verdict,
or floating-point calculation.

## 5. Independent completion by whole point stars

`reference_star.py` maintains the same mathematical constraints but makes a
different decomposition. It selects a point with positive remaining degree
`d` and enumerates its **entire** remaining `d`-block star. A valid bundle
must cover every missing triple through that point. Once the bundle is
chosen, all other candidate blocks through that point are removed.

Every completion has exactly one such star at the selected point, so this
branching is exhaustive. For `d=1,2`, bundles are enumerated directly; for
larger `d`, a recursive uncovered-triple search enumerates all possibilities
with progressive exclusion as above. Each block through the pivot covers
at most ten triples through it, giving the safe check `missing<=10*d`.
Degree and pair margins are updated within bundle enumeration and restored
before a finished bundle is applied to the outer search. A pivot is chosen
outside two designated points; if no eligible point has positive margin,
a six-element block cannot remain, so the branch is impossible.

`star_audit.cpp` is an exact native implementation of this independent
algorithm. Its independence comes from the point-bijection joins, full
labeled decoration domain, and whole-star branching, not from using C++.
The Python version remains available for the entire audit with
`--python-audit`.

## 6. Exhaustive results and the upper bound

The complete primary computation gives:

| Point degrees | Roots | Compatible joined unions | Recursive states |
|---|---:|---:|---:|
| `(12,9^12)` | 954 | 72,730 | 813,354 |
| `(11,10,9^11)` | 8,451 | 999,042 | 22,611,825 |
| `(10^3,9^10)` | 12,819 | 1,849,757 | 101,401,375 |
| Total | 22,224 | 2,921,529 | 124,826,554 |

The independent computation gives:

| Point degrees | Roots | Compatible joined unions | Point states | Bundle states |
|---|---:|---:|---:|---:|
| `(12,9^12)` | 1,284 | 176,343 | 179,409 | 22,465,196 |
| `(11,10,9^11)` | 14,124 | 2,786,106 | 2,897,360 | 463,107,711 |
| `(10^3,9^10)` | 23,540 | 6,179,962 | 6,635,122 | 1,100,431,360 |
| Total | 38,948 | 9,142,411 | 9,711,891 | 1,586,004,267 |

All compatible unions in both tables have no completion. A union is counted
once per decorated root; the totals are not global isomorphism counts.
The larger independent root domain deliberately includes equivalent
decorations. Wherever both methods choose the same first link, decoration,
and second point, all configuration-set hashes agree: 474, 3,928, and 5,799
root comparisons for the three profiles, respectively.

Every root index is checked for complete coverage without duplicates when
workers are merged. `EXPECTED.json` and `AUDIT_EXPECTED.json` give all totals
and 321 per-design records each, with hashes of canonical root records.
Each root record also hashes its complete sorted list of joined unions.
The reproduction commands compare the entire summary structure, including
these hashes, to the reference files. Hashes make output comparisons
compact; they are not standalone nonexistence certificates.

`check_upper.py` checks the known 21-block witness directly using sets and
all 286 triples. Hence `C(13,6,3)<=21`. If any smaller covering existed,
one could add distinct six-subsets to obtain a twenty-block covering, since
there are 1,716 available blocks. The twenty-block exclusion proves the
reverse inequality and establishes the claimed value.

## 7. Validation and trust boundary

Both packaged algorithms were replayed over all three profiles, and every
per-design root-record digest was compared against the complete preceding
prototype run. For 13,214 completed balanced audit roots, the native and
Python reference results agree in every recorded field except wall time:
3,559,694 completion instances, 3,742,205 point states, and 587,973,947 bundle
states. This is a partial Python reference comparison, not a claim that a
full Python audit was run.

The compact 142-instance `NATIVE_CASES.json` includes samples across all
three profiles and roots with large bundle counts per instance. Adding
seven known positive completions and an inconsistent-degree case yields
150 cases on which native release, Python reference, and address/undefined
behavior sanitizer builds agree exactly, including state counts and
positive witnesses. All three completion engines also recover the known
cover with one through seven blocks removed and reject a degree-sum mutation.
`join_controls.py` recovers two actual complete links of the known cover
with both join algorithms, including the maximal-index normalization.

The primary search uses only the Python standard library. The native audit
uses standard C++20 and `ctypes`. Its block masks use 13 bits, candidate
domains use 462 bits in eight 64-bit words, and triple sets use 286 bits in
five words. Point margins and pair capacities remain within small signed
integer bounds (initial targets and capacities lie in `0..21`); recursion
adds at most 21 blocks. State counters are unsigned 64-bit integers with
explicit overflow checks. All production values are well below the limit.
Processes partition roots; native cache objects are used sequentially
within each process, with no shared mutable state between processes.

The upstream catalogue's primary and independent classification runs were
also replayed in this pass and matched their references. Its degree-five
bound still imports the earlier checked SAT/DRAT proof and its independent
review; those proof traces were not regenerated here. Thus this package
removes the earlier *global profile exclusions* from the dependency chain,
but does not remove this upstream SAT/DRAT dependency. No earlier global
triple-multiplicity bound is needed.

The result trusts the stated mathematical reductions, the completeness of
the imported catalogue, the supplied exact search source, Python, the C++
compiler/runtime and FFI for the native audit, and hardware. Code inspection,
two different exhaustive algorithms, upstream replays, positive witnesses,
native/reference comparisons, and sanitizer tests provide evidence for these
bridges. They do not constitute external peer review or formal kernel
verification. Large intermediate logs and search trees are deliberately
omitted; all proof computations can be regenerated from compact source.
