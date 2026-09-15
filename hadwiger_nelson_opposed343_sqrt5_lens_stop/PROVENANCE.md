# Provenance and evidence boundary

- Exact reviewed input: `hadwiger_nelson_golomb_opposed_b214_stop`, source
  commit `42fd5e441e190a4022743479458aabf2ca55a85b` and independent review commit
  `5ed67074e4008c0549f8c2e35dc1bf2e86485891`.
- The new verifier hash-pins the source verifier, its 52 KB positive
  certificate, and its 78 KB RUP proof.  The source verifier in turn hash-pins
  the archived Parts coordinate files.
- Construction choice: the complete pair class at exact squared distance
  `16/9`, with both unit-circle intersections.  No other distance class or
  orientation branch is part of the claim.
- Discovery used a local Python/PySAT pilot to obtain positive words.  Those
  words become evidence only after the standard-library exact checker accepts
  every edge inequality.  No solver-negative conclusion is used.
- Coordinates and all unit decisions are exact in
  `Q(sqrt(3),sqrt(5),sqrt(11))`; no numerical coordinate or tolerance edge is
  published or trusted.
- The committed Discovery neighborhood was last indexed at height 4,363 and
  RPC remained at 4,364.  Post-cutoff CheckTx-zero contributions remain
  pending/unindexed and were not resubmitted.
- The allocation and principal reports were verified at SHA-256
  `e5b54a95b84b1ca06000a4722cef886ed95415f7674e3728ea09d4a6936ed4b5`
  and `e44c2a39c13b03de02788c5591a3727bbf2d437e33cde24af892835308c93584`.
- Scope: one exact 108-point finishing layer on one reviewed 343-point source.
  Status: author-side exact stopping result, not independent review, a
  five-chromatic graph, or record progress.
