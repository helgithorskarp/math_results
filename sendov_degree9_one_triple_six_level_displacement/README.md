# Whole one-triple six-level degree-nine displacement and phase basin

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Complete ordinary written author proof and exact rational evidence.
Every kernel was freshly rebuilt under normal and optimized execution,
with entire selected-case comparisons and complete record-union gates.
Independent review is pending; the proof is unformalized.

[PROOF.md](PROOF.md) proves the credited J_* maximum and equality orbit
on every balanced max-normalized profile with at most five actual values
or exactly six of multiplicities3,1,1,1,1,1. The new global direction bound is

    dist(theta/sqrt(mu2),O*)^2<=5000(J*-J).

The proof includes all singleton-saturated triple-interior profiles and
collision boundaries. It extends the credited sharp complex displacement
basin and near-sharp geometry to the corresponding original-phase class,
with eight independent inward depths:

    R_(6,3)(a)^2/[(1+a)(a-5/8)] -> 106496/(5J*).

The scalar optimum and prior smaller-class results are credited.
The remaining six-level2+2+1^4 cohort, seven/eight-level maximum, effective
cutoffs and unrestricted first-power endpoint remain open here.
[LITERATURE.md](LITERATURE.md) states all input and review boundaries.

## Exact mechanism and reproduction

Seven full homogeneous kernels cover rank1,2,5 of the ordered triple;
rank3,4 use a complete convex moment bound. Six simplex targets have
all14950 coefficients nonnegative each. A grouped target handles the
remaining simplex by61 scalar tables,6 strict domination tables and
an exact map to the credited all-balanced local region7823.

CPython3.11.2 standard library, native threads1, run sequentially:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -I -B verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -I -B -O verify.py
```

The aggregate verification path reports PASS,110504 explicit checks,
105641 target sign entries,7 kernels,61 scalar tables,6 domination tables,
46 full defining-matrix controls,36 exact polytope vertices, and
canonical regenerated-record SHA256

    322417850b2cd906df7a9a1bc97574353357667e64ff6efe6f505a475e07ddaf

The canonical mathematical record is unchanged by the bounded mode below.
`expected.json` is mandatory and compared in full. `--manifest PATH`
selects another fixture; `--write-manifest PATH` is explicit author
generation, not verification. `--progress` writes per-kernel timing to
stderr. `--test-manifest-rejections` additionally exercises five missing/
damaged fixtures through the same verification gate after regeneration.

## Bounded complete reproduction and measured evidence

The first aggregate normal replay reached its210s operational wall cap.
It was stopped without a mathematical conclusion or a resource increase.
Rational monomial evaluation now clears a common denominator once, with
cached integer powers. Exact values and the canonical mathematical record
are unchanged. All seven cases were freshly regenerated in both modes,
one child at a time with a60s cap. The longest was17.084s; total normal
98.542s, optimized98.512s; largest measured child RSS41776KiB.
The failed aggregate was not blindly rerun.

To reproduce as seven independently resumable jobs per mode, from this
directory in a POSIX shell:

```sh
set -e
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
mkdir -p case-replays/normal case-replays/optimized
for key in 5-0 2-0 2-1 2-2 1-0 1-1 1-2; do
  python3 -I -B verify.py --case "${key%-*}:${key#*-}" \
    --write-case "case-replays/normal/$key.json"
done
python3 -I -B verify.py --collect-cases case-replays/normal/*.json \
  --test-manifest-rejections
for key in 5-0 2-0 2-1 2-2 1-0 1-1 1-2; do
  python3 -I -B -O verify.py --case "${key%-*}:${key#*-}" \
    --write-case "case-replays/optimized/$key.json"
done
python3 -I -B -O verify.py --collect-cases case-replays/optimized/*.json \
  --test-manifest-rejections
```

Each selected run returns **PASS_CASE only**, rebuilds the full integer
kernel/signs/defining controls and the common36-vertex section record,
and compares the entire case/common record to the required fixture.
`--write-case` saves that freshly verified compact record; the generated
directory is ignored and is not publication source. Check each command's
exit status before continuing; pause on a timeout/failure. Timing caps
were imposed by the author's private runner, not these CLI options.

The collector checks seven unique case identifiers, matching source and
fixture hashes, entire common records and mathematical check counts, and
then the **entire assembled record** against expected.json. It returns
**PASS_RECORD_UNION**, not a new mathematical regeneration. Existing case
files are inputs; the collector alone does not authenticate how they
were obtained. Complete verification evidence consists of all seven
successful fresh case runs plus that union gate, separately in each mode.
Both complete case payloads agree across normal/optimized execution.

The observed union output includes57 gate checks,110502 mathematical
checks represented,105641 target sign entries,7 kernels,61 scalar tables,
6 domination tables,46 full defining controls,36 vertices and5 rejected
fixtures. The five fixtures are absent manifest, changed sign digest,
changed gap vertex, changed local mass cutoff and changed defining Psi;
all reject through the same full-record comparison under each mode.
The manifest is the complete84KiB author record, not a coefficient dump.
The default aggregate path remains available, but no fresh default whole
normal/O run is asserted by this bounded validation.

Exact Python, ordinary coverage/invariant-block/projection/Rolle/cluster
arguments and credited scalar/local/analytic inputs remain outside a
formal kernel. The46 author controls use full8x8 matrices and a separate
symmetric-commutant projection; they are not independent review. No
private module, large coefficient corpus, solver or floating proof input
is needed. Source publication alone would not establish acceptance.
