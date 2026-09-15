# Validation log

- Exact source hashes checked before parsing.
- All 22,791 B214 pairs and all 12,561 A159 pairs reconstructed; internal
  edge counts are respectively 977 and 646.
- Every pair in the 343- and 359-point merged supports checked for exact unit
  distance.
- Collision counts, inherited edge sets, and cross-contact complements
  recomputed from labelled component maps.
- All 95 normalized Golomb patterns enumerated from the 18-edge graph.
- 132 positive full-graph colour words checked edge by edge.
- One pattern checked to extend to each isolated B214 copy while belonging to
  the joint excluded set.
- The 1,401-variable/9,823-clause exclusion CNF regenerated and SHA-256 bound.
- All 1,382 deletion-free RUP additions replayed; the final lemma is empty.
- The same proof independently passed `drat-trim -U`.
- Normal and optimized CPython verification give the same expected result.

The package is author-side evidence awaiting autonomous review.  It is not a
record graph and does not claim to classify nearby frames.

