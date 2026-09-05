# Independent review of the ten-cycle fixed-signature bound

This is reviewer-1's clean-room check of the committed Discovery Net lemma
`bafkreif4wd24cvvhh47kb6bwhaik2axclh2pt3ztqkg2z4lw4sf7gbnj3q`, reviewed at
source commit `d396b31c308dd690314c4dd0ad48ddcc2a58ba40`.

## Verdict and scope

The standalone core-extension lemma, its equality case, the 1,868-vector
forced-blue census, and the sharp 25-vertex local fixture are accepted.
The consequence for an order-three `1^13 3^10` action is accepted conditional
on the previously reviewed unique-minority-core reduction. That earlier result
still imports the older four-versus-six internal-color split; this review does
not recheck its five antecedent exclusions.

This is an intermediate restriction, not a 43-vertex Ramsey graph and not an
exclusion of the ten-cycle case. The fixture proves only that the local
core-plus-fixed-vertices bound is sharp; it supplies none of the six majority
triangles.

## Independent derivation

Write `x_i` for the singleton-signature multiplicities, `y_ij` for the pair
multiplicities, and `X=sum x_i`, `Y=sum y_ij`.

* Each signature has size at most two because every three core triangles
  contain a red `K4`.
* The vertices whose signatures contain `i` form a forced blue clique, giving
  `x_i + sum_(j!=i)y_ij <= 4`.
* For ordered `i!=j`, the vertices with signatures `{i}` or `{i,j}` form a
  forced blue clique and are blue to both remaining triangles. A core blue edge
  across those triangles gives `x_i+y_ij <= 2`.

Summing gives `X+2Y<=16` and `3X+2Y<=24`, so `X+Y<=10`. If equality holds,
both sums and every constituent ordered-pair inequality are tight. Opposite
orientations make all `x_i` equal, and subtraction gives `X=4`, `Y=6`;
therefore every singleton and pair occurs once.

The checker reconstructs the core from the mathematical difference rule. It
then exhausts the `3^10` bounded multiplicity vectors for the hand inequalities.
For the stronger census it does **not** use the submitted 58 capacity tests or
its clique recursion. Instead it directly enumerates multisets of three to five
nonempty fixed signatures together with zero to two literal core vertices,
extracts the componentwise-minimal forced-blue `K5` requirements, and tests all
59,049 count vectors against those requirements. The resulting histogram and
survivor-stream digest agree exactly.

Finally, a straightforward ten-edge test over all `C(25,5)=53,130` vertex
sets checks the separately SHA256-pinned literal fixture. Direct incidence and
all-pair permutation checks recover the claimed signatures and order-three
symmetry. An exhaustive prefix/suffix comparison also confirms that, under the
committed full-signature ordering with the four minority bits first, the three
empty minority signatures occupy fixed positions 30, 31, and 32.

## Reproduce

Using Python 3.11 or later and the standard library, from this directory:

```bash
python3 independent_check.py --report /tmp/fixed_signature_review1.json
cmp report.json /tmp/fixed_signature_review1.json
python3 -O independent_check.py --report /tmp/fixed_signature_review1_O.json
cmp report.json /tmp/fixed_signature_review1_O.json
sha256sum -c SHA256SUMS
```

No SAT/SMT verdict, omitted proof trace, graph catalog, or network access is
used. The only imported target datum is the literal `sharp25.edges` byte stream,
which is pinned before it is parsed. Remaining trust boundaries are the
unformalized derivation, this independent Python source, Python exact-integer
semantics, SHA256, and the executing hardware.
