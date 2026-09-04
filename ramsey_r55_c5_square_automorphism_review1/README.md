# Independent review evidence for the `C_5^2` Ramsey obstruction

This directory contains reviewer-1's clean-room verification of the claim
that the forced `C_5^2` action on a hypothetical Ramsey `(5,5;43)` graph has
no invariant red/blue coloring avoiding monochromatic five-sets.

The standard-library checker is independent of the submitted Python source,
submitted C++ checker, and `drat-trim`. It:

1. solves the orbit-count equations for a 43-point `C_5^2`-set whose
   nonidentity elements have 3 or 8 fixed points;
2. checks transitivity of `GL(2,5)` on the twenty triples of projective
   lines;
3. constructs the 43-point action from two generators and independently
   enumerates its 51 edge orbits;
4. rebuilds all projected Ramsey five-set clauses and matches the canonical
   CNF SHA-256; and
5. decompresses the submitted 6,890-byte proof and checks all 172 additions
   by direct reverse unit propagation, ending with the empty clause.

Run from the repository root:

```bash
python3 ramsey_r55_c5_square_automorphism_review1/independent_verify.py \
  ramsey_r55_c5_square_automorphism_obstruction/proof.drat.xz
```

Expected output:

```text
PASS solutions=20 line_triples=1 edge_orbits=51 clauses=52362 cnf_sha256=ffb03c6ae916ee712a94a66f5cbbfc85d86ae08e19e4476a6e8c504e2505561f rup_additions=172 deletions=232 final_empty=true
```

This evidence verifies only the new `C_5^2` finite obstruction and its
group-action reduction. The full theorem also imports the classification
that order-five automorphisms can have only seven or eight 5-cycles. During
this review, the four previously unreviewed middle-type DRAT proofs were
freshly reconstructed and replayed with pinned `drat-trim`; reviewer-1 had
already independently reviewed the fixed-33 and fixed-38 exclusions. Those
larger dependency proofs are not duplicated here.

Trust is confined to CPython integer/container semantics, SHA-256 and xz
decompression, the checked-in proof bytes, the transparent CNF bridge, and
the separately reviewed order-five classification. This is not a proof
assistant formalization and proves a structural automorphism restriction,
not existence of a 43-vertex Ramsey graph or `R(5,5) >= 44`.
