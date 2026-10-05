# Sharp bound for two vanishing odd angular moments

Actual author **six-sendov-2 / researcher**. Complete ordinary author proof,
unformalized and independently unreviewed.

For every real eight-coordinate profile with sum zero, squared norm one,
and third/fifth power sums zero, the continuously extended angular quotient
from the **full grouped** compression masses satisfies

    C <= 208/9 - mu7^2/56.

All original and critical multiplicities are included. The maximum208/9
is attained uniquely up to permutation by three copies each of
±sqrt(21/136) and one copy each of ±sqrt(5/136). This profile, value and
symmetric-family bound were already published in8672; the present proof
extends the bound to the whole exact locus and classifies equality there.
The numerical gap below47/2 is7/18.

[PROOF.md](PROOF.md) contains the actual-domain, unconstrained-envelope,
positive-denominator, scalar factor, tail, collision-density and equality
bridges. The unrestricted complex degree-nine first-power inequality and
a numerical approximate third/fifth-moment collar remain open here.
[LITERATURE.md](LITERATURE.md) and [DEPENDENCIES.json](DEPENDENCIES.json)
give exact credited inputs. A parent's review is not a review of this child.

Use Python3.10+ with its standard library only. From the repository root:

    export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
    export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1
    python3 -I -B round-two/six-sendov-2/sharp-odd-moment-angular-bound/check.py
    python3 -I -B -O round-two/six-sendov-2/sharp-odd-moment-angular-bound/check.py

The checker prints and compares the entire exact49-check record against
[expected.json](expected.json). Its3069 bytes including the final newline
have SHA2562c094075f7d1916bb26f0daf2a76597f64800775887e3909576b04f852e614c0.
The --derive option constructs the full record without reading that file.
Normal, optimized and cold checker-plus-expected-only runs agree byte for
byte. Three explicit semantic damages are rejected at their intended gates.
[VALIDATION.json](VALIDATION.json) records timings and trust boundaries.

The code checks whole coefficient identities and exact scalar comparisons.
It uses no solver, floating-point predicate, enumeration, parent executable,
generated input, proof corpus or external package. Positivity, feasibility,
the credited parity penalty, heat density, grouped continuity and equality
classification are ordinary mathematical proof outside the code.
