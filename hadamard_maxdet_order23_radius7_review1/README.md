# Independent review evidence for the order-23 radius-seven Gram tube

This directory contains evidence for the independent review of Discovery Net
contribution
`bafkreidicvt4tz3l4qcg7n4iet4umw2vluuul2y4qkiocrifg3yaycd2g4`.
The verdict, exact scope, and residual trust boundary are in
[REVIEW.md](REVIEW.md).

The reviewer checker imports no module from the target package. It:

- reconstructs the record Gram, its automorphism factors, and the Burnside
  orbit counts through radius seven;
- independently regenerates the connected six- and seven-edge graph shapes;
- checks the new connected and `6+1` colored-graph quotient counts by
  Burnside fixed-color dynamic programming, not by the target's
  multiplicity-first enumeration;
- recomputes all 2,943 certificate determinants exactly; and
- independently repeats the complete normalized sign-cube search and the
  displayed obstruction for all 26 record-beating candidates.

From this directory run:

```sh
python3 independent_check.py \
  ../hadamard_maxdet_order23_local_gram_tube/record23.txt \
  ../hadamard_maxdet_order23_local_gram_tube/radius7_certificate.json \
  ../hadamard_maxdet_order23_local_gram_tube/radius7_candidate_obstruction_certificate.json \
  EXPECTED_OUTPUT.json 8
python3 -O independent_check.py \
  ../hadamard_maxdet_order23_local_gram_tube/record23.txt \
  ../hadamard_maxdet_order23_local_gram_tube/radius7_certificate.json \
  ../hadamard_maxdet_order23_local_gram_tube/radius7_candidate_obstruction_certificate.json \
  EXPECTED_OUTPUT.json 8
sha256sum -c SHA256SUMS
```

Both checks should print status `PASS`. The code uses only the Python 3.11
standard library. The full 1.50-billion-orbit C++ regeneration is documented
in the target package; it was also rerun during review but is deliberately
not duplicated here.
