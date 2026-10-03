# Fixed prime-617 independent-phase construction boundary

Actual author: **six-vdw-1**, role **researcher**, 2026-10-03.

For three fixed character inputs rooted at 0,1,4 modulo617, every phase may
choose its own arbitrary 8-bit Boolean table. Every actual occurrence of
all three original roots remains independently free. The code proves that
AP7 avoidance forces every table to be a single character projection or
its complement by prefix length632. This reduces 2^48 regular assignments
to 6^6=46656 necessary assignments. A separate compact original integer-AP
certificate excludes the entire unrestricted table family at length3704.
An independently checked historical length3703 coloring shows that the
family's maximum prefix length is exactly3703.

See [PROOF.md](PROOF.md) for definitions, implications and comparison.
These statements supply no unrestricted van der Waerden upper bound and
no improvement of its numerical lower bound. The six projection choices
per phase do not guarantee avoidance of mixed-phase progressions.

Run from the repository root with standard-library Python3.11 or later:

```sh
python3 round-two/six-vdw-1/finite-pattern-phase617/reproduce.py --output /tmp/finite617-fresh-check.json
```

The output path must be new. The runner checks all source/evidence pins,
then checks six complete mathematical/control records in normal and -O
modes, using twelve serial children, six numerical thread variables set
to1, and unchanged35-second child guards. Its completed output contains
every whole mathematical record, output hash, timing and peak child RSS.
The expected final status is
`EXACT_FIXED_PHASE617_PROJECTION632_AND_MAXIMUM3703_REPRODUCED`.
There are30 genuine semantic damage rejections per mode and genuine
positive coloring and proof controls. The primary validation used
CPython3.12.14 in the campaign's existing1CPU/2GiB scope.

Individual entry points:

- `check_rows.py` independently reconstructs all188700 same-phase APs,
  all182084 root-free ones, all256 truth tables in every phase, all1500
  nonprojection witnesses and every surviving projection's full domain.
- `check_kernel.py` independently rebuilds each of198 signed clauses from
  its literal original seven-point integer progression, then checks all39
  positive RUP proof additions and999 propagation hints.
- `check_seed.py` reconstructs the classical3703 word and its complement,
  checks all1140833 literal integer APs for each, and rejects two real
  endpoint/assignment damages. This positive control is prior art.
- `controls_rows.py`, `controls_kernel.py`, and `controls_rup.py` damage
  actual coordinates, field roots, phase variables, table coverage,
  signed clauses and proof semantics, requiring the intended rejections.

The only certificate inputs are compact literal APs and a4-KiB RUP proof.
`check_kernel.py` rebuilds the entire compact CNF from original APs;
`check_rows.py` independently rebuilds all canonical table witnesses.
The large experimental model and converter output are unnecessary for
the public proof. No SAT solver, converter, native library, private ledger,
key, campaign state, ancestor executable or large proof corpus is needed.
Ordinary Boolean implication, Gauss's lemma, the literal decoders, the
strict RUP kernel, Python and the operating system remain trust boundaries.
This is unformalized and no independent-person review is claimed.
