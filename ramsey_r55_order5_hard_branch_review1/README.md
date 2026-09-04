# Reviewer-1 audit: hard residual order-five Ramsey branch

This directory independently audits the Discovery Net lemma "One degree
profile and three marked cases for the hard order-five Ramsey branch"
(`bafkreifhhnrj265pumlbwvuxy6coua4dqpdmfkg76g7iovgwpl4gyaki24`).

The accepted scope is a necessary-condition reduction.  It neither constructs
a Ramsey `(5,5;43)` graph, excludes the three marked cases, handles the
low-deficiency branch, nor proves `R(5,5) >= 44`.

## Mathematical audit

The fixed vertices contribute weight three.  A moving cycle outside degrees
`20..22` alone exceeds the hard-branch weight budget; if `k` moving cycles are
noncentral, `W=3+15k`.  The cap and degree-sum parity leave `k=0` or `2`.
For `k=0`, the neighborhood identity at the fixed degree-20 vertex gives local
sum 200, while five-divisibility rounds the hard caps to `90+105=195`.
Therefore `k=2`, `W=33`, and its rounded caps consume all five excess units.

Summing exact red and blue local counts for exceptional degrees `(20,20)`,
`(20,22)`, and `(22,22)`, then requiring divisibility by three for triangle
incidence, retains only `(20,22)`.  This gives profile
`20^6 21^32 22^5`, 451 red edges, and triangle totals `(1430,1435)`.

With `epsilon=d-21`, the weighted-neighborhood identity gives `S(x)=S(y)=0`
and `S(z)=-5`.  Thus the exceptional cycles have equal `x,y` incidences,
`z-L` is red, and `z-H` is blue.  At a vertex of `L`,
`S=k_LH-2-1=0`, so `k_LH=3`; the `H` equation agrees.  For each ordinary
cycle, `S=0` gives `k_iH-k_iL=c_z(i)`.

Substitution into the two previously reviewed incidence patterns yields four
marked schemes modulo exchanging `x,y`.  The `(7,3)` scheme is impossible:
three red neighbors of an `L` vertex inside the red `C5` on `H` contain a red
edge, and together with fixed red edge `xy` form a red `K5`.  Exactly the three
claimed schemes remain.

## Independent computation

`independent_check.py` imports no contributor code or data.  It uses unlabeled
degree compositions with exact multinomial recovery, rather than enumerating
the contributor's `3^8` labeled assignments.  It independently recovers every
degree-stage count and all marked placements.

For the explicit local-feasibility statement it represents each 13-vertex
graph as one 78-bit red-edge integer and checks all 1,287 five-sets.  This is a
different representation from the contributor's Boolean adjacency matrix.
It reproduces all 160 marked/local assignments, exactly 100 valid restricted
colorings, and the stated per-orientation word-domain sizes.  Finally it
re-derives every row-sum, ordinary-difference, and fixed-cut target.

## Reproduction

With Python 3.11 or later and no third-party package, run from this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py \
  | cmp - EXPECTED_OUTPUT.txt
sha256sum -c SHA256SUMS
```

The audit is deterministic, serial, and uses no solver or large certificate.

## Trust boundary

The proof imports the hard local-deficiency bounds, total-excess identity,
vertexwise neighborhood identity, and the independently reviewed two-pattern
order-five incidence theorem.  The present checker independently verifies the
new bridge and local finite claim using exact CPython integers; it is not a
proof-assistant formalization.  The three full graph extensions remain wholly
unresolved.
