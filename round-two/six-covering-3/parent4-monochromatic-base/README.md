# Parent4 monochromatic BASE obstruction

six-covering-3, researcher, 2026-10-02. Under the literal prefix
`8:0, 9:0, 10:1, 14:1, 12:10`, no original36-BASE inventory leaves all its
holes in parent4 and mod3 color1 or2. With the credited published13-case
reduction and two-row obstruction, a completed inventory satisfying A4 with
every other parent BASE-clear has at most87 parent4 holes modulo2520.

Read [proof.md](proof.md) for the complete required-set reductions and scope.
There is no global minimum-eight bound improvement or full covering witness.
The ordinary proof is unformalized; external independent review is not claimed.

Python3.11.2, standard library only. From this directory:

```bash
python3 -B compute.py --joint
python3 -B audit.py expected.json --controls
python3 -O -B audit.py expected.json --controls
```

Run these sequentially. Each checked child had a20-second external guard,
one CPU and threads1. They need neither a solver nor generated input data.
`expected.json` contains the complete compact mathematical records, capacities,
histograms, extrema, witnesses, enumeration counts and full-run digests.
The producer prints that record. The independently structured auditor recomputes
all core/joint gains and864 conditioned marginal rows, compares every record,
and rejects20 mutations to the actual certificate when `--controls` is used.

Expected color1:1293 required points,240 retained core vectors,2,419,200 joint
vectors,864 marginal vectors, maximum conditioned total1190. The deficit103
is conditional on the two necessary filters. Expected color2:1293 required
points versus1283 individual capacity, giving an unconditional10-point
required-set deficit. Canonical case-record SHA256:
`3184eca8d3512c86ead0d677b0e96299514c12010edffd2fe7a1f6ee55fc8d0f`.

`validation.json` records the successful normal/optimized runs; `manifest.json`
records source bytes. Full gain arrays are regenerated in memory and deliberately
omitted. No proof corpus, ledger, credentials or private checkpoint is needed.
