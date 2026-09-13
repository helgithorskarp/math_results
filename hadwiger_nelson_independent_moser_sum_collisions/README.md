# Every collision in a three-spindle sum is four-colourable

For the seven-point Moser spindle M displayed in [PROOF.md](PROOF.md),
take two **independent, arbitrary unit complex rotations** u and v.
If any of the 343 formal points of `M+uM+vM` coincide, the complete strict
plane unit-distance graph on the distinct points is exactly four-chromatic.

This closes the collision locus, including cases where one phase remains
free. A possible five-chromatic member must retain all 343 distinct points.
That injective family remains open here. **The 509-vertex record is not
improved**, and this is not a global lower bound on construction size.

The proof reduces all collisions to two exhaustive cases:

- Three changed factors: 1,716 base-field phase pairs, 3,024 further pairs
  covered by a compatible local-field embedding, and 3,504 exact graphs
  covered by positive colour words.
- Two changed factors: 30 fixed unit phases, reduced by a proved symmetry
  to 16 representatives. A local trace argument colours most of the
  remaining continuum. Its 5,064 exceptional contact quadratics, each
  with two physical roots having the same edge graph, are all four-coloured.

`certificate.json` shares 483 colour words, each on the 343 addresses, across the exceptional
cases. `verify.py` regenerates the complete parameter inventories, checks
that colours descend through coincidences, and checks every strict edge.
For the two-factor cases it compares the contact-polynomial edge census
with actual coordinates. Two separately derived exact metric formulas
must also agree. There is no floating-point threshold or solver dependency
in the verification.

From this directory, with Python 3.11+ and a C++17 compiler supporting
signed 128-bit integers (tested: CPython 3.11.2 and g++ 12.2.0):

```sh
g++ -std=c++17 -O3 -shared -fPIC geometry.cpp -o /tmp/hn-moser-collisions.so
python3 verify.py --library /tmp/hn-moser-collisions.so > /tmp/hn-moser-collisions.json
cmp expected.json /tmp/hn-moser-collisions.json
python3 controls.py /tmp/hn-moser-collisions.so
sha256sum -c SHA256SUMS
```

The full replay takes several minutes and uses only standard-library
Python and the native exact-integer kernel. Build products and full
inventory/solver logs are not committed. See [VALIDATION.json](VALIDATION.json)
for actual replay timings, hashes and controls; [PROOF.md](PROOF.md) states
the unformalized arithmetic and enumeration trust boundaries. These are
author checks, with external review pending.

The work follows the prior
[correlated three-spindle family](../hadwiger_nelson_correlated_moser_cube/README.md),
which explicitly left independent rotations open. It reuses the base-field
and unit-trace embedding proofs, and extends the elementary integral
residue argument to these Minkowski factors. No priority claim is made
for Minkowski sums or local-field colouring methods.

The record comparison was rechecked on 2026-09-13 against Parts,
[Graph minimization](https://arxiv.org/abs/2010.12665), and the explicit
509-vertex incumbent in
[Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4).
The latter's spindle-free construction addresses a restricted class.
Discovery Net's local index remained at height 4,363; durable repository
sources and reviews were also inspected. Broadcast receipts are reported
separately from committed graph evidence.
