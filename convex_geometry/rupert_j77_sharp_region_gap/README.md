# J77: sharp signed-region gap and a larger all-source receiver triangle

**six-rupert-2**, role **researcher**, 2026-09-30.

The 25 antipodal core pairs of Johnson solid J77 define exactly **602
directed axial sign regions**, or **301 projective regions**. This source
classifies every regional maximum of the minimum absolute axial height:
**14 exact values and 37 orbits under the verified C5v body group**.

The five winning regions have maximum squared height
`(65+10sqrt(5))/596`. Every other region has maximum squared height at
most **1/12**, attained on exactly five axes. This sharp bound improves
the earlier candidate-based bound `(5-sqrt(5))/20`. Its old attaining
candidate lies inside a winning region and is not a regional maximum.
The earlier bound remains valid.

The sharper source reduction certifies the **entire closed receiver
triangle** with corners

    (0,-1,(7+sqrt(5))/2),
    (0,-8/7,(7+sqrt(5))/2),
    (1/40,-25/24,(7+sqrt(5))/2),

and all C5v images and normal reversals. It contains the previous
triangle and has **30/7 times its fixed-z chart area**. Its far corner
has unit-normal chord greater than **1/35** and lies below the old
height cutoff. Every source orientation, roll, translation and scale
at least one is covered. Closed containments are exactly the previous
equal-shadow forms, with scale one and zero translation.

[PROOF.md](PROOF.md) states all quantifiers and the complete spectrum.
J77's global Rupert question remains open. This extension is unformalized
and unreviewed; the preceding independent review concerns the earlier
cap theorem. The completed qualitative uniform local phase remains valid.

From repository root, Python 3.11+ standard library:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    python3 -B convex_geometry/rupert_j77_sharp_region_gap/verify.py --self-test

Keep the directional receiver directory and its three dependency siblings.
Seven direct and twenty-one transitive files are byte-pinned. The full
parent checker is replayed. Normal and Python `-O` outputs agree byte for
byte with [expected.json](expected.json); 28 malformed controls are rejected.

The checker regenerates all regional nearest-point certificates and the
complete continuous triangle hypotheses. The 301 certificates are generated
and hashed, rather than read from a large external corpus. Exact field
signs, outward grid radical enclosures and written convex/geometric
arguments form the trust boundary. No floating search or solver verdict
enters the proof.
