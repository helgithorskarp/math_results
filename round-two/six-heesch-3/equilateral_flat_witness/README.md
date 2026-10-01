# Flat ports permit two coronas on an imbalanced bowed Tile(1,1)

Author: **six-heesch-3**, role **researcher**, 2026-10-01.

An explicit Jordan disk with four inward quartic bows, two outward bows
and eight flat unit ports has

    2 <= Hc <= Hh <= 10.

The bow multiplier can be any `0<epsilon<=1/4`; the literal certificate
uses 1/4. Two strict disk coronas have cumulative sizes 1, 8 and 23.
The all-motion finite upper bound uses curvature, including arbitrary
motions, reflections and partial flat interfaces. See [proof.md](proof.md).

This is an intermediate construction, not a Heesch record. It shows why
the nonflat hypothesis in the earlier [amplitude-class exclusion](../equilateral_hat_bows)
is necessary. Its specific 23-copy branch cannot reach seven coronas by
the same rigorous resource bound; exact H remains undetermined.

Reproduce from the repository root with CPython 3.11, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -B round-two/six-heesch-3/equilateral_flat_witness/check.py --expected
```

The solver-free reader verifies all 116 shared unit ports, the three
simple boundary cycles, every fully covered older vertex and port,
20,836 nonincident segment pairs and four malformed controls. The least
squared reference-edge separation is exactly `4-2*sqrt(3)`. The graph
isotopy and curvature-injection steps are written proofs. There is no
primary atlas, incomplete enumeration or numerical geometry in the reader.

Files: [certificate.json](certificate.json), [check.py](check.py),
[geometry.py](geometry.py), [expected.json](expected.json), [proof.md](proof.md).
Normal and optimized readers agree. Measured runs took 2.356 and 2.347 seconds,
with 20,616 KiB peak child RSS on one CPU. Certificate SHA256:
`36daa77684dc2b5f6d85e050a1b638b12df4135dd548623de9cccfa8d5c81bae`.
The geometry source is reused unchanged from the published nonflat package.

Primary polygon/Spectre attribution: Smith, Myers, Kaplan, Goodman-Strauss,
[A chiral aperiodic monotile, Section 2](https://arxiv.org/html/2305.17743v2).
The obstruction uses the prior campaign [curvature resource lemma](../curvature_capacity/proof.md).
The [author's Heesch census](https://cs.uwaterloo.ca/~csk/heesch/) fixes Hc/Hh conventions.
