# Proof and finite certificate

## Graph family

Vertices are `Z/43Z`.  The cyclic seed colors `uv` red exactly when the least
cyclic length of `uv` belongs to

```text
{1,2,7,10,12,13,14,16,18,20,21}.
```

Edges of `K_43` are indexed lexicographically.  Source `i` toggles the edge
indices in row `i` of the hash-pinned 238-row input.  Write its red indicator
as `b_i(u,v)`.

For a switch vector `s in {0,1}^43`, its Seidel switch is

```text
b_i^s(u,v) = b_i(u,v) xor s_u xor s_v.
```

Vectors `s` and `s xor 1` define the same graph, so set `s_0=0`.  This loses
nothing.  It also gives exactly `2^42` distinct labeled graphs for each fixed
source: equality of two normalized switches on every edge `0v` forces their
bits `s_v` to agree.

## Physical obstruction clauses

Fix five vertices `X` and let `a` be its least vertex.  If switching can make
`X` monochromatic with color `c`, then necessarily

```text
s_v xor s_a = b_i(a,v) xor c             (v in X - {a}).
```

Substitution into the other six pairs decides whether this necessary pattern
is consistent.  If it is, exactly the two complementary local switch patterns
make `X` monochromatic.  Under `s_0=0`, both patterns remain when `0` is not in
`X`; exactly one remains when `0` is in `X`.

The full source formula has one clause excluding each remaining pattern.  Its
variables are `s_1,...,s_42`; a forbidden bit one contributes a negative
literal and a forbidden bit zero a positive literal.  Clauses therefore have
width five, or width four when the physical five-set contains vertex zero.
The production formulas contain 55,901 through 57,402 clauses.  The exhaustive
local control tests every one of the 1,024 colored `K5`s and all 32 local
switch patterns, totaling 32,768 truth cases.

For the theorem, completeness of these large generated formulas need not be
trusted.  A smaller sufficient certificate is used: any subset of physical
obstruction clauses that is itself UNSAT proves that every switch creates a
monochromatic five-set.

## Compact certificates

`cores.dimacs` contains one standard DIMACS block for each source, preceded by
`c source i`.  The 238 blocks contain 84,099 clauses in total, between 259 and
476 per source.  `check_certificate.py` reconstructs `b_i` directly from the
pinned row.  For every core clause it recovers the five physical vertices and
the locally forbidden switch values and checks all ten resulting edge colors
are identical.  It rejects nonphysical, duplicate, malformed, or out-of-range
clauses.

`proofs.drat` contains the corresponding deletion/RUP traces.  Starting from
each physical core, the checker performs plain repeated unit propagation for
every addition, applies deletions with multiplicity, forbids additions after
the empty clause, and requires the final empty clause.  Across all blocks it
checks 18,396 additions and 99,088 deletions.  Every addition is RUP; no RAT
logic, SAT solver, or external proof checker is in the compact trust base.

Therefore every normalized switch assignment falsifies at least one physical
obstruction clause for every one of the 238 sources.  That clause's five
vertices form a monochromatic `K5`.  This proves the claimed family exclusion.

Finally, for any vertex permutation `pi`, relabeling a switched graph gives
the switch of the relabeled graph by the permuted vector.  Hence the conclusion
also covers all cyclic rotations represented by each pinned source row.

## Production provenance and controls

`generate.py` constructs a full source formula from the local criterion.
`decide_all.py` ran all 238 independent formulas.  UNSAT was accepted only
after DRAT-trim verified the raw Kissat proof and extracted its core and
trimmed proof.  There were 238 verified UNSAT results, zero SAT results, and
zero UNKNOWN results.  `collect.py` checked every per-case hash and status
before creating the committed aggregate files.

The standalone checker imports none of those three production programs.
`controls.py` exercises a real positive certificate, exhausts the local
coherence lemma, and rejects nine corruptions covering physical clauses,
proof termination and range, parsing, section order, and source identity.
Normal and `python -O` runs agree.

The upstream assertion that the input is the complete `A12` representative
list is imported from the q13 boundary package.  This proof establishes no
statement about the other 69,071,588 primary sublevel-twelve rotation orbits,
disconnected cyclic-landscape components, arbitrary non-switching edge edits,
or the h3987 q10 survivor formulas.
