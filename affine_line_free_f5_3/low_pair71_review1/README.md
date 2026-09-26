# Independent review: two low planes at 71 points

This directory independently reviews the computer-assisted theorem in
[`low_pair71`](../low_pair71/) at exact source commit
`0d331185c9dbfb6db32ebffc8bdaae4e0b4aa144`.

**Verdict:** accept with high confidence the scoped theorem that every
71-point line-free subset of \(\mathbb F_5^3\) has at least two nonparallel
affine-plane sections of size at most nine, and the consequent complete cover
by 15 pairs of normalized low-plane profiles.

This is a structural reduction, not a decision of the remaining extremal
case. It neither constructs nor excludes a 71-point set, so the independently
accepted campaign interval remains
\(70\le r_5(\mathbb F_5^3)\le71\). See [`REVIEW.md`](REVIEW.md) for the proof
audit, exact guarantees, and trust boundary.

## Independent method

[`independent_check.py`](independent_check.py) imports none of the reviewed
Python or C++ modules. It:

1. compiles [`gray_spectra.cpp`](gray_spectra.cpp), which visits all
   \(2^{25}\) planar subsets in Gray-code order and updates only the six line
   occupancies through each toggled point;
2. independently regenerates the 85 centered profiles, all 15 low-profile
   pair types, and all \(5^6=15{,}625\) symmetric quadratic forms;
3. rebuilds all 698 sparse columns of the 71-row incidence system directly
   from row names; and
4. checks every integer inequality and right-hand-side evaluation in all 14
   Farkas certificates, followed by three malformed-certificate controls.

The independent planar output matches the reviewed catalogue byte for byte.
The certificate check obtains slack digest
`d55b69e4a7e6903fadbc50f2a31609e6c727b9b1a3d658047d96f88d11862c02`
and the same weakest exact bound
\(117641713/100000000>1\).

## Reproduce

Use Python 3.11 or later and a C++20 compiler:

```sh
python3 independent_check.py --out /tmp/low-pair71-independent \
  | cmp - EXPECTED.json
sha256sum -c SHA256SUMS
```

The review used Python 3.11.2 and GCC 12.2.0. The ordinary replay took about
seven seconds. The complete native census also passed AddressSanitizer and
UndefinedBehaviorSanitizer:

```sh
ASAN_OPTIONS=detect_leaks=1:halt_on_error=1 \
UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 \
python3 independent_check.py --sanitize \
  --out /tmp/low-pair71-independent-sanitize \
  | cmp - EXPECTED.json
```
