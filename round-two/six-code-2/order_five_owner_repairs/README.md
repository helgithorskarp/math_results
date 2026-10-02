# Saturated C5 bases: sharp retention-63 bound

**six-code-2, researcher.** Every arbitrary A(18,6,5) packing sharing at
least 63 words with a member of the specified saturated-fixed-point C5
68-word family, or any point relabeling of one, has at most 68 words.
See [PROOF.md](PROOF.md) for the full hypotheses, reduction, dependencies
and limits. The target packing has no symmetry assumption.

The proof uses positive owner/color labels, not a solver's absence verdict.
A global four-deletion field reduces 52,120,640 five-type deletion anchors
to 3,833 exceptional domains, all independently regenerated and properly
five-colored by `verify.py`. Actual point maps cover the eight original
centralizer representatives. The prior full base census remains a separate
mathematical dependency. This new repair claim has no independent researcher
review yet.

Run from the repository root using CPython 3.11 or later, standard library
only, with fresh output directories:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-code-2/order_five_owner_repairs/verify.py --work /tmp/c5-five-owner-check
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O -B round-two/six-code-2/order_five_owner_repairs/verify.py --work /tmp/c5-five-owner-check-optimized
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-code-2/order_five_owner_repairs/validate.py --work /tmp/c5-five-owner-damages
```

Successful verification writes `EXACT_RESULT.json` equal to `EXPECTED.json`,
4,248 bytes with SHA256
`9e670c39ccaa4e06e678ec7e446698c443f145dab8409a3f1dbd22a230c78dc5`.
It reports `COMPLETE_POSITIVE_OWNERSHIP_AND_SPARSE_FIVE_COLOR_CERTIFICATE_AUDIT`
and sharp maximum 68 when at least 63 base words are retained. Timing and
peak memory are separate in `EXECUTION.json`. The initial exact-check guard
is 60 seconds; an interrupted or incomplete check establishes nothing.

`CLASSIFICATION.json` is the exact eight-base fixture from the census source
`8ad8ea28df4a8fd12f4927e4bad879a1831f96ab`. `POINT_MAPS.json` contains
the four positive transports previously checked in retention-65 source
`25cd2b0e604b2cbf525030f13910edb558d4e780`. The checker validates their
literal mathematical properties; neither fixture's metadata is an oracle.
`OWNERS_FOUR.json` has 7,365 outside-word owner labels. `COLORS_FIVE.json`
has 3,690 five-blocker-word labels and 143 conditional recolorings.

The previous five-type classification, classical design and known 69-word
construction are prior art. This certificate does not improve an unrestricted
bound or cover all 68-word packings. Large private discovery outputs are not
needed for reproduction and are not included.
