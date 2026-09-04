# Medium-prime automorphism obstruction for Ramsey `(5,5,43)`

Let `G` be a graph on 43 vertices with neither a clique nor an independent
set of order five. Then `Aut(G)` contains no element of order

```text
13, 17, 19, or 23.
```

This is an exact computer-assisted structural theorem. Combined with the
repository's independently certified exclusions for orders 7 and 11, its
long-prime obstruction, and its circulant classification, Cauchy's theorem
gives the construction-facing corollary

```text
every prime divisor of |Aut(G)| is 2, 3, or 5.
```

Neither statement constructs a 43-vertex Ramsey graph or improves a bound on
`R(5,5)`.

## Exhaustion of prime-order cycle types

An element of prime order `p` has cycle type `1^f p^k` with `f+pk=43`.
For the four primes in scope this gives exactly eight conjugacy types:

```text
p=13: (f,k)=(4,3), (17,2), (30,1)
p=17: (f,k)=(9,2), (26,1)
p=19: (f,k)=(5,2), (24,1)
p=23: (f,k)=(20,1)
```

For fixed `p,f,k`, the induced action on the 903 unordered edges has

```text
C(f,2) + f*k + k*(p-1)/2 + p*C(k,2)
```

orbits. The four terms count fixed--fixed, fixed--cycle, within-cycle, and
between-cycle edge orbits. One Boolean variable records the color of each
edge orbit. For every five-set `A`, project its ten edges to the set `M(A)`
of distinct orbit variables. The pair of clauses

```text
OR_{x in M(A)} x          OR_{x in M(A)} not x
```

is equivalent to requiring both colors on `A`. Enumerating all
`C(43,5)=962,598` five-sets and deduplicating therefore gives an exact direct
Ramsey formula.

## Complete centralizer normalization

Three compatible normalizations reduce the formulas without losing a
solution:

1. Permute the `p`-cycles so their phase-invariant `(p-1)/2`-bit internal
   distance profiles are sorted.
2. Permute the fixed vertices so their `k`-bit incidence profiles to the
   ordered cycles are sorted.
3. Use cycle zero as phase anchor and independently rotate each other cycle
   so its `p`-bit cross-edge word with the anchor is lexicographically least
   among its rotations.

Every profile list can be sorted, and the independent phase changes preserve
the first two profile families. Hence every centralizer orbit retains a
representative.

When `k=1`, the sorted fixed-to-cycle incidence word is a threshold word with
`T` one-bits. If `S` of the `(p-1)/2` internal cyclic distances are red, every
moving vertex has red degree `T+2S`. The known equality `R(4,5)=25` forces
every degree of a target into `[18,24]`; transparent boundary clauses encode

```text
18 <= T + 2*S <= 24.
```

This necessary restriction is used only in the four single-cycle cases. The
exhaustive unit test checks all 64,704 threshold/internal assignments across
those cases.

## Exact instances and UNSAT certificates

| order | fixed | cycles | variables | clauses | proof |
|---:|---:|---:|---:|---:|---:|
| 13 | 4 | 3 | 75 | 164,796 | 38,599 RUP additions |
| 13 | 17 | 2 | 195 | 161,936 | DRAT, 395,223 bytes |
| 13 | 30 | 1 | 471 | 402,223 | 34 RUP additions |
| 17 | 9 | 2 | 87 | 262,848 | 602 RUP additions |
| 17 | 26 | 1 | 359 | 222,839 | 70 RUP additions |
| 19 | 5 | 2 | 57 | 723,284 | 56 RUP additions |
| 19 | 24 | 1 | 309 | 165,411 | 74 RUP additions |
| 23 | 20 | 1 | 221 | 95,213 | 113 RUP additions |

Seven formulas were solved by PySAT Glucose 4.2. Their retained traces are
RUP and are replayed clause by clause by the standard-library checker in
`verify.py`. The `(p,f)=(13,17)` case was solved by Kissat 4.0.4; its
395,223-byte DRAT proof is checked in as a 46,724-byte xz stream and is
replayed by drat-trim 2.2. Across all eight cases the retained proofs contain
42,258 additions and 2,596,934 uncompressed bytes.

`generate_formula.py` constructs edge orbits by least images under powers of
the displayed permutation. The verifier does not import it: it independently
constructs edge orbits with a disjoint-set union, regenerates the complete
clause set using integer enumeration, and checks the deterministic CNF hash
recorded in `result.json` before proof replay. It also checks the edge-orbit
size histogram in every case.

## Reproduction

Requirements are CPython 3.11 or later, `python-sat==1.9.dev15`, xz, and
[drat-trim commit `2e3b2dc`](https://github.com/marijnheule/drat-trim/commit/2e3b2dc0ecf938addbd779d42877b6ed69d9a985).
From this directory run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

.venv/bin/python build_manifest.py --result result.regenerated.json
cmp result.json result.regenerated.json

DRAT_TRIM=/path/to/drat-trim ./verify.sh
```

The verifier prints one `PASS` line for each of the eight cases and ends with

```text
PASS medium-prime census additions=42258 deletions=23016 proof_bytes=2596934
s VERIFIED
```

followed by the unit-test report. All computation is deterministic and uses
one process, exact integer and Boolean operations, no random choice, no
floating point, and no network input. Generated DIMACS files are omitted and
ignored; the eight compact proof traces and their manifest are checked in.

## Group-theoretic consequence and construction relevance

The primes between 7 and 43 are

```text
7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43.
```

The present theorem closes the middle four. Sibling artifacts close 7 and
11, exclude prime cycles of lengths 29, 31, 37, and 41 analytically, and
classify every 43-cycle (equivalently every circulant coloring). Thus a
hypothetical target has no automorphism of any prime order at least seven.
By Cauchy's theorem, `|Aut(G)|` has no prime divisor at least seven.

This materially redirects symmetry-first construction search: candidate
actions whose group order has any prime divisor at least seven can be rejected
before building an edge-orbit formula. It does not prune asymmetric search,
and it leaves groups whose orders have only the prime divisors 2, 3, and 5.

## Scope, provenance, and trust boundary

The theorem depends mathematically on cycle-type exhaustion, the orbit CNF
equivalence, completeness of the centralizer normalizations, and
McKay--Radziszowski's `R(4,5)=25` degree consequence in the four indicated
cases. The computational trust boundary comprises two independently written
formula reconstructions, CPython integer/set semantics, the retained proof
bytes, xz decompression, and the RUP/drat-trim checkers. Solver UNSAT exit
codes are not trusted without proof replay.

Exoo's [*A lower bound for R(5,5)*](https://doi.org/10.1002/jgt.3190130113)
and Ge--Jayasooriya--Qiu--Sun--Yuan's
[*Study of Exoo's lower bound for Ramsey number R(5,5)*](https://arxiv.org/abs/2212.12630)
give the structured-construction context. Angeltveit--McKay's
[*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709) gives the current upper
bound. The inspected primary sources and refreshed Discovery Net graph did
not state these four prime-order exclusions. Novelty is claimed only relative
to those searched sources, not as a universal priority claim.
