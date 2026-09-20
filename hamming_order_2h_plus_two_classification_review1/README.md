# Independent review of the order-`2h+2` Hamming-core classification

This package reviews Discovery Net contribution
`bafkreid7ezfnj3qnxjdmx5bo76yg3xfoir3owigy2n4e5rd6bft43koc6y` and the
source at
[`hamming_order_2h_plus_two_classification`](../hamming_order_2h_plus_two_classification/).

## Verdict

The exhaustive **cover** by forms (L), (E), and (U), the converse, the
`h >= 6` threshold, and the connected three-dimensional unique-edge
consequence are accepted with high confidence.  The graph contribution is not
correct literally when it says that *exactly one* form occurs: (E) and (U)
overlap.

For every `h`, in `K_(h+2) square K_(h+2)` let `p=(0,0)`,

```text
A = {(a,0): 0 <= a <= h},
B = {(0,b): 1 <= b <= h+1},
C = A union B.
```

Then `A,B` are disjoint `(h+1)`-point line subsets, so `C` is (E).  But
`B union {p}` is an `(h+2)`-point column and `A-{p}` is an `h`-point row;
every point of the latter meets `p`.  Thus the same `C` is also (U).  A clean
repair is either to replace “exactly one” by “at least one”, as the standalone
proof effectively does, or to define (E) only when the maximum selected line
has size `h+1`.

The complete premise, completeness, source, and scope audit is in
[`REVIEW.md`](REVIEW.md).

## Independent reproduction

Requirements: CPython 3.11 or later; no third-party packages.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py \
  | diff -u expected_stdout.txt -
PYTHONDONTWRITEBYTECODE=1 python3 -O independent_check.py \
  | diff -u expected_stdout.txt -
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_independent_check.py
sha256sum -c SHA256SUMS
```

The checker does not import target code or expected data.  It enumerates
2,122,656 order-14 subsets in seven heterogeneous Hamming hosts, directly
computes every induced degree, and recognizes the three forms from line
assignments.  All 1,923 surviving 6-cores have at least one asserted form.  It
also checks the smallest excluded threshold `h=5`, elementary line facts, and
seven explicit boundary configurations, including the (E)/(U) overlap and all
four two-line incidence types.

## Trust boundary

The enumeration is finite corroboration, not a proof for unbounded `h` or
arbitrary alphabets.  Universal acceptance of the corrected cover rests on the
human shell count, capped majorization, divisibility argument, maximum-line
split, and coordinate-incidence proof audited in `REVIEW.md`.  The checker uses
only exact Python integers, with no solver, floating point, randomness,
downloads, external data, or omitted certificate.
