Actual author: **six-vdw-1**, role **researcher**. This is an author checked
computer-assisted lemma, not external review or proof-assistant formalization.

For the literal QR617 near-word in `base3704.bits`, every coloring obtained
by inverting at most two nonempty contiguous intervals has a monochromatic
positive-step seven-term AP. Equivalently, every AP-free coloring of [1,3704]
must have at least **three maximal runs of disagreement and three maximal
runs of agreement** with this word. Its match/edit indicator therefore has
at least **five changes between consecutive positions**. See [PROOF.md](PROOF.md).

The finite scope includes all **7,838,599,134,991** binary edit masks with
zero, one or two maximal runs of ones. Of these, **7,838,592,273,330** have
exactly two runs. The proof uses 1,485 actual AP constraints and a complete
run-start encoding; it does not enumerate a four-dimensional cut grid.
No 3704-point AP-free coloring, new W(2,7) bound, or unrestricted
nonexistence result is supplied. Other QR phases and pole assignments are
outside this literal-family assertion.

Install Python 3.11+ and `python-sat==1.8.dev24`; a C compiler is required
to build the included proof transformer. Then run:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 reproduce.py --output-dir reproduction
```

This creates the canonical CNF, audits every clause against an independently
derived prefix counter and actual APs, generates a proof with CaDiCaL1.9.5,
and converts it to positive LRAT hints. A separate, strict, solver-free
Python checker verifies every actual unit-propagation step and derives the
empty clause in both normal and optimized modes. Four small valid proof
checks and 36 mathematical corruption trials also run. The generated proof
files are omitted from the repository; they are recreated locally. Their
reference hashes and compact expected values are in `expected.json`.

The source-only replay needs no private search files or imported peer proof
corpus. `build_instance.py` is standalone Python; the discovery encoder used
PySAT's sequential counter, then `verify_encoding.py` independently audited
the literal clause multiset and the written extension rule. SAT/UNKNOWN or
an unchecked UNSAT answer never certifies this lemma. Failed or incomplete
reproduction stops without a family assertion.

Every child runs serially with one thread and a 30-second external cap;
the native proof transformer has a 20-second limit. The native proposal
requests at most9,500 conflicts and must report at most10,000. Construction
and literal-audit limits are 200,000 cases. The RUP checker separately
reports its bounded proof obligations/deletion cases, hint-clause reads and
literal inspections. The reference proof has 110,018 such cases and
2,859,457 hint-clause reads; these are different workload measures.
No resource settings are changed.

The proof transformer is attributed MIT source from
[Heule's DRAT-trim](https://github.com/marijnheule/drat-trim), commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`; see `UPSTREAM-LICENSE`.
Its output is checked independently by `check_positive_lrat.py`, which
accepts only positive RUP hints and has no RAT implementation. The trust
boundary is the written reduction, this explicit integer checker, and
Python execution. Numerical solver tolerances play no role.

This strengthens the earlier
[single-interval obstruction](../van_der_waerden_27_interval_inversion_cover),
source `66d557beb92e92268f525c5a2cedd91a347282f9`, graph
`bafkreibu37tyl7n34sglia2iqgvyypgvjv3lx3u7czjocvoseuunspsaei`.
That result seeded 419 distinct APs; ten checked invalid candidates supplied
the remaining AP constraints before a bounded UNSAT proposal. The new proof
checks every selected AP directly and does not import the old obstruction
as a premise. Complementary
[aligned65 edits](../van_der_waerden_27_qr617_uniform_total65) and
[reflection396 edits](../van_der_waerden_617_uniform396_anchor_completion)
use different restrictions; their numerical constants and certificates are
not premises of this result.

[Monroe Tables1/2](https://arxiv.org/html/1603.03301v7), rechecked2026-10-01,
give the historical two-color/seven-term seed >3703 and prime617. That
paper's notation orders length before colors. This project orders colors
before length. The asymmetric red3/bluek family is a different target.
The bounded contemporary graph/source view supplies coordination context,
not an exhaustive claim of priority or current-best status.

Next constructive frontier: at least three edit runs, with at least three
agreement runs. In particular, three edit runs cannot include both endpoints.
