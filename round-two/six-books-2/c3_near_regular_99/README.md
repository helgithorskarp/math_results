# Near-regular99-edge C3 obstruction

Actual author **six-books-2**, role **researcher**. The [proof](PROOF.md)
excludes every ordinary red-B4/blue-B7-free22-vertex graph with red degree
multiset **8^3,9^16,10^3** and an automorphism of cycle type **3^7 1**.
It also proves a nonsymmetric local lemma: at most99 red edges, a degree-nine
vertex cannot have red-neighbor degree multiset8^3,9^6, whatever the outside
degrees. Other degree profiles, full99/C3 and R(B4,B7) are not resolved.

Use CPython3.11+ on Linux, its standard library, and g++ with C++17. Runs
recorded in [evidence.json](evidence.json) used Python3.11.2/g++12.2.0.
No solver, numerical library, private census, ledger or network service is
needed. Source publication is independent of any later graph transport.

From the repository root run these commands **sequentially**, with fresh
empty work directories outside the public source:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1
python3 round-two/six-books-2/c3_near_regular_99/reproduce.py --work scratch/c3-near-cold
python3 round-two/six-books-2/c3_near_regular_99/reproduce.py --work scratch/c3-near-optimized --optimized
python3 round-two/six-books-2/c3_near_regular_99/validate.py --replay scratch/c3-near-cold --work scratch/c3-near-validation
```

The main replay returns `COMPLETE_COLD_NEAR_REGULAR_C3_REPLAY`, with828,360
completion choices and0 valid. AA uses30 incidence frames and15,768 K
words; BB uses28 frames and12,690 K words. Their full outcome streams and
the entire typed frozen mathematical record must match [EXPECTED.json](EXPECTED.json),
SHA256 `6c73fb19876fa10b4a6354346abe8ee31f6f13883b736392bb3debef96738b47`.
The five-case ordinary lemma is verified by a separate exact load DP.
Normal and optimized runs independently regenerate the data; neither uses
the other's output. Validation repeats both entire native censuses with
ASan/UBSan and rejects incomplete/forged marked frames and typed records.

The wrapper keeps one intensive child at a time, numerical threads1,
program guards25s and child guards30s. No limit is raised automatically.
A failure, timeout, killed process or incomplete phase supplies no
nonexistence conclusion. Files already generated in scratch remain there
for diagnosis; choose another empty directory after fixing a software issue.
The actual process scope in this campaign remains1CPU/2GiB.

The public sources are generators/checkers plus a compact frozen fixture,
not an opaque large proof corpus. Full local records, native candidates,
outcome streams, compiler products and phase logs are reproducibly generated
in the work directory. Different same-author algorithms are not independent
peer review. Ordinary mathematical/completeness/relabeling/code bridges are
written in the proof and remain unformalized. Independent review is pending.

Primary literature and the21-point baseline are credited in the proof.
The earlier public nine-regular C3 implementation is method credit, not a
mathematical premise; the new degree marks, incidences and K caps have been
re-derived. See the proof's explicit placement and screen distinctions.
