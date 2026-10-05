# Elementary-kernel cyclic-subgroup counts

Local research lane authored by Rowan / studio-researcher-4 for the
2026-10-05 Colloquium. The shared target is the prove-or-refute
nonsolvable eta<=6 classification; this package establishes only the
extension lemma and a specialization conditional on the proposed
quotient family. Nova / studio-researcher-3 has internally checked the
fixed proof and independently reproduced all 22 fixture mathematical
outputs; the accepted scope is recorded in
[his report](internal_checks/nova_v1/REPORT.md). Historical novelty
remains unclaimed. This is an internal check, with the computational
trust boundaries stated below.

`PROOF.md` gives an exact formula, a lower bound and equality conditions
for an arbitrary elementary abelian normal kernel V=(F_p)^d. The full
extension need not split and the quotient may contain p-elements.
An affine norm calculation identifies the exact defect. The persistent
prime specialization excludes 2,3,5 and isolates a central rank-one
eta=6 boundary for p>=7 under the stated quotient hypothesis.

`verify.py` uses only the Python standard library. The reference run used
Python3.12.14, one process, exact integers and `Fraction`; no mathematical
comparison uses floating point. From this directory run:

```sh
python3 verify.py --check
```

Expected: `FINITE_CONTROLS_PASS`, 22 fixtures, complete entrywise agreement
with `EXPECTED.json`, and rejection of three malformed extension controls.
The author replay took1.575s and used21,716KiB maximum resident memory
on the campaign Linux VM. Resource measurements are descriptive, not proof.

The fixtures include central cyclic towers, split and nonsplit rank-one
extensions, the characteristic-two action exception, odd-characteristic
action defect, nonfaithful and unipotent actions, Heisenberg groups, the
central SL(2,5) extension and the attained A5 x C49 boundary. For each
fixture the program compares literal cyclic-subgroup sets and literal
orders against affine norm solutions, per quotient coset, then checks
both defect terms and the exact equality conditions. It derives the action
from conjugation rather than trusting a supplied fixed-space dimension.
Projection identities are checked on all generator edges; the declared
generators are checked to generate the entire explicitly constructed group.
The standard group constructions supply associativity; the checker does
not exhaust all multiplication triples.

The output includes canonical subgroup-set and full coset-entry hashes.
Complete per-coset records can be regenerated, and individual fixtures
can be explored, without publishing bulky certificates:

```sh
python3 verify.py --certificate /tmp/extension-cosets.json
python3 verify.py --only SL2_F5_central_C2
```

Nova's independent checker uses GAP-native permutation, polycyclic and
matrix groups. It imports neither the author implementation nor its
norm matrices. It checks the affine identity in every coset, reproduces
both full histograms and all representation-invariant fixture fields,
and adds four changed inputs and three malformed-data guards. Coordinate
digests are representation-dependent and are not compared. GAP's group
constructors and arithmetic remain trust boundaries; the universal proof
is separate from these finite controls. The eight check files are copied
unchanged from Nova's accepted package.

With GAP 4.12.1, SmallGrp 1.5.1 and Python 3.12, run from
`internal_checks/nova_v1`:

```sh
gap -A -b -q -m 64m -o 512m --quitonbreak check_extensions.g
python3 compare_expected.py
```

Expected: `ALL_22_MATHEMATICAL_OUTPUTS_MATCH`, four changed inputs and
three rejection controls. Running only the Python comparison checks the
stored independent output, rather than recomputing GAP groups.
`SOURCES.md` credits the graph and primary literature.

The explicit source-publication allowlist is `PUBLICATION_FILES.txt`.
It contains the compact core source/evidence and Nova's accepted internal
check. The later modular-family and minimal-normal-kernel supplements
have separate checking assignments and are excluded from this list.

Central-extension identification, the radical-free base and the integrated
induction are separate tasks. The fixtures support the proof, and do not
enumerate all extensions. Existing coprime formulas and eta=4 results are
prior art. This package is supporting source for those separate tasks;
it does not establish the full nonsolvable classification.
