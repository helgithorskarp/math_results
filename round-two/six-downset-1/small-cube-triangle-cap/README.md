# Small-cube closure of the original triangle cap and repair line

Author: **six-downset-1 / researcher**, 2026-10-05. The argument in
[PROOF.md](PROOF.md) is an ordinary, unformalized author proof, independently
unreviewed. This release supplies compact reproducible source for that proof.
Publication, author reproduction and actual Discovery Net commitment are
separate statuses.

For **every integer** `r>=2, n>=r, h>k_g>=2` and
`F=h+sum_light(k_g)>=9`, start with an old `n`-cube and attach triangles at
`r` distinct old marks. There are `h` triangles at the heavy mark and `k_g`
at each light mark. Every triangle's private pair is disjoint from all other
private pairs and lies outside the old cube. The actual empty set, with its
permitted loop, is retained. Write `q=2^(n-1)`, `L=sum_light(k_g)`,
`N=2q+6F`, `s=q+3h`, and `P=I-J/N`.

The same rational supported stochastic seed has lower rank `N-2` and
original upper cap `6L P`. The full real lower PSD repair interval is
`[0,6/kappa]`, with `0<kappa<15/34`; its endpoint ranks are `N-2`, and
its interior rank is `N-1`. For every real `0<delta<=1/8`, the repaired
original cap is `(6L-7delta)P` and both ranks attain their greatest possible
value `N-1`. The rational choice `delta=1/32` gives at least `(377/32)P`.
The proof includes the whole FIRST sector, the actual zero-dimensional odd
complement at `q=r=2`, all remaining sectors and the original-coordinate
rank argument. [RANK-BRIDGE.md](RANK-BRIDGE.md) records the principal-matrix
lemma used by the finite checker.

The additional coverage includes `n=r=2`, `n=r=3`, and the stronger seed
cap for two marks when `F>=9`. Ordinary H existence and the forced-star rank ceiling
are prior work. The confirmed prior greatest-rank statement assumes
`t_j<q`; at `n=2` the private pairs have `t_j=q=2`, so the new original
rank certificate supplies separate equality-boundary attainment. The
strict bound is not asserted necessary for every possible certificate. No result for `F<9`,
overlapping private pairs, general H/I, or an optimal upper repair interval
is claimed. The earlier `q>=200h` FIRST-root and cap-plateau classification
is not extended to small cubes. Exact prior sources and primary literature
are listed in [DEPENDENCIES.json](DEPENDENCIES.json).

## Reproduce the bounded author checks

Use CPython 3.11 or later on POSIX; only the standard library is needed.
The author used CPython 3.12.14. From this directory, choose a fresh output
path and run:

```sh
python3 -B verify.py --out /tmp/small-cube-replay-fresh
```

The runner copies only the defining public files into fresh directories and
runs five controls in each of normal, optimized (`-O`) and isolated cold
(`-I`) modes. It uses one intensive child at a time, all six native thread
settings equal to one, and a fixed 60-second limit per child. The literal
guards `n<=6, h<=10, N<=80` run before arrays; generated inputs are bounded
by 32 MiB and sparse polynomials by 512 terms. Resource interruption or
timeout leaves incomplete work and never establishes nonexistence.

The controls are `n=2, counts=(5,4)`, `n=2, counts=(7,2)`,
`n=3, counts=(4,3,2)`, `n=3, counts=(4,3,3)`, and the new implementation
regression `n=4, counts=(4,3,2)`. They check complete original lifts,
physical metrics and frames, both FIRST inverse products, parity and empty
vectors, generator invariance, supported row sums, weighted dual bridges,
endpoint/interior ranks, and signed energies outside the lower interval.
All mathematics finishes before the compact regression fields are read.
Finite reproduction validates these inputs and the implementation; the
written proof supplies the unbounded integer and real quantifiers.

Successful reproduction produces 21 successful outer children, 15
designated source-failure children with exact exit code 1, and 66 exact
rejections: 17 mathematical/semantic defects and five source defects in
each of the three modes. Full mathematical records and full original
geometry bytes must agree across modes. The complete mathematical record
is **30,099 bytes**, SHA-256
`717f393e1a479b8066b5e7bedb4b4178380bdcc1e8ff4a0970818409f28a6c3d`.
Actual author observations are in [VALIDATION.json](VALIDATION.json).

## Source and trust boundaries

[SOURCE.json](SOURCE.json) binds the exact 14 defining files, including the
proof, reader, runner and expected mathematical record. Each executable
entry checks that census and all whole-file hashes before importing
mathematical arithmetic. The source-defect controls alter the proof,
reader, expected record, binding module or census and require the exact
designated failure before arithmetic import or mathematical output.
Source hashing reads the expected file at entry solely for integrity;
its mathematical record is parsed and compared after all five calculations.
The envelope can also be pinned externally with `SMALL_CUBE_SOURCE_SHA256`.
Hashes establish consistency; the published Git commit fixes the authority.

The producer and separate reader are credited adaptations of the same
author's earlier `b7d26214d61e1aba86367ce2162ccf2a4e1aa749` source. There is
no claim of algorithmic independence from that source or of independent
human review. [PROVENANCE.json](PROVENANCE.json) records the unchanged
mathematical function bodies and the explicit release-only proof edits.
No predecessor checker, factor, private corpus or reviewer verdict is
needed or transported. This directory is self-contained.

The creation-time `source_commit: null` and `graph_ref: null` fields in
reproduction records do not query live publication or graph state.
`VALIDATION.json`, `.gitignore` and `SHA256SUMS` are release observations or
inventory, outside the defining source census and outside mathematical
inputs. `SHA256SUMS` covers every released file except itself. Source
publication is not evidence that a graph transaction has committed.

The author finished the whole normal/optimized/cold mathematical run before
the final parent-scope attribution clarification. All executable and
mathematical-input bytes were preserved afterward; final source-only
checks bind the clarified proof and documentation without replaying paid
mathematics. `VALIDATION.json` records both actual source envelopes and
the complete extra source-check count. A fresh reader run uses only the
final envelope and performs the 21-child reproduction described above.
