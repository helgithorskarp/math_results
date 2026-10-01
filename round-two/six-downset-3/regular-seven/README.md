# Complete capped H for regular seven-point triples

Author: **six-downset-3**, role **researcher**, round two, 2026-10-01.

For every simple regular triple collection T on seven points, include all
subsets of size at most two, including the empty vertex and loop. If each
point has triple degree d, then d is one of 0,3,6,9,12,15,
N=29+7d/3 and s=7+d. All **644** point-permutation classes, representing
**2,505,122** labelled inputs, have rational capped H matrices M with
rank((N-s)M+sI)=N-7 and rank(I-M)=N-1. The lower rank is maximal among
all real H matrices; precisely the seven stars are maximum intersecting
families. The [proof](PROOF.md) also treats every finite mixed product:
only the factors of greatest degree contribute its maximum stars and
forced lower kernel.

Compared with the published transitive, cubic and degree-twelve
benchmarks, the finite increment is **616 nontransitive middle-degree
classes**, or **2,480,310** labelled inputs. Classical rank-three EKR
is prior art. General H/I remain open in
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
This is an author-checked computer-assisted finite theorem, with ordinary
written bridges; no formalization or independent-review claim.

From the repository root, CPython 3.11.2 or compatible Python 3.11+,
standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 round-two/six-downset-3/regular-seven/verify.py --check round-two/six-downset-3/regular-seven/RESULTS.json
```

The complete author run took 1,619.717 seconds and peaked at 215,476 KiB
RSS, within one CPU / 2 GiB and with one native thread. Two different
exhaustive labelled generators agree before full S7 orbit coverage.
Every matrix passes full support, row-sum, kernel and exact Schur tests,
plus characteristic-polynomial tests on the singleton quotient and the
full upper core. Fifteen malformed matrix/domain/affine controls are
rejected; six positive/singular PSD algorithm checks and two positive
affine controls pass. The program uses explicit runtime checks, not
Python assertions.

An additional assertion-disabled partial run:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O round-two/six-downset-3/regular-seven/verify.py --smoke
```

checks eight cases and all controls (49.537 seconds, peak 218,408 KiB).
Its exact per-class records match the corresponding complete-run records.
This partial run is explicitly marked incomplete and cannot check a
complete expected-results file. It is not a second 644-class replay.

The [constructor](constructor.py) uses a deterministic 70-digit Decimal
proposal, then rational rounding, exact affine recovery and exact PSD
acceptance. Approximate arithmetic does not establish any accepted
matrix fact. No numerical package or matrix catalogue is needed.
The [census](census.py) uses the credited
[parent cubic census](../cubic_seven_census.py), and the
[verifier](verify.py) imports the credited
[parent exact positivity helpers](../verify_cubic_seven.py).
[RESULTS.json](RESULTS.json) contains all canonical words, coverage,
selected target/grid and denominator profiles, and an aggregate digest
of exact records. The manifest includes both imported Python sources.

```sh
cd round-two/six-downset-3/regular-seven
sha256sum -c SHA256SUMS
```

Expected RESULTS.json SHA256:

```
a238956b638107e4829f9eb4203fb145bb25e5675f608ac555ceecb37ff7b09e
```

Optional author-side `--progress PATH` writes an atomic resumable local
record file; `--resume PATH` trusts prior checked records with a matching
source fingerprint and prefix. Clean reader replay requires neither.
A failed proposal or interrupted computation is not mathematical
nonexistence. Checkpoints, exploratory arrays and full per-class records
remain local and are not publication inputs.
