# Exact optional-path projection for H514

The four added vertices of the [H514 support](../hadwiger_nelson_heule514_interface/README.md)
can be eliminated exactly from its four-colouring problem. Their extension
relation is an **irredundant CNF with 37 prime clauses and 286 literals**, in
four selection bits and twelve colour-availability bits. Direct enumeration
checks all **16 × 8^4 = 65,536** local states against an independent assignment
oracle. The relation applies to every one of the **258,914 residual graphs**
from the parent result, including every block composition.

The essential bridge is that the origin and **all fifteen old neighbours of
the added path are forced in any non-four-colourable H514 subgraph**.
Sixteen explicit singleton-deletion colourings are checked directly on the
exact graph. Thus availability depends on colours of a fixed boundary; it
needs no boundary-vertex activation conditions.

This is an exact reduction, **not a family closure or a record graph**.
There were no new graph queries. The existing residual count is unchanged.
Generic path states need not be realizable by colourings of the old graph.
No priority claim is made for the elementary path-list argument.

## Exact geometric and certificate boundary

H514 consists of H510 in increasing union-certificate `510` label order,
followed by centres 170, 436, 1239, 1527 of the fixed published completion
table. The positive-radical basis is
`1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165)`.
These points use integer coefficients at scale 96. The checker reconstructs
all 131,841 pairs by integer multiquadratic arithmetic, yielding 2,526 unit
edges, and confirms the induced path `510–511–512–513`.

Every added vertex is adjacent to origin 0. Its other old neighbours are

| New vertex | Old neighbours other than 0 |
|---:|---|
| 510 | 361,417,495,503,509 |
| 511 | 418,498,506,508 |
| 512 | 359,362,502 |
| 513 | 358,416,507 |

These fifteen indices are distinct. Together with 0 they form B.
[`boundary_witnesses.json`](boundary_witnesses.json) contains a full proper
four-colouring of H514−v for each v in B. These 16 witnesses occupy 8,832
bytes and pass 40,246 retained-edge checks. A non-four-colourable subgraph
must therefore contain B. This holds at every order, not just at most 508.

The parent result proves that a target-order non-four-colourable subgraph
exists in this support if and only if one of its specified 258,914 induced
508-vertex residual graphs is non-four-colourable. Its free-vertex set is
disjoint from B. We use this pinned theorem and do not repeat its census.
The present projection works more generally for all 2^498 vertex subsets
containing B. It does not settle their colouring status.

## Pointwise extension relation

Fix any retained old vertex set containing B and any proper old colouring,
normalized so origin 0 has colour 0. Write p_i=510+i, i=0,1,2,3, and let
s_i indicate whether p_i is selected. Its list L_i is the subset of
{1,2,3} absent from its old-neighbour colours in the table above. Let a_ic
mean c belongs to L_i.

The old colouring extends to exactly the selected new vertices if and only
if the following clauses hold. For each consecutive interval I of the path,
take the listed maximal forbidden lists M_i and require

`OR(i in I) not s_i  OR  OR(i in I, c not in M_i) a_ic`.

| Interval length | Forbidden lists along the interval | Number of clauses | Clause length |
|---:|---|---:|---:|
| 1 | empty | 4 | 4 |
| 2 | {a}, {a} | 9 | 6 |
| 3 | {a}, {a,b}, {b}, with a≠b | 12 | 8 |
| 4 | {a}, {a,b}, {b,c}, {c}, with a≠b and b≠c | 12 | 10 |

Letters range over {1,2,3}; a=c is allowed in the length-four row. Every
interval position is included. A clause fails precisely when that interval
is selected and each actual list is contained in its forbidden list.
Empty lists, disconnected selections and unused lists are all covered.
[PROOF.md](PROOF.md) proves the characterization by forced propagation and
establishes the graph-level and CNF quantifiers.

[`certificate.json`](certificate.json) gives all 37 clauses with their
maximal bad states. DIMACS variables 1..4 are s_0..s_3 and variables 5..16
are a_01,a_02,a_03,a_11,...,a_33. List-mask bit c (c=0,1,2) denotes global
colour c+1. The complete truth stream accepts **48,516** and rejects
**17,020** states. With all four vertices selected, 1,924 of 4,096 list
tuples extend. These are local list counts, not counts of actual graph
colourings or unresolved target graphs.

## Changed formula and witness reconstruction

[`compile.py`](compile.py) emits an equisatisfiable colouring CNF for any
fixed H514 omission set disjoint from B. It keeps four Boolean colour
indicators per old vertex and uses twelve availability variables. There
are **no colour indicators for the four new vertices**. Availability is
reified by 57 clauses on the old boundary, then the 37-clause relation is
specialized to the selected path vertices. Old colour indicators use
at-least-one and unit-edge inequalities; at-most-one is unnecessary.
The proof explains extraction from models with multiple true indicators.

The first unchanged parent residual, omissions `46,108,152,210,219,294`,
compiles to **2,052 variables, 10,371 clauses, 136,345 bytes**, with SHA-256

```
ac42a25de4dae7bdc957a5f6e8b77fd8f0368acfc091177183e7ee9e2ba914e6
```

This formula was generated and checked, **not solved**. Its DIMACS file
stays local and is regenerated by the command below. There is no runtime
improvement claim. A dynamic program in `relation.py` reconstructs path
colours from a satisfying availability state.

## Independent verification and reproduction

Run from the repository root with Python 3.11.2; only the standard library
is needed. No SAT package, floating point computation or solver proof is
part of this certificate.

```sh
python3 hadwiger_nelson_heule514_path_projection/relation.py --out /tmp/p4-rebuilt.json
cmp /tmp/p4-rebuilt.json hadwiger_nelson_heule514_path_projection/certificate.json
python3 hadwiger_nelson_heule514_path_projection/verify.py --report /tmp/p4-verify.json
python3 hadwiger_nelson_heule514_path_projection/validate.py --report /tmp/p4-validation.json
python3 hadwiger_nelson_heule514_path_projection/compile.py --omitted 46,108,152,210,219,294 --out /tmp/p4-example.cnf
```

`relation.py` uses dynamic programming; `verify.py` imports neither the
producer nor the compiler. It enumerates every proper three-colour
assignment on each selected path, then tests the lists directly. This
independent oracle agrees with every clause evaluation and the entire
producer truth-stream digest. Each of the 37 maximal bad states violates
only its own clause. All 286 favourable single-bit flips have direct
colourings, proving every literal is necessary. The availability definition
passes all 384 one-colour Boolean controls, including non-one-hot inputs.

`validate.py` additionally audits the actual compiler output: complete old
edge clauses, all 65,536 specialized kernel states, and 6,144 reification
assignments across the sixteen selections. It maps each of 25 pinned
positive old colourings through every path-selection mask and reconstructs
and checks the full graph colouring: **400 positive models**. These reuse
known colourings; they add no new deletion cuts or graph decisions.

The independent verifier ran in 3.1801 seconds, and actual-formula validation
in 7.2317 seconds. Timings vary. Truth bytes use mask order 0..15 followed by
lexicographic list tuples in {0,..,7}^4; each state is one byte 0 or 1:

```
6bc4a12484424862154e2be7fbeb908f3bec2351950c76f196997a759134b39d
```

Input hashes are in `manifest.json`; public file hashes are in `SHA256SUMS`.
The trust boundary is the exact input coordinates, integer arithmetic,
finite enumeration, positive witness checks and the unformalized proof.
The 258,914-family theorem is inherited from the pinned parent certificate.
This is new author-run evidence with algorithmically independent checking,
not a separate-author review or a proof-assistant formalization.

## Handoff

This pass completes one projection phase. No graph solver or background
process remains active. A useful next bounded decision is to test whether
**every proper colouring of the induced 16-vertex boundary extends over the
full added path**. The new relation makes that a local obstruction test.
If true, it would combine with the existing
[H510 target-order closure](../hadwiger_nelson_parts509_heule_union_minimum/README.md)
to close H514 at once. If false, a locally valid obstructed colouring need not
extend to the rest of H510, so it would only refute this shortcut. That test
and all subsequent graph queries are unstarted; an unchanged omission-master
continuation and a new deletion-stratum ladder remain parked.

The prepublication refresh also found HN-3's
[terminal-only 159/214 assembly theorem](../hadwiger_nelson_long_terminal_gluing/README.md),
commit 91fbc8611c732752b51251df14bfc882da524807, Discovery Net height 3194.
It excludes those specified assemblies below 509 vertices by terminal
separation and positive extensions. Its terminal-only hypotheses do not
cover this H514 support, and it is not a premise of this projection.
The complementary construction lane and all retired supports remain outside
the present work.
