# Exact degree-four obstruction signatures of the Parts-509 graph

## Result

Let `G` be the strict unit-distance graph on Jaan Parts's 509 points: every
pair of listed points at Euclidean distance exactly one is an edge.  Its six
vertices of minimum degree four are

```text
D = (310, 313, 316, 319, 322, 325).
```

They are independent.  Put `H = G - D`.  For a proper 4-coloring `c` of `H`,
call `v` in `D` **blocked** when its four neighbors use all four colors, and
write

\[
B(c)=\{v\in D:c(N_G(v))=\{0,1,2,3\}\}.
\]

The exact computer-assisted classification is

\[
\begin{split}
\{B(c):c\text{ is a proper 4-coloring of }H\}
=\{&\{310\},\{313\},\{316\},\{319\},\{322\},\{325\},\\
&\{310,319\},\{313,322\},\{316,325\}\}.
\end{split}
\]

All nine displayed signatures occur.  Thus every coloring blocks at least one
and at most two of the six vertices, and two can be blocked together only in
one of the three displayed pairs.

There is a natural cyclic description.  The shared neighbors

```text
(150, 153, 158, 161, 166, 169)
```

induce a 6-cycle.  In the order shown above, each vertex of `D` is the apex of
one consecutive cycle edge; the three feasible two-vertex signatures are the
three pairs of opposite apexes.  Each apex also has two private neighbors, and
its full four-vertex neighborhood induces exactly the corresponding cycle
edge.

Because `D` is independent, a core coloring extends over a subset `R` of `D`
exactly when `R` is disjoint from `B(c)`.  The theorem therefore compresses
the simultaneous extension behavior of all six minimum-degree vertices to six
Boolean variables and nine feasible states.  This is a small interface for
future vertex-replacement and augmentation searches around the current record
graph.

This result does **not** give a graph on fewer than 509 vertices, prove global
minimality, or improve `5 <= chi(R^2) <= 7`.

## Certificate and proof architecture

`certificate.json` contains one explicit proper 4-coloring of the 503-vertex
core for each of the nine signatures.  `classify_degree4.py verify` checks all
2,418 core edges and recomputes every blocked set directly, without a solver.

Completeness is one UNSAT claim.  `classify_degree4.py generate` writes a CNF
under `/scratch` with:

- exactly one of four colors at each core vertex;
- the 2,418 core-edge constraints;
- three sound color-symmetry pins on triangle `(0,149,152)`;
- six Boolean blocked variables, truth-table reified against the four neighbor
  colors; and
- nine clauses excluding exactly the nine claimed signatures.

A satisfying assignment would be a proper core coloring whose blocked set was
not on the list.  CaDiCaL 2.1.2 reports UNSAT for the 2,042-variable,
14,741-clause CNF.  The resulting 15 MiB DRAT proof was checked independently:

```text
c parsing input formula with 2042 variables and 14741 clauses
c 9623 of 14741 clauses in core
c 51321 of 84730 lemmas in core using 3515036 resolution steps
c 0 RAT lemmas in core; 47870 redundant literals in core lemmas
s VERIFIED
```

The proof log, CNF, and solver logs are intentionally not committed; all stay
under `/scratch`.  The CNF is regenerated deterministically with SHA-256

```text
682440579f9d48e7fcd20bd34d97573f3d980597a69171f5b52e5a2e663ec283
```

An additional Kissat 4.0.4 run independently returned UNSAT on the audited CNF.

`independent_audit.py` imports none of the classification generator.  It:

1. reconstructs all 2,442 unit pairs from the algebraic coordinates using the
   sibling exact-arithmetic checker;
2. matches the independent edge manifest exactly;
3. derives the degree-four vertices and the shared-neighbor 6-cycle;
4. replays the nine positive witnesses; and
5. independently reconstructs the intended clause multiset and compares it
   with the generated DIMACS file, including its recorded hash.

## Reproduction

Run from this directory in a clone preserving the sibling contribution
directories.  Keep environments, CNFs, proofs, and logs under `/scratch`.

```bash
python3 -m venv /scratch/parts509-degree4-venv
/scratch/parts509-degree4-venv/bin/pip install -r requirements.txt

python3 classify_degree4.py verify certificate.json

mkdir -p /scratch/parts509-degree4-run
python3 classify_degree4.py generate \
  --cadical /path/to/cadical \
  --scratch /scratch/parts509-degree4-run/witnesses \
  --certificate /scratch/parts509-degree4-run/certificate.json \
  --cnf /scratch/parts509-degree4-run/classification.cnf

/path/to/cadical --no-binary \
  /scratch/parts509-degree4-run/classification.cnf \
  /scratch/parts509-degree4-run/classification.drat \
  > /scratch/parts509-degree4-run/cadical.log

/path/to/drat-trim \
  /scratch/parts509-degree4-run/classification.cnf \
  /scratch/parts509-degree4-run/classification.drat \
  > /scratch/parts509-degree4-run/drat-trim.log

/scratch/parts509-degree4-venv/bin/python independent_audit.py \
  --criticality-dir ../hadwiger_nelson_parts509_criticality \
  --edge-manifest ../hadwiger_nelson_parts509_degree10_replacements/edges.json \
  --certificate certificate.json \
  --cnf /scratch/parts509-degree4-run/classification.cnf
```

The short expected summaries are in `expected_check.txt`.  CaDiCaL exits with
code 20 on a successful UNSAT solve; `drat-trim` exits with code 0 and prints
`s VERIFIED`.

## Trust boundary

- Exact geometry trusts the published coordinate input, SymPy 1.14.0 parsing,
  CPython rational arithmetic, and the compact multiquadratic-field code in
  `../hadwiger_nelson_parts509_criticality/parts509.py`.  Equality testing after
  parsing is exact; no floating-point tolerance is used.
- Existence of all nine signatures is witnessed by explicit colorings and
  checked directly.  The SAT solver that found them is outside this part of the
  trust boundary.
- Completeness trusts the stated CNF reduction, the independent semantic audit,
  CaDiCaL's proof production, and `drat-trim`'s DRAT checking.  Neither solver
  nor checker is formally verified.  The independent Kissat answer is a
  corroborating reproduction, not a proof certificate.
- The committed CNF hash is a regression identifier, not evidence of UNSAT by
  itself.  The DRAT proof is deliberately omitted under the repository's
  large-output policy and can be regenerated in seconds.

## Scope, provenance, and novelty

The base graph and its 509-vertex record are due to Parts.  Its exact
5-vertex-criticality and strict 2,442-edge reconstruction were already
certified in the sibling contribution.  This directory establishes only the
new, finer six-vertex simultaneous-extension classification.

A targeted search of the Parts paper, the graph neighborhood, and current
record sources found no statement or certificate of these nine blocked-set
signatures.  The classification is new to the searched sources and to the
Discovery Net graph; no historical-priority claim is made.

- Jaan Parts, *Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane*, Geombinatorics 29(4) (2020), 137--166,
  <https://arxiv.org/abs/2010.12665>.
- Marijn J. H. Heule, *Computing Small Unit-Distance Graphs with Chromatic
  Number 5*, Geombinatorics 28(1) (2018), 32--50,
  <https://arxiv.org/abs/1805.12181>.
