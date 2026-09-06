# H517 requires at least 134 small-block vertices

**Every subgraph of H517 using at most 133 vertices of its small block is
four-colourable.** In particular, the entire family retaining all 375
large-block vertices and having at most 508 vertices is closed.

This is a negative family result, not a record graph or a closure of the
unrestricted H517 family on at most 508 vertices. Any remaining
non-four-colourable subgraph of H517 must use at least 134 small vertices.
A remaining target on at most 508 vertices must therefore delete at
least one large vertex. The lower bound 134 is not claimed sharp.

The frozen selector pilot completed after 222 tested selections. Its
master became UNSAT with a checked DRAT proof. More compactly, the public
certificate consists of 206 proper colourings of vertex-deleted H517
supports. A solver-free checker verifies these witnesses and covers all
817190 remaining nine-omission choices. The theorem can therefore be
reproduced without trusting or regenerating a negative SAT proof.

## Fixed graph and exact scope

Use G from the [H517 pilot](../hadwiger_nelson_heule517_family_pilot/README.md),
source `59d634e906f6c6ed5945c0180b5352ba03c3babd`, with the
[certified joint interface](../hadwiger_nelson_heule517_joint_interface/README.md),
source `dfabbb59e9d59215737e0b8e6321ca0f1e6321a9`.

The support has 517 distinct exact points and 2555 unit edges. Its large
block L has 375 vertices and 1920 edges, its small block S has 142 vertices
and 605 edges, and there are 30 cross-edges. The seven added points are
G indices 510..516; they are independent and all their 51 edges end in
the old 135-point small block. The complete boundary has 19 large
vertices and 30 small terminals.

G indices 0..509 are the increasing union-certificate labels marked
`510`; 510..516 are the centre indices 327,439,671,1040,1074,1377,1383,
in that order. These are not original Heule or Parts labels. Coordinates
have denominator 96 in the basis
1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165), with
positive square roots. L consists of the points whose sqrt(5),sqrt(15),
sqrt(55),sqrt(165) coefficients vanish in both coordinates. The exact
input files and relevant code dependencies are pinned in
[manifest.json](manifest.json).

## Positive certificate and direct finite proof

For each row in [certificate.json](certificate.json), D is a nonempty
subset of S and the row decodes to a proper four-colouring of G minus D.
Consequently every non-four-colourable subgraph of G must select at least
one vertex of D. This implication makes no assumption that L is retained.

The final 206 rows are an inclusion antichain: 119 singleton rows, 41
pairs, 25 triples, 13 four-sets, five five-sets, one six-set and two
seven-sets. They comprise 117 references to the prior H517 pilot's
colourings and 89 new small-block colourings paired with an explicit
large-block witness from the joint-interface certificate. References
avoid copying earlier full colour strings. They refer to zero-based row
indices in the pinned earlier 526-row certificate.

A new `case` row stores a 142-character small-block colour string in
increasing S order, with digits 0..3 and dots for omissions, plus its
zero-based boundary-case index. Combining it with that case's supplied
375-character L colouring gives the complete G minus D witness. A `seed`
row uses the earlier witness recipe. Every decoded colouring is checked
on the complete exact G edge list; no negative theorem about an earlier
graph is used.

Let F be the 119 singleton vertices. Any non-four-colourable subgraph
must contain F. The remaining 23 small vertices are

```
U = [358,359,360,361,362,370,378,379,393,395,399,432,434,
     438,459,505,510,511,512,513,514,515,516].
```

The other 87 cuts lie in U. For every nine-element O subset U, at least
one of these cuts D satisfies D subset O. The checker verifies this by
enumerating **all binomial(23,9)=817190 subsets**, testing exact integer
bit-mask containment. No search symmetry or sampling is used.

Now take any subgraph X of G with at most 133 small vertices. At least
nine small vertices are absent. If a vertex of F is absent, its singleton
witness colours X. Otherwise choose any nine absent vertices O from U.
The exhaustive cover gives D subset O, so X is a subgraph of the properly
four-coloured G minus D. Restrict that colouring to X. This proves the
theorem even when X omits large vertices or edges.

This proof needs only the positive witnesses, exact geometry and finite
coverage loop. Completeness of the earlier 20-pattern large relation was
useful for choosing the oracle, but its negative exhaustion proof is not
a premise of this new closure theorem.

## Bounded discovery and SAT encodings

The [frozen plan](plan.json) allowed at most 512 candidate selections,
513 master calls and 10240 small-case calls, each with 100000 conflicts
and 4 GiB address space. It required stopping on UNKNOWN or the declared
candidate limit. Neither limit was extended.

Initially, exactly 148 rows of the earlier 526-row certificate had D
entirely in S, including 100 singleton rows. All other cuts are already
hit when L is fixed, so they are omitted from this master. All 148
inherited positive witnesses were checked directly.

The master uses one omission variable y_v per vertex of S. A row D gives
the clause OR over v in D of not y_v. A backward prefix-threshold encoding
requires at least nine omissions, equivalently at most 133 selected
small vertices. For z(i,j), with 1<=j<=min(i,9), the clauses are

```
not z(i,j) or z(i-1,j) or y_i
not z(i,j) or z(i-1,j) or z(i-1,j-1)  (j >= 2).
```

Unavailable predecessors are false, and z(142,9) is asserted. Induction
proves that a true z(i,j) implies at least j true inputs in its prefix;
assigning actual threshold values proves the converse projection.
No equivalence is claimed for every individual auxiliary variable.
The final master has 1384 variables and 2549 clauses.

Each satisfying selection is enlarged to exactly 133 small vertices.
This preserves every hitting constraint. The oracle tries the 20
certified boundary cases in their fixed public order, stopping at the
first SAT answer. Each case has four colour variables per S vertex,
guarded at-least-one clauses, small-edge inequalities and unit clauses
forbidding cross-edge conflicts with the fixed boundary row. All 142
activation assumptions specify which vertices are selected. Inactive
vertices may have every colour variable false. At-most-one clauses are
unnecessary because adjacent true-colour sets are disjoint. The small
part and the supplied large witness share the same boundary colours.

Every SAT model is decoded and checked on G, then greedily extended
over omitted small vertices while retaining that same large colouring.
Its remaining omitted set gives a new cut. Redundant cuts are removed
by inclusion. No assertion is made that a cut is globally minimal among
all deletions making G four-colourable.

The run tested 222 selections, all four-colourable, and made 223 master
calls and 442 small-case calls. Of the latter, 222 were SAT and 220 were
UNSAT hints before another case supplied a colouring. Those individual
negative hints are not claimed as separately certified results. There
were no UNKNOWN answers and no all-20-negative target selection.
The final master UNSAT answer was independently proof-checked.

Total discovery time was 12.0905 seconds, peak RSS 58280 KiB. The final
Kissat proof took 0.0319 seconds and its DRAT check 0.1654 seconds. The
master CNF SHA256 is
`3ba8836a84c32d10fac5bcc1272f5c26d2b0058d804f30e22b0944c7cb7173f8`.
Its 23776-byte binary DRAT proof has SHA256
`ca0f408b7d596c53cb6236edc9e11df6dd9f01a1de31c8cec66d0c4c828b020c`.
That optional trace and native logs remain local. The public direct
cover proof replaces them for theorem verification.

## Reproduction and verification boundary

Use a full checkout with Python 3.11.2 (tested), standard library only:

```bash
python3 -B verify.py --report /scratch/heule517-small-verification.json
sha256sum -c SHA256SUMS
```

Expected status:
`ALL SUBGRAPHS WITH AT MOST133 SMALL VERTICES ARE FOUR-COLOURABLE`.
The report has `fixed_L_at_most508_family_closed=true`,
`small_vertices_needed_by_any_nonfour_subgraph_at_least=134` and
`negative_solver_proof_required=false`.

The checker imports the previous independent geometric verifier's
hash-pinned monomial graph routine, not the new selector/producer. It
reconstructs all 133386 pair distances exactly, checks the 206 decoded
colourings against every retained edge (523267 inequalities), validates
the 148 initial inherited witnesses, and checks the complete omission
cover. Python arbitrary-precision integer arithmetic and these finite
loops remain in the proof boundary. No floating-point or negative
native-solver trust is required for the theorem.

The author also ran `verify.py --work /path/to/original-run`, which checked
all 222 native positive extensions (561461 edge inequalities), compared
all 20 actual activation formulas and the final native master byte for
byte. The full verification took 7.8740 seconds, including 2.2180 seconds
for the exhaustive omission cover. [verification.json](verification.json)
records this original-run audit. A public-only run omits those additional
native-log checks and still verifies the full mathematical closure.

Discovery used CaDiCaL 1.9.5 via python-sat 1.8.dev24, Kissat 4.0.4 and
drat-trim. The exact environment and controls are recorded in
[validation.json](validation.json). In the PySAT environment,
`controls.py` compares the activated encoding with exhaustive ordinary
colourings in 64 tiny cases, tests a rainbow-blocked vertex both active
and inactive, checks a complete ten-case omission cover and rejects an
incomplete one. No production query was repeated for these controls.
The checker is independently implemented and author-run; no separate
author review or proof-assistant formalization is claimed.

To reconstruct the optional SAT proof input without discovery:

```bash
python3 -B write_master.py --out /scratch/heule517-small-master.cnf
```

The resulting bytes were compared with the actual native final master.
`run.py` preserves the bounded discovery procedure for reproducibility;
there is no reason to repeat this now-closed 133-small-vertex family as
another research milestone. All 222 native colourings and raw solver
state remain in the local checkpoint; only the compact final certificate
is committed.

## Decision and next boundary

The fixed-L target family is closed. The unrestricted <=508 family is
still open, and no improved graph was established. The next proposed
bounded decision is the adjacent 134-small-vertex level, with all L375
retained: either close it too, proving every non-four-colourable subgraph
of G needs at least 135 small vertices, or certify a 509-vertex obstruction
that can guide a subsequent large-deletion test. A 509-vertex obstruction
would not itself improve the record. This new stratum has not started.
The 20 full-L patterns must not be treated as complete after deleting
large vertices.

HN-3's [common-neighbour contact theorem](../hadwiger_nelson_heptagon_moser_sum/COMMON_NEIGHBOUR.md),
source `6882c980c31f08481228629aa5ea193c04e32ca2`, Discovery Net height
3086, was inspected. It closes every mixed contact with a unit heptagon
difference and leaves a necessary event set of size at most 11424 for
the separate geometric construction. Those remaining angles have not
been enumerated by that result. No premise from that lane is used here.
No background job or unfinished proof remains.
