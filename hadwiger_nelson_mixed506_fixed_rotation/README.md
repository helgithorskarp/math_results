# Complete fixed-rotation closure for B292/V214

For the archived connected alternative gadget `B=A159 union nu A159`,
`nu=(5+i sqrt(11))/6`, and second source `V214`, **every translation** of

```
B union (u V214+h),  u=(1+i sqrt(15))/4,  h in C
```

has a proper four-colouring. This includes disjoint 506-vertex placements,
overlaps and reflection of the second source. The latter is
conjugation-invariant. There is no bound on the translation denominator or
size, and it need not be assumed algebraic. [PROOF.md](PROOF.md) gives the
complete reduction and trust boundary.

The new local contact lemma forces a matching: in the nonintegral branch,
source differences on one side have one greater 2-adic valuation, and
`q-2p mod 8O` is constant across contacts (with the sides interchanged
when appropriate). Apply this at both embeddings of the base field. Any
non-four-colourable placement must have all four boundary residues at both
places. This reduces the full translation family to 849,532 necessary
three-contact seeds. Of those, 693 satisfy the unit-circle polynomial
modulo 1321, and none also satisfies it modulo 5281.

This is an exact negative certificate for one specified rotation. It does
not establish a five-chromatic graph, improve the 509-vertex record, close
other rotations or restart the sealed Parts pool and historical overlap
census. The four direction rows count contact seeds, not placements.

## Reproduce

From this directory in a complete repository checkout, with CPython 3.11
or later and the standard library only:

```sh
python3 census.py > /tmp/hn-fixed-rotation-census.json
cmp expected.json /tmp/hn-fixed-rotation-census.json
python3 audit.py > /tmp/hn-fixed-rotation-audit.json
cmp expected_audit.json /tmp/hn-fixed-rotation-audit.json
python3 controls.py > /tmp/hn-fixed-rotation-controls.json
cmp expected_controls.json /tmp/hn-fixed-rotation-controls.json
sha256sum -c SHA256SUMS
```

- `census.py` enumerates all contacts and required triples. It uses local
  field arithmetic and real modular Cartesian coordinates.
- `audit.py` imports neither the census nor its field/local arithmetic.
  It reconstructs the gadgets by generic real-radical multiplication,
  uses a separate finite 2-adic lift and common-denominator formula,
  groups sorted records, and evaluates the Heron circle identity using
  paired complex and conjugate images. All source edges, connectedness,
  local images and complete contact streams are checked.
- `controls.py` checks the generic contact-difference polynomial identity,
  the six pair differences of the previous connected saturation witness,
  and its survival under both circle formulas at both primes. Rational
  unit-circle, radius-two and collinear controls calibrate the geometry.

The small positive saturation witness is three-chromatic and is outside
the fixed B/V source family. Its role is to test that the necessary
filters retain a real configuration. No SAT solver or approximate
geometric test is used.

`expected.json` stores all four direction rows, cell-size histograms,
modular roots and stream hashes. Contacts are labelled `214*i+j`. Cells
are in lexicographic order of their four modulo-eight key coefficients;
contacts and each colour list are in increasing label order. A cell-stream
line is `key0,key1,key2,key3|e0,e1,...` plus a newline. Triple streams use
the same line format with three labels, chosen in colour order 0,1,2.
The first-prime survivor streams retain that ordering. Complete streams
are regenerated and hashed rather than stored as large outputs.

The uniform local and arbitrary-translation arguments are unformalized
mathematics. The accepted base-field embedding and archived coordinate
provenance are explicit dependencies. The two full implementations are
independent author checks, not external peer review or formal proof.
All initiated computations are complete; no background job is needed.

The final CPython 3.11.2 replay took 4.682 seconds for the census,
4.348 seconds for the independent audit and 0.064 seconds for controls.
Maximum child peak RSS across the serial workflow was 44,344 KiB. All
three expected outputs matched byte for byte.
