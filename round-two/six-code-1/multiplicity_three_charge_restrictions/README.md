# A(18,6,5): the 16/19 hub pair occurs at least four times

**six-code-1, researcher**, 2026-10-01.

For a71-word code with replication profile `(16,19,20^16)`,
[PROOF.md](PROOF.md) proves that its two unsaturated points occur
together **at least four times**. The new argument completely excludes
multiplicity three; the published lower bound three8567 supplies the
other cases. The intermediate reduction at multiplicity three gives:

- All saturated internal deficits are zero or one.
- The nineteen-word hub has no low-low leave edge. Its shortened
  replication profile must be `(3,4^7,5^9)`.
- With `k=|(B union T) intersect C|`, `c=|T intersect C|` and `z=|Z|`,
  only `(6,1,0/1)`, `(5,2,0/1)` and `(6,2,0/1)` remain.
- The cohort deficient only to the sixteen-word hub has at most one
  charged vertex, and none if z=1.

The final charge argument closes all six intermediate inventories:
it forces a common-tail point with the isolated u hub to have a good
A neighbor sharing that same hub. The published shared-hub lemmas
forbid the resulting deficit-one edge. The definitions, quantified
hypotheses, capacity argument and imported premises are in the proof.
Multiplicities four and five and the other size71 profiles remain open.
Global campaign bounds remain69--71. Independent review of this
structural transfer is pending; its ordinary bridges are unformalized.

From this directory, Python3.11+ with only its standard library:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B verify.py
python3 -B -O verify.py
```

Both must report COMPLETE and manifest SHA256
`ab6e135f8ed18310448ac105132049a766825373c0cc758eca1d12fbd0ad1892`.
The run decodes all46 published marked nineteen-star representatives
and compares every actual anchor/candidate/block and every relevant
point-level readout between two decoders. Thirteen classes have the
required unique replication-three point. The244 small charge assignments
leave only three cases for the **written** shared-hub exclusion; the
checker explicitly records those rather than presenting arithmetic as
having proved that last step. Exact degree/capacity arithmetic then
leaves six intermediate parameter inventories. All6174 assignments
of their covered-low points to W centers are checked, leaving62 charge
patterns; every pattern has a fully forced common-T center and a good
A friend, for the final **written** isolation/shared-hub contradiction.
Sixteen malformed packing controls fail under both ordinary and optimized Python.

The unchanged known69-word fixture is checked for its hash, weight,
distinctness, every distance and all replications. Baseline reproduction
is validation, not the contribution. [acl69.txt](acl69.txt) comes from
the [Aw--Chee--Ling primary word list](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69),
described in [their2003 paper](https://ymchee66.github.io/home/PDF/6cwc.pdf),
Theorem1/AppendixA.

[NINETEEN_STARS.json](NINETEEN_STARS.json) is a byte-for-byte copy of
six-code-3's compact [census manifest](../../six-code-3/nineteen_star_classification/expected.json),
not a new enumeration. Source commit and file hashes are in
[DEPENDENCIES.json](DEPENDENCIES.json). Its complete census theorem8537,
the universal20 theorem8323, the two-hub incidence theorem8497 and the
three shared-hub lemmas8356/8397/8438 are imported mathematical premises.
The census's completeness and the ordinary counting/isolation bridges
are not checked by a hash or by decoding its representatives. The
prior transfer8567 is refined and its lower bound three is used for the
final at-least-four statement. Its zero-overlap capacity proof is
reproduced here. Same-author alternate implementations are not
independent peer review or proof-assistant formalization.

[expected.json](expected.json) records every relevant literal packing,
marked neighborhood, forced charge entry, assignment survivor,
parameter exclusion and final charge-pattern coverage. It is compact output, not a standalone exhaustive
code-search certificate. No heuristic, solver or floating-point result
is used. The readout needs no network or generated private corpus.
[VALIDATION.json](VALIDATION.json) records both completed serial runs;
each took below a second, with the measured child peak below21MiB and
all numerical-library threads one.

The concrete next frontier is hub multiplicity four in the16/19 profile,
using the nineteen-star marked point of replication four, common tails
and the charge budget. Historical priority of this
restricted transfer remains unassessed. The [maintained external table](https://aeb.win.tue.nl/codes/Andw.html)
still lists69--72; the campaign's reviewed upper71 is separately
[published prior art](../../../constant_weight_18_6_5_equality_structure/UPPER71.md).
