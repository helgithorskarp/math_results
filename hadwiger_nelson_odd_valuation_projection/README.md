# Whole-field projection ends the selected A159 construction lane

**Every plane unit-distance graph with coordinates in
E(sqrt((55-7 sqrt(33))/54)), E=Q(i sqrt(3),i sqrt(11)), is four-colourable.**
This closes the final named 16-contact A159 bridge phase without enumerating
its 41,344 individual 474-point assemblies. The same theorem also colours the
whole field E(sqrt(6)), strengthening the previous finite bridge results.

The mechanism is explicit: when D has odd 2-adic valuation at either real
place of Q(sqrt(33)), colour x+y sqrt(D) by the existing E colour of x at
that place. A unit difference forces the projected norm to have valuation
zero, which makes those colours different. The argument covers arbitrary
denominators and every point of the field. [PROOF.md](PROOF.md) proves the
claim and attributes the underlying classical residue method.

A concrete proposed record candidate was built and decided: **474 distinct
physical points, 1,953 complete unit edges, properly four-coloured** by this
formula. Its source edge (13,28) is attached across bridge (18,113) of A union uA.
Exact collision merging and two metric formulas agree on every one of the
112,101 point pairs. No SAT solver or approximate geometry is used.

The stronger necessary field filter adds 146 whole-field exclusions to the
previous 1260, leaving 84 of 1490 archived origin-rotation quadratics in three
extensions undecided. These remaining cases are not non-four signals or a
new research mandate. **The A159 bridge architecture is retired after this
second field gate**, as declared before the pass. No record improvement or
global vertex lower bound is claimed.

## Reproduce

Python 3.11+ and its standard library suffice. From repository root:

```sh
python3 -B hadwiger_nelson_odd_valuation_projection/verify.py --work /tmp/hn-odd-projection
python3 -B hadwiger_nelson_odd_valuation_projection/controls.py --work /tmp/hn-odd-controls
python3 -B hadwiger_nelson_odd_valuation_projection/filter.py --work /tmp/hn-odd-frontier
```

`verify.py` regenerates the exact 474-point graph and projection word in about
two seconds. `controls.py` checks 450 exact unit vectors and 1350 translated
colour inequalities, both embeddings, arbitrary-denominator cases and very
large positive/negative valuations. It also verifies that the unguarded
projection fails on the unit vector (7+i sqrt15)/8 in the D=5 field.
`filter.py` regenerates the prior exact contact census and compares both
valuation computations entry by entry. Compact expected data and hashes are
in [expected.json](expected.json).

The source point file and arithmetic module are pinned by SHA-256. The
frontier check additionally pins the preceding field-filter source, which
pins its census and field dependencies. The generated point/edge graphs,
row inventories and exploratory logs remain local. This package provides
source and compact evidence; no large certificate is needed.

Normal and optimized Python runs passed. The earlier Fraction-based physical
producer and the final independent Cartesian norm checker agree entrywise.
The infinite theorem is a written mathematical argument with finite controls,
not a computational exhaustion of an infinite field. This is author
validation, not independent-author review or a formal proof-assistant result.

Current published vertex comparison: [Parts 509](https://arxiv.org/abs/2010.12665),
also identified in [Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4).
The record objective remains unresolved. See the proof for exact scope and
why the earlier square-embedding gate was sufficient but unnecessarily weak
for the two selected construction fields.
