# Independent ordinary cross-shell remaining-row audit

Actual agent six-reviewer-2, independent mathematical reviewer, pass35.
[Review and scope](REVIEW.md), [complete independent proof](PROOF.md),
[reviewer checker](audit.py), [complete compact record](PRIMARY.json),
[pre-native seal](PRIMARY_SEAL.json), [primary runs](PRIMARY_VALIDATION.json),
[late comparator](late_compare.py), [native file pins](NATIVE_INPUTS.json),
[late record](LATE.json), [late/native runs](LATE_VALIDATION.json).

The confirming verdict concerns LEMMA9847's exact E<=108 shell, using
ordinary9795 and9685 with matched hypotheses. The proved exact-rank
interface refinement concerns remaining-row forcing only. Neither statement
resolves the unrestricted Book Ramsey problem or imposes a host automorphism.

CPython3.11.2 standard library. Set each of OMP_NUM_THREADS,
OPENBLAS_NUM_THREADS, MKL_NUM_THREADS, NUMEXPR_NUM_THREADS,
VECLIB_MAXIMUM_THREADS, BLIS_NUM_THREADS to1. Run serially:

```sh
python3 audit.py --output scratch/normal.json --check PRIMARY.json
python3 -O audit.py --output scratch/optimized.json --check PRIMARY.json
```

Create scratch first. The whole mathematical record, excluding its LF,
has55,571 bytes and SHA256
5f41f49d22f6551315f3a68b3493f281665ed180643bc6d44faebcc3b712f92b.
These primary checks need no network, producer executable or external data.
The complete known graphs and physical pages are constructed from the
literal written hypotheses. Explicit require checks remain active in -O.

Optional late native reproduction, with the same environment and serially:

```sh
python3 download_native.py --output scratch/native
python3 late_compare.py --native scratch/native --output scratch/late-normal.json --check LATE.json
python3 -O late_compare.py --native scratch/native --output scratch/late-optimized.json --check LATE.json
python3 scratch/native/reproduce.py --output scratch/native-normal.json --check scratch/native/RESULTS.json
python3 -O scratch/native/reproduce.py --output scratch/native-optimized.json --check scratch/native/RESULTS.json
```

The downloader fetches only ten source files at the exact public native
commit and checks all whole byte pins before execution. It refuses differing
existing local inputs. Native code corroborates the target author; it is
explicitly not a premise of the sealed independent proof. Whole core/domain
comparisons are in LATE.json. No24MB generated image or private campaign
ledger is required or included; that image is checked entrywise and streamed
into its hash. All four unchanged primary seals are verified by the late
comparator. Source/checks contain no Python assert statements.

The mathematical code uses thirty-second guards and the reported runs use
sixty-second child timeouts, serial1CPU/2GiB/native threads1. An incomplete
run, exception, resource kill or timeout supplies no mathematical exclusion.
The ordinary proof is unformalized. New graph relations belong to the review
and are attached atomically after source and direct-reader verification.
