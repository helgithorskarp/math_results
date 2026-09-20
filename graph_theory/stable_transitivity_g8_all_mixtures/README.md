# Exact stable transitivity on the complete `G8` mixture face

## Result

Let `G8` be the partial tournament on vertices `0,...,7` with fixed arcs

```text
01 02 03 40 60 70 13 14 51 16 71 23 24 52 62 27 35 36 37 45
```

and unspecified pairs

```text
05 12 34 46 47 56 57 67.
```

A **degree-`k` extension of `G8`** is a `k`-tournament in which every fixed
arc above has multiplicity `k`, while the increasing orientation of each
unspecified pair has an arbitrary multiplicity in `{0,...,k}`.  If `m(W)` is
the stable-transitivity number of a `k`-tournament `W`, the source and compact
certificates here prove:

> **Exact computer-assisted theorem.** For every `k>=1` and every degree-`k`
> extension `W` of `G8`,
>
> ```text
> m(W) = ceil(7k/6).
> ```

This class contains `(k+1)^8` labeled mixtures at each degree.  It includes
all rays through the 256 ordinary completions of `G8`, but also all mixtures
strictly inside that eight-dimensional box.

The theorem is parameter-uniform.  The computer checks six finite residue
boxes; an exact additive argument then proves all `k`.

## Proof idea

The key profile equivalence says `m(W)<=a` exactly when `k+2a` total orders
can be chosen so that every arc `e` occurs `W(e)+a` times.  Every total order
predicts at most 13 of the 20 fixed `G8` arcs, so any such profile obeys

```text
20(k+a) <= 13(k+2a),
```

and hence `a>=ceil(7k/6)`.

For each residue degree `r=1,...,6`, the files `corners_dr.txt` give sharp
profiles at all `2^8` corners.  Swapping adjacent vertices across one of the
eight unspecified pairs changes exactly that one target coordinate.  The
verifier performs these exchanges while retaining only the first profile for
each target and certifies all `(r+1)^8` targets.  Finally, write `k=6q+r` and
split each of the eight target coordinates into `q` digits in `{0,...,6}` and
one digit in `{0,...,r}`.  Adding the corresponding certified profiles gives
the upper bound `7q+ceil(7r/6)=ceil(7k/6)`.

See [THEOREM.md](THEOREM.md) for the complete argument.

## Verification

Only a C++17 compiler is needed for the theorem check:

```bash
g++ -O3 -std=c++17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
  verify_boxes.cpp -o verify_boxes

./verify_boxes corners_d1.txt corners_d2.txt corners_d3.txt \
  corners_d4.txt corners_d5.txt corners_d6.txt
```

The expected output is in `EXPECTED_OUTPUT.txt`.  On the recorded Debian 12
run with GCC 12.2.0, verification took about 10 seconds and used no solver,
randomness, or floating point.  The largest retained table has `7^8 =
5,764,801` entries.

The sanitizer exercise used during production was:

```bash
g++ -O1 -g -std=c++17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
  -fsanitize=address,undefined -fno-omit-frame-pointer \
  verify_boxes.cpp -o verify_boxes_san

ASAN_OPTIONS=detect_leaks=1:halt_on_error=1 \
UBSAN_OPTIONS=halt_on_error=1 \
  ./verify_boxes_san corners_d1.txt corners_d2.txt corners_d3.txt \
  corners_d4.txt corners_d5.txt corners_d6.txt --max-degree 4
```

Use `sha256sum -c SHA256SUMS` to check the committed sources and certificates.

## Files and trust boundary

- `verify_boxes.cpp` independently enumerates all `8!` total orders, validates
  every corner profile from arc definitions, constructs all valid adjacent
  exchanges, and checks complete box coverage.
- `corners_d1.txt`, ..., `corners_d6.txt` contain 256 sharp corner profiles
  each.  Together they are about 146 KB.
- `derive_corners.py` reproducibly transforms the cited order-eight and ray
  certificates into the six corner files.  Regeneration is provenance, not a
  proof dependency: the C++ verifier checks the committed profiles directly.
- `PROVENANCE.md` records immutable source commits and hashes.

The theorem trusts the stated finite reduction, the inspected C++
implementation, compiler, and hardware.  It does not trust the upstream
profile generator or any optimizer: every imported profile is decoded and
checked against all 28 pair margins.  The exchange closure is a transparent
exhaustive computation rather than a separately stored multi-gigabyte
certificate.

## Scope and literature status

Davis and Schroeder introduced stable transitivity and `m(n,k)` in
[*Relating tournaments and permutations with xrays*](https://arxiv.org/abs/2606.21532v1)
(2026).  Chindelevitch and Harutyunyan identified the common `G8` obstruction
in ordinary tournament predictability in
[*Tournaments determined by three and five voters*](https://arxiv.org/abs/2607.26690v1)
(2026).  Earlier certified work proved the exact ray formula
`m(kT)=ceil(7k/6)` for each ordinary completion `T`, and a later Discovery Net
result covered the whole degree-two box.  Targeted primary-source and graph
searches through 2026-09-20 found no prior classification of every degree-`k`
extension of `G8`; the theorem is therefore apparently new relative to those
searches, not a historical-priority claim.

The result is confined to this exposed `G8` face.  It does **not** determine
`m(8,k)` over arbitrary `k`-tournaments and makes no claim at order nine.
