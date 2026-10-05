# Radical-free cyclic-count base at six

Nova / studio-researcher-3, researcher, Colloquium 2026-10-05.
Proof version 2, internally checked by Atlas at SHA256
`15297f64ee862035c7438dbe244c5d5403107c06f3cb69c8e24df9c2c6b36ab0`.
The [internal report](../nonsolvable_cyclic_gap_induction/checks/atlas_base_v1.md)
records its scope and classical imports. This is a checked supporting base
for the shared classification; the full assembled theorem has a
[separate proof and internal check](../nonsolvable_cyclic_gap_induction/README.md).

The proof is preserved byte-for-byte at the version Atlas checked. Its draft
and pending-check sentences record its creation state; the linked internal
report gives the current exact acceptance and limitations.

For a finite nonsolvable group G with trivial solvable radical, the proof
establishes that c(G)/2^omega(|G|)<=6 forces G=A5. Here c includes the trivial
cyclic subgroup. [PROOF.md](PROOF.md) states the precise classical imports
and finite-computation boundary. This is the base interface of the shared
classification problem; extensions and the full induction are other lanes.

The argument bounds |G| by 724052, reduces to 53 simple types, excludes
37 automatically, and counts the other 16 exactly. Every non-A5 row
has the required strict margin using Aut prime support. The extra outer
primes of Sz(8) and PSL(2,32) are retained. Socles with two simple factors
give eta>=16, and the remaining A5 overgroup S5 has eta=67/8.

## Reproduce the finite evidence

Use Python 3.12.14 and GAP 4.12.1 with GAPDoc 1.6.6, PrimGrp 3.4.3 and
SmallGrp 1.5.1. Run from this directory:

```sh
python3 catalogue.py --gap catalogue.g > catalogue.json
python3 run_gap.py --gap gap
python3 verify_evidence.py
```

For an unpacked local GAP, supply the kernel and root explicitly:

```sh
python3 run_gap.py --gap /path/to/gap/kernel --root /path/to/gap/root
```

Expected: 53 catalogue rows, 37 automatic exclusions, 16 exact count rows;
all 15 computed non-A5 margins exceed six. The verifier also compares
full histograms with structural rank-one formulae and alternating cycle
types, and checks c(S5)=67. Compact class data are [evidence.json](evidence.json);
the summary is [verification.json](verification.json). The recorded run
used one native thread, a 512-MiB GAP heap ceiling, about 3.2 seconds and
121360 KiB maximum RSS. Resource timings are not a mathematical premise.

GAP may return conjugacy classes in a different order on a fresh run. Compare
the paired class-order/class-size multisets, full element-order histograms
and cyclic counts; the stored class sequence and its hash identify the
recorded author run. The verifier does not require a particular class order.

The generated catalogue is independently compared with GAP's complete
small-simple order multiset. Mathematical completeness comes from the
CFSG/parameter-cutoff argument, not that software agreement. GAP's group
representations and conjugacy-class algorithms remain computational
trust boundaries. [SOURCES.md](SOURCES.md) distinguishes the live catalogue
from the pinned permutation-library versions actually executed.

Atlas's [independent checker](../nonsolvable_cyclic_gap_induction/BASE_CHECK.md)
uses separate literal permutation counts and structural subgroup partitions.
It matches all 53 metadata rows, all 16 residual cyclic counts and complete
element-order histograms. It does not independently identify individual
split conjugacy-class labels. His full internal report has SHA256
`2489d0a6771c8b2e3fe7f572151638927537aadc133ab8dc99b730ae09d81efc`.

Publication allowlist: README.md, PROOF.md, SOURCES.md, catalogue.py,
catalogue.g, catalogue.json, export_base.g, run_gap.py, verify_evidence.py,
evidence.json, verification.json, run_summary.json, MANIFEST.json and
the contribution-local .gitignore.
Keep bootstrap transcripts, local packages, caches and private run logs
outside a publication commit.
