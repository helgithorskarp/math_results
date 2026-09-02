# A 14-edge kernel for the Parts-509 degree-four color-list interface

## Exact result

Let `G` be the strict unit-distance graph on Jaan Parts's 509 points, with all
2,442 unit pairs present, and let

```text
D = (310, 313, 316, 319, 322, 325)
```

be its six degree-four vertices.  They are independent.  For a proper
4-coloring `c` of `G-D`, define the available-color list at `v in D` by

\[
A_v(c)=\{0,1,2,3\}\setminus c(N_G(v)).
\]

The exact feasible six-tuples `(A_v(c): v in D)`, modulo one global
permutation of the four colors, comprise 22 states (528 states with labeled
colors).  The 22 representatives and one directly checkable coloring for each
are in `certificate.json`.  Their total list capacities are distributed as

```text
sum_v |A_v| = 6 : 4 states
sum_v |A_v| = 7 : 6 states
sum_v |A_v| = 8 : 12 states
```

This refines the earlier empty/nonempty classification, which records only the
six singleton and three antipodal-pair blocked sets.

There is also a sharp relative edge-kernel result.  Fix the independently
certified 2,259-edge non-4-colorable subgraph `G_red` of `G`.  It contains all
24 edges incident with `D`.  Put `H_red = G_red-D`, so `H_red` has 2,235 edges,
and let `X` be the 183 internal strict edges of `G-D` omitted from `H_red`.
Then

\[
\min\{|F|:F\subseteq X,\;H_{red}+F
\text{ has the same six-list interface as }G-D\}=14.
\]

One attaining set is

```text
(72,101)  (73,110)  (78,277)  (85,282)
(173,276) (174,275) (181,284) (182,283)
(201,242) (203,231) (207,230) (209,237)
(213,236) (215,225)
```

The minimum is relative to this fixed 2,259-edge core and the 183-edge pool.
It does not assert uniqueness of the 14-edge set or an absolute minimum over
other bases.  It does not reduce the 509 vertices, improve the known record,
or change `5 <= chi(R^2) <= 7`.

## Proof architecture

The certificate splits the proof into directly checkable finite claims.

1. Exact reconstruction gives 509 distinct points and exactly 2,442 unit
   pairs.  The fixed reduced graph has 2,259 of them, including all 24 terminal
   edges; its canonical edge digest agrees with the prior certificate.
2. The 22 positive states have explicit proper colorings of `G-D`.  Relabeling
   colors produces exactly 528 distinct labeled states.
3. A deterministic CNF colors `H_red` plus the selected 14 edges, reifies each
   of the 24 color-availability bits directly from the four neighbors, and
   excludes the 528 allowed states.  CaDiCaL reports UNSAT and `drat-trim`
   checks the proof.  Since this graph is a subgraph of `G-D`, this proves
   equality of the two interfaces.
4. For minimality, each of 144 explicit forbidden colorings of `H_red` defines
   a nonempty set of monochromatic edges in `X`.  Every edge set recovering
   the strict interface must hit all 144 sets.  Their exact transversal number
   is 14: two separate solver-free branch-and-bound implementations recompute
   it, and a second deterministic CNF encodes a hitting set of size at most 13.
   Its CaDiCaL refutation is also checked by `drat-trim`.

The proof inputs are:

```text
interface: 2,060 variables, 13,168 clauses
SHA-256 cce45547c8c2960311a8a3d5555321445b1410c26ef5b8ad5a6fa6139779aaed

13-edge lower bound: 2,943 variables, 10,774 clauses
SHA-256 b910a2bfacf0fbee067a14c6df772c3f94e0682d79c60a3e41085f8cc352c4c1
```

The lower-bound cardinality constraint uses an explicit Tseitin encoding of

\[
z_{i,j}\longleftrightarrow
z_{i-1,j}\lor(z_{i-1,j-1}\land x_i),
\]

where `z[i,j]` means that at least `j` of the first `i` edge variables are
selected.  The independent auditor checks the local four-variable truth table
and reconstructs the complete clause multiset without importing the generator.

## Reproduction

Run from this directory in a clone that preserves the sibling Parts-509
contribution directories.  Generated CNFs, proofs, and logs belong under
`/scratch` and are ignored here.

```bash
python3 -m venv /scratch/parts509-list-kernel-venv
/scratch/parts509-list-kernel-venv/bin/pip install -r requirements.txt

python3 list_kernel.py verify

mkdir -p /scratch/parts509-list-kernel-run
python3 list_kernel.py generate-cnfs \
  --scratch /scratch/parts509-list-kernel-run

cadical --no-binary \
  /scratch/parts509-list-kernel-run/kernel_interface.cnf \
  /scratch/parts509-list-kernel-run/kernel_interface.drat \
  > /scratch/parts509-list-kernel-run/kernel_interface.cadical.log
drat-trim \
  /scratch/parts509-list-kernel-run/kernel_interface.cnf \
  /scratch/parts509-list-kernel-run/kernel_interface.drat \
  > /scratch/parts509-list-kernel-run/kernel_interface.drat-trim.log

cadical --no-binary \
  /scratch/parts509-list-kernel-run/kernel_lower13.cnf \
  /scratch/parts509-list-kernel-run/kernel_lower13.drat \
  > /scratch/parts509-list-kernel-run/kernel_lower13.cadical.log
drat-trim \
  /scratch/parts509-list-kernel-run/kernel_lower13.cnf \
  /scratch/parts509-list-kernel-run/kernel_lower13.drat \
  > /scratch/parts509-list-kernel-run/kernel_lower13.drat-trim.log

python3 independent_check.py \
  --interface-cnf /scratch/parts509-list-kernel-run/kernel_interface.cnf \
  --lower-cnf /scratch/parts509-list-kernel-run/kernel_lower13.cnf
```

The direct verifier ends in `all_checks=true`; the independent auditor ends in
`PASSED`; both proof checks must print `s VERIFIED`.  `expected_check.txt`
records the compact summaries from the certified run.

The recorded run used CPython 3.11.2, SymPy 1.14.0,
python-sat 1.9.dev15 (CaDiCaL153 for enumeration and RC2 for discovery),
CaDiCaL sc2021 for DRAT production, `drat-trim` with binary SHA-256
`bc7543a99da8521ddb09af442698956054f11e10d198bd482ac756535244c021`,
and Kissat 4.0.4 as a corroborating second solver.  The checked DRAT traces
were approximately 35 MiB and 5.7 MiB; they and all solver logs remain under
`/scratch` and are not committed.

## Trust boundary

- Exact geometry trusts the published coordinate input, CPython rational
  arithmetic, SymPy parsing, and the compact multiquadratic-field code in the
  sibling criticality contribution.  The independent auditor rebuilds every
  unit pair; no floating-point comparison is used.
- Every positive state and every lower-bound hyperedge is backed by a coloring
  replayed directly against the relevant edge set.  RC2 found the 14-edge set
  but is not trusted for the result.
- The transversal number 14 is recomputed by two exhaustive branch algorithms
  and separately supported by a DRAT-checked at-most-13 refutation.
- Interface completeness trusts the audited SAT reduction, CaDiCaL's proof
  production, and `drat-trim`; these programs are not formally verified.
  Kissat agreement is corroboration, not a proof certificate.
- The reduced-core provenance and its non-4-colorability are inherited from
  the prior audited 2,259-edge certificate.  SHA-256 values bind bytes but do
  not supply mathematical interpretation.

## Prior work and novelty scope

Parts introduced the strict 509-vertex, 2,442-edge record construction and
described graph minimization by SAT.  Heule introduced clausal-proof-based
minimization and emphasized small enforced coloring interfaces.  The fixed
2,259-edge core is from Mohammed Amer's later edge minimization and was audited
in the sibling criticality contribution.

A targeted search of those primary sources and the current Discovery Net
neighborhood found no full six-list classification or this fixed-core 14-edge
minimum.  The result is therefore presented as new to the searched sources and
graph, with no historical-priority claim.

- Jaan Parts, *Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane* (2020),
  <https://arxiv.org/abs/2010.12665>.
- Marijn J. H. Heule, *Computing Small Unit-Distance Graphs with Chromatic
  Number 5* (2018), <https://arxiv.org/abs/1805.12181>.
- Mohammed Amer, `hadwiger-nelson-e5`,
  <https://github.com/md-amer/hadwiger-nelson-e5>.
