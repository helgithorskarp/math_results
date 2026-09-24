# Independent review evidence for C(13,6,3)=21

This directory reviews Discovery Net contribution
`bafkreibyzidibsfv6t2ycihb5vlalyy3uscaitmmspui5ozx7lsyxgqyfa` at exact
source commit `b9e68cee8e2071374921b6dd713595d0bc3022c1`.

The complete primary and whole-star searches in
`../covering_design_c13_6_3_exact_value/` were both rerun over every root and
matched their full expected summaries. The essential upstream 107-class link
catalogue was also regenerated with its primary search, independent
column-bundle search, and separate marked-degree-five decomposition.

`independent_audit.py` is additional reviewer-written evidence. It imports no
reviewed module. From the two JSON inputs it:

- checks that the 107 link records are the exact upstream projection;
- directly checks every catalogue covering;
- reconstructs all point automorphisms by pair-colour backtracking and a final
  block-family test;
- recomputes the three primary decoration-orbit counts and the independent
  labelled-root counts; and
- verifies the 21-block upper cover from the definition.

From the repository root, run:

```sh
python3 covering_design_c13_6_3_exact_value_review1/independent_audit.py \
  covering_design_c13_6_3_exact_value \
  covering_design_c12_5_2_classification \
  > /tmp/c1363-review.json
cmp /tmp/c1363-review.json \
  covering_design_c13_6_3_exact_value_review1/EXPECTED_OUTPUT.json
sha256sum -c covering_design_c13_6_3_exact_value_review1/SHA256SUMS
```

The structural checker is not an UNSAT certificate for the millions of joined
instances. Rechecking that exclusion requires the two documented full search
commands in the target directory and acceptance of their explicit execution
trust boundaries.
