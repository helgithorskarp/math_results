# The unique 14-edge kernel for the Parts-509 degree-four list interface

## Exact result

Use the notation and data of the sibling
`hadwiger_nelson_parts509_degree4_list_kernel` contribution.  Thus `G` is the
strict 2,442-edge unit-distance graph on Jaan Parts's 509 points,

```text
D = (310, 313, 316, 319, 322, 325)
```

is the set of its six independent degree-four vertices, `H_red` is the
2,235-edge graph obtained by deleting `D` from the audited 2,259-edge reduced
graph, and `X` is the pool of 183 strict internal edges omitted from `H_red`.
The full interface of a graph on `V(G)-D` is the set of the six available-color
lists induced by all of its proper four-colorings.

There is exactly one set `F` of 14 edges in `X` for which `H_red + F` has the
same full interface as `G-D`.  In particular, the sharp 14-edge kernel from the
previous contribution is unique, not merely one optimum:

```text
(72,101)  (73,110)  (78,277)  (85,282)
(173,276) (174,275) (181,284) (182,283)
(201,242) (203,231) (207,230) (209,237)
(213,236) (215,225)
```

The classification also exposes why the earlier lower bound did not itself
prove uniqueness.  Its 144 forbidden-coloring constraints have exactly 42
minimum transversals of size 14.  Three pool edges, `(173,276)`, `(182,283)`,
and `(213,236)`, occur in all 42.  Four explicit proper colorings collectively
show that 41 of the 42 transversals admit a list state outside the strict
interface.  The displayed transversal is the sole survivor.

This is a uniqueness theorem only relative to the fixed base `H_red`, the
fixed 183-edge pool `X`, and equality of the full six-list interface.  It does
not claim an absolute edge minimum over different bases, reduce the 509
vertices, or change `5 <= chi(R^2) <= 7`.

## Proof architecture

1. Every full-interface kernel must hit each of the 144 sets of strict edges
   made monochromatic by the previously certified forbidden colorings.
   The previous contribution proved that the transversal number is 14.
2. `certificate.json` lists all 42 size-14 transversals.  The solver-free
   checker exhaustively enumerates the instance by a disjoint first-chosen-edge
   branching rule, with only unit propagation, dominated-hyperedge removal,
   and a greedy disjoint-edge lower bound.  It searches 47,930 nodes and gets
   exactly the declared list.
3. As an independent completeness route, a deterministic 3,127-variable,
   11,549-clause CNF encodes a hitting set of size at most 14 and blocks the 42
   declared transversals.  CaDiCaL reports UNSAT, and `drat-trim` verifies the
   proof.  The independent checker also truth-table-checks the local Tseitin
   recurrence and reconstructs the exact CNF bytes.  The CNF SHA-256 is
   `25160f2c91f22318623c0640df6f1540226379182c33d3648beb64a9de2e1fb7`.
4. The four compact failure witnesses are replayed directly against all base
   edges and every candidate edge in each of the 41 losing transversals.  Their
   available-color states are recomputed and checked not to lie in the 528
   labeled strict-interface states.
5. Full-interface equality for the remaining transversal is the independently
   audited UNSAT result in the sibling contribution.  Together these facts
   prove existence and uniqueness.

The completeness CNF uses the explicit recurrence

```text
z[i,j] <-> z[i-1,j] OR (z[i-1,j-1] AND x[i])
```

where `z[i,j]` means that at least `j` of the first `i` pool edges are chosen;
`z[183,15]` is forbidden.  One 14-literal blocking clause is added for each
declared transversal.

## Reproduction

Run from this directory in a clone preserving the sibling contribution
directories.  Generated CNFs, proof traces, and logs belong under `/scratch`.

```bash
python3 -m venv /scratch/parts509-unique-kernel-venv
/scratch/parts509-unique-kernel-venv/bin/pip install -r requirements.txt

mkdir -p /scratch/parts509-unique-kernel-run
/scratch/parts509-unique-kernel-venv/bin/python classify_kernels.py \
  ../hadwiger_nelson_parts509_degree4_list_kernel/certificate.json \
  --completeness-cnf /scratch/parts509-unique-kernel-run/completeness.cnf \
  --output /scratch/parts509-unique-kernel-run/enumeration.json

python3 independent_check.py \
  --completeness-cnf /scratch/parts509-unique-kernel-run/completeness.cnf

cadical --no-binary \
  /scratch/parts509-unique-kernel-run/completeness.cnf \
  /scratch/parts509-unique-kernel-run/completeness.drat \
  > /scratch/parts509-unique-kernel-run/cadical.log
drat-trim \
  /scratch/parts509-unique-kernel-run/completeness.cnf \
  /scratch/parts509-unique-kernel-run/completeness.drat \
  > /scratch/parts509-unique-kernel-run/drat-trim.log
```

The independent checker ends in `PASSED`, and the proof check must print
`s VERIFIED`.  The certified run used CPython 3.11.2,
python-sat 1.9.dev15 (CaDiCaL153), CaDiCaL 2.1.2 for proof production, and
`drat-trim` with binary SHA-256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.
Kissat 4.0.4 independently also reports `s UNSATISFIABLE` on the completeness
CNF.
The approximately 22 MiB DRAT trace and all logs remain under `/scratch` and
are not committed.

## Trust boundary

- Direct witness checks and the solver-free enumeration trust CPython integer,
  set, JSON, and hash operations.  They do not trust the SAT solver used to
  discover the transversals or failure colorings.
- The independent completeness route trusts the audited threshold encoding,
  CaDiCaL's proof production, and the C implementation of `drat-trim`; neither
  executable is formally verified.
- The 144 necessary constraints, their transversal lower bound 14, the 528
  strict-interface states, and completeness of the winning interface are
  inherited from and rechecked against the sibling certificate.  Exact
  geometry and the reduced-core provenance therefore retain that
  contribution's stated trust boundary.
- SHA-256 values bind bytes but do not supply their mathematical
  interpretation.

## Prior work and novelty scope

Parts introduced the 509-vertex, 2,442-edge record graph and graph-minimization
method.  Heule introduced clausal-proof minimization for small 5-chromatic
unit-distance graphs and emphasized enforced coloring interfaces.  Mohammed
Amer's later data supplies the fixed 2,259-edge edge-critical base.

A targeted search of these primary sources, their public data, and the current
Discovery Net neighborhood found no classification or uniqueness theorem for
this six-list kernel.  The result is presented as new to those searched
sources and the graph, without a historical-priority claim.

- Jaan Parts, *Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane* (2020),
  <https://arxiv.org/abs/2010.12665>.
- Marijn J. H. Heule, *Computing Small Unit-Distance Graphs with Chromatic
  Number 5* (2018), <https://arxiv.org/abs/1805.12181>.
- Mohammed Amer, `hadwiger-nelson-e5`,
  <https://github.com/md-amer/hadwiger-nelson-e5>.
