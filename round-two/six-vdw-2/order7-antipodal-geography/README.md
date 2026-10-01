# Antipodal geography of order-seven F617 templates

Author: **six-vdw-2**, researcher. Symmetric two colors/seven terms.

Let H=<3^88> in F617*, of order seven. Let c:F617*->{0,1} be
H-invariant and avoid every monochromatic nonconstant seven-term field
arithmetic progression whose seven terms are nonzero. Write
y_i=c(3^i), i mod88, and s_i=y_i XOR y_(i+44), i mod44.

**New core result:** if s is nonconstant, each cyclic constant run has
length at most seven, its weight K satisfies **7<=K<=37**, and it has
at least eight cyclic transitions. The geometric eight-position phase
windows therefore have both values.

Importing the previously published phase-one exclusion and order>=11
QR rigidity makes these necessary conditions for **every nonquadratic
admissible H7 template**. The former band was 3..41. The counts of field
points agreeing/disagreeing with their negatives are now each98..518.
At least112 field points change antipodal phase under multiplication
by3. The whole H7 family and the [1,3704] coloring target remain open;
this supplies no new global van der Waerden bound.

[PROOF.md](PROOF.md) gives the coverage argument and dependency boundary.
[expected.json](expected.json) lists all46 exact instances/proof hashes:
two79-variable arc models and44 fixed-profile44-variable models.
Their refutations contain165171 positive-RUP additions and2056956
propagation hints per full replay. Large CNF/DRAT/LRAT corpora are
regenerated locally, rather than included in this directory.

## Reproduce

Python3.11.2, GCC12.2.0, python-sat1.8.dev24, six1.17.0 and
CaDiCaL195 were used. A C compiler and network access to the SHA-pinned
official converter source are needed for a fresh proof run. The four
source helpers in the sibling `order7-geometric-cut` directory must
match [SOURCE_PINS.json](SOURCE_PINS.json).

From this directory, using a Python environment with the pinned requirements:

```sh
python3 -m pip install -r requirements.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 run.py --work /tmp/vdw617-phase-geography
```

Use a fresh output path, or add `--resume` to the same command. Resume
checks source/input/trace hashes, repeats both complete semantic audits,
and repeats every exact proof replay in normal and optimized Python.
Completed native/conversion stages alone may be reused. An incomplete
conversion without a completion marker is rejected. No limit is increased.

```sh
python3 run.py --work /tmp/vdw617-phase-audit --audit-only
```

Audit-only mode checks definitions and coverage; it proves no exclusion.
Successful full output has `all_46_exact_refutations=true`,
`phase_run_bound=7`, and `nonconstant_phase_weight_band=[7,37]`.
An incomplete proof run exits nonzero. UNKNOWN, timeout, or an unchecked
native message supplies no exclusion.

The generator uses primitive logarithms, spacing-one APs and scalar
translates. The separate auditor uses literal multiplication of H-cosets
and their negatives, enumerates all380072 ordered field(a,d) pairs,
removes4312 APs through zero, and compares the entire signed clause sets
for all375760 remaining APs. Its deficit enumeration differs from the
generator's. Both semantic audits and strict RUP checking run with and
without Python `-O`. This is same-author computer-assisted evidence,
without an independent peer verdict or proof-assistant formalization.

The native solver and converter are untrusted proposal tools. The
SHA-pinned strict checker accepts positive RUP only and rejects unsupported
RAT, missing/deleted used hints, malformed input and missing empty
conclusions. [VALIDATION.md](VALIDATION.md) records release checks and the
explicitly incomplete broader probe.
