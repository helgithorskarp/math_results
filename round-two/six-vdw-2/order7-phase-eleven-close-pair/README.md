# H7 exact-eleven close-pair certificate

six-vdw-2, researcher. See [PROOF.md](PROOF.md) for the quantified
restricted-family lemma and ordinary completeness argument. The four
checked cases require a selected pair within cyclic distance two at
phase weights11/33. Neither endpoint weight is excluded.

From the repository root, in a Python environment with PySAT1.8.dev24
and CaDiCaL195, use the pinned drat-trim source identified in
[SOURCE_PINS.json](SOURCE_PINS.json). Build that converter outside the
repository contribution directory. It must have drat-trim.c next to
the executable so the driver can check its source hash.

```sh
python3 round-two/six-vdw-2/order7-phase-eleven-close-pair/reproduce.py \
  --work /tmp/eleven-close-pair-fresh --converter /path/to/drat-trim
```

Use a nonexistent work directory. The run regenerates both branches,
requires whole normal/O definition and damage records to agree with
[VERIFICATION.json](VERIFICATION.json), then proposes and strictly checks
each case serially at the unchanged caps. [EXPECTED.csv](EXPECTED.csv)
contains canonical CNF/LRAT hashes and counts. A valid regenerated proof
may have different regression bytes with a different native version;
the driver records that difference separately from its strict verdict.

`--certificate-cache DIR` accepts untrusted previously generated LRATs
with the fixture filenames/hashes. It still regenerates and independently
audits every complete CNF and checks every LRAT in both modes. `--resume`
accepts only an already complete positive four-case replay; failed or
incomplete identical native inputs cannot be resumed.

All numerical threads are one and cases/stages are serial. Respect the
host's1CPU/2GiB research scope. Every incomplete stage gives no exclusion;
stop and retain the generated evidence without retrying the same hash.
No generated models, proof corpus, private protocol wire, ledger,
credentials or operations/account state is included in this source.
The generator and literal-field/checker algorithms are distinct code
owned by one researcher, not independent-person review or formal proof.
