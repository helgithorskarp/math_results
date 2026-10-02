# Exact contact domains and a forced neighbor for regular polyhex strips

six-heesch-2, researcher. Author-checked computer-assisted lemmas with an
ordinary unformalized reduction. Independent review is pending; no priority
or Heesch record is claimed.

For every integer k>=6, the literal area-(4k+3) strip T_k has exactly 96k+184
registered disjoint contacts with its root. A complete affine rectangle
description reduces the varying families to integer intervals. Its notch
has exactly nine affine suppliers. A side-contact restriction and a six-cell
packing obstruction then force one half-turn neighbor in a particular E2
pair cover. See [the complete proof](proof.md).

These are registered local contact statements. They do not establish the
full E2 inclusion needed by the earlier conditional upper-three lemma, an
unconditional all-k Heesch upper, or the finite-five polyhex target.

From the repository root, run:

```sh
python3 round-two/six-heesch-2/strip-contact-domains/verify.py
```

Python3.10+ on Unix, standard library only; tested Python3.11.2 on Linux.
The runner executes serial normal and optimized generation and search-free
checking. It pins the three adjacent published geometry files listed in
[expected.json](expected.json): the two modules in
[parametric-strip-obstruction](../parametric-strip-obstruction) and
[strip-t5/exact.py](../strip-t5/exact.py). No private closure census, solver,
virtual environment, signed key or ledger is needed.

The compact expected evidence is96k+184 raw contacts, nine notch suppliers,
two surviving side shifts, and a 16-node rejection over46 suppliers for six
demanded cells. The reader performs separate endpoint sweeps and critical-cut
reconstruction, direct unit-edge inventories and materialized geometry audits,
and rejects six damaged inputs. Shared affine/height kernels and the ordinary
all-k reduction remain trust boundaries; same-author checks are not peer review.

Each child has 43/45/47-second work/signal/external guards and the finite search
has a 100000-node cap. Generated certificates and reports stay in the ignored
strip-contact-domain directory. A guard, timeout or incomplete computation
proves no negative statement. An optional DISCOVERY_RESEARCH_TEAM_ROOT environment
variable enables campaign pause checks without making the source host-specific.
