# Homogeneous A5 pencils cannot concur

All 189 homogeneous four-position A5 pencils containing a binomial are
complex-affinely nonconcurrent, covering 387,072 unit-row lifts. Together with
the independently accepted three-position and no-binomial results, this
physically excludes **all 279 homogeneous nonmonomial pencils** and their
502,272 raw lifts.

The complete 1,404-pair anchor envelope has **4,320 distinct real parameters**.
Every resulting complete physical unit-distance graph is exactly
three-chromatic, including all 200 collision parameters. This is a restricted
A5 result, not a five-chromatic construction or a record improvement.

- [Proof and scope](PROOF.md)
- [Exact reproduction commands](REPRODUCE.md)
- [Complete verified counts and transcript hashes](EXPECTED.json)
- [Source provenance and prior proof premises](CONTEXT.json)

The generator uses the separating coordinate x+2y. The verifier independently
counts square-free fibers over x, including the 57 pairs that the previous
linear-fiber representation could not handle. It then checks the complete
physical graphs and positive colourings. The large root table is generated
locally and is not committed.

The starting named asymmetric class was h4195 pencil 412. The intrinsic
classification also covers all 27 binomial pencils removed before h4195;
no earlier exclusion or conditional aggregate allowance is assumed for them.
Independent-author review of this new package remains outstanding.
