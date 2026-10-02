# Nine-regular C3 Book Ramsey exclusion

Actual author six-books-2, role researcher, 2026-10-02.
See [PROOF.md](PROOF.md) for the exact theorem and ordinary coverage argument.
It excludes only nine-regular22-point red graphs with automorphism type3^7 1;
irregular99/102-edge and unrestricted Ramsey frontiers remain open.

From the repository root, using Python3.11+ and g++12/C++17:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 round-two/six-books-2/c3_regular_nine_99/reproduce.py --work scratch/c3-nine-replay
python3 round-two/six-books-2/c3_regular_nine_99/reproduce.py --work scratch/c3-nine-optimized --optimized
python3 round-two/six-books-2/c3_regular_nine_99/validate.py --replay scratch/c3-nine-replay --work scratch/c3-nine-validation
```

Use EMPTY work directories outside this source directory. All programs set
threads1, run serially, and fail on incomplete phases or altered frozen
mathematics. Program guards25 seconds, child guards30 seconds, unchanged
1CPU2GiB campaign scope. No solver/package/network or external catalogue is
needed. Generated lists, executables, streams and logs stay in scratch.

The cold entry point regenerates495 local templates, the complete108-word
necessary projection in three declared relabeling groups, all37 incidence
templates, and15,768 five-regular outside words. Independent entire-set
comparisons precede583,416 full completion predicates with zero positives.
The native outside generator checks all2^22 words; Python instead expands
degree-matching mask weights. Complete sorted outside and per-choice outcome
streams agree, not just hashes or totals. A literal primary21 matrix is
checked first with its credited color normalization.

Validation uses the WHOLE native ASan/UBSan census, seven native damaged
inputs, six repaired primary-table damages, four typed-frozen/schema damages,
64 varied literal controls/all14,784 spines, and graph threshold controls.
Normal/O mathematical summaries agree. Metadata and measured costs are in
[evidence.json](evidence.json). The17 damage tests are recorded in the normal
validation run; no unperformed optimized-damage replay is claimed.

The compiler, interpreter, exact programs and unformalized coverage/code
bridges remain trust inputs. All algorithms have one author, and independent
review is pending. Frozen fixtures and checksums are not proofs by themselves.
The short new replay imports no previous finite host catalogue or global
degree-bound theorem. The earlier105-edge method and boundary-construction
frontier are credited with links in PROOF.md.
