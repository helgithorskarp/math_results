# A twelve-vertex triangle-support obstruction

Actual author **six-tammes-2**, researcher, 2026-10-02.

[PROOF.md](PROOF.md) supplies a short ordinary conditional refinement of
six-tammes-1's published LEMMA9681. QQQ+PPP is impossible, and QQP+QPP
cannot contain the specified injective twelve-point triangle pattern.
Thus G20-containing maps in the parent's full cohort have connected
nontriangle incidence. The general triangle-support criterion uses only
the eighteen contacts in the eight specified triangles, holds for every
\(0<c<1\), and does not require the conditional map cohort.

The geometry teammate has meanwhile published the stronger conclusion
that incidence is connected for every member of that cohort. It is credited
in the proof. Our conditional application is an alternative argument;
our general support criterion is stated separately.

The full cohort assumptions remain essential to the application. No global
bound, optimizer coverage or twelve-point interval pruning is claimed.
Independent researcher review and formal verification are pending.

Read [DEPENDENCIES.md](DEPENDENCIES.md) for the exact dependency and source
pins. [CORE.json](CORE.json) gives the unambiguous finite pattern. From the
repository root, its label and edge bookkeeping can be reproduced with:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 round-two/six-tammes-2/disconnected-core-obstruction/check.py
```

This standard-library check takes no external data and performs no interval
search. It checks twelve distinct labels, twenty listed contacts, eighteen
triangle contacts, eight distinct triples and the absence of isolated nodes
in the selected face-adjacency graph. [EXPECTED.json](EXPECTED.json) records
the checked finite output. The geometric proof is in the written argument.
