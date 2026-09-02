# Packing total chromatic numbers of the first open cycles

This directory gives finite, checkable evidence for

\[
\chi_{\rho}^{\prime\prime}(C_{14})=10,\qquad
\chi_{\rho}^{\prime\prime}(C_{15})=9,\qquad
\chi_{\rho}^{\prime\prime}(C_{16})=10,
\]

and

\[
\chi_{\rho}^{\prime\prime}(C_n)=9\quad(17\le n\le26).
\]

These are the first unresolved cycle orders in Ferme and Mesarič Štesl,
*On packing total coloring*, arXiv:2508.08691v2 (2026).  That paper defines
the invariant, determines the orders through 13, gives bounds for all later
cycles, and explicitly asks for exact values when `n >= 14`.  It also supplies
an 8-color pattern at `n = 27`, so the interval above closes the entire gap
between the published exact small cases and that first published later
construction.

## Finite reduction

Order the elements of `V(C_n) union E(C_n)` as

```text
v_0, e_0, v_1, e_1, ..., v_(n-1), e_(n-1),
```

where `e_j = v_j v_(j+1)` and subscripts are modulo `n`.  The total graph in
this order is the square of the cycle `C_(2n)`.  Hence its distance between
positions `a,b` is

```text
ceil(min(|a-b|, 2n-|a-b|) / 2).
```

A word `w` over colors `1,...,k` is therefore a packing total coloring exactly
when equal entries `w[a] = w[b] = i` have cyclic separation greater than
`2*i`.

`generate_cnf.py` encodes this condition with Boolean variable `x_(p,i)`,
exactly one color per position, and one binary conflict clause for each
forbidden equal-color pair.  Its optional symmetry clauses are complete:

- some coloring can be rotated to put color 1 at position zero (if color 1 is
  absent, first replace the least used color by the weaker color 1);
- colors at least the diameter are singleton colors and can be put in
  first-appearance order.

Thus UNSAT for the symmetry-broken formula is equivalent to nonexistence.
The lower-bound formulas use 9 colors at `n = 14,16`, and 8 colors at every
other `n` in `14,...,26`.

## Reproduction

The compact upper-bound certificates are in `witnesses.json`.  Check them
directly from the definition, using an explicit total graph and breadth-first
distances rather than the cyclic-word reduction:

```bash
python3 verify_witnesses.py
python3 verify_capacity_bounds.py
python3 test_suite.py
```

Expected terminal lines are:

```text
verified 13 packing total coloring witnesses for C_14 through C_26
verified 4 strict capacity lower bounds
all 3 tests passed
```

To reproduce a lower bound, generate a CNF under scratch storage, audit the
whole instance against an independently constructed total graph, ask CaDiCaL
for a textual DRAT proof, and replay it with `drat-trim`.  For example:

```bash
mkdir -p /scratch/packing-total-proof
python3 generate_cnf.py 18 8 /scratch/packing-total-proof/c18_k8.cnf --symmetry
python3 audit_cnf.py 18 8 /scratch/packing-total-proof/c18_k8.cnf --symmetry
cadical --unsat --binary=false -q \
  /scratch/packing-total-proof/c18_k8.cnf \
  /scratch/packing-total-proof/c18_k8.drat
drat-trim \
  /scratch/packing-total-proof/c18_k8.cnf \
  /scratch/packing-total-proof/c18_k8.drat
```

The four cases `(n,k) = (16,9), (17,8), (19,8), (22,8)` instead have the
strict elementary capacity bound checked by `verify_capacity_bounds.py`.
Repeat the DRAT command for `(14,9), (15,8), (18,8), (20,8), (21,8)` and
`(n,8)` for `23 <= n <= 26`.  `proof_summary.tsv` records the checked formulas
and proof replays from the production run; the large DRAT files and solver
transcripts are deliberately excluded from this repository.

The code uses only Python's standard library and exact integer/graph
operations.  The production run used Python 3.11.2, CaDiCaL `sc2021`, and
`drat-trim` (commit/version reported in `proof_summary.tsv`).

## Trust boundary and scope

The upper bounds trust only Python and the small definition-level verifier.
Four lower bounds are elementary cyclic capacity arguments.  The other lower
bounds additionally trust the CNF/DRAT parsing and the independently run
`drat-trim` checker; `audit_cnf.py` removes the generator's mathematical
encoding from that trust boundary.  No floating point, timeout, random choice,
or unverified solver status enters the claimed table.


The computation determines only the displayed thirteen cycle orders.  It does
not classify all `n`, and it does not claim historical priority.  The result is
apparently new relative to the cited primary source, targeted web searches
through 2026-09-02, and Discovery Net at the pre-publication indexed height.

Primary source: <https://arxiv.org/abs/2508.08691v2>.
