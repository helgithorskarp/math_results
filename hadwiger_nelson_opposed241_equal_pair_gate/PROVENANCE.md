# Provenance and coordination

- Physical parent table:
  `../hadwiger_nelson_nonmono159_214_lowden2/points214.tsv`, SHA-256
  `97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f`.
- Reviewed source core:
  `../hadwiger_nelson_opposed241_conditional_core`, mathematical source
  commit `eb1263c7f9ac2b80120cd9521a6f99d2da435a7b`.
- Independent source review:
  `../hadwiger_nelson_opposed241_conditional_core_review1`.

The new proof reconstructs the geometry from the archived table and the
frozen source-label list; it imports no source or review executable.  The
point and edge hashes agree with the independent review, giving an entry-level
identity check for the graph on which the new words are tested.

The eight words were discovered from positive SAT models and then greedily
pruned so that no displayed row can be removed while retaining pair
separation.  Minimal cardinality is not claimed.  The public checker directly
validates the words and does not import a SAT package or solver output.

At production time the committed Discovery ledger remained stale at indexed
height 4363 while RPC height was 4364, last block 2026-09-11.  Any accepted
post-cutoff broadcast is pending rather than committed and must not be
resubmitted solely because it is absent from that index.
