# The line-free maximum in F_5^3 is at most 71

**Exact computer-assisted theorem:** no 72-point subset of
\(\mathbb F_5^3\) avoids every complete affine line. Therefore

\[
70\le r_5(\mathbb F_5^3)\le71.
\]

A set of 71 points is not constructed or excluded here. The exact value
remains open in this work. Independent peer review is pending.

The [complete reduction](THEOREM.md) covers every possible candidate by
16,192 normalized quotient matrices in 4,332 affine classes. Two different
enumeration algorithms agree entry by entry. Every representative has a
checked UNSAT proof for a direct formula with just **125 variables**.
Fiber cardinalities are expressed by explicit subset clauses; there are
no auxiliary variables or cardinality-encoding library calls.

## Reproduce

Requires Python 3.10+, a C++20 compiler named `g++`, and
`python-sat==1.9.dev15`. Tested with Python 3.12.14 and GCC 12.2.0.
From this directory:

```sh
python3 -m pip install -r requirements.txt
python3 verify.py --out /tmp/upper71-verify
```

Expected status: `UPPER_BOUND71_REDUCTION_VERIFIED`, matching
[expected.json](expected.json). This command checks both enumerations,
the full affine partition, independent geometry and full-group controls,
all 160 fiber-cardinality truth assignments, the exact low-plane counting
dependency, both known 70-point controls, and every proof-input SHA256.
It does **not** regenerate the UNSAT proofs themselves.

Build the official [DRAT-trim](https://github.com/marijnheule/drat-trim)
checker, tested at source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, then run:

```sh
python3 replay.py --out /tmp/upper71-proofs --drat-trim /path/to/drat-trim
```

This regenerates all 4,332 proofs and checks each in a separate DRAT-trim
process. A successful checker must exit zero and report `s VERIFIED`.
UNKNOWN, SAT, a mismatched input or a failed proof check stops the run.
A SAT model is saved and checked directly against all affine lines and
fiber weights. A conflict limit is never treated as an exclusion.

The complete order is the order of [orbits.json](orbits.json): indices
0–163 have canonical type AA, 164–1415 type AB, and 1416–4331 type BB.
To use two workers, choose separate output directories and disjoint
intervals `--start 0 --stop 2166` and `--start 2166 --stop 4332`.
Both complete intervals are required. Per-case JSONs support restarting
an explicitly chosen interval after interruption; partial runs are marked
incomplete. The default conflict limit is 500,000 per case.

## Compact evidence and trust boundary

[certificates.csv](certificates.csv) has one row for every checked proof:
`index,cnf_sha256,proof_sha256,proof_bytes`. Each row represents an actual
UNSAT trace accepted by DRAT-trim. [validation.json](validation.json)
records complete coverage, production resources, independent checks and
versions. [SHA256SUMS](SHA256SUMS) covers the published source and evidence.
The 4,332 original binary traces totaled 617,263,694 bytes. Their cumulative
solver-and-checker time was about 965 seconds on the author run; replay
time depends on hardware and concurrent load. The hardest case used
18,339 conflicts, well below the 500,000 limit.

The small public pipeline control exercises the first and last case, both
type boundaries, and the hardest case. It also requires an UNKNOWN run
and an empty proof to be rejected:

```sh
python3 pipeline_controls.py --out /tmp/upper71-controls --drat-trim /path/to/drat-trim
```

Raw formulas, traces, checker logs and execution checkpoints stay outside
Git. They are reproducible from this source. Proof bytes may vary across
solver builds; acceptance requires a valid proof against the matching
input, not matching a search history. The runner flushes the native binary
proof stream before copying it: this avoids the pinned PySAT version's
`get_proof()` buffering and text-decoder problems.

The only prior mathematical result needed by the new exclusion is the
exact bound \(a_8+a_9\ge5\) from
[the global low-plane counting package](../low_planes72/README.md),
together with its planar bound 16. The verifier replays its ordinary
integer certificate and enumeration. [dependencies.json](dependencies.json)
pins all imported source and control files by hash; the low-plane child
interpreter ignores Python environment flags so its assertions remain
enabled. The remainder of the proof here
covers **all** AA/AB/BB quotient classes directly. It does not require the
earlier [AA](../two_eight_planes72/README.md) or
[AB](../no_eight_planes72/README.md) solver proofs, or the
[weighted/frame strengthening](../nine_plane_frame72/README.md).
Those results remain useful independent checkpoints and informed this
consolidated route.

The trust boundary is the written reduction, ordinary exact enumeration
and canonicalization code, the small direct CNF generator, the cited
integer counting certificate and DRAT-trim. A solver verdict alone is not
accepted. This is not a proof-assistant formalization and no independent
peer review is claimed.

## Sources and coordination

The principal literature source is Elsholtz et al.,
[*Maximal line-free sets in* \(\mathbb F_p^n\)](https://arxiv.org/abs/2310.03382v2),
Periodica Mathematica Hungarica 90 (2025), 7–21,
[DOI](https://doi.org/10.1007/s10998-024-00617-x). Its 70-point construction
is the lower-bound control. A second 70-point control comes from
researcher 4's [odd-symmetry theorem](../odd_symmetry/README.md).
Neither control is presented as a new construction here.

Researcher 1's [four-collinear-normal theorem](../four_collinear_nine_planes72/README.md),
researcher 3's [quadratic moment theorem](../quadratic_moments72/README.md),
and researcher 4's exclusion of odd-order affine symmetries were inspected
before publication. The first two give further restrictions at 72 but
are not dependencies of this complete lifting exclusion. The independent
[AA review](../two_eight_planes72_review1/REVIEW.md) also used a direct
point-variable encoding, supporting the simplification made here; that
review does not cover this new 4,332-case proof.
No symmetry is imposed on the lift: a symmetric quotient does not imply
a symmetric point set. Relevant teammate reports, commits and graph
feedback were refreshed before publication. A bounded primary-source
search found no matching exclusion; no historical priority claim is made.

The previous [upper bound 72](../upper_bound72.md) is superseded by this
numerical result but is not a proof premise: any set larger than 71
would contain a 72-subset, which the complete certificate cover excludes.
