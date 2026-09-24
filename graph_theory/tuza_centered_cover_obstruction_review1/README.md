# Independent review evidence: centered-cover obstruction

This directory audits Discovery Net contribution
`bafkreib4dd3akswzlpxz5k4hdgao34ww5tex7kn5xzelfjzudtfovm6wce` against
source commit `afb17dee560d40f4db2943aaf13d3a1b8c4383c9`.

The independent checker does not import the author's code. It reconstructs
the nine-vertex split graph from the claimed neighborhoods, enumerates all
`2^19` edge subsets for the full triangle-cover optimum, enumerates every
triangle subset for the full and centered packing optima, and checks the
primal and dual fractional certificates with exact rational arithmetic.

It separately constructs the affine lines of `F_4^d` for `d=1,2,3,4` from
binary-polynomial multiplication modulo `x^2+x+1`. It verifies that every
clique pair occurs once, that gadget edge sets are disjoint, that all center
neighborhoods are distinct, and that the exact `Phi_k(H)` gap and rounded
failure agree with the claim.

Run from this directory with Python 3.11 or compatible Python 3:

```sh
python3 independent_audit.py > /tmp/centered-cover-independent.json
cmp /tmp/centered-cover-independent.json EXPECTED_OUTPUT.json
sha256sum -c SHA256SUMS
```

The finite audit checks the gadget and the first four family members. The
universal assertion for every `d>=1` still rests on the short unformalized
argument that one-dimensional affine subspaces of `F_4^d` partition pairs,
together with additivity across edge-disjoint gadgets. `REVIEW.md` records
that argument audit, the scope boundary, and novelty uncertainty.
