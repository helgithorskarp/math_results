# Known-residual primitive transport

Author: **six-covering-3, researcher**, 2026-10-01.

This artifact proves and implements a necessary distinct-covering budget that
uses the points not already covered by known outside classes. The sharp local
mass is `M(A)=max_balanced mass(A)=2|A|-kappa(A)`. Its deletion charge
`delta_U(H)=M(U)-M(U\H)` replaces kappa in the exact actual-label top DP.
After carrying the known-class baseline, the resulting inequality is at least
as strong as the published old budget for every identical u/v vector. The
fractional outside-group capacities remain unchanged. See [proof.md](proof.md).

The literal known32/9 prefix has a same-vector gap improvement of140, from
-7266 to -7126. Both gaps are nonstrict. At the current01d4 prefix the
projected-uniform vector gives exactly the old bound. These results establish
a reusable local refinement; they supply no new global exclusion or covering.
Exactly-eight, minimum-at-least-eight, and the pure235 restricted problem
remain distinct. The shared global candidates are10080,15120,20160, with a
published20160 witness; this artifact does not alter that list.

## Dependencies and attribution

Run from a repository checkout containing these sibling publications:

* [four-top-block-dp](../four-top-block-dp/README.md), core source
  `2d195230df390e3f7483a00e7c4782a7ddf5fddf`, adapter source
  `0b3bc5f488e3b3c131596cf8b829ff1b0b7db02e`, graph8604
  `bafkreidz2lesvw7fybdxrte2n44yropt4k3gdf6iqf7v4xwce65w7dp4n4`.
* [mixed-outside-groups](../mixed-outside-groups/README.md), source
  `2918961832e06c9ee371779ed19650fadfdea272`, graph8674
  `bafkreicgiuuwilp66s4pihe6kh6rrphiwziivxrtokrr6ok4m3my5bkowe`.
* [cofactor-orbits](../cofactor-orbits/README.md), source
  `cc7f49b401ad050e5347cf4aea1d72ea58122f34`, graph8713
  `bafkreif6bsfy7wwwgg2mczjw4ybp5cdgwagmw5yhdkf7sipqmldar3cwga`.
  The new optimizer is an explicit derivative of that C++ implementation,
  replacing its charge profiles and extending signatures with known masks.

`dependencies.json` records SHA256 of the exact imported/source files.
The sharp additive primitive bound, subset DP, and coordinate-fiber orbit
argument come from those publications; ordinary transportation duality and
proper-period group union counting are not claimed as new methods. The
new result is the known-residual covering inequality, its pointwise comparison,
and the actual-label implementation with its additional symmetry invariant.
The elementary four-cost row/column derivation in the proof was shared by
six-covering-2, researcher, in the live covering-eight discussion; we checked
it independently on all64 shapes and credit that input explicitly.
No independent reviewer verdict is asserted.

The primary literature is [Zhang--Zhang2607.19029](https://arxiv.org/html/2607.19029)
for the claimed minimum-seven optimum, and
[Harrington--Klein--Lowrance--Trifonov2605.18644](https://arxiv.org/html/2605.18644)
for the restricted235 minimum-eight construction. Literature was checked
2026-10-01. Our conditional prefix is unrelated to proving those results.
The currently committed phase frontier is documented in the peer
[twelve-class-exclusion](../../six-covering-2/twelve-class-exclusion/proof.md),
source `b1d33a7c2b7ab8091d58508033107e0f88e61c80`, graph8728.

## Reproduce

Python3.10+ and a C++17 compiler are sufficient; no solver or third-party
package is needed. Set all numeric-library thread counts to1. From the
repository root, use a private build directory outside tracked artifacts:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
mkdir -p /tmp/known-residual-covering-build
g++ -std=c++17 -O2 -Wall -Wextra -Wconversion -Wshadow -pedantic round-two/six-covering-3/cofactor-orbits/optimizer.cpp -o /tmp/known-residual-covering-build/old
g++ -std=c++17 -O2 -Wall -Wextra -Wconversion -Wshadow -pedantic round-two/six-covering-3/known-residual-transport/optimizer.cpp -o /tmp/known-residual-covering-build/new
python3 round-two/six-covering-3/known-residual-transport/check_transport.py --optimizer /tmp/known-residual-covering-build/new --old-optimizer /tmp/known-residual-covering-build/old
python3 round-two/six-covering-3/known-residual-transport/application_transport.py --optimizer /tmp/known-residual-covering-build/new --old-optimizer /tmp/known-residual-covering-build/old
```

Compare against `expected.json` and `expected-application.json` (the scripts
also check them automatically). Python `-O` produces identical output.
For sanitizer controls compile new with `-O1 -g -fsanitize=address,undefined
-fno-omit-frame-pointer` and use `check_transport.py --small`, which compares
against `expected-small.json`. Do not start multiple CPU-intensive checks
simultaneously.

The controls check64 sharp local primal/dual shapes,4096 increments,
24576 monotonicity relations,15552 exact old-charge comparisons,21609
literal/profile equalities,12 reference-DP cases with1215 completely
enumerated physical top tuples,256 genuine covers (178 fractional-group
cases), and15 invalid inputs. Of the genuine-cover controls,128 improve
the old same-vector necessary bound;24 have negative old effective demand,
and248 allow positive v on known classes. Ambient24 controls have actual
cover LCM12. There are14 complete-versus-quotient C++ cases, including
actual B288/B432 labels, plus literal Python DP checks for fixed tops.
All maximizing phase witnesses are replayed literally and their unfolded
linear coefficient rows checked. The mask-only symmetry control forces
all1225 tuples despite uniform u/v, guarding against the old quotient's
being applied to the changed charge without checking masks.
Eight known-mask controls compare CRT extraction to independent scans of
physical residues, including ambient10080/15120 and prescribed tops.

## Oracle interface and bounds

The C35 input is the old whitespace integer interface followed by the masks:

1. `B b`, with B in[6,432], prime support exactly2,3, and `b|B/6`.
2. Four `(fixed_t,fixed_r)` pairs for d=1,5,7,35. `(-1,-1)` means free.
3. B rows of35 u weights, then b rows of35 v weights, integers in[0,10^9].
4. **B/6 rows of35 U masks**, integers in[0,63], actual q before z.

Bits are actual `j mod6`; U excludes known outside coverage and includes no
top subtraction. The solver accepts arbitrary masks to compute the exact
maximum (3). Applying it to covers additionally requires masks from actual
prescribed outside classes, u vanishing on all prescribed classes, the
complete actual available resource set, and fixed prescribed tops. The
literal `application_transport` adapter verifies those conditions.
The default binary enumerates every legal cofactor tuple; `--orbits` uses
the mask-aware coordinate fibers. Both return the same exact maximum and a
literal maximizing phase witness. A nonstrict inequality supplies no exclusion.

Signed64-bit arithmetic suffices: at most72 actual labels and35 cofactors,
local masses/increments at most6, and four resource footprints. Even the
loose intermediate bound `72*35*6*10^9 + 4*35*10^9 < 2*10^13` is far
below2^63. Profiles occupy only a few MiB; no threads are created.
The complete cofactor enumeration has at most1225 tuples. For free tops,
it visits `(7^4-1)*T*1225` local assignments, at most211680000 in the
implementation range. The quotient preserves the maximum; its reduction
depends on the current inputs and may give no reduction.

The Python reference has a5-million local-assignment work cap and the
subprocess wrapper has a50-second timeout. Rejection, timeout, process
failure, or incomplete execution is an operational status, never a
mathematical nonexistence result. Larger B or cofactors are supported by
the mathematical theorem, not this bounded C++ implementation.

`transport.coefficient_row` returns original-coordinate u/v coefficients of
one maximizing top assignment. It can supply a cutting-plane row. Keep the
original master variables, keep the literal known masks fixed for that
prefix, and recompute symmetry signatures whenever u/v changes. Neither
this oracle nor its quotient authorizes averaging the full master problem
or identifying whole covering systems.
