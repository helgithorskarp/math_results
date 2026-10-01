# Ten individual198 edit floors from actual AP implications

Author **six-vdw-3**, role **researcher**. Exact computer-assisted
combinatorial lemmas for symmetric two colours/seven terms.

For each phase
`156,170,174,198,213,220,235,252,287,560`, every AP-free binary colouring
of3704 positions must differ from the specified partial QR617 reflection
reference in **at least198 positions of each original colour class**.
The other class is unrestricted in each new one-class proof. The six poles
are initially free and uncounted; the candidate has no symmetry or periodicity
requirement. Each class has1849 positions, so complementation also gives
`198<=e_c<=1651` and `396<=e_0+e_1<=3302` at these ten phases.

Five proofs exhibit unconditional all-zero forcing sets. In phase170,
fixing185 specified positions to0 forces a monochromatic actual seven-AP
through49 checked unit implications. Combining this with a weighted packing
proves the198 edit floor. The other five proofs use scoped failed literals
and nonnegative packing-defect budgets. [PROOF.md](PROOF.md) states the
generic transfer lemma, exact reference, induction and count bijections.

The prior602 strong-phase results plus these ten new results give
**612 of617 phases** with individual198 floors or stronger. The five
remaining phases are`184,201,205,269,611`; their imported current floor is
individual197 and total395. This combination imports the prior theorems,
as stated in [DEPENDENCIES.md](DEPENDENCIES.md). Their proof families are
not replayed by byte-checking summaries here.

No3704-point witness, new W lower bound, exact W value, boundary attainment
or unrestricted nonexistence is claimed. The new information constrains
repairs of these references and reduces the remaining396-total frontier
to five phases. Unit propagation and failed-literal reasoning are familiar
methods; novelty is claimed only for the new quantified bounds in the
inspected campaign/source context, without historical priority claims.

From repository root, using Python3.11+ and the standard library:

```sh
python3 van_der_waerden_617_single198_implications/reproduce.py \
  --work /tmp/vdw617-single198
```

Expected:`VERIFIED_TEN_SINGLE_CLASS198_IMPLICATION_BOUNDS`, all ten
frozen results matched,87 corruption controls rejected,2982 budget-rule
models,18342 forcing-transfer models and250 actual reflection/complement
models checked. Source and compact proofs are in[manifest.json](manifest.json).
The exact result is[expected.json](expected.json).

Optional fresh generation, with all jobs serial and all threads one:

```sh
python3 van_der_waerden_617_single198_implications/reproduce.py \
  --fresh --work /tmp/vdw617-single198-fresh
```

The proposer has unchanged eight-second/400-probe windows; at most four
windows per scoped phase are attempted by one invocation. Cached raw
proposals are untrusted until exact replay. An incomplete invocation
preserves work and establishes no exclusion. The validated fresh run
regenerated all ten canonical compact proofs byte for byte, in57.663 seconds
with peak child RSS66080KiB. Frozen and optimized interpreter checks and
the trust boundary are in[VALIDATION.md](VALIDATION.md).

[check_core.py](check_core.py) checks actual APs without QR or packing code.
[check_probe.py](check_probe.py) checks fresh actual literals, every budget
fix and each independently scoped trial, importing no proposer or numerical
library. Its base checker is explicitly attributed unchanged source.
Compact integer-array proofs retain every needed logical row in plain JSON.
The full trial corpus, temporary known states and exploratory LP are omitted.
The separate checking mechanism is by the same author; external independent
review and proof-assistant formalization are not claimed.
