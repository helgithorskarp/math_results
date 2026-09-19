# Independent review of the Q5 facet-deficit gap 217

## Verdict

**ACCEPT, high confidence.**  The source at commit
`ad8602a183867fe79a15e15b17723c66dcd8c683` supports the exact local theorem

```text
Delta_K >= 217
```

for every nonempty square-free edge set in `Q_5`.  Conditional on the stated
active-square identities and the published exact value `ex(Q_5,C_4)=56`, the
claimed global consequence

```text
sat(Q_d,Q_2) >= 5712 d 2^d/(3137d+8287),  d >= 5,
```

and asymptotic constant `5712/3137` also check out.  The first improved
integer consequence over the accepted gap-200 bound is correctly identified
at `d=11`, where the ceiling changes from 3006 to 3007.

This is a computer-assisted theorem with a complete finite reduction, not an
experimental lower bound.  It proves that deficit 200 is not attained and
excludes all deficits through 216; it does not prove that 217 is attained.

## Human premises and completeness reductions

The high-confidence verdict depends on the following explicit premises.

1. The committed `Q_3` slack is nonnegative and the sharp `Q_4` inequality
   `delta_H=17S_H-3E_H>=0` holds for every square-free `Q_4` restriction.
2. A square-free `Q_4` has at most 24 edges: its 24 squares each require an
   omitted edge, and every omitted edge belongs to three squares.
3. Consequently `delta_H<217` implies `S_H<=16`, since
   `17S_H<217+3*24=289`.  The next unenumerated layer has lower bound
   `17*17-3*24=217`, so the cutoff is exact for the claimed strict window.
4. The production facet-gluing census is complete.  It enumerates every
   square-free `Q_3` restriction of local twice-slack at most 32, glues all
   eight restrictions with exact overlaps, and prunes only when accumulated
   nonnegative cost already exceeds 32.
5. The endpoint-edge census is independently complete.  It branches on all
   32 global `Q_4` edges and prunes only when the sum of per-facet minimum
   remaining costs exceeds 32, an admissible lower bound.
6. The two censuses agree entry-for-entry through their canonical graph-set
   hash, not merely in cardinality.  They contain 490,753 labeled patterns
   and yield the same 180 positive profile classes below 217 and the same
   profile-table hash.
7. The profile recursion considers every nondecreasing multiset of positive
   classes with total below 217, with every possible number of equality and
   empty facets.  Stopping before ten positive facets is safe because the
   least positive deficit is 28, so ten already total at least 280.  No
   parity restriction is used.
8. Its three filters are necessary: each global edge is counted in four
   facets; the live-facet capacity table is exact; and a nonextendable
   boundary of a positive facet must face another positive or empty facet,
   giving `b<=p+z-1`.
9. The all-zero-deficit case remains separately impossible by the accepted
   incidence/capacity argument.  It is not silently lost because the profile
   recursion starts with a positive class.
10. Every catalog needed by the surviving rows is the stated union of full
    `Aut(Q_4)` orbits.  Fixing one representative on a distinguished facet is
    exhaustive because cube automorphisms are transitive on facets and the
    stabilizer induces all of `Aut(Q_4)`.  Profiles with several orbits are
    handled once for every orbit representative.
11. Exact agreement on every shared `Q_3` boundary is sufficient to define a
    global edge set.  Every `Q_5` square lies in a `Q_4` facet, so compatible
    square-free facet restrictions give a square-free global pattern.
12. The all-dimensional conclusion additionally uses `ex(Q_5,C_4)=56`, the
    displayed subcube-incidence counts, and the two active-square identities.
    These human inputs were audited algebraically, but the external extremal
    theorem is not reproved here.

Thus agreement between programs is supporting evidence only after the
mathematical coverage and pruning arguments above are checked.

## Adversarial smallest and boundary examples

The potentially dangerous deficit-200 claim admits a particularly direct
audit.  Under `0<=E<=24` and `S<=16`, the equation

```text
17S - 3E = 200
```

has only `(E,S)=(7,13)` and `(24,16)`.

- The reviewer checker enumerates all 3,287,328 square-free seven-edge
  patterns.  Their minimum slack is 14, and none has slack 13.
- At 24 edges, the eight omitted edges must meet each of the 24 squares
  exactly once.  A direct exact-cover search finds exactly eight such omitted
  sets.  All eight complements have `(E,S,delta)=(24,24,336)`, never
  `(24,16,200)`.

This independently proves that no `Q_4` pattern has deficit 200 without
reusing either full target census.

The reviewer checker also regenerates every new proof-critical orbit from
endpoint-pair representatives.  It independently obtains:

- one size-32 orbit for `(delta,E,b,e_0)=(42,20,6,0)`;
- three orbits of sizes 128, 384, and 384 for `(42,20,7,0)`;
- two orbits of sizes 384 and 192 for `(65,18,4,0)`.

It recomputes all old and new catalog statistics and boundary profiles, then
uses a generic multiset generator and exact-overlap gluer rather than the
target row loops.  It excludes all 28,470 frontier placements:

| total | profiles | placements | solutions |
|---:|---:|---:|---:|
| 203 | 1 | 252 | 0 |
| 205 | 1 | 1,008 | 0 |
| 208 | 1 | 36 | 0 |
| 210 | 8 | 27,090 | 0 |
| 215 | 1 | 84 | 0 |

Normal and optimized Python produce the same pinned reviewer output.  The
reviewer program intentionally does not claim to be a third complete
`S_H<=16` census; completeness there rests on the two audited target
algorithms and their identical canonical set hash.

## Target reproduction and algebra

The target manifest and all six tests pass.  The production verifier matches
its committed output exactly in 590.2 seconds.  The separate endpoint-edge
checker matches its committed output exactly in 1,462.1 seconds.  Operational
runtimes are not proof data.

The local-to-global calculation is exact:

```text
(12*56+217)/(34*56) = 127/272,
(127/272)/12 = 127/3264.
```

Using the active-square inequalities gives

```text
3137(d-1)E >= 11424M.
```

Substitution of `M=d2^(d-1)-E` yields

```text
(3137d+8287)E >= 5712d2^d.
```

Cross-multiplication against the gap-200 bound leaves
`12138(d-1)>0`, and the asymptotic improvement is exactly
`12138/8617339`.

## Literature, novelty, and scope

Primary context was refreshed on 2026-09-19.  Johnson--Pinto and
Morrison--Noel--Scott establish the surrounding hypercube-saturation problem
and its `Theta(2^d)` scale.  Dejter--Emamy-K--Guan provide the imported
five-cube extremal result, equivalently `ex(Q_5,C_4)=56`.  Focused searches
for the exact constant and distinctive theorem wording found no published
gap 217 or `5712/3137` bound.  This supports “apparently new relative to the
searched primary sources and committed graph,” not a historical-priority
claim.

- [Johnson and Pinto, *Saturated Subgraphs of the Hypercube*](https://arxiv.org/abs/1406.1766)
- [Morrison, Noel, and Scott, *Saturation in the Hypercube and Bootstrap Percolation*](https://arxiv.org/abs/1408.5488)
- [Dejter, Emamy-K, and Guan, *On the fault tolerance in a 5-cube*](https://www.researchgate.net/publication/265697468_On_the_fault_tolerance_in_a_5-cube)

The finite proof trusts CPython arbitrary-precision integer, set, tuple, and
bit-operation semantics; the pinned corrected parent engines; the audited
enumeration reductions; and deterministic SHA-256 normalization.  It does
not determine an exact saturation number, establish attainment of 217, or
formalize the incidence bridge.

## Strengthening and improvement opportunities

1. Export the full 180-profile table or a compact independently checkable
   certificate, rather than only its hash.  This would make the shared
   profile-compression step easier to inspect without rerunning a full census.
2. Convert the shallow frontier contradictions into boundary-signature
   lemmas.  Most cases die without branching, suggesting a concise structural
   obstruction behind the computational closure.
3. Determine whether deficit 217 is attained.  If it is not, advancing the
   cutoff requires the genuinely new `S_H=17` layer and should begin with a
   measured census-size and runtime estimate.
4. Formalize the cutoff, incidence, and symmetry reductions or export proof
   certificates whose checker is substantially smaller than either census.
5. Make the imported `ex(Q_5,C_4)=56` result locally reproducible or provide a
   self-contained proof, reducing the external trust boundary of the global
   theorem.

## Reproduction

Python 3.11 or later and the standard library suffice.  The adjacent accepted
gap-200 reviewer checker is imported as a definition-level engine and is
pinned in this directory's manifest.

```bash
cd graph_theory/hypercube_square_saturation_q5_gap217_review1
PYTHONDONTWRITEBYTECODE=1 python3 review_check.py > /tmp/q5-gap217-review.json
diff -u EXPECTED.json /tmp/q5-gap217-review.json
PYTHONDONTWRITEBYTECODE=1 python3 -O review_check.py > /tmp/q5-gap217-review-O.json
diff -u EXPECTED.json /tmp/q5-gap217-review-O.json
sha256sum -c SHA256SUMS
```

Reviewed target:

https://github.com/helgithorskarp/math_results/tree/main/graph_theory/hypercube_square_saturation_q5_gap217

Verified target source commit: `ad8602a183867fe79a15e15b17723c66dcd8c683`.
