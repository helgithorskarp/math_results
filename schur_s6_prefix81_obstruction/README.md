# An 81-entry obstruction to extending the Fredricksen–Sweet partition

**Exact restricted result.** Let `b` be the six-colouring of `[1,536]` printed
by Fredricksen and Sweet (2000), with their colour labels, transcribed in
`baseline.txt`. There is no classical sum-free six-colouring `c` of `[1,537]`
such that `c(x)=b(x)` for every `1 <= x <= 81`.

The other 456 colours, including that of 537, are unrestricted. The conclusion
also holds after any global permutation of the six labels. No reflection or
other symmetry is assumed for `c`. Repeated summands `x=y` are included.
This is a fixed-prefix obstruction, **not** an upper bound for S(6), and no
new lower bound is claimed.

The certificate consists of **351 elementary colour deletions**, including
23 deductions using doubling triples. Each deletion names one triple `x+y=z`
whose other distinct vertices have already been forced to the deleted colour.
Eventually all six colours of 537 are excluded. The separate checker uses
sets of possible colours and the integer equation directly; it imports no
generator, SAT solver, or third-party package. See [PROOF.md](PROOF.md).

## Reproduce

Python 3.11 or later, standard library only; tested with CPython 3.11.2.
From this directory:

```sh
python3 check.py
python3 test_checker.py
python3 generate.py --output /tmp/schur-prefix81-proof.json
cmp prefix81_proof.json /tmp/schur-prefix81-proof.json
sha256sum -c SHA256SUMS
```

`check.py` prints [expected.json](expected.json): `verified: true`, 351 deletions,
23 doubling steps, contradiction at 537, and 71,824 checked unordered baseline
triples. The four checker controls pass; they include the classical two-colour
Schur obstruction and rejection of corrupted or truncated deductions. Generation
and checking each take well under a second on the development host.

The baseline file contains 536 digits, with colour labels `1` through `6`,
followed by a newline. Its SHA-256 is
`2fdf85110de782426dd5deccfa7244f182441fda9870db64ba8e4eea7e3d600d`.

## Scope and search consequence

A search for a 537-colouring must allow a change within the first 81 entries of
this particular baseline. Fixing a longer prefix cannot help. This conclusion
allows arbitrary changes outside the prefix, regardless of their number.

The generator also reports two limited controls. Fixing only the first 80
entries on `[1,537]` leaves 95 singleton domains and no contradiction under this
propagation rule. This is **not** evidence that the remaining constraints are
satisfiable. Fixing the first 81 on `[1,536]` produces 443 singleton domains,
consistent with the known baseline. Thus 81 is the threshold for this specific
unbranched propagation experiment, not a proved minimum prefix length for
nonextendibility. The contradiction certificate does not depend on this
threshold claim or on completeness of the generator.

## Sources and provenance

- H. Fredricksen and M. M. Sweet, *Symmetric Sum-Free Partitions and Lower Bounds
  for Schur Numbers*, Electronic Journal of Combinatorics 7 (2000), R32,
  [publisher page](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32),
  [paper](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v7i1r32/pdf).
  The displayed construction lists the smaller member of each reflection pair
  about 537, except that 179 and 358 are explicitly given different colours.
  We transcribed those entries, reflected the ordinary pairs, and directly
  checked all 71,824 Schur triples. This input is an old construction.
- N. Bengone et al., *Shifted S-templates and improved lower bounds for Schur
  numbers*, [arXiv:2607.15034v1](https://arxiv.org/abs/2607.15034v1), July 2026,
  still uses S(6) >= 536. The convention here is the largest colourable integer,
  so a new lower bound starts at 537.

The computation was performed on 2026-09-28. The baseline agrees byte for byte
with the separate Team Schur computational researcher's transcription. A
targeted literature search and the committed Discovery Net graph were checked
for overlapping work. No priority claim is made. The separate distance-from-
baseline project is outside this contribution's scope.

Trust boundary: elementary integer arithmetic, the small checker, and its
Python runtime. This is a directly checkable finite deduction, not a
proof-assistant formalization or independent peer review. Source transcription
identifies the historical input; the certificate's logical validity is checked
against the supplied explicit prefix.
