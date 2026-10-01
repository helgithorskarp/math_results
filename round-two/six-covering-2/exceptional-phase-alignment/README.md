# Exceptional parity alignment at period 10080

Author **six-covering-2**, role **researcher**, 2026-10-01.

For a distinct covering of minimum modulus exactly8 whose moduli divide10080,
the two complete new trees exclude normalized roots01d4 and01d6. Combined with
the credited old parity/modulus12 lemmas, they imply: if no PRESENT10 class
opposes the eight-class parity and actual12 has that parity, then14 is present
with opposite parity,9 is present with a phase different from12 modulo3,
and a12=a8+2 modulo4. Such an exception exists if and only if the root01d10
can be completed. **That root remains open.**

In particular, a12=a8 modulo4 forces a PRESENT10 class of opposite parity.
The combined exact phase frontier has14 unexcluded affine representatives;
the global L_min(8) candidates stay10080,15120,20160, with20160 witnessed.
No minimum-at-least-eight or universal period exclusion follows.

See [proof.md](proof.md) for the actual-class/adjoined-class argument,
certificate completeness and trust boundaries. This is an author-checked
exact computer-assisted conditional lemma; the written proof is unformalized
and independent review is pending.

## Dependencies

Use a repository checkout containing these sibling source directories:

* The parent [integer certificate engine](../README.md), source
  `2d66a2b1ed2d5549e1316117d1def22a474bb179`, graph8557
  `bafkreih3y7ovbsfsqmxizyrcdho5ynff3hqzstw5kpocuoyvezqku3neaq`.
* [Five-class affine reduction and old exclusion](../five-class-exclusion/README.md),
  source `433efdee31eb6f95e5ab0a753b78bb5601245714`, graph8606
  `bafkreibgg6wg7b3wrd54kqt6e2q3ktzbmhcq2mlhc5rjwmgtqw73g4xxku`.
* [Parity exclusion](../parity-class-exclusion/README.md), source
  `23565f309733c60a6ad4345bcd8189794fca7c93`, graph8680
  `bafkreib6exe3fkpmlxqdjznoozbtwkywcld4vodk5gqko4nmpape4cgbga`.
* [Modulus12 necessity and phase disjunction](../twelve-class-exclusion/README.md),
  source `b1d33a7c2b7ab8091d58508033107e0f88e61c80`, graph8728
  `bafkreibbmkj4sx4jy5gfc2nnsa4bsapfezivsa6l6ty4pokny6wsr55mci`.

The wrapper directly checks only the two new roots. The intrinsic lemma imports
8680/8728; the combined fourteen-form frontier also imports8606. It does not
claim independent replay of those old certificates. `manifest.json` pins all
nine imported code files. Weighted counting, fractional resource incidence
and affine normalization are credited methods. NumPy/SciPy only propose
integer certificates; their numeric solver decisions are not proof premises.

## Reproduction

Literal checking and complete phase controls need Python3.10+ standard library.
Discovery used Python3.12.14, NumPy2.4.6, SciPy1.17.1; install the pinned
parent [requirements-discovery.txt](../requirements-discovery.txt) only for
regeneration. Use one numerical thread and one intensive job at a time.
From the repository root:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-covering-2/exceptional-phase-alignment/frontier_alignment.py
python3 -O -B round-two/six-covering-2/exceptional-phase-alignment/frontier_alignment.py
```

Regenerate both trees sequentially in a private directory using a Python
environment with the discovery dependencies:

```bash
python3 -B round-two/six-covering-2/exceptional-phase-alignment/reproduce.py --generate --generated /tmp/covering-alignment-trees --require-manifest
```

This wrapper gives each root at most eight bounded180-second/700-new-node
resume batches. It stops explicitly INCOMPLETE if this voluntary allowance is
exhausted. The unchanged generator's own per-LP limits remain in force.
A timeout, UNKNOWN or incomplete enumeration proves no exclusion. Exact
checking may pass with a different valid proof tree; `--require-manifest`
additionally requires the author's exact replay hashes/counts.

After regeneration, replay independently of the numeric packages:

```bash
python3 -B round-two/six-covering-2/exceptional-phase-alignment/reproduce.py --generated /tmp/covering-alignment-trees --require-manifest
```

Expected compact output includes `author_manifest_match: true`,2264 nodes,
362 expansions,8414 actual phases,7808 transports,1111001 selected pair-phase
entries,7560 newly forbidden tuples and14 remaining forms. The two trees
have1902 strict leaves. Author combined replay:69.333s/64372KiB maximum RSS;
normal/optimized phase enumeration agrees and four quantifier guards reject
wrong-root/period/minimum/incomplete inputs. Per-root event/transport/pair hashes are recorded in
the manifest. The parent literal checker reconstructs every progression,
weight and selected union; it rejects incomplete and malformed proof evidence.

Large trees, environments and scratch experiments are intentionally omitted.
Only reproducible source, proof and a compact manifest are published; no private
input is required. `SHA256SUMS` covers this directory's compact source files.

Primary literature refreshed live2026-10-01: [Zhang–Zhang](https://arxiv.org/html/2607.19029)
claims the minimum-seven optimum10080; [Harrington–Klein–Lowrance–Trifonov](https://arxiv.org/html/2605.18644)
studies the restricted2,3,5 support and constructs minimum-eight LCM172800.
Those numerical exclusions are not premises of the present two roots. The
bounded literature/commit/graph refresh found no earlier matching two-case
exclusion or intrinsic condition; exhaustive historical priority is unclaimed.
