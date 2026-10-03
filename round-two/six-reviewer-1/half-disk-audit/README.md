# Independent marked-half-disk audit

Actual **six-reviewer-1**, independent mathematical reviewer.

[REVIEW.md](REVIEW.md) confirms the complete ordinary, unformalized
degree-nine half-disk theorem of LEMMA10092 and derives the explicit uniform
refinement
\[
\sum_{j=1}^8|a-\zeta_j|^{-1}>8001/1000\qquad(|a|\le1/2).
\]
All nine original zeros lie in the closed unit disk; all eight critical
multiplicities are counted, with zero denominators contributing infinity.
There is no second-moment, reality, conjugacy or separation assumption.
The global first-power conjecture remains open. [PROOF.md](PROOF.md) gives
the full continuous argument and the enlarged standalone channel theorem.

Written target proof/data exposed, **not blind**. Fresh implementation and
proof sealed before native code/fixture access. Standard-library CPython3.10+
(observed3.12.14); no third-party libraries, solver, external certificate,
proof assistant or native author implementation is required:

```sh
python3 -B check.py
python3 -B -O check.py
python3 -B literal.py
python3 -B -O literal.py
python3 -B reproduce.py
```

`check.py` emits the complete53400-byte rational record, SHA256
`ea0235c15f8728508488dae9be0a93798f63c467f2be65ca767613e228b498db`.
`literal.py` emits the complete25632-byte identity/control record, SHA256
`ae84b0fbb5cbf5d4dc540ae62137251cffb30f8402140917c20a7fcfb8936529`.
Every complete normal/optimized/original/cold stream is compared byte for
byte. Bulky run outputs stay outside the repository; deterministic source
regenerates them without importing any target fixture.

`reproduce.py` sets six numeric thread variables to1, runs one mathematical
child at a time under fixed45s guards, verifies every primary seal, and
rejects26 consequential mathematical damages and12 complete-result damages.
Its timings and temporary path vary; its mathematical streams do not.
The existing1CPU/2GiB scope is unchanged.

Optional late corroboration takes the author's complete freshly emitted
JSON record as **data only**, after its native verification:

```sh
python3 -B compare_native.py /path/to/native-record.json
```

The native record is identified in [PROVENANCE.json](PROVENANCE.json).
Neither this optional record nor native code is required by the independent
proof/checker. Literal controls validate exact identities and include
collisions; they are not asserted to be disk-rooted originals.

[LITERATURE.md](LITERATURE.md), [VALIDATION.json](VALIDATION.json),
[PRIMARY_SEAL.json](PRIMARY_SEAL.json) and [PROVENANCE.json](PROVENANCE.json)
state authorship, mathematical credit, exact scope and trust boundaries.
