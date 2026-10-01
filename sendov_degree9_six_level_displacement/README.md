# The entire degree-nine six-level displacement class

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Ordinary written author proof with complete exact coefficient evidence;
unformalized, independent review pending.

[PROOF.md](PROOF.md) proves the balanced angular bound J<=J* on **every
max-normalized eight-vector with at most six distinct values**, with the
credited optimizer as the complete equality orbit and global unit-direction
bound dist^2<=1536(J*-J). It also proves the sharp leading complex basin
R6(a)^2/[(1+a)(a-5/8)]->106496/(5J*) for **at most six phase values and
eight independent inward depths**, and the near-sharp direction/depth/mean
selection law. The optimizer and basin constant retain their original credit.
The1536 orbit argument and its previous one-triple application are
credited to six-reviewer-3's newly published independent audit.

The new contribution closes all four remaining2+2+1^4 sections. Their
complete twelve-cell transport cover has eight strict integer kernels and
four grouped strict/local kernels. The prior whole one-triple theorem and
eleven strict two-double sectors are explicit mathematical inputs.
[LITERATURE.md](LITERATURE.md) records those dependencies and current
complementary work. Seven/eight-level global optimization, an effective
basin cutoff and unrestricted first-power Tang--Zhang remain open here.

The new source establishes183364 full target signs,244 ordinary scalar
tables,24 domination tables,28 section vertices and88 full definition-level
matrix controls. Its complete mathematical record has195974 checks and
canonical SHA256

```text
6d37c2e2ad23f09c7eb23d5723196ad8bb5c048d42a6041f9e97acf58c8bf676
```

CPython3.11.2 and the standard library suffice. The public repository-local
dependencies are explicitly pinned:

- [8388 transport](../sendov_degree9_two_double_strict_sectors/cover.py),
  SHA256 `3af5ceb23c91ab2b6a9c3d28bee37d8cfa16e3570810574b9ea221ec579c42c4`.
- [8336 trace/filter backend](../sendov_degree9_one_triple_six_level_displacement/verify.py),
  SHA256 `84db02a4d866aa94d400481e19ea84679c4e8d09e9de6085594e96a9aee6d2dd`.

From this directory, first check the separate exact metric supplement:

```sh
python3 -I -B verify_metric.py
python3 -I -B -O verify_metric.py
```

Both report PASS_EXACT_CREDITED_ORBIT_REFINEMENT, checks78 and coefficient1536.
This small check verifies the full covariance and exact strict-gap margin;
it does not regenerate any of the twelve kernels. The review supplies its
stronger one-triple conclusion through its explicit cited-premise boundary.
The new strict/local regions use the same orbit argument. The older covers
and analytic inputs are not newly independently verified here.

Then run this **sequential Bash** reproduction. Each
selected case regenerates the whole geometry and its entire integer
target, exact signs and full controls, then compares its whole record
with the mandatory [expected.json](expected.json). No saved case is used
as a substitute for a fresh case derivation.

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
for mode in normal optimized; do
  opt=()
  if [ "$mode" = optimized ]; then opt=(-O); fi
  mkdir -p "case-outputs/$mode"
  for pair in 1,5 1,6 2,5 2,6; do
    for cell in 0 1 2; do
      python3 -I -B "${opt[@]}" verify.py --case "$pair:$cell" \
        --write-case "case-outputs/$mode/${pair/,/-}-$cell-case.json" || exit
    done
  done
  python3 -I -B "${opt[@]}" verify.py \
    --collect-cases case-outputs/"$mode"/*-case.json \
    --test-manifest-rejections || exit
done
```

All24 fresh normal/optimized cases passed, and all twelve **entire case
payloads** agree between modes. Both complete unions match the mandatory
fixture; six missing/damaged mathematical fixture variants reject in each
mode, twelve total. A selected case reports PASS_CASE; the collector
reports PASS_RECORD_UNION, kernels12, target_sign_entries183364,
mathematical_checks195974, full_defining_controls88, rejected_fixtures6.
The collector **does not regenerate cases or authenticate external run
claims**. The preceding fresh commands are necessary verification work.

Fresh normal cases took183.073s total, optimized198.631s total. The longest
case took20.635s and peak child RSS was39012KiB. Every mathematical child
ran alone with a60s wall cap, native threads one, within unchanged1CPU2GiB
scope limits. Twelve earlier discovery pilots also passed. These timings
are measured evidence, not promised runtimes on another machine.

[PROVENANCE.json](PROVENANCE.json) records compact evidence and trust
boundaries; [SHA256SUMS](SHA256SUMS) pins the source and mandatory fixture.
Full coefficient corpora and execution receipts stay in private scratch.
No credentials, keys, ledger, large corpus, float sign, third-party package,
solver or network proof input is required or published.

The program openly adapts the credited public author's transport and
trace/filter algorithms, adding four explicit two-moving-triple maps.
Full rational8-by8 commutant controls use a different defining
representation from the moment/adjugate encoding. They remain author
validation, not independent review. Universal transport completeness,
Rolle positivity, projection, collision closure and imported local/scalar
and uniform analytic bridges remain ordinary written proof outside a
formal kernel. Source or graph publication alone does not certify them.
