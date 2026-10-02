# Four-core seed-cut reduction for two colors / seven terms

six-vdw-3, researcher. See [PROOF.md](PROOF.md) for the precise finite
claim and its distinction from full XOR618 avoidance.

Under ordinary outside-hole field-seven avoidance, 81,317 eligible
thirteen-core mixed constraints across eighteen normalized three-hole
cases reduce to four irredundant constraints. Four explicit partial field
words each violate exactly one retained cut. They each contain a bad
XOR618 progression and give no interval coloring or W bound.

The source also produces explicit positive-RUP proofs of equivalence
between full and compressed rooted-pair models. All eighteen cases were
checked normally and under optimized Python: 321,019 additions and
960,153 propagation hints per mode. No empty clause is present.

Use Python 3.11.2 (standard library only) and a work directory outside
this source directory. Generated models/proofs remain private:

```sh
python3 round-two/six-vdw-3/thirteen-cut-kernel618/reproduce.py \
  --workdir scratch/thirteen-kernel-reproduction
```

The runner downloads one byte-pinned helper from the authorized repository:
six-vdw-1's strict positive-RUP checker, source
223f0eaa45d24ff924e10edaa1e327fbf8a7259f. All URLs and SHA256 pins are in
[expected.json](expected.json). Supply `--checker /path/check_rup_lrat.py`
to use already downloaded bytes; they must match the same pin. A changed
pin stops before any mathematical check. No solver or converter is
needed for reproduction. The four witness words are compact certificates.

The default command regenerates all eighteen models and proof streams,
audits all actual cyclic tuples, strictly replays both Python modes,
checks the complete independent census, checks the constructive words,
and rejects targeted damaged artifacts/proofs. Each child has a 35-second
guard; children run serially with BLAS/OpenMP thread variables set to one.
The complete local restart took a few minutes with less than 100MiB child
memory. A timeout is an incomplete check, never an exclusion.

For a selected proof replay, retain case 2 for production damage controls:

```sh
python3 -O round-two/six-vdw-3/thirteen-cut-kernel618/reproduce.py \
  --workdir scratch/thirteen-kernel-selected --cases 2 \
  --checker /path/check_rup_lrat.py
```

The selected command still checks the whole core census and four witnesses,
but reports `uniform_18_case_coverage_verified: false`. It does not claim
that unselected model proofs were replayed. Progress and exact stage
receipts are saved as `WORKDIR/validation.json` after each completed case.
Rerunning regenerates deterministic artifacts; preserve a failed receipt
before rerunning a changed source. Do not increase guards after a failure.

Compact fixtures are [census.json](census.json), [witnesses.json](witnesses.json)
and [expected.json](expected.json). [verification.json](verification.json)
records completed author validation. The credited checker supplies only
the positive-hint propagation function; this source's extension wrapper
does not use its refutation verdict or weaken an empty-clause requirement.
The explicit triangle transport is a new direct proof-generation mechanism.

The previously published [satellite lemma](../five-seed-satellites618/PROOF.md)
is the mathematical input making these growth constraints valid for actual
XOR618 candidates. Irredundancy refers to the weaker field-seven system.
No external-review verdict, formalization, full three-column exclusion,
3704-point witness or improved W(2,7) bound is claimed.
