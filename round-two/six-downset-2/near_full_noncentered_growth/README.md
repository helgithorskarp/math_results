# Positive near-middle support without centering

**six-downset-2**, researcher, 2026-10-02.
[PROOF.md](PROOF.md) gives an ordinary, unformalized author proof.
It has not been independently reviewed.

For every real capped H on all actual subsets of[n] of size at most n-2,
including the actual empty loop, the theorem forces a positive original
entry on a proper disjoint pair whose two sizes exceed
n/2-sqrt((n/2)log(4n^2)), at every integer n>=24.
Its positive original mass above the corresponding integer cutoff is
greater than1/(2n^2). No centering is required.

The near-half scale and log(4n^2) constant were already proved under
centering in the credited reviewer-3 audit of9201. The new increment is
removal of centering, positive entries and mass, and a general-k exact
weighted-tail criterion. The proof extends9424's k2 original-coordinate
two-test mechanism. This extra cap is distinct from Conjecture I; no
general H/I resolution, positive construction or optimal cutoff is claimed.

From this directory, with Python>=3.10 and no third-party package:

~~~sh
python3 -B verify.py --check expected.json
python3 -O -B verify.py --check expected.json
~~~

Both modes compare the **entire** frozen compact record.
Its SHA256 is
3577f7abccd41b481d946c7acb83840dd066ef08a9e97cdc6525eaf197501c84.
The summary reports606 full-star affine directions,64,258 checked
literal original entries, growth_start24, logarithm_constant4 and
positive_original_entries_and_mass=true.

[certificate.py](certificate.py) regenerates exact Fraction profiles,
weights, constants and sufficient cutoffs. [verify.py](verify.py) has
independent literal norm/count and original-coordinate checks, including
a signed noninvariant32-position trade. [affine.py](affine.py) is a
credited byte-copy of9365's direct/RREF star-only completion;
[model.py](model.py) is copied from9424's physical forms.
[expected.json](expected.json) is compact exact validation evidence.

Development was checked with CPython3.12.14, serial45-second guards and
all six native-thread variables1. Finite affine tables and perturbations
are not claimed PSD. The written all-n PSD/kernel, counted moment,
induction, calculus and Chernoff arguments supply the coverage bridge.
No solver, floating eigenspectrum, enumeration completeness, large
private artifact or external data is needed.
